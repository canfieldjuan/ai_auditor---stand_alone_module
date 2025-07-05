@echo off
echo 🚀 Setting up AI SEO Auditor environment...
echo.

echo 📁 Checking virtual environment...
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Creating new virtual environment...
    python -m venv venv
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate

echo 📦 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🧪 To test the integration:
echo    python app_integrated_test.py
echo.
echo 🌐 Then visit: http://localhost:5001
echo.
pause
