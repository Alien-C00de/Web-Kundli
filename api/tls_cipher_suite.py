import ssl
import socket
from colorama import Fore, Style
from util.config_uti import Configuration

class TLS_Cipher_Suit:
    Error_Title = None
    
    def __init__(self,url, domain):
        self.url=url
        self.domain = domain

    async def Get_TLS_Cipher_Suit(self):
        config = Configuration()
        self.Error_Title = config.TLS_CIPHER_SUIT
        output=""
        try:
            # print("tls_cipher_suite.py: start")
            res = await self.__final_result(self.domain)
            output = await self.__formatting_Output(res)
            # print("tls_cipher_suite.py: output: ")
            return output

        # output=self.__formatting_Output(domain,issue_org,issue,expire,protocal_verion,cipher,length,serial)
        # return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_TLS_Cipher_Suit : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __final_result(self,domain):
        default={'Domain Name': None, 'Issuing Organization': None, 'Issue Date': None, 'Expire Date': None, 'Serial Number': None, 'Protocol Version': None, 'Cipher Suite': None, 'Public key length': None}
        try:
            result={}
            context = ssl.create_default_context()
            s=context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = domain)
            content=s.connect((domain, 443))
            result["Domain Name"] = domain
            cert=s.getpeercert()
            if 'issuer' in cert:
                issuer=cert['issuer']
                organization=issuer[1][0][1]
                result["Issuing Organization"]=organization
            else:
                result["Issuing Organization"]=None
            if 'notBefore' in cert:
                register_date=cert['notBefore']
                result["Issue Date"]=register_date
            else:
                result["Issue Date"]=None
            if 'notAfter' in cert:
                expire_date=cert['notAfter']
                result["Expire Date"]=expire_date
            else:
                result["Expire Date"]=None
            if 'serialNumber' in cert:
                serial_no=cert['serialNumber']
                result['Serial Number']=serial_no
            else:
                result['Serial Number']=serial_no
            try:
                result['Protocol Version']=s.version()
            except Exception as e:
                result['Protocol Version']=None
            try:
                result['Cipher Suite']=s.cipher()[0]
            except Exception as e:
                result['Cipher Suite']=None
            try:
                result['Public key length']=s.cipher()[2]
            except Exception as e:
                result['Public key length']=None
            return result    
        except Exception as e:
            return default

    async def __formatting_Output(self,data):
        htmlValue = ""
        htmlValue = await self.__html_table(data)
        return str(htmlValue) 

    async def __html_table(self,data):

        domain = str(data['Domain Name'])
        issue_org = str(data['Issuing Organization'])
        issue_date = str(data['Issue Date'])
        expire_date = str(data['Expire Date'])
        sr_no = str(data['Serial Number'])
        protocol = str(data['Protocol Version'])
        cipher = str(data['Cipher Suite'])
        public_key = str(data['Public key length'])

        percentage = await self.__rating(domain, issue_org, issue_date, expire_date, sr_no, protocol, cipher, public_key)

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
                        <td>""" + domain + """</td>
                    </tr>
                    <tr>
                        <td>Issuing Organization</td>
                        <td>""" + issue_org + """</td>
                    </tr>
                    <tr>
                        <td>Issue Date</td>
                        <td>>""" + issue_date + """</td>
                    </tr>
                    <tr>
                        <td>Expire Date</td>
                        <td>""" + expire_date + """</td>
                    </tr>
                    <tr>
                        <td>Serial Number</td>
                        <td>""" + sr_no + """</td>
                    </tr>
                    <tr>
                        <td>Protocol Version</td>
                        <td >""" + protocol + """</td>
                    </tr>
                    <tr>
                        <td>Cipher Suite</td>
                        <td >""" + cipher + """</td>
                    </tr>
                    <tr>
                        <td>Public key length</td>
                        <td>""" + public_key + """</td>
                    </tr>
            </table>"""
        )
        return table


    async def __rating(self, domain, issue_org, issue_date, expire_date, sr_no, protocol, cipher, public_key):

        condition1 = domain != None
        condition2 = issue_org != None
        condition3 = issue_date != None
        condition4 = expire_date != None
        condition5 = sr_no != None
        condition6 = protocol != None
        condition7 = cipher != None
        condition8 = public_key != None


        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4, condition5, condition6, condition7, condition8])
        
        # Determine the percentage based on the number of satisfied conditions

        if satisfied_conditions == 8:
            percentage = 100
        elif satisfied_conditions == 7:
            percentage = 84
        elif satisfied_conditions == 6:
            percentage = 72
        elif satisfied_conditions == 5:
            percentage = 60
        elif satisfied_conditions == 4:
            percentage = 48
        elif satisfied_conditions == 3:
            percentage = 36
        elif satisfied_conditions == 2:
            percentage = 24
        elif satisfied_conditions == 1:
            percentage = 12
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage