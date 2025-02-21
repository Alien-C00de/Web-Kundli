import os
import time
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from util.config_uti import Configuration

class Analysis_Report:
    def __init__(self, domain, timestamp):
        self.domain = domain
        self.timestamp = timestamp

    async def Generate_Analysis_Report(self, website, cookies, server_location, server_info, SSL_Cert, Archive, Asso_Host):

        config = Configuration()
        # report_timestamp = str(time.strftime("%A %d-%b-%Y %H:%M:%S", self.timestamp))
        report_timestamp = self.timestamp.strftime("%A %d-%b-%Y %H:%M:%S")

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
                                height: 40px;
                            }
                            .header h1 {
                                color: #00FF00;
                                margin: 0;
                                font-size: 2em;
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
                                background: rgb(169, 128, 246);
                                color: #0f0f0e;
                                padding: 5px;
                                font-size: 1em;
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
                            .date {
                                padding: 5px;
                                margin-right: 20px;
                            }
                            .date h3 {
                                margin: 0;
                                font-size: 0.8em;
                                align-items: center;
                            }
                            .footer {
                                background-color: rgb(189, 189, 204);
                                color: #fff;
                                display: flex;
                                align-items: center;
                                text-align: center; 
                                justify-content: center;
                                margin-right: 10px;
                                margin-left: 10px;
                                height: 30px;
                            }
                            .footer h3{
                                font-size: 0.9em;
                                align-items: center;
                                color: #0f0f0e;
                                margin-right: 10px;
                                margin-left: 10px;
                            }
                        </style>
                    </head>"""
        )
        body = (
                """<body>
                        <div class="header">
                            <h2 align="left"; margin-left: 20px; style="color:#FFA500;">""" + config.REPORT_HEADER + """ <h2>
                            <h1 align="center"; style="color:#00FF00;"> """ + config.ANALYSIS_REPORT_HEADER + """ <i class="fas fa-heartbeat" icon-color></i> </h1>
                            <h2 align="right"; margin-right: 40px; style="color:#FFA500;">""" + website + """</h2>
                        </div>
                        <div class="date">
                            <h3 align="right" ; margin-right: 10px;  align-items: center; style="color:blue;">""" + report_timestamp + """</h3>
                        </div>
                        <div class="container main">
                            """ + cookies + """
                            """ + server_location + """
                            """ + server_info + """
                            """ + SSL_Cert + """
                            """ + Archive + """
                            """ + Asso_Host + """
                        </div>

                        <div class="footer">
                            <h3 align="center";> """ + config.ANALYSIS_REPORT_FOOTER + """&nbsp;&nbsp;&copy;&nbsp;""" + config.YEAR + """ </h3>
                        </div>
                        
                    </body>
                    </html>""" )

        Analysis_report = "%s_%s_%s.html" % (config.ANALYSIS_REPORT_FILE_NAME.replace("/", "_"), self.domain, self.timestamp.strftime("%d%b%Y_%H-%M-%S"))

        Analysis_report = os.path.join("./output", Analysis_report)

        with open(Analysis_report, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(body)