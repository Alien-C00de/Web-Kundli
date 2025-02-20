import dns.resolver
from colorama import Fore, Style

class DNS_Records():
    Error_Title = None
    
    def __init__(self, url, domain):
        self.url=url
        self.domain = domain

    async def Get_DNS_Records(self):
        try:
            # print("dns_record_fetch.py: start")
            result = await self.__final_result(self.domain)
            output = await self.__html_table(self.domain, *result)
            # print("dns_record_fetch.py: output: ")
            return output

        except Exception as e:
            error_msg = str(e.args[0])
            msg = "[-] " + self.Error_Title + " => Get_DNS_Records : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return error_msg

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTIONS
    async def __final_result(self, domain):
        A_record=await self.__get_A_record(domain)
        AAAA_record=await self.__get_AAAA_record(domain)
        mx_record=await self.__get_MX__record(domain)
        NS_record=await self.__get_NS__record(domain)
        CNAME_record=await self.__get_CNAME__record(domain)
        txt_record=await self.__get_TXT__record(domain)
        return A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record

    async def __get_A_record(self,domain):
        try:
            answers = dns.resolver.resolve(domain, 'A')
            required_a=[rdata.to_text() for rdata in answers]
            if len(required_a)==1:
                return required_a[0]
            else:
                req_a=""
                l=required_a
                for i in l:
                    req_a+=i
                    req_a+=" ,\n"
                return req_a

        except Exception as e:
            return None

    async def __get_AAAA_record(self,domain):
        try:
            answers = dns.resolver.resolve(domain, 'AAAA')
            required_aaaa=[rdata.to_text() for rdata in answers]
            if len(required_aaaa)==1:
                return required_aaaa[0]
            else:
                req_aaaa=""
                l=required_aaaa
                for i in l:
                    req_aaaa+=i
                    req_aaaa+=" ,\n"
                return req_aaaa

        except Exception as e:
            return None

    async def __get_MX__record(self,domain):
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            required_mx=[rdata.to_text() for rdata in answers]
            if len(required_mx)==1:
                return required_mx[0]
            else:
                req_mx=""
                l=required_mx
                for i in l:
                    req_mx+=i
                    req_mx+=" ,\n"
                return req_mx

        except Exception as e:
            return None

    async def __get_NS__record(self, domain):
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            required_NS=[rdata.to_text() for rdata in answers]
            if len(required_NS)==1:
                return required_NS[0]
            else:
                req_ns=""
                l=required_NS
                for i in l:
                    req_ns+=i
                    req_ns+=" ,\n"
                return req_ns
        except Exception as e:
            return None

    async def __get_CNAME__record(self,domain):
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            required_CNAME=[rdata.to_text() for rdata in answers]
            if len(required_CNAME)==1:
                return required_CNAME[0]
            else:
                req_cname=""
                l=required_CNAME
                for i in l:
                    req_cname+=i
                    req_cname+=" ,\n"
                return req_cname

        except Exception as e:
            return None

    async def __get_TXT__record(self,domain):
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            required_TXT=[rdata.to_text() for rdata in answers]
            if len(required_TXT)==1:
                return required_TXT[0]
            else:
                req_txt=""
                l=required_TXT
                for i in l:
                    req_txt+=i
                    req_txt+=" ,\n"
                return req_txt

        except Exception as e:
            return None

    async def __html_table(self, domain, A_record, AAAA_record, mx_record, NS_record, CNAME_record, txt_record):
        
        percentage = await self.__rating(domain, A_record, AAAA_record, mx_record, NS_record, CNAME_record, txt_record)
        table = (
            """<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Domain Name</td>
                        <td>""" + str(domain) + """</td>
                    </tr>
                    <tr>
                        <td>A RECORD</td>
                        <td>""" + str(A_record) + """</td>
                    </tr>
                    <tr>
                        <td>AAAA RECORD</td>
                        <td>""" + str(AAAA_record) + """</td>
                    </tr>
                    <tr>
                        <td>MX RECORD</td>
                        <td>""" + str(mx_record) + """</td>
                    </tr>
                    <tr>
                        <td>NS RECORD</td>
                        <td>""" + str(NS_record) + """</td>
                    </tr>
                    <tr>
                        <td>CNAME RECORD</td>
                        <td>""" + str(CNAME_record) + """</td>
                    </tr>
                    <tr>
                        <td>TXT RECORD</td>
                        <td>""" + str(txt_record) + """</td>
                    </tr>
                </table>"""
        )
        return table

    async def __rating(self, domain, A_record, AAAA_record, mx_record, NS_record, CNAME_record, txt_record):

        condition1 = domain != None
        condition2 = A_record != None
        condition3 = AAAA_record != None
        condition4 = mx_record != None
        condition5 = NS_record != None
        condition6 = CNAME_record != None
        condition7 = txt_record != None

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