import ssl
import socket
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style
from util.config_uti import Configuration

class tls_cipher:
    Error_Title = None
    
    def __init__(self,url):
        self.url=url

    async def Get_TLS_Cipher(self):
        config = Configuration()
        self.Error_Title = config.TLS_CIPHER_SUIT
        output=""
        try:
            domain_name = urlparse(self.url).netloc 
            res=await self.__final_result(domain_name)
            output= await self.__formatting_Output(res)
            return output

        # output=self.__formatting_Output(domain_name,issue_org,issue,expire,protocal_verion,cipher,length,serial)
        # return output
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_TLS_Cipher : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __final_result(self,domain_name):
        default={'Domain Name': None, 'Issuing Organization': None, 'Issue Date': None, 'Expire Date': None, 'Serial Number': None, 'Protocol Version': None, 'Cipher Suite': None, 'Public key length': None}
        try:
            result={}
            context = ssl.create_default_context()
            s=context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain_name)
            content=s.connect((domain_name, 443))
            result["Domain Name"]=domain_name
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
        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Domain Name</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Domain Name'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Issuing Organization</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Issuing Organization'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Issue Date</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Issue Date'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Expire Date</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Expire Date'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Serial Number</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Serial Number'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Protocol Version</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Protocol Version'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Cipher Suite</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Cipher Suite'])
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Public key length</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(data['Public key length'])
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
