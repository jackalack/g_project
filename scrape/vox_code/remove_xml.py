import re
import os
import csv

def remove_xml():
    with open('../vox_all_article_links.csv', 'rb') as f:
        reader = csv.reader(f)
        articles_urls = list(reader)[0]


    file_names = [x.split('/')[-1] for x in articles_urls]

    names_text = {}

    for i, article in enumerate(file_names):
        filename = '../vox_articles/' + article + '.txt'
        if os.path.isfile(filename):
            with open(filename) as f:
                s = f.read()
                m = re.search('\[if gte mso 9\][\s\S]*endif]', s)
            # do stuff with file_str
            if m!=None:
                with open(filename, "w") as f:
                    s = s.replace(m.group(0), '')
                    f.write(s)



if __name__ == '__main__':
    remove_xml()