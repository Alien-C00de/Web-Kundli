import asyncio
from urllib.parse import urlparse
from util.config_uti import Configuration
from colorama import Fore, Style
import whois

class domain_whois():
    Error_Title = None
    
    def __init__(self, url):
        self.url = url

    async def Get_Whois_Info(self):
        config = Configuration()
        self.Error_Title = config.WHOIS
        output = ""
        try:
            domain_name = urlparse(self.url).netloc 
            domain_info =  whois.whois(domain_name)
            output = await self.__formatting_Output(domain_info)
            return output
        except Exception as ex:
            error_msg = ex.args[0]
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

        table = """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Registered Domain</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">""" +  str(domain_info.domain) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Creation Date</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(domain_info.creation_date) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Updated Date</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(domain_info.updated_date) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Registry Expiry Date</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(domain_info.expiration_date) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Registry Domain ID</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(" ") +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Registrar WHOIS Server</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(whois_server) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Registrar</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(domain_info.registrar) +  """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Registrar IANA ID</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">""" + str(domain_info.registrar_iana) +  """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        return table
