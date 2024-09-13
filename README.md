# Toolbox

A collection of handy scripts, utilities, and configuration files for setting up and working on new workstations. This repository automates the installation of frequently used tools and provides scripts to simplify common tasks.

## Table of Contents
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

To set up your toolbox on a new workstation:

1. Clone the repository:

    ```bash
    git clone https://github.com/cloudartisan/toolbox.git
    cd toolbox
    ```

2. Run the installation script:

    ```bash
    ./install_toolbox.sh
    ```

This will:
- Symlink scripts from `bin/` to `$HOME/bin/`
- Symlink configuration files from `config/` to the home directory
- Install dependencies, if necessary
- Add `$HOME/bin` to your PATH

## Directory Structure

toolbox/
├── bin/                    # Executable scripts
├── lib/                    # Reusable libraries or modules
├── config/                 # Configuration files (dotfiles, etc.)
├── install.sh              # Installation script for new workstations
├── README.md               # This file
└── LICENSE                 # License for this repository

- **`bin/`**: Executable scripts to be symlinked to `$HOME/bin/` during installation for easy access.
- **`lib/`**: Shared libraries or reusable code used by the scripts in `bin/`.
- **`config/`**: Configuration files that will be symlinked to your home directory during installation.
- **`install.sh`**: Automates the setup process on new workstations.
  
## Usage

Once installed, all scripts in the `bin/` directory can be run from anywhere, as long as `$HOME/bin` is in your `PATH`.

### Example Usage

1. **Decode JWTs** with `dejwt.py`:

    ```bash
    echo "Bearer <JWT>" | dejwt.py
    ```

2. **Calculate a Falcon hash** with `fi_hash_36.py`:

    ```bash
    fi_hash_36.py aws-prod9-apnortheast1
    ```

## Configuration

The `config/` directory should contain configuration files depended upon ONLY by the toolbox (i.e., not vimrc, bashrc, no credentials, etc).

## Dependencies

Some scripts in the toolbox may require specific dependencies. The installation script will attempt to install these if they aren't already present.

### Example Dependencies:
- **Python 3**: Used by scripts like `dejwt.py`
- **Additional utilities**: Specified in the `install_toolbox.sh` script (e.g., `brew`, `apt`)

## License

This project is licensed under the [MIT License](LICENSE).
