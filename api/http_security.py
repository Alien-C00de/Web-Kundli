from util.config_uti import Configuration
from colorama import Fore, Style


class HTTP_Security:
    Error_Title = None

    def __init__(self, url, response):
        self.url = url
        self.response = response

    async def Get_HTTP_Security(self):
        config = Configuration()
        self.Error_Title = config.HTTP_SECURITY
        output = ""
        try:
            # print("http_security.py: start ")
            headers = self.response.headers
            output = await self.__formatting_Output(headers)
            # print("http_security.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_HTTP_Security : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, data):
        htmlValue = []
        htmlValue.append(await self.__html_http_Sec_table(data))
        htmlValue.append(await self.__html_headers_table(data))
        return htmlValue

    async def __html_headers_table(self, data):
        server = data.get("Server", None)
        date = data.get("Date", None)
        content_type = data.get("Content-Type", None)
        transfer_encoding = data.get("Transfer-Encoding", None)
        connection = data.get("Connection", None)
        x_frame_option = data.get("X-Frame-Options", None)
        x_content_type_options = data.get("X-Content-Type-Options", None)
        referrer_policy = data.get("Referrer-Policy", None)

        percentage = await self.__rating_header(x_frame_option, x_content_type_options)

        table = (
            f"""<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Server</td>
                        <td>"""+ str(server) + """</td>
                    </tr>
                    <tr>
                        <td>Date</td>
                        <td>""" + str(date) + """</td>
                    </tr>
                    <tr>
                        <td>Content-Type</td>
                        <td>""" + str(content_type) + """</td>
                    </tr>
                    <tr>
                        <td>transfer-encoding</td>
                        <td>""" + str(transfer_encoding) + """</td>
                    </tr>
                    <tr>
                        <td>connection</td>
                        <td>""" + str(connection) + """</td>
                    </tr>
                    <tr>
                        <td>x-frame-options</td>
                        <td>""" + str(x_frame_option) + """</td>
                    </tr>
                    <tr>
                        <td>x-content-type-options</td>
                        <td>""" + str(x_content_type_options) + """</td>
                    </tr>
                    <tr>
                        <td>referrer-policy</td>
                        <td>""" + str(referrer_policy) + """</td>
                    </tr>
                </table>"""
        )
        return table

    async def __html_http_Sec_table(self, data):

        cont_sec = "No" if data.get("Content-Security-Policy", None) is None else "Yes"
        trans_sec = (
            "No" if data.get("Strict-Transport-Security", None) is None else "Yes"
        )
        cont_type = "No" if data.get("X-Content-Type-Options", None) is None else "Yes"
        x_frame = "No" if data.get("X-Frame-Options", None) is None else "Yes"
        x_xss = "No" if data.get("X-XSS-Protection", None) is None else "Yes"
        # "No" if data('Connection', None) is None else "Yes"

        percentage = await self.__rating(cont_sec, trans_sec, cont_type, x_frame, x_xss)

        table = (
            f"""<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Content Security Policy</td>
                        <td>""" + str(cont_sec) + """</td>
                    </tr>
                    <tr>
                        <td>Strict Transport Policy</td>
                        <td>""" + str(trans_sec) + """</td>
                    </tr>
                    <tr>
                        <td>X-Content-Type-Options</td>
                        <td>""" + str(cont_type) + """</td>
                    </tr>
                    <tr>
                        <td>X-Frame-Options</td>
                        <td>""" + str(x_frame) + """</td>
                    </tr>
                    <tr>
                        <td>X-XSS-Protection</td>
                        <td>""" + str(x_xss) + """</td>
                    </tr>
            </table>"""
        )
        return table

    async def __rating(self, cont_sec, trans_sec, cont_type, x_frame, x_xss):

        condition1 = cont_sec != None
        condition2 = trans_sec != None
        condition3 = cont_type != None
        condition4 = x_frame != None
        condition5 = x_xss != None

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
    
    async def __rating_header(self, x_frame_option, x_content_type_options):

        condition1 = False
        condition2 = False

        if x_frame_option == "DENY" or x_frame_option == "SAMEORIGIN":
            condition1 = True
        if x_content_type_options == "nosniff":
            condition2 = True

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2])
        
        # Determine the percentage based on the number of satisfied conditions
        if satisfied_conditions == 2:
            percentage = 100
        elif satisfied_conditions == 1:
            percentage = 50
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage