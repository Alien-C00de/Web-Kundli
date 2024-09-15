import aiohttp
from colorama import Fore, Style
from urllib.parse import urljoin
from util.config_uti import Configuration

class Crawl_Rules:
    Error_Title = None

    def __init__(self, url):
        self.url = url

    async def Get_Crawl_Rules(self):
        config = Configuration()
        self.Error_Title = config.CRAWL_RULES
        output = ""
        robot_url = urljoin(self.url, config.CRAWL_FILE)
        try:
            # print("crawl_rules.py: start ")
            async with aiohttp.ClientSession() as session:
                async with session.get(robot_url) as response:
                    crawl_rules = []
                    user_agent = ""
                    if response.status == 200:
                        # Parse robots.txt and extract rules
                        lines = (await response.text()).splitlines()
                        
                        for line in lines:
                            if line.lower().startswith("user-agent:"):
                                user_agent = line.split(":")[1].strip()
                            elif line.lower().startswith(("allow:", "disallow:")):
                                rule = line.split(":")[1].strip()
                                crawl_rules.append((user_agent, rule))

            output = await self.__formatting_Output(user_agent, crawl_rules)
            # print("crawl_rules.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Crawl_Rules : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, user_agent, decodedResponse):
        htmlValue = ""
        htmlValue = await self.__html_table(user_agent, decodedResponse)
        return str(htmlValue)

    async def __html_table(self, user_agent, data):

        if data:
            percentage = 100
            table = (
                    """<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                                    </div>
                                </td>
                            </tr>"""
                    + "".join(
                        f"""<tr>
                                <td>User Agent : {user_agent}</td>
                                <td>{rule}</td>
                        </tr>"""
                        for user_agent, rule in data
                    )
                    + """</table>"""
                )
        else:
            percentage = 0
            table = (
                    """<table>
                            <tr>
                                <td colspan="1">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Failed to fetch robots.txt</td>
                            </tr>
                    </table>"""
            )
        return table
