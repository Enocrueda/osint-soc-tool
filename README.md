# OSINT SOC Toolkit v1.0.0


![Python](https://img.shields.io/badge/Python-3.8+-blue)
![SOC](https://img.shields.io/badge/SOC-Tier%201-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![OSINT](https://img.shields.io/badge/OSINT-Reconnaissance-purple)

A Python-based OSINT tool for SOC Tier 1 analysts. Automates domain and IP investigation to support incident response and threat intelligence.


## Features

- WHOIS Lookup - Domain registration information (registrar, dates, name-servers).
- DNS Enumeration - A, AAAA, MX, TXT, NS, CNAME records.
- IP Geolocation - Country, City, ISP, Coordinates via ip-api.com.
- Port Scanning - 20+ common ports with service identification.
- Banner Grabbing - Capture banners from open services.
- JSON Export - Structured results for documentation and further analysis.
- Concurrent Scanning - Fast port scanning using ThreadPoolExecutor

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### installation

``` bash
# 1. Clone the repository
git clone https://github.com/Enocrueda/osint-soc-tool.git
cd osint-soc-tool

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
# venv/Scripts/activate    # On Windows 

# 3. Install dependencies
pip install -r requirements.txt]

# 4. Verify installation
python3 osint.py --help


## Basic Usage

### Domain Investigation
```bash
# Quick WHOIS lookup
python3 osint.py -d example.com

# Full domain analysis (WHOIS + DNS)
python3 osint.py -d examples.com -v
	
# Save results to JSON
python3 osint.py -d example.com -v -o reports/example.json

```

### IP investigation
```bash
# Basic Geolocation
python3 osint.py -i 8.8.8.8

# Geolocation + Port Scan
python3 osint.py -i 8.8.8.8 -v

# Save results to JSON
pyhon3 osint.py -i 8.8.8.8 -v -o reports/8.8.8.8.json


## Example Output
```bash
python3 osint.py -i 8.8.8.8 -v

📍 Geolocating 8.8.8.8...
✅ Geolocation successful
   Country: United States
   City: Ashburn
   ISP: Google LLC
   Coordinates: 39.0437, -77.4875

🔍 Scanning common ports on 8.8.8.8...
   ✅ Port 53: DNS (open)
   ✅ Port 443: HTTPS (open)
   📊 Open ports found: 2
```

## Project Strucuture
```
osint-soc-tool/
├── osint.py                 # Main script
├── config.yaml              # Configuration file
├── requirements.txt         # Dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore               # Git ignore rules
├── docs/                    # Detailed documentation
│   ├── INSTALL.md           # Installation guide
│   ├── USAGE.md             # Usage guide with examples
│   └── API.md               # API documentation
└── reports/                 # Generated reports (empty in repo)
```
## Documentation
- Installation Guide - Detailed setup instructions
- Usage Guide - Command examples and workflows
- API Documentation - API references and rate limit

## Technologies
- Python 3.8+ - Core language
- python-whois -  WHOIS lookup
- dnspython - DNS queries
- requests - HTTP requests for geolocation
- ThreadPoolExecutor - Concurrent port scanning

## Use Cases for SOC Analysts

### 1. Suspicius IP Investigation
```bash
python3 osint.py -i 203.0.113.5 -v -o reports/suspicius_ip.json

### 2. Pishing Domain Analysis
python3 osint.py -d phishing-site.xyz -v -o reports/pishing_case.json

### 3. IOC Enrichment
for ip in $(cat iocs.txt); do
    python3 osint.py -i $ip -o "reports/${ip}.json"
done

```
## Ethical Use Warning
This tool is intended for authorized security testing and incident response only.
Users are responsible for complyning with all applicable laws and regulations. The
Author assumes no liability for misuse.


## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request


## License
THis proyect is licensed under the MIT LIcense - see the LICENSE file for details.


## Author
Enoc Rueda - Aspirant SOC Analyst
Email: enoctrd@gmail.com
Linkedln: www.linkedin.com/in/enoctrd
Github: github.com/Enocrueda.git


## Acknowledgments
- ip-api.com for free geolocation API
- python-whois library
- dnspython library
- TryHackMe & HackTheBox for hands-on labs
- THe OSINT community for knowledge sharing


## Version History
- v1.0.0 (2024-02-18) - Initial release
- WHOIS lookups
- DNS enumeration
- IP geolocation
- Port Scanning
- JSON export


