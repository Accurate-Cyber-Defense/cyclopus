#!/usr/bin/env python3
"""
CYCLOPUS - Requirements Checker
Verifies all dependencies are installed correctly
"""

import subprocess
import sys
import importlib
import os
import platform

REQUIRED_PACKAGES = [
    ('requests', 'requests'),
    ('dotenv', 'python-dotenv'),
    ('colorama', 'colorama'),
    ('psutil', 'psutil'),
    ('cryptography', 'cryptography'),
    ('paramiko', 'paramiko'),
    ('discord', 'discord.py'),
    ('telethon', 'telethon'),
    ('slack_sdk', 'slack-sdk'),
    ('flask', 'Flask'),
    ('flask_socketio', 'Flask-SocketIO'),
    ('flask_cors', 'Flask-CORS'),
    ('socketio', 'python-socketio'),
    ('scapy', 'scapy'),
    ('dns', 'dnspython'),
    ('whois', 'python-whois'),
    ('qrcode', 'qrcode'),
    ('pyshorteners', 'pyshorteners'),
    ('matplotlib', 'matplotlib'),
    ('seaborn', 'seaborn'),
    ('numpy', 'numpy'),
    ('reportlab', 'reportlab'),
    ('pynput', 'pynput'),
    ('selenium', 'selenium'),
    ('webdriver_manager', 'webdriver-manager'),
    ('pyperclip', 'pyperclip'),
    ('pygetwindow', 'pygetwindow'),
    ('pyautogui', 'pyautogui'),
]

OPTIONAL_PACKAGES = [
    ('pyinstaller', 'pyinstaller'),
]

def check_package(import_name, pypi_name):
    """Check if a package is installed"""
    try:
        importlib.import_module(import_name)
        return True, f"✅ {pypi_name}"
    except ImportError:
        return False, f"❌ {pypi_name} (missing)"

def check_tool_windows(tool):
    """Check if a tool exists on Windows using where command"""
    try:
        # On Windows, use 'where' command
        result = subprocess.run(['where', tool], capture_output=True, shell=True)
        return result.returncode == 0
    except:
        return False

def check_tool_unix(tool):
    """Check if a tool exists on Unix using which command"""
    try:
        result = subprocess.run(['which', tool], capture_output=True)
        return result.returncode == 0
    except:
        return False

def check_tools():
    """Check for system tools"""
    tools = ['nmap', 'curl', 'wget', 'ping', 'ssh', 'docker', 'nikto', 'hashcat', 'nc', 'dig', 'traceroute']
    results = []
    
    # Detect OS
    is_windows = platform.system().lower() == 'windows'
    
    for tool in tools:
        try:
            if is_windows:
                found = check_tool_windows(tool)
            else:
                found = check_tool_unix(tool)
            
            if found:
                results.append(f"✅ {tool}")
            else:
                results.append(f"⚠️ {tool} (not found)")
        except Exception:
            results.append(f"⚠️ {tool} (check failed)")
    
    return results

def main():
    print("=" * 60)
    print("🐙 CYCLOPUS - Dependency Checker")
    print("=" * 60)
    
    print("\n📦 Python Version:")
    print(f"   {sys.version}")
    
    print("\n📦 Required Packages:")
    all_ok = True
    for import_name, pypi_name in REQUIRED_PACKAGES:
        ok, msg = check_package(import_name, pypi_name)
        print(f"   {msg}")
        if not ok:
            all_ok = False
    
    print("\n📦 Optional Packages:")
    for import_name, pypi_name in OPTIONAL_PACKAGES:
        ok, msg = check_package(import_name, pypi_name)
        print(f"   {msg}")
    
    print("\n🔧 System Tools:")
    for result in check_tools():
        print(f"   {result}")
    
    print("\n" + "=" * 60)
    
    if all_ok:
        print("✅ All required packages are installed!")
        print("\n💡 To install missing packages:")
        print("   pip install -r requirements.txt")
    else:
        print("❌ Some required packages are missing!")
        print("\n💡 To install all dependencies:")
        print("   pip install -r requirements.txt")
    
    # Show OS-specific installation instructions
    is_windows = platform.system().lower() == 'windows'
    
    if is_windows:
        print("\n💡 For Windows system tools (using Chocolatey):")
        print("   choco install nmap curl wget openssh docker-cli nikto hashcat netcat dnsutils traceroute")
        print("   Or download tools manually from their official websites")
    else:
        print("\n💡 For system tools (Ubuntu/Debian):")
        print("   sudo apt install nmap curl wget ssh docker.io nikto hashcat netcat-openbsd dnsutils traceroute")
        print("\n💡 For Arch Linux:")
        print("   sudo pacman -S nmap curl wget openssh docker nikto hashcat netcat dnsutils traceroute")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())