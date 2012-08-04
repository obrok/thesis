# -*- coding: utf-8 -*-

import os
import math
from operator import itemgetter
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
    self.topics = {}
    self.topic_no = topics

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

  def get_topic(self, topic_index):
    if not topic_index in self.topics:
      self.topics[topic_index] = self.model.show_topic(topic_index, len(self.dictionary))
    return self.topics[topic_index]

  def perplexity(self, docs):
    perplexity = 0.0

    for doc in docs:
      vector = self.process(doc)
      total = sum(map(lambda x: x[1], vector))
      doc_logprob = 0.0

      for word in doc:
        word_prob = 0.0
        word_vector = self.process([word])
        for (topic_index, weight) in word_vector:
          topic = self.get_topic(topic_index)
          topic_total = sum(map(itemgetter(0), topic))
          topic_entry = filter(lambda x: x[0] == topic_index, vector)
          word_entry = filter(lambda x: x[1] == word, topic)
          if len(word_entry) > 0 and len(topic_entry) > 0:
            weight = word_entry[0][0]
            topic_weight = topic_entry[0][1]
            word_prob += topic_weight / total * weight / topic_total

        if word_prob > 0:
          doc_logprob += math.log(word_prob)

      perplexity += doc_logprob / len(doc)

    return math.exp(-perplexity / len(docs))

