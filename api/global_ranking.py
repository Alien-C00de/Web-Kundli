import aiohttp
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class Global_Ranking:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Global_Rank(self):
        config = Configuration()
        self.Error_Title = config.THREATS
        output = ""

        try:
            # print("global_ranking.py: start ")
            async with aiohttp.ClientSession() as session:
                endpoint = f"{config.TRANCO_ENDPOINT_URL}{self.domain}"
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        ranks = data.get("ranks", [])

            output = await self.__html_table(ranks)
            # print("global_ranking.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Global_Rank : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, ranks):

        if ranks:
            # Find the latest date in the ranks data
            latest_rank = max(ranks, key=lambda x: x["date"])
            latest_date = latest_rank["date"]
            latest_rank_value = latest_rank["rank"]

            percentage = await self.__rating(latest_date, latest_rank_value)
            table = f"""<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>Date</td>
                            <td>{latest_date}</td>
                        </tr>
                        <tr>
                            <td>Rank</td>
                            <td>{latest_rank_value}</td>
                        </tr>
                    </table>"""
        else:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        return table

    async def __rating(self, date, value):

        if  value:
            percentage = 100
        else:
            percentage = 0

        return percentage
