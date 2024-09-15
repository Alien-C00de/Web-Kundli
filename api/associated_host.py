import aiohttp
from util.config_uti import Configuration
from colorama import Fore, Style
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Associated_Hosts:
    Error_Title = None

    def __init__(self, url):
        self.url = url

    async def Get_Associated_Hosts(self):
        config = Configuration()
        self.Error_Title = config.ASSOCIATED_HOSTS
        domain = urlparse(self.url).netloc
        output = ""

        try:
            # print("associated_host.py: start ")
            subdomains = set()
            async with aiohttp.ClientSession() as session:
                url = config.ASSOCIATED_ENDPOINT_URL.replace("{domain}", domain)
                html = await self.__fetch(session, url)
                soup = BeautifulSoup(html, 'html.parser')
                # Extract subdomains from the table in the HTML
                for row in soup.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > 4:
                        subdomain = cells[4].get_text().strip()
                        if subdomain.endswith(domain):
                            subdomains.add(subdomain)

            output = await self.__formatting_Output(subdomains)
            # print("associated_host.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Associated_Hosts : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def __formatting_Output(self, decodedResponse):
        htmlValue = ""
        htmlValue = await self.__html_table(decodedResponse)
        return str(htmlValue)

    async def __html_table(self, data):

        percentage = 100

        if not data:
            percentage = 0
            table = f"""
                        <table>
                            <tr>
                                <td colspan="1">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                                    </div>
                                </td>
                            </tr>
                        </table>"""
            return table

        table = (
        f"""<table>
                <tr>
                    <td colspan="1">
                        <div class="progress-bar-container">
                            <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                        </div>
                    </td>
            </tr>
            {''.join(
                f'<tr><td>{subdomain}</td></tr>' for subdomain in sorted(data))}
        </table>""")

        return table
