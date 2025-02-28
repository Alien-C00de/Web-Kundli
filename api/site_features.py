import aiohttp
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config
import re
import datetime


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

        try:
            api_url = config.BUILTWITH_ENDPOINT_URL.format(apiKey = config.BUILTWITH_API, url = self.domain)
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if 200 <= response.status <= 299:
                        result = await response.json()  # Convert response to JSON
                    
            output = await self.__html_table(result)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Site_Features : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output


    async def __html_table(self, data):
        if not data:
            report_util = Report_Utility()
            return await report_util.Empty_Table()

        # Define required categories
        required_categories = {"javascript", "widgets", "payment"}
        percentage = 100
        rows = []
        
        for group in data.get("groups", []):
            category_name = group["name"].lower()
            if category_name not in required_categories:
                continue  # Skip categories not in the required list
            
            # Add category header
            rows.append(f'<tr><td><h3>{category_name.capitalize()}</h3></td><td></td></tr>')

            # Add subcategories
            for category in group.get("categories", []):
                sub_name = category.get("name", "Unknown")
                live_count = category.get("live", 0)
                dead_count = category.get("dead", 0)
                dead_text = f" ({dead_count} dead)" if dead_count > 0 else ""
                
                rows.append(f"""
                <tr>
                    <td>{sub_name}</td>
                    <td>{live_count} Live{dead_text}</td>
                </tr>""")


        last_scanned = await self.__convet_epoch(data['last']) # Example, replace with actual timestamp if needed

        table = (
            f"""<table>
                <tr>
                    <td colspan="2">
                        <div class="progress-bar-container">
                            <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                        </div>
                    </td>
                </tr>
                    {''.join(rows)}
                <tr>
                    <td colspan="2" style="text-align: left;"><h4>Last scanned on {last_scanned}</h4></td>
                </tr>
            </table>""")

        return table


    # import datetime

    async def __convet_epoch(self, epoch_time):
        # Epoch time
        # Convert to datetime object
        normal_time = datetime.datetime.fromtimestamp(epoch_time)

        # Format the datetime object into a readable format
        formatted_time = normal_time.strftime("%d %B %Y at %I:%M %p")

        return formatted_time
