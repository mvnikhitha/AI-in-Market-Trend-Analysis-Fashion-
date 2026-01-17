#!/bin/bash

# Kalainayam Development Start Script

echo "🎨 Kalainayam — Fashion Intelligence Platform"
echo "============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "backend/app.py" ]; then
    echo -e "${RED}Error: Please run this script from the Kalainayam root directory${NC}"
    exit 1
fi

# Start backend
echo -e "${YELLOW}Starting backend server...${NC}"
cd backend

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1

# Start Flask server
echo -e "${GREEN}Backend running on http://localhost:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
python app.py &
BACKEND_PID=$!

# Go back to root
cd ..

# Start frontend server
echo ""
echo -e "${YELLOW}Starting frontend server...${NC}"
cd frontend

# Check if Python http.server is available
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}Frontend running on http://localhost:8000${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    python3 -m http.server 8000
else
    echo -e "${RED}Error: Python 3 not found${NC}"
    kill $BACKEND_PID
    exit 1
fi
