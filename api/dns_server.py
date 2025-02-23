import aiohttp
import socket
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config
from colorama import Fore, Style

class DNS_Server():
    Error_Title = None

    def __init__(self, ip_address, url, domain):
        self.ip_address = ip_address
        self.url = url
        self.domain = domain

    async def Get_DNS_Server(self):
        config = Configuration()
        self.Error_Title = config.DNS_SERVER
        DoH = "No"
        output = ""

        try:
            # print("dns_server_info.py: start)
            doh_url = f"https://{self.ip_address}/dns-query"

            async with aiohttp.ClientSession() as session:
                async with session.get(doh_url) as response:
                    if response.status == 200 : DoH = "Yes"

            output = await self.__html_table(DoH)
        except (socket.herror, UnicodeError) as e:
            error_msg = e.strerror
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            output = await self.__html_table(DoH)
            return output
        except aiohttp.ClientConnectorError:
            output = await self.__html_table(DoH)
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            output = await self.__html_table(DoH)
            return output

    async def __html_table(self, DoH):
        rep_data = []
        html = ""
        if not DoH:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage, html = await self.__DNS_Server_score(DoH)
            table = (
                """<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>IP Address</td>
                            <td>""" + str(self.ip_address) + """</td>
                        </tr>
                        <tr>
                            <td>Hostname</td>
                            <td>""" + str(self.domain) + """</td>
                        </tr>
                        <tr>
                            <td>DoH Support</td>
                            <td>""" + str(DoH) + """</td>
                        </tr>
                    </table>"""
            )
        rep_data.append(table)
        rep_data.append(html)
        return rep_data
    
    async def __DNS_Server_score(self, DoH):

        issues = []
        suggestions = []
        html_tags = ""
        percentage = 0

        if DoH:
            # Session Name - Should not be empty or generic
            if DoH.upper() == 'NO':
                issues.append(Issue_Config.ISSUE_DNS_SERVER)
                suggestions.append(Issue_Config.SUGGESTION_DNS_SERVER)
                percentage = 50
            else:
                percentage = 100
    
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.MODULE_DNS_SERVER, issues, suggestions, int(percentage))

        return int(percentage), html_tags