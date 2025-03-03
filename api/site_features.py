import aiohttp
from colorama import Fore, Style
from util.config_uti import Configuration
from util.report_util import Report_Utility
from util.issue_config import Issue_Config
import datetime


class Site_Features:
    Error_Title = None

    def __init__(self, url, response, domain):
        self.url = url
        self.response = response
        self.domain = domain

    async def Get_Site_Features(self):
        config = Configuration()
        self.Error_Title = config.SITE_FEATURES
        output = []

        try:
            api_url = config.BUILTWITH_ENDPOINT_URL.format(apiKey = config.BUILTWITH_API, url = self.domain)
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if 200 <= response.status <= 299:
                        result = await response.json()  # Convert response to JSON
                    
            output = await self.__html_table(result)
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Site_Features : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output


    async def __html_table(self, data):
        rep_data = []
        html = ""
        if not data:
            report_util = Report_Utility()
            table = await report_util.Empty_Table()
        
        else:
            percentage, html = await self.__site_score(data)
            # Define required categories
            required_categories = {"javascript", "widgets", "payment"}
            rows = []
            
            for group in data.get("groups", []):
                category_name = group["name"].lower()
                if category_name not in required_categories:
                    continue  # Skip categories not in the required list
                
                # Add category header
                rows.append(f'<tr><td><h3>{category_name.capitalize()}</h3></td><td></td></tr>')

                # Add subcategories
                for category in group.get("categories", []):
                    sub_name = category.get("name", "Unknown")
                    live_count = category.get("live", 0)
                    dead_count = category.get("dead", 0)
                    dead_text = f" ({dead_count} dead)" if dead_count > 0 else ""
                    
                    rows.append(f"""
                    <tr>
                        <td>{sub_name}</td>
                        <td>{live_count} Live{dead_text}</td>
                    </tr>""")


            last_scanned = await self.__convet_epoch(data['last']) # Example, replace with actual timestamp if needed

            table = (
                f"""<table>
                    <tr>
                        <td colspan="2">
                            <div class="progress-bar-container">
                                <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                            </div>
                        </td>
                    </tr>
                        {''.join(rows)}
                    <tr>
                        <td colspan="2" style="text-align: left;"><h4>Last scanned on {last_scanned}</h4></td>
                    </tr>
                </table>""")

        rep_data.append(table)
        rep_data.append(html)
        return rep_data


    async def __site_score(self, data):
        """
        Calculate vulnerability score based on fetched JSON data for JavaScript, Widget, and Payment categories.
        """
        max_score = 0  # Total number of evaluated features
        dead_features = 0  # Number of dead features affecting security
        issues = []
        suggestions = []
        
        # Define the categories we want to analyze
        required_categories = {
            "javascript": [
                "jquery-plugin", "ui", "slider", "javascript-library",
                "animation", "compatibility"
            ],
            "widgets": [
                "fonts", "mobile", "captcha", "tag-management", "site-search",
                "bookmarking", "social-sharing", "privacy-compliance",
                "image-provider", "wordpress-plugins"
            ],
            "payment": ["currency"]
        }

        # Mapping feature names to their security concerns and recommendations
        feature_risks = {
            "jquery-plugin": (Issue_Config.ISSUE_SITE_FEATURE_JQUERY, Issue_Config.SUGGESTION_SITE_FEATURE_JQUERY),
            "ui": (Issue_Config.ISSUE_SITE_FEATURE_UI, Issue_Config.SUGGESTION_SITE_FEATURE_UI),
            "slider": (Issue_Config.ISSUE_SITE_FEATURE_SLIDER, Issue_Config.SUGGESTION_SITE_FEATURE_SLIDER),
            "javascript-library": (Issue_Config.ISSUE_SITE_FEATURE_JAVASCRIPT, Issue_Config.SUGGESTION_SITE_FEATURE_JAVASCRIPT),
            "animation": (Issue_Config.ISSUE_SITE_FEATURE_ANIMATION, Issue_Config.SUGGESTION_SITE_FEATURE_ANIMATION),
            "compatibility": (Issue_Config.ISSUE_SITE_FEATURE_COMPATIBILITY, Issue_Config.SUGGESTION_SITE_FEATURE_COMPATIBILITY),
            "fonts": (Issue_Config.ISSUE_SITE_FEATURE_FONTS, Issue_Config.SUGGESTION_SITE_FEATURE_FONTS),
            "mobile": (Issue_Config.ISSUE_SITE_FEATURE_MOBILE, Issue_Config.SUGGESTION_SITE_FEATURE_MOBILE),
            "captcha": (Issue_Config.ISSUE_SITE_FEATURE_CAPTCHA, Issue_Config.SUGGESTION_SITE_FEATURE_CAPTCHA),
            "tag-management": (Issue_Config.ISSUE_SITE_FEATURE_TAG, Issue_Config.SUGGESTION_SITE_FEATURE_TAG),
            "site-search": (Issue_Config.ISSUE_SITE_FEATURE_SITE_SERACH, Issue_Config.SUGGESTION_SITE_FEATURE_SITE_SEARCH),
            "bookmarking": (Issue_Config.ISSUE_SITE_FEATURE_BOOKMARKING, Issue_Config.SUGGESTION_SITE_FEATURE_BOOKMARKING),
            "social-sharing": (Issue_Config.ISSUE_SITE_FEATURE_SOCIAL_SHARING, Issue_Config.SUGGESTION_SITE_FEATURE_SOCIAL_SHARING),
            "privacy-compliance": (Issue_Config.ISSUE_SITE_FEATURE_PRIVACY, Issue_Config.SUGGESTION_SITE_FEATURE_PRIVACY),
            "image-provider": (Issue_Config.ISSUE_SITE_FEATURE_IMAGE_PROVDER, Issue_Config.SUGGESTION_SITE_FEATURE_IMAGE_PROVIDER),
            "wordpress-plugins": (Issue_Config.ISSUE_SITE_FEATURE_WORDPRESS, Issue_Config.SUGGESTION_SITE_FEATURE_WORDPRESS),
            "currency": (Issue_Config.ISSUE_SITE_FEATURE_CURRENCY, Issue_Config.SUGGESTION_SITE_FEATURE_CURRENCY)
        }

        # Iterate through the JSON response to analyze vulnerabilities
        for group in data.get("groups", []):
            category_name = group["name"].lower()
            if category_name in required_categories:
                for category in group.get("categories", []):
                    feature_name = category.get("name", "").lower()
                    
                    # Skip if feature is not in our required list
                    if feature_name not in required_categories[category_name]:
                        continue
                    
                    live_count = category.get("live", 0)
                    dead_count = category.get("dead", 0)
                    max_score += 1  # Count this feature in the total evaluation
                    
                    # If there are dead instances, consider it a security risk
                    if dead_count > 0:
                        dead_features += 1
                        issue, suggestion = feature_risks.get(feature_name, ("Potential security risk due to outdated implementation.", "Update to the latest secure version."))
                        issues.append(f"{feature_name.capitalize()}: {issue}")
                        suggestions.append(f"{feature_name.capitalize()}: {suggestion}")

        # Avoid division by zero
        if max_score == 0:
            percentage_score = 0
        else:
            percentage_score = round((dead_features / max_score) * 100, 2)

        # Generate the HTML report
        report_util = Report_Utility()
        html_tags = await report_util.analysis_table(Configuration.ICON_SITE_FEATURES, Configuration.MODULE_SITE_FEATURES, issues, suggestions, int(percentage_score))

        return int(percentage_score), html_tags


    async def __convet_epoch(self, epoch_time):
        # Epoch time Convert to datetime object
        normal_time = datetime.datetime.fromtimestamp(epoch_time)

        # Format the datetime object into a readable format
        formatted_time = normal_time.strftime("%d %B %Y at %I:%M %p")

        return formatted_time
