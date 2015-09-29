from bs4 import BeautifulSoup
import threading
import multiprocessing
from uuid import uuid4
import Queue
import time
import sys
import urllib2
import csv
import re



page = urllib2.build_opener(urllib2.HTTPCookieProcessor).open('http://www.vox.com/2015/9/23/9389443/junipero-serra-vox-sentences')
soup = BeautifulSoup(page)
print soup.find("a", {"class": "m-global-header__dropdown--selected"}).contents[0]=='Vox Sentences'