from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class Tech_Stack:
    Error_Title = None

    def __init__(self, url, response, domain):
        self.url = url
        self.response = response
        self.domain = domain

    async def Get_Tech_Stack(self):
        config = Configuration()
        self.Error_Title = config.TECH_STACK
        output = ""

        try:
            # print ("tech_stack.py: start ")
            # response = requests.head(self.url, allow_redirects=True)
            self.response.raise_for_status()

            if self.response.headers:
                technologies = {
                        'Server': self.response.headers.get('Server', 'Unknown'),
                        'X-Powered-By': self.response.headers.get('X-Powered-By', 'Not specified'),
                        'X-AspNet-Version': self.response.headers.get('X-AspNet-Version', 'Not specified'),
                    }
            else:
                technologies = None

            output = await self.__html_table(technologies)
            # print("tech_stack.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Tech_Stack : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, data):
        if not data:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage = 100
            rows = [
                f"""
                <tr>
                    <td>{key}</td>
                    <td>{value}</td>
                </tr>"""
                for key, value in data.items()
            ]

            table = f"""
            <table>
                <tr>
                    <td colspan="2">
                        <div class="progress-bar-container">
                            <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                        </div>
                    </td>
                </tr>
                    {''.join(rows)}
            </table>"""

        return table
