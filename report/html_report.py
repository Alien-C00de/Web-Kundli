import datetime
import os
import time
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from util.config_uti import Configuration

class HTML_Report:
    def __init__(self) -> None:
        pass

    async def check_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    async def __create_dirs(self, root, subfolders=None):
        root = root if subfolders == None else f"{root}/{subfolders}/"
        if not os.path.exists(root):
            os.makedirs(f"{root}", exist_ok=True)

    async def __ranking_percentage(self, Server_Location, SSL_Cert, Whois, ser_info, HTTP_sec, headers, cookies, dns_server_info, 
                             tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record, 
                             ports, archive_info, associated_info, block_info, carbon_info, crawl_info, site_info, dns_sec_info,
                             tech_stack_info, firewall_info, social_tag_info, threats_info, global_ranking_info, security_txt_info):
        # List of parameters
        params = {
            'Server_Location': Server_Location,
            'SSL_Cert': SSL_Cert,
            'Whois': Whois,
            'ser_info': ser_info,
            'HTTP_sec': HTTP_sec,
            'headers': headers,
            'cookies': cookies,
            'DNS_Server': dns_server_info,
            'tls_cipher_suite': tls_cipher_suite,
            'dns_info': dns_info,
            'txt_info': txt_info,
            'server_status_info': server_status_info,
            'mail_configuration_info': mail_configuration_info,
            'redirect_Record': redirect_Record,
            'ports': ports,
            'archive_info': archive_info,
            'associated_info': associated_info,
            'block_info': block_info,
            'carbon_info': carbon_info,
            'crawl_info': crawl_info,
            'site_info': site_info,
            'dns_sec_info': dns_sec_info,
            'tech_stack_info': tech_stack_info,
            'firewall_info': firewall_info,
            'social_tag_info': social_tag_info,
            'threats_info': threats_info,
            'global_ranking_info': global_ranking_info,
            'security_txt_info': security_txt_info
        }

        percent = 0
        # Loop through parameters
        for name, value in params.items():
            if isinstance(value, str):
                progress = await self._extract_progress_from_html(value)
                if progress:
                    no_percent_strip = progress.rstrip('%')
                    percent += int(no_percent_strip)
                    # print(f"{name}: Progress - {progress}")

        final = (percent / len(params)) 
        # print(f"Params {len(params)}: Percent - {percent} Final {final}")
        return round(final, 2)

    async def _extract_progress_from_html(self, html_content):
        """Extract the progress percentage from HTML content."""
        # Simulate an asynchronous operation if needed
        # await asyncio.sleep(0)  # No actual async operation here, but for demonstration

        soup = BeautifulSoup(html_content, 'html.parser')
        progress_div = soup.find('div', class_='progress')
        if progress_div:
            return progress_div.get_text(strip=True)
        return None

    async def outputHTML(self, website, Server_Location, SSL_Cert, Whois, ser_info, HTTP_sec, headers, cookies, dns_server_info, 
                         tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record, 
                         ports, archive_info, associated_info, block_info, carbon_info, crawl_info, site_info, dns_sec_info,
                         tech_stack_info, firewall_info, social_tag_info, threats_info, global_ranking_info, security_txt_info, nmap_info):

        config = Configuration()
        report_timestamp = str(time.strftime("%A %d-%b-%Y %H:%M:%S", time.localtime(time.time())))
        percent = await self.__ranking_percentage(Server_Location, SSL_Cert, Whois, ser_info, HTTP_sec, headers, cookies, dns_server_info, 
                         tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record, 
                         ports, archive_info, associated_info, block_info, carbon_info, crawl_info, site_info, dns_sec_info,
                         tech_stack_info, firewall_info, social_tag_info, threats_info, global_ranking_info, security_txt_info)
        header = (
            """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>
        Web Kundli
        </title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"/>
        <style>
        body {
                    background-color: #1e1e1e;
                    color: #d4d4d4;
                    font-family: 'Courier New', Courier, monospace;
                    margin: 0;
                    padding: 0;
                }
                .header {
                    background-color: #333;
                    padding: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-right: 20px;
                    margin-left: 20px;
                }
                .header h1 {
                    color: #FFA500;
                    margin: 0;
                    font-size: 3em;
                }
                .header h2 {
                    color: #FFA500;
                    margin: 0;
                    font-size: 1.5em;
                }
                .header h3 {
                    color: #FFA500;
                    margin: 0;
                    font-size: 1em;
                }
                .ranking-container {
                    background-color: #333;
                    display: flex;
                    align-items: center; /* Vertically align items */
                    justify-content: space-between; /* Space between header and progress bar */
                    margin-right: 20px;
                    margin-left: 20px;
                }
                .ranking-container h1 {
                    margin: 20px;
                    padding: 10px;
                    color: #00FF00;
                }
                .progress-bar-container {
                    flex: 1; /* Allow progress bar to take available space */
                    background-color: #A9A9A9;
                    border-radius: 4px;
                    margin-left: 20px; /* Space between header and progress bar */
                    margin-right: 20px;
                    overflow: hidden;
                }
                .progress-bar {
                    height: 40px;
                    color: #FFFF00;
                    text-align: center;
                    line-height: 40px;
                    border-radius: 4px;
                    background-color: #8F00FF;  /* #76c7c0 Default color, adjust as needed */
                    transition: width 0.5s, background-color 0.5s;
                    font-size: 20px; /* Adjust font size as needed */
                    font-weight: bold; /* Makes the percentage text bold */
                }
                .progress {
                    height: 20px;
                    color: red;
                    text-align: center;
                    line-height: 20px;
                    border-radius: 4px;
                    background-color: #FFFF00; /* #76c7c0 Default color, adjust as needed */
                    transition: width 0.5s, background-color 0.5s;
                    font-size: 16px; /* Adjust font size as needed */
                    font-weight: bold; /* Makes the percentage text bold */
                }
                .date {
                    padding: 5px;
                    margin-right: 30px;
                }
                .date h3 {
                    color: #FFA500;
                    margin: 0;
                    font-size: 1em;
                }
                .content {
                    display: flex;
                    flex-wrap: wrap;
                    padding: 10px;
                }
                .card {
                    background-color: #2d2d2d;
                    margin: 10px;
                    padding: 10px;
                    flex: 1;
                    min-width: 300px;
                    max-width: 100%;
                    border-radius: 5px;
                    position: relative;
                    overflow: auto;
                    height: 450px; 
                    word-wrap: break-word;
                }
                .card h2 {
                    color: #FFA500;
                    margin-top: 0;
                }
                .card .refresh {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    color: #d4d4d4;
                    cursor: pointer;
                }
                .card table {
                    width: 100%;
                    border-collapse: collapse;
                    table-layout: fixed;
                }
                .card table td {
                    padding: 5px;
                    border-bottom: 1px solid #444;
                    text-overflow: ellipsis; 
                    overflow: hidden;
                    word-wrap: break-word;
                }
                .card table td:last-child {
                    text-align: right;
                }
                .card .map {
                    width: 100%;
                    height: 100px;
                    background: url('https://placehold.co/300x200') no-repeat center center;
                    background-size: cover;
                 .icon-color {
                        color: #F0F8FF;
                    }
                }
        </style>
        </head>
        <body>
            <div class="header">
                <h1>
                    <i class="fas fa-user-secret" icon-color></i> Web Kundli
                </h1>
                <h2 align="right"; margin-right: 40px; style="color:#a6e22e;">""" + website + """</h2>
            </div>
            <div class="date">
                <h3 align="right"; margin-right: 20px; style="color:blue;">""" + report_timestamp + """</h3>
            </div>
            <div class="ranking-container">
                <h1>Website Health <i class="fas fa-heartbeat"></i></h1>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: """ + str(percent) + """%;">""" + str(percent) + """%</div>
                </div>
            </div>"""
        )
        body = (
            """<div class="content">
                <div class="card">
                    <h2> Server Location </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + Server_Location +
                """</div>
                <div class="card">
                    <h2> SSL Certificate </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + SSL_Cert +
                """</div>
                <div class="card">
                    <h2> Domain Whois </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + Whois +
                """</div>
                <div class="card">
                    <h2> Server Info </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + ser_info +
                """</div>
                <div class="card">
                    <h2> Headers </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + headers +
                """</div>
                <div class="card">
                    <h2> Cookies </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + cookies + 
                """</div>
                <div class="card">
                    <h2> HTTP Security </h2>
                    <i class="fas fa-sync-alt refresh"> </i>"""  + HTTP_sec +
                """</div>
                <div class="card">
                    <h2> DNS Server </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + dns_server_info +
                """</div>
                <div class="card">
                    <h2> TLS Cipher Suites </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + tls_cipher_suite +
                """</div>
                <div class="card">
                    <h2> DNS Records </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + dns_info +
                """</div>    
                <div class="card">
                    <h2> TXT Records </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + txt_info +
                """</div>    
                <div class="card">
                    <h2> Server Status </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + server_status_info +
                """</div>    
                <div class="card">
                    <h2> Email Configuration </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + mail_configuration_info +
                """</div>    
                <div class="card">
                    <h2> Redirect Chain </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + redirect_Record +
                """</div>    
                <div class="card">
                    <h2> Open Ports </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + ports +
                """</div>    
                <div class="card">
                    <h2>  Archive History </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + archive_info +
                """</div>    
                <div class="card">
                    <h2> Associated Hosts </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + associated_info +
                """</div>    
                <div class="card">
                    <h2> Block Detection </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + block_info +
                """</div>    
                <div class="card">
                    <h2> Carbon Footprint </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + carbon_info +
                """</div>    
                <div class="card">
                    <h2> Crawl Rules </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + crawl_info +
                """</div>    
                <div class="card">
                    <h2> Site Features </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + site_info +
                """</div>    
                <div class="card">
                    <h2> DNS Security </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + dns_sec_info +
                """</div>    
                <div class="card">
                    <h2> Tech Stack </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + tech_stack_info +
                """</div>  
                <div class="card">
                    <h2> Firewall Detection </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + firewall_info +
                """</div>  
                <div class="card">
                    <h2> Social Tags </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + social_tag_info +
                """</div> 
                <div class="card">
                    <h2> Threats </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + threats_info +
                """</div> 
                <div class="card">
                    <h2> Global Rank </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + global_ranking_info +
                """</div> 
                <div class="card">
                    <h2> Security.Txt </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + security_txt_info +
                """</div> """ )
        # Conditionally add Whois section
        if nmap_info:
            body += (
                """<div class="card">
                    <h2> NMAP OS Version </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + nmap_info[0] +
                """</div> 
                <div class="card">
                    <h2> NMAP Version Result </h2>
                    <i class="fas fa-sync-alt refresh"> </i>""" + nmap_info[1] +
                """</div>"""
            )

        # Close the main content div
        body += """</div>"""

        # save html closing </ body> and </ html> tags to a variable named "footer"
        footer = ("""<div class="date">
                        <h3 align="right"; margin-right: 20px; style="color:#00FF00;">Developed by:👽 """ + config.AUTHOR + """  """ + config.YEAR + """ ver: """ + config.VERSION +  """</h3>
                        <div style="display: flex; justify-content: flex-end; align-items: center;">
                            <i class="far fa-envelope"></i>
                            <h3 align="right"; margin-right: 20px; style="color:#00FF00;">: """ + config.EMAIL + """</h3>
                        </div>
                        <div style="display: flex; justify-content: flex-end; align-items: center;">
                            <i class="fab fa-github"></i>
                            <h3 align="right"; margin-right: 20px; style="color:#00FF00;">: """ + config.GITHUB + """</h3>
                        </div>
                    </div>
                </body>
            </html>""")

        # create and open the new WebKundli.html file
        # timestamp = int(datetime.datetime.now().timestamp())
        timestamp  =  datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name_html = "%s_%s.html" % (config.REPORT_FILE_NAME.replace("/", "_"), timestamp)

        await self.__create_dirs("output")

        file_name_html = os.path.join("./output", file_name_html)

        with open(file_name_html, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(body)
            # for x in self.__html:
            #     f.write(x)
            f.write(footer)

        if os.name == "nt":
            filenameH = file_name_html.partition("./output\\")[-1]
            os.system(f'start "" "{file_name_html}"')
        else:
            filenameH = file_name_html.partition("output/")[-1]
            os.system(f'xdg-open "{file_name_html}"')

        print(
            Fore.GREEN + Style.BRIGHT + f"\n[+] HTML" + Fore.WHITE + Style.BRIGHT,
            filenameH,
            Fore.GREEN + Style.BRIGHT + f"File Is Ready",
            Fore.RESET,
        )
