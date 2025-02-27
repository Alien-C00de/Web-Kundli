import dns.resolver
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config

class Mail_Records():
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Mail_Records(self):
        config = Configuration()
        self.Error_Title = config.MAIL_CONFIGURATION
        output=""
        try:
            # print("mail_configration_fetch.py: start")
            result = await self.__final_result(self.domain)
            output = await self.__html_table(result)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Mail_Records : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    # THIS IS FINAL RESULT FUNCTION TO GET RESULT OF ALL FUNCTIONS
    async def __final_result(self, domain):
        mx_records = dns.resolver.resolve(domain, "MX")
        # Get TXT records
        txt_records = dns.resolver.resolve(domain, "TXT")
        # Filter for only email related TXT records (SPF, DKIM, DMARC, and certain provider verifications)
        email_txt_records = [
            record.to_text().strip('"')
            for record in txt_records
            if record.to_text().startswith("v=spf1")
            or record.to_text().startswith("v=DKIM1")
            or record.to_text().startswith("v=DMARC1")
            or record.to_text().startswith("protonmail-verification=")
            or record.to_text().startswith("google-site-verification=")
            or record.to_text().startswith("MS=")
            or record.to_text().startswith("zoho-verification=")
            or record.to_text().startswith("titan-verification=")
            or "bluehost.com" in record.to_text()
        ]

        # Identify specific mail services
        mail_services = []
        for record in email_txt_records:
            if record.startswith("protonmail-verification="):
                mail_services.append(
                    {"provider": "ProtonMail", "value": record.split("=")[1]}
                )
            elif record.startswith("google-site-verification="):
                mail_services.append(
                    {"provider": "Google Workspace", "value": record.split("=")[1]}
                )
            elif record.startswith("MS="):
                mail_services.append(
                    {"provider": "Microsoft 365", "value": record.split("=")[1]}
                )
            elif record.startswith("zoho-verification="):
                mail_services.append(
                    {"provider": "Zoho", "value": record.split("=")[1]}
                )
            elif record.startswith("titan-verification="):
                mail_services.append(
                    {"provider": "Titan", "value": record.split("=")[1]}
                )
            elif "bluehost.com" in record:
                mail_services.append({"provider": "BlueHost", "value": record})

        # Check MX records for Yahoo
        yahoo_mx = [
            record
            for record in mx_records
            if "yahoodns.net" in record.exchange.to_text()
        ]
        if yahoo_mx:
            mail_services.append(
                {"provider": "Yahoo", "value": yahoo_mx[0].exchange.to_text()}
            )

        # Check MX records for Mimecast
        mimecast_mx = [
            record
            for record in mx_records
            if "mimecast.com" in record.exchange.to_text()
        ]
        if mimecast_mx:
            mail_services.append(
                {"provider": "Mimecast", "value": mimecast_mx[0].exchange.to_text()}
            )

        return {
            "mxRecords": [record.to_text() for record in mx_records],
            "txtRecords": email_txt_records,
            "mailServices": mail_services,
        }

    async def __html_table(self, records):
        html = ""
        if not records:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        else:
            # percentage = await self.__rating(str(self.domain), str(result[0]), str(result[1]))
            percentage = 70
            table = """<table>
                            <tr>
                                <td colspan="2">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width:{0}%;">{0}%</div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <h3>Mail Security Checklist</h3>
                                </td>
                            </tr>
                            <tr>
                                <td>SPF:</td>
                                <td>{1}</td>
                            </tr>
                            <tr>
                                <td>DKIM:</td>
                                <td>{2}</td>
                            </tr>
                            <tr>
                                <td>DMARC:</td>
                                <td>{3}</td>
                            </tr>
                            <tr>
                                <td>BIMI:</td>
                                <td>{4}</td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <h3>MX Records</h3>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <ul>
                                        {5}
                                    </ul>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <h3>External Mail Services</h3>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <ul>
                                        {6}
                                    </ul>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <h3>Mail-related TXT Records</h3>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <ul>
                                        {7}
                                    </ul>
                                </td>
                            </tr>
                        </table>
            """.format(
                percentage,
                (
                    "Enabled"
                    if any("v=spf1" in record for record in records["txtRecords"])
                    else "Not Enabled"
                ),
                (
                    "Enabled"
                    if any("v=DKIM1" in record for record in records["txtRecords"])
                    else "Not Enabled"
                ),
                (
                    "Enabled"
                    if any("v=DMARC1" in record for record in records["txtRecords"])
                    else "Not Enabled"
                ),
                "Not Enabled",  # Assume BIMI is not enabled for this example
                "".join(
                    f"<li>{mx.split()[1]} Priority: {mx.split()[0]}</li>"
                    for mx in records["mxRecords"]
                ),
                "".join(
                    f"<li>{service['provider']}: {service['value']}</li>"
                    for service in records["mailServices"]
                ),
                "".join(f"<li>{record}</li>" for record in records["txtRecords"]),
            )

        return table

    async def __rating(self, domain, mail_record, ext_mail_record):

        condition1 = domain != None
        condition2 = mail_record != None
        condition3 = ext_mail_record != None

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3])

        # Determine the percentage based on the number of satisfied conditions
        if satisfied_conditions == 3:
            percentage = 100
        elif satisfied_conditions == 2:
            percentage = 66
        elif satisfied_conditions == 1:
            percentage = 33
        else:
            percentage = 0  # In case no conditions are satisfied

        return percentage
