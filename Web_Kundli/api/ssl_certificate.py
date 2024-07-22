import ssl
import socket
from colorama import Fore, Style
from util.config_uti import Configuration
from urllib.parse import urlparse
from OpenSSL import crypto
from datetime import datetime

class ssl_certificate():
    Error_Title = None

    def __init__(self) -> None:
        pass    

    def __init__(self, url):
        self.url = url

    # Get SSL Certificate Information
    async def Get_SSL_Certificate_Info(self, port=443):
        config = Configuration()
        self.Error_Title = config.SSL_CERTIFICATE
        result =  urlparse(self.url)
        host = result.netloc
        output = ""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname = host) as sock:
                    certificate = sock.getpeercert()
                    if certificate is None:
                        print(
                            Fore.RED
                            + Style.BRIGHT
                            + "Failed to retrieve SSL certificate."
                            + Fore.RESET
                            + Style.RESET_ALL
                        )
                        return None

                    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(sock.getpeercert(True)))
                    output = await self.__formatting_Output(x509)
                    return output
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_SSL_Certificate_Info : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        finally:
            sock.close()

    async def __formatting_Output(self, x509):
        htmlValue = ""        
        htmlValue = await self.__html_table(x509)
        return str(htmlValue)

    async def __html_table(self, x509):
        expires_date = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        renewed_date = datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Subject</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x509.get_subject().CN)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Issuer</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + x509.get_issuer().CN
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Expires</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(expires_date)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Renewed</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(renewed_date)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Serial Num</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x509.get_serial_number())
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;"><span class="lbl">Fingerprint</span><span class="lbl"><br /></span></span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x509.digest("sha256").decode("utf-8")) + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
