import dns.resolver
from urllib.parse import urlparse
from colorama import Fore, Style
from util.config_uti import Configuration


class TXT_Records():
    Error_Title = None
    
    def __init__(self,url):
        self.url=url

    async def Get_TXT_Records(self):
        config = Configuration()
        self.Error_Title = config.TLS_RECORD
        output  = ""
        try:
            # print("txt_record_fetch.py: start")
            domain_name = urlparse(self.url).netloc
            result = await self.__final_result(domain_name)
            output = await self.__formatting_Output(domain_name,result)
            # print("txt_record_fetch.py: output: ")
            return output

        except Exception as e:
            error_msg = str(e.args[0])
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
        percentage = 0

        if txt_record != None:
            percentage = 100
            
        table = (
            f"""<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Domain Name</td>
                        <td>""" + str(domain) + """</td>
                    </tr>
                    <tr>
                        <td>TXT RECORD</td>
                        <td>""" + str(txt_record) + """</td>
                    </tr>
            </table>"""
        )
        return table
