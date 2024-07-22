import requests
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style
from util.config_uti import Configuration

class SERVER_STATUS():
    Error_Title = None

    def __init__(self,url):
        self.url=url

    async def Get_Server_Status(self):
        config = Configuration()
        self.Error_Title = config.SERVER_STATUS
        output=""
        try:
            domain_name = urlparse(self.url).netloc
            result=await self.__final_result()
            output= await self.__formatting_Output(domain_name,result)
            return output
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_Server_Status : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTION
    async def __final_result(self):
        try:
            response = requests.get(self.url,timeout=1)
            if response.status_code >= 200 and response.status_code < 300:
                return 'Server is Up'
            else:
                return 'Server is Down'
        except Exception as e:
            return None

    async def __formatting_Output(self,domain_name,result):
        # print(domain,A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record)
        htmlValue = ""
        htmlValue = await self.__html_table(domain_name,result)
        return str(htmlValue) 

    async def __html_table(self,domain,result):
        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Domain Name</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(domain)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">SERVER STATUS</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(result)
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
