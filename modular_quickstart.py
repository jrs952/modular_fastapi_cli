#!/usr/bin/env python3


import click
import os
import shutil
from pathlib import Path

@click.group()
def modular_quickstart():
    """CLI tool to generate developer projects, plugins, and services."""
    pass

@modular_quickstart.command()
@click.argument('project_name')
def create_project(project_name):
    """Create a new developer project."""
    click.echo(f"Creating new project: {project_name}")
    project_dir = Path(project_name)
    if project_dir.exists():
        click.echo(f"Error: Directory '{project_name}' already exists.")
        return

    # Create project directories
    project_dir.mkdir()
    (project_dir / 'custom_plugins').mkdir()
    (project_dir / 'custom_services').mkdir()

    # Create main.py
    main_py = project_dir / 'main.py'
    main_py_content = f"""# main.py

from quickstart import app, initialize_app
from custom_plugins import my_custom_plugin
from custom_services import my_custom_service

# Define custom services (if any)
custom_services = {{
    "my_custom_service": lambda: my_custom_service.MyCustomService()
}}

# Initialize the app with custom plugins and services
initialize_app(custom_plugins=[my_custom_plugin], custom_services=custom_services)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""

    main_py.write_text(main_py_content)

    # Create __init__.py files
    (project_dir / 'custom_plugins' / '__init__.py').touch()
    (project_dir / 'custom_services' / '__init__.py').touch()

    # Create sample custom plugin
    sample_plugin = project_dir / 'custom_plugins' / 'my_custom_plugin.py'
    sample_plugin_content = """# custom_plugins/my_custom_plugin.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel

def setup_routes(service_container):
    router = APIRouter(
        prefix="/custom",
        tags=["Custom"]
    )

    class CustomResponse(BaseModel):
        message: str

    @router.get("/hello", response_model=CustomResponse)
    async def say_hello():
        return CustomResponse(message="Hello from custom plugin!")

    return router
"""
    sample_plugin.write_text(sample_plugin_content)

    # Create sample custom service
    sample_service = project_dir / 'custom_services' / 'my_custom_service.py'
    sample_service_content = """# custom_services/my_custom_service.py

class MyCustomService:
    def do_something(self):
        return "Custom service is working!"

def register_service(config_path=None):
    service_name = "my_custom_service"
    service_class = lambda: MyCustomService()
    return service_name, service_class
"""
    sample_service.write_text(sample_service_content)

    # Create requirements.txt
    requirements_txt = project_dir / 'requirements.txt'
    requirements_content = """quickstart
"""
    requirements_txt.write_text(requirements_content)

    click.echo(f"Project '{project_name}' created successfully.")

@modular_quickstart.command()
@click.argument('plugin_name')
def generate_plugin(plugin_name):
    """Generate a boilerplate plugin."""
    click.echo(f"Generating plugin: {plugin_name}")
    plugins_dir = Path('custom_plugins')
    if not plugins_dir.exists():
        click.echo("Error: 'custom_plugins' directory does not exist. Please run this command inside your project directory.")
        return

    plugin_file = plugins_dir / f"{plugin_name}.py"
    if plugin_file.exists():
        click.echo(f"Error: Plugin '{plugin_name}' already exists.")
        return

    plugin_content = f"""# custom_plugins/{plugin_name}.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel

def setup_routes(service_container):
    router = APIRouter(
        prefix="/{plugin_name}",
        tags=["{plugin_name.capitalize()}"]
    )

    class {plugin_name.capitalize()}Response(BaseModel):
        message: str

    @router.get("/hello", response_model={plugin_name.capitalize()}Response)
    async def say_hello():
        return {plugin_name.capitalize()}Response(message="Hello from {plugin_name} plugin!")

    return router
"""
    plugin_file.write_text(plugin_content)
    click.echo(f"Plugin '{plugin_name}' generated successfully in 'custom_plugins/{plugin_name}.py'.")

@modular_quickstart.command()
@click.argument('service_name')
def generate_service(service_name):
    """Generate a boilerplate service."""
    click.echo(f"Generating service: {service_name}")
    services_dir = Path('custom_services')
    if not services_dir.exists():
        click.echo("Error: 'custom_services' directory does not exist. Please run this command inside your project directory.")
        return

    service_file = services_dir / f"{service_name}.py"
    if service_file.exists():
        click.echo(f"Error: Service '{service_name}' already exists.")
        return

    service_content = f"""# custom_services/{service_name}.py

class {service_name.capitalize()}Service:
    def do_something(self):
        return "{service_name.capitalize()} service is working!"

def register_service(config_path=None):
    service_name = "{service_name}"
    service_class = lambda: {service_name.capitalize()}Service()
    return service_name, service_class
"""
    service_file.write_text(service_content)
    click.echo(f"Service '{service_name}' generated successfully in 'custom_services/{service_name}.py'.")

if __name__ == '__main__':
    modular_quickstart()
