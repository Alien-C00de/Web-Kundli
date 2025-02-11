from colorama import Fore, Style
from util.config_uti import Configuration
from util.issue_config import Issue_Config
from util.report_util import Report_Utility
from datetime import datetime, timezone
import datetime
import re

class Cookies():
    Error_Title = None

    def __init__(self, url, response, domain):
        self.url = url
        self.response = response
        self.domain = domain

    async def Get_Cookies(self):
        config = Configuration()
        self.Error_Title = config.COOKIES
        try:
            # print("cookies.py: start ")
            self.response.raise_for_status()  # Raise an error for non-200 status codes

            cookies = self.response.cookies
            cookie_info = {}
            for cookie in cookies:
                cookie_info = []
                for cookie in cookies:
                    cookie_info.append((cookie.name, cookie.value, cookie.domain, cookie.path, cookie.expires, cookie.secure))

            output = await self.__formatting_Output(cookie_info)
            # print("cookies.py: output: ")
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + "=> Get_Cookies : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return msg

    async def __formatting_Output(self, cookie_info):
        htmlValue = []
        htmlValue = await self.__html_cookies_table(cookie_info)

        return htmlValue

    async def __html_cookies_table(self, cookie_info):

        rep_data = []
        # percentage = await self.__rating(cookie_info)
        percentage, html = await self.__evaluate_cookie_security(cookie_info)

        if not cookie_info:
            table_html = f"""<table>
                            <tr>
                                <td colspan="1">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>No Cookies Details Found</td>
                            </tr>
                    </table>"""
            return table_html

        for cookie in cookie_info:
            name  = cookie[0] 
            value = cookie[1]
            domain = cookie[2]
            path = cookie[3]
            secure = cookie[5]
            if cookie[4]:
                expires = datetime.fromtimestamp(cookie[4], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            else:
                expires = ""

            table_html = f"""<table>
                                <tr>
                                    <td colspan="2">
                                        <div class="progress-bar-container">
                                            <div class="progress" style="width: {percentage} %;">{percentage}%</div>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Name</td>
                                    <td>{name}</td>
                                </tr>
                                <tr>
                                    <td>Session ID</td>
                                    <td>{value}</td>
                                </tr>
                                <tr>
                                    <td>Expires </td>
                                    <td>{expires}</td>
                                </tr>
                                <tr>
                                    <td>Path</td>
                                    <td>{path}</td>
                                </tr>
                                <tr>
                                    <td>Domain</td>
                                    <td>{domain}</td>
                                </tr>
                                <tr>
                                    <td>Secure</td>
                                    <td>{secure}</td>
                                </tr>
                            </table>"""
        rep_data.append(table_html)
        rep_data.append(html)
        return rep_data

    async def __evaluate_cookie_security(self, cookie):
        issue_config = Issue_Config()
        score = 0
        max_score = 6  # 6 parameters to evaluate
        session_name  = cookie[0][0] 
        session_value = cookie[0][1]
        domain = cookie[0][2]
        path = cookie[0][3]
        expires = cookie[0][4]
        secure = cookie[0][5]

        issues = []
        suggestions = []

        # return score, percentage_score, issues, suggestions
        # Session Name - Should not be empty or generic
        if not session_name or session_name == 'session':
            issues.append(issue_config.ISSUE_SESSION_NAME)
            suggestions.append(issue_config.SUGGESTION_SESSION_NAME)
        else:
            score += 1

        # Session ID - Should not be simple (For simplicity, we will use regex)
        if not session_value or re.match(r'^[a-zA-Z0-9]{8,}$', session_value) is None:
            issues.append(issue_config.ISSUE_SESSION_VALUE)
            suggestions.append(issue_config.SUGGESTION_SESSION_VALUE)
        else:
            score += 1

        # Expires - Should not be far-off date or missing
        if not expires or datetime.strptime(expires, "%a, %d-%b-%Y %H:%M:%S GMT") < datetime.now():
            issues.append(issue_config.ISSUE_COOKIES_EXPIRES)
            suggestions.append(issue_config.SUGGESTION_EXPIRES)
        else:
            score += 1

        # Path - Should not be overly broad (must be specific like `/app` or `/secure`)
        if path == '/' or not path:
            issues.append(issue_config.ISSUE_PATH)
            suggestions.append(issue_config.SUGGESTION_PATH)
        else:
            score += 1

        # Domain - Should be a specific domain, not localhost or too general
        if not domain or domain in ['localhost', '127.0.0.1', '']:
            issues.append(issue_config.ISSUE_DOMAIN)
            suggestions.append(issue_config.SUGGESTION_DOMAIN)
        else:
            score += 1

        # Secure - Should be True
        if secure != True:
            issues.append(issue_config.ISSUE_SECURE)
            suggestions.append(issue_config.SUGGESTION_SECURE)
        else:
            score += 1

        percentage_score = (score / max_score) * 100
        # html_tags = await self.__analysis_table(issues, suggestions, int(percentage_score))
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags

    # async def __analysis_table(self, issues, suggestions, percentage):
    #     html = ""
    #     if issues:
    #         html_template = """<div class="module" id="cookies">
    #                             <h2>""" + Configuration.MODULE_COOKIES + """&nbsp; Score = """ + str(percentage) + """%</h2>
    #                             <div style="display: inline; font-weight: bold;">Summary :</div>
    #                             <span style="display: inline;">The cookies used on the website meet most security standards. However, there are a couple of issues that need to be addressed.</span>
    #                             <div class="issues">
    #                                 <h4>Identified Issues:</h4>
    #                                 <ul>
    #                                     {issue_items}
    #                                 </ul>
    #                             </div>
    #                             <div class="suggestions">
    #                                 <h4>Suggestions for Improvement:</h4>
    #                                 <ul>
    #                                     {suggestion_items}
    #                                 </ul>
    #                             </div> 
    #                     </div>"""

    #         # Generate the list items for issues and suggestions
    #         issue_items = ''.join([f"<li>{issue}</li>" for issue in issues])
    #         suggestion_items = ''.join([f"<li>{suggestion}</li>" for suggestion in suggestions])

    #         # Insert the list items into the HTML template
    #         html = html_template.format(issue_items=issue_items, suggestion_items=suggestion_items)
    #     return html

    # async def __rating(self, cookie_info):

    #     score = 0
    #     c_secure = cookie_info[0][5]
    #     c_expire = cookie_info[0][4]
    #     c_domain = cookie_info[0][2]
    #     c_path = cookie_info[0][3]

    #     # Scoring based on Secure flag
    #     if c_secure:
    #         score += 40  # Secure flag contributes 40% to the score

    #     # Scoring based on Expiry
    #     if c_expire is not None:
    #         now = datetime.datetime.now()
    #         expires = datetime.datetime.strptime(c_expire, "%Y-%m-%d %H:%M:%S")
    #         delta = expires - now
    #         if delta.days > 30:
    #             score += 30  # Long expiry (more than 30 days) contributes 30% to the score
    #         elif delta.days > 0:
    #             score += 15  # Medium expiry (less than 30 days) contributes 15% to the score

    #     # Scoring based on Domain (example criteria)
    #     if self.domain in c_domain:
    #         score += 20  # Specific domain contributes 20% to the score

    #     # Additional Scoring based on Path
    #     if c_path == "/":
    #         score += 10  # Root path contributes 10% to the score

    #     return int(score)
