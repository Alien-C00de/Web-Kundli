from urllib.parse import urlparse
from util.config_uti import Configuration
from colorama import Fore, Style
import whois

class Domain_Whois():
    Error_Title = None
    
    def __init__(self, url):
        self.url = url

    async def Get_Whois_Info(self):
        config = Configuration()
        self.Error_Title = config.WHOIS
        output = ""
        try:
            # print("domain_whois.py: start")
            domain_name = urlparse(self.url).netloc 
            domain_info =  whois.whois(domain_name)
            output = await self.__formatting_Output(domain_info)
            # print("domain_whois.py: output: ")
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Whois_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, decodedResponse):
        htmlValue = ""        
        htmlValue = await self.__html_table(decodedResponse)
        return str(htmlValue)

    async def __html_table(self, domain_info):
        whois_server = ""
        if domain_info.whois_server is not None:
            whois_server = domain_info.whois_server
        else:
            whois_server = domain_info.registrar_url
        
        percentage = await self.__rating(domain_info)

        table = """<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Registered Domain</td>
                        <td>""" + str(domain_info.domain) + """</td>
                    </tr>
                    <tr>
                        <td>Creation Date</td>
                        <td>""" + str(domain_info.creation_date) +  """</td>
                    </tr>
                    <tr>
                        <td>Updated Date</td>
                        <td>""" + str(domain_info.updated_date) +  """</td>
                    </tr>
                    <tr>
                        <td>Registry Expiry Date</td>
                        <td>""" + str(domain_info.expiration_date) +  """</td>
                    </tr>
                    <tr>
                        <td>Registry Domain ID</td>
                        <td>""" + str(" ") +  """</td>
                    </tr>
                    <tr>
                        <td>Registrar WHOIS Server</td>
                        <td>""" + str(whois_server) +  """</td>
                    </tr>
                    <tr>
                        <td>Registrar</td>
                        <td>""" + str(domain_info.registrar) +  """</td>
                    </tr>
                    <tr>
                        <td>Registrar IANA ID</td>
                        <td>""" + str(domain_info.registrar_iana) +  """</td>
                    </tr>
                </table>"""
        return table

    async def __rating(self, domain_info):

        if domain_info.whois_server is not None:
            whois_server = domain_info.whois_server
        else:
            whois_server = domain_info.registrar_url

        condition1 = domain_info.domain != None
        condition2 = domain_info.creation_date != None
        condition3 = domain_info.updated_date != None
        condition4 = domain_info.expiration_date != None
        condition5 = whois_server != None
        condition6 = domain_info.registrar != None
        condition7 = domain_info.registrar_iana != None

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