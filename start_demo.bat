
@echo off
echo ====================================
echo Speech Health Demo - One Click Start
echo ====================================

REM Create virtual environment if needed
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate environment
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Warm up DEMUCS (optional but recommended)
echo Warming up DEMUCS model...
python -c "from enhancement.demucs_model import enhance; import numpy as np; enhance(np.zeros(16000),16000)"

REM Start server
echo Starting FastAPI server...
uvicorn app:app --host 127.0.0.1 --port 8000

pause
