import dns.resolver
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style


class DNS_RECORDS():
    def __init__(self,url):
        self.url=url

    async def Get_DNS_Records(self):
        try:
            domain_name = urlparse(self.url).netloc
            result=await self.__fina_result(domain_name)
            output=await self.__formatting_Output(domain_name,*result)
            return output

        except Exception as e:
            error_msg = e.args[0]
            msg = "[-] " + self.Error_Title + " => Get_DNS_Server_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return error_msg

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTIONS
    async def __fina_result(self,domain_name):
        A_record=await self.__get_A_record(domain_name)
        AAAA_record=await self.__get_AAAA_record(domain_name)
        mx_record=await self.__get_MX__record(domain_name)
        NS_record=await self.__get_NS__record(domain_name)
        CNAME_record=await self.__get_CNAME__record(domain_name)
        txt_record=await self.__get_TXT__record(domain_name)
        return A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record

    async def __get_A_record(self,domain_name):
        try:

            answers = dns.resolver.resolve(domain_name,'A')
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

    async def __get_AAAA_record(self,domain_name):
        try:

            answers = dns.resolver.resolve(domain_name,'AAAA')
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

    async def __get_MX__record(self,domain_name):
        try:

            answers = dns.resolver.resolve(domain_name,'MX')
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

    async def __get_NS__record(self,domain_name):
        try:
            answers = dns.resolver.resolve(domain_name,'NS')
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

    async def __get_CNAME__record(self,domain_name):
        try:

            answers = dns.resolver.resolve(domain_name,'CNAME')
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

    async def __get_TXT__record(self,domain_name):
        try:
            answers = dns.resolver.resolve(domain_name,'TXT')
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

    async def __formatting_Output(self,domain, A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record):
        # print(domain,A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record)
        htmlValue = ""
        htmlValue = await self.__html_table(domain,A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record)
        return str(htmlValue) 

    async def __html_table(self,domain,A_record,AAAA_record,mx_record,NS_record,CNAME_record,txt_record):
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
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">A RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(A_record)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">AAAA RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(AAAA_record)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">MX RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(mx_record)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">NS RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(NS_record)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">CNAME RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(CNAME_record)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">TXT RECORD</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(txt_record)
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
