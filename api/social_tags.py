from bs4 import BeautifulSoup
from colorama import Fore, Style
from util.config_uti import Configuration

class Social_Tags:
    Error_Title = None

    def __init__(self, url, response, domain):
        self.url = url
        self.response = response
        self.domain = domain

    async def Get_Social_Tags(self):
        config = Configuration()
        self.Error_Title = config.SOCIAL_TAGS
        output = ""

        try:
            # print("social_tag.py: start ")
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(self.url) as response:
            if self.response.status_code == 200:
                html = self.response.text
                soup = BeautifulSoup(html, 'html.parser')

            metadata = {
                # Basic meta tags
                'title': soup.find('title').get_text() if soup.find('title') else None,
                'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None,
                'keywords': soup.find('meta', attrs={'name': 'keywords'})['content'] if soup.find('meta', attrs={'name': 'keywords'}) else None,
                'canonicalUrl': soup.find('link', attrs={'rel': 'canonical'})['href'] if soup.find('link', attrs={'rel': 'canonical'}) else None,

                # OpenGraph Protocol
                'ogTitle': soup.find('meta', attrs={'property': 'og:title'})['content'] if soup.find('meta', attrs={'property': 'og:title'}) else None,
                'ogType': soup.find('meta', attrs={'property': 'og:type'})['content'] if soup.find('meta', attrs={'property': 'og:type'}) else None,
                'ogImage': soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else None,
                'ogUrl': soup.find('meta', attrs={'property': 'og:url'})['content'] if soup.find('meta', attrs={'property': 'og:url'}) else None,
                'ogDescription': soup.find('meta', attrs={'property': 'og:description'})['content'] if soup.find('meta', attrs={'property': 'og:description'}) else None,
                'ogSiteName': soup.find('meta', attrs={'property': 'og:site_name'})['content'] if soup.find('meta', attrs={'property': 'og:site_name'}) else None,

                # Twitter Cards
                'twitterCard': soup.find('meta', attrs={'name': 'twitter:card'})['content'] if soup.find('meta', attrs={'name': 'twitter:card'}) else None,
                'twitterSite': soup.find('meta', attrs={'name': 'twitter:site'})['content'] if soup.find('meta', attrs={'name': 'twitter:site'}) else None,
                'twitterCreator': soup.find('meta', attrs={'name': 'twitter:creator'})['content'] if soup.find('meta', attrs={'name': 'twitter:creator'}) else None,
                'twitterTitle': soup.find('meta', attrs={'name': 'twitter:title'})['content'] if soup.find('meta', attrs={'name': 'twitter:title'}) else None,
                'twitterDescription': soup.find('meta', attrs={'name': 'twitter:description'})['content'] if soup.find('meta', attrs={'name': 'twitter:description'}) else None,
                'twitterImage': soup.find('meta', attrs={'name': 'twitter:image'})['content'] if soup.find('meta', attrs={'name': 'twitter:image'}) else None,

                # Misc
                'themeColor': soup.find('meta', attrs={'name': 'theme-color'})['content'] if soup.find('meta', attrs={'name': 'theme-color'}) else None,
                'robots': soup.find('meta', attrs={'name': 'robots'})['content'] if soup.find('meta', attrs={'name': 'robots'}) else None,
                'googlebot': soup.find('meta', attrs={'name': 'googlebot'})['content'] if soup.find('meta', attrs={'name': 'googlebot'}) else None,
                'generator': soup.find('meta', attrs={'name': 'generator'})['content'] if soup.find('meta', attrs={'name': 'generator'}) else None,
                'viewport': soup.find('meta', attrs={'name': 'viewport'})['content'] if soup.find('meta', attrs={'name': 'viewport'}) else None,
                'author': soup.find('meta', attrs={'name': 'author'})['content'] if soup.find('meta', attrs={'name': 'author'}) else None,
                'publisher': soup.find('link', attrs={'rel': 'publisher'})['href'] if soup.find('link', attrs={'rel': 'publisher'}) else None,
                'favicon': soup.find('link', attrs={'rel': 'icon'})['href'] if soup.find('link', attrs={'rel': 'icon'}) else None
            }

            output = await self.__html_table(metadata)
            # print("social_tag.py: output: ")
            return output

        except Exception as ex:
            error_msg = str(ex.args[0])
            msg = "[-] " + self.Error_Title + " => Get_Social_Tags : " + error_msg
            print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
            return output

    async def __html_table(self, metadata):
        if not metadata:
            percentage = 0
            table = f"""
                        <table>
                            <tr>
                                <td colspan="1">
                                    <div class="progress-bar-container">
                                        <div class="progress" style="width: {str(percentage) }%;">{str(percentage)}%</div>
                                    </div>
                                </td>
                            </tr>
                        </table>"""
        else:
            title = str(metadata.get ('title', 'N/A'))
            description = str(metadata.get('description', 'N/A'))
            keywords = str(metadata.get('keywords', 'N/A'))
            cononical = str(metadata.get('canonicalUrl', 'N/A'))
            twitter  =str(metadata.get('twitterSite', 'N/A'))
            theme_color = metadata.get('themeColor', 'N/A')

            percentage = await self.__rating(title, description, keywords, cononical, theme_color, twitter)

            table = (
                f"""<table>
                        <tr>
                            <td colspan="2">
                                <div class="progress-bar-container">
                                    <div class="progress" style="width: {str(percentage)}%;">{str(percentage)}%</div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>Title</td>
                            <td>{title}</td>
                        </tr>
                        <tr>
                            <td>Description</td>
                            <td>{description}</td>
                        </tr>
                        <tr>
                            <td>Keywords</td>
                            <td>{keywords}</td>
                        </tr>
                        <tr>
                            <td>Canonical URL</td>
                            <td>{cononical}</td>
                        </tr>
                        <tr>
                            <td>Theme Color</td>
                            <td>{theme_color}</td>
                        </tr>
                        <tr>
                            <td>Twitter Site    </td>
                            <td>{twitter}</td>
                        </tr>
                    </table>"""
            )
        return table

    async def __rating(self, title, description, keywords, cononical, theme_color, twitter):

        condition1 = title != ""
        condition2 = description != ""
        condition3 = keywords != ""
        condition4 = cononical != ""
        condition5 = theme_color != ""
        condition6 = twitter != ""

        # Count the number of satisfied conditions
        satisfied_conditions = sum([condition1, condition2, condition3, condition4])
        
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