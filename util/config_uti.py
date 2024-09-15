import os
from configparser import ConfigParser


class Configuration:
    # Reading Configs
    config = ConfigParser()
    config_path = os.path.join("./config", "config.ini")
    config.read(config_path)

    "General" in config
    VERSION = config["General"]["VERSION"]
    AUTHOR = config["General"]["AUTHOR"]
    YEAR = config["General"]["YEAR"]
    EMAIL = config["General"]["EMAIL"]
    GITHUB = config["General"]["GITHUB"]

    'Error_Module' in config
    SERVER_LOCATION = config['Error_Module']['SERVER_LOCATION']
    ENGINE = config['Error_Module']['ENGINE']
    SSL_CERTIFICATE = config['Error_Module']['SSL_CERTIFICATE']
    WHOIS = config['Error_Module']['WHOIS']
    SERVER_INFO = config['Error_Module']['SERVER_INFO']
    HTTP_SECURITY = config['Error_Module']['HTTP_SECURITY']
    COOKIES = config['Error_Module']['COOKIES']
    DNS_SERVER = config['Error_Module']['DNS_SERVER']
    SERVER_LOCATION = config["Error_Module"]["SERVER_LOCATION"]
    SERVER_STATUS = config["Error_Module"]["SERVER_STATUS"]
    TLS_CIPHER_SUIT = config["Error_Module"]["TLS_CIPHER_SUIT"]
    TLS_RECORD = config["Error_Module"]["TLS_RECORD"]
    MAIL_CONFIGURATION = config["Error_Module"]["MAIL_CONFIGURATION"]
    PORT_SCANNING = config["Error_Module"]["PORT_SCANNING"]
    REDIRECT_FETCH = config["Error_Module"]["REDIRECT_FETCH"]
    ARCHIVE_HISTORY = config["Error_Module"]["ARCHIVE_HISTORY"]
    ASSOCIATED_HOSTS = config["Error_Module"]["ASSOCIATED_HOSTS"]
    BLOCK_DETECTION = config["Error_Module"]["BLOCK_DETECTION"]
    CARBON_FOOTPRINT = config["Error_Module"]["CARBON_FOOTPRINT"]
    CRAWL_RULES = config["Error_Module"]["CRAWL_RULES"]
    SITE_FEATURES = config["Error_Module"]["SITE_FEATURES"]
    DNS_SECURITY_EXT = config["Error_Module"]["DNS_SECURITY_EXT"]
    TECH_STACK = config["Error_Module"]["TECH_STACK"]
    FIREWALL = config["Error_Module"]["FIREWALL"]
    SOCIAL_TAGS = config["Error_Module"]["SOCIAL_TAGS"]
    THREATS = config["Error_Module"]["THREATS"]
    GLOBAL_RANKING = config["Error_Module"]["GLOBAL_RANKING"]
    SECURITY_TXT = config["Error_Module"]["SECURITY_TXT"]
    NMAP_SCAN = config["Error_Module"]["NMAP_SCAN"]

    'Report' in config
    REPORT_HEADER = config['Report']['REPORT_HEADER']
    REPORT_SUB_TITLE = config['Report']['REPORT_SUB_TITLE']
    REPORT_FILE_NAME = config['Report']['REPORT_FILE_NAME']

    'IPAPI.IO' in config
    IPAPI_IO_ENDPOINT_URL = config['IPAPI.IO']['ENDPOINT_URL'] 
    IPAPI_IO_REPORT_SUB_TITLE = config['IPAPI.IO']['REPORT_SUB_TITLE']

    'SHODAN' in config
    SHODAN_ENDPOINT_URL = config['SHODAN']['ENDPOINT_URL']
    SHODAN_API_KEY = config['SHODAN']['API_KEY']

    "ARCHIVE.ORG" in config
    ARCHIVE_ENDPOINT_URL = config["ARCHIVE.ORG"]["ENDPOINT_URL"]

    "ASSOCIATED" in config
    ASSOCIATED_ENDPOINT_URL = config["ASSOCIATED"]["ENDPOINT_URL"]

    "CARBON_API" in config
    CARBON_API_ENDPOINT_URL = config["CARBON_API"]["ENDPOINT_URL"]    

    "CRAWL_FILE" in config
    CRAWL_FILE = config["CRAWL_FILE"]["FILE_NAME"]   

    "DNS_SECURITY_API" in config
    DNS_SECURITY_API = config["DNS_SECURITY_API"]["ENDPOINT_URL"]

    "VIRUS_TOTAL" in config
    VIRUS_TOTAL_ENDPOINT_URL = config["VIRUS_TOTAL"]["ENDPOINT_URL"]
    VIRUS_TOTAL_API_KEY = config["VIRUS_TOTAL"]["API_KEY"]
    
    "TRANCO" in config
    TRANCO_ENDPOINT_URL = config["TRANCO"]["ENDPOINT_URL"]
