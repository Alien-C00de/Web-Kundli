import ssl
import socket
from colorama import Fore, Style
from util.config_uti import Configuration
from urllib.parse import urlparse
from OpenSSL import crypto
from datetime import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
import hashlib

class SSL_Certificate():
    Error_Title = None

    def __init__(self) -> None:
        pass    

    def __init__(self, url):
        self.url = url

    # Function to fetch and extract certificate details
    async def Get_SSL_Certificate(self, port: int = 443):

        config = Configuration()
        self.Error_Title = config.SSL_CERTIFICATE
        result = urlparse(self.url)
        hostname = result.netloc
        output = ""

        try:
            # Establish SSL connection
            context = ssl.create_default_context()
            connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = hostname)
            connection.connect((hostname, port))

            # Get the certificate in binary form
            cert = connection.getpeercert(binary_form=True)
            # Load the certificate using the cryptography library
            cert_obj = x509.load_der_x509_certificate(cert, default_backend())

            # Extract the details from the certificate
            cert_details = {
                "Subject": cert_obj.subject,
                "Issuer": cert_obj.issuer,
                "Expires": cert_obj.not_valid_after_utc,
                "Renewed": cert_obj.not_valid_before_utc,
                "Serial Number": cert_obj.serial_number,
            }

            # Compute the Fingerprint (SHA-256)
            fingerprint = hashlib.sha256(cert).hexdigest()
            cert_details["Fingerprint"] = fingerprint

            # Extract Extended Key Usage (EKU) for server and client authentication
            ext_key_usage = []
            for eku in cert_obj.extensions:
                if eku.oid == x509.oid.ExtensionOID.EXTENDED_KEY_USAGE:
                    extended_usage = eku.value
                    for purpose in extended_usage:
                        if purpose == x509.oid.ExtendedKeyUsageOID.SERVER_AUTH:
                            ext_key_usage.append("TLS Web Server Authentication")
                        if purpose == x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH:
                            ext_key_usage.append("TLS Web Client Authentication")

            cert_details["Extended Key Usage"] = ext_key_usage
            output = await self.__formatting_Output(cert_details)
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_SSL_Certificate : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output
        finally:
            connection.close()

    # # Get SSL Certificate Information
    # async def Get_SSL_Certificate(self, port=443):
    #     config = Configuration()
    #     self.Error_Title = config.SSL_CERTIFICATE
    #     result =  urlparse(self.url)
    #     host = result.netloc
    #     output = ""
    #     try:
    #         # print("ssl_certificate.py: start")
    #         context = ssl.create_default_context()
    #         with socket.create_connection((host, port)) as sock:
    #             with context.wrap_socket(sock, server_hostname = host) as sock:
    #                 certificate = sock.getpeercert()
    #                 if certificate is None:
    #                     print(Fore.RED + Style.BRIGHT + "Failed to retrieve SSL certificate." + Fore.RESET + Style.RESET_ALL)
    #                     return None

    #                 x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(sock.getpeercert(True)))
    #                 output = await self.__formatting_Output(x509)
    #                 # print("ssl_certificate.py: output: ")
    #                 return output
    #     except Exception as ex:
    #         error_msg = str(ex.args[0])
    #         msg = "[-] " + self.Error_Title + " => Get_SSL_Certificate : " + error_msg
    #         print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
    #         return output
    #     finally:
    #         sock.close()

    async def __formatting_Output(self, cert_details):
        htmlValue = ""        
        htmlValue = await self.__html_table(cert_details)
        return str(htmlValue)

    async def __html_table(self, cert_details):

        percentage = await self.__rating(cert_details)

        subject = cert_details["Subject"].get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
        issuer = cert_details["Issuer"].get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
        expires_date = cert_details["Expires"]
        formatted_expire = expires_date.strftime('%d %B %Y').lstrip('0').replace(" 0", " ")
        renewed_date = cert_details["Renewed"]
        formatted_renew = renewed_date.strftime('%d %B %Y').lstrip('0').replace(" 0", " ")
        serial_number = cert_details["Serial Number"]
        fingerprint = cert_details["Fingerprint"]
        # Rate Extended Key Usage (100% if both server and client auth are found)
        if ("TLS Web Server Authentication" in cert_details["Extended Key Usage"]
            and "TLS Web Client Authentication" in cert_details["Extended Key Usage"]):
            TLS_Web_Server = cert_details["Extended Key Usage"][0]
            TLS_Web_Client = cert_details["Extended Key Usage"][0]
            TLS_OK = True
        else:
            TLS_Web_Server = ""
            TLS_Web_Client = ""
            TLS_OK = False
        # expires_date = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        # formatted_expire = expires_date.strftime('%d %B %Y').lstrip('0').replace(" 0", " ")
        # renewed_date = datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
        # formatted_renew = renewed_date.strftime('%d %B %Y').lstrip('0').replace(" 0", " ")

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
                        <td>""" + str(subject) + """</td>
                    </tr>
                    <tr>
                        <td>Issuer</td>
                        <td>""" + str(issuer) + """</td>
                    </tr>
                    <tr>
                        <td>Expires</td>
                        <td>""" + str(formatted_expire) + """</td>
                    </tr>
                    <tr>
                        <td>Renewed</td>
                        <td>""" + str(formatted_renew) + """</td>
                    </tr>
                    <tr>
                        <td>Serial Num</td>
                        <td>""" + str(serial_number) + """</td>
                    </tr>
                    <tr>
                        <td>Fingerprint</td>
                        <td>""" + str(fingerprint) + """</td>
                    </tr>""" + ("""
                    <tr>
                        <td> <h3>Extended Key Usage</h3> </td>
                        <td></td>
                    </tr> 
                    <tr>
                        <td>""" + str(TLS_Web_Server) + """</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>""" + str(TLS_Web_Client) + """</td>
                        <td></td>
                    </tr>
                    """ if TLS_OK else "")  # Add this block only if TLS_OK is True
            + """
            </table>"""
        )
        return table

    async def __rating(self, cert_details):
        score = 0

        # Define weights for each parameter
        weights = {
            "Subject": 15,
            "Issuer": 10,
            "Expires": 15,
            "Renewed": 10,
            "Serial Number": 10,
            "Fingerprint": 15,
            "Extended Key Usage": 25,
        }

        # Rate Subject (100% if present and valid)
        if cert_details["Subject"]:
            score += weights["Subject"]

        # Rate Issuer (100% if present and valid)
        if cert_details["Issuer"]:
            score += weights["Issuer"]

        # Rate Expiration Date (100% if valid)
        if cert_details["Expires"].replace(tzinfo=None)  > datetime.utcnow().replace(tzinfo=None):
            score += weights["Expires"]

        # Rate Renewed Date (100% if valid)
        if cert_details["Renewed"].replace(tzinfo=None)  < datetime.utcnow().replace(tzinfo=None):
            score += weights["Renewed"]

        # Rate Serial Number (100% if present)
        if cert_details["Serial Number"]:
            score += weights["Serial Number"]

        # Rate Fingerprint (100% if present)
        if cert_details["Fingerprint"]:
            score += weights["Fingerprint"]

        # Rate Extended Key Usage (100% if both server and client auth are found)
        if (
            "TLS Web Server Authentication" in cert_details["Extended Key Usage"]
            and "TLS Web Client Authentication" in cert_details["Extended Key Usage"]
        ):
            score += weights["Extended Key Usage"]

        # Calculate percentage score
        total_weight = sum(weights.values())
        percentage_score = int((score / total_weight) * 100)
        return percentage_score
