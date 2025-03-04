import dns.asyncresolver
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config

class Mail_Records:

    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain
        self.resolver = dns.asyncresolver.Resolver()
        self.resolver.nameservers = ["8.8.8.8", "1.1.1.1"]  # Google & Cloudflare DNS
        self.resolver.lifetime = 40  # Increase timeout

    async def Get_Mail_Records(self):
        config = Configuration()
        self.Error_Title = config.MAIL_CONFIGURATION
        output=""
        try:
            # print("mail_configration_fetch.py: start")
            result = await self.__fetch_dns_records(self.domain)
            output = await self.__html_table(result)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Mail_Records : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __fetch_dns_records(self, domain):
        """Fetches MX, TXT, and other email security records asynchronously."""
        try:
            mx_records = await self.resolver.resolve(domain, 'MX')
            txt_records = await self.resolver.resolve(domain, 'TXT')
        except Exception as e:
            print(f"DNS Lookup Error: {e}")
            return None

        mx_list = [(mx.exchange.to_text(), mx.preference) for mx in mx_records]
        txt_list = [txt.to_text() for txt in txt_records]

        # Detecting External Mail Services
        external_services = []
        for mx in mx_list:
            if "google" in mx[0]:
                external_services.append("Google Workspace")
            elif "outlook" in mx[0] or "office365" in mx[0]:
                external_services.append("Microsoft 365")
            elif "zoho" in mx[0]:
                external_services.append("Zoho Mail")

        return {
            "mx_records": mx_list,
            "txt_records": txt_list,
            "external_services": external_services
        }

    async def __html_table(self, security_info):
        """Generates an HTML table with mail security details, MX records, and TXT records."""
        rep_data = []
        html = ""

        if not security_info:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            
            mx_records = security_info['mx_records']
            external_services = security_info['external_services']
            txt_records = security_info['txt_records']
            
            # Initialize Mail Security Checklist status
            spf = dkim = dmarc = bimi = "Not Enabled"
            for txt in txt_records:
                if txt.startswith('"v=spf1'):
                    spf = "Enabled"
                if 'dkim' in txt.lower():
                    dkim = "Enabled"
                if 'dmarc' in txt.lower():
                    dmarc = "Enabled"
                if 'bimi' in txt.lower():
                    bimi = "Enabled"
            percentage, html = await self.__security_score(spf, dkim, dmarc, bimi)
            table = f"""<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: {percentage}%;">{percentage}%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td><h3>Mail Security Checklist</h3></td><td></td>
                            </tr>
                            <tr>
                                <td>SPF</td>
                                <td>{"✅ Enabled" if spf == "Enabled" else "❌ Not Enabled"}</td>
                            </tr>
                            <tr>
                                <td>DKIM</td>
                                <td>{"✅ Enabled" if dkim  == "Enabled" else "❌ Not Enabled"}</td>
                            </tr>
                            <tr>
                                <td>DMARC</td>
                                <td>{"✅ Enabled" if dmarc == "Enabled" else "❌ Not Enabled"}</td>
                            </tr>
                            <tr>
                                <td>BIMI</td>
                                <td>{"✅ Enabled" if bimi == "Enabled" else "❌ Not Enabled"}</td>
                            </tr>
                            <tr>
                                <td><h3>MX Records</h3></td><td></td>
                            </tr>
                        """
            # Add MX Records
            if mx_records:
                for mx in mx_records:
                    table += f"<tr><td>{mx[0]}</td><td>Priority: {mx[1]}</td></tr>"
            else:
                table += "<tr><td>No MX records found.</td></tr>"

            # Add External Mail Services
            table += """<tr><td><h3>External Mail Services</h3></td><td></td></tr>"""
            if external_services:
                for service in external_services:
                    table += f"<tr><td>{service}</td><td>External Mail Provider</td></tr>"
            else:
                table += "<tr><td>No external mail services detected.</td></tr>"

            # Add Mail-related TXT Records
            table += """<tr><td><h3>Mail-related TXT Records</h3></td><td></td></tr>"""
            if txt_records:
                for txt in txt_records:
                    table += f"<tr><td>{txt}</td></tr>"
            else:
                table += "<tr><td colspan='1'>No mail-related TXT records found.</td></tr>"

            table += "</table>"

        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __security_score(self, spf, dkim, dmarc, bimi):
        """Calculates security score and generates issue/suggestion report."""
        score = 0
        max_score = 4  # SPF, DKIM, DMARC, BIMI
        issues = []
        suggestions = []

        # Security checks
        if spf == "Enabled": 
            score += 1
        else: 
            issues.append("SPF is missing.")
            suggestions.append("Implement an SPF record to prevent spoofing.")

        if dkim == "Enabled": 
            score += 1
        else: 
            issues.append("DKIM is not configured.")
            suggestions.append("Set up DKIM signatures to validate outgoing emails.")

        if dmarc == "Enabled": 
            score += 1
        else: 
            issues.append("DMARC is missing.")
            suggestions.append("Enable DMARC to prevent phishing attacks.")

        if bimi: 
            score += 1
        else: 
            issues.append("BIMI is not enabled.")
            suggestions.append("Implement BIMI to display your logo in email clients.")

        percentage_score = (score / max_score) * 100

        # Generate analysis report
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_EMAIL_CONFIGURATION, Configuration.MODULE_EMAIL_CONFIGURATION, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags
