# Usage Guide - OSINT SOC TIER 1 Toolkit v1.0.0

# Table of Contents
- [Basic Commands](#basic-commands)
- [Domain Investigation](#domain-investigation)
- [IP Investigation](#ip-investigation)
- [Command Options](#command-options)
- [Examples](#examples)
- [Output Format](#output-format)
- [Workflow Examples](#workflow-examples)

# Basic Commands


## Display help menu
```bash
python3 osint.py --help


## Check Version
```bash
python3 osint.py --version



# Domain Investigation

## Basic WHOIS Lookup
```bash
python3 osint.py -d example.com

## Full Domain Analysis (WHOIS + DNS)
```bash
python3 osint.py -d example.com -v

## Save Domain Results to file
```bash
python3 osint.py -d example.com -o dominio_report.json

## Domain Analysis with ALL Details
```bash
python3 osint.py -d example.com -v -o dominio_fullreport.json



# IP Investigation

## Basic Geolocation (Using Google IP as Example)
python3 osint.py -i 8.8.8.8

## Geolocation + PortScan
python3 osint.py -i 8.8.8.8 -v

## Save IP reports to file
python3 osint.py -i 8.8.8.8 -o ip_report.json

## Full IP Analysis
python3 osint.py -i 8.8.8.8 -v -o ip_fullreport.json



# Command Options
| Option | Description | Example |
|--------|-------------|---------|
| `-d, --dominio` | Target domain to investigate | `-d google.com` |
| `-i, --ip` | Target IP address to analyze | `-i 8.8.8.8` |
| `-o, --output` | Save results to JSON file | `-o reporte.json` |
| `-v, --verbose` | Show detailed output | `-v` |
| `--help` | Display help menu | `--help` |
| `--version` | Show tool version | `--version` |


# Examples with Real Output

## Domain Examples
$ python3 osint.py -d google.com -v

🔍 Consultando WHOIS para google.com...
   ✅ WHOIS completado.
   📋 Registrado por: MarkMonitor Inc.
   📅 Creado: 1997-09-15
   ⏰ Expira: 2028-09-13

🔍 Consultando DNS para google.com...
   • A: 6 registros
   • MX: 5 registros
   ✅ DNS completado (3 tipos encontrados).

## IP Examples (8.8.8.8)
$ python3 osint.py -i 8.8.8.8 -v

📍 Consultando geolocalización para 8.8.8.8...
✅ Geolocalización encontrada con éxito.
   País: United States
   Ciudad: Ashburn
   ISP: Google LLC
   Latitud: 39.0437
   Longitud: -77.4875

🔍 Escaneando puertos comunes en 8.8.8.8...
   ✅ Puerto 53: DNS (abierto)
   ✅ Puerto 443: HTTPS (abierto)
   📊 Puertos abiertos encontrados: 2

📌 Resumen de IP:
------------------------------
   País: United States
   Ciudad: Ashburn
   ISP: Google LLC
   Latitud: 39.0437
   Longitud: -77.4875
   Puertos abiertos: 2
     53: DNS
     443: HTTPS



# Output Format

## Domain Output Structure (JSON)
{
  "metadata": {
    "fecha": "2024-02-18T10:30:00",
    "objetivo": "google.com",
    "tipo_de_analisis": "dominio",
    "herramienta": "OSINT-SOC-Toolkit v1.0.0"
  },
  "whois": {
    "dominio": "google.com",
    "registrar": "MarkMonitor Inc.",
    "fecha_creacion": "1997-09-15",
    "fecha_expiracion": "2028-09-13",
    "servidores_dns": ["ns1.google.com", "ns2.google.com"],
    "pais": "US",
    "org": "Google LLC"
  },
  "dns": {
    "A": ["142.250.185.46", "142.250.185.46"],
    "MX": [
      {"prioridad": 10, "servidor": "aspmx.l.google.com"},
      {"prioridad": 20, "servidor": "alt1.aspmx.l.google.com"}
    ]
  }
}

## IP Output Structure (JSON)
{
  "metadata": {
    "fecha": "2024-02-18T10:30:00",
    "objetivo": "8.8.8.8",
    "tipo_de_analisis": "IP",
    "herramienta": "OSINT-SOC-Toolkit v1.0.0"
  },
  "geo": {
    "Ip": "8.8.8.8",
    "Pais": "United States",
    "Ciudad": "Ashburn",
    "Isp": "Google LLC",
    "Latitud": 39.0437,
    "Longitud": -77.4875
  },
  "puertos": [
    {
      "puerto": 53,
      "estado": "abierto",
      "servicio": "DNS",
      "banner": "No disponible"
    },
    {
      "puerto": 443,
      "estado": "abierto",
      "servicio": "HTTPS",
      "banner": "HTTP/1.1 400 Bad Request"
    }
  ]
}



# Workflow Examples

## Investigate a Suspicious Domain
- Step 1: Quick WHOIS Check
python3 osint.py -d threath.xyz

- Step 2: Detailed DNS Analysis
python3 osint.py -d threath.xyz -v

- Step 3: Save full Report
python3 osint.py -d threath.xyz -v -o analysis_case.json


## Investigate a Suspicious IP
- Step 1: Geolocation
python3 osint.py -i 192.145.1.1

- Step 2: Port Scan
python3 osint.py -i 192.145.1.1 -v

- Step 3: Save Full Report
python3 osint.py -i 192.145.1.1 -v -o ip_analysis.json



# Tips & Best Practices
- Always use verbose mode first to understand what's happening

- Save outputs with -o for documentation and evidence

- Use virtual environment to avoid dependency conflicts

- Check rate limits when scanning multiple IPs

- Verify findings with other tools



# Error Handling

- Error            	- Solution
"Module not found"	- Run pip install -r requirements.txt
"Connection timeout"	- Check internet connection
"Invalid domain"	- Verify domain exists
"API limit reached"	- Wait 60 seconds and try again



#See Also
- [Installation Guide](INSTALL.md)
- [API Documentation](API.md)
- [GitHub Repository](https://github.com/Enocrueda/osint-soc-tool)
