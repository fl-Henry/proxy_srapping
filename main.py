# https://geonode.com/free-proxy-list
# Srapping and testing free proxies

import aiohttp
import asyncio
import aiofiles
from aiohttp_socks import ProxyConnector
import os
import requests
import json


def proxy_json_requests(pages_amount: int, force=False):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.'
                      '4951.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # url = 'https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc'
    """
    &anonymityLevel=anonymous
    &protocols=socks5
    &protocols=http
    &speed=fast
    &country=FI  FR  RU 
    """
    url_before_page = 'https://proxylist.geonode.com/api/proxy-list?limit=100&page='
    url_after_page = '&sort_by=lastChecked&sort_type=desc&country=RU'

    if force:
        print('force=True')

    proxy_json_list = []
    for counter in range(1, pages_amount + 1):
        url = f'{url_before_page}{counter}{url_after_page}'
        json_file_path = f'proxy_page_{counter}.json'

        if not os.path.exists(json_file_path) or force:
            print(f'Proxy list updating: {counter}/{pages_amount}')
            proxy_list_json = requests.get(url=url, headers=headers).json()
            save_json(proxy_list_json, path=json_file_path)
        else:
            proxy_list_json = read_json_file(json_file_path)
        proxy_json_list.append(proxy_list_json)

    return proxy_json_list


def save_json(proxy_json, path: str):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(proxy_json, file, indent=4, ensure_ascii=False)


def read_json_file(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def save_result(data, file_path):
    with open(file_path, 'w'):
        pass

    with open(file_path, 'a', newline='\n') as f:
        for item in data:
            f.write(item + '\n')


def parse_proxy_json(proxy_json_list):
    proxy_list = []
    for proxy_list_json in proxy_json_list:
        data = proxy_list_json['data']
        for proxy_counter in range(len(data)):
            proxy_item = data[proxy_counter]
            # socks5://user:password@127.0.0.1:1080
            port = proxy_item['port']
            ip = proxy_item['ip']
            protocols = proxy_item['protocols'][0]
            if protocols != 'https':
                proxy = f'{protocols}://{ip}:{port}'
                proxy_list.append(proxy)
        # print(len(proxy_list))
    return proxy_list


async def proxy_test_task(url, connector, proxy, good_proxies_path):
    try:
        async with aiohttp.ClientSession(connector=connector, timeout=.5) as session:
            # print(proxy)
            # set timeout  ---------/---------/---------/---------/---------/---------/---------/---------/---------/
            async with session.get(url=url, timeout=2) as response:
                if response.status < 400:
                    print()
                    print(f'good proxy, status_code -{response.status}-', proxy, end='')

                    async with aiofiles.open(good_proxies_path, mode='a') as f:
                        await f.write(proxy)
                else:
                    print('.', end='')

    except Exception as _ex:
        # print(repr(_ex))
        print('x', end='')
        # pass


async def proxy_test(good_proxies_path, test_url, raw_proxies_path):
    url = test_url

    async with aiofiles.open(good_proxies_path, mode='w'):
        pass

    async with aiofiles.open(raw_proxies_path, mode='r') as f:
        tasks = []
        for prx in await f.readlines():
            connector = ProxyConnector.from_url(prx)
            task = proxy_test_task(url, connector, prx, good_proxies_path)
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    # pages_amount and Force updating ----------/----------/----------/----------/----------/----------/----------/
    proxy_json_list = proxy_json_requests(10, force=True)
    proxy_list = parse_proxy_json(proxy_json_list)
    raw_proxies_path = 'raw_proxies.txt'
    save_result(proxy_list, raw_proxies_path)

    # Test URL ----------/----------/----------/----------/----------/----------/----------/----------/----------/
    test_url = 'https://parsinger.ru/html/index1_page_1.html'
    good_proxies_path = 'good_proxies.txt'
    asyncio.run(proxy_test(good_proxies_path, test_url, raw_proxies_path))


if __name__ == '__main__':
    main()
