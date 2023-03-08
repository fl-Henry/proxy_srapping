# Srapping and testing free proxies
Free proxies was extracted from: 
    
    https://geonode.com/free-proxy-list 


URL for testing gathered proxies is in: 

    test_url = 'https://parsinger.ru/html/index1_page_1.html'

Count of pages for proxy gathering is specified in:  

    proxy_json_list = proxy_json_requests(10, force=True)

10 means 10 pages of proxies; \
force=True means force updating of gathered proxies, else: gathered proxies are saved to a file and read from a file

Request timeout from the testing page is specified in:

    async with session.get(url=url, timeout=2) as response:

Keys for filter is in:

    """
    &anonymityLevel=anonymous
    &protocols=socks5
    &protocols=http
    &speed=fast
    &country=FI  FR  RU 
    """

And placed to the end of URL (instead of "&country=RU"):

    url_after_page = '&sort_by=lastChecked&sort_type=desc&country=RU'