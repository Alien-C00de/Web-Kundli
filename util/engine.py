import asyncio
import aiohttp
from colorama import Fore, Style
import datetime
import socket
import requests
import os
import traceback
from urllib.parse import urlparse
from util.URL_Verifier import URL_Verifier
from api.server_location import Server_Location 
from api.ssl_certificate import SSL_Certificate
from api.domain_whois import Domain_Whois
from api.cookies import Cookies 
from api.http_security import HTTP_Security
from api.dns_server import DNS_Server
from api.tls_cipher_suite import TLS_Cipher_Suit
from api.dns_records import DNS_Records
from api.server_status import Server_Status
from api.mail_record import Mail_Records
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
from api.nmap_ops import Nmap_Ops
from report.summary_report import Summary_Report
from report.analysis_report import Analysis_Report
from util.config_uti import Configuration

class engine():
    ip_address = None
    domain = None
    Error_Title = None

    def __init__(self) -> None:
        pass

    def __init__(self, url, mode, isNmap):
        self.url = url
        self.mode = mode
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
        self.domain = await self.__get_domain()
        response = await self.__get_response()
        # aiohttp_res = await self.__get_aiohttp_response()

        ser_loc = Server_Location(self.ip_address, self.domain)
        ssl_cert = SSL_Certificate(self.url, self.domain)
        whois_info = Domain_Whois(self.url, self.domain)
        http_sec = HTTP_Security(self.url, response, self.domain)
        cookies_info = Cookies(self.url, response, self.domain)
        dns_Server = DNS_Server(self.ip_address, self.url, self.domain)
        tls_data = TLS_Cipher_Suit(self.url, self.domain)
        dns_record_info = DNS_Records(self.url, self.domain)
        # txt_record = TXT_Records(self.url, self.domain)
        server_status = Server_Status(self.url, response, self.domain)
        mail_config = Mail_Records(self.url, self.domain)
        redirect_Record = Redirect_Chain(self.url, self.domain)
        ports = Open_Ports(self.url, self.ip_address, self.domain)
        archive = Archive_History(self.url, self.domain)
        associated_host = Associated_Hosts(self.url, self.domain)
        block_detect = Block_Detection(self.url, self.ip_address, self.domain)
        carbon_print = Carbon_Footprint(self.url, self.domain)
        crawl_rule = Crawl_Rules(self.url, self.domain)
        site_feat = Site_Features(self.url, response, self.domain)
        dns_security = DNS_Security_Ext(self.url, self.domain)
        tech_stack = Tech_Stack(self.url, response, self.domain)
        firewall = Firewall_Detection(self.url, self.domain)
        social_tags = Social_Tags(self.url, response, self.domain)
        threats = Threats(self.ip_address, self.url, self.domain)
        global_rank = Global_Ranking(self.url, self.domain)
        security_txt = Security_TXT(self.url, self.domain)
        # nmap_scan = NMap_Scan(self.ip_address, self.url, self.domain)
        nmap_ops  = Nmap_Ops(self.ip_address, self.url, self.domain)

        Server_location = []
        SSL_Cert = []
        Whois = []
        Header = []
        cookie = []
        dns_server_info = []
        tls_cipher_suite = []
        dns_txt_email_config_info = []
        server_status_info = []
        mail_config_info = []
        redirect_info = []
        port_info = []
        archive_info = []
        associated_info = []
        block_info = []
        carbon_info = []
        crawl_info = []
        site_info = []
        dns_sec_info = []
        tech_stack_info = []
        firewall_info = []
        social_tags_info = []
        threats_info = []
        global_ranking_info = []
        security_txt_info = []
        nmap_ops_data = []

        try:
            tasks = [ser_loc.Get_Server_Location(), ssl_cert.Get_SSL_Certificate(), whois_info.Get_Whois_Info(),
                    http_sec.Get_HTTP_Security(), cookies_info.Get_Cookies(), dns_Server.Get_DNS_Server(),
                    tls_data.Get_TLS_Cipher_Suit(), dns_record_info.Get_DNS_Records(), 
                    server_status.Get_Server_Status(), mail_config.Get_Mail_Records(), redirect_Record.Get_Redirect_Chain(),
                    ports.Get_Open_Ports(), archive.Get_Archive_History(), associated_host.Get_Associated_Hosts(),
                    block_detect.Get_Block_Detection(), carbon_print.Get_Carbon_Footprint(), crawl_rule.Get_Crawl_Rules(),
                    site_feat.Get_Site_Features(), dns_security.Get_DNS_Security_Ext(), tech_stack.Get_Tech_Stack(),
                    firewall.Get_Firewall_Detection(), social_tags.Get_Social_Tags(),  threats.Get_Threats(),         
                    global_rank.Get_Global_Rank(), security_txt.Get_Security_TXT()]

            if self.isNmap:
                tasks.append(nmap_ops.Get_Nmap_Ops())

            results = await asyncio.gather(*tasks)

            (Server_location, SSL_Cert, Whois, Header, cookie, dns_server_info, tls_cipher_suite, dns_txt_email_config_info,  
            server_status_info, mail_config_info, redirect_info, port_info, archive_info, associated_info, block_info, carbon_info, 
            crawl_info, site_info, dns_sec_info, tech_stack_info, firewall_info, social_tags_info, threats_info, 
            global_ranking_info, security_txt_info) = results[:25]
            if self.isNmap:
                nmap_ops_data = results[25]
            else:
                nmap_ops_data = None

            if self.isNmap:
                nmap = nmap_ops_data
            else:
                nmap = []

            timestamp = datetime.datetime.now()

            await self.__create_dirs("output")

            summary_report = Summary_Report(self.domain, timestamp)
            analysis_report = Analysis_Report(self.domain, timestamp)

            final_report = [summary_report.Generate_Summary_Report(self.url, str(Server_location[0]), str(SSL_Cert[0]), str(Whois[0]), 
                                    str(Server_location[2]), str(Header[0]), str(Header[2]), str(cookie[0]), str(dns_server_info[0]), 
                                    str(tls_cipher_suite[0]), str(dns_txt_email_config_info[0]), str(dns_txt_email_config_info[2]), str(server_status_info[0]), 
                                    str(mail_config_info[0]), str(redirect_info[0]), str(port_info[0]), str(archive_info[0]), 
                                    str(associated_info[0]), str(block_info[0]), str(carbon_info[0]), str(crawl_info[0]), 
                                    str(site_info[0]), str(dns_sec_info[0]), str(tech_stack_info[0]), str(firewall_info[0]), 
                                    str(social_tags_info[0]), str(threats_info[0]), str(global_ranking_info[0]), str(security_txt_info[0]), 
                                    nmap, int(self.mode)), 
                            
                            analysis_report.Generate_Analysis_Report(self.url, str(cookie[1]), str(Server_location[1]), str(Server_location[3]), 
                                    str(SSL_Cert[1]), str(archive_info[1]), str(associated_info[1]), str(block_info[1]), str(carbon_info[1]), 
                                    str(crawl_info[1]), str(dns_sec_info[1]), str(dns_server_info[1]), str(Whois[1]), str(Header[1]),
                                    str(Header[3]), str(firewall_info[1]), str(global_ranking_info[1]), str(port_info[1]), str(redirect_info[1]),
                                    str(security_txt_info[1]), str(server_status_info[1]), str(site_info[1]), str(social_tags_info[1]),
                                    str(tech_stack_info[1]), str(threats_info[1]), str(dns_txt_email_config_info[1]), 
                                    str(dns_txt_email_config_info[3]), str(tls_cipher_suite[1]), str(mail_config_info[1]), 
                                    nmap)]

            await asyncio.gather(*final_report)
            
        except Exception as ex:
            error_type, error_message, tb = ex.__class__.__name__, str(ex), traceback.extract_tb(ex.__traceback__)
            error_details = tb[-1]  # Get the last traceback entry (most recent call)
            file_name = error_details.filename
            method_name = error_details.name
            line_number = error_details.lineno

            error_msg = f"❌ {self.Error_Title} => ERROR in method '{method_name}' at line {line_number} : {error_type}: {error_message}"
            print(Fore.RED + Style.BRIGHT + error_msg + Fore.RESET + Style.RESET_ALL)
                    
            # error_msg = ex.args[0]
            # msg = "[-] " + self.Error_Title + " => Start Process : " + error_msg
            # print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

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
            print(f"🌐 The {self.url} IP Address is {ip}\n")
            return ip
        except socket.gaierror as ex:
            error_msg = str(ex)
            msg = "[-] " + self.Error_Title + ": Invalid URL " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL) 
            exit(0)

    # Domain name of the given URL
    async def __get_domain(self):
        try:
            result = urlparse(self.url)
            domain = result.netloc
            return domain
        except socket.gaierror as ex:
            error_msg = str(ex)
            msg = "[-] " + self.Error_Title + ": Invalid URL " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL) 
            exit(0)

    async def __get_response(self):
        response = requests.get(self.url)
        return response

    async def __create_dirs(self, root, subfolders = None):
        root = root if subfolders == None else f"{root}/{subfolders}/"
        if not os.path.exists(root):
            os.makedirs(f"{root}", exist_ok=True)

    async def __get_aiohttp_response(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return response
