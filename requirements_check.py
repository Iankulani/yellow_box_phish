#!/usr/bin/env python3
"""
Requirements Checker for YellowBoxPhish
Verifies all dependencies are installed
"""

import sys
import subprocess
import importlib
import shutil
import platform
from typing import List, Tuple, Dict, Optional

class DependencyChecker:
    """Check all dependencies"""
    
    def __init__(self):
        self.results = []
        self.optional = [
            'paramiko', 'scapy', 'discord', 'telethon', 'slack_sdk',
            'selenium', 'webdriver_manager', 'qrcode', 'pyshorteners',
            'flask', 'flask_socketio', 'whois'
        ]
        self.required = [
            'colorama', 'cryptography', 'requests', 'psutil',
            'sqlite3', 'json', 'time', 'socket', 'threading'
        ]
        # System tools that are optional but recommended
        self.system_tools = {
            'ping': 'Network connectivity testing',
            'nmap': 'Port scanning',
            'curl': 'HTTP requests',
            'dig': 'DNS lookups',
            'traceroute': 'Network path tracing',
            'ssh': 'SSH connections',
            'nikto': 'Web server scanning'
        }
        # Essential system tools
        self.essential_tools = ['python3', 'pip']
        
        self.os_type = platform.system()
    
    def check_python(self) -> bool:
        """Check Python version"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            self.results.append(('Python', True, f"{version.major}.{version.minor}.{version.micro}"))
            return True
        self.results.append(('Python', False, f"{version.major}.{version.minor}.{version.micro} (3.7+ required)"))
        return False
    
    def check_modules(self, modules: List[str], required: bool = True) -> bool:
        """Check Python modules"""
        all_ok = True
        for module in modules:
            try:
                # Handle modules with dots (e.g., flask_socketio)
                importlib.import_module(module)
                status = True
                version = "✓"
            except ImportError:
                status = False
                version = "✗"
                all_ok = False
            
            module_name = module.replace('_', ' ').title()
            self.results.append((module_name, status, version, required))
        
        return all_ok
    
    def check_system_tool(self, tool: str) -> Optional[str]:
        """Check if a system tool is available"""
        # Special handling for Windows
        if self.os_type == 'Windows':
            if tool == 'dig':
                # Check for nslookup as alternative on Windows
                return shutil.which('nslookup')
            elif tool == 'traceroute':
                # Check for tracert as alternative on Windows
                return shutil.which('tracert')
            elif tool == 'ssh':
                # Check for ssh in Windows
                return shutil.which('ssh')
        
        return shutil.which(tool)
    
    def check_system_tools(self) -> bool:
        """Check system tools"""
        all_ok = True
        
        # Check essential tools
        for tool in self.essential_tools:
            found = shutil.which(tool) is not None
            if not found:
                all_ok = False
            self.results.append((tool, found, "✓" if found else "✗", True))
        
        # Check optional system tools
        for tool, description in self.system_tools.items():
            found = self.check_system_tool(tool) is not None
            
            # Provide alternative names for clarity
            display_name = tool
            if self.os_type == 'Windows':
                if tool == 'dig':
                    display_name = 'dig (or nslookup)'
                elif tool == 'traceroute':
                    display_name = 'traceroute (or tracert)'
            
            # For nmap on Windows, check if it's in PATH
            if tool == 'nmap' and self.os_type == 'Windows':
                # Common nmap installation paths on Windows
                nmap_paths = [
                    r'C:\Program Files (x86)\Nmap\nmap.exe',
                    r'C:\Program Files\Nmap\nmap.exe'
                ]
                for path in nmap_paths:
                    if shutil.which(path) or shutil.which('nmap'):
                        found = True
                        break
            
            self.results.append((display_name, found, "✓" if found else "✗", False, description))
            if not found:
                all_ok = False
        
        return all_ok
    
    def check_installed_packages(self) -> Dict:
        """Check installed pip packages"""
        try:
            # Try using pip3 first, fallback to pip
            pip_cmd = shutil.which('pip3') or shutil.which('pip')
            if not pip_cmd:
                return {}
                
            result = subprocess.run(
                [pip_cmd, 'list', '--format=freeze'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return {}
                
            packages = {}
            for line in result.stdout.split('\n'):
                if '==' in line:
                    pkg, ver = line.split('==', 1)
                    packages[pkg.lower()] = ver
            return packages
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, Exception):
            return {}
    
    def get_installation_commands(self) -> List[str]:
        """Generate installation commands for missing dependencies"""
        commands = []
        
        # Check for missing required Python modules
        missing_modules = []
        for module in self.required:
            try:
                importlib.import_module(module)
            except ImportError:
                missing_modules.append(module)
        
        # Check for missing optional modules
        missing_optional = []
        for module in self.optional:
            try:
                importlib.import_module(module)
            except ImportError:
                missing_optional.append(module)
        
        if missing_modules or missing_optional:
            pip_cmd = shutil.which('pip3') or shutil.which('pip') or 'pip'
            if missing_modules:
                commands.append(f"{pip_cmd} install {' '.join(missing_modules)}")
            if missing_optional:
                commands.append(f"{pip_cmd} install {' '.join(missing_optional)}")
        
        # System tool installation commands based on OS
        missing_tools = []
        for tool in self.system_tools:
            if not self.check_system_tool(tool):
                missing_tools.append(tool)
        
        if missing_tools:
            if self.os_type == 'Linux':
                # Try to determine package manager
                if shutil.which('apt'):
                    cmds = [f"sudo apt-get install {' '.join(missing_tools)}"]
                    commands.extend(cmds)
                elif shutil.which('yum'):
                    cmds = [f"sudo yum install {' '.join(missing_tools)}"]
                    commands.extend(cmds)
                elif shutil.which('dnf'):
                    cmds = [f"sudo dnf install {' '.join(missing_tools)}"]
                    commands.extend(cmds)
                elif shutil.which('brew'):
                    cmds = [f"brew install {' '.join(missing_tools)}"]
                    commands.extend(cmds)
            elif self.os_type == 'Darwin':  # macOS
                if shutil.which('brew'):
                    cmds = [f"brew install {' '.join(missing_tools)}"]
                    commands.extend(cmds)
            elif self.os_type == 'Windows':
                commands.append("Please install missing tools manually or use Chocolatey:")
                for tool in missing_tools:
                    if tool == 'dig':
                        commands.append(f"  choco install bind-toolsonly")
                    elif tool == 'traceroute':
                        commands.append(f"  choco install traceroute")
                    elif tool == 'nmap':
                        commands.append(f"  choco install nmap")
                    elif tool == 'ssh':
                        commands.append(f"  choco install openssh")
                    else:
                        commands.append(f"  choco install {tool}")
        
        return commands
    
    def run(self) -> bool:
        """Run all checks"""
        print("="*60)
        print("🔍 YellowBoxPhish - Requirements Checker")
        print("="*60)
        print(f"📌 Operating System: {self.os_type}")
        print("-"*60)
        
        # Check Python
        self.check_python()
        
        # Check system tools
        self.check_system_tools()
        
        # Check installed packages
        packages = self.check_installed_packages()
        
        # Check required modules
        self.check_modules(self.required, required=True)
        
        # Check optional modules
        self.check_modules(self.optional, required=False)
        
        # Print report
        print("\n📊 Dependency Status Report:")
        print("-" * 60)
        
        for item in self.results:
            if len(item) == 5:  # System tool with description
                name, status, version, required, description = item
                status_str = "✅" if status else "❌"
                req_str = "✓" if required else "⭕"
                print(f"  {req_str} {status_str} {name:25} {version}  ({description})")
            elif len(item) == 4:  # Python module
                name, status, version, required = item
                status_str = "✅" if status else "❌"
                req_str = "✓" if required else "⭕"
                print(f"  {req_str} {status_str} {name:25} {version}")
            else:  # Simple check
                name, status, version = item
                status_str = "✅" if status else "❌"
                print(f"  ⭕ {status_str} {name:25} {version}")
        
        print("-" * 60)
        
        # Summary
        failures = sum(1 for r in self.results 
                      if not r[1] and (len(r) >= 4 and r[3] or len(r) == 3 and r[0] in ['Python', 'pip', 'python3']))
        
        if failures:
            print(f"❌ {failures} required dependencies missing")
            
            # Show installation commands
            commands = self.get_installation_commands()
            if commands:
                print("\n📥 To install missing dependencies:")
                print("-" * 60)
                for cmd in commands:
                    print(f"  {cmd}")
                print("-" * 60)
            
            return False
        else:
            print("✅ All required dependencies satisfied")
            
            # Check optional
            optional_failures = sum(1 for r in self.results 
                                   if not r[1] and (len(r) >= 4 and not r[3]))
            
            # Check missing optional system tools
            system_missing = sum(1 for r in self.results 
                               if len(r) == 5 and not r[1])
            
            total_optional = optional_failures + system_missing
            
            if total_optional:
                print(f"⭕ {total_optional} optional dependencies missing (some features disabled)")
                
                # Show which features might be affected
                print("\n💡 Missing optional components:")
                for r in self.results:
                    if len(r) == 5 and not r[1]:  # System tools
                        print(f"  - {r[0]}: {r[4]}")
                    elif len(r) == 4 and not r[1] and not r[3]:  # Optional Python modules
                        print(f"  - {r[0]}: Optional feature")
            
            return True

def main():
    checker = DependencyChecker()
    success = checker.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()