import os
from colorama import Back, Fore, Style
from util.config_uti import Configuration

class Analysis_Report:
    def __init__(self, domain, timestamp):
        self.domain = domain
        self.timestamp = timestamp

    async def Generate_Analysis_Report(self, website, cookies, server_location, server_info, SSL_Cert, Archive, Asso_Host, Block_Detect,
                            CO2_print, crawl_rule, DNS_Security, DNS_Server, whois, http_security, web_header, firewall, global_rank,
                            open_ports, redirect_chain, security_TXT, server_status, site_feature, social_tags, tech_stack, threats):

        config = Configuration()
        report_timestamp = self.timestamp.strftime("%A %d-%b-%Y %H:%M:%S")

        header = ("""<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Web Health Analysis Report</title>
                            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
                            <style>
                                body {
                                    font-family: Arial, sans-serif;
                                    background-color: #1e1e1e;
                                    color: #ffffff;
                                    margin: 0;
                                    padding: 20px;
                                }
                                .container {
                                    max-width: 900px;
                                    margin: auto;
                                    background: #444;
                                    padding: 20px;
                                    border-radius: 10px;
                                    box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
                                }
                                .header {
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    background: #ffcc00;
                                    color: #222;
                                    padding: 15px;
                                    border-radius: 5px;
                                }
                                .header h1, .header h2, .header h3 {
                                    margin: 0;
                                }
                                .header .icon {
                                    
                                    font-size: 40px;
                                }
                                .section {
                                    margin-bottom: 20px;
                                    padding: 15px;
                                    border-radius: 8px;
                                }
                                .cookies { background: #6600cc; }
                                .carbon { background: #0066cc; }
                                .dns { background: #cc6600; }
                                .section .refresh {
                                    color: #FFA500;
                                    font-size: 30px;
                                }
                                .issues {
                                    background: #e74c3c;
                                    padding: 10px;
                                    border-radius: 5px;
                                }
                                .suggestions {
                                    background: #2ecc71;
                                    padding: 10px;
                                    border-radius: 5px;
                                }
                                ul {
                                    margin: 5px 0 0;
                                    padding-left: 20px;
                                }
                                footer {
                                    text-align: center;
                                    padding: 10px;
                                    margin-top: 20px;
                                    background: #ffcc00;
                                    color: #222;
                                    border-radius: 5px;
                                }
                                .timestamp {
                                    text-align: right;
                                    font-size: 14px;
                                    margin-bottom: 10px;
                                }
                            </style>
                        </head>""")
        body = ("""<body>
                    <div class="container">
                        <div class="header">
                            <h1><i class="fas fa-globe icon"></i>&nbsp;""" + config.REPORT_HEADER + """</h1>
                            <h2>""" + config.ANALYSIS_REPORT_HEADER + """</h2>
                            <h3><a href=""" + website + """ style="color: #222; text-decoration: none;">""" + website + """</a></h3>
                        </div>
                        <div class="timestamp">
                            <i class="far fa-clock"></i> Report Generated: """  + report_timestamp + """
                        </div>
                                """ + cookies + """
                                """ + server_location + """
                                """ + server_info + """
                                """ + SSL_Cert + """
                                """ + Archive + """
                                """ + Asso_Host + """
                                """ + Block_Detect + """
                                """ + CO2_print + """
                                """ + crawl_rule + """
                                """ + DNS_Security + """
                                """ + DNS_Server + """
                                """ + whois + """
                                """ + http_security + """
                                """ + web_header + """
                                """ + firewall + """
                                """ + firewall + """
                                """ + global_rank + """
                                """ + open_ports + """
                                """ + redirect_chain + """
                                """ + security_TXT + """
                                """ + server_status + """
                                """ + site_feature + """
                                """ + social_tags + """
                                """ + tech_stack + """
                                """ + threats + """
                            <footer>
                                """ + config.ANALYSIS_REPORT_FOOTER + """&nbsp;&nbsp;&copy;&nbsp;""" + config.YEAR + """
                            </footer>
                    </div>
                </body>
                </html>""" )

        Analysis_report = "%s_%s_%s.html" % (config.ANALYSIS_REPORT_FILE_NAME.replace("/", "_"), self.domain, self.timestamp.strftime("%d%b%Y_%H-%M-%S"))

        Analysis_report = os.path.join("./output", Analysis_report)

        with open(Analysis_report, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(body)