from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility
import re

class Site_Features:
    Error_Title = None

    def __init__(self, url, response, domain):
        self.url = url
        self.response = response
        self.domain = domain

    async def Get_Site_Features(self):
        config = Configuration()
        self.Error_Title = config.SITE_FEATURES
        output = ""
        site_val = []
        features = {
                    'ssl': 'ssl',
                    'javascript': 'javascript-library1|javascript',
                    'framework': 'framework1',
                    'us-hosting': 'us-hosting3',
                    'cloud-hosting': 'cloud-hosting2',
                    'cloud-paas': 'cloud-paas3',
                    'server-location': 'server-location1',
                    'application-performance': 'application-performance1',
                    'audience-measurement': 'audience-measurement2',
                    'dmarc': 'dmarc1' 
                    }
        try:
            # print ("site_feature.py: start")
            output = await self.__html_table(features)
            # print("site_feature.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Site_Features : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __check_feature(self, url, feature):
        try:
            # response = requests.get(url)
            if self.response.status_code == 200:
                html_content = self.response.text
                if re.search(feature + r'[^a-zA-Z0-9_-]', html_content, re.IGNORECASE):
                    return 'Live'
                else:
                    return 'Dead'
            else:
                return 'Error: Unable to fetch URL'
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => __check_feature : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

    async def __html_table(self, data):
        if not data:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage = 100
            # Step 1: Get results asynchronously
            results = [await self.__check_feature(self.url, value) for key, value in data.items()]
            # Step 2: Construct the HTML table
            rows = [
                f"""
                <tr>
                    <td>{key}</td>
                    <td>{result}</td>
                </tr>"""
                for (key, value), result in zip(data.items(), results)
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
