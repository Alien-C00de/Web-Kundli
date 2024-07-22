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
