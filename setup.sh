#!/bin/bash
echo "Setting up Veeresh AI Bot..."

# Create required directories
mkdir -p config logs user_memories

# Check for Python installation
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

echo "Setup completed successfully!"
echo "Run the bot using: python3 src/main.py"