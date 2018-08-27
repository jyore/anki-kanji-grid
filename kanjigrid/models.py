import re
from aqt import mw
from anki.utils import ids2str

from .config import Config


class KanjiSet(Config):

    def __init__(self, filepath):
        super(Config, self).__init__(self, filepath)
        self.set = None


    def reset(self):
        self.config = {}
        self.load(self)


    def get_set_names(self):
        return self.config.keys()


    def select_set(self, name):
        self.set = self.config[name]


    def num_tiers(self):
        return len(self.set) if self.set else -1
    

    def get_tier(self, tier):
        return self.set[tier] if self.set else None




class KanjiStats:

    def __init__(self, decks, nrev=500):
        self.decks = decks
        sekf.nrev = nrev
        self.kanji = {}

        # regex to pull out all kanji characters. ignores hiragana, 
        # katakana, romanized characters, numbers, punctuation, etc.
        self.kanji_regex = re.compile(ur"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]")


    def generate(self):

        # all notes
        notes = mw.col.db.all('select id,flds from notes') 
        for note in notes:
                 
            # all reviews for each note in selected decks
            reviews = mw.col.db.all('select id,ease,time from revlog where cid = (select id from cards where nid = %s and did in %s)' % (note[0], ids2str(self.decks)))
      
            # get unique list of kanji from note data (all fields)
            characters = set(self.kanji_regex.findall(note[1]))
            
            for k in characters:
                if k not in self.kanji:
                    self.kanji[k] = {
                        'count':    0,
                        'reviews':  0,
                        'first':    9999999999999,
                        'last':     0,
                        'pass':     0,
                        'fail':     0,
                        'time':     0,
                    }
           
                self.kanji[k]['count'] += 1
                self.kanji[k]['reviews'] += len(reviews)
          
                for review in reviews:
                    self.kanji[k]['first'] = min(kanji[k]['first'], review[0]/1000.0)
                    self.kanji[k]['last'] = max(kanji[k]['last'], review[0]/1000.0)
                    self.kanji[k]['time'] = kanji[k]['time'] + review[2]/1000.0
          
                    if review[1] == 1:
                        self.kanji[k]['fail'] += 1
                    else:
                        self.kanji[k]['pass'] += 1

                self.kanji[k]['rate']     = self.kanji[k]['pass']/(self.kajii[k]['pass'] + self.kanji[k]['fail'])
                self.kanji[k]['strength'] = self.__calculate_strength(self.kanji[k])
      


    # simple formula until more data is analyzed
    # just return value between 0 and 1 based on
    # the number of times a kanji has been reviewed
    # relative to the configured max range
    def __calculate_strength(self, kanji):
        return min(kanji['reviews'] / float(self.nrev), 1.0)



class KanjiGridUI:

    def __init__(self):
        pass
