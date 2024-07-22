import datetime
import os
import time
from colorama import Back, Fore, Style
from util.config_uti import Configuration


class html_report:
    def __init__(self) -> None:
        pass

    async def check_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    async def __create_dirs(self, root, subfolders=None):
        root = root if subfolders == None else f"{root}/{subfolders}/"
        if not os.path.exists(root):
            os.makedirs(f"{root}", exist_ok=True)

    async def outputHTML(self, Server_Location, SSL_Cert, Whois, ser_info, HTTP_sec, headers,
                         cookies, DNS_Server, tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record, ports):

        config = Configuration()
        header = (
            """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Automated VirusTotal Analysis Report | API v3</title>
            <style>
                body {
                font-family: Sans-Serif;
                color: #1d262e;
                }
                h1 {
                    font-size: 3.25em;
                    margin: 50px 0 0 50px;
                }
                h2 {
                    font-size: .75em;
                    font-weight:normal;
                    margin: 5px 0 15px 50px;
                    color: #7d888b;
                }
                h3 {
                    font-size: 1.50em;
                    font-weight:normal;
                    margin: 0 0 20px 50px;
                    color: #7d888b;
                }
                h4 {
                    font-size: .750em;
                    font-weight:normal;
                    margin: 0 0 20px 50px;
                    text-align:right;
                    color: orange;
                }
                table {
                    text-align: left;
                    width: 100%;
                    border-collapse: collapse;
                    border: none;
                    padding: 0;
                    margin-left: 50px;
                    margin-bottom: 40px;
                    max-width: 1200px;
                }
                th { 
                    text-align: left;
                    border:none;
                    padding: 10px 0 5px 10px;
                    margin-left: 10px;
                }
                tr { 
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                    border-top: none;
                    border-left: none;
                    border-right: none;
                    padding-left: 10px;
                    margin-left: 0;
                }
                td { 
                    border-bottom: none;
                    border-top: none;
                    border-left: none;
                    border-right: none;
                    padding-left: 10px;
                }
                tr th {
                    padding: 10px 10px 5px 10px;
                }

            </style>
        </head>
        <body>
        <h1 class="reportHeader">"""
            + config.REPORT_HEADER
            + """</h1>
        <h2>"""
            + config.REPORT_SUB_TITLE
            + """</h2>
        """
        )
        # add report timestamp
        report_timestamp = str(
            "<h3>" + time.strftime("%c", time.localtime(time.time())) + "</h3>"
        )

        body = (
            """
                <table style="border-collapse: collapse; width: 100%; height: 252px;" border="1">
                <tbody>
                <tr style="height: 54px;">
                <td style="width: 20%; height: 54px;">
                <h3 id="server-location" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">Server Location</h3>
                <p> """
            + Server_Location
            + """</p> </td>
                <td style="width: 20%; height: 54px;">
                <h3 id="ssl-certificate" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">SSL Certificate</h3>
                <p> """
            + SSL_Cert
            + """</p> </td>
                <td style="width: 20%; height: 54px;">
                <h3 id="domain-whois" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">Domain Whois</h3>
                <p> """
            + Whois
            + """</p> </td>
                </tr>
                <tr style="height: 54px;">
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="server-info" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">Server Info</h3>
                <p> """
            + ser_info
            + """</p> </td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="headers" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">HTTP Security</h3>
                <p> """
            + HTTP_sec
            + """</p> </td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">Headers</h3>
                <p> """
            + headers
            + """</p> </td>
                </tr>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">COOKIES</h3>
                <p> """
            + cookies
            + """</p> </td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">DNS Server</h3>
                <p> """
            + DNS_Server
            + """</p> </td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">TLS Cipher Suites</h3>
                <p>"""
            + tls_cipher_suite
            + """</p></td>
                </tr>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">DNS RECORD INFO</h3>
                <p>"""
            + dns_info
            + """</p></td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">TXT RECORD INFO</h3>
                <p>"""
            + txt_info
            + """</p></td>
            <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">SERVER STATUS</h3>
                <p>"""
            + server_status_info
            + """</p></td>
                </tr>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">EMAIL CONFIGURATION</h3>
                <p>"""
            + mail_configuration_info
            + """</p></td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">REDIRECT CHAIN INFO</h3>
                <p>"""
            + redirect_Record
            + """</p></td>
                <td style="width: 33.3333%; height: 54px;">
                <h3 id="host-names" class="sc-bczSft dfkxtP inner-heading" style="text-align: center;" align="left">REDIRECT CHAIN INFO</h3>
                <p>"""
            + ports
            + """</p></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                <td style="width: 33.3333%; height: 18px;">&nbsp;</td>
                </tr>
                </tbody>
                </table> """
        )

        # save html closing </ body> and </ html> tags to a variable named "footer"
        footer = (
            """
             <script>
                const td_ele = document.querySelectorAll("td");
                function change_td_ele_color() {
                    for (let i = 0; i < td_ele.length; i++) { // iterate all thorugh td
                        if(td_ele[i].innerText.includes("malicious")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/malicious/g,'<span style="color:red">malicious</span>');                            
                        }
                        if(td_ele[i].innerText.includes("malware")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/malware/g,'<span style="color:red">malware</span>');                            
                        }
                        if(td_ele[i].innerText.includes("suspicious")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/suspicious/g,'<span style="color:orange">suspicious</span>');                            
                        }
                        if(td_ele[i].innerText.includes("undetected")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/undetected/g,'<span style="color:grey">undetected</span>');                            
                        }
                        if(td_ele[i].innerText.includes("unrated")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/unrated/g,'<span style="color:grey">unrated</span>');                
                        }
                        if(td_ele[i].innerText.includes("harmless")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/harmless/g,'<span style="color:green">harmless</span>');                            
                        }
                        if(td_ele[i].innerText.includes("clean")){
                            var ele = td_ele[i];
                            var html = ele.innerHTML;
                            td_ele[i].innerHTML = html.replace(/clean/g,'<span style="color:green">clean</span>');                            
                        }
                    }
                }        
                change_td_ele_color();
            </script>
            <h2 align="right">Developed by : """
            + config.AUTHOR
            + """  """
            + config.YEAR
            + """ ver: """
            + config.VERSION
            + """</h2>
            </body>
            </html>
        """
        )
        # create and open the new VirusTotalReport.html file
        timestamp = int(datetime.datetime.now().timestamp())
        file_name_html = "%s_%s.html" % (
            config.REPORT_FILE_NAME.replace("/", "_"),
            timestamp,
        )

        await self.__create_dirs("output")

        file_name_html = os.path.join("./output", file_name_html)

        with open(file_name_html, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(report_timestamp)
            f.write(body)
            # for x in self.__html:
            #     f.write(x)
            f.write(footer)

        if os.name == "nt":
            filenameH = file_name_html.partition("./output\\")[-1]
        else:
            filenameH = file_name_html.partition("output/")[-1]

        print(
            Fore.GREEN + Style.BRIGHT + f"\n[+] HTML" + Fore.WHITE + Style.BRIGHT,
            filenameH,
            Fore.GREEN + Style.BRIGHT + f"File Is Ready",
            Fore.RESET,
        )
