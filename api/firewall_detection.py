import requests
from util.config_uti import Configuration
from colorama import Fore, Style


class Firewall_Detection():
    Error_Title = None
    
    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Firewall_Detection(self):
        config = Configuration()
        self.Error_Title = config.FIREWALL
        output = ""
        waf_identifiers = {'cloudflare': 'Cloudflare', 'aws lambda': 'AWS WAF', 'akamaighost': 'Akamai',    
                           'sucuri': 'Sucuri', 'barracudawaf': 'Barracuda WAF', 'f5 big-ip': 'F5 BIG-IP',
                            'big-ip': 'F5 BIG-IP', 'fortiweb': 'Fortinet FortiWeb WAF', 'imperva': 'Imperva SecureSphere WAF',
                            'sqreen': 'Sqreen', 'reblaze': 'Reblaze WAF', 'citrix netscaler': 'Citrix NetScaler',
                            'wangzhanbao': 'WangZhanBao WAF', 'webcoment': 'Webcoment Firewall', 'yundun': 'Yundun WAF',
                            'safe3waf': 'Safe3 Web Application Firewall', 'naxsi': 'NAXSI WAF','ibm websphere datapower': 'IBM WebSphere DataPower',
                        }
        try:
            # print("firewall.py: start ")
            response = requests.get(self.url, timeout=10)
            headers = response.headers
            
            header_checks = {
                'server': lambda val: any(keyword in val.lower() for keyword in waf_identifiers.keys()),
                'x-powered-by': lambda val: 'aws lambda' in val.lower(),
                'x-sucuri-id': lambda _: True,
                'x-sucuri-cache': lambda _: True,
                'x-protected-by': lambda val: 'sqreen' in val.lower(),
                'x-waf-event-info': lambda _: True,
                'set-cookie': lambda val: '_citrix_ns_id' in val,
                'x-denied-reason': lambda _: True,
                'x-wzws-requested-method': lambda _: True,
                'x-webcoment': lambda _: True,
                'x-yd-waf-info': lambda _: True,
                'x-yd-info': lambda _: True,
                'x-datapower-transactionid': lambda _: True,
            }
            
            for header, check in header_checks.items():
                if header in headers and check(headers[header]):
                    for key, waf in waf_identifiers.items():
                        if key in headers.get('server', '').lower():
                            decode = {'Firewall': True, 'WAF': waf}
                            output = await self.__html_table(decode)
                            return output
                    decode = {'Firewall': True, 'WAF': waf_identifiers.get(header.lower(), 'Unknown WAF')}
                    output = await self.__html_table(decode)
                    return output
            
            decode = {'hasWaf': False, 'wafName': '*The domain may be protected with a proprietary or custom WAF which we were unable to identify automatically'}
            output = await self.__html_table(decode)
            # print("firewall.py: output: ")
            return output
        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Firewall : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, data):

        percentage = 100
        if not data:
            percentage = 0
            table = f"""
                        <table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                                    </div>
                                </td>
                            </tr>
                        </table>"""
            return table

        rows = [
            f"""
            <tr>
                <td>{key}</td>
                <td>{value}</td>
            </tr>"""
            for key, value in data.items()
        ]

        table = f"""
        <table>
            <tr>
                <td colspan="2">
                    <div class="progress-bar-container">
                        <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                    </div>
                </td>
            </tr>
                {''.join(rows)}
        </table>"""

        return table