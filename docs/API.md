# API Documentation - OSINT SOC Toolkit

## Geolocation API: ip-api.com

### Endpoint


```
GET http://ip-api.com/json/{ip}
```
### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `ip` | string | IPv4 or IPv6 address to locate |

### Response Format (Success)
```json
{
  "status": "success",
  "country": "United States",
  "countryCode": "US",
  "region": "CA",
  "regionName": "California",
  "city": "Mountain View",
  "zip": "94043",
  "lat": 37.4229,
  "lon": -122.085,
  "timezone": "America/Los_Angeles",
  "isp": "Google LLC",
  "org": "Google Public DNS",
  "as": "AS15169 Google LLC",
  "query": "8.8.8.8"
}



### Response Format(ERROR)
```json
{
  "status": "fail",
  "message": "invalid query",
  "query": "invalid.ip"
}
```

### Rate Limits
- Free Tire: 45 requests per minute
- Pro Tier: Unlimited (Paid)
- Source: ip-api.com/docs


### Implementation in Code
```python
def geo_ip(ip, verbose=False):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    if data.get('status') == 'success':
        return {
            'Ip': data.get('query'),
            'Pais': data.get('country'),
            'Ciudad': data.get('city'),
            'Isp': data.get('isp'),
            'Latitud': data.get('lat'),
            'Longitud': data.get('lon')
        }

```

## WHOIS Library: python-whois

### Description:
 Library for performing WHOIS lookups on domain. No API key required.

### Installation
```bash
pip install python-whois

### Basic Usage
```python
import whois

w = whois.whois('google.com')
print(f"Registrar: {w.registrar}")
print(f"Creation Date: {w.creation_date}")
print(f"Name Servers: {w.name_servers}")

```

 
### Response Fields

| Field | Description |
|-------|-------------|
| registrar       | Domain registrar organization |
| creation_date	  | Date domain was registered    |
| expiration_date | Date domain expires           |
| name_servers	  | List of DNS servers           |
| country	  | Registrar country             |
| org	          | Organization name             |




### Rate Limit
- No API key required
- Rate limited by WHOIS servers (typically 10-20 queries per minute)0
- Be respectful and add delays for bulk queries




## DNS Library: dnspython

### Description:
Library for performing DNS queries. No API key required

### Installation
```bash 
pip install dnspython
```
### Basic Usage
```python
import dns.resolver

answers = dns.resolver.resolve('google.com', 'A')
for rdata in answers:
    print(f"A: {rdata.address}")

answers = dns.resolver.resolve('google.com', 'MX')
for rdata in answers:
    print(f"MX: {rdata.exchange} (priority {rdata.preference})")

```


### Supported Record Types
_____________________
| Type  |Description|
|_______|___________|
A     |	IPv4 address records          |
AAAA  |	IPv6 address records          |
MX    | Mail exchange records         |
TXT   |	Text records (SPF, DKIM, etc.)|
NS    |	Name server records           |
CNAME |	Canonical name records        |




### Error Handling
```python
try:
    answers = dns.resolver.resolve(domain, 'A')
except dns.resolver.NoAnswer:
    print("No A records found")
except dns.resolver.NXDOMAIN:
    print("Domain does not exist")
except Exception as e:
    print(f"Error: {e}")
```



## Best Practice


### Rate Limits
```python
import time

def rate_limited_request(ip):
    """Example with rate limiting"""
    response = requests.get(f"http://ip-api.com/json/{ip}")
    time.sleep(1)  # Wait 1 second between requests
    return response

```

### Error Handling
```python
def safe_api_call(func):
    """Decorator for safe API calls"""
    try:
        return func()
    except requests.Timeout:
        return {"error": "Timeout"}
    except requests.ConnectionError:
        return {"error": "Connection error"}
    except Exception as e:
        return {"error": str(e)}


### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_whois(domain):
    """Cache WHOIS results"""
    return whois.whois(domain)

```


## Response Comparison

###Domain Investigation
____________________________________________
| Data Source	   |    Information Provided|
--------------------------------------------
| WHOIS	Registrar    |  dates, name servers        |
| DNS	IP addresses |  mail servers, text records |


### IP Investigation

___________________________________________
|  Data Source	 |    Information Provided|
-------------------------------------------
| Geolocation	 |      Country, city, ISP, coordinates|
| Port Scan	 |      Open ports, services, banners  |




## Troubleshooting

### Common Issues

______________________________
|  Problem      |    Solution|
------------------------------
| "Connection timeout"  | Check internet connection, increase timeout   |
| "API limit reached"	| Add delays, use caching, upgrade to pro       |
| "Invalid domain"	| Verify domain exists and is properly formatted|
| "No answer"	        | Domain may not have that record type          |
| "NXDOMAIN"	        | Domain does not exist                         |




## Testing APIs Manually
```bash
### Test geolocation API
curl http://ip-api.com/json/8.8.8.8

### Test WHOIS (command line)
whois google.com

### Test DNS (command line)
nslookup google.com
dig google.com MX
```



## REFERENCES
- ip-api.com Documentation

- python-whois Documentation

- dnspython Documentation

- IANA WHOIS Service

- DNS Record Types



## Notes
- All APIs used are free with rate limits

- No authentication required

- For production use, consider:

- Implementing proper caching

  - Adding retry logic

  - Monitoring API quotas

  - Respecting terms of service
