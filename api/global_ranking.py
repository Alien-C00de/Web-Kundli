import aiohttp
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config

class Global_Ranking:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Global_Rank(self):
        config = Configuration()
        self.Error_Title = config.GLOBAL_RANKING
        output = []

        try:
            # print("global_ranking.py: start ")
            async with aiohttp.ClientSession() as session:
                endpoint = f"{config.TRANCO_ENDPOINT_URL}{self.domain}"
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        ranks = data.get("ranks", [])

            output = await self.__html_table(ranks)
            print(f"✅ {config.MODULE_GLOBAL_RANK} has successfully completed.")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Global_Rank : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, ranks):
        rep_data = []
        html = ""
        if ranks:
            # Find the latest date in the ranks data
            latest_rank = max(ranks, key=lambda x: x["date"])
            latest_date = latest_rank["date"]
            latest_rank_value = latest_rank["rank"]

            percentage, html = await self.__global_rank_score(latest_rank_value)
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
        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __global_rank_score(self, rank):
        max_score = 2
        score = 0
        issues = []
        suggestions = []

        # Thresholds for rank-based scoring
        high_risk_threshold = 50000
        medium_risk_threshold = 100000

        # Check rank and deduct points based on thresholds
        if rank <= high_risk_threshold:
            issues.append(Issue_Config.ISSUE_GLOBAL_RANK_LOW)
            suggestions.append(Issue_Config.SUGGESTION_GLOBAL_RANK_LOW)
        else:
            score += 1

        if rank <= medium_risk_threshold:
            issues.append(Issue_Config.ISSUE_GLOBAL_RANK_MODERATE)
            suggestions.append(Issue_Config.SUGGESTION_GLOBAL_RANK_MODERATE)
        else:
            score += 1

        # Calculate the vulnerability score percentage
        percentage_score = (score / max_score) * 100
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_GLOBAL_RANK, Configuration.MODULE_GLOBAL_RANK, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags