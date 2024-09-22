#!/bin/bash

# Install the CLI script to the user's local bin and add it to PATH if necessary

# Set the target directory
LOCAL_BIN="$HOME/.local/bin"

# Ensure the local bin directory exists
mkdir -p "$LOCAL_BIN"

# Copy the cli.py script to the local bin directory with the desired name
cp modular_quickstart.py "$LOCAL_BIN/modular_quickstart"

# Make the script executable
chmod +x "$LOCAL_BIN/modular_quickstart"

# Check if the local bin directory is in the PATH
if ! echo "$PATH" | grep -q "$LOCAL_BIN"; then
    # Determine the user's shell
    SHELL_NAME=$(basename "$SHELL")
    if [ "$SHELL_NAME" = "bash" ]; then
        RC_FILE="$HOME/.bashrc"
    elif [ "$SHELL_NAME" = "zsh" ]; then
        RC_FILE="$HOME/.zshrc"
    else
        RC_FILE="$HOME/.profile"
    fi

    # Add the local bin directory to the PATH in the shell configuration file
    echo "" >> "$RC_FILE"
    echo "# Added by modular_quickstart installer" >> "$RC_FILE"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$RC_FILE"

    echo "Added $LOCAL_BIN to PATH in $RC_FILE."
    echo "Please restart your terminal or run 'source $RC_FILE' to update your PATH."
else
    echo "$LOCAL_BIN is already in your PATH."
fi

echo "CLI script installed as $LOCAL_BIN/modular_quickstart"
echo "You can now use the CLI commands without prefixing 'python'."
