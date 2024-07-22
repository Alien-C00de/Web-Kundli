import asyncio
from colorama import Fore, Style
import socket
from urllib.parse import urlparse
from util.URL_Verifier import URL_Verifier
from api.server_location import server_location 
from api.ssl_certificate import ssl_certificate
from api.domain_whois import domain_whois
from api.server_info import ServerInfo
from api.cookies import cookies
from api.http_security import http_security
from api.DNS_Server_Info import DNS_Server_Info
from api.tls_cipher_cuite import tls_cipher
from api.dns_record_fetch import DNS_RECORDS
from api.txt_record_fetch import TXT_RECORDS
from api.server_status_fetch import SERVER_STATUS
from api.mail_configration_fetch import MAIL_RECORDS
from api.redirect_fetch import REDIRECT_PAGE
from api.Port_Scanning import OPEN_PORTS
from report.html_report import html_report
from util.config_uti import Configuration

class engine():
    ip_address = None
    Error_Title = None

    def __init__(self) -> None:
        pass

    def __init__(self, url):
        self.url = url

    # Global function to start the engine
    async def Start_Engine(self):
        config = Configuration()
        self.Error_Title = config.ENGINE
        if await self.__Is_Valid_Site():
            await self.__Start_Process()
        else:
            print(Fore.RED + Style.BRIGHT + f"[-] Invalid Website : {self.url}", Style.RESET_ALL, flush=True, end="\n\n")
            exit(0)

    # To start all the 38 processes parallely
    async def __Start_Process(self):
        self.ip_address = await self.__get_ip_address()

        ser_loc = server_location(self.ip_address)
        ssl_cert = ssl_certificate(self.url)
        whois_info = domain_whois(self.url)
        ser_info = ServerInfo(self.ip_address, self.url)
        http_sec = http_security(self.url)
        cookies_info = cookies(self.url)
        dns_Server = DNS_Server_Info(self.ip_address, self.url)
        tls_data = tls_cipher(self.url)
        dns_record_info = DNS_RECORDS(self.url)
        txt_record = TXT_RECORDS(self.url)
        server_status = SERVER_STATUS(self.url)
        main_configurations = MAIL_RECORDS(self.url)
        redirect_Record = REDIRECT_PAGE(self.url)
        ports = OPEN_PORTS(self.url)

        Server_location = ""
        SSL_Cert = ""
        Whois = ""
        Server_INFO = ""
        Header = []
        cookie = ""
        DNS_Server = ""
        tls_cipher_suite = ""
        dns_info = ""
        txt_info = ""
        server_status_info = ""
        mail_configuration_info = ""
        redirect_info = ""
        port_info = ""

        try:
            Server_location, SSL_Cert, Whois, Server_INFO, Header, cookie, DNS_Server ,tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_info, port_info = (
                await asyncio.gather(
                    ser_loc.Get_Server_Location(),
                    ssl_cert.Get_SSL_Certificate_Info(),
                    whois_info.Get_Whois_Info(),
                    ser_info.Get_Server_Info(),
                    http_sec.Get_HTTP_Headers(),
                    cookies_info.Get_Cookies(),
                    dns_Server.Get_DNS_Server_Info(),
                    tls_data.Get_TLS_Cipher(),
                    dns_record_info.Get_DNS_Records(),
                    txt_record.Get_TXT_Records(),
                    server_status.Get_Server_Status(),
                    main_configurations.Get_Mail_Records(),
                    redirect_Record.Get_Redirect(),
                    ports.Get_Open_Ports(),
                )
            )
            tb1 = str(Server_location)
            tb2 = str(SSL_Cert)
            tb3 = str(Whois)
            tb4 = str(Server_INFO)
            tb5 = str(Header[0])
            tb6 = str(Header[1])
            tb7 = str(cookie)
            tb8 = str(DNS_Server)
            tb9 = str(tls_cipher_suite)
            tb10 = str(dns_info)
            tb11 = str(txt_info)
            tb12 = str(server_status_info)
            tb13 = str(mail_configuration_info)
            tb14 = str(redirect_info)
            tb15 = str(port_info)
            await self.__Generate_Report(tb1, tb2, tb3, tb4, tb5, tb6, tb7, tb8, tb9, tb10, tb11, tb12, tb13, tb14, tb15)
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Start Process : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

    # Generate the HTML Report
    async def __Generate_Report(self, server_location, SSL_Cert, Whois, ser_info, HTTP_Sec, headers, 
                                cookies, DNS_Server, tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record, ports):
        try:
            config = Configuration()
            html_repo = html_report()
            await html_repo.outputHTML(server_location, SSL_Cert, Whois, ser_info, HTTP_Sec, headers,
                                        cookies, DNS_Server, tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record, ports)
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Generate report : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

    # Is the given URL is valid or not
    async def __Is_Valid_Site(self):
        try:
            auth = URL_Verifier(self.url)
            if await auth.is_url() or await auth.is_ip_address():
                # print(f"[+] Valid Website : {self.url}", flush=True)
                return True
            else:
                return False
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + ": " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL) 

    # Ip Address of the given URL
    async def __get_ip_address(self):
        try:
            domain_name = urlparse(self.url).netloc
            ip = socket.gethostbyname(domain_name)
            print(f'[+] The {self.url} IP Address is {ip}')
            return ip
        except socket.gaierror as ex:
            error_msg = str(ex)
            msg = "[-] " + self.Error_Title + ": Invalid URL " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL) 
            exit(0)
