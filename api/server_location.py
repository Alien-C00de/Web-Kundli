import pandas as pd
import aiohttp
import asyncio
from util.config_uti import Configuration
from util.issue_config import Issue_Config
from util.report_util import Report_Utility
from colorama import Fore, Style

class Server_Location():
    Error_Title = None

    def __init__(self, ip_address, domain):
        self.ip_address = ip_address
        self.domain = domain

    async def Get_Server_Location(self):
        config = Configuration()
        self.Error_Title = config.SERVER_LOCATION
        tasks = []
        decodedResponse = []
        location = []
        info = [] 
        output = []

        headers = {'Accept': 'application/json',}

        try:
            # print("server_location.py: start")
            async with aiohttp.ClientSession(headers=headers) as session:
                url = config.IPAPI_IO_ENDPOINT_URL + self.ip_address + "/json/"
                tasks.append(asyncio.create_task(session.request(method="GET", url=url)))

                responses = await asyncio.gather(*tasks)
                for response in responses:
                    decodedResponse.append(await response.json())

            dataframe = pd.DataFrame.from_dict(decodedResponse[0], orient='index')
            location = await self.__html_server_loc_table(dataframe)
            info = await self.__html_server_info_table(dataframe)
            output = location + info
            # print("server_location.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Server_Location : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_server_info_table(self, dataframe):
        rep_data = []
        html = ""
        if dataframe.empty:
            percentage = 0
            report_util = Report_Utility()
            table = report_util.Empty_Table()
        else:
            org = str(dataframe[0]["org"])
            asn = str(dataframe[0]["asn"])
            ip = str(dataframe[0]["ip"])
            location =  str(dataframe[0]["region"]) + ",\n " + str(dataframe[0]["country_name"])

            percentage, htmltags = await self.__server_info_score(org, asn, ip, location)

            table = """<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width:""" + str(percentage) + """%;">""" + str(percentage) + """%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Organization</td>
                                <td>""" + org +  """</td>
                            </tr>
                            <tr>
                                <td>ASN Code</td>
                                <td>""" + asn +  """</td>
                            </tr>
                            <tr>
                                <td>IP</td>
                                <td>""" + ip +  """</td>
                            </tr>
                            <tr>
                                <td>Location</td>
                                <td>""" + location +  """</td>
                            </tr>
                    </table>"""

        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __html_server_loc_table(self, dataframe):
        rep_data = []
        html = ""
        if dataframe.empty:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            city =  str(dataframe[0]["city"])
            postal = str(dataframe[0]["postal"])
            region = str(dataframe[0]["region"])
            country = str(dataframe[0]["country_name"])
            country_code = str(dataframe[0]["country_code"]).lower()
            timezone = str(dataframe[0]["timezone"])
            languages =  str(dataframe[0]["languages"])
            currency_name = str(dataframe[0]["currency_name"])
            currency = str(dataframe[0]["currency"])

            percentage, html = await self.__server_Location_score(city, country, timezone, languages, currency)

            table = """<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width:""" + str(percentage) + """%;">""" + str(percentage) + """%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>City</td>
                                <td>""" + postal + ", " + city + ", " + region + """</td>
                            </tr>
                            <tr>
                                <td>Country</td>
                                <td> """ + country + """ <span id="country-icon" class="flag-icon"></span></td>
                            </tr>
                            <tr>
                                <td>Timezone</td>
                                <td>""" + timezone +  """</td>
                            </tr>
                            <tr>
                                <td>Languages</td>
                                <td>""" + languages +  """</td>
                            </tr>
                            <tr>
                                <td>Currency</td>
                                <td>""" + currency_name  + "  (" + currency + ")" """</td>
                            </tr>
                    </table>
                    <script>
                        function displayCountryIcon() {
                            const countryIconElement = document.getElementById('country-icon');
                            countryIconElement.className = 'flag-icon flag-icon-$ """ + country_code + """';
                        }
                        displayCountryIcon();
                    </script>"""
        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __server_Location_score(self, city, country, timezone, languages, currency):

        issue_config = Issue_Config()
        total_score = 0
        total_weight = 100  # Max total score

        issues = []
        suggestions = []

        # Weights assigned to each parameter (equally distributed here)
        parameter_weight = total_weight / 5  # 5 parameters: City, Country, Timezone, Languages, Currency

        # Check City
        if city != "Unknown" and city != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LOCATION_CITY)
            suggestions.append(issue_config.SUGGESTION_LOCATION_CITY)

        # Check Country
        if country != "Unknown" and country != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LOCATION_COUNTRY)
            suggestions.append(issue_config.SUGGESTION_LOCATION_COUNTRY)

        # Check Timezone
        if timezone != "Unknown" and timezone != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LOCATION_TIMEZONE)
            suggestions.append(Issue_Config.SUGGESTION_LOCATION_TIMEZONE)

        # Check Languages
        if languages != "Unknown" and languages != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LOCATION_LANGUAGES)
            suggestions.append(issue_config.SUGGESTION_LOCATION_LANGUAGES)

        # Check Currency
        if currency != "Unknown" and currency != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LOCATION_CURRENCY)
            suggestions.append(issue_config.SUGGESTION_LOCATION_CURRENCY)

        # Calculate percentage score
        percentage_score = (total_score / total_weight) * 100
        # html_tags = await self.__analysis_location_table(issues, suggestions, int(security_score_percentage))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.MODULE_SERVER_LOCATION, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags

    async def __server_info_score(self, organization, asn_code, ip, location):
        issue_config = Issue_Config()
        total_score = 0
        total_weight = 100  # Max total score

        issues = []
        suggestions = []

        # Weights assigned to each parameter (equally distributed here)
        parameter_weight = total_weight / 4  # 4 parameters: Organization, ASN Code, IP, Location

        # Check Organization
        if organization != "Unknown" and organization != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_SERVER_INFO_ORGANIZATION)
            suggestions.append(issue_config.SUGGESTION_SERVER_INFO_ORGANIZATION)

        # Check ASN Code
        if asn_code != "Unknown" and asn_code != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_SERVER_INFO_ASN)
            suggestions.append(issue_config.SUGGESTION_SERVER_INFO_ASN)

        # Check IP
        if ip != "Unknown" and ip != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_IP)
            suggestions.append(issue_config.SUGGESTION_SERVER_INFO_IP)

        # Check Location
        if location != "Unknown" and location != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_SERVER_INFO_LOCATION)
            suggestions.append(issue_config.SUGGESTION_SERVER_INFO_LOCATION)

        # Calculate percentage score
        percentage_score = (total_score / total_weight) * 100

        # html_tags = await self.__analysis_server_table(issues, suggestions, int(server_info_score_percentage))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.MODULE_SERVER_INFO, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags