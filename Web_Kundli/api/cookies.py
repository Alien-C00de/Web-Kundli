import requests
from colorama import Fore, Style
from util.config_uti import Configuration
from datetime import datetime, timezone

class cookies():
    Error_Title = None

    def __init__(self, url):
        self.url = url

    async def Get_Cookies(self):
        config = Configuration()
        self.Error_Title = config.COOKIES
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for non-200 status codes

            cookies = response.cookies
            cookie_info = {}
            for cookie in cookies:
                cookie_info = []
                for cookie in cookies:
                    cookie_info.append((cookie.name, cookie.value, cookie.domain, cookie.path, cookie.expires, cookie.secure))

            output = await self.__formatting_Output(cookie_info)
            return output
        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + ": " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return msg

    async def __formatting_Output(self, cookie_info):
        htmlValue = ""
        htmlValue = await self.__html_cookies_table(cookie_info)
        return htmlValue

    async def __html_cookies_table(self, cookie_info):
        if not cookie_info:
            return ""

        table_html = """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1"><tbody>"""
        for cookie in cookie_info:
            name  = cookie[0] 
            domain = cookie[2]
            path = cookie[3]
            secure = cookie[5]
            expires = datetime.fromtimestamp(cookie[4], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            table_html += f"""<tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;"> {name} </span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;"></span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Expires</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">{expires}</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Path</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">{path}</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Domain</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">{domain}</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Secure</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">{secure}</span></strong></td>"""
        table_html += """</tbody></table>"""
        return table_html
