import asyncio
import aiohttp
from colorama import Fore, Style
import socket
import requests
from urllib.parse import urlparse
from util.URL_Verifier import URL_Verifier
from api.server_location import Server_Location 
from api.ssl_certificate import SSL_Certificate
from api.domain_whois import Domain_Whois
from api.server_info import Server_Info
from api.cookies import Cookies
from api.http_security import HTTP_Security
from api.dns_server import DNS_Server
from api.tls_cipher_suite import TLS_Cipher_Suit
from api.dns_records import DNS_Records
from api.txt_records import TXT_Records
from api.server_status import Server_Status
from api.mail_records import Mail_Records
from api.redirect_chain import Redirect_Chain
from api.open_ports import Open_Ports
from api.archive_history import Archive_History
from api.associated_host import Associated_Hosts
from api.block_detection import Block_Detection
from api.carbon_footprint import Carbon_Footprint
from api.crawl_rules import Crawl_Rules
from api.site_features import Site_Features
from api.dns_security_ext import DNS_Security_Ext
from api.tech_stack import Tech_Stack
from api.firewall_detection import Firewall_Detection
from api.social_tags import Social_Tags
from api.threats import Threats
from api.global_ranking import Global_Ranking
from api.security_txt import Security_TXT
from api.nmap_scan import NMap_Scan
from report.html_report import HTML_Report
from util.config_uti import Configuration

class engine():
    ip_address = None
    Error_Title = None

    def __init__(self) -> None:
        pass

    def __init__(self, url, isNmap):
        self.url = url
        self.isNmap = isNmap

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
        response = await self.__get_response()
        aiohttp_res = await self.__get_aiohttp_response()

        ser_loc = Server_Location(self.ip_address)
        ssl_cert = SSL_Certificate(self.url)
        whois_info = Domain_Whois(self.url)
        ser_info = Server_Info(self.ip_address, self.url)
        http_sec = HTTP_Security(self.url, response)
        cookies_info = Cookies(self.url, response)
        dns_Server = DNS_Server(self.ip_address, self.url)
        tls_data = TLS_Cipher_Suit(self.url)
        dns_record_info = DNS_Records(self.url)
        txt_record = TXT_Records(self.url)
        server_status = Server_Status(self.url, response)
        mail_config = Mail_Records(self.url)
        redirect_Record = Redirect_Chain(self.url)
        ports = Open_Ports(self.url)
        archive = Archive_History(self.url)
        associated_host = Associated_Hosts(self.url)
        block_detect = Block_Detection(self.url)
        carbon_print = Carbon_Footprint(self.url)
        crawl_rule = Crawl_Rules(self.url)
        site_feat = Site_Features(self.url, response)
        dns_security = DNS_Security_Ext(self.url)
        tech_stack = Tech_Stack(self.url, response)
        firewall = Firewall_Detection(self.url)
        social_tags = Social_Tags(self.url, response)
        threats = Threats(self.ip_address, self.url)
        global_rank = Global_Ranking(self.url)
        security_txt = Security_TXT(self.url)
        nmap_scan = NMap_Scan(self.ip_address, self.url)

        Server_location = ""
        SSL_Cert = ""
        Whois = ""
        Server_INFO = ""
        Header = []
        cookie = ""
        dns_server_info = ""
        tls_cipher_suite = ""
        dns_info = ""
        txt_info = ""
        server_status_info = ""
        mail_config_info = ""
        redirect_info = ""
        port_info = ""
        archive_info = ""
        associated_info = ""
        block_info = ""
        carbon_info = ""
        crawl_info = ""
        site_info = ""
        dns_sec_info = ""
        tech_stack_info = ""
        firewall_info = ""
        social_tags_info = ""
        threats_info = ""
        global_ranking_info = ""
        security_txt_info = ""
        nmap_info = []

        try:
            tasks = [ ser_loc.Get_Server_Location(), ssl_cert.Get_SSL_Certificate(), whois_info.Get_Whois_Info(),
                    ser_info.Get_Server_Info(), http_sec.Get_HTTP_Security(), cookies_info.Get_Cookies(), dns_Server.Get_DNS_Server(),
                    tls_data.Get_TLS_Cipher_Suit(), dns_record_info.Get_DNS_Records(), txt_record.Get_TXT_Records(),
                    server_status.Get_Server_Status(), mail_config.Get_Mail_Records(), redirect_Record.Get_Redirect_Chain(),
                    ports.Get_Open_Ports(), archive.Get_Archive_History(), associated_host.Get_Associated_Hosts(),
                    block_detect.Get_Block_Detection(), carbon_print.Get_Carbon_Footprint(), crawl_rule.Get_Crawl_Rules(),
                    site_feat.Get_Site_Features(), dns_security.Get_DNS_Security_Ext(), tech_stack.Get_Tech_Stack(),
                    firewall.Get_Firewall_Detection(), social_tags.Get_Social_Tags(),  threats.Get_Threats(),         
                    global_rank.Get_Global_Rank(), security_txt.Get_Security_TXT(),]
            
            if self.isNmap:
                tasks.append(nmap_scan.Get_Nmap_Scan())

            # Server_location, SSL_Cert, Whois, Server_INFO, Header, cookie, DNS_Server, tls_cipher_suite, dns_info, txt_info, server_status_info, mail_config_info, redirect_info, port_info, archive_info, associated_info, block_info, carbon_info, crawl_info, site_info, dns_sec_info, tech_stack_info, firewall_info, social_tags_info, threats_info, global_ranking_info, security_txt_info, nmap_info = (
            #     await asyncio.gather(*tasks))
            
            results = await asyncio.gather(*tasks)

            (Server_location, SSL_Cert, Whois, Server_INFO, Header, cookie, dns_server_info, tls_cipher_suite, dns_info, txt_info, 
            server_status_info, mail_config_info, redirect_info, port_info, archive_info, associated_info, block_info, carbon_info, 
            crawl_info, site_info, dns_sec_info, tech_stack_info, firewall_info, social_tags_info, threats_info, 
            global_ranking_info, security_txt_info) = results[:27]
            if self.isNmap:
                nmap_info = results[27]
            else:
                nmap_info = None
            
            tb1 = str(Server_location)
            tb2 = str(SSL_Cert)
            tb3 = str(Whois)
            tb4 = str(Server_INFO)
            tb5 = str(Header[0])
            tb6 = str(Header[1])
            tb7 = str(cookie)
            tb8 = str(dns_server_info)
            tb9 = str(tls_cipher_suite)
            tb10 = str(dns_info)
            tb11 = str(txt_info)
            tb12 = str(server_status_info)
            tb13 = str(mail_config_info)
            tb14 = str(redirect_info)
            tb15 = str(port_info)
            tb16 = str(archive_info)
            tb17 = str(associated_info)
            tb18 = str(block_info)
            tb19 = str(carbon_info)
            tb20 = str(crawl_info)
            tb21 = str(site_info)
            tb22 = str(dns_sec_info)
            tb23 = str(tech_stack_info)
            tb24 = str(firewall_info)
            tb25 = str(social_tags_info)
            tb26 = str(threats_info)
            tb27 = str(global_ranking_info)
            tb28 = str(security_txt_info)
            if self.isNmap:
                tb29 = nmap_info
            else:
                tb29 = []

            await self.__Generate_Report(tb1, tb2, tb3, tb4, tb5, tb6, tb7, tb8, tb9, tb10, tb11, tb12, tb13, tb14, tb15, 
                                         tb16, tb17, tb18, tb19, tb20, tb21, tb22, tb23, tb24, tb25, tb26, tb27, tb28, tb29)
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Start Process : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

    # Generate the HTML Report
    async def __Generate_Report(self, server_location, SSL_Cert, Whois, ser_info, HTTP_Sec, headers, cookies, dns_server_info, 
                                tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record,
                                ports, archive_info, associated_info, block_info, carbon_info, crawl_info, site_info, dns_sec_info, 
                                tech_stack_info, firewall_info, social_tags_info, threats_info, global_ranking_info, security_txt_info, nmap_info):
        try:
            config = Configuration()
            html_repo = HTML_Report()
            await html_repo.outputHTML(self.url, server_location, SSL_Cert, Whois, ser_info, HTTP_Sec, headers, cookies, dns_server_info, 
                                       tls_cipher_suite, dns_info, txt_info, server_status_info, mail_configuration_info, redirect_Record,
                                       ports, archive_info, associated_info, block_info, carbon_info, crawl_info, site_info, dns_sec_info,
                                       tech_stack_info, firewall_info, social_tags_info, threats_info, global_ranking_info, security_txt_info, nmap_info)
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

    async def __get_response(self):
        response = requests.get(self.url)
        return response
    
    async def __get_aiohttp_response(self):
        async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    return response