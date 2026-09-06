@echo off

REM Ensure virtual environment exists
IF NOT EXIST ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

echo Starting Discord Timer Bot...
python main.py
pause
