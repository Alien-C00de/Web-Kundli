import aiohttp
from util.config_uti import Configuration
from colorama import Fore, Style
from bs4 import BeautifulSoup

class Associated_Hosts:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Associated_Hosts(self):
        config = Configuration()
        self.Error_Title = config.ASSOCIATED_HOSTS
        output = ""

        try:
            # print("associated_host.py: start ")
            subdomains = set()
            async with aiohttp.ClientSession() as session:
                url = config.ASSOCIATED_ENDPOINT_URL.replace("{domain}", self.domain)
                html = await self.__fetch(session, url)
                soup = BeautifulSoup(html, 'html.parser')
                # Extract subdomains from the table in the HTML
                for row in soup.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > 4:
                        subdomain = cells[4].get_text().strip()
                        if subdomain.endswith(self.domain):
                            subdomains.add(subdomain)

            output = await self.__html_table(subdomains)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Associated_Hosts : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

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
