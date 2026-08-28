#!/bin/bash
# CYCLOPUS - Bash Installation Script
# Supports Ubuntu/Debian, Arch Linux, macOS

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🐙 CYCLOPUS Installation Script${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Detect OS
OS=$(uname -s)
if [[ "$OS" == "Linux" ]]; then
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO=$ID
        echo -e "${GREEN}✅ Detected Linux: $DISTRO${NC}"
    else
        echo -e "${YELLOW}⚠️ Unknown Linux distribution${NC}"
        DISTRO="unknown"
    fi
elif [[ "$OS" == "Darwin" ]]; then
    DISTRO="macos"
    echo -e "${GREEN}✅ Detected macOS${NC}"
elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "CYGWIN"* ]]; then
    DISTRO="windows"
    echo -e "${GREEN}✅ Detected Windows (Git Bash)${NC}"
else
    echo -e "${RED}❌ Unsupported OS: $OS${NC}"
    exit 1
fi

# Check Python
echo -e "${BLUE}📦 Checking Python...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check pip
echo -e "${BLUE}📦 Checking pip...${NC}"
if command -v pip3 &>/dev/null; then
    echo -e "${GREEN}✅ pip found${NC}"
else
    echo -e "${YELLOW}⚠️ pip not found, installing...${NC}"
    python3 -m ensurepip --upgrade
fi

# Install system dependencies
echo -e "${BLUE}🔧 Installing system dependencies...${NC}"
case $DISTRO in
    ubuntu|debian)
        sudo apt update
        sudo apt install -y python3-pip python3-venv nmap curl wget ssh netcat-openbsd \
            dnsutils traceroute whois nikto hashcat docker.io docker-compose git make \
            build-essential libssl-dev libffi-dev
        ;;
    arch)
        sudo pacman -S --noconfirm python-pip nmap curl wget openssh netcat dnsutils \
            traceroute whois nikto hashcat docker docker-compose git make base-devel
        ;;
    fedora|centos|rhel)
        sudo dnf install -y python3-pip nmap curl wget openssh-clients netcat \
            bind-utils traceroute whois nikto hashcat docker git make gcc \
            openssl-devel libffi-devel python3-devel
        ;;
    macos)
        if ! command -v brew &>/dev/null; then
            echo -e "${YELLOW}⚠️ Homebrew not found, installing...${NC}"
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3 nmap curl wget openssh netcat dnsutils whois nikto hashcat docker git make
        ;;
    windows)
        echo -e "${YELLOW}⚠️ Please install system dependencies manually:${NC}"
        echo "   - Nmap: https://nmap.org/download.html"
        echo "   - Docker: https://www.docker.com/products/docker-desktop"
        echo "   - Git: https://git-scm.com/download/win"
        ;;
    *)
        echo -e "${YELLOW}⚠️ Please install dependencies manually:${NC}"
        echo "   - Python 3.8+"
        echo "   - pip"
        echo "   - nmap, curl, wget, ssh, netcat, dnsutils, traceroute, whois, nikto, hashcat, docker"
        ;;
esac

# Create virtual environment
echo -e "${BLUE}📦 Setting up Python virtual environment...${NC}"
if [[ "$DISTRO" != "windows" ]]; then
    python3 -m venv venv
    source venv/bin/activate
else
    python3 -m venv venv
    source venv/Scripts/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install additional optional packages
echo -e "${BLUE}📦 Installing optional packages...${NC}"
pip install pyperclip pygetwindow pyautogui

# Run requirements check
echo -e "${BLUE}🔍 Running dependency check...${NC}"
python3 requirements-check.py

# Create configuration directory
echo -e "${BLUE}📁 Creating configuration directories...${NC}"
mkdir -p .cyclopus
mkdir -p .cyclopus/payloads .cyclopus/workspaces .cyclopus/reports
mkdir -p .cyclopus/phishing_pages .cyclopus/captured_credentials .cyclopus/ssh_keys
mkdir -p .cyclopus/traffic_logs .cyclopus/nikto_results
mkdir -p .cyclopus/keylog_exfil .cyclopus/deployments .cyclopus/cracking
mkdir -p .cyclopus/arp_logs .cyclopus/mac_logs .cyclopus/nat_logs
mkdir -p .cyclopus/docker_scans .cyclopus/email_composer .cyclopus/pdf_reports
mkdir -p cyclopus_reports
mkdir -p logs

# Create .env file
if [[ ! -f .env ]]; then
    echo -e "${BLUE}📄 Creating .env file...${NC}"
    cp .env.example .env
fi

# Create executable script
echo -e "${BLUE}🔧 Creating executable...${NC}"
cat > cyclopus-run << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 cyclopus.py "$@"
EOF
chmod +x cyclopus-run

# Success message
echo ""
echo -e "${GREEN}✅ CYCLOPUS Installation Complete!${NC}"
echo -e "${CYAN}🐙 CYCLOPUS v1.0.0${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo -e "${GREEN}📁 Installation Directory: $(pwd)${NC}"
echo -e "${GREEN}🐍 Virtual Environment: $(pwd)/venv${NC}"
echo -e "${GREEN}📄 Configuration: $(pwd)/.cyclopus${NC}"
echo -e "${GREEN}📄 Reports: $(pwd)/cyclopus_reports${NC}"
echo -e "${GREEN}📄 Logs: $(pwd)/logs${NC}"
echo ""
echo -e "${YELLOW}🚀 To start CYCLOPUS:${NC}"
echo -e "   ${CYAN}./cyclopus-run${NC}"
echo -e "   ${CYAN}source venv/bin/activate && python3 cyclopus.py${NC}"
echo ""
echo -e "${YELLOW}🐳 To run with Docker:${NC}"
echo -e "   ${CYAN}docker-compose up -d${NC}"
echo ""
echo -e "${YELLOW}🔍 To check requirements:${NC}"
echo -e "   ${CYAN}python3 requirements-check.py${NC}"
echo ""
echo -e "${YELLOW}🧪 To run tests:${NC}"
echo -e "   ${CYAN}python3 commands-test.py${NC}"