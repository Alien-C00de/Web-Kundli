import ssl
import socket
from colorama import Fore, Style
from util.config_uti import Configuration
from util.issue_config import Issue_Config
from util.report_util import Report_Utility
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
import hashlib
from datetime import datetime

class SSL_Certificate():
    Error_Title = None

    def __init__(self) -> None:
        pass    

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    # Function to fetch and extract certificate details
    async def Get_SSL_Certificate(self, port: int = 443):

        config = Configuration()
        self.Error_Title = config.SSL_CERTIFICATE
        output = ""

        try:
            # Establish SSL connection
            context = ssl.create_default_context()
            connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = self.domain)
            connection.connect((self.domain, port))

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

    async def __formatting_Output(self, cert_details):
        htmlValue = []        
        htmlValue = await self.__html_table(cert_details)
        return htmlValue

    async def __html_table(self, cert_details):

        subject = cert_details["Subject"].get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
        issuer = cert_details["Issuer"].get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
        expires_date = cert_details["Expires"]
        formatted_expire = expires_date.strftime('%d %B %Y').lstrip('0').replace(" 0", " ")
        renewed_date = cert_details["Renewed"]
        formatted_renew = renewed_date.strftime('%d %B %Y').lstrip('0').replace(" 0", " ")
        serial_number = cert_details["Serial Number"]
        fingerprint = cert_details["Fingerprint"]
        ext_key_usage = cert_details["Extended Key Usage"]

        # Rate Extended Key Usage (100% if both server and client auth are found)
        if ("TLS Web Server Authentication" in cert_details["Extended Key Usage"]
            and "TLS Web Client Authentication" in cert_details["Extended Key Usage"]):
            TLS_Web_Server = cert_details["Extended Key Usage"][0]
            TLS_Web_Client = cert_details["Extended Key Usage"][1]
            TLS_OK = True
        else:
            TLS_Web_Server = ""
            TLS_Web_Client = ""
            TLS_OK = False

        # percentage = await self.__rating(cert_details)
        percentage, html = await self.__ssl_score(subject, issuer, expires_date, renewed_date, serial_number, fingerprint, TLS_Web_Server, TLS_Web_Client)
        rep_data = []

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
        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __ssl_score(self, subject, issuer, expire, renew, serial_number, fingerprint, TLS_Web_Server, TLS_Web_Client):
        score = 0
        max_score = 8  
        issues = []
        suggestions = []

        normalized_subject = subject.replace(" ", "").lower()
        # Extract domain part (before '.in') and normalize
        normalized_domain_part = self.domain.split('.')[0].lower()

        # Check if the domain part is contained in the subject
        if normalized_domain_part in normalized_subject:
            score += 1
        else:
            # if subject != "example.com":
            issues.append(Issue_Config.ISSUE_SSL_SUBJECT)
            suggestions.append(Issue_Config.SUGGESTION_SSL_SUBJECT)

        # Check Issuer validity
        trusted_issuers = ["Let's Encrypt Authority X3", "DigiCert", "GlobalSign"]  # Example trusted CAs
        if not any(issuer.startswith(trusted_issuer) for trusted_issuer in trusted_issuers):
            issues.append(Issue_Config.ISSUE_SSL_ISSUER)
            suggestions.append(Issue_Config.SUGGESTION_SSL_ISSUER)
        else:
            score += 1

        # Check expiration date
        if expire.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            issues.append(Issue_Config.ISSUE_SSL_EXPIRES)
            suggestions.append(Issue_Config.SUGGESTION_SSL_EXPIRES)
        else:
            score += 1

        # Check renewal date
        if (datetime.now().replace(tzinfo=None) - renew.replace(tzinfo=None)).days > 365:
            issues.append(Issue_Config.ISSUE_SSL_RENEWED)
            suggestions.append(Issue_Config.SUGGESTION_SSL_RENEWED)
        else:
            score += 1

        # Check Serial Number (ensure it's alphanumeric and not empty)
        if not serial_number or not isinstance(serial_number, str) or not serial_number.isalnum():
            # if not serial_number or not serial_number.isalnum():
            issues.append(Issue_Config.ISSUE_SSL_SERIAL_NUM)
            suggestions.append(Issue_Config.SUGGESTION_SSL_SERIAL_NUM)
        else:
            score += 1

        # Check Fingerprint (ensure it's in the expected format, e.g., 'sha256/...')
        if (not fingerprint.startswith("sha256/") or len(fingerprint) != 71):
            issues.append(Issue_Config.ISSUE_SSL_FINGERPRINT)
            suggestions.append(Issue_Config.SUGGESTION_SSL_FINGERPRINT)
        else:
            score += 1

        # Check Extended Key Usage
        if "TLS Web Server Authentication" not in TLS_Web_Server:
            issues.append(Issue_Config.ISSUE_SSL_TLS_WEB_SERVER_AUTH)
            suggestions.append(Issue_Config.SUGGESTION_SSL_TLS_WEB_SERVER_AUTH)
        else:
            score += 1

        # Check Extended Key Usage
        if "TLS Web Client Authentication" not in TLS_Web_Client:
            issues.append(Issue_Config.ISSUE_SSL_TLS_WEB_CLIENT_AUTH)
            suggestions.append(Issue_Config.SUGGESTION_SSL_TLS_WEB_CLIENT_AUTH)
        else:
            score += 1

        percentage_score = (score / max_score) * 100
        # html_tags = await self.__analysis_table(reasons, suggestions, int(percentage_score))

        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.MODULE_SSL_CERTIFICATE, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags
