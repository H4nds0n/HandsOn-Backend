# Setting Up the Python Virtual Environment and Managing Dependencies

## Introduction
Guide for setting up the python virtual environment 

## Steps

### 1. Creating and Activating the Virtual Environment
```bash
# Execute in the root folder of your project
python -m venv handson_pythonenv 

# Activating the virtual environment
# Windows
handson_pythonenv\Scripts\activate

# macOS and Linux
source handson_pythonenv/bin/activate

cd ./pyenv

# Install the dependencies
pip install -r requirements.txt

flask run

