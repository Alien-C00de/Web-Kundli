import os
from colorama import Back, Fore, Style
from util.config_uti import Configuration

class Analysis_Report:
    def __init__(self, domain, timestamp):
        self.domain = domain
        self.timestamp = timestamp

    async def Generate_Analysis_Report(self, website, cookies, server_location, server_info, SSL_Cert, Archive, Asso_Host, Block_Detect,
                            CO2_print, crawl_rule, DNS_Security, DNS_Server, whois, http_security, web_header, firewall, global_rank,
                            open_ports, redirect_chain, security_TXT, server_status, site_feature, social_tags, tech_stack, threats,
                            dns_records, txt_records, tls_cipher_suit, email_config, nmap_ops):

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
                                    margin-bottom: 15px;
                                    padding: 10px;
                                    border-radius: 4px;
                                }
                                .cookies { background: #6600cc; }
                                .carbon { background: #0066cc; }
                                .dns { background: #cc6600; }
                                .report { background: #656563; }
                                .section .refresh {
                                    color: #00FF00;
                                    font-size: 30px;
                                }
                                .issues {
                                    background: #e74c3c;
                                    padding: 10px;
                                    margin-bottom: 5px;
                                    border-radius: 5px;
                                }
                                .suggestions {
                                    background: #2ecc71;
                                    padding: 10px;
                                    margin-top: 5px; 
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
                                    margin-top: 10px;
                                    margin-bottom: 10px;
                                }
                                .score-container {
                                    font-family: Arial, sans-serif;
                                    font-size: 20px;
                                    text-align: center;
                                    padding: 10px;
                                    width: 90%;
                                    margin: auto;
                                    border-radius: 10px;
                                    color: white;
                                    font-weight: bold;
                                }   
                                .excellent { background-color: green; }
                                .moderate { background-color: orange; }
                                .poor { background-color: red; }
                                .very-poor { background-color: darkred; }
                            </style>
                        </head>""")
        script = ("""<script>
                    function getURLParameter(name) {
                        const urlParams = new URLSearchParams(window.location.search);
                        return urlParams.get(name);
                    }

                    function displayValueAndCategorize() {
                        const reportValue = getURLParameter('report');  // Fetch 'report' parameter
                        let scoreValue = document.getElementById('passedValue');
                        let scoreDisplay = document.getElementById("scoreDisplay");
                        let healthStatus = document.getElementById("healthStatus");

                        if (reportValue) {
                            let numericScore = parseFloat(reportValue); // Convert to float for decimal support
                            scoreValue.innerText = numericScore.toFixed(2);
                            categorizeHealth(numericScore);
                        } else {
                            scoreValue.innerText = 'No value passed';
                            healthStatus.innerText = "N/A";
                            scoreDisplay.className = "score-container";
                        }
                    }

                    function categorizeHealth(score) {
                        let container = document.getElementById("scoreDisplay");
                        let statusText = document.getElementById("healthStatus");

                        if (score >= 80) {
                            statusText.innerText = "Excellent";
                            container.className = "score-container excellent";
                        } else if (score >= 60) {
                            statusText.innerText = "Moderate";
                            container.className = "score-container moderate";
                        } else if (score >= 40) {
                            statusText.innerText = "Poor";
                            container.className = "score-container poor";
                        } else {
                            statusText.innerText = "Very Poor";
                            container.className = "score-container very-poor";
                        }
                    }
                </script>""")
        body = ("""<body onload="displayValueAndCategorize()">
                    <div class="container">
                        <div class="header">
                            <h1><i class="fas fa-user-secret icon"></i>&nbsp;""" + config.REPORT_HEADER + """</h1>
                            <h2>""" + config.ANALYSIS_REPORT_HEADER + """</h2>
                            <h3><a href=""" + website + """ style="color: #222; text-decoration: none;">""" + website + """</a></h3>
                        </div>
                        <div class="timestamp">
                            <i class="far fa-clock"></i> Report Generated: """  + report_timestamp + """
                        </div>
                        <div class="section report">
                            <h2><i class="fas fa-chart-bar refresh"></i>&nbsp;&nbsp;&nbsp;Final Score&nbsp;= <span id="passedValue"></span>%</h2>
                            <p style="padding-left: 50px;"><strong>80%+ → Excellent : ✅ </strong> Well-optimized with minimal issues.</p>
                            <p style="padding-left: 50px;"><strong>60-79% → Moderate : ⚠️  </strong> Needs some improvements.</p>
                            <p style="padding-left: 50px;"><strong>40-59% → Poor ❌ </strong> Several issues require attention.</p>
                            <p style="padding-left: 50px;"><strong>Below 40% → Very Poor 🚨 </strong> Critical issues, urgent action needed.</p>
                            <div id="scoreDisplay" class="score-container">
                                Health Status: <span id="healthStatus"></span>
                            </div>
                        </div>
                                """ + server_location + """
                                """ + SSL_Cert + """
                                """ + whois + """
                                """ + server_info + """
                                """ + web_header + """
                                """ + cookies + """
                                """ + http_security + """
                                """ + DNS_Server + """
                                """ + tls_cipher_suit + """
                                """ + dns_records + """
                                """ + txt_records + """ 
                                """ + server_status + """
                                """ + email_config + """
                                """ + redirect_chain + """
                                """ + open_ports + """
                                """ + Archive + """
                                """ + Asso_Host + """
                                """ + Block_Detect + """
                                """ + CO2_print + """
                                """ + crawl_rule + """
                                """ + site_feature + """
                                """ + DNS_Security + """
                                """ + tech_stack + """
                                """ + firewall + """
                                """ + social_tags + """
                                """ + threats + """
                                """ + global_rank + """
                                """ + security_TXT + """ """)
        if nmap_ops:
            body += (f"""
                                """ + nmap_ops[1] + """
                                """ + nmap_ops[3] + """
                                """ + nmap_ops[5] + """
                                """ + nmap_ops[7] + """
                                """ + nmap_ops[9] + """
                                """ + nmap_ops[11] + """
                                """ + nmap_ops[13] + """
                                """ + nmap_ops[15] + """ """)
        body += ("""
                            <footer>
                                """ + config.ANALYSIS_REPORT_FOOTER + """&nbsp;&nbsp;&copy;&nbsp;""" + config.YEAR + """
                            </footer>
                    </div>
                </body>
                </html>""" )

        if nmap_ops:
            Analysis_report = "%s_%s_%s_%s.html" % (config.ANALYSIS_REPORT_FILE_NAME, self.domain, 'nmap', self.timestamp.strftime("%d%b%Y_%H-%M-%S"))
        else:    
            Analysis_report = "%s_%s_%s.html" % (config.ANALYSIS_REPORT_FILE_NAME, self.domain, self.timestamp.strftime("%d%b%Y_%H-%M-%S"))

        Analysis_report = os.path.join("./output", Analysis_report)

        with open(Analysis_report, "a", encoding="UTF-8") as f:
            f.write(header)
            f.write(script)
            f.write(body)