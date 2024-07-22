# Web-Kundli - Python Tool

Explore the internal mechanisms of a website: identify possible vulnerabilities, examine server setup, review security settings, and discover the technologies in use.

At present, the dashboard displays: IP information, SSL chain, DNS records, cookies, headers, domain details, search crawl rules, page map, server location, redirect log, open ports, traceroute, DNS security extensions, site performance, trackers, related hostnames, and carbon footprint. More features will be added soon!

## Installation
To install and run the Auto IP Reputation Tool, follow these steps:

Install the required Python libraries:
    ```bash
    1. pip install python-whois
    2. pip install requests
    3. pip install asyncio
    4. pip install aiohttp
    5. pip install configparser
    6. pip install colorama
    7. pip install dnspython
    8. pip install httpx
    9. pip install dohq-artifactory
    10.pip install dohq-tfs
    11.pip install scapy
    ```

## Usage

Execute the tool using the following commands:

- For a single website search:
    ```bash
    python main.py -s https://google.com
    ```

## Files

- `./config/conftg.ini`: This file contains API keys and URL links. Please obtain your API key to run the program.

## Report Files

HTML report files are located under the `./output` directory:

`Web_kundli_timestamp.html`

🚀 Happy Website analysis! 🚀
