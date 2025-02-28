import os
from configparser import ConfigParser


class Issue_Config:

    # Reading Configs
    config = ConfigParser()
    config_path = os.path.join("./config", "issue_list.ini")
    config.read(config_path)

    "Cookies" in config
    ISSUE_COOKIES_SESSION_NAME = config["Cookies"]["ISSUE_COOKIES_SESSION_NAME"]
    ISSUE_COOKIES_SESSION_VALUE = config["Cookies"]["ISSUE_COOKIES_SESSION_VALUE"]
    ISSUE_COOKIES_DOMAIN = config["Cookies"]["ISSUE_COOKIES_DOMAIN"]
    ISSUE_COOKIES_PATH = config["Cookies"]["ISSUE_COOKIES_PATH"]
    ISSUE_COOKIES_EXPIRES = config["Cookies"]["ISSUE_COOKIES_EXPIRES"]
    ISSUE_COOKIES_SECURE = config["Cookies"]["ISSUE_COOKIES_SECURE"]

    SUGGESTION_COOKIES_SESSION_NAME = config["Cookies"]["SUGGESTION_COOKIES_SESSION_NAME"]
    SUGGESTION_COOKIES_SESSION_VALUE = config["Cookies"]["SUGGESTION_COOKIES_SESSION_VALUE"]
    SUGGESTION_COOKIES_DOMAIN = config["Cookies"]["SUGGESTION_COOKIES_DOMAIN"]
    SUGGESTION_COOKIES_PATH = config["Cookies"]["SUGGESTION_COOKIES_PATH"]
    SUGGESTION_COOKIES_EXPIRES = config["Cookies"]["SUGGESTION_COOKIES_EXPIRES"]
    SUGGESTION_COOKIES_SECURE = config["Cookies"]["SUGGESTION_COOKIES_SECURE"]

    "Server Location" in config
    ISSUE_LOCATION_CITY = config["Server Location"]["ISSUE_LOCATION_CITY"]
    ISSUE_LOCATION_COUNTRY = config["Server Location"]["ISSUE_LOCATION_COUNTRY"]
    ISSUE_LOCATION_TIMEZONE = config["Server Location"]["ISSUE_LOCATION_TIMEZONE"]
    ISSUE_LOCATION_LANGUAGES = config["Server Location"]["ISSUE_LOCATION_LANGUAGES"]
    ISSUE_LOCATION_CURRENCY = config["Server Location"]["ISSUE_LOCATION_CURRENCY"]

    SUGGESTION_LOCATION_CITY = config["Server Location"]["SUGGESTION_LOCATION_CITY"]
    SUGGESTION_LOCATION_COUNTRY = config["Server Location"]["SUGGESTION_LOCATION_COUNTRY"]
    SUGGESTION_LOCATION_TIMEZONE = config["Server Location"]["SUGGESTION_LOCATION_TIMEZONE"]
    SUGGESTION_LOCATION_LANGUAGES = config["Server Location"]["SUGGESTION_LOCATION_LANGUAGES"]
    SUGGESTION_LOCATION_CURRENCY = config["Server Location"]["SUGGESTION_LOCATION_CURRENCY"]

    "Server info" in config
    ISSUE_SERVER_INFO_ORGANIZATION = config["Server info"]["ISSUE_SERVER_INFO_ORGANIZATION"]
    ISSUE_SERVER_INFO_ASN = config["Server info"]["ISSUE_SERVER_INFO_ORGANIZATION"]
    ISSUE_SERVER_INFO_IP = config["Server info"]["ISSUE_SERVER_INFO_ORGANIZATION"]
    ISSUE_SERVER_INFO_LOCATION = config["Server info"]["ISSUE_SERVER_INFO_ORGANIZATION"]

    SUGGESTION_SERVER_INFO_ORGANIZATION = config["Server info"]["SUGGESTION_SERVER_INFO_ORGANIZATION"]
    SUGGESTION_SERVER_INFO_ASN = config["Server info"]["SUGGESTION_SERVER_INFO_ASN"]
    SUGGESTION_SERVER_INFO_IP = config["Server info"]["SUGGESTION_SERVER_INFO_IP"]
    SUGGESTION_SERVER_INFO_LOCATION = config["Server info"]["SUGGESTION_SERVER_INFO_LOCATION"]

    "SSL Certificate" in config
    ISSUE_SSL_SUBJECT = config["SSL Certificate"]["ISSUE_SSL_SUBJECT"]
    ISSUE_SSL_ISSUER = config["SSL Certificate"]["ISSUE_SSL_ISSUER"]
    ISSUE_SSL_EXPIRES = config["SSL Certificate"]["ISSUE_SSL_EXPIRES"]
    ISSUE_SSL_RENEWED = config["SSL Certificate"]["ISSUE_SSL_RENEWED"]
    ISSUE_SSL_SERIAL_NUM = config["SSL Certificate"]["ISSUE_SSL_SERIAL_NUM"]
    ISSUE_SSL_FINGERPRINT = config["SSL Certificate"]["ISSUE_SSL_FINGERPRINT"]
    ISSUE_SSL_TLS_WEB_SERVER_AUTH = config["SSL Certificate"]["ISSUE_SSL_TLS_WEB_SERVER_AUTH"]
    ISSUE_SSL_TLS_WEB_CLIENT_AUTH = config["SSL Certificate"]["ISSUE_SSL_TLS_WEB_CLIENT_AUTH"]

    SUGGESTION_SSL_SUBJECT = config["SSL Certificate"]["SUGGESTION_SSL_SUBJECT"]
    SUGGESTION_SSL_ISSUER = config["SSL Certificate"]["SUGGESTION_SSL_ISSUER"]
    SUGGESTION_SSL_EXPIRES = config["SSL Certificate"]["SUGGESTION_SSL_EXPIRES"]
    SUGGESTION_SSL_RENEWED = config["SSL Certificate"]["SUGGESTION_SSL_RENEWED"]
    SUGGESTION_SSL_SERIAL_NUM = config["SSL Certificate"]["SUGGESTION_SSL_SERIAL_NUM"]
    SUGGESTION_SSL_FINGERPRINT = config["SSL Certificate"]["SUGGESTION_SSL_FINGERPRINT"]
    SUGGESTION_SSL_TLS_WEB_SERVER_AUTH = config["SSL Certificate"]["SUGGESTION_SSL_TLS_WEB_SERVER_AUTH"]
    SUGGESTION_SSL_TLS_WEB_CLIENT_AUTH = config["SSL Certificate"]["SUGGESTION_SSL_TLS_WEB_CLIENT_AUTH"]

    "Archive History" in config
    ISSUE_ARCHIVE_HISTORY_FIRST_SCAN = config["Archive History"]["ISSUE_ARCHIVE_HISTORY_FIRST_SCAN"]
    ISSUE_ARCHIVE_HISTORY_LAST_SCAN = config["Archive History"]["ISSUE_ARCHIVE_HISTORY_LAST_SCAN"]
    ISSUE_ARCHIVE_HISTORY_TOTAL_SCANS = config["Archive History"]["ISSUE_ARCHIVE_HISTORY_TOTAL_SCANS"]
    ISSUE_ARCHIVE_HISTORY_CHANGE_COUNTS = config["Archive History"]["ISSUE_ARCHIVE_HISTORY_CHANGE_COUNTS"]
    ISSUE_ARCHIVE_HISTORY_AVG_SIZE = config["Archive History"]["ISSUE_ARCHIVE_HISTORY_AVG_SIZE"]
    ISSUE_ARCHIVE_HISTORY_AVG_DAYS = config["Archive History"]["ISSUE_ARCHIVE_HISTORY_AVG_DAYS"]

    SUGGESTION_ARCHIVE_HISTORY_FIRST_SCAN = config["Archive History"]["SUGGESTION_ARCHIVE_HISTORY_FIRST_SCAN"]
    SUGGESTION_ARCHIVE_HISTORY_LAST_SCAN = config["Archive History"]["SUGGESTION_ARCHIVE_HISTORY_LAST_SCAN"]
    SUGGESTION_ARCHIVE_HISTORY_TOTAL_SCANS = config["Archive History"]["SUGGESTION_ARCHIVE_HISTORY_TOTAL_SCANS"]
    SUGGESTION_ARCHIVE_HISTORY_CHANGE_COUNTS = config["Archive History"]["SUGGESTION_ARCHIVE_HISTORY_CHANGE_COUNTS"]
    SUGGESTION_ARCHIVE_HISTORY_AVG_SIZE = config["Archive History"]["SUGGESTION_ARCHIVE_HISTORY_AVG_SIZE"]
    SUGGESTION_ARCHIVE_HISTORY_AVG_DAYS = config["Archive History"]["SUGGESTION_ARCHIVE_HISTORY_AVG_DAYS"]

    "Associated Hosts" in config
    ISSUE_ASSO_HOSTS = config["Associated Hosts"]["ISSUE_ASSO_HOSTS"]
    SUGGESTION__ASSO_HOSTS = config["Associated Hosts"]["SUGGESTION__ASSO_HOSTS"]

    "Carbon Footprint" in config
    ISSUE_CO2_INITIAL_SIZE = config["Carbon Footprint"]["ISSUE_CO2_INITIAL_SIZE"]
    ISSUE_CO2_INITIAL_LOAD = config["Carbon Footprint"]["ISSUE_CO2_INITIAL_LOAD"]
    ISSUE_CO2_ENERGY_USE = config["Carbon Footprint"]["ISSUE_CO2_ENERGY_USE"]
    ISSUE_CO2_EMITTED = config["Carbon Footprint"]["ISSUE_CO2_EMITTED"]

    SUGGESTION_CO2_INITIAL_SIZE = config["Carbon Footprint"]["SUGGESTION_CO2_INITIAL_SIZE"]
    SUGGESTION_CO2_INITIAL_LOAD = config["Carbon Footprint"]["SUGGESTION_CO2_INITIAL_LOAD"]
    SUGGESTION_CO2_ENERGY_USE = config["Carbon Footprint"]["SUGGESTION_CO2_ENERGY_USE"]
    SUGGESTION_CO2_EMITTED = config["Carbon Footprint"]["SUGGESTION_CO2_EMITTED"]

    "Crawl Rules" in config
    ISSUE_CRAWL_RULES = config["Crawl Rules"]["ISSUE_CRAWL_RULES"]
    SUGGESTION__CRAWL_RULES = config["Crawl Rules"]["SUGGESTION__CRAWL_RULES"]

    "DNS Security" in config
    ISSUE_DNS_SECURITY_DNS_TYPE = config["DNS Security"]["ISSUE_DNS_SECURITY_DNS_TYPE"]
    ISSUE_DNS_SECURITY_RD = config["DNS Security"]["ISSUE_DNS_SECURITY_RD"]
    ISSUE_DNS_SECURITY_RA = config["DNS Security"]["ISSUE_DNS_SECURITY_RA"]
    ISSUE_DNS_SECURITY_TC = config["DNS Security"]["ISSUE_DNS_SECURITY_TC"]
    ISSUE_DNS_SECURITY_AD = config["DNS Security"]["ISSUE_DNS_SECURITY_AD"]
    ISSUE_DNS_SECURITY_CD = config["DNS Security"]["ISSUE_DNS_SECURITY_CD"]

    SUGGESTION_DNS_SECURITY_DNS_TYPE = config["DNS Security"]["SUGGESTION_DNS_SECURITY_DNS_TYPE"]
    SUGGESTION_DNS_SECURITY_DNS_FLAG = config["DNS Security"]["SUGGESTION_DNS_SECURITY_DNS_FLAG"]

    "DNS Server" in config
    ISSUE_DNS_SERVER = config["DNS Server"]["ISSUE_DNS_SERVER"]

    SUGGESTION_DNS_SERVER = config["DNS Server"]["SUGGESTION_DNS_SERVER"]

    "Domain Whois" in config
    ISSUE_WHOIS_DOMAIN_AGE = config["Domain Whois"]["ISSUE_WHOIS_DOMAIN_AGE"]
    ISSUE_WHOIS_EXPIRY = config["Domain Whois"]["ISSUE_WHOIS_EXPIRY"]
    ISSUE_WHOIS_UPDATE_FREQUENCY = config["Domain Whois"]["ISSUE_WHOIS_UPDATE_FREQUENCY"]
    ISSUE_WHOIS_REGISTRAR = config["Domain Whois"]["ISSUE_WHOIS_REGISTRAR"]
    ISSUE_WHOIS_REGISTRAR_TRUSTED = config["Domain Whois"]["ISSUE_WHOIS_REGISTRAR_TRUSTED"]
    ISSUE_WHOIS_REGISTRAR_FLAGGED = config["Domain Whois"]["ISSUE_WHOIS_REGISTRAR_FLAGGED"]
    ISSUE_WHOIS_REGISTRAR_NEUTRAL = config["Domain Whois"]["ISSUE_WHOIS_REGISTRAR_NEUTRAL"]

    SUGGESTION_WHOIS_DOMAIN_AGE = config["Domain Whois"]["SUGGESTION_WHOIS_DOMAIN_AGE"]
    SUGGESTION_WHOIS_EXPIRY = config["Domain Whois"]["SUGGESTION_WHOIS_EXPIRY"]
    SUGGESTION_WHOIS_UPDATE_FREQUENCY = config["Domain Whois"]["SUGGESTION_WHOIS_UPDATE_FREQUENCY"]
    SUGGESTION_WHOIS_REGISTRAR = config["Domain Whois"]["SUGGESTION_WHOIS_REGISTRAR"]
    SUGGESTION_WHOIS_REGISTRAR_TRUSTED = config["Domain Whois"]["SUGGESTION_WHOIS_REGISTRAR_TRUSTED"]
    SUGGESTION_WHOIS_REGISTRAR_FLAGGED = config["Domain Whois"]["SUGGESTION_WHOIS_REGISTRAR_FLAGGED"]
    SUGGESTION_WHOIS_REGISTRAR_NEUTRAL = config["Domain Whois"]["SUGGESTION_WHOIS_REGISTRAR_NEUTRAL"]

    "Headers" in config
    ISSUE_HEADERS_SERVER = config["Headers"]["ISSUE_HEADERS_SERVER"]
    ISSUE_HEADERS_CHARSET = config["Headers"]["ISSUE_HEADERS_CHARSET"]
    ISSUE_HEADERS_TRAN_ENCODE = config["Headers"]["ISSUE_HEADERS_TRAN_ENCODE"]
    ISSUE_HEADERS_CONNECTION = config["Headers"]["ISSUE_HEADERS_CONNECTION"]
    ISSUE_HEADERS_X_FRAME = config["Headers"]["ISSUE_HEADERS_X_FRAME"]
    ISSUE_HEADERS_X_CONTENT = config["Headers"]["ISSUE_HEADERS_X_CONTENT"]
    ISSUE_HEADERS_REF_POLICY = config["Headers"]["ISSUE_HEADERS_REF_POLICY"]

    SUGGESTION_HEADERS_SERVER = config["Headers"]["SUGGESTION_HEADERS_SERVER"]
    SUGGESTION_HEADERS_CHARSET = config["Headers"]["SUGGESTION_HEADERS_CHARSET"]
    SUGGESTION_HEADERS_TRAN_ENCODE = config["Headers"]["SUGGESTION_HEADERS_TRAN_ENCODE"]
    SUGGESTION_HEADERS_CONNECTION = config["Headers"]["SUGGESTION_HEADERS_CONNECTION"]
    SUGGESTION_HEADERS_X_FRAME = config["Headers"]["SUGGESTION_HEADERS_X_FRAME"]
    SUGGESTION_HEADERS_X_CONTENT = config["Headers"]["SUGGESTION_HEADERS_X_CONTENT"]
    SUGGESTION_HEADERS_REF_POLICY = config["Headers"]["SUGGESTION_HEADERS_REF_POLICY"]

    "HTTP Security" in config
    ISSUE_HTTP_SEC_CONTENT_SECURITY = config["HTTP Security"]["ISSUE_HTTP_SEC_CONTENT_SECURITY"]
    ISSUE_HTTP_SEC_STRICT_TRANS = config["HTTP Security"]["ISSUE_HTTP_SEC_STRICT_TRANS"]
    ISSUE_HTTP_SEC_X_TYPE = config["HTTP Security"]["ISSUE_HTTP_SEC_X_TYPE"]
    ISSUE_HTTP_SEC_X_OPTIONS = config["HTTP Security"]["ISSUE_HTTP_SEC_X_OPTIONS"]
    ISSUE_HTTP_SEC_X_XSS = config["HTTP Security"]["ISSUE_HTTP_SEC_X_XSS"]

    SUGGESTION_HTTP_SEC_CONTENT_SECURITY = config["HTTP Security"]["SUGGESTION_HTTP_SEC_CONTENT_SECURITY"]
    SUGGESTION_HTTP_SEC_STRICT_TRANS = config["HTTP Security"]["SUGGESTION_HTTP_SEC_STRICT_TRANS"]
    SUGGESTION_HTTP_SEC_X_TYPE = config["HTTP Security"]["SUGGESTION_HTTP_SEC_X_TYPE"]
    SUGGESTION_HTTP_SEC_X_OPTIONS = config["HTTP Security"]["SUGGESTION_HTTP_SEC_X_OPTIONS"]
    SUGGESTION_HTTP_SEC_X_XSS = config["HTTP Security"]["SUGGESTION_HTTP_SEC_X_XSS"]

    "Firewall Detection" in config
    ISSUE_FIREWALL_HAS_WAF = config["Firewall Detection"]["ISSUE_FIREWALL_HAS_WAF"]
    ISSUE_FIREWALL_WAF_NAME = config["Firewall Detection"]["ISSUE_FIREWALL_WAF_NAME"]

    SUGGESTION_FIREWALL_HAS_WAF = config["Firewall Detection"]["SUGGESTION_FIREWALL_HAS_WAF"]
    SUGGESTION_FIREWALL_WAF_NAME =  config["Firewall Detection"]["SUGGESTION_FIREWALL_WAF_NAME"]

    "Global Rank" in config
    ISSUE_GLOBAL_RANK_LOW = config["Global Rank"]["ISSUE_GLOBAL_RANK_LOW"]
    ISSUE_GLOBAL_RANK_MODERATE = config["Global Rank"]["ISSUE_GLOBAL_RANK_MODERATE"]

    SUGGESTION_GLOBAL_RANK_LOW = config["Global Rank"]["SUGGESTION_GLOBAL_RANK_LOW"]
    SUGGESTION_GLOBAL_RANK_MODERATE = config["Global Rank"]["SUGGESTION_GLOBAL_RANK_MODERATE"]

    "Open Ports" in config
    ISSUE_OPEN_PORT_FTP = config["Open Ports"]["ISSUE_OPEN_PORT_FTP"]
    ISSUE_OPEN_PORT_SSH = config["Open Ports"]["ISSUE_OPEN_PORT_SSH"]
    ISSUE_OPEN_PORT_TELNET = config["Open Ports"]["ISSUE_OPEN_PORT_TELNET"]
    ISSUE_OPEN_PORT_SMTP = config["Open Ports"]["ISSUE_OPEN_PORT_SMTP"]
    ISSUE_OPEN_PORT_DNS = config["Open Ports"]["ISSUE_OPEN_PORT_DNS"]
    ISSUE_OPEN_PORT_POP3 = config["Open Ports"]["ISSUE_OPEN_PORT_POP3"]
    ISSUE_OPEN_PORT_IMAP = config["Open Ports"]["ISSUE_OPEN_PORT_IMAP"]
    ISSUE_OPEN_PORT_MYSQL = config["Open Ports"]["ISSUE_OPEN_PORT_MYSQL"]
    ISSUE_OPEN_PORT_RDP = config["Open Ports"]["ISSUE_OPEN_PORT_RDP"]
    ISSUE_OPEN_PORT_UNKNOW = config["Open Ports"]["ISSUE_OPEN_PORT_UNKNOW"]

    SUGGESTION_OPEN_PORT_FTP = config["Open Ports"]["SUGGESTION_OPEN_PORT_FTP"]
    SUGGESTION_OPEN_PORT_SSH = config["Open Ports"]["SUGGESTION_OPEN_PORT_SSH"]
    SUGGESTION_OPEN_PORT_TELNET = config["Open Ports"]["SUGGESTION_OPEN_PORT_TELNET"]
    SUGGESTION_OPEN_PORT_SMTP = config["Open Ports"]["SUGGESTION_OPEN_PORT_SMTP"]
    SUGGESTION_OPEN_PORT_DNS = config["Open Ports"]["SUGGESTION_OPEN_PORT_DNS"]
    SUGGESTION_OPEN_PORT_POP3 = config["Open Ports"]["SUGGESTION_OPEN_PORT_POP3"]
    SUGGESTION_OPEN_PORT_IMAP = config["Open Ports"]["SUGGESTION_OPEN_PORT_IMAP"]
    SUGGESTION_OPEN_PORT_MYSQL = config["Open Ports"]["SUGGESTION_OPEN_PORT_MYSQL"]
    SUGGESTION_OPEN_PORT_RDP = config["Open Ports"]["SUGGESTION_OPEN_PORT_RDP"]
    SUGGESTION_OPEN_PORT_UNKNOW = config["Open Ports"]["SUGGESTION_OPEN_PORT_UNKNOW"]

    "Redirect Chain" in config
    ISSUE_REDIRECT_TOTAL_REDIRECT = config["Redirect Chain"]["ISSUE_REDIRECT_TOTAL_REDIRECT"]
    ISSUE_REDIRECT_HTTP_TO_HTTPS = config["Redirect Chain"]["ISSUE_REDIRECT_HTTP_TO_HTTPS"]
    ISSUE_REDIRECT_HTTP_TO_HTTP = config["Redirect Chain"]["ISSUE_REDIRECT_HTTP_TO_HTTP"]
    ISSUE_REDIRECT_HTTPS_TO_HTTP = config["Redirect Chain"]["ISSUE_REDIRECT_HTTPS_TO_HTTP"]

    SUGGESTION_REDIRECT_TOTAL_REDIRECT = config["Redirect Chain"]["SUGGESTION_REDIRECT_TOTAL_REDIRECT"]
    SUGGESTION_REDIRECT_HTTP_TO_HTTPS = config["Redirect Chain"]["SUGGESTION_REDIRECT_HTTP_TO_HTTPS"]
    SUGGESTION_REDIRECT_HTTP_TO_HTTP = config["Redirect Chain"]["SUGGESTION_REDIRECT_HTTP_TO_HTTP"]
    SUGGESTION_REDIRECT_HTTPS_TO_HTTP = config["Redirect Chain"]["SUGGESTION_REDIRECT_HTTPS_TO_HTTP"]

    "Security.Txt" in config
    ISSUE_SECURITY_TXT_MISSING = config["Security.Txt"]["ISSUE_SECURITY_TXT_MISSING"]
    ISSUE_SECURITY_TXT_LOCATION = config["Security.Txt"]["ISSUE_SECURITY_TXT_LOCATION"]
    ISSUE_SECURITY_TXT_PGP = config["Security.Txt"]["ISSUE_SECURITY_TXT_PGP"]

    SUGGESTION_SECURITY_TXT_MISSING = config["Security.Txt"]["SUGGESTION_SECURITY_TXT_MISSING"]
    SUGGESTION_SECURITY_TXT_LOCATION = config["Security.Txt"]["SUGGESTION_SECURITY_TXT_LOCATION"]
    SUGGESTION_SECURITY_TXT_PGP = config["Security.Txt"]["SUGGESTION_SECURITY_TXT_PGP"]

    "Server Status" in config
    ISSUE_SERVER_STATUS_IS_UP = config["Server Status"]["ISSUE_SERVER_STATUS_IS_UP"]
    ISSUE_SERVER_STATUS_300 = config["Server Status"]["ISSUE_SERVER_STATUS_300"]
    ISSUE_SERVER_STATUS_400 = config["Server Status"]["ISSUE_SERVER_STATUS_400"]
    ISSUE_SERVER_STATUS_500 = config["Server Status"]["ISSUE_SERVER_STATUS_500"]
    ISSUE_SERVER_STATUS_TIME_200 = config["Server Status"]["ISSUE_SERVER_STATUS_TIME_200"]
    ISSUE_SERVER_STATUS_TIME_100 = config["Server Status"]["ISSUE_SERVER_STATUS_TIME_100"]

    SUGGESTION_SERVER_STATUS_IS_UP = config["Server Status"]["SUGGESTION_SERVER_STATUS_IS_UP"]
    SUGGESTION_SERVER_STATUS_300 = config["Server Status"]["SUGGESTION_SERVER_STATUS_300"]
    SUGGESTION_SERVER_STATUS_400 = config["Server Status"]["SUGGESTION_SERVER_STATUS_400"]
    SUGGESTION_SERVER_STATUS_500 = config["Server Status"]["SUGGESTION_SERVER_STATUS_500"]
    SUGGESTION_SERVER_STATUS_TIME_200 = config["Server Status"]["SUGGESTION_SERVER_STATUS_TIME_200"]
    SUGGESTION_SERVER_STATUS_TIME_100 = config["Server Status"]["SUGGESTION_SERVER_STATUS_TIME_100"]