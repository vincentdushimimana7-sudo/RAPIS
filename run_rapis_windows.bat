@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer, then run this file again.
  pause
  exit /b 1
)
if not exist .venv (
  python -m venv .venv
  if errorlevel 1 goto failed
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 goto failed
pip install -r requirements.txt
if errorlevel 1 goto failed
python scripts\validate_project.py
if errorlevel 1 goto failed
streamlit run app\streamlit_app.py
if errorlevel 1 goto failed
goto end
:failed
echo RAPIS setup or launch failed. Read the error above and check README.md.
pause
:end
endlocal
