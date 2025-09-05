# Virtual Environment Activation Script for PowerShell
Write-Host "Activating Python virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "To deactivate, run: deactivate" -ForegroundColor Yellow
Write-Host "To run tests, run: python run_tests.py" -ForegroundColor Yellow
Write-Host "To test SDK import, run: python -c \"import sys; sys.path.insert(0, 'src'); from rocketreach.sdk import RocketReachClient; print('SDK imported successfully!')\"" -ForegroundColor Yellow
