import aiohttp
from colorama import Fore, Style
from util.config_uti import Configuration


class Security_TXT:
    Error_Title = None

    def __init__(self, url):
        self.url = url
        self.dict = {}

    SECURITY_TXT_PATHS = [
        "/security.txt",
        "/.well-known/security.txt",]

    async def Get_Security_TXT(self):
        config = Configuration()
        self.Error_Title = config.SECURITY_TXT
        output = ""

        try:
            # print("security_TXT.py: start ")
            for path in self.SECURITY_TXT_PATHS:
                url = f"{self.url}{path}"
                # print("Threats.py: start ")
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            result = await response.text()
                            if result and '<html' in result:
                                self.dict = {"isPresent": False}
                            if result:
                                self.dict = {
                                    "isPresent": True,
                                    "foundIn": path,
                                    "content": result,
                                    "isPgpSigned": await self.__is_pgp_signed(result),
                                    "fields": await self.__parse_result(result),
                                }

            output = await self.__formatting_Output(self.dict)
            # print("security_TXT.py: output: ")
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Security_TXT : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __is_pgp_signed(self, result):
        return '-----BEGIN PGP SIGNED MESSAGE-----' in result

    async def __parse_result(self, result):
        output = {}
        counts = {}
        lines = result.split('\n')
        for line in lines:
            if not line.startswith("#") and not line.startswith("-----") and line.strip() != '':
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    if key in output:
                        counts[key] = counts.get(key, 0) + 1
                        key += str(counts[key])
                    output[key] = value
        return output

    async def __formatting_Output(self, result):
        htmlValue = ""
        htmlValue = await self.__html_table(result)
        return str(htmlValue)

    async def __html_table(self, result):

        percentage = 0

        if result:
            if result["isPresent"]:
                file_location = result["foundIn"]

                percentage = 100
                table = ( f"""<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td> Present </td>
                                <td>{ '✅ Yes' }</td>
                            </tr>
                            <tr>
                                <td> File Location </td>
                                <td>{file_location }</td>
                            </tr>
                            <tr>
                                <td> PGP Signed </td>
                                <td>{'✅ Yes' if result["isPgpSigned"] else '❌ No' }</td>
                            </tr>"""
                            + "".join(
                                        f"""<tr>
                                            <td> {key} </td>
                                            <td> {value}  </td>
                                        </tr>"""
                                        for key, value in result['fields'].items()
                                    )
                            + """</table>"""
                            )
                return table
        else:
            percentage = 0
            table = f"""<table>
                        <tr>
                            <td colspan="1">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>URL is not responding to this query.</td>
                        </tr>
                    </table>"""
            return table

    async def __rating(self, phishing, malware):

        if phishing > 0 or malware > 0:
            percentage = 0
        else:
            percentage = 100

        return percentage
