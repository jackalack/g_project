# import modules & set up logging
import gensim, logging
import os


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = MySentences('../vox_articles') # a memory-friendly iterator

print "begin training"
model = gensim.models.Word2Vec(sentences, workers = 4)
print "model built"
model.save('/tmp/mymodel')