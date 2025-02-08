import aiohttp
import asyncio
from util.config_uti import Configuration
from colorama import Fore, Style
from datetime import datetime, timedelta
from statistics import mean

class Archive_History:
    Error_Title = None

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain

    async def Get_Archive_History(self):
        config = Configuration()
        self.Error_Title = config.ARCHIVE_HISTORY
        tasks = []
        decodedResponse = []
        output = ""
        url = ""

        headers = {"Accept": "application/json",}

        try:
            # print("archive_history.py: start ")
            async with aiohttp.ClientSession(headers=headers) as session:
                url = config.ARCHIVE_ENDPOINT_URL.replace("{url}", self.url)

                tasks.append(
                    asyncio.create_task(session.request(method="GET", url=url))
                    )

                responses = await asyncio.gather(*tasks)
                for response in responses:
                    decodedResponse.append(await response.json())

            output = await self.__formatting_Output(decodedResponse)
            # print("archive_history.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Archive_History : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __formatting_Output(self, decodedResponse):
        htmlValue = ""
        htmlValue = await self.__html_table(decodedResponse)
        return str(htmlValue)

    async def __convert_timestamp_to_date(self, timestamp):
        year = int(timestamp[0:4])
        month = int(timestamp[4:6])
        day = int(timestamp[6:8])
        hour = int(timestamp[8:10])
        minute = int(timestamp[10:12])
        second = int(timestamp[12:14])
        return datetime(year, month, day, hour, minute, second)

    async def __count_page_changes(self, results):
        prev_digest = None
        change_count = 0
        for result in results:
            if result[2] != prev_digest:
                change_count += 1
                prev_digest = result[2]
        return change_count

    async def __get_average_page_size(self, scans):
        sizes = [int(scan[3]) for scan in scans]
        return round(mean(sizes))

    async def __get_scan_frequency(self, first_scan, last_scan, total_scans, change_count):
        days_between_scans = (last_scan - first_scan).days / total_scans
        days_between_changes = (last_scan - first_scan).days / change_count
        if (last_scan - first_scan).days > 0:
            scans_per_day = (total_scans - 1) / (last_scan - first_scan).days
            changes_per_day = change_count / (last_scan - first_scan).days
        else:
            scans_per_day = 0
            changes_per_day = 0
        return {
            'Days Between Scans': round(days_between_scans, 2),
            'Days Between Changes': round(days_between_changes, 2),
            'Scans Per Day': round(scans_per_day, 2),
            'Changes Per Day': round(changes_per_day, 2)
        }

    async def __html_table(self, data):
        if data and not any(data):
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
                            <td>No Data Found</td>
                        </tr>
                    </table>"""
            return table
        else:
            data[0].pop(0)
            first_scan = await self.__convert_timestamp_to_date(data[0][0][0])
            last_scan = await self.__convert_timestamp_to_date(data[-1][-1][0])
            total_scans = len(data[0])
            change_count = await self.__count_page_changes(data[0])
            average_page_size = await self.__get_average_page_size(data[0])
            scan_frequency = await self.__get_scan_frequency(first_scan, last_scan, total_scans, change_count)
            
            percentage = await self.__rating(first_scan, last_scan, total_scans, change_count, average_page_size, scan_frequency)

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
                            <td>First Scan</td>
                            <td>""" + first_scan.strftime("%Y-%m-%d %H:%M:%S") + """</td>
                        </tr>
                        <tr>
                            <td>Last Scan</td>
                            <td>""" + last_scan.strftime("%Y-%m-%d %H:%M:%S") + """</td>
                        </tr>
                        <tr>
                            <td>Last Scan</td>
                        <td>""" + str(total_scans) + """</td>
                        </tr>
                        <tr>
                            <td>Last Scan</td>
                            <td>""" + str(change_count) + """</td>
                        </tr>
                        <tr>
                            <td>Last Scan</td>
                        <td>""" + str(average_page_size) + """</td>
                        </tr>
                        <tr>
                            <td>Last Scan</td>
                            <td>""" + str(scan_frequency) + """</td>
                        </tr>
                    </table>"""
            )
            return table            

    async def __rating(self, first_scan, last_scan, total_scans, change_count, average_page_size, scan_frequency):
        
        condition1 = first_scan != ""
        condition2 = last_scan != ""
        condition3 = total_scans != ""
        condition4 = change_count != ""
        condition5 = average_page_size != ""
        condition6 = scan_frequency != ""
        

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4, condition5, condition6])
        
        # Determine the percentage based on the number of satisfied conditions
        if satisfied_conditions == 6:
            percentage = 100
        elif satisfied_conditions == 5:
            percentage = 80
        elif satisfied_conditions == 4:
            percentage = 64
        elif satisfied_conditions == 3:
            percentage = 48
        elif satisfied_conditions == 2:
            percentage = 32
        elif satisfied_conditions == 1:
            percentage = 16
        else:
            percentage = 0  # In case no conditions are satisfied
    
        return percentage

