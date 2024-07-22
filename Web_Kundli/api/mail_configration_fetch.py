import dns.resolver
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style
from util.config_uti import Configuration

class MAIL_RECORDS():
    Error_Title = None
    
    def __init__(self,url):
        self.url=url

    async def Get_Mail_Records(self):
        config = Configuration()
        self.Error_Title = config.MAIL_CONFIGURATION
        output=""
        try:
            domain_name = urlparse(self.url).netloc
            result=await self.__final_result(domain_name)
            output=await self.__formatting_Output(domain_name,result)
            return output

        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_Mail_Records : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTIONS
    async def __final_result(self,domain_name):
        record_types = ['MX', 'TXT',]
        result=[]
        for i in record_types:
            try:
                answers = dns.resolver.resolve(domain_name,i)
                required_a=[data.to_text() for data in answers]
                if len(required_a)==1:
                    result.append(required_a[0])
                else:
                    req_a=""
                    l=required_a
                    for i in l:
                        req_a+="\n"
                        req_a+="\t{}\t".format(i)
                        req_a+=" \n,\n"
                    result.append(req_a)
            except Exception as e:
                result.append(None)
        return result

    async def __formatting_Output(self,domain, result):
        # print(domain,A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record)
        htmlValue = ""
        htmlValue = await self.__html_table(domain,result)
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
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">MAIL RECORDS</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(result[0])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">EXTERNAL MAIL RECORDS</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(result[1])
            + """</span></strong></td>
                </tr> 
                </tbody>
                </table>"""
        )
        return table
