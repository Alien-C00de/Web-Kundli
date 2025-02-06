from colorama import Fore, Style
from util.config_uti import Configuration
from urllib.parse import urlparse
from datetime import datetime, timezone
import datetime

class Cookies():
    Error_Title = None

    def __init__(self, url, response):
        self.url = url
        self.response = response

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
        htmlValue = ""
        htmlValue = await self.__html_cookies_table(cookie_info)

        return htmlValue

    async def __html_cookies_table(self, cookie_info):

        percentage = await self.__rating(cookie_info)

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
        return table_html

    async def __rating(self, cookie_info):

        score = 0
        c_secure = cookie_info[0][5]
        c_expire = cookie_info[0][4]
        c_domain = cookie_info[0][2]
        result = urlparse(self.url)
        hostname = result.netloc
        c_path = cookie_info[0][3]

        # Scoring based on Secure flag
        if c_secure:
            score += 40  # Secure flag contributes 40% to the score

        # Scoring based on Expiry
        if c_expire is not None:
            now = datetime.datetime.now()
            expires = datetime.datetime.strptime(c_expire, "%Y-%m-%d %H:%M:%S")
            delta = expires - now
            if delta.days > 30:
                score += 30  # Long expiry (more than 30 days) contributes 30% to the score
            elif delta.days > 0:
                score += 15  # Medium expiry (less than 30 days) contributes 15% to the score

        # Scoring based on Domain (example criteria)
        if hostname in c_domain:
            score += 20  # Specific domain contributes 20% to the score

        # Additional Scoring based on Path
        if c_path == "/":
            score += 10  # Root path contributes 10% to the score

        return int(score)
