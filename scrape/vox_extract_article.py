from bs4 import BeautifulSoup
from timeit import Timer
import threading
import multiprocessing
from uuid import uuid4
import urllib2
import csv
import re


def in_parallel(fn, l):
       for i in l:
           Thread(target=fn, args=(i,)).start()
 
# def download_image(i):
#        print "saving -> "+i
#        f=open(str(uuid4())+".jpg",'wb')
#        f.write(from_page(i))
#        f.close()
 
# def all_links(p):
#        links = re.findall(r'href="([^"]+)"',p)
#        return [links[i] for i in xrange(0,len(links)) if "http" and "jpg" in links[i]]
 
# def from_page(u):
#        return urllib2.urlopen(u).read()
 
# in_parallel(download_image, all_links(from_page("http://www.reddit.com/r/pics")))


def import_article_links():
    with open('vox_all_article_links.csv', 'rb') as f:
        reader = csv.reader(f)
        return list(reader)[0]

import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def get_article_text(url):
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
        f = open(url.split('/')[-1]+".txt", 'w')
        f.write(article)


#get_article_text("http://www.vox.com/2015/9/22/9370549/black-on-black-crime")
#print article_links[23]


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
    for x in xrange(0,len(s)+1, 50):
        if x < len(s)-60:
            y = x + 50
        else:
            y = len(s)+1
        print x,y
        concurrent_scrape(x,y)


