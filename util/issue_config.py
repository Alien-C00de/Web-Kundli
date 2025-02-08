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
    ISSUE_EXPIRES = config["Cookies"]["ISSUE_EXPIRES"]
    ISSUE_SECURE = config["Cookies"]["ISSUE_SECURE"]

    SUGGESTION_SESSION_NAME = config["Cookies"]["SUGGESTION_SESSION_NAME"]
    SUGGESTION_SESSION_VALUE = config["Cookies"]["SUGGESTION_SESSION_VALUE"]
    SUGGESTION_DOMAIN = config["Cookies"]["SUGGESTION_DOMAIN"]
    SUGGESTION_PATH = config["Cookies"]["SUGGESTION_PATH"]
    SUGGESTION_EXPIRES = config["Cookies"]["SUGGESTION_EXPIRES"]
    SUGGESTION_SECURE = config["Cookies"]["SUGGESTION_SECURE"]
