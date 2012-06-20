# -*- coding: utf-8 -*-

import re

TOKENIZER_SLICER = re.compile(u'''#\d+|(?:\d+\.\d+)+|(?:\w|\-|ą|ę|ś|ć|ż|ź|ó|ł|ń|Ą|Ę|Ś|Ć|Ż|Ź|Ó|Ł|Ń)+|[^\t\n\r ]''')

class Tokenizer:
  def __init__(self, io):
    self.io = io

  def __iter__(self):
    for word in TOKENIZER_SLICER.findall(self.io.read()):
      yield word
