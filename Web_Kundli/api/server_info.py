import aiohttp
import asyncio
from ipwhois import IPWhois
from util.config_uti import Configuration
from colorama import Fore, Style


class ServerInfo():
    Error_Title = None

    def __init__(self, ip_address, url):
        self.ip_address = ip_address
        self.url = url

    async def Get_Server_Info(self):
        # Get the IP address
        config = Configuration()
        self.Error_Title = config.SERVER_INFO
        tasks = []
        decodedResponse = []
        output = ""

        headers = {'Accept': 'application/json',}

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                # url = config.SHODAN_ENDPOINT_URL + self.ip_address + "?key=" + config.SHODAN_API_KEY
                url = config.SHODAN_ENDPOINT_URL + '8.8.8.8' + "?key=" + config.SHODAN_API_KEY

                tasks.append(asyncio.create_task(session.request(method="GET", url=url)))

                responses = await asyncio.gather(*tasks)
                for response in responses:
                    decodedResponse.append(await response.json())

            output = await self.__formatting_Output(decodedResponse)
            return output

        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, decodedResponse):
        htmlValue = ""        
        htmlValue = await self.__html_table(decodedResponse)
        return str(htmlValue)

    async def __html_table(self, data):
        table = """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Organization</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(data[0]['org']) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">ASN Code</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(data[0]['asn']) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Ports</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(data[0]["ports"]) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">IP</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(data[0]["ip_str"]) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Type</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(data[0]["tags"]) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Location</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(data[0]["city"]) + ", " + str(data[0]["country_name"]) +  """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        return table
