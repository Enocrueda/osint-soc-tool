# Installation Guide - OSINT SOC TIER 1 Toolkit


## Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection
- Git (Optional)

## Step 1: Get the code
```bash
git clone https://github.com/Enocrueda/osint-soc-tool.git
cd osint-soc-tool

## Step 2: Set up virtual enviroment
python3 -m venv venv
source venv/bin/activate #Linux/Mac

## Step 3: Install dependencies
pip install -r requirements.txt

## Step 4: Verify installation
python3 osint.py --help

## Troubleshooting
pip install -r requirements.txt --force-reinstall


