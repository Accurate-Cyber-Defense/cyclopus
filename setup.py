#!/usr/bin/env python3
"""
CYCLOPUS - Setup Script
"""

from setuptools import setup, find_packages
import os
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="cyclopus",
    version="1.0.0",
    author="Ian Carter Kulani, MSc",
    author_email="ian@cyclopus.io",
    description="Ultimate Cybersecurity Command & Control Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iancarter/cyclopus",
    project_urls={
        "Bug Reports": "https://github.com/iancarter/cyclopus/issues",
        "Source": "https://github.com/iancarter/cyclopus",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Security Researchers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "tox>=4.0.0",
        ],
        "docker": [
            "docker>=6.0.0",
        ],
        "gui": [
            "tk",
            "PyQt5",
        ],
    },
    entry_points={
        "console_scripts": [
            "cyclopus=cyclopus:main",
            "cyclopus-check=requirements-check:main",
        ],
    },
    scripts=[
        "install.sh",
        "uninstall.sh",
    ],
    package_data={
        "cyclopus": [
            "*.txt",
            "*.md",
            "*.yml",
            "*.yaml",
            "config/*.json",
            "templates/*.html",
            "assets/*",
        ],
    },
    zip_safe=False,
)