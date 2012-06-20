# -*- coding: utf-8 -*-

import unittest
import StringIO
from thesis.util.tokenizer import Tokenizer

class TokenizerTest(unittest.TestCase):
  def check(self, text, output):
    io = StringIO.StringIO(text)
    tokenizer = Tokenizer(io)
    words = list(tokenizer)
    self.assertEqual(output, words)

  def test_simple_words(self):
    self.check("some words like this", ["some", "words", "like", "this"])

  def test_capitalized_words(self):
    self.check("Some wORds like thiS", ["Some", "wORds", "like", "thiS"])

  def test_numbers(self):
    self.check("109 and 2010 and 122.1", ["109", "and", "2010", "and", "122.1"])

  def test_interpunction(self):
    self.check("A, sentence. Another one!", ["A", ",", "sentence", ".", "Another", "one", "!"])

  def test_skip_whitespace(self):
    self.check('''some

      words
    ''', ["some", "words"])

  def test_pap_header(self):
    self.check("#100", ["#100"])

  def test_polish_chars(self):
    self.check(u"ąęść", [u"ąęść"])

  def test_words_with_hyphens(self):
    self.check("hyphen-word", ["hyphen-word"])
