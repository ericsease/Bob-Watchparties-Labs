# Prerequisites & Setup Guide

This guide will help you set up everything you need to complete the Bob hands-on labs.

## Table of Contents
- [General Requirements](#general-requirements)
- [Lab-Specific Requirements](#lab-specific-requirements)
- [Installation Instructions](#installation-instructions)
- [Verification Steps](#verification-steps)
- [Troubleshooting](#troubleshooting)

---

## General Requirements

These are required for all labs:

### 1. Bob IDE
**Required for:** All labs

Bob must be installed and configured on your system.

**Installation:**
- Contact your administrator for Bob installation instructions
- Ensure you have a valid Bob license
- Verify Bob is running and accessible

**Verification:**
```bash
# Bob should launch when you run it
# Check that you can create a new project or open a folder
```

### 2. Git
**Required for:** All labs (for cloning the repository)

**Version:** 2.x or higher

**Installation:**

**macOS:**
```bash
# Using Homebrew
brew install git

# Or download from: https://git-scm.com/download/mac
```

**Windows:**
```bash
# Download installer from: https://git-scm.com/download/win
# Run the installer and follow the prompts
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

**Verification:**
```bash
git --version
# Should show: git version 2.x.x or higher
```

### 3. Text Editor (Optional)
**Recommended:** VS Code or any text editor you're comfortable with

While Bob IDE is the primary tool, having a separate text editor can be helpful for reference.

**VS Code Installation:**
- Download from: https://code.visualstudio.com/

---

## Lab-Specific Requirements

### Lab 1: Bring Your Own Use Case

**Requirements:** Flexible - depends on your chosen project

**Common scenarios:**

**For web projects (HTML/CSS/JavaScript):**
- No additional software required
- Just a web browser (Chrome, Firefox, Safari, Edge)

**For Python projects:**
- Python 3.8+ (see installation below)
- pip package manager

**For Node.js projects:**
- Node.js 14+ and npm
- Download from: https://nodejs.org/

**Recommendation:** Start with a web-based project (HTML/CSS/JavaScript) to avoid setup complexity.

---

### Lab 2: Building a Todo Application

**Required:**
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

**Python Packages (installed during lab):**
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
pytest==7.4.3
pytest-cov==4.1.0
coverage==7.3.2
```

**Installation:**

**macOS:**
```bash
# Check if Python 3 is installed
python3 --version

# If not installed, use Homebrew
brew install python@3.11

# Verify pip is installed
pip3 --version
```

**Windows:**
```bash
# Download Python from: https://www.python.org/downloads/
# During installation, check "Add Python to PATH"

# Verify installation
python --version
pip --version
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

**Verification:**
```bash
# Check Python version (should be 3.8+)
python3 --version
# or on Windows:
python --version

# Check pip
pip3 --version
# or on Windows:
pip --version

# Test virtual environment creation
python3 -m venv test_env
# Should create a test_env directory without errors
rm -rf test_env  # Clean up
```

---

### Lab 3: Security Analysis & Code Fixes

**Required:**
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

**Python Packages (installed during lab):**
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
```

**Installation:**

Same as Lab 2 - Python 3.8+ with pip and virtual environment support.

```bash
# Check Python version
python3 --version
# Should show 3.8.x or higher

# Verify pip
pip3 --version
```

**Verification:**
```bash
# Verify Python 3.8+
python3 --version

# Verify pip
pip3 --version

# Test virtual environment creation
python3 -m venv test_env
# Should create a test_env directory without errors
rm -rf test_env  # Clean up
```

**Note:** This lab focuses on security analysis and doesn't require any special tools beyond Python and the packages listed above. The vulnerable application code is provided in the lab materials.

---

## Installation Instructions

### Complete Setup Walkthrough

#### Step 1: Install Git

Follow the Git installation instructions for your operating system above.

#### Step 2: Install Python

**macOS:**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Verify
python3 --version
pip3 --version
```

**Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or higher
3. Run the installer
4. **Important:** Check "Add Python to PATH" during installation
5. Verify in Command Prompt:
   ```bash
   python --version
   pip --version
   ```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip

# Verify
python3 --version
pip3 --version
```

#### Step 3: Set Up Virtual Environments

Virtual environments isolate project dependencies. Here's how to use them:

**Create a virtual environment:**
```bash
# Navigate to your project directory
cd path/to/project

# Create virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

**Install packages:**
```bash
# With virtual environment activated
pip install -r requirements.txt
```

**Deactivate when done:**
```bash
deactivate
```

#### Step 4: Verify Bob IDE

1. Launch Bob IDE
2. Try opening a folder
3. Try creating a new file
4. Verify you can interact with Bob's chat interface

---

## Verification Steps

### Complete System Check

Run these commands to verify everything is set up correctly:

```bash
# 1. Check Git
git --version
# Expected: git version 2.x.x or higher

# 2. Check Python
python3 --version
# Expected: Python 3.8.x or higher (3.10+ for Lab 2)

# 3. Check pip
pip3 --version
# Expected: pip 20.x or higher

# 4. Test virtual environment
python3 -m venv test_venv
source test_venv/bin/activate  # or test_venv\Scripts\activate on Windows
pip --version
deactivate
rm -rf test_venv

# 5. Test package installation (optional)
pip3 install --dry-run flask
# Should show what would be installed
```

### Lab-Specific Verification

**For Lab 1:**
```bash
# Verify you can install Flask
pip3 install --dry-run Flask==3.0.0
# Should succeed without errors
```

**For Lab 2:**
```bash
# Verify Python 3.10+
python3 --version | grep -E "3\.(1[0-9]|[2-9][0-9])"
# Should show your Python version if 3.10+

# Verify you can install required packages
pip3 install --dry-run pandas numpy
# Should succeed without errors
```

---

## Troubleshooting

### Common Issues

#### Python Not Found

**Problem:** `python: command not found` or `python3: command not found`

**Solution:**
```bash
# Try different commands
python --version
python3 --version
py --version  # Windows

# If none work, Python isn't installed or not in PATH
# Reinstall Python and ensure "Add to PATH" is checked
```

#### Wrong Python Version

**Problem:** Python version is too old (< 3.8 for Lab 1, < 3.10 for Lab 2)

**Solution:**
```bash
# Install a newer version alongside the old one
# macOS:
brew install python@3.11

# Windows: Download from python.org
# Linux: Use your package manager

# Use the specific version
python3.11 --version
python3.11 -m venv venv
```

#### pip Not Found

**Problem:** `pip: command not found`

**Solution:**
```bash
# Try different commands
pip --version
pip3 --version
python -m pip --version
python3 -m pip --version

# If none work, reinstall Python with pip included
# Or install pip separately:
python3 -m ensurepip --upgrade
```

#### Virtual Environment Issues

**Problem:** Can't create or activate virtual environment

**Solution:**
```bash
# Ensure venv module is installed
# Ubuntu/Debian:
sudo apt-get install python3-venv

# Create with full path
python3 -m venv ./venv

# Activate with full path
# macOS/Linux:
source ./venv/bin/activate

# Windows:
.\venv\Scripts\activate

# If activation fails on Windows, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Permission Errors

**Problem:** Permission denied when installing packages

**Solution:**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install package_name

# Or use --user flag (not recommended)
pip3 install --user package_name

# Never use sudo with pip (can break system Python)
```

#### Package Installation Fails

**Problem:** Error installing packages from requirements.txt

**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Try installing packages one by one to identify the problem
pip install flask
pip install flask-cors
# etc.

# Check for system dependencies
# Some packages need build tools:
# macOS: xcode-select --install
# Ubuntu: sudo apt-get install build-essential python3-dev
# Windows: Install Visual Studio Build Tools
```

#### Git Clone Fails

**Problem:** Can't clone the repository

**Solution:**
```bash
# Check Git is installed
git --version

# Check network connection
ping github.com

# Try HTTPS instead of SSH
git clone https://github.com/username/repo.git

# If behind a proxy, configure Git:
git config --global http.proxy http://proxy.example.com:8080
```

#### Bob IDE Issues

**Problem:** Bob not responding or not working correctly

**Solution:**
1. Restart Bob IDE
2. Check Bob is up to date
3. Verify your license is active
4. Check system resources (RAM, disk space)
5. Contact your administrator

---

## Quick Reference

### Essential Commands

```bash
# Clone repository
git clone <repository-url>
cd <repository-name>

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

# Check versions
python3 --version
pip3 --version
git --version
```

### Lab-Specific Quick Start

**Lab 1 (BYOC):**
```bash
cd lab2
# Setup depends on your chosen project
```

**Lab 2 (Beginner - Todo App):**
```bash
cd lab3
# You'll create everything from scratch with Bob's help
# No pre-existing files to set up
```

**Lab 3 (Advanced - Security):**
```bash
cd lab3/financial-trading-bot
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python seed_data.py
python app.py
```

---

## Getting Help

If you're still having issues after trying the troubleshooting steps:

1. **Check the lab-specific README** - Each lab has its own troubleshooting section
2. **Use Bob's Ask Mode** - Ask Bob to help diagnose the issue
3. **Review error messages carefully** - They often contain the solution
4. **Search online** - Many setup issues have well-documented solutions
5. **Ask for help** - Contact your instructor or administrator

---

## Summary Checklist

Before starting the labs, verify:

- [ ] Git is installed and working (`git --version`)
- [ ] Python 3.8+ is installed (`python3 --version`)
- [ ] pip is installed and working (`pip3 --version`)
- [ ] You can create virtual environments (`python3 -m venv test`)
- [ ] Bob IDE is installed and running
- [ ] You've cloned the lab repository
- [ ] You've opened the repository in Bob

**All set?** → [Return to Main README](README.md) to start the labs!

---

*Last Updated: June 2026*