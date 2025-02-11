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
        output = ""

        headers = {'Accept': 'application/json',}

        try:
            # print("server_location.py: start")
            async with aiohttp.ClientSession(headers=headers) as session:
                url = config.IPAPI_IO_ENDPOINT_URL + self.ip_address + "/json/"
                tasks.append(asyncio.create_task(session.request(method="GET", url=url)))

                responses = await asyncio.gather(*tasks)
                for response in responses:
                    decodedResponse.append(await response.json())

            output = await self.__formatting_Output(decodedResponse[0])
            # print("server_location.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Server_Location : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, decodedResponse):
        location = []
        info = [] 
        htmlValue = []        
        dataframe = pd.DataFrame.from_dict(decodedResponse, orient='index')
        location = await self.__html_server_loc_table(dataframe)
        info = await self.__html_server_info_table(dataframe)
        htmlValue = location + info
        return htmlValue

    async def __html_server_info_table(self, data):
        rep_data = []
        org = str(data[0]["org"])
        asn = str(data[0]["asn"])
        ip = str(data[0]["ip"])
        location =  str(data[0]["region"]) + ",\n " + str(data[0]["country_name"])

        percentage, htmltags = await self.__calculate_server_info_score(org, asn, ip, location)

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
        rep_data.append(htmltags)
        return rep_data

    async def __html_server_loc_table(self, data):
        rep_data = []
        city =  str(data[0]["city"])
        postal = str(data[0]["postal"])
        region = str(data[0]["region"])
        country = str(data[0]["country_name"])
        country_code = str(data[0]["country_code"]).lower()
        timezone = str(data[0]["timezone"])
        languages =  str(data[0]["languages"])
        currency_name = str(data[0]["currency_name"])
        currency = str(data[0]["currency"])

        # percentage = await self.__rating_loc(city, country, timezone, languages, currency)
        percentage, htmltags = await self.__calculate_server_Location_score(city, country, timezone, languages, currency)

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
        rep_data.append(htmltags)
        return rep_data

    async def __calculate_server_Location_score(self, city, country, timezone, languages, currency):

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
            issues.append(issue_config.ISSUE_CITY)
            suggestions.append(issue_config.SUGGESTION_CITY)

        # Check Country
        if country != "Unknown" and country != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_COUNTRY)
            suggestions.append(issue_config.SUGGESTION_COUNTRY)

        # Check Timezone
        if timezone != "Unknown" and timezone != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_TIMEZONE)
            suggestions.append(Issue_Config.SUGGESTION_TIMEZONE)

        # Check Languages
        if languages != "Unknown" and languages != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LANGUAGES)
            suggestions.append(issue_config.SUGGESTION_LANGUAGES)

        # Check Currency
        if currency != "Unknown" and currency != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_CURRENCY)
            suggestions.append(issue_config.SUGGESTION_CURRENCY)

        # Calculate percentage score
        percentage_score = (total_score / total_weight) * 100
        # html_tags = await self.__analysis_location_table(issues, suggestions, int(security_score_percentage))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags

    async def __calculate_server_info_score(self, organization, asn_code, ip, location):
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
            issues.append(issue_config.ISSUE_ORGANIZATION)
            suggestions.append(issue_config.SUGGESTION_ORGANIZATION)

        # Check ASN Code
        if asn_code != "Unknown" and asn_code != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_ASN)
            suggestions.append(issue_config.SUGGESTION_ASN)

        # Check IP
        if ip != "Unknown" and ip != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_IP)
            suggestions.append(issue_config.SUGGESTION_IP)

        # Check Location
        if location != "Unknown" and location != "":
            total_score += parameter_weight
        else:
            issues.append(issue_config.ISSUE_LOCATION)
            suggestions.append(issue_config.SUGGESTION_LOCATION)

        # Calculate percentage score
        percentage_score = (total_score / total_weight) * 100

        # html_tags = await self.__analysis_server_table(issues, suggestions, int(server_info_score_percentage))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags

    async def __analysis_location_table(self, issues, suggestions, percentage):
        # config = Configuration()
        html = ""
        if issues:
            html_template = """<div class="module" id="location">
                                <h2>""" + Configuration.MODULE_SERVER_LOCATION + """ &nbsp;Score = """ + str(percentage) + """%</h2>
                                <div style="display: inline; font-weight: bold;">Summary :</div>
                                <span style="display: inline;">The Server Location used on the website meet most security standards. However, there are a couple of issues that need to be addressed.</span>
                                <div class="issues">
                                    <h4>Identified Issues:</h4>
                                    <ul>
                                        {issue_items}
                                    </ul>
                                </div>
                                <div class="suggestions">
                                    <h4>Suggestions for Improvement:</h4>
                                    <ul>
                                        {suggestion_items}
                                    </ul>
                                </div> 
                        </div>"""

            # Generate the list items for issues and suggestions
            issue_items = "".join([f"<li>{issue}</li>" for issue in issues])
            suggestion_items = "".join([f"<li>{suggestion}</li>" for suggestion in suggestions])

            # Insert the list items into the HTML template
            html = html_template.format(issue_items=issue_items, suggestion_items=suggestion_items)
        return html

    async def __analysis_server_table(self, issues, suggestions, percentage):
        # config = Configuration()
        html = ""
        if issues:
            html_template = """<div class="module" id="info">
                                <h2>""" + Configuration.MODULE_SERVER_INFO + """ &nbsp; Score = """ + str(percentage) + """%</h2>
                                <div style="display: inline; font-weight: bold;">Summary :</div>
                                <span style="display: inline;">The Server Info used on the website meet most security standards. However, there are a couple of issues that need to be addressed.</span
                                <div class="issues">
                                    <h4>Identified Issues:</h4>
                                    <ul>
                                        {issue_items}
                                    </ul>
                                </div>
                                <div class="suggestions">
                                    <h4>Suggestions for Improvement:</h4>
                                    <ul>
                                        {suggestion_items}
                                    </ul>
                                </div> 
                        </div>"""

            # Generate the list items for issues and suggestions
            issue_items = "".join([f"<li>{issue}</li>" for issue in issues])
            suggestion_items = "".join([f"<li>{suggestion}</li>" for suggestion in suggestions])

            # Insert the list items into the HTML template
            html = html_template.format(issue_items=issue_items, suggestion_items=suggestion_items)
        return html

    # async def __rating_loc(self, city, country, timezone, languages, currency):

    #     weights = {
    #         "city": 0.20,
    #         "country": 0.20,
    #         "timezone":0.20,
    #         "language": 0.20,
    #         "currency": 0.20,
    #     }

    #     # Initialize rating
    #     rating = 0

    #     # Calculate rating based on the presence of each detail
    #     if city:
    #         rating += weights["city"]
    #     if country:
    #         rating += weights["country"]
    #     if timezone:
    #         rating += weights["timezone"]
    #     if languages:
    #         rating += weights["language"]
    #     if currency:
    #         rating += weights["currency"]

    #     # Convert rating to percentage
    #     percentage = rating * 100
    #     return int(percentage)

    # async def __rating_info(self, org, asn, ip, location):
    #     condition1 = org != None
    #     condition2 = asn != None
    #     condition3 = ip != None
    #     condition4 = location != None

    #     # Count the number of satisfied conditions
    #     satisfied_conditions = sum([condition1, condition2, condition3, condition4])

    #     # Determine the percentage based on the number of satisfied conditions

    #     if satisfied_conditions == 4:
    #         percentage = 100
    #     elif satisfied_conditions == 3:
    #         percentage = 75
    #     elif satisfied_conditions == 2:
    #         percentage = 50
    #     elif satisfied_conditions == 1:
    #         percentage = 25
    #     else:
    #         percentage = 0  # In case no conditions are satisfied

    #     return percentage
