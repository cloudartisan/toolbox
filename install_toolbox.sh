#!/bin/bash

echo "Setting up toolbox..."

# Create the bin directory in $HOME if it doesn't already exist
if [ ! -d "$HOME/bin" ]; then
  echo "Creating $HOME/bin directory..."
  mkdir -p "$HOME/bin"
fi

# Symlink each script in the toolbox/bin directory to $HOME/bin
echo "Linking scripts to $HOME/bin..."
for script in $(ls bin/); do
  ln -sf "$(pwd)/bin/$script" "$HOME/bin/$script"
done

# Symlink configuration files from config/ to the home directory
echo "Linking configuration files..."
for config_file in $(ls config/); do
  ln -sf "$(pwd)/config/$config_file" "$HOME/.$config_file"
done

# Install necessary dependencies (add or remove as needed)
echo "Installing dependencies..."
if [ "$(uname)" == "Darwin" ]; then
  # MacOS-specific installations
  #brew install some_dependency
  :
elif [ "$(uname)" == "Linux" ]; then
  # Linux-specific installations
  #sudo apt update
  #sudo apt install -y some_dependency
	:
fi

# Set up environment variables (if necessary)
#if ! grep -q 'export PATH=$HOME/bin:$PATH' "$HOME/.bashrc"; then
  #echo 'export PATH=$HOME/bin:$PATH' >> "$HOME/.bashrc"
  #echo "Added $HOME/bin to PATH in .bashrc"
#fi

# Source .bashrc to apply changes
#source "$HOME/.bashrc"

# Completion message
echo "Toolbox setup complete!"
