# Web Kundli - Unveil the Secrets of the Website!

### Unveil the Secrets of Your Website: Secure, Analyze, Optimize.
- Web Kundli is a comprehensive tool designed to uncover details about a website.
- The main idea is straightforward: provide URL to the tool, and it will collect, organize, and display a wide range of open data for you to explore.
- This data helps identify potential vulnerabilities in the website and help optimizing its configurations. Further fine-tuning reduces the website’s potential risks.

## Features
- This Tool is developed in **Python programming**.
- Developed using **asynchronous programming**, allowing modules to run in parallel and achieve faster results.
- The **NMAP scan feature** is also available. Reports can be generated with or without the NMAP scan.
- Based on the output of each module, it calculates the percentage for that module and then calculate the overall performance across all modules. This data is used to **display Website Health**.
- At present, the HTML report dashboard **supports 30 modules**. More features will be added soon! 
  
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
To install and run the Web Kundli Tool, follow these steps:

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
12. `pip install pyfiglet`
13. `pip install pyOpenSSL`
14. `pip install python3-nmap - Ensure that the nmap software is installed on your machine.`

## Usage

### The tool is a command-line utility compatible with Windows and Linux OS.

Execute the tool using the following commands:

- **Without Nmap**:
    ```bash
    python main.py -s https://google.com
    ```
- **With Nmap**:
    ```bash
    python main.py -sn https://google.com
    ```

## Files

- `./config/config.ini`: This file contains API keys and URL links. Please obtain your API key to run the program.

## Report Files

HTML report files are located under the `./output` directory:

`e.g. WebKundli_google.com_21Sep2024_12-13-55.html`

## Image
- **Input Screen:**
  
![Screenshot from 2024-10-06 19-34-52](https://github.com/user-attachments/assets/70f37846-0d32-4121-b103-480caa739c4c)

- **Output HTML Report Screenshot:**
  
![Screenshot from 2024-10-06 19-35-29](https://github.com/user-attachments/assets/e5ec573c-5b37-48d0-bd33-e6c2729f1d68)

- **Report with NMAP Result**

![NMAP](https://github.com/user-attachments/assets/79341c66-50a0-40fa-959d-52f74c29fad0)


🚀 Happy Website analysis! 🚀
