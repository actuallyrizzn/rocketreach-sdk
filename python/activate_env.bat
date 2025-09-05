@echo off
REM Virtual Environment Activation Script for Windows
echo Activating Python virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!
echo.
echo To deactivate, run: deactivate
echo To run tests, run: python run_tests.py
echo To run basic test, run: python -c "import sys; sys.path.insert(0, 'src'); from rocketreach.sdk import RocketReachClient; print('SDK imported successfully!')"
