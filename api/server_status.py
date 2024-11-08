from urllib.parse import urlparse
from colorama import Fore, Style
from util.config_uti import Configuration

class Server_Status():
    Error_Title = None

    def __init__(self, url, response):
        self.url = url
        self.response = response

    async def Get_Server_Status(self):
        config = Configuration()
        self.Error_Title = config.SERVER_STATUS
        output = ""
        try:
            # print("server_status_fetch.py: start")
            domain_name = urlparse(self.url).netloc
            result = await self.__final_result()
            output = await self.__formatting_Output(domain_name,result)
            # print("server_status_fetch.py: output: ")
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Server_Status : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTION
    async def __final_result(self):
        try:
            # response = requests.get(self.url,timeout=1)
            if self.response.status_code >= 200 and self.response.status_code < 300:
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

    async def __html_table(self, domain, result):

        percentage = 0
        
        if result != None:
            percentage = 100

        table = (
            """<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width:""" + str(percentage) + """%;">""" + str(percentage) + """%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Domain Name</td>
                        <td>""" + str(domain) + """</td>
                    </tr>
                    <tr>
                    <td>SERVER STATUS</td>
                        <td >""" + str(result) + """</td>
                    </tr>
            </table>"""
        )
        return table
