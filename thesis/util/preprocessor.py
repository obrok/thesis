# -*- coding: utf-8 -*-

STOP_LIST = set([
  u'przez', u'po', u'rosyjski', u'bank', u'poinformować', u'punkt', u'we', u'Rosja', u'grupa', u'Czeczenia',
  u'klub', u'pod', u'wzróść', u'warszawa', u'uważać', u'prezes', u'środa', u'wtorek', u'ostatni', u'rada',
  u'premiera', u'mistrzostwo', u'zdać', u'lider', u'biga', u'luty', u'rynek', u'inny', u'styczeń', u'dobry',
  u'puchar', u'praca', u'amerykański', u'papa', u'oświadczyć', u'europ', u'wygrać', u'komisja', u'sejm',
  u'mecz', u'czwartek', u'związek', u'kurs', u'zająć', u'przyjąć', u'odbyć', u'wig', u'pierwszy', u'niedziela',
  u'nagroda', u'Jerzy', u'Niemcy', u'bliski', u'móc', u'udział', u'przedstawiciel', u'powinien', u'mieć',
  u'cena', u'sobota', u'żyć', u'organizacja', u'projekt', u'decyzja', u'zagraniczny', u'podać', u'strona',
  u'nad', u'rzecznik', u'wzrost', u'miasto', u'główny', u'zmienić', u'ustawa', u'trzeci', u'dziennikarz',
  u'st', u'marzec', u'chcieć', u'spaść', u'wysoki', u'piątek', u'wynikać', u'siła', u'turniej', u'kandydat',
  u'giełda', u'zakończyć', u'czeczeński', u'marek', u'urząd', u'fundusz', u'bg', u'spółka', u'niemiecki',
  u'bardzo', u'stać', u'prawo', u'prowadzić', u'zdecydować', u'usa', u'kolejny', u'działać', u'Andrzej',
  u'Austria', u'informacja', u'dolar', u'r', u'zespół', u'pokonać', u'pzę', u'uw', u'członek', u'otrzymać',
  u'porozumienie', u'światowy', u'sesja', u'większość', u'południe', u'cały', u'tydzień', u'warszawski',
  u'sytuacja', u'rozpocząć', u'wielki', u'firma', u'polityka', u'wśród', u'uieć', u'piłkarski', u'stan',
  u'temat', u'uznać', u'dotyczyć', u'rozmowa', u'oko', u'poniedziałek', u'film', u'znaleźć', u'mówić',
  u'stosunek', u'bojownik', u'sprzedaż', u'kilometr', u'przeciwko', u'dodać', u'poprzeć', u'miał', u'tempo',
  u'przy', u'zmiana', u'sekunda', u'sld', u'kobieta', u'poseł', u'zdobyć', u'wspólny', u'Moskwa', u'powód',
  u'reprezentacja', u'koniec', u'zachodni', u'przeprowadzić', u'program', u'poziom', u'maić', u'zachód',
  u'stanowisko', u'nata', u'haider', u'letni', u'prasowy', u'Jan', u'śnieg', u'opublikować', u'ważny',
  u'obrona', u'wniosek', u'austriacki', u'ciąg', u'przyznać', u'część', u'narodowy', u'ii', u'raport',
  u'zapowiedzieć', u'osiągnąć', u'francuski', u'wyrazić', u'prawić', u'wojna', u'Paweł', u'żołnierz',
  u'między', u'makler', u'miesiąc', u'publiczny', u'parlamentarny', u'agencja', u'twierdzić'
])

class Preprocessor:
  def __init__(self, docs):
    self.docs = docs

  def processed(self):
    stopped = map(docs, self.stop);
    

  def stop(self, doc):
    return filter(doc, lambda word: word not in STOP_LIST)
