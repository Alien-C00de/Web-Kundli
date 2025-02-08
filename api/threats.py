import aiohttp
import asyncio
import base64
from colorama import Fore, Style
from util.config_uti import Configuration


class Threats:
    Error_Title = None

    def __init__(self, ip_address, url, domain):
        self.ip_address = ip_address
        self.url = url
        self.domain = domain

    async def Get_Threats(self):
        config = Configuration()
        self.Error_Title = config.THREATS
        tasks = []
        decodedResponse = []
        output = ""

        headers = {"Accept": "application/json", "x-apikey": config.VIRUS_TOTAL_API_KEY}
        try:
            # print("Threats.py: start ")
            encoded_url = await self.__url_to_base64(self.url)
            async with aiohttp.ClientSession(headers = headers) as session:
                url = config.VIRUS_TOTAL_ENDPOINT_URL + encoded_url

                tasks.append(asyncio.create_task(session.request(method="GET", url=url)))

                responses = await asyncio.gather(*tasks)
                for response in responses:
                    decodedResponse.append(await response.json())

            output = await self.__formatting_Output(decodedResponse)
            # print("Threats.py: output: ")
            return output

        except Exception as ex:
            if len(ex.args) > 1 and ex.args[1]:
                error_msg = str(ex.args[0]) + " : " + str(ex.args[1])
            else:
                error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Threats : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __url_to_base64(self, url):
        """Encode URL to a format suitable for VirusTotal API."""
        return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    async def __formatting_Output(self, decodedResponse):
        htmlValue = ""
        htmlValue = await self.__html_table(decodedResponse)
        return str(htmlValue)

    async def __html_table(self, decodedResponse):

        if decodedResponse is not None:
            percentage = 0
            table = f"""<table>
                        <tr>
                            <td colspan="1">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>No Data Found</td>
                        </tr>
                    </table>"""

            if 'error' in decodedResponse[0]:
                return table
            else:
                phishing = int(decodedResponse[0]["data"]["attributes"]["last_analysis_stats"]["suspicious"])
                malware = int(decodedResponse[0]["data"]["attributes"]["last_analysis_stats"]["malicious"])

                percentage = await self.__rating(phishing, malware)
                table = f"""<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Phishing Status</td>
                                <td>{'✅ No Phishing Found' if phishing == 0 else '❌ Phishing'}</td>
                            </tr>
                            <tr>
                                <td>Malware Status</td>
                                <td>{'✅ No Malwares Found' if malware == 0 else '❌ Malware Found'}</td>
                            </tr>
                        </table>"""
                return table
        else:
            return table

    async def __rating(self, phishing, malware):

        if phishing > 0 or malware > 0:
            percentage = 0
        else:
            percentage = 100

        return percentage
