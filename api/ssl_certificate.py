import ssl
import socket
from colorama import Fore, Style
from util.config_uti import Configuration
from urllib.parse import urlparse
from OpenSSL import crypto
from datetime import datetime

class SSL_Certificate():
    Error_Title = None

    def __init__(self) -> None:
        pass    

    def __init__(self, url):
        self.url = url

    # Get SSL Certificate Information
    async def Get_SSL_Certificate(self, port=443):
        config = Configuration()
        self.Error_Title = config.SSL_CERTIFICATE
        result =  urlparse(self.url)
        host = result.netloc
        output = ""
        try:
            # print("ssl_certificate.py: start")
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
                    # print("ssl_certificate.py: output: ")
                    return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_SSL_Certificate : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        finally:
            sock.close()

    async def __formatting_Output(self, x509):
        htmlValue = ""        
        htmlValue = await self.__html_table(x509)
        return str(htmlValue)

    async def __html_table(self, x509):

        percentage =  await self.__rating(x509)

        expires_date = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        renewed_date = datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
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
                        <td>Subject</td>
                        <td>""" + str(x509.get_subject().CN) + """</td>
                    </tr>
                    <tr>
                        <td>Issuer</td>
                        <td>""" + str(x509.get_issuer().CN) + """</td>
                    </tr>
                    <tr>
                        <td>Expires</td>
                        <td>""" + str(expires_date) + """</td>
                    </tr>
                    <tr>
                        <td>Renewed</td>
                        <td>""" + str(renewed_date) + """</td>
                    </tr>
                    <tr>
                        <td>Serial Num</td>
                        <td>""" + str(x509.get_serial_number()) + """</td>
                    </tr>
                    <tr>
                        <td>Fingerprint</td>
                        <td>""" + str(x509.digest("sha256").decode("utf-8")) + """</td>
                    </tr>
            </table>"""
        )
        return table

    async def __rating(self, x509):
        issuer =  str(x509.get_issuer().CN)
        expires_date = str(datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ'))
        renewed_date = str(datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ'))
        fingerprint = str(x509.digest("sha256").decode("utf-8"))

        condition1 = issuer != ""
        condition2 = expires_date != ""
        condition3 = renewed_date != ""
        condition4 = fingerprint != ""

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

