import pandas as pd
import csv
import os.path

def create_db():
    with open('../vox_all_article_links.csv', 'rb') as f:
        reader = csv.reader(f)
        articles_urls = list(reader)[0]


    file_names = [x.split('/')[-1] for x in articles_urls]

    names_text = {}

    for i, article in enumerate(file_names):
        file_path = '../vox_articles/' + article + '.txt'
        if os.path.isfile(file_path):
            with open(file_path) as f:
                names_text[article] = f.read()

    df = pd.DataFrame(names_text.items())

    return df


