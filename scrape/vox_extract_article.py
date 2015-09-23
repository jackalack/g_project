from bs4 import BeautifulSoup
import threading
import multiprocessing
from uuid import uuid4
import time
import sys
import urllib2
import csv
import re


articles = {}

def in_parallel(fn, l):
       for i in l:
           Thread(target=fn, args=(i,)).start()
 
def import_article_links():
    with open('vox_all_article_links.csv', 'rb') as f:
        reader = csv.reader(f)
        return list(reader)[0]

import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def get_article_text(url):
    time.sleep(2)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    soup =  soup.find("div", "m-entry__body")
    article = []
    if soup!=None:
        for paragraph in soup.findAll("p"):
            returned_list = paragraph.contents 
            for i, x in enumerate(returned_list):
                if str(type(x)) == "<class 'bs4.element.Tag'>" and (x.select('a')!=None or x.select('em')!=None):
                    returned_list[i] = x.get_text(' ', strip=True)
                elif str(type(x)) == "<class 'bs4.element.Tag'>":
                    del returned_list[i] 
            article.append(''.join(returned_list))
        article = ''.join([ch for ch in ''.join(article) if ord(ch)<128])
        articles[url] = article


def write_articles(url):
    f = open(url.split('/')[-1]+".txt", 'w')
    f.write(article)


#get_article_text("http://www.vox.com/2015/9/22/9370549/black-on-black-crime")
#print article_links[23]


# def worker():
#     """thread worker function"""
#     print 'Worker'
#     return

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#     t.start()


def concurrent_scrape(minimum,maximum):
    jobs = []

    for i in range(minimum,maximum):
        thread = threading.Thread(name=i, target=get_article_text, args=(article_links[i],))
        jobs.append(thread)
        thread.start()
    
    for j in jobs:
        j.join()


if __name__ == '__main__':
    print "begin"
    article_links = import_article_links()
    s = set()
    for item in article_links:
        s.add(item)
    for x in xrange(0,len(s)+1, 20):
        if x < len(s)-19:
            y = x + 20
        else:
            y = len(s)+1
        print x,y
        concurrent_scrape(x,y)


