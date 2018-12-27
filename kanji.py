
import re

from aqt import mw
from anki.utils import ids2str


RE_KANJI = re.compile(u"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]")

CARD_SEARCH = """select 
    c.id, 
    n.flds, 
    n.mid 
from 
    cards c 
join 
    notes n on c.nid=n.id 
where 
    c.did in %s"""

REVIEW_SEARCH = """select
    id/1000.0,
    ease,
    time/1000.0
from
    revlog
where
    cid = %s"""


def kanji_search(decks, exclusions={}):
    kanji = {}
    results = mw.col.db.all(CARD_SEARCH % ids2str(decks))

    for (card,flds,model) in results:

        if str(model) in exclusions:
            flist = flds.split("")
            [flist.pop(i) for i in sorted(exclusions[str(model)],reverse=True)]
            flds = "".join(flist)

        characters = set(RE_KANJI.findall(flds))
        reviews = mw.col.db.all(REVIEW_SEARCH % card)
        for k in characters:
            if k not in kanji:
                kanji[k] = {
                    'name':    k,
                    'count':   0,
                    'reviews': 0,
                    'first':   9999999999999.0,
                    'last':    0.0,
                    'pass':    0,
                    'fail':    0,
                    'time':    0,
                }
            kanji[k]['count'] += 1
            kanji[k]['reviews'] += len(reviews)

            for (date, ease, sec) in reviews:
                kanji[k]['first'] = min(float(kanji[k]['first']), date)
                kanji[k]['last']  = max(float(kanji[k]['last']), date)
                kanji[k]['time']  += float(sec)

                if ease == 1:
                    kanji[k]['fail'] += 1
                else:
                    kanji[k]['pass'] += 1

    return kanji



def find_kanji_in_tier(characters, kanji_list):

    found = []
    for character in characters:
        if character in kanji_list:
            found.append(character)

    return ([characters[x] for x in found], list(set(kanji_list) - set(found)))
        
