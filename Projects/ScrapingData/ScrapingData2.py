import requests
from bs4 import BeautifulSoup
import pprint

url = 'https://news.ycombinator.com/'
res = requests.get(url)

soup = BeautifulSoup(res.content, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')


def custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'Points': points})
    return hn


pprint.pprint(custom_hn(links, subtext))
