import aiohttp
import asyncio
from util.config_uti import Configuration
from colorama import Fore, Style


class Server_Info():
    Error_Title = None

    def __init__(self, ip_address, url):
        self.ip_address = ip_address
        self.url = url

    async def Get_Server_Info(self):
        # Get the IP address
        config = Configuration()
        self.Error_Title = config.SERVER_INFO
        tasks = []
        decodedResponse = []
        output = ""

        headers = {'Accept': 'application/json',}

        try:
            # print("server_info.py: start")
            async with aiohttp.ClientSession(headers=headers) as session:
                # url = config.SHODAN_ENDPOINT_URL + self.ip_address + "?key=" + config.SHODAN_API_KEY
                url = config.SHODAN_ENDPOINT_URL + '8.8.8.8' + "?key=" + config.SHODAN_API_KEY

                tasks.append(asyncio.create_task(session.request(method="GET", url=url)))

                responses = await asyncio.gather(*tasks)
                for response in responses:
                    decodedResponse.append(await response.json())

            output = await self.__formatting_Output(decodedResponse)
            # print("server_info.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, decodedResponse):
        htmlValue = ""        
        htmlValue = await self.__html_table(decodedResponse)
        return str(htmlValue)

    async def __html_table(self, data):

        org =  str(data[0]['org'])
        asn_code = str(data[0]['asn'])
        ports = str(data[0]["ports"])
        ip = str(data[0]["ip_str"])
        type = str(data[0]["tags"])
        city = str(data[0]["city"])
        country = str(data[0]["country_name"])

        percentage = await self.__rating(org, asn_code, ports, ip, type, city, country)

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
                            <td>""" + asn_code +  """</td>
                        </tr>
                        <tr>
                            <td>Ports</td>
                            <td>""" + ports +  """</td>
                        </tr>
                        <tr>
                            <td>IP</td>
                            <td>""" + ip +  """</td>
                        </tr>
                        <tr>
                            <td>Type</td>
                            <td>""" + type +  """</td>
                        </tr>
                        <tr>
                            <td>Location</td>
                            <td>""" + city + ", " + country +  """</td>
                        </tr>
                </table>"""
        return table

    async def __rating(self, org, asn_code, ports, ip, type, city, country):

        condition1 = org != None
        condition2 = asn_code != None
        condition3 = ports != None
        condition4 = ip != None
        condition5 = type != None
        condition6 = city != None
        condition7 = country != None


        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4, condition5, condition6, condition7])
        
        # Determine the percentage based on the number of satisfied conditions

        if satisfied_conditions == 7:
            percentage = 100
        elif satisfied_conditions == 6:
            percentage = 90
        elif satisfied_conditions == 5:
            percentage = 75
        elif satisfied_conditions == 4:
            percentage = 60
        elif satisfied_conditions == 3:
            percentage = 45
        elif satisfied_conditions == 2:
            percentage = 30
        elif satisfied_conditions == 1:
            percentage = 15
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage