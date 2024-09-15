import pandas as pd
import aiohttp
import asyncio
from urllib.parse import urlparse
from util.config_uti import Configuration
from colorama import Fore, Style

class Server_Location():
    Error_Title = None

    def __init__(self, ip_address):
        self.ip_address = ip_address

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
        htmlValue = ""        
        dataframe = pd.DataFrame.from_dict(decodedResponse, orient='index')
        htmlValue = await self.__html_table(dataframe)
        return str(htmlValue)

    async def __html_table(self, data):

        city = str(data[0]["city"])
        county = str(data[0]["country_name"])
        timezone = str(data[0]["timezone"])
        languages =  str(data[0]["languages"])
        currency = str(data[0]["currency_name"])

        percentage = await self.__rating(city, county, timezone, languages, currency)

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
                            <td>""" + city +  """</td>
                        </tr>
                        <tr>
                            <td>Country</td>
                            <td>""" + county +  """</td>
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
                            <td>""" + currency +  """</td>
                        </tr>
                </table>"""
        return table

    async def __rating(self, city, county, timezone, languages, currency):
        condition1 = city != None
        condition2 = county != None
        condition3 = timezone != None
        condition4 = languages != None
        condition5 = currency != None

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4, condition5])
        
        # Determine the percentage based on the number of satisfied conditions

        if satisfied_conditions == 5:
            percentage = 100
        elif satisfied_conditions == 4:
            percentage = 80
        elif satisfied_conditions == 3:
            percentage = 60
        elif satisfied_conditions == 2:
            percentage = 40
        elif satisfied_conditions == 1:
            percentage = 20
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage