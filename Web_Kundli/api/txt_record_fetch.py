import dns.resolver
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style
from util.config_uti import Configuration


class TXT_RECORDS():
    Error_Title = None
    
    def __init__(self,url):
        self.url=url

    async def Get_TXT_Records(self):
        config = Configuration()
        self.Error_Title = config.TLS_RECORD
        output  = ""
        try:
            domain_name = urlparse(self.url).netloc
            result=await self.__final_result(domain_name)
            output=await self.__formatting_Output(domain_name,result)
            return output

        except Exception as e:
            error_msg = e.args[0]
            msg = "[-] " + self.Error_Title + " => Get_TXT_Records : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTIONS
    async def __final_result(self,domain_name):
        try:
            answers = dns.resolver.resolve(domain_name,'TXT')
            required_TXT=[data.to_text() for data in answers]
            if len(required_TXT)==1:
                return required_TXT[0]
            else:
                req_txt=""
                l=required_TXT
                for i in l:
                    req_txt+="\n"
                    req_txt+=i
                    req_txt+=" ,\n "
                return req_txt    
        except Exception as e:
            return None

    async def __formatting_Output(self,domain, txt_record):
        # print(domain,A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record)
        htmlValue = ""
        htmlValue = await self.__html_table(domain,txt_record)
        return str(htmlValue) 

    async def __html_table(self,domain,txt_record):
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
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">TXT RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(txt_record)
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
