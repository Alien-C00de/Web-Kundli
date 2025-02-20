from scapy.all import *
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class Open_Ports():
    Error_Title = None

    def __init__(self, url, ip_address, domain):
        self.url = url
        self.ip_address = ip_address
        self.domain = domain
    
    async def Get_Open_Ports(self):
        config = Configuration()
        self.Error_Title = config.PORT_SCANNING
        output=""
        try:
            # print("port_scanning.py: start")
            # ip_address = socket.gethostbyname(self.domain)
            #print(ip_address)
            result= await self.__final_result(self.ip_address)
            output = await self.__html_table(result)

            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Open_Ports : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __final_result(self, ip_address):
        open_ports=[]
        ports = list(range(0, 1024 + 1))
        try: 
            syn_packets = IP(dst=ip_address) / TCP(dport=ports, flags='S')
            responses, unanswered = sr(syn_packets, timeout=0.5, verbose=0)
            for sent, received in responses:
                if received.haslayer(TCP):
                    tcp_layer = received.getlayer(TCP)
                    if tcp_layer.flags == 0x12:  # SYN-ACK
                #print(f"Port {sent[TCP].dport} is open")
                        open_ports.append(sent[TCP].dport)
                # Send RST to close the open connection
                        rst_packet = IP(dst=ip_address) / TCP(dport=sent[TCP].dport, flags='R')
                        send(rst_packet, verbose=0)
            return open_ports
        except Exception as e:
            return []
        
    async def __html_table(self, open_ports):

        if len(open_ports) > 0:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage = 100
            table = (
                """<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width:""" + str(percentage) + """%;">""" + str(percentage) + """%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>Domain Name</td>
                            <td>""" + str(self.domain) + """</td>
                        </tr>
                        <tr>
                            <td>IP ADDRESS</td>
                            <td>""" + str(self.ip_address) + """</td>
                        </tr>
                        </tr>
                        <tr>
                            <td>OPEN PORTS</td>
                            <td>""" + str(open_ports) + """</td>
                        </tr>
                    </table>"""
            )
        return table
