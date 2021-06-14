import requests
from bs4 import BeautifulSoup
import pprint


def link_fun():
    pages = 3  # example
    news = []
    for page in range(pages):
        url = 'https://news.ycombinator.com/news?p=' + str(page)  # page number
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        ''' Need to pull the subtext here because few of the articles will come without votes,
        I just want to remove them because I only want to pull the best articles'''

        for link, score in zip(links, subtext):  # iterating the links, scores
            story_url = link.get('href', None)
            title = link.getText()
            votes = score.select('.score')
            if len(votes):
                points = int(votes[0].text.replace(' points', ''))
                if points > 99:
                    news.append({'Title': title, 'Link': story_url, 'Votes': points})
    return news


news_final = link_fun()
news_final.sort(key=lambda k:k['Votes'], reverse=True)

pprint.pprint(news_final)
