#! python3
# Usage: py.exe link_verification.py <link>

import sys
import bs4
import requests
import re


def link_verfication():
    if len(sys.argv) == 1:
        link = sys.argv[1]

        try:
            resp = requests.get(link)
            resp.raise_for_status()

            broken = []
            working = []
            print(f'Verifying all links on page: {link}')
            soup = bs4.BeautifulSoup(resp.text, 'html.parser')
            for page_link in soup.find_all('a',
                                           {'href': re.compile('^http(s)?')}):
                link = page_link['href']
                if link not in working and link not in broken:
                    resp = requests.get(link)
                    if resp.status_code == 404:
                        broken.append(link)
                        print(f'{link} broken')
                    else:
                        working.append(link)
                        print(f'{link} fine')
            if broken:
                print(f'Broken Links:\n{broken}')

        except Exception as err:
            print(f'There was a problem: {err}')


if __name__ == '__main__':
    link_verfication()
