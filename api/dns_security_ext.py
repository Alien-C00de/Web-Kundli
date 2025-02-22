import aiohttp
import asyncio
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class DNS_Security_Ext:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_DNS_Security_Ext(self):
        config = Configuration()
        self.Error_Title = config.DNS_SECURITY_EXT
        output = ""

        try:
            # print("dns_security.py: start ")
            dns_types = ['DNSKEY', 'DS', 'RRSIG']
            records = {}

            async with aiohttp.ClientSession() as session:
                tasks = [self.__fetch_dns_record(session, self.url, dns_type, config.DNS_SECURITY_API) for dns_type in dns_types]
                results = await asyncio.gather(*tasks)

            for dns_type, result in zip(dns_types, results):
                records[dns_type] = result

            output = await self.__html_table(records)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_DNS_Security_Ext : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output


    async def __fetch_dns_record(self, session, domain, dns_type, url):
        new_url = url.replace("{domain}", domain).replace("{dns_type}", dns_type)
        headers = {'Accept': 'application/dns-json'}

        try:
            async with session.get(new_url, headers=headers) as response:
                response.raise_for_status()
                dns_response = await response.json()

                return {
                        'isFound': bool(dns_response.get('Answer')),
                        'answer': dns_response.get('Answer', []),
                        'flags': dns_response.get('AD'),
                        }
        except Exception as error:
            raise Exception(f"Error fetching {dns_type} record: {error}")


    async def __html_table(self, data):
        percentage = 100
        if not data:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            dns_flags = [
                ('Recursion Desired (RD)', True),
                ('Recursion Available (RA)', True),
                ('TrunCation (TC)', False),
                ('Authentic Data (AD)', lambda record: ' ✅' if record['flags'] else ' ❌'),
                ('Checking Disabled (CD)', False)
            ]

            rows = [
                f"""
                <tr>
                    <td><h3>{dns_type}</h3></td> <td></td>
                </tr>
                <tr>
                    <td>{dns_type} - Present?</td>
                    <td>{'✅ Yes' if record['isFound'] else '❌ No'}</td>
                </tr>
                {''.join([f"""
                <tr>
                <td style="padding-left: 20px;">{description}</td>
                <td>{status(record) if callable(status) else ('✅' if status else '❌')}</td>
                </tr>""" for description, status in dns_flags])}
                """ for dns_type, record in data.items()
            ]

            table = f"""
            <table>
                <tr>
                    <td colspan="2">
                        <div class="progress-bar-container">
                            <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                        </div>
                    </td>
                </tr>
                {''.join(rows)}
            </table>"""

        return table

