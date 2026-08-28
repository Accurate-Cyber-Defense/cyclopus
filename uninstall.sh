#!/bin/bash
# CYCLOPUS - Uninstall Script

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🐙 CYCLOPUS Uninstall Script${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

read -p "Are you sure you want to uninstall CYCLOPUS? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstall cancelled.${NC}"
    exit 0
fi

echo -e "${YELLOW}⚠️ Removing CYCLOPUS...${NC}"

# Deactivate virtual environment
deactivate 2>/dev/null || true

# Remove virtual environment
if [[ -d "venv" ]]; then
    echo -e "${BLUE}Removing virtual environment...${NC}"
    rm -rf venv
fi

# Remove configuration
if [[ -d ".cyclopus" ]]; then
    echo -e "${BLUE}Removing configuration...${NC}"
    rm -rf .cyclopus
fi

# Remove reports
if [[ -d "cyclopus_reports" ]]; then
    echo -e "${BLUE}Removing reports...${NC}"
    rm -rf cyclopus_reports
fi

# Remove logs
if [[ -d "logs" ]]; then
    echo -e "${BLUE}Removing logs...${NC}"
    rm -rf logs
fi

# Remove executable
if [[ -f "cyclopus-run" ]]; then
    echo -e "${BLUE}Removing executable...${NC}"
    rm -f cyclopus-run
fi

# Remove .env
if [[ -f ".env" ]]; then
    echo -e "${BLUE}Removing .env...${NC}"
    rm -f .env
fi

# Remove temp files
echo -e "${BLUE}Cleaning up...${NC}"
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf .mypy_cache
rm -rf *.pyc

echo -e "${GREEN}✅ CYCLOPUS uninstalled successfully!${NC}"