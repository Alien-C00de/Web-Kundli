import os
from configparser import ConfigParser


class Issue_Config:

    # Reading Configs
    config = ConfigParser()
    config_path = os.path.join("./config", "issue_list.ini")
    config.read(config_path)

    "Cookies" in config
    ISSUE_SESSION_NAME = config["Cookies"]["ISSUE_SESSION_NAME"]
    ISSUE_SESSION_VALUE = config["Cookies"]["ISSUE_SESSION_VALUE"]
    ISSUE_DOMAIN = config["Cookies"]["ISSUE_DOMAIN"]
    ISSUE_PATH = config["Cookies"]["ISSUE_PATH"]
    ISSUE_COOKIES_EXPIRES = config["Cookies"]["ISSUE_COOKIES_EXPIRES"]
    ISSUE_SECURE = config["Cookies"]["ISSUE_SECURE"]

    SUGGESTION_SESSION_NAME = config["Cookies"]["SUGGESTION_SESSION_NAME"]
    SUGGESTION_SESSION_VALUE = config["Cookies"]["SUGGESTION_SESSION_VALUE"]
    SUGGESTION_DOMAIN = config["Cookies"]["SUGGESTION_DOMAIN"]
    SUGGESTION_PATH = config["Cookies"]["SUGGESTION_PATH"]
    SUGGESTION_EXPIRES = config["Cookies"]["SUGGESTION_EXPIRES"]
    SUGGESTION_SECURE = config["Cookies"]["SUGGESTION_SECURE"]

    "Server Location" in config
    ISSUE_CITY = config["Server Location"]["ISSUE_CITY"]
    ISSUE_COUNTRY = config["Server Location"]["ISSUE_COUNTRY"]
    ISSUE_TIMEZONE = config["Server Location"]["ISSUE_TIMEZONE"]
    ISSUE_LANGUAGES = config["Server Location"]["ISSUE_LANGUAGES"]
    ISSUE_CURRENCY = config["Server Location"]["ISSUE_CURRENCY"]

    SUGGESTION_CITY = config["Server Location"]["SUGGESTION_CITY"]
    SUGGESTION_COUNTRY = config["Server Location"]["SUGGESTION_COUNTRY"]
    SUGGESTION_TIMEZONE = config["Server Location"]["SUGGESTION_TIMEZONE"]
    SUGGESTION_LANGUAGES = config["Server Location"]["SUGGESTION_LANGUAGES"]
    SUGGESTION_CURRENCY = config["Server Location"]["SUGGESTION_CURRENCY"]

    "Server info" in config
    ISSUE_ORGANIZATION = config["Server info"]["ISSUE_ORGANIZATION"]
    ISSUE_ASN = config["Server info"]["ISSUE_ORGANIZATION"]
    ISSUE_IP = config["Server info"]["ISSUE_ORGANIZATION"]
    ISSUE_LOCATION = config["Server info"]["ISSUE_ORGANIZATION"]

    SUGGESTION_ORGANIZATION = config["Server info"]["SUGGESTION_ORGANIZATION"]
    SUGGESTION_ASN = config["Server info"]["SUGGESTION_ASN"]
    SUGGESTION_IP = config["Server info"]["SUGGESTION_IP"]
    SUGGESTION_LOCATION = config["Server info"]["SUGGESTION_LOCATION"]

    "SSL Certificate" in config
    ISSUE_SUBJECT = config["SSL Certificate"]["ISSUE_SUBJECT"]
    ISSUE_ISSUER = config["SSL Certificate"]["ISSUE_ISSUER"]
    ISSUE_EXPIRES = config["SSL Certificate"]["ISSUE_EXPIRES"]
    ISSUE_RENEWED = config["SSL Certificate"]["ISSUE_RENEWED"]
    ISSUE_SERIAL_NUM = config["SSL Certificate"]["ISSUE_SERIAL_NUM"]
    ISSUE_FINGERPRINT = config["SSL Certificate"]["ISSUE_FINGERPRINT"]
    ISSUE_TLS_WEB_SERVER_AUTH = config["SSL Certificate"]["ISSUE_TLS_WEB_SERVER_AUTH"]
    ISSUE_TLS_WEB_CLIENT_AUTH = config["SSL Certificate"]["ISSUE_TLS_WEB_CLIENT_AUTH"]

    SUGGESTION_SUBJECT = config["SSL Certificate"]["SUGGESTION_SUBJECT"]
    SUGGESTION_ISSUER = config["SSL Certificate"]["SUGGESTION_ISSUER"]
    SUGGESTION_EXPIRES = config["SSL Certificate"]["SUGGESTION_EXPIRES"]
    SUGGESTION_RENEWED = config["SSL Certificate"]["SUGGESTION_RENEWED"]
    SUGGESTION_SERIAL_NUM = config["SSL Certificate"]["SUGGESTION_SERIAL_NUM"]
    SUGGESTION_FINGERPRINT = config["SSL Certificate"]["SUGGESTION_FINGERPRINT"]
    SUGGESTION_TLS_WEB_SERVER_AUTH = config["SSL Certificate"]["SUGGESTION_TLS_WEB_SERVER_AUTH"]
    SUGGESTION_TLS_WEB_CLIENT_AUTH = config["SSL Certificate"]["SUGGESTION_TLS_WEB_CLIENT_AUTH"]
