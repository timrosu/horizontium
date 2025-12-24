#!/bin/sh
# horizontium linux installer

echo "creating virtual environment"
python -m venv env

echo "entering environment"
source env/bin/activate
echo "installing requirements in environment"
pip install -r requirements.txt

echo "generating run script (run.sh)"
cat > run.sh << EOL
cd $(pwd)
source env/bin/activate
python main.py
EOL

echo "All done! You can copy run script to your desired location or link it to a shortcut."
