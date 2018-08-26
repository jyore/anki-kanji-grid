import re
import time,codecs,math,os,unicodedata
from aqt import mw
from anki.utils import ids2str

# regex to pull out all kanji characters. ignores hiragana, katakana, romanized characters, numbers, punctuation, etc.
ALL_KANJI_REGEX = re.compile(ur"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]")


def build_kanji_statistics(decks):
  kanji = {}

  # all notes
  notes = mw.col.db.all('select id,flds from notes') # TODO: Allow exclusion list
  for note in notes:

    # all reviews for each note in selected decks
    reviews = mw.col.db.all('select id,ease,time from revlog where cid = (select id from cards where nid = %s and did in %s)' % (note[0], ids2str(decks)))

    if len(reviews) > 0:

      # get unique list of kanji from note data (all fields)
      characters = set(ALL_KANJI_REGEX.findall(note[1]))
      
      for k in characters:
        if k not in kanji:
          kanji[k] = {
            'count':   0,
            'reviews': 0,
            'first':   9999999999999,
            'last':    0,
            'pass':    0,
            'fail':    0,
            'time':    0,
          }
   
        kanji[k]['count'] += 1
        kanji[k]['reviews'] += len(reviews)
  
        for review in reviews:
          kanji[k]['first'] = min(kanji[k]['first'], review[0]/1000.0)
          kanji[k]['last'] = max(kanji[k]['last'], review[0]/1000.0)
          kanji[k]['time'] = kanji[k]['time'] + review[2]/1000.0
  
          if review[1] == 1:
            kanji[k]['fail'] += 1
          else:
            kanji[k]['pass'] += 1

  return kanji

