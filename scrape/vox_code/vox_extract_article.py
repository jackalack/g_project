from bs4 import BeautifulSoup
import threading
import multiprocessing
from uuid import uuid4
import unicodedata
import Queue
import time
import sys
import urllib2
import csv
import re


dirty_links = []
daily_summaries = []

def in_parallel(fn, l):
       for i in l:
           Thread(target=fn, args=(i,)).start()
 
def import_article_links():
    with open('../vox_all_article_links.csv', 'rb') as f:
        reader = csv.reader(f)
        return list(reader)[0]

    
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def write_csv(filename, input_list):
    f = open(filename, 'wt')
    writer = csv.writer(f)
    for item in input_list:
        writer.writerow(item)
    f.close()

def get_article_text(url):
    try:
        page = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
        # response = urllib2.urlopen(url)
        # page = response.read()
        soup = BeautifulSoup(page)
        global_header = soup.find("a", {"class": "m-global-header__dropdown--selected"})
        daily_summary = global_header.contents[0]=='Vox Sentences' if global_header else False
        soup =  soup.find("div", "m-entry__body")
        article = []
        if daily_summary:
            print url
            daily_summaries.append(url)
        elif soup!=None:
            for paragraph in soup.findAll("p"):
                returned_list = paragraph.contents 
                for i, x in enumerate(returned_list):
                    if str(type(x)) == "<class 'bs4.element.Tag'>" and (x.select('a')!=None or x.select('em')!=None):
                        returned_list[i] = x.get_text(' ', strip=True)
                    elif str(type(x)) == "<class 'bs4.element.Tag'>":
                        del returned_list[i] 
                article.append(' '.join(returned_list))
            article = ''.join([strip_accents(s) for s in ' '.join(article)])
            article = ''.join([ch for ch in article if ord(ch)<128])
            f = open('../vox_articles/' + url.split('/')[-1]+".txt", 'w')
            f.write(article)

    except urllib2.HTTPError, e:
        print url
        dirty_links.append(url)



# import unicodedata
    
# def strip_accents(s):
#    return ''.join(c for c in unicodedata.normalize('NFD', s)
#                   if unicodedata.category(c) != 'Mn')

# def concurrent_scrape(minimum, maximum):
#     jobs = []
#     events = []

#     q = Queue.Queue()
#     for i in range(minimum,maximum):
#         # time.sleep(.3)
#         # thread_event = threading.Event()

#         thread = threading.Thread(name=i, target=get_article_text, args=(article_links[i],))
#         jobs.append(thread)
#         events.append(thread_event)
#         thread.daemon = True
#         thread.start()
    
#     for j in jobs:
#         j.join()

#     # for event in events:
#     #     event.set()


if __name__ == '__main__':
    print "begin"
    article_links = import_article_links()
    s = set()
    for item in article_links:
        s.add(item)
    for i in xrange(0,len(s)+1):
        if i % 50 == 0:
            print i
        get_article_text(article_links[i])
    write_csv('../daily_summaries.csv', daily_summaries)
    write_csv('../dirty_links.csv', dirty_links)


