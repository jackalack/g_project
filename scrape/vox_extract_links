from bs4 import BeautifulSoup
from vox_extract_article import get_article_text
import urllib2
import csv
import re


def extract_article_num():
    page = urllib2.urlopen("http://www.vox.com/news")
    soup = BeautifulSoup(page)
    soup =  soup.find("span", "m-pagination__count")
    number_of_articles = int(soup.contents[2].split('of ')[-1].replace(',', ''))
    number_of_pages =  (number_of_articles / 25 ) + 1
    return number_of_pages

def extract_article_links(number_of_pages):
    links = []

    for x in xrange(1, number_of_pages+1):
        print "http://www.vox.com/news/" + str(x)
        if x == 1:
            page = urllib2.urlopen("http://www.vox.com/news")
        else:
            page = urllib2.urlopen("http://www.vox.com/news/" + str(x))
        soup = BeautifulSoup(page.read()).select("div header h3 a")
        [links.append(element['href']) for element in soup]
    return links
        # articles = [td.findAll("div", { "class": "m-block article post"}) for td in soup.findAll("div", { "class": "l-chunk"})]
        # print articles[0]


print "begin"
number_of_pages = extract_article_num()
articles = extract_article_links(number_of_pages)

f = open("vox_all_article_links.csv", 'w')
writer = csv.writer(f)
writer.writerow(articles)
print "end"

