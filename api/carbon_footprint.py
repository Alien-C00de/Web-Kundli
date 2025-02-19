import aiohttp
from colorama import Fore, Style
from util.config_uti import Configuration

class Carbon_Footprint:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain  = domain

    async def Get_Carbon_Footprint(self):
        config = Configuration()
        self.Error_Title = config.CARBON_FOOTPRINT
        output = ""

        try:
            # print("carbon.py: start ")
            async with aiohttp.ClientSession() as session:
                size_in_bytes = await self.__get_html_size(self.url)
                api_url = config.CARBON_API_ENDPOINT_URL.replace("{size_in_bytes}", str(size_in_bytes))
                async with session.get(api_url) as response:
                    response.raise_for_status()
                    decodedResponse = await response.json()

            output = await self.__html_table(decodedResponse)
            # print("carbon.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Carbon_Footprint : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output


    async def __get_html_size(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html_content = await response.text()
                    size_in_bytes = len(html_content.encode('utf-8'))
                    return size_in_bytes
        except aiohttp.ClientResponseError as e:
            if e.status == 403:
                msg = "[-] " + self.Error_Title + " => get_html_size : Forbidden: You don't have permission to access this resource."
                raise ValueError(msg)
            else:
                msg = "[-] " + self.Error_Title + " => get_html_size : Error fetching HTML size: {e}"
                raise ValueError(msg)

    async def __html_table(self, data):
        HTML_Initial_Size = str(data['statistics']['adjustedBytes']) + " bytes"
        CO2_Load = str(data['statistics']['co2']['grid']['grams']) + " grams"
        Energy_Usage = f"{data['statistics']['energy']:.4f} KWg"
        CO2_Emitted =  str(data['statistics']['co2']['renewable']['grams']) + " grams"
        percentage = await self.__rating(HTML_Initial_Size, CO2_Load, Energy_Usage, CO2_Emitted)

        table = (
            """<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>HTML Initial Size</td>
                        <td>""" + str(HTML_Initial_Size) + """</td>
                    </tr>
                    <tr>
                        <td>CO2 for Initial Load:</td>
                        <td>""" + str(CO2_Load) + """</td>
                    </tr>
                    <tr>
                        <td>Energy Usage for Load:</td>
                        <td>""" + str(Energy_Usage) + """</td>
                    </tr>
                    <tr>
                        <td>CO2 Emitted:</td>
                        <td>""" + str(CO2_Emitted)  + """</td>
                    </tr>
                </table>"""
        )
        return table

    async def __rating(self, HTML_Initial_Size, CO2_Load, Energy_Usage, CO2_Emitted):

        condition1 = HTML_Initial_Size != ""
        condition2 = CO2_Load != ""
        condition3 = Energy_Usage != ""
        condition4 = CO2_Emitted != ""

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