import dns.resolver
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class Mail_Records():
    Error_Title = None
    
    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Mail_Records(self):
        config = Configuration()
        self.Error_Title = config.MAIL_CONFIGURATION
        output=""
        try:
            # print("mail_configration_fetch.py: start")
            result = await self.__final_result(self.domain)
            output = await self.__html_table(result)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Mail_Records : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTIONS
    async def __final_result(self, domain):
        record_types = ['MX', 'TXT',]
        result=[]
        for i in record_types:
            try:
                answers = dns.resolver.resolve(domain, i)
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

    async def __html_table(self, result):

        if not result:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage = await self.__rating(str(self.domain), str(result[0]), str(result[1]))

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
                            <td>MAIL RECORDS</td>
                            <td>""" + str(result[0]) + """</td>
                        </tr>
                        <tr>
                            <td>EXTERNAL MAIL RECORDS</td>
                            <td>""" + str(result[1]) + """</td>
                        </tr> 
                    </table>"""
            )
        return table

    async def __rating(self, domain, mail_record, ext_mail_record):

        condition1 = domain != None
        condition2 = mail_record != None
        condition3 = ext_mail_record != None

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3])
        
        # Determine the percentage based on the number of satisfied conditions
        if satisfied_conditions == 3:
            percentage = 100
        elif satisfied_conditions == 2:
            percentage = 66
        elif satisfied_conditions == 1:
            percentage = 33
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage