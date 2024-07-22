from scapy.all import *
from urllib.parse import urlparse
import asyncio
from colorama import Fore, Style
import socket
from util.config_uti import Configuration

class OPEN_PORTS():
    Error_Title = None
    def __init__(self,url):
        self.url=url
    async def Get_Open_Ports(self):
        config = Configuration()
        self.Error_Title = config.PORT_SCANNING
        output=""
        try:
            domain_name = urlparse(self.url).netloc
            ip_address = socket.gethostbyname(domain_name)
            #print(ip_address)
            result= await self.__final_result(ip_address)
            output = await self.__formatting_Output(domain_name,ip_address,result)
            return output

        except Exception as ex:
            error_msg = ex.args[0]
            msg = "[-] " + self.Error_Title + " => Get_Open_Ports : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __final_result(self,ip_address):

        open_ports=[]
        ports = list(range(0, 1024+ 1))
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
        
    async def __formatting_Output(self, domain,ipaddress,res):
        htmlValue = ""        
        htmlValue = await self.__html_table(domain,ipaddress,res)
        return str(htmlValue)
    
    async def __html_table(self,domain,ip,res):
        table = (
            """<table style="border-collapse: collapse; width: 100%; height: 90px;" border="1">
                <tbody>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span class="lbl" style="color: #ffffff;">Domain Name</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(domain)
            + """</span></strong></td>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">IP ADDRESS</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(ip)
            + """</span></strong></td>
                </tr>
                </tr>
                <tr style="height: 18px;">
                <td style="width: 30.5324%; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">OPEN PORTS</span></strong></td>
                <td style="width: 69.4676%; text-align: right; height: 18px; background-color: gray;"><strong><span style="color: #ffffff;">"""
            + str(res)
            + """</span></strong></td>
                </tr>
                </tbody>
                </table>"""
        )
        return table
