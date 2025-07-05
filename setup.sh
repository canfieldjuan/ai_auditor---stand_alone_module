#!/bin/bash
# setup.sh - Git Bash compatible setup script

echo "🚀 Setting up AI SEO Auditor environment..."
echo ""

echo "📁 Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating new virtual environment..."
    python -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/Scripts/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🧪 To test the integration:"
echo "   python app_integrated_test.py"
echo ""
echo "🌐 Then visit: http://localhost:5001"
echo ""
echo "Press any key to continue..."
read -n 1 -s
