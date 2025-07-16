#!/bin/bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Environment setup complete!"
deactivate
echo "You can activate the virtual environment with 'source venv/bin/activate'."
echo "To install dependencies, run 'pip install -r requirements.txt' again if needed."
echo "To exit the virtual environment, use 'deactivate'."
echo "Remember to activate the virtual environment before running your Python scripts."
echo "For more information, refer to the documentation."
echo "Happy coding! 🎉  "