#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Python and Pip
install_python_and_pip() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
            pip install --upgrade pip
        elif command_exists dnf; then
            sudo dnf install -y python3 python3-pip
            pip install --upgrade pip
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Check if Python is already installed
        if ! command_exists python; then
            echo "Please install Python from https://www.python.org/downloads/"
            exit 1
        fi
        if ! command_exists pip; then
            echo "Please install pip."
            exit 1
        fi
    fi
}

# Set up the virtual environment
setup_virtualenv() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        python -m venv venv
        source venv/Scripts/activate
    else
        python3 -m venv venv
        source venv/bin/activate
    fi
}

# Install pipenv
install_pipenv() {
    pip install --upgrade pip
    pip install pipenv
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

[requires]
python_version = "3.11"
EOF
    else
        echo "Pipfile already exists"
    fi
}

# Install dependencies
install_dependencies() {
    PIPENV_IGNORE_VIRTUALENVS=1 pipenv install --dev
    pipenv run
}

# Main function to coordinate setup
main() {
    install_python_and_pip
    setup_virtualenv
    install_pipenv
    create_pipfile
    install_dependencies
    echo "Environment setup complete. To activate the environment, run 'source venv/bin/activate' or 'venv\\Scripts\\activate' on Windows."
}

# Execute the main function
main
