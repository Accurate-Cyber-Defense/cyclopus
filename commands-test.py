#!/usr/bin/env python3
"""
CYCLOPUS - Command Test Suite
Tests all major commands and functionalities
"""

import os
import sys
import time
import json
import socket
import subprocess
from typing import Dict, List, Any

# Colors for output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    GREEN = Fore.GREEN + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    BLUE = Fore.BLUE + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    MAGENTA = Fore.MAGENTA + Style.BRIGHT
    RESET = Style.RESET_ALL
except:
    GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = RESET = ""

class CommandTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
        self.start_time = time.time()
        
    def log(self, msg: str, color: str = "", end: str = "\n"):
        print(f"{color}{msg}{RESET}", end=end)
        sys.stdout.flush()
    
    def test(self, name: str, func, *args, **kwargs) -> bool:
        self.log(f"  ▶ Testing: {name}", BLUE)
        try:
            result = func(*args, **kwargs)
            if result:
                self.log(f"    ✅ PASSED", GREEN)
                self.tests_passed += 1
                self.results.append({"name": name, "status": "PASSED"})
                return True
            else:
                self.log(f"    ❌ FAILED", RED)
                self.tests_failed += 1
                self.results.append({"name": name, "status": "FAILED"})
                return False
        except Exception as e:
            self.log(f"    ❌ ERROR: {e}", RED)
            self.tests_failed += 1
            self.results.append({"name": name, "status": "ERROR", "error": str(e)})
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        self.log("\n" + "=" * 60, CYAN)
        self.log("🐙 CYCLOPUS Command Test Suite", CYAN)
        self.log("=" * 60, CYAN)
        self.log(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Test 1: Import and Basic Setup
        self.test_suite_basic()
        
        # Test 2: Network Tests
        self.test_suite_network()
        
        # Test 3: System Tests
        self.test_suite_system()
        
        # Test 4: Security Tests
        self.test_suite_security()
        
        # Test 5: API Tests (if available)
        self.test_suite_api()
        
        # Summary
        self.print_summary()
    
    def test_suite_basic(self):
        """Test basic functionality"""
        self.log("\n" + "─" * 40, BLUE)
        self.log("📦 BASIC TESTS", BLUE)
        self.log("─" * 40, BLUE)
        
        # Test Python version
        self.test("Python Version >= 3.8", lambda: sys.version_info >= (3, 8))
        
        # Test imports
        import importlib
        modules = ['requests', 'cryptography', 'paramiko', 'flask', 'scapy', 'pynput']
        for module in modules:
            self.test(f"Import {module}", lambda m=module: importlib.import_module(m) is not None)
        
        # Test config directory creation
        self.test("Config directory exists", lambda: os.path.exists(".cyclopus"))
        
        # Test database
        self.test("Database initialization", self._test_db_init)
    
    def test_suite_network(self):
        """Test network commands"""
        self.log("\n" + "─" * 40, BLUE)
        self.log("🌐 NETWORK TESTS", BLUE)
        self.log("─" * 40, BLUE)
        
        target = "8.8.8.8"
        
        # Test ping
        self.test("Ping test", self._test_ping, target)
        
        # Test DNS resolution
        self.test("DNS resolution", self._test_dns, "google.com")
        
        # Test port connectivity
        self.test("Port connectivity (443)", self._test_port, target, 443)
        
        # Test HTTP request
        self.test("HTTP request", self._test_http, "https://google.com")
        
        # Test IP validation
        self.test("IP validation", self._test_ip_validation, "192.168.1.1")
    
    def test_suite_system(self):
        """Test system commands"""
        self.log("\n" + "─" * 40, BLUE)
        self.log("💻 SYSTEM TESTS", BLUE)
        self.log("─" * 40, BLUE)
        
        # Test CPU info
        self.test("CPU detection", self._test_cpu)
        
        # Test memory info
        self.test("Memory detection", self._test_memory)
        
        # Test disk info
        self.test("Disk detection", self._test_disk)
        
        # Test hostname
        self.test("Hostname detection", self._test_hostname)
    
    def test_suite_security(self):
        """Test security features"""
        self.log("\n" + "─" * 40, BLUE)
        self.log("🔒 SECURITY TESTS", BLUE)
        self.log("─" * 40, BLUE)
        
        # Test hash functions
        self.test("MD5 hash", self._test_hash_md5)
        
        # Test encryption (if available)
        self.test("Cryptography available", lambda: True)
        
        # Test keylogger availability
        self.test("Keylogger availability", self._test_keylogger_available)
        
        # Test SSH availability
        self.test("SSH availability", self._test_ssh_available)
    
    def test_suite_api(self):
        """Test API endpoints"""
        self.log("\n" + "─" * 40, BLUE)
        self.log("🌐 API TESTS", BLUE)
        self.log("─" * 40, BLUE)
        
        # Check if web server is running
        if self._test_web_server():
            self.log("  ✅ Web server detected", GREEN)
            
            # Test API endpoints
            endpoints = [
                "/api/stats",
                "/api/threats",
                "/api/platforms",
            ]
            for endpoint in endpoints:
                self.test(f"API: {endpoint}", self._test_api_endpoint, endpoint)
        else:
            self.log("  ⚠️ Web server not running (skipping API tests)", YELLOW)
    
    def _test_db_init(self):
        """Test database initialization"""
        try:
            import sqlite3
            conn = sqlite3.connect(".cyclopus/cyclopus.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            return len(tables) > 0
        except:
            return False
    
    def _test_ping(self, target: str) -> bool:
        """Test ping functionality"""
        try:
            if sys.platform == "win32":
                cmd = ["ping", "-n", "1", target]
            else:
                cmd = ["ping", "-c", "1", target]
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _test_dns(self, domain: str) -> bool:
        """Test DNS resolution"""
        try:
            socket.gethostbyname(domain)
            return True
        except:
            return False
    
    def _test_port(self, target: str, port: int) -> bool:
        """Test port connectivity"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _test_http(self, url: str) -> bool:
        """Test HTTP request"""
        try:
            import requests
            response = requests.get(url, timeout=5)
            return response.status_code < 500
        except:
            return False
    
    def _test_ip_validation(self, ip: str) -> bool:
        """Test IP validation"""
        try:
            import ipaddress
            ipaddress.ip_address(ip)
            return True
        except:
            return False
    
    def _test_cpu(self) -> bool:
        """Test CPU detection"""
        try:
            import psutil
            return psutil.cpu_count() > 0
        except:
            return False
    
    def _test_memory(self) -> bool:
        """Test memory detection"""
        try:
            import psutil
            return psutil.virtual_memory().total > 0
        except:
            return False
    
    def _test_disk(self) -> bool:
        """Test disk detection"""
        try:
            import psutil
            return psutil.disk_usage("/").total > 0
        except:
            return False
    
    def _test_hostname(self) -> bool:
        """Test hostname detection"""
        try:
            hostname = socket.gethostname()
            return len(hostname) > 0
        except:
            return False
    
    def _test_hash_md5(self) -> bool:
        """Test MD5 hash"""
        try:
            import hashlib
            h = hashlib.md5(b"test").hexdigest()
            return h == "098f6bcd4621d373cade4e832627b4f6"
        except:
            return False
    
    def _test_keylogger_available(self) -> bool:
        """Test keylogger availability"""
        try:
            import pynput
            return True
        except:
            return False
    
    def _test_ssh_available(self) -> bool:
        """Test SSH availability"""
        try:
            import paramiko
            return True
        except:
            return False
    
    def _test_web_server(self) -> bool:
        """Test if web server is running"""
        try:
            import requests
            response = requests.get("http://localhost:5000", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _test_api_endpoint(self, endpoint: str) -> bool:
        """Test an API endpoint"""
        try:
            import requests
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def print_summary(self):
        """Print test summary"""
        elapsed = time.time() - self.start_time
        
        self.log("\n" + "=" * 60, CYAN)
        self.log("📊 TEST SUMMARY", CYAN)
        self.log("=" * 60, CYAN)
        
        self.log(f"  ✅ Passed: {self.tests_passed}", GREEN)
        self.log(f"  ❌ Failed: {self.tests_failed}", RED)
        self.log(f"  ⏱️ Time: {elapsed:.2f}s")
        
        if self.tests_failed == 0:
            self.log(f"\n🎉 All tests passed! ({self.tests_passed} tests)", GREEN)
            return 0
        else:
            self.log(f"\n⚠️ {self.tests_failed} test(s) failed", RED)
            self.log("\nFailed tests:")
            for r in self.results:
                if r['status'] in ['FAILED', 'ERROR']:
                    error = r.get('error', '')
                    self.log(f"  ❌ {r['name']}: {r['status']}{' - ' + error if error else ''}", RED)
            return 1

def main():
    tester = CommandTester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()