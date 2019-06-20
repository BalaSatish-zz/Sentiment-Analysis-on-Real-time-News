import requests
import pandas as pd
from bs4 import BeautifulSoup

def html_text(p):
    soup = BeautifulSoup(p.content, 'html.parser')
    content = soup.select('h2.intro + div p, div.article-topics-container + div p')
    content_text = [tag.get_text() for tag in content]
    return "".join(content_text)

#useCols values
#1=title 2=date 3=link 6=initCrime 8=lat 9=long

# seed = pd.read_csv('DataSourceHindu.csv',header=None,encoding="latin1",usecols=(1,2,3,6,8,9))
# links = seed[3]
link_count = 0
error_count = 0
# # print(seed)
# print("Links =" + str(len(links)))
text = []
links=['https://www.thehindu.com/news/international/new-zealand-mosque-shooting/article26541269.ece']
for link in links:
    page = requests.get(link)
    
    if (page.status_code == 200):
        text.append(html_text(page))
        link_count += 1
        rem = len(links) - link_count
        print("Completed: " + str(link_count) + " Remaining: " + str(rem),text)
    else:
        text.append("404 Empty")
        error_count += 1
        print("Found 404 Error")
print("Total Error: " + str(error_count))