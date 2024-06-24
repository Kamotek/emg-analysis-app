#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Python and Pip
install_python_and_pip() {
    if [[ "$(uname -s)" == "Linux" ]]; then
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command_exists dnf; then
            sudo dnf install -y python3 python3-pip
        fi
    elif [[ "$(uname -s)" == "CYGWIN"* || "$(uname -s)" == "MINGW"* ]]; then
        if ! command_exists python; then
            echo "Please install Python from https://www.python.org/downloads/"
            exit 1
        fi
        if ! command_exists pip; then
            echo "Please install pip."
            exit 1
        fi
    else
        echo "Unsupported OS. Please install Python and Pip manually."
        exit 1
    fi
    pip install --upgrade pip
}

# Set up the virtual environment
setup_virtualenv() {
    if [[ "$(uname -s)" == "CYGWIN"* || "$(uname -s)" == "MINGW"* ]]; then
        python -m venv venv
        if [ -f "venv/Scripts/Activate.ps1" ]; then
            echo "Use 'venv\\Scripts\\Activate.ps1' to activate on PowerShell."
        elif [ -f "venv/Scripts/activate" ]; then
            echo "Use 'source venv/Scripts/activate' to activate on CMD."
        fi
    else
        python3 -m venv venv
        echo "Use 'source venv/bin/activate' to activate."
    fi
}

# Install pipenv
install_pipenv() {
    pip install --upgrade pipenv
}

# Create Pipfile if it doesn't exist
create_pipfile() {
    if [ ! -f "Pipfile" ]; then
        echo "Creating Pipfile..."
        cat << EOF > Pipfile
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
pandas = "*"
PyYAML = "*"
PySide6 = "*"
bluepy = "*"
numpy = "*"
scipy = "*"
filterpy = "*"
scikit-learn = "*"
imbalanced-learn = "*"
pydrive = "*"
matplotlib = "*"
pytest = "*"

[requires]
python_version = "3.11"
EOF
    else
        echo "Pipfile already exists"
    fi
}

# Install dependencies
install_dependencies() {
    export PIPENV_IGNORE_VIRTUALENVS=1
    export PIPENV_VERBOSITY=-1
    pipenv install --dev
}

# Activate the virtual environment
activate() {
    if [[ "$(uname -s)" == "CYGWIN"* || "$(uname -s)" == "MINGW"* ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
        pipenv run -v sudo python main.py
    fi
}

# Main function to coordinate setup
main() {
    install_python_and_pip
    setup_virtualenv
    install_pipenv
    create_pipfile
    install_dependencies
    activate
    echo "Environment setup completed."
}

# Execute the main function
main
