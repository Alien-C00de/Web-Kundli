import aiohttp
import socket
from util.config_uti import Configuration
from util.report_util import Report_Utility
from colorama import Fore, Style

class DNS_Server():
    Error_Title = None

    def __init__(self, ip_address, url, domain):
        self.ip_address = ip_address
        self.url = url
        self.domain = domain

    async def Get_DNS_Server(self):
        # Get the IP address
        config = Configuration()
        self.Error_Title = config.DNS_SERVER
        DoH = None
        output = ""

        try:
            # print("dns_server_info.py: start)
            doh_url = f"https://{self.ip_address}/dns-query"

            async with aiohttp.ClientSession() as session:
                async with session.get(doh_url) as response:
                    if response.status == 200 : DoH = "Yes"

            output = await self.__formatting_Output(self.domain, DoH)
            # print("dns_server_info.py: output: ")
        except (socket.herror, UnicodeError) as e:
            error_msg = e.strerror
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        except aiohttp.ClientConnectorError:
            DoH = "No"
            output = await self.__html_table(DoH)
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        # finally:


    async def __html_table(self, DoH):

        if not DoH:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage = await self.__rating(self.ip_address, self.domain, DoH)
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
        return table
    
    async def __rating(self, ip, domain, DoH):

        condition1 = ip != None
        condition2 = domain != None
        condition3 = DoH != None

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3])
        
        # Determine the percentage based on the number of satisfied conditions
        if satisfied_conditions == 3:
            percentage = 100
        elif satisfied_conditions == 2:
            percentage = 66
        elif satisfied_conditions == 1:
            percentage = 33
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage
