:: horizontium windows installer
@echo off

echo creating virtual environment
python -m venv env

echo entering environment
call env\Scripts\activate.bat
echo installing requirements in environment...
pip install -r requirements.txt

echo "generating run script (run.bat)"
(
echo @echo off
echo cd /d %%~dp0
echo call env\Scripts\activate.bat
echo python main.py
) > run.bat

echo "All done! You can copy run script to your desired location or link it to a shortcut."
