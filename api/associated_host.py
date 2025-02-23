import aiohttp
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config
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
        output = []

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
        rep_data = []
        html = ""
        if not data:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage, html = await self.__associated_host_score(data)
            table = (f"""<table>
                    <tr>
                        <td colspan="1">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                            </div>
                        </td>
                </tr>
                {''.join(
                    f'<tr><td>{subdomain}</td></tr>' for subdomain in sorted(data))}
            </table>""")

        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __associated_host_score(self, hosts):
        score = 0
        max_score = 1  # 6 parameters to evaluate
        issues = []
        suggestions = []
        html_tags = ""

        if hosts:
            main_domains = set(self.domain for host in hosts)

            if len(main_domains) == 1:
                score += 1
            else:
                issues.append(Issue_Config.ISSUE_ASSO_HOSTS)
                suggestions.append(Issue_Config.SUGGESTION__ASSO_HOSTS)

        percentage_score = (score / max_score) * 100
        # html_tags = await self.__analysis_table(issues, suggestions, int(percentage_score))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_ASSOCIATED_HOSTS, Configuration.MODULE_ASSOCIATED_HOSTS, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags