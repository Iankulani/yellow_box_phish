#!/usr/bin/env python3
"""
Setup script for YellowBoxPhish
"""

from setuptools import setup, find_packages
import os
import re

with open("yellow_box_phish.py", "r") as f:
    content = f.read()
    version_match = re.search(r'v(\d+\.\d+\.\d+)', content)
    version = version_match.group(1) if version_match else "2.0.0"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="yellow-box-phish",
    version=version,
    author="Ian Carter Kulani",
    description="Multi-Platform Phishing & Command Center",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iancarterkulani/yellow-box-phish",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.6",
        "cryptography>=41.0.7",
        "requests>=2.31.0",
        "psutil>=5.9.6",
        "Flask>=3.0.0",
        "flask-socketio>=5.3.4",
        "python-socketio>=5.10.0",
        "eventlet>=0.33.3",
        "paramiko>=3.3.1",
        "scapy>=2.5.0",
        "python-whois>=0.8.0",
        "netaddr>=0.9.0",
        "qrcode>=7.4.2",
        "pyshorteners>=1.0.1",
        "discord.py>=2.3.2",
        "telethon>=1.34.0",
        "slack-sdk>=3.26.2",
        "selenium>=4.15.2",
        "webdriver-manager>=4.0.1",
        "sqlite3-utils>=3.36.0",
        "dataclasses-json>=0.5.14",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "click>=8.1.7",
        "tabulate>=0.9.0",
        "rich>=13.7.0",
        "tqdm>=4.66.1",
        "schedule>=1.2.0",
        "jinja2>=3.1.2",
        "markdown>=3.5.1",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "bandit>=1.7.0",
        ],
        "docker": [
            "docker>=6.0.0",
        ],
        "all": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "bandit>=1.7.0",
            "docker>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yellowbox=yellow_box_phish:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)