import requests
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class Redirect_Chain():
    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Redirect_Chain(self):
        config = Configuration()
        self.Error_Title = config.REDIRECT_FETCH
        output=""
        try:
            # print("redirect_fetch.py: start")
            result = await self.__final_result()
            output = await self.__html_table(result)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Redirect_Chain : " + error_msg
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

    async def __html_table(self, result):

        if not result:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage = await self.__rating(str(self.domain), str(result[0]), str(result[1]), str(result[2]))
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
                            <td>""" + str(self.domain) + """</td>
                        </tr>
                        <tr>
                            <td>Number of Redirects</td>
                            <td>""" + str(result[0]) + """</td>
                        </tr>
                        <tr>
                            <td>Redirect Link</td>
                            <td>""" + str(result[1]) + """</td>
                        </tr>
                        <tr>
                            <td>Final Page</td>
                            <td>""" + str(result[2]) + """</td>
                        </tr>
                    </table>"""
            )
        return table

    async def __rating(self, doman, no_of_redirect, redirect_link, final_page):
        condition1 = doman != None
        condition2 = no_of_redirect != None
        condition3 = redirect_link != None
        condition4 = final_page != None

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