import socket
import ipaddress
from util.config_uti import Configuration
from util.report_util import Report_Utility
from colorama import Fore, Style

class Block_Detection:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    DNS_SERVERS = [
        {'name': 'AdGuard', 'ip': '176.103.130.130'},
        {'name': 'AdGuard Family', 'ip': '176.103.130.132'},
        {'name': 'CleanBrowsing Adult', 'ip': '185.228.168.10'},
        {'name': 'CleanBrowsing Family', 'ip': '185.228.168.168'},
        {'name': 'CleanBrowsing Security', 'ip': '185.228.168.9'},
        {'name': 'CloudFlare', 'ip': '1.1.1.1'},
        {'name': 'CloudFlare Family', 'ip': '1.1.1.3'},
        {'name': 'Comodo Secure', 'ip': '8.26.56.26'},
        {'name': 'Google DNS', 'ip': '8.8.8.8'},
        {'name': 'Neustar Family', 'ip': '156.154.70.3'},
        {'name': 'Neustar Protection', 'ip': '156.154.70.2'},
        {'name': 'Norton Family', 'ip': '199.85.126.20'},
        {'name': 'OpenDNS', 'ip': '208.67.222.222'},
        {'name': 'OpenDNS Family', 'ip': '208.67.222.123'},
        {'name': 'Quad9', 'ip': '9.9.9.9'},
        {'name': 'Yandex Family', 'ip': '77.88.8.7'},
        {'name': 'Yandex Safe', 'ip': '77.88.8.88'},]

    KNOWN_BLOCK_IPS = [
        '146.112.61.106', '185.228.168.10', '8.26.56.26', '9.9.9.9', '208.69.38.170', '208.69.39.170', '208.67.222.222',
        '208.67.222.123', '199.85.126.10', '199.85.126.20', '156.154.70.22', '77.88.8.7', '77.88.8.8', '::1',
        '2a02:6b8::feed:0ff', '2a02:6b8::feed:bad', '2a02:6b8::feed:a11', '2620:119:35::35', '2620:119:53::53',
        '2606:4700:4700::1111', '2606:4700:4700::1001', '2001:4860:4860::8888', '2a0d:2a00:1::', '2a0d:2a00:2::']

    async def Get_Block_Detection(self):
        config = Configuration()
        self.Error_Title = config.BLOCK_DETECTION
        output = ""
        results = []

        try:
            # print("block_detection.py: start")
            for server in self.DNS_SERVERS:
                is_blocked = await self.__is_domain_blocked(self.domain, server['ip'])
                result_text = f"YES" if is_blocked else f"NO"
                results.append({'server': server['name'], 'isBlocked': result_text})

            output = await self.__html_table(results)
            # print("block_detection.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Block_Detection : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __is_domain_blocked(self, domain: str, server_ip: str) -> bool:
        try:
            addresses = socket.gethostbyname_ex(domain)[-1]
            for addr in addresses:
                if addr in self.KNOWN_BLOCK_IPS:
                    return True
            return False
        except socket.gaierror as e:
            try:
                addresses6 = socket.getaddrinfo(domain, None, socket.AF_INET6)
                for addr_info in addresses6:
                    addr = ipaddress.ip_address(addr_info[4][0])
                    if str(addr) in self.KNOWN_BLOCK_IPS:
                        return True
                return False
            except (socket.gaierror, socket.herror) as e:
                if e.errno in (socket.EAI_NONAME, socket.EAI_NODATA, socket.EAI_FAIL):
                    return True
                return False

    async def __html_table(self, data):
        if data and not any(data):
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage =  await self.__rating(data)
            table = (
            """<table>
                <tr>
                    <td colspan="2">
                        <div class="progress-bar-container">
                            <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                        </div>
                    </td>
                </tr>"""
            + "".join(
                f"""<tr>
                    <td> {block['server']} </td>
                    <td> {'✅  Not Blocked' if block['isBlocked'] == "NO" else '❌ Blocked'}  </td>
                </tr>"""
                for block in data
            )
            + """</table>"""
        )
        return table

    async def __rating(self, data):
        count = 0
        percentage = 0

        for block in data:
            if block['isBlocked'].upper() == "NO":
                count += 1

        ser = len(self.DNS_SERVERS)
        percentage = (100 * count) / ser
    
        return int(percentage)