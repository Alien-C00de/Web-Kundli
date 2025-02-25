from datetime import datetime, timezone
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config
from colorama import Fore, Style
import whois
import re

class Domain_Whois():
    Error_Title = None
    
    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Whois_Info(self):
        config = Configuration()
        self.Error_Title = config.WHOIS
        output = []
        try:
            # print("domain_whois.py: start")
            domain_info =  whois.whois(self.domain)
            output = await self.__html_table(domain_info)
            # print("domain_whois.py: output: ")
            return output
        except Exception as ex:
            if len(ex.args) > 1 and ex.args[1]:
                error_msg = str(ex.args[0]) + " : " + str(ex.args[1])
            else:
                error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Whois_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, domain_info):
        rep_data = []
        html = ""
        whois_server = ""
        if domain_info.whois_server is not None:
            whois_server = domain_info.whois_server
        else:
            whois_server = domain_info.registrar_url
        

        if not domain_info:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage, html = await self.__whois_score(domain_info.registrar, str(domain_info.creation_date), str(domain_info.updated_date), str(domain_info.expiration_date))
            table = """<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>Registered Domain</td>
                            <td>""" + str(domain_info.domain) + """</td>
                        </tr>
                        <tr>
                            <td>Creation Date</td>
                            <td>""" + str(domain_info.creation_date) +  """</td>
                        </tr>
                        <tr>
                            <td>Updated Date</td>
                            <td>""" + str(domain_info.updated_date) +  """</td>
                        </tr>
                        <tr>
                            <td>Registry Expiry Date</td>
                            <td>""" + str(domain_info.expiration_date) +  """</td>
                        </tr>
                        <tr>
                            <td>Registry Domain ID</td>
                            <td>""" + str(" ") +  """</td>
                        </tr>
                        <tr>
                            <td>Registrar WHOIS Server</td>
                            <td>""" + str(whois_server) +  """</td>
                        </tr>
                        <tr>
                            <td>Registrar</td>
                            <td>""" + str(domain_info.registrar) +  """</td>
                        </tr>
                        <tr>
                            <td>Registrar IANA ID</td>
                            <td>""" + str(domain_info.registrar_iana) +  """</td>
                        </tr>
                    </table>"""
        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __whois_score(self, registrar, creation_date, updated_date, expiry_date):
        score = 100  # Start with full score
        issues = []
        suggestions = []
        
        # Convert dates from string to datetime objects
        creation_dt = await self.__get_date(creation_date)
        # creation_dt = creation_dt.strptime(creation_dt, "%Y-%m-%d %H:%M:%S")
        updated_dt = await self.__get_date(updated_date)
        # updated_dt = updated_dt.datetime.strptime(updated_date, "%Y-%m-%d %H:%M:%S")
        expiry_dt = await self.__get_date(expiry_date) 
        today = datetime.now(timezone.utc)
        
        # Check domain age (older is better)
        domain_age = (today.replace(tzinfo=None) - creation_dt.replace(tzinfo=None)).days
        if domain_age < 365:
            score -= 20
            issues.append(Issue_Config.ISSUE_WHOIS_DOMAIN_AGE)
            suggestions.append(Issue_Config.SUGGESTION_WHOIS_DOMAIN_AGE)
        
        # Check time to expiration (short expiry can be a red flag)
        days_to_expiry = (expiry_dt.replace(tzinfo=None) - today.replace(tzinfo=None)).days
        if days_to_expiry < 180:
            score -= 30
            issues.append(Issue_Config.ISSUE_WHOIS_EXPIRY)
            suggestions.append(Issue_Config.SUGGESTION_WHOIS_EXPIRY)
        
        # Check update frequency (recent updates are better)
        days_since_update = (today.replace(tzinfo=None) - updated_dt.replace(tzinfo=None)).days
        if days_since_update > 365:
            score -= 15
            issues.append(Issue_Config.ISSUE_WHOIS_UPDATE_FREQUNCY)
            suggestions.append(Issue_Config.SUGGESTION_WHOIS_UPDATE_FREQUNCY)
        
        if registrar and "Error" not in registrar:
            registrar_result = await self.__check_registrar_reputation(registrar)
            score = min(score, registrar_result['score'])
            if registrar_result['status'] != "Trusted":
                issues.append(f"Registrar '{registrar}' is {registrar_result['status']}.")
                suggestions.append(registrar_result['suggestion'])
        else:
            issues.append(Issue_Config.ISSUE_WHOIS_REGISTRAR)
            suggestions.append(Issue_Config.SUGGESTION_WHOIS_REGISTRAR)
        
        # Ensure score remains within bounds
        score = max(0, min(100, score))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_DOMAIN_WHOIS, Configuration.MODULE_DOMAIN_WHOIS, issues, suggestions, int(score))
        return int(score), html_tags
    
    
    async def __get_date(self, creation_date_str):
        # Check if creation_date_str is a string that looks like a list of datetime objects
        if creation_date_str.startswith('['):
            # Use regex to extract the first datetime object from the string
            match = re.search(r'datetime\.datetime\(([^)]+)\)', creation_date_str)
            if match:
                # Parse the extracted datetime string into a datetime object
                return datetime(*map(int, match.group(1).split(', ')))
        else:
            # Parse the creation_date string
            return datetime.strptime(creation_date_str, "%Y-%m-%d %H:%M:%S")

    async def __check_registrar_reputation(self, registrar):
        """
        Checks the reputation of a given domain registrar.
        """
        trusted_registrars = [
            "GoDaddy.com, LLC", "Google Domains", "Namecheap, Inc.", 
            "Cloudflare, Inc.", "Gandi SAS", "Tucows Domains Inc."
        ]
        flagged_registrars = [
            "Alibaba Cloud Computing", "Freenom", "PDR Ltd. d/b/a PublicDomainRegistry.com"
        ]
        
        if registrar in trusted_registrars:
            return {"score": 100, "status": Issue_Config.ISSUE_WHOIS_REGISTRAR_TRUSTED, "suggestion": Issue_Config.SUGGESTION_WHOIS_REGISTRAR_TRUSTED}
        elif registrar in flagged_registrars:
            return {"score": 50, "status": Issue_Config.ISSUE_WHOIS_REGISTRAR_FLAGGED, "suggestion": Issue_Config.SUGGESTION_WHOIS_REGISTRAR_FLAGGED}
        else:
            return {"score": 70, "status": Issue_Config.ISSUE_WHOIS_REGISTRAR_NEUTRAL, "suggestion": Issue_Config.SUGGESTION_WHOIS_REGISTRAR_NEUTRAL}