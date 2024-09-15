import ipaddress
from urllib.parse import urlparse

class URL_Verifier():
    
    def __init__(self, url):
        self.url = url

    # Check if the provided website is valid or not
    async def is_url(self):
        result =  urlparse(self.url)
        if result.scheme and result.netloc:
            return True
        else:
            return False
    
    # Check if provided IP is valid IPv4 or not
    async def __is_ipv4_address(self):
        try:
            ipaddress.IPv4Address(self.url)
            return True
        except ipaddress.AddressValueError:
            return False
        
    # Check if provided IP is valid IPv6 or not
    async def __is_ipv6_address(self):
        try:
            ipaddress.IPv6Address(self.url)
            return True
        except ipaddress.AddressValueError:
            return False

    # Check if provided IP is valid IPv4 or IPv6
    async def is_ip_address(self):
        return await self.__is_ipv4_address() or await self.__is_ipv6_address()   