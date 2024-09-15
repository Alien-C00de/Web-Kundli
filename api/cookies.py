from colorama import Fore, Style
from util.config_uti import Configuration
from datetime import datetime, timezone

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

        if not cookie_info:
            return 0
        else:
            condition1 = cookie_info[0][0] != None
            condition2 = cookie_info[0][2] != None
            condition3 = cookie_info[0][3] != None
            condition4 = cookie_info[0][4] != None
            condition5 = cookie_info[0][5] != None

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4, condition5])
        
        # Determine the percentage based on the number of satisfied conditions
        if satisfied_conditions == 5:
            percentage = 100
        elif satisfied_conditions == 4:
            percentage = 80
        elif satisfied_conditions == 3:
            percentage = 60
        elif satisfied_conditions == 2:
            percentage = 40
        elif satisfied_conditions == 1:
            percentage = 20
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage