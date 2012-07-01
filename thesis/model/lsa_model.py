# -*- coding: utf-8 -*-

import os
from gensim import corpora, models, similarities

STOPLIST = set(["NUMBER", ".", "", ",", "-", ")", "(", "\"", u"być", "a"])
NUM_TOPICS = 200
NO_BELOW = 2
NO_ABOVE = 0.7

class ModelWrapper:
  def __init__(self, docs, model, topics=None):
    if(topics == None): topics = NUM_TOPICS

    self.docs = docs
    self.dictionary = corpora.Dictionary(docs)
    self.dictionary.filter_extremes(NO_BELOW, NO_ABOVE, None)
    self.vectors = map(self.vectorize, docs)
    self.logmodel = models.LogEntropyModel(self.vectors, self.dictionary)
    self.vectors = self.logmodel[self.vectors]
    self.model = model(self.vectors, id2word=self.dictionary, num_topics=topics)
    self.vectors = self.model[self.vectors]
    self.index = self.index = similarities.MatrixSimilarity(self.vectors)

  def vectorize(self, doc):
    return self.dictionary.doc2bow(doc)

  def process(self, doc):
    vector = self.vectorize(doc)
    vector = self.logmodel[vector]
    return self.model[vector]

  def topics(self):
    return self.model.show_topics(-1, 10)

  def similar(self, doc):
    sims = self.index[self.process(doc)]
    sims = sorted(enumerate(sims), key=lambda x: -x[1])
    return map(lambda x: x[0], sims)
