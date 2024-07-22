import aiohttp
import asyncio
from ipwhois import IPWhois
from util.config_uti import Configuration
from colorama import Fore, Style


class http_security:
    Error_Title = None

    def __init__(self, url):
        self.url = url

    async def Get_HTTP_Headers(self):
        config = Configuration()
        self.Error_Title = config.HTTP_SECURITY
        output = ""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    headers = response.headers
            output = await self.__formatting_Output(headers)
            return output

        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_HTTP_Headers : " + error_msg
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

        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Server</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(server)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Date</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(date)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Content-Type</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(content_type)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">transfer-encoding</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(transfer_encoding)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">connection</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(connection)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">x-frame-options</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x_frame_option)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">x-content-type-options</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x_content_type_options)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">referrer-policy</span></strong></td>
                <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(referrer_policy)
            + """</span></strong></td>
                </tr>
                </tbody>
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

        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                    <tbody>
                    <tr style="height: 18px;">
                    <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Content Security Policy</span></strong></td>
                    <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(cont_sec)
            + """</span></strong></td>
                    </tr>
                    <tr style="height: 18px;">
                    <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">Strict Transport Policy</span></strong></td>
                    <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(trans_sec)
            + """</span></strong></td>
                    </tr>
                    <tr style="height: 18px;">
                    <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">X-Content-Type-Options</span></strong></td>
                    <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(cont_type)
            + """</span></strong></td>
                    </tr>
                    <tr style="height: 18px;">
                    <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">X-Frame-Options</span></strong></td>
                    <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x_frame)
            + """</span></strong></td>
                    </tr>
                    <tr style="height: 18px;">
                    <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">X-XSS-Protection</span></strong></td>
                    <td style="width: 69.4676%; height: 18px; text-align: right; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(x_xss)
            + """</span></strong></td>
                    </tr>
                    </tbody>
                    </table>"""
        )
        return table
