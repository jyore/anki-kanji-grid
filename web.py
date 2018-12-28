import time
from yattag import Doc

def hsvrgbstr(h, s=0.8, v=0.9):
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0: return "#%0.2X%0.2X%0.2X" % (int(v*256),int(t*256),int(p*256))
    if i == 1: return "#%0.2X%0.2X%0.2X" % (int(q*256),int(v*256),int(p*256))
    if i == 2: return "#%0.2X%0.2X%0.2X" % (int(p*256),int(v*256),int(t*256))
    if i == 3: return "#%0.2X%0.2X%0.2X" % (int(p*256),int(q*256),int(v*256))
    if i == 4: return "#%0.2X%0.2X%0.2X" % (int(t*256),int(p*256),int(v*256))
    if i == 5: return "#%0.2X%0.2X%0.2X" % (int(v*256),int(p*256),int(q*256))


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def calculate_strength(reviews, threshold):
    return min(reviews / float(threshold), 1.0)/2


def format_time(t):
    tf = float(t)
    if tf > 60.0:
        if tf > 360.0:
            return "%.1fh" % (tf/360.0)
        else:
            return "%.1fm" % (tf/60.0)
    else:
        return "%.1fs" % tf

def jisho_kanji(n):
    return 'https://jisho.org/kanji/details/%s' % n


def tooltip(c, separator=' | '):
    return separator.join([
        'Character: %s'      % c['name'],
        'Cards: %s'          % c['count'],
        'Reviews: %s'        % c['reviews'],
        'First Rep: %s'      % ('New' if c['reviews'] <= 0 else time.strftime('%Y-%m-%d', time.localtime(c['first']))),
        'Last Rep: %s'       % ('New' if c['reviews'] <= 0 else time.strftime('%Y-%m-%d', time.localtime(c['last']))),
        'Reviews Passed: %s' % c['pass'],
        'Reviews Failed: %s' % c['fail'],
        'Pass Rate: %s'      % ('0.0%' if c['reviews'] <= 0 else '%.1f%%' % (100.0*c['pass']/float(c['reviews']))),
        'Time: %s'           % format_time(c['time']),
    ])
    

def legend():
    chart = []
    for c in [n/6.0 for n in range(7)]:
        chart.append('<span class="key" style="background-color: %s;">&nbsp;</span>' % hsvrgbstr(c/2))
    return "".join(chart)


def html_doc(decks, elements, threshold=500):
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('title'):
                text('Kanji Grid Advanced')
            doc.stag('meta', ('http-equiv', 'Contect-Type'), content='text/html; charset=UTF-8')
            with tag('style', type='text/css'):
                text('.key {display:inline-block; width:3em;} a,a:visited{color:#000;text-decoration:none;}')
        with tag('body', bgcolor='#ffffff'):
            with tag('span', style='font-size: 3em; color: #888;'):
                text('Kanji Grid:')
            with tag('span', style='font-size: 1em; color: #888; margin-left: 20px;'):
                text('%s' % decks)
            doc.stag('br')
            with tag('div', style='margin-bottom: 24pt; padding: 20pt;'):
                with tag('p', style='float: left'):
                    text('Key (based on %s reviews):' % threshold)
                doc.asis('<p style="float: right">Weak&nbsp; %s &nbsp;Strong</p>' % legend())
            with tag('div', style='clear: both;'):
                doc.stag('br')
                doc.stag('hr', style='border-style:dashed; border-color:#666; width:60%')
                doc.stag('br')
            with tag('center'):
                for element in elements:
                    doc.asis(element)

    return doc.getvalue()


def tier_html(name, results, found, missing, cols=40, threshold=500, separator=' | ', force_percent=False):
    doc, tag, text = Doc().tagtext()
    with tag('h2', style='color:#888;'):
        text(name)

        with tag('h4', style='color:#888;'):
            nf = len(found)

            if force_percent or len(missing) > 0:
                nt = len(found) + len(missing)
                try:
                    pct = (nf*100.0)/nt
                except ZeroDivisionError:
                    pct = 0.0

                text('%d of %d - %0.2f%%' % (nf,nt,pct))
            else:
                text('%d Kanji' % nf)



    with tag('table', width='85%'):
        for chunk in chunks(found, cols):
            with tag('tr'):
                for char in chunk:
                    bgcolor = hsvrgbstr(calculate_strength(results[char]['reviews'],threshold)) if results[char]['reviews'] > 0 else '#ffffff'
                    with tag('td', align='center', valign='top', style='background:%s;white-space:pre-line;' % bgcolor, title=tooltip(results[char], separator=separator)):
                        with tag('a', href=jisho_kanji(char)):
                            text(char)
    doc.stag('br')

    if len(missing) > 0:
        with tag('details'):
            with tag('summary'):
                text('Missing Kanji')
            with tag('table', style='max-width:75%;'):
                for chunk in chunks(missing, cols):
                    with tag('tr'):
                        for char in chunk:
                            with tag('td', align='center', valign='top', style='background:#eee;color:#fff;', title='Character: %s' % char):
                                with tag('a', href=jisho_kanji(char), style='color:#888;', target="_blank"):
                                    text(char)

    return doc.getvalue()


if __name__ == "__main__":

    tiers = [
        {
            'name': 'Tier 1',
            'found': [
                {
                    'name': '私',
                    'count': 123,
                    'reviews': 1234,
                    'first': 0,
                    'last': 0,
                    'pass': 1200,
                    'fail': 3,
                    'rate': 99.9,
                    'time': 58,
                },
                {
                    'name': '開',
                    'count': 123,
                    'reviews': 123,
                    'first': 0,
                    'last': 0,
                    'pass': 120,
                    'fail': 3,
                    'rate': 99.9,
                    'time': 6000,
                }
            ],
            'missing': ['足','目']
        },
        {
            'name': 'Additional',
            'found': [
                {
                    'name': '歩',
                    'count': 123,
                    'reviews': 50,
                    'first': 0,
                    'last': 0,
                    'pass': 35,
                    'fail': 3,
                    'rate': 99.9,
                    'time': 58,
                },
            ],
            'missing': []
        }
    ]
    tier_docs = []
    for tier in tiers:
        tier_docs.append(tier_html(tier['name'],tier['found'],tier['missing']))

    html = html_doc("decks", ''.join(tier_docs))

    print(html)
