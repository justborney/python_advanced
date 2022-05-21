import asyncio

import aiohttp
from bs4 import BeautifulSoup

all_links = set()
urls = {'https://www.geeksforgeeks.org/'}


async def main(urls, deepth=3):
    for link in urls:
        all_links.add(link)
    await crawler(urls, deepth)
    with open('results.txt', mode='a') as f:
        [f.write(link + '\n') for link in all_links]


async def crawler(urls, deepth):
    if deepth >= 1:
        for url in urls:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    result = await response.read()
                    soup = BeautifulSoup(result, 'html.parser')
            await worker(soup, deepth)


async def worker(soup, deepth):
    new_urls = set()
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            if link['href'].find('http') == 0:
                new_urls.add(link['href'])
                all_links.add(link['href'])
    deepth -= 1
    await crawler(new_urls, deepth)


if __name__ == '__main__':
    asyncio.run(main(urls))
