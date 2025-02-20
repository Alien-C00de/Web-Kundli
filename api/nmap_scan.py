import nmap3
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility

class NMap_Scan:
    Error_Title = None
    nmap = nmap3.Nmap()

    def __init__(self, ip_address, url, domain):
        self.url = url
        self.ip_address = ip_address
        self.domain = domain

    async def Get_Nmap_Scan(self):
        config = Configuration()
        self.Error_Title = config.NMAP_SCAN
        output = []

        try:
            # print("nmap_scan.py: start ")
            version_result = self.nmap.nmap_version_detection(self.domain)
            os_results = self.nmap.nmap_os_detection(self.ip_address)

            # print("nmap_scan.py: output: ")
            output = await self.__html_table(version_result, os_results)
            return list(output)

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Nmap_Scan : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, version_result, os_results):

        nmap_lst = []
        report_util = Report_Utility()
        no_data = await report_util.Empty_Table()

        if os_results is not None:
            os = await self.__os_result_html(os_results)
        else:
            os = no_data

        if version_result is not None:
            version = await self.__version_result_html(version_result)
        else:
            version = no_data

        nmap_lst.append(os)
        nmap_lst.append(version)
        
        return nmap_lst

    async def __os_result_html(self, os_result):

        try:
            # print(os_result)
            ip_address = self.ip_address
            osmatches = os_result.get(ip_address, {}).get('osmatch', [])

            # Check for errors: Ensure 'osmatch' is a list and contains dictionaries with required keys
            if not isinstance(osmatches, list) or not all(isinstance(item, dict) for item in osmatches):
                raise ValueError("Invalid 'osmatch' data format")
            
            if not osmatches:
                return """<table> <tr><td>Error</td><td>No Data Available</td></tr></table>"""

            # Start HTML table
            html = """<table border="1">"""
            html += """<tr>"""
            
            # Define headers
            headers = ['Name', 'Accuracy', 'Line', 'OS Type', 'OS Vendor', 'OS Family', 'OS Gen', 'OS Accuracy']
            
            # Add table headers
            for header in headers:
                html += f"""    <th>{header}</th>"""
            html += """  </tr>"""
            
            # Loop through JSON data and add rows
            for match in osmatches:
                name = match.get('name', '')
                accuracy = match.get('accuracy', '')
                line = match.get('line', '')
                osclass = match.get('osclass', {})
                
                # Ensure osclass is a dictionary and contains required keys
                if not isinstance(osclass, dict):
                    raise ValueError("Invalid 'osclass' data format")
                
                os_type = osclass.get('type', '')
                os_vendor = osclass.get('vendor', '')
                os_family = osclass.get('osfamily', '')
                os_gen = osclass.get('osgen', '')
                os_accuracy = osclass.get('accuracy', '')
                
                html += """  <tr>"""
                html += f"""    <td>{name}</td>"""
                html += f"""    <td>{accuracy}</td>"""
                html += f"""    <td>{line}</td>"""
                html += f"""    <td>{os_type}</td>"""
                html += f"""    <td>{os_vendor}</td>"""
                html += f"""    <td>{os_family}</td>"""
                html += f"""    <td>{os_gen}</td>"""
                html += f"""    <td>{os_accuracy}</td>"""
                html += """  </tr>"""
            
            # End HTML table
            html += """</table>"""
            # print("OS Retul \n\n\n",html, "\n\n\n")
            return html

        except Exception as e:
            # Handle any errors and return an empty table with error message
            return """<table>  <tr><td>Error</td><td>No Data Available</td></tr></table>"""

    async def __version_result_html(self, version_result):
        try:
            ip_address = self.ip_address
            ports = version_result.get(ip_address, {}).get('ports', [])

            # Check for errors: Ensure 'ports' is a list and contains dictionaries with required keys
            if not isinstance(ports, list) or not all(isinstance(item, dict) for item in ports):
                raise ValueError("Invalid 'ports' data format")
            
            if not ports:
                return """<table > <tr><tdError</td><td>No Data Available</td></tr> </table>"""

            # Start HTML table
            html = '<table border="1">'
            html += '  <tr>'
            
            # Define headers
            headers = ['Protocol', 'Port ID', 'State', 'Reason', 'Reason TTL', 'Service Name', 'Service Product', 'Service Version', 'Service Extra Info', 'Service OS Type', 'Service Method', 'Service Conf']
            
            # Add table headers
            for header in headers:
                html += f"""    <th>{header}</th>"""
            html += """  </tr>"""
            
            # Loop through JSON data and add rows
            for port in ports:
                protocol = port.get('protocol', '')
                portid = port.get('portid', '')
                state = port.get('state', '')
                reason = port.get('reason', '')
                reason_ttl = port.get('reason_ttl', '')
                service = port.get('service', {})
                
                # Ensure service is a dictionary and contains required keys
                if not isinstance(service, dict):
                    raise ValueError("Invalid 'service' data format")
                
                service_name = service.get('name', '')
                service_product = service.get('product', '')
                service_version = service.get('version', '')
                service_extrainfo = service.get('extrainfo', '')
                service_ostype = service.get('ostype', '')
                service_method = service.get('method', '')
                service_conf = service.get('conf', '')
                
                html += """  <tr>"""
                html += f"""    <td>{protocol}</td>"""
                html += f"""    <td>{portid}</td>"""
                html += f"""    <td>{state}</td>"""
                html += f"""    <td>{reason}</td>"""
                html += f"""    <td>{reason_ttl}</td>"""
                html += f"""    <td>{service_name}</td>"""
                html += f"""    <td>{service_product}</td>"""
                html += f"""    <td>{service_version}</td>"""
                html += f"""    <td>{service_extrainfo}</td>"""
                html += f"""    <td>{service_ostype}</td>"""
                html += f"""    <td>{service_method}</td>"""
                html += f"""    <td>{service_conf}</td>"""
                html += """  </tr>"""
            
            # End HTML table
            html += """</table>"""
            # print(" Version \n\n\n", html, "\n\n\n")
            return html

        except Exception as e:
            # Handle any errors and return an empty table with error message
            return """<table> <tr><td>Error</td><td>No Data Available</td></tr></table>"""