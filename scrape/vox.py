from bs4 import BeautifulSoup
import urllib2
import re

page = urllib2.urlopen("http://www.vox.com/2015/9/22/9368591/trump-global-warming")

soup = BeautifulSoup(page)

# print soup.find("div", "m-entry__body")
soup =  soup.find("div", "m-entry__body")

print soup

print "---------------------------------------------------------------------"
print "---------------------------------------------------------------------"
print "---------------------------------------------------------------------"
print "---------------------------------------------------------------------"


#print soup.findAll("p")[0].find('a').contents[0]

def get_article_text():
    article = []
    for paragraph in soup.findAll("p"):
        returned_list = paragraph.contents 
        for i, x in enumerate(returned_list):
            if str(type(x)) == "<class 'bs4.element.Tag'>" and paragraph.find('a')!=None:
                returned_list[i] = returned_list[i].contents[0].decode()
            elif str(type(x)) == "<class 'bs4.element.Tag'>":
                del returned_list[i] 
        article.append(''.join(returned_list))
    return ''.join(article)

print get_article_text()