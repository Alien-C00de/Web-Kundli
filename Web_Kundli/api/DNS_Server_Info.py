import aiohttp
import asyncio
import socket
from urllib.parse import urlparse
from util.config_uti import Configuration
from colorama import Fore, Style


class DNS_Server_Info():
    Error_Title = None

    def __init__(self, ip_address, url):
        self.ip_address = ip_address
        self.url = url

    async def Get_DNS_Server_Info(self):
        # Get the IP address
        config = Configuration()
        self.Error_Title = config.DNS_SERVER
        DoH = None
        output = ""
        domain = urlparse(self.url).netloc
        dns_servers = []

        try:
            hostname = socket.gethostbyaddr(self.ip_address)[0].encode('idna').decode('utf-8')
            doh_url = f"https://{self.ip_address}/dns-query"

            async with aiohttp.ClientSession() as session:
                async with session.get(doh_url) as response:
                    if response.status == 200 : DoH = "Yes"

            output = await self.__formatting_Output(hostname, DoH)
        except (socket.herror, UnicodeError) as e:
            error_msg = e.strerror
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        except aiohttp.ClientConnectorError:
            DoH = "No"
            output = await self.__formatting_Output(hostname, DoH)
            return output
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        # finally:

    async def __formatting_Output(self, hostname, DoH):
        htmlValue = ""
        htmlValue = await self.__html_table(hostname, DoH)
        return str(htmlValue)

    async def __html_table(self, hostname, DoH):
        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">IP Address</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(self.ip_address)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Hostname</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(hostname)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">DoH Support</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(DoH)
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
