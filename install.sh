#!/bin/bash

# YellowBoxPhish Installation Script
# Author: Ian Carter Kulani
# Version: 2.0.0

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║${CYAN}          🐠 YELLOW_BOX_PHISH v2.0.0 - INSTALLATION        ${YELLOW}║${NC}"
echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
OS="$(uname -s)"
echo -e "${BLUE}🔍 Detected OS: ${OS}${NC}"

# Check Python version
echo -e "${BLUE}🐍 Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"
    
    if [ "$(echo $PYTHON_VERSION | cut -d. -f1)" -lt 3 ] || ([ "$(echo $PYTHON_VERSION | cut -d. -f1)" -eq 3 ] && [ "$(echo $PYTHON_VERSION | cut -d. -f2)" -lt 7 ]); then
        echo -e "${RED}❌ Python 3.7+ required${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo -e "${YELLOW}📦 Installing Python...${NC}"
    if [ "$OS" = "Linux" ]; then
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y python3 python3-pip python3-venv
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v apk &> /dev/null; then
            sudo apk add python3 py3-pip
        fi
    elif [ "$OS" = "Darwin" ]; then
        if command -v brew &> /dev/null; then
            brew install python3
        else
            echo -e "${RED}❌ Please install Python 3.7+ manually${NC}"
            exit 1
        fi
    fi
fi

# Install system dependencies
echo -e "${BLUE}📦 Installing system dependencies...${NC}"
if [ "$OS" = "Linux" ]; then
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y nmap curl dig traceroute openssh-client nikto \
            build-essential libffi-dev libssl-dev chromium-browser \
            chromium-chromedriver tcpdump net-tools iptables
    elif command -v yum &> /dev/null; then
        sudo yum install -y nmap curl bind-utils traceroute openssh-clients nikto \
            gcc libffi-devel openssl-devel chromium chromium-driver \
            tcpdump net-tools iptables
    elif command -v apk &> /dev/null; then
        sudo apk add nmap curl dig traceroute openssh-client nikto \
            build-base libffi-dev openssl-dev chromium chromium-chromedriver \
            tcpdump net-tools iproute2 iptables
    fi
elif [ "$OS" = "Darwin" ]; then
    if command -v brew &> /dev/null; then
        brew install nmap curl traceroute openssh nikto chromium
    else
        echo -e "${YELLOW}⚠️ Install Homebrew: https://brew.sh/${NC}"
    fi
fi

# Create virtual environment
echo -e "${BLUE}🐍 Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p .yellow_box_phish reports logs config data
mkdir -p .yellow_box_phish/{payloads,workspaces,scans,nikto_results,whatsapp_session}
mkdir -p .yellow_box_phish/{phishing_pages,traffic_logs,phishing_templates,captured_credentials}
mkdir -p .yellow_box_phish/{ssh_keys,ssh_logs,time_history,wordlists,custom_phishing,signal_session,web_ui,webhooks}

# Setup permissions
echo -e "${BLUE}🔐 Setting permissions...${NC}"
chmod +x yellow_box_phish.py test_commands.py requirements_check.py

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file${NC}"
fi

echo -e ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${YELLOW}          ✅ INSTALLATION COMPLETE!                        ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e ""
echo -e "${CYAN}🚀 To start YellowBoxPhish:${NC}"
echo -e "  source venv/bin/activate"
echo -e "  python3 yellow_box_phish.py"
echo -e ""
echo -e "${CYAN}🌐 Web Interface:${NC}"
echo -e "  http://localhost:8080"
echo -e ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo -e "  README.md"
echo -e ""
echo -e "${YELLOW}💡 Type 'help' for commands, 'exit' to quit${NC}"