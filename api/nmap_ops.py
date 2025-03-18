import asyncio
import xml.etree.ElementTree as ET
import subprocess
import os
import re
from colorama import Fore, Style
from util.config_uti import Configuration
from util.issue_config import Issue_Config
from util.report_util import Report_Utility

class Nmap_Ops:
    Error_Title = None

    def __init__(self, ip_address, url, domain):
        self.url = url
        self.ip_address = ip_address
        self.domain = domain
        os.makedirs(self.xml_folder, exist_ok=True)  # Ensure folder exists

    nmap_scripts = {
        'general_vulnerabilities': 'http-vuln*',
        'sql_injection': 'http-sql-injection',
        'xss': 'http-stored-xss,http-dombased-xss',
        'shellshock': 'http-shellshock',
        'rce_exploits': 'http-vuln-cve2017-5638',
        'web_server_checks': 'http-enum,http-headers,http-methods',
    }

    target_ip = "192.168.0.178"
    ports_to_scan = "21,22,25,53,80,110,143,443,465,587,993,995,8080,8443"
    xml_folder = "nmap_xml"

    async def Get_Nmap_Ops(self):
        config = Configuration()
        self.Error_Title = config.NMAP_OPERATION
        output = []
        try:
            tasks = [self.__os_detection(self.target_ip), self.__port_scan(self.target_ip)]
            for category, script in self.nmap_scripts.items():
                tasks.append(self.__run_nmap(self.target_ip, category, script))

            await asyncio.gather(*tasks)

            scan_data = {}
            scan_data["os_detection"] = await self.__parse_nmap_xml(f"{self.xml_folder}/nmap_output_os_detection.xml", "os_detection")

            scan_data["port_scan"] = await self.__parse_nmap_xml(f"{self.xml_folder}/nmap_output_port_scan.xml", "port_scan")

            for category in self.nmap_scripts.keys():
                scan_data[category] = await self.__parse_nmap_xml(f"{self.xml_folder}/nmap_output_{category}.xml", category)

            output = await asyncio.gather(*(self.__html_table(category, data) for category, data in scan_data.items()))
            print(f"✅ {config.MODULE_NMAP_OPERATION} has successfully completed.")
            return [table for sublist in output for table in sublist]  # Flatten list
            # return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Nmap_Ops : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, category, scan_data):
        rep_data = []
        html = ""
        table_parts = []

        if not scan_data:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage, html = await self.__nmap_score(scan_data)
            table_parts = [
                '<table>',
                '<tr>',
                f'<td colspan="2"><div class="progress-bar-container">'
                f'<div class="progress" style="width: {percentage}%;">{percentage}%</div></div></td>',
                '</tr>'
            ]

            for data in scan_data:
                if category == "os_detection":
                    table_parts.append(
                        f'<tr><td>OS Details</td><td>{data["os"]}</td></tr>'
                    )
                elif category == "port_scan":
                    table_parts.append(
                        f'<tr><td>{data["port"]}</td><td>{data["service"]}</td></tr>'
                    )
                else:
                    table_parts.append(
                        f'<tr><td colspan="3" style="text-align: left;"><h3>{data["script_id"]}</h3></td></tr>'
                        f'<tr><td colspan="3" style="text-align: left;">{data["output"]}</td></tr>'
                    )

        table_parts.append("</table>")
        table = "".join(table_parts)  # Combine all parts into a single string

        rep_data.append(table.replace("\n", ""))  # Remove all newline characters
        rep_data.append(html.replace("\n", ""))   # Ensure the report does not contain newlines
        return rep_data

    async def __nmap_score(self, scan_data):
        issues = []
        suggestions = []
        score = 0
        max_score = 2
        
        for data in scan_data:
            score = 0  # Reset score for each entry
            
            if 'port' in data and data['port'] not in ["80", "443"]:
                issues.append(f"Non-standard port {data['port']} open")
                suggestions.append("Restrict access or close unnecessary ports")
            else:
                score += 1
            
            if 'output' in data and "vulnerable" in data['output'].lower():
                issues.append(f"Potential vulnerability detected in {data.get('script_id', 'unknown script')}")
                suggestions.append("Apply patches & security updates")
            else:
                score += 1
        
        percentage_score = (score / max_score) * 100
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_NMAP_OPERATION, Configuration.MODULE_NMAP_OPERATION, issues, suggestions, int(percentage_score))
        return int(percentage_score), html_tags

    async def __run_nmap(self, target_ip, script_category, nmap_script):
        output_file = f"{self.xml_folder}/nmap_output_{script_category}.xml"
        command = ["sudo", "nmap", "-sT", "-T2", "-p", self.ports_to_scan, "--script", nmap_script, "-oX", output_file, target_ip]
        print(f"    ⚙️  Running NMAP script : {nmap_script}")
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await process.communicate()

    async def __os_detection(self, target_ip):
        output_file = f"{self.xml_folder}/nmap_output_os_detection.xml"
        command = ["sudo", "nmap", "-O", "-oX", output_file, target_ip]
        print(f"    ⚙️  Running NMAP OS Detection.")
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await process.communicate()

    async def __port_scan(self, target_ip):
        output_file = f"{self.xml_folder}/nmap_output_port_scan.xml"
        command = ["sudo", "nmap", "-p-", "-oX", output_file, target_ip]
        print(f"    ⚙️  Running NMAP Port Scan.")
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await process.communicate()

    async def __parse_nmap_xml(self, xml_file, category):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            scan_data = []
            for host in root.findall('host'):
                # host_ip = host.find('address').get('addr')
                # host_status = host.find('status').get('state')

                if category == "os_detection":
                    os_info = host.find(".//osmatch")
                    os_name = os_info.get('name') if os_info is not None else "Unknown"
                    scan_data.append({'os': os_name})

                elif category == "port_scan":
                    for port in host.findall(".//port"):
                        port_id = port.get('portid')
                        state = port.find(".//state")
                        state = state.get('state')
                        service = port.find(".//service")
                        service_name = service.get('name') if service is not None else "Unknown"
                        scan_data.append({'port': port_id, 'state': state, 'service': service_name})

                else:
                    for script in host.findall(".//script"):
                        script_id = script.get('id')
                        script_output = script.get('output', 'No output')

                        # Remove HTML tags from script output
                        clean_output = re.sub(r'<[^>]+>', '', script_output)
                        scan_data.append({'script_id': script_id, 'output': clean_output})
            return scan_data
        except Exception as e:
            print(f"Error parsing XML {xml_file}: {e}")
            return []
