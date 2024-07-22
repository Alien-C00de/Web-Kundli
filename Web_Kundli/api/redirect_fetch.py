import requests
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style
from util.config_uti import Configuration

class REDIRECT_PAGE():
    def __init__(self,url):
        self.url=url

    async def Get_Redirect(self):
        config = Configuration()
        self.Error_Title = config.REDIRECT_FETCH
        output=""
        try:
            domain_name = urlparse(self.url).netloc
            result=await self.__final_result()
            output=await self.__formatting_Output(domain_name,result)
            return output

        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_Redirect : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTION
    async def __final_result(self):
        error_ans=[0,None,None]
        respond=[]
        count=0
        ans=""
        try:
            response = requests.get(self.url, allow_redirects=True)
            final_url = response.url

            if response.history:
                for resp in response.history:
                    count+=1
                    ans+=str(resp.url)
                    ans+=',\n'
                count+=1
                ans+=str(final_url)
                ans+=',\n'
                respond.append(count)
                respond.append(ans)
                respond.append(final_url)
                return respond
            else:
                respond.append(count+1)
                respond.append(final_url)
                respond.append(final_url)
                return respond

        except Exception as e:
            print(e)
            return error_ans

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
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">NUMBER OF REDIRECTS</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(result[0])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">REDIRECT LINK</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(result[1])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">FINAL PAGE</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(result[2])
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
