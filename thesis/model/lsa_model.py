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
    # self.index = similarities.MatrixSimilarity(self.vectors)
    self.topics = {}
    self.topic_no = topics
    self.probabilities = {}

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

  def probability(self, topic_index, word):
    if not topic_index in self.probabilities:
      self.probabilities[topic_index] = {}
    if not word in self.probabilities[topic_index]:
      topic = self.get_topic(topic_index)
      topic_total = sum(map(itemgetter(0), topic))
      minimum = min(map(itemgetter(0), [(0,0)] + topic))
      if minimum < 0:
        topic_total -= minimum * len(topic)
      word_entry = filter(lambda x: x[1] == word, topic)
      if len(word_entry) > 0:
        weight = word_entry[0][0]
        if minimum < 0:
          weight -= minimum
        self.probabilities[topic_index][word] = weight / topic_total
      else:
        self.probabilities[topic_index][word] = 0

    return self.probabilities[topic_index][word]


  def perplexity(self, docs):
    perplexity = 0.0

    for doc in docs:
      vector = self.process(doc)
      total = sum(map(lambda x: x[1], vector))
      minimum = min(map(lambda x: x[1], [(0,0)] + vector))
      if minimum < 0:
        total -= minimum * len(vector)
      doc_logprob = 0.0

      for word in doc:
        word_prob = 0.0
        word_vector = self.process([word])
        for (topic_index, weight) in word_vector:
          topic_entry = filter(lambda x: x[0] == topic_index, vector)
          if len(topic_entry) > 0:
            weight = topic_entry[0][1]
            if minimum < 0:
              weight -= minimum
            word_prob += self.probability(topic_index, word) * weight / total

        if word_prob > 0:
          doc_logprob += math.log(word_prob)

      perplexity += doc_logprob / len(doc)

    return math.exp(-perplexity / len(docs))

  def cosine_perplexity(self, docs):
    perplexity = 0.0

    word_vectors = {}
    for word_index in self.dictionary:
      word_vectors[word_index] = self.process([self.dictionary[word_index]])

    for doc in docs:
      doc_vector = self.process(doc)
      denominator = 0.0
      for word_index in word_vectors:
        other_word_vector = word_vectors[word_index]
        denominator += math.pi - math.acos(self.cosine(doc_vector, other_word_vector))
      for word in doc:
        word_vector = self.process([word])
        numerator = math.pi - math.acos(self.cosine(doc_vector, word_vector))
        perplexity += math.log(numerator / denominator) / len(doc)

    return math.exp(-perplexity / len(docs))

  def cosine(self, vector1, vector2):
    other_index = 0
    result = 0.0
    norm1 = self.norm(vector1)
    norm2 = self.norm(vector2)

    for (index, value) in vector1:
      while other_index < len(vector2) and vector2[other_index][0] < index:
        other_index += 1

      if other_index < len(vector2) and index == other_index:
        result += value * vector2[other_index][1] / norm1 / norm2

    return result

  def norm(self, vector):
    result = 0.0

    for (index, value) in vector:
      result += math.pow(value, 2)

    return math.sqrt(result)
