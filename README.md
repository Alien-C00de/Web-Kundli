# Web Kundli - A Python Tool

Explore the internal mechanisms of a website: identify possible vulnerabilities, examine server setup, review security settings, and discover the technologies in use.

## Features
- Based on the details of each module, it calculates the percentage for that module and then determines the overall performance percentage across all modules. This data is used to display **Website Health** accordingly.
- The **NMAP scan feature** is also available. Reports can be generated with or without the NMAP scan to avoid network scanning.
- It supports **asynchronous programming**, allowing modules to run in parallel and achieve faster results.
- At present, the dashboard **supports 30 modules**. More features will be added soon!
  
  `1. SSL certificates`
  `2. DNS Records`
  `3. Cookies`
  `4. Crawl Rules`
  `5. Headers`
  `6. Server Location`
  `7. Associated Hosts`
  `8. Redirect Chain`
  `9. TXT Records`
  `10. Server Status`
  `11. Open Ports`  
  `12. Carbon Footprint`
  `13. Server Info`
  `14. Whois Lookup`
  `15. DNS Security Extensions`  
  `16. Site Features`
  `17. DNS Server`
  `18. Tech Stack`
  `19. Security.txt`
  `20. Social Tags`  
  `21. Mail Configuration`
  `22. Firewall Detection`
  `23. HTTP Security Features`
  `24. Archive History`
  `25. Global Ranking`
  `26. Block Detection`
  `27. Malware & Phishing Detection`
  `28. TLS Cipher Suites`  
  `29. Nmap Scan OS Detection`
  `30. Nmap_Scan Version Result`      

## Installation
To install and run the Auto IP Reputation Tool, follow these steps:

Install the required Python libraries:
1. `pip install python-whois`
2. `pip install requests`
3. `pip install asyncio`
4. `pip install aiohttp`
5. `pip install configparser`
6. `pip install colorama`
7. `pip install dnspython`
8. `pip install scapy`
9. `pip install beautifulsoup4`
10. `pip install pybase64`
11. `pip install tldextract`
12. `pip install python3-nmap - Ensure that the nmap software is installed on your machine.`

## Usage

Execute the tool using the following commands:

- For a single website **WithOut Nmap** details search:
    ```bash
    python main.py -s https://google.com
    ```
- For a single website **With Nmap** details search:
    ```bash
    python main.py -sn https://google.com
    ```

## Files

- `./config/conftg.ini`: This file contains API keys and URL links. Please obtain your API key to run the program.

## Report Files

HTML report files are located under the `./output` directory:

`e.g. Web_kundli_2024-09-15_14-41-32.html`

## Image
- **Input Screen:**
  
![Screenshot from 2024-09-15 15-37-05](https://github.com/user-attachments/assets/5937972c-7985-436d-b07f-6125a0b42781)

- **Output HTML Report Screenshot:**
  
![Screenshot from 2024-09-15 15-39-06](https://github.com/user-attachments/assets/ce41b92d-2e31-4841-b91b-f9144a273f95)

- **Report with NMAP Result**

![NMAP](https://github.com/user-attachments/assets/79341c66-50a0-40fa-959d-52f74c29fad0)


🚀 Happy Website analysis! 🚀
