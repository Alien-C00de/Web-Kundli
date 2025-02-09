import os
import time
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from util.config_uti import Configuration

class Analysis_Report:
    def __init__(self, domain, timestamp):
        self.domain = domain
        self.timestamp = timestamp

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

    async def outputHTML(self, website, cookies):

        config = Configuration()
        report_timestamp = str(time.strftime("%A %d-%b-%Y %H:%M:%S", time.localtime(time.time())))

        header = (
            """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title> """ + config.ANALYSIS_REPORT_HEADER + """ </title>
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"/>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                margin: 0;
                                padding: 0;
                                background-color: #f4f4f4;
                            }
                            .container {
                                margin: auto;
                                overflow: hidden;
                                margin-right: 10px;
                                margin-left: 10px;
                            }
                            .header {
                                background-color: #333;
                                padding: 10px;
                                display: flex;
                                align-items: center;
                                justify-content: space-between;
                                margin-right: 10px;
                                margin-left: 10px;
                            }
                            .header h1 {
                                color: #00FF00;
                                margin: 0;
                                font-size: 2.5em;
                            }
                            header a {
                                color: #fff;
                                text-decoration: none;
                                text-transform: uppercase;
                                font-size: 16px;
                            }
                            header ul {
                                padding: 0;
                                list-style: none;
                            }
                            header li {
                                float: left;
                                display: inline;
                                padding: 0 20px 0 20px;
                            }
                            header #branding {
                                float: left;
                            }
                            header #branding h1 {
                                margin: 0;
                            }
                            header nav {
                                float: right;
                                margin-top: 10px;
                            }
                            .module {
                                margin-bottom: 20px;
                            }
                            .module h2 {
                                background: rgb(246, 167, 128);
                                color: #0f0f0e;
                                padding: 10px;
                            }
                            .module p {
                                padding: 10px;
                                background: #e4e4e4;
                                align-items: center;
                                padding: 10px;
                                display: flex;
                            }
                            .issues, .suggestions {
                                background-color: #f2d7d5;
                                padding: 5px;
                                border-radius: 5px;
                                margin-top: 10px;
                                border-left: 5px solid #e74c3c;
                            }
                            .issues h4{
                                margin-top: 5px;
                                margin-bottom: 1px;
                            }
                            .suggestions {
                                background-color: #d6eaf8;
                                border-left: 5px solid #3498db;
                            }
                            .suggestions h4{
                                margin-top: 5px;
                                margin-bottom: 1px;
                            }
                            .footer {
                                background-color: rgb(144, 144, 228);
                                color: #fff;

                                display: flex;
                                align-items: center;
                                justify-content: space-between;
                                margin-right: 10px;
                                margin-left: 10px;
                            }
                            .footer h3{
                                font-size: 0.9em;
                                align-items: center;
                                color: #0f0f0e;
                                margin-right: 10px;
                                margin-left: 10px;
                            }
                        </style>
                    </head>""")
        body = (
                """<body>
                        <div class="header">
                            <h1> """ + config.ANALYSIS_REPORT_HEADER + """ <i class="fas fa-heartbeat" icon-color></i> </h1>
                            <h2 align="right"; margin-right: 40px; style="color:#00FF00;">""" + website + """</h2>
                        </div>
                        <div class="container main">
                            """ + cookies + """
                        </div>

                        <div class="footer">
                            <h3 align="center";> Web Kundli Health Analysis Report © 2025 <h3>
                        </div>
                        
                    </body>
                    </html>""" )

        Analysis_report = "%s_%s_%s.html" % (config.ANALYSIS_REPORT_FILE_NAME.replace("/", "_"), self.domain, self.timestamp)

        Analysis_report = os.path.join("./output", Analysis_report)

        with open(Analysis_report, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(body)

        # if os.name == "nt":
        #     filenameH = file_name_html.partition("./output\\")[-1]
        #     os.system(f'start "" "{file_name_html}"')
        # else:
        #     filenameH = Analysis_report.partition("output/")[-1]
        #     os.system(f'xdg-open "{Analysis_report}"')

        # print(
        #     Fore.GREEN + Style.BRIGHT + f"\n[+] HTML" + Fore.WHITE + Style.BRIGHT,
        #     filenameH,
        #     Fore.GREEN + Style.BRIGHT + f"File Is Ready",
        #     Fore.RESET,
        # )
