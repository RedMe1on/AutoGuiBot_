import json
from bs4 import BeautifulSoup
import requests
from typing import List

# proxies_1 = {
#     'http': 'http://157.230.103.189:45153',
#     'https': 'https://198.20.116.74:8080',
# }
# proxies_2 = {
#     'http': 'http://172.67.181.177:80',
#     'https': 'https://117.197.117.255:8080',
# }


def _parse_size(soup: BeautifulSoup) -> List[str]:
    data = json.loads(soup.find('script', type="application/json").string)
    product_sizes = data['props']['initialProps']['pageProps']['product']['productSizes']
    size_list = [size_dict['sizeDescription'] for size_dict in product_sizes]
    return size_list


def get_html(page: str) -> BeautifulSoup:
    try:
        r = requests.get(page)
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(e)


def get_size_list(page: str):
    return _parse_size(get_html(page))


if __name__ == "__main__":
    print(get_size_list('https://launches.endclothing.com/product/nike-dunk-low-og-w-dm9467-700'))
