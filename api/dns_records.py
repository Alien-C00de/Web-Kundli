import asyncio
import dns.asyncresolver
from util.config_uti import Configuration
from util.issue_config import Issue_Config
from util.report_util import Report_Utility
from colorama import Fore, Style

class DNS_Records():
    Error_Title = None

    def __init__(self, url, domain):
        self.url=url
        self.domain = domain

    async def Get_DNS_Records(self):
        config = Configuration()
        self.Error_Title = config.ICON_DNS_RECORDS
        output = []
        try:
            result = await self.__final_result(self.domain)
            
            DNS_Records = await self.__html_DNS_table(result[0], result[1], result[2], result[3], result[4])
            TXT_Records = await self.__html_TXT_table(self.domain, result[5])
            output = DNS_Records + TXT_Records
            return output
        except Exception as e:
            error_msg = str(e.args[0])
            msg = f"[-] {self.Error_Title} => Get_DNS_Records : {error_msg}"
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return error_msg

    async def __final_result(self, domain):
        record_types = ["A", "AAAA", "MX", "NS", "CNAME", "TXT"]
        tasks = [self.__get_record(domain, record_type) for record_type in record_types]
        results = await asyncio.gather(*tasks)
        return results

    async def __get_record(self, domain, record_type):
        try:
            resolver = dns.asyncresolver.Resolver()
            resolver.nameservers = ["8.8.8.8", "1.1.1.1"]  # Google & Cloudflare DNS
            resolver.lifetime = 40  # Increase timeout

            answers = await resolver.resolve(domain, record_type)
            return f"{record_type} Records: " + ", ".join([rdata.to_text() for rdata in answers])

        except Exception as ex:
            # print(ex)
            return None

    async def __html_DNS_table(self, A_record, AAAA_record, mx_record, NS_record, CNAME_record):
        rep_data = []
        html = ""

        percentage, html = await self.__dns_records_score(A_record, AAAA_record, mx_record, NS_record, CNAME_record)
        table = (
            """<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>A RECORD</td>
                        <td>""" + str(A_record) + """</td>
                    </tr>
                    <tr>
                        <td>AAAA RECORD</td>
                        <td>""" + str(AAAA_record) + """</td>
                    </tr>
                    <tr>
                        <td>MX RECORD</td>
                        <td>""" + str(mx_record) + """</td>
                    </tr>
                    <tr>
                        <td>NS RECORD</td>
                        <td>""" + str(NS_record) + """</td>
                    </tr>
                    <tr>
                        <td>CNAME RECORD</td>
                        <td>""" + str(CNAME_record) + """</td>
                    </tr>
                </table>"""
        )
        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __html_TXT_table(self, domain, txt_record):
        rep_data = []
        html = ""

        if txt_record == "":
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            percentage, html = await self.__txt_records_score(txt_record)
            table = (
                """<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: """+ str(percentage) +"""%;">"""+ str(percentage) +"""%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>Domain Name</td>
                            <td>""" + str(domain) + """</td>
                        </tr>
                        <tr>
                            <td>TXT RECORD</td>
                            <td>""" + str(txt_record) + """</td>
                        </tr>
                    </table>"""
            )
        rep_data.append(table)
        rep_data.append(html)
        return rep_data

    async def __dns_records_score(self, A_record, AAAA_record, mx_record, NS_record, CNAME_record):
        score = 0
        max_score = 5
        issues = []
        suggestions = []

        if not A_record:  # A Record
            issues.append(Issue_Config.ISSUE_DNS_RECORDS_A)
            suggestions.append(Issue_Config.SUGGESTION_DNS_RECORDS_A)
        else:
            score += 1

        if not AAAA_record:  # AAAA Record
            issues.append(Issue_Config.ISSUE_DNS_RECORDS_AAAA)
            suggestions.append(Issue_Config.SUGGESTION_DNS_RECORDS_AAAA)
        else:
            score += 1

        if not mx_record:  # MX Record
            issues.append(Issue_Config.ISSUE_DNS_RECORDS_MX)
            suggestions.append(Issue_Config.SUGGESTION_DNS_RECORDS_MX)
        else:
            score += 1

        if not NS_record:  # NS Record
            issues.append(Issue_Config.ISSUE_DNS_RECORDS_NS)
            suggestions.append(Issue_Config.SUGGESTION_DNS_RECORDS_NS)
        else:
            score += 1

        if not CNAME_record:  # CNAME Record
            issues.append(Issue_Config.ISSUE_DNS_RECORDS_CNAME)
            suggestions.append(Issue_Config.SUGGESTION_DNS_RECORDS_CNAME)
        else:
            score += 1

        percentage_score = (score / max_score) * 100
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_DNS_RECORDS, Configuration.MODULE_DNS_RECORDS, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags

    async def __txt_records_score(self, txt_record):
        score = 0
        max_score = 1
        issues = []
        suggestions = []

        if not txt_record:  # TXT Record
            issues.append(Issue_Config.ISSUE_DNS_RECORDS_TXT)
            suggestions.append(Issue_Config.SUGGESTION_DNS_RECORDS_TXT)
        else:
            score += 1

        percentage_score = (score / max_score) * 100
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_TXT_RECORDS, Configuration.MODULE_TXT_RECORDS, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags
