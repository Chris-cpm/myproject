#!/bin/bash

# MindMate Project Setup Script
# Run this script to automatically set up and run the project

echo "🧠 MindMate Project Setup"
echo "=========================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Check if pip is installed
echo "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed. Please install pip.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"
echo ""

# Install/Check Jac
echo "Installing Jac language..."
pip3 install jaclang --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Jac language installed${NC}"
else
    echo -e "${YELLOW}⚠️  Jac installation had issues, but continuing...${NC}"
fi
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install streamlit requests pandas plotly --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All Python packages installed${NC}"
else
    echo -e "${RED}❌ Failed to install some packages${NC}"
    exit 1
fi
echo ""

# Create requirements.txt
echo "Creating requirements.txt..."
cat > requirements.txt << EOF
streamlit==1.31.0
requests==2.31.0
pandas==2.1.4
plotly==5.18.0
jaclang
EOF
echo -e "${GREEN}✅ requirements.txt created${NC}"
echo ""

# Check if backend file exists
if [ ! -f "mindmate_backend.jac" ]; then
    echo -e "${YELLOW}⚠️  mindmate_backend.jac not found${NC}"
    echo "Please save the corrected JAC backend code as 'mindmate_backend.jac'"
    echo ""
fi

# Check if frontend file exists
if [ ! -f "mindmate_frontend.py" ]; then
    echo -e "${YELLOW}⚠️  mindmate_frontend.py not found${NC}"
    echo "Please save the fixed frontend code as 'mindmate_frontend.py'"
    echo ""
fi

# Create README
echo "Creating README.md..."
cat > README.md << 'EOF'
# 🧠 MindMate - Mental Wellness Tracker

AI-powered mental wellness tracking application built with Jac and Streamlit.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run mindmate_frontend.py
```

## Features

- 📝 Mood entry tracking
- 🧠 AI-powered analysis
- 📊 Analytics dashboard
- 🎵 Music recommendations
- 💡 Personalized advice

## Usage

1. Login with any username
2. Describe your mood
3. Get instant analysis and recommendations
4. Track your mental wellness over time

## Crisis Support

⚠️ In crisis? Contact:
- 911 (US National Suicide Prevention Lifeline)
- Text HELLO to 0717734206 (Crisis Text Line)

## License

For wellness tracking only. Not a substitute for professional mental health care.
EOF
echo -e "${GREEN}✅ README.md created${NC}"
echo ""

# Summary
echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Ensure 'mindmate_backend.jac' exists in this directory"
echo "2. Ensure 'mindmate_frontend.py' exists in this directory"
echo "3. Run the application:"
echo ""
echo -e "   ${GREEN}streamlit run mindmate_frontend.py${NC}"
echo ""
echo "4. Browser will open at http://localhost:8501"
echo ""
echo "Need help? Check README.md for full documentation"
echo ""