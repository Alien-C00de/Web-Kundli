import pandas as pd
import aiohttp
import asyncio
from util.config_uti import Configuration
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
        htmlValue = []        
        dataframe = pd.DataFrame.from_dict(decodedResponse, orient='index')
        htmlValue.append(await self.__html_server_loc_table(dataframe))
        htmlValue.append(await self.__html_server_info_table(dataframe))
        return htmlValue

    async def __html_server_info_table(self, data):
        org = str(data[0]["org"])
        asn = str(data[0]["asn"])
        ip = str(data[0]["ip"])
        location =  str(data[0]["region"]) + ",\n " + str(data[0]["country_name"])

        percentage = await self.__rating_info(org, asn, ip, location)

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
        return table

    async def __html_server_loc_table(self, data):

        city =  str(data[0]["city"])
        postal = str(data[0]["postal"])
        region = str(data[0]["region"])
        country = str(data[0]["country_name"])
        country_code = str(data[0]["country_code"]).lower()
        timezone = str(data[0]["timezone"])
        languages =  str(data[0]["languages"])
        currency_name = str(data[0]["currency_name"])
        currency = str(data[0]["currency"])

        percentage = await self.__rating_loc(city, country, timezone, languages, currency)

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
        return table

    async def __rating_loc(self, city, country, timezone, languages, currency):

        weights = {
            "city": 0.20,
            "country": 0.20,
            "timezone":0.20,
            "language": 0.20,
            "currency": 0.20,
        }

        # Initialize rating
        rating = 0

        # Calculate rating based on the presence of each detail
        if city:
            rating += weights["city"]
        if country:
            rating += weights["country"]
        if timezone:
            rating += weights["timezone"]
        if languages:
            rating += weights["language"]
        if currency:
            rating += weights["currency"]

        # Convert rating to percentage
        percentage = rating * 100
        return int(percentage)

    async def __rating_info(self, org, asn, ip, location):
        condition1 = org != None
        condition2 = asn != None
        condition3 = ip != None
        condition4 = location != None

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4])

        # Determine the percentage based on the number of satisfied conditions

        if satisfied_conditions == 4:
            percentage = 100
        elif satisfied_conditions == 3:
            percentage = 75
        elif satisfied_conditions == 2:
            percentage = 50
        elif satisfied_conditions == 1:
            percentage = 25
        else:
            percentage = 0  # In case no conditions are satisfied

        return percentage
