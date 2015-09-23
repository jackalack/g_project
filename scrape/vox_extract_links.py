from bs4 import BeautifulSoup
from vox_extract_article import get_article_text
import urllib2
import re

page = urllib2.urlopen("http://www.vox.com/news")

soup = BeautifulSoup(page)

# print soup.find("div", "m-entry__body")
soup =  soup.find("span", "m-pagination__count")

number_of_articles = int(soup.contents[2].split('of ')[-1].replace(',', ''))

print (number_of_articles / 25 ) + 1

#print soup.findAll("p")[0].find('a').contents[0]

# def get_article_text():
#     article = []
#     for paragraph in soup.findAll("p"):
#         returned_list = paragraph.contents 
#         for i, x in enumerate(returned_list):
#             if str(type(x)) == "<class 'bs4.element.Tag'>" and paragraph.find('a')!=None:
#                 returned_list[i] = returned_list[i].contents[0].decode()
#             elif str(type(x)) == "<class 'bs4.element.Tag'>":
#                 del returned_list[i] 
#         article.append(''.join(returned_list))
#     return ''.join(article)

# print get_article_text()


print get_article_text("http://www.vox.com/2015/9/22/9368591/trump-global-warming")