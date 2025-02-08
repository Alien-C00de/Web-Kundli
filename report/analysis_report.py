import datetime
import os
import time
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from util.config_uti import Configuration

class Analysis_Report:
    def __init__(self, domain):
        self.domain = domain

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
                        <title>Website Security Analysis Report</title>
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
                            header {
                                background: #3498db;
                                color: #fff;
                                padding-top: 50px;
                                min-height: 60px;
                                border-bottom: #77aaff 3px solid;
                                align-items: center;
                                justify-content: space-between;
                                margin-right: 10px;
                                margin-left: 10px;
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
                            .main {
                                padding: 20px;
                                background: #fff;
                                margin-top: 20px;
                            }
                            .module {
                                margin-bottom: 20px;
                            }
                            .module h2 {
                                background: #332;
                                color: #FFA500;
                                padding: 10px;
                            }
                            .module p {
                                padding: 20px;
                                background: #e4e4e4;
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
                            footer {
                                background-color: #333;
                                color: #fff;
                                padding: 10px;
                                display: flex;
                                align-items: center;
                                justify-content: space-between;
                                margin-right: 10px;
                                margin-left: 10px;
                            }
                        </style>
                    </head>""")
        body = (
                """<body>
                        <header>
                            <div class="container">
                                <div id="branding">
                                    <h1>Website Security Analysis Report</h1>
                                </div>
                            </div>
                        </header>

                        <div class="container main">
                            """ + cookies + """
                        </div>

                        <footer>
                            <p>Website Security Analysis Report &copy; 2025</p>
                        </footer>
                    </body>
                    </html>""" )

        timestamp  =  datetime.datetime.now().strftime("%d%b%Y_%H-%M-%S")
        file_name_html = "%s_%s_%s.html" % (config.ANALYSIS_REPORT_FILE_NAME.replace("/", "_"), self.domain, timestamp)

        file_name_html = os.path.join("./output", file_name_html)

        with open(file_name_html, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(body)

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
