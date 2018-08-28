import time,codecs,os,re,random,unicodedata
from aqt import mw
from aqt.qt import *
from aqt.webview import AnkiWebView
from anki.utils import ids2str
from aqt.utils import showInfo


from .config import Config

UI_PATH = 'kanjigrid/ui.json'
UI_DEFAULTS = {
    'decks' : {},
    'cols_table': "20",
    'cols_export': "48",
    'group': 0,
    'rev_strength': '500',
}

DEFAULT_SETS = 'kanjigrid/defaultsets.json'
CUSTOM_SETS = 'kanjigrid/customsets.json'


class KanjiSet(Config):

    def __init__(self, filepath):
        super(KanjiSet, self).__init__(filepath)
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
        self.nrev = nrev
        self.kanji = {}

        # regex to pull out all kanji characters. ignores hiragana, 
        # katakana, romanized characters, numbers, punctuation, etc.
        self.kanji_regex = re.compile(ur"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]")


    def generate(self):

        # all notes
        notes = mw.col.db.all('select id,flds from notes') 
        for note in notes:
                 
            # all reviews for each note in selected decks
            reviews = mw.col.db.all('select id/1000.0,ease,time/1000.0 from revlog where cid = (select id from cards where nid = %s and did in %s)' % (note[0], ids2str(self.decks)))
      
            # get unique list of kanji from note data (all fields)
            characters = set(self.kanji_regex.findall(note[1]))
            for k in characters:
                if k not in self.kanji:
                    self.kanji[k] = {
                        'count':    0,
                        'reviews':  0,
                        'first':    9999999999999.0,
                        'last':     0.0,
                        'pass':     0,
                        'fail':     0,
                        'time':     0,
                    }
           
                self.kanji[k]['count'] += 1
                self.kanji[k]['reviews'] += len(reviews)
          
                for (date,ease,sec) in reviews:
                    self.kanji[k]['first'] = min(self.kanji[k]['first'], date)
                    self.kanji[k]['last'] = max(self.kanji[k]['last'], date)
                    self.kanji[k]['time'] = self.kanji[k]['time'] + sec
          
                    if ease == 1:
                        self.kanji[k]['fail'] += 1
                    else:
                        self.kanji[k]['pass'] += 1


        for k in self.kanji:
            if self.kanji[k]['reviews'] > 0:
                self.kanji[k]['first'] = time.strftime(_('%Y-%m-%d'), time.localtime(self.kanji[k]['first']))
                self.kanji[k]['last']  = time.strftime(_('%Y-%m-%d'), time.localtime(self.kanji[k]['last']))
                self.kanji[k]['rate']  = "%.1f%%" % (100*self.kanji[k]['pass']/float(self.kanji[k]['reviews']))
                self.kanji[k]['strength'] = self.__calculate_strength(self.kanji[k])
            else:
                self.kanji[k]['first'] = self.kanji[k]['last'] = "New"
                self.kanji[k]['rate'] = "0.0%"
                self.kanji[k]['strength'] = 0
     


    # simple formula until more data is analyzed
    # just return value between 0 and 1 based on
    # the number of times a kanji has been reviewed
    # relative to the configured max range
    def __calculate_strength(self, kanji):
        return min(kanji['reviews'] / float(self.nrev), 1.0)



class KanjiGridUI:

    def __init__(self, mw, cfg_path=UI_PATH, cfg_defaults=UI_DEFAULTS, default_sets=DEFAULT_SETS, custom_sets=CUSTOM_SETS):

        self.config_action = QAction("Generate Kanji Grid", mw)
        mw.connect(self.config_action, SIGNAL("triggered()"), self.setup)
        mw.form.menuTools.addAction(self.config_action)

        self.options = Config(os.path.join(mw.pm.addonFolder(), cfg_path), cfg_defaults)
        self.options.load()

        self.default_sets = KanjiSet(os.path.join(mw.pm.addonFolder(), default_sets))
        self.custom_sets  = KanjiSet(os.path.join(mw.pm.addonFolder(), custom_sets))



    def populate_settings(self):
        self.cols_table.setText(self.options['cols_table'])
        self.cols_export.setText(self.options['cols_export'])
        self.rev_strength.setText(self.options['rev_strength'])
        self.group_by.setCurrentIndex(self.options['group'])


    def update_settings(self):
        self.options['cols_table'] = self.cols_table.text()
        self.options['cols_export'] = self.cols_export.text()
        self.options['group'] = self.group_by.currentIndex()
        self.options['rev_strength'] = self.rev_strength.text()


    def setup(self):
        self.swin = QDialog(mw)
        layout = QVBoxLayout()
        layout.addWidget(self.create_layout())
        self.swin.setLayout(layout)

        self.options.load()
        self.populate_settings()

        self.swin.setMinimumWidth(600)
        self.swin.setMaximumWidth(600)


        if self.swin.exec_():
            mw.progress.start(immediate=True)
            self.update_settings()
            self.options.save()
            self.show_grid()
            mw.progress.finish()
            self.win.show()


    def create_layout(self):
        hz_group_box = QGroupBox("Kanji Grid Setup")
        layout = QGridLayout()

        self.decklist = self.cb_list()


        self.cols_table   = QLineEdit()
        self.cols_export  = QLineEdit()
        self.rev_strength = QLineEdit()

        self.group_by = QComboBox()
        self.group_by.addItems(self.load_group_sets())


        self.generatebtn = QPushButton("Generate")
        self.generatebtn.connect(self.generatebtn, SIGNAL("clicked()"), self.swin, SLOT("accept()"))
        self.cancel = QPushButton("Cancel")
        self.cancel.connect(self.cancel, SIGNAL("clicked()"), self.swin, SLOT("reject()"))

        # row 0
        layout.addWidget(QLabel("Check Each Deck to Include in Scan"), 0, 0, 1, 4)
        layout.addWidget(QLabel("Number colums in table"), 0, 7, 1, 4)

        # row 1
        layout.addWidget(self.decklist, 1, 0, 6, 4) # through row 5
        layout.addWidget(self.cols_table, 1, 7, 1, 4)

        # row 2
        layout.addWidget(QLabel("Number columns in export"), 2, 7, 1, 4)
        

        # row 3
        layout.addWidget(self.cols_export, 3, 7, 1, 4)


        # row 4
        layout.addWidget(QLabel(""), 4, 7, 1, 4)


        # row 5
        layout.addWidget(QLabel("Number reviews for strength"), 5, 7, 1, 4)


        # row 6
        layout.addWidget(self.rev_strength, 6, 7, 1, 4)


        # row 7
        layout.addWidget(QLabel("Group Results by"), 7, 0, 1, 4)


        # row 9
        layout.addWidget(self.group_by, 8, 0, 1, 4)
        #layout.addWidget(QPushButton("Upload Custom Set"), 8, 7, 1, 4) #TODO: allow custom upload


        # row 10
        layout.addWidget(QLabel(""), 9, 0, 1, 4)


        # row 11
        layout.addWidget(self.cancel, 10, 0, 1, 4)
        layout.addWidget(self.generatebtn, 10, 7, 1, 4)


        hz_group_box.setLayout(layout)
        return hz_group_box



    def cb_list(self):
        widget = QListWidget()
        widget.itemChanged.connect(self.list_state_changed)

        decks = mw.col.decks.all()

        for deck in decks:
            name = deck["name"]
            item = QListWidgetItem(name)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            

            if name in self.options['decks']:
                item.setCheckState(Qt.Checked if self.options['decks'][name]['state'] else Qt.Unchecked)
            else:
                self.options['decks'][name] = {'state': True }
                item.setCheckState(Qt.Checked)

            # always update the id (in case of rare event someone deletes a
            # deck and recreates a deck with the same name
            self.options['decks'][name]['id'] = deck['id']

            widget.addItem(item)

        return widget


    def load_group_sets(self):
        self.default_sets.load()
        self.custom_sets.load()

        defaults = self.default_sets.get_set_names()
        customs  = self.custom_sets.get_set_names()
        defaults.extend(customs)
        return defaults 


    def list_state_changed(self, item):
        self.options['decks'][item.text()]['state'] = item.checkState()


    def show_grid(self):
        decks = []
        for i in range(self.decklist.count()):
            item = self.decklist.item(i)

            if item.checkState():
                decks.append(self.options['decks'][item.text()]['id'])

        self.scan = KanjiStats(decks,nrev=self.options['rev_strength'])
        self.scan.generate()

        # Optimize?
        self.default_sets.select_set(self.group_by.itemText(self.options['group']))
        self.display_grid()
        


    def generate(self,save=False):

        decks = []
        for d in self.options['decks']:
            if self.options['decks'][d]['state'] != 0 or self.options['decks'][d]['state'] != False:
                decks.append(d)


        chart = []
        table = ""
        for c in [n/6.0 for n in range(7)]:
            chart.append('<span class="key" style="background-color: %s;">&nbsp;</span>' % hsvrgbstr(c/2))


        table = self.html_for_tier(save=save)

        self.html = """
<!DOCTYPE HTML>
<html><head><title>Anki Kanji Grid</title></head><body bgcolor="#FFF">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<span style="font-size: 3em;color: #888;">Kanji Grid - %s</span><br>
<div style="margin-bottom: 24pt;padding: 20pt;"><p style="float: left">Key:</p>
<style type="text/css">.key{display:inline-block;width:3em}a,a:visited{color:#000;text-decoration:none;}</style>
<p style="float: right">Weak&nbsp;
%s
&nbsp;Strong</p></div>
<div style="clear: both;"><br><hr style="border-style: dashed;border-color: #666;width: 60%%;"><br></div>
<center>
%s
</center></body></html>
        """ % (", ".join(decks), "".join(chart), table)


    def savehtml(self):

        fileName = QFileDialog.getSaveFileName(self.win, "Save Page", QDesktopServices.storageLocation(QDesktopServices.DesktopLocation), "Web Page (*.html *.htm)")
        if fileName != "":
            decks = []
            for i in range(self.decklist.count()):
                item = self.decklist.item(i)

                if item.checkState():
                    decks.append(self.options['decks'][item.text()]['id'])
            
            self.scan = KanjiStats(decks,nrev=self.options['rev_strength'])
            self.scan.generate()

            mw.progress.start(immediate=True)
            if not ".htm" in fileName:
                fileName += ".html"
            fileOut = codecs.open(fileName, 'w', 'utf-8')
            self.generate(save=True)
            fileOut.write(self.html)
            fileOut.close()
            mw.progress.finish()
            showInfo("Page saved to %s!" % os.path.abspath(fileOut.name))
        return


    def savepng(self):
        fileName = QFileDialog.getSaveFileName(self.win, "Save Page", QDesktopServices.storageLocation(QDesktopServices.DesktopLocation), "Portable Network Graphics (*.png)")
        if fileName != "":
            mw.progress.start(immediate=True)
            if not ".png" in fileName:
                fileName += ".png"
            p = self.web.page()
            oldsize = p.viewportSize()
            p.setViewportSize(p.mainFrame().contentsSize())
            image = QImage(p.viewportSize(), QImage.Format_ARGB32)
            painter = QPainter(image)
            p.mainFrame().render(painter)
            painter.end()
            image.save(fileName, "png")
            p.setViewportSize(oldsize)
            mw.progress.finish()
            showInfo("Image saved to %s!" % os.path.abspath(fileName))
        return

    def display_grid(self):
        self.generate()

        self.win = QDialog(mw)
        self.web = AnkiWebView()
        vl = QVBoxLayout()
        vl.setMargin(0)
        vl.addWidget(self.web)
        self.web.stdHtml(self.html)
        hl = QHBoxLayout()
        vl.addLayout(hl)
        sh = QPushButton("Save HTML")
        sh.connect(sh, SIGNAL("clicked()"), self.savehtml)        
        sp = QPushButton("Save Image")
        sp.connect(sp, SIGNAL("clicked()"), self.savepng)        
        bb = QPushButton("Close")
        bb.connect(bb, SIGNAL("clicked()"), self.win, SLOT("reject()"))
        hl.addWidget(sh)
        hl.addWidget(sp)
        hl.addWidget(bb)
        
        self.win.setLayout(vl)
        self.win.resize(500,400)
        return 0
        
        


    def html_for_tier(self, save=False):
        table = ""
        for t in xrange(0,self.default_sets.num_tiers()):
            tier = self.default_sets.get_tier(t)
            name = tier.keys()[0]
            chars = tier.values()[0]

            count = 0
            found_chars = []
            cols = int(self.options['cols_export'] if save else self.options['cols_table'])
            table += '<h2 style="color:#888;">%s</h2>{stats}<table width="85%%"><tr>' % name
            total = len(chars)

            for char in chars:

                if count % cols == 0 and count != 0:
                    table += '</tr><tr>'

                if char in self.scan.kanji.keys():
                    stats = self.scan.kanji[char]
                    bgcolor = hsvrgbstr(self.scan.kanji[char]['strength']) if self.scan.kanji[char]['strength'] > 0 else '#ffffff'
                    tooltip =  "Character: %s | Cards: %s | Reviews: %s | First Rep: %s | " % (
                        char, 
                        stats['count'], 
                        stats['reviews'], 
                        stats['first']
                    )
                    tooltip += "Last Rep: %s | Reviews Passed: %s | Reviews Failed: %s | Pass Rate: %s | Time: %s" % (
                        stats['last'], 
                        stats['pass'], 
                        stats['fail'],
                        stats['rate'],
                        stats['time']
                    )
                    table += '<td align="center" valign="top" style="background:%s;white-space: pre-line;" title="%s"><a href="https://jisho.org/kanji/details/%s">%s</a></td>' % (bgcolor, tooltip, char, char)

                    # Remove kanji from datasets
                    found_chars.append(char)
                    del self.scan.kanji[char]
                    count += 1

            found = count
            table += '</tr></table><br><details><summary>Missing Kanji</summary><table style="max-width:75%;"><tr>'
            count = 0
            missing = set(chars).difference(found_chars)

            for char in missing:

                if count % cols == 0 and count != 0:
                    table += "</tr><tr>"

                table += '<td align="center" valign="top" style="background:#EEE;color:#FFF;" title="Character: %s">' % char
                table += '<a href="https://jisho.org/kanji/details/%s" style="color:#888;">%s</a></td>' % (char, char)
                count += 1

            if count == 0:
                table += '<strong style="color:#CCC">None</strong>'
            
            table += "</td></table></details>"
            table = table.replace("{stats}", '<h4 style="color:#888;">%d of %d - %0.2f%%</h4>' % (found, total, (found*100.0)/total))


        additional = self.scan.kanji.keys()
        count = 0
        if len(additional):
            table += '<h2 style="color:#888;">Additional Kanji</h2>{stats}<table width="85%"><tr>'

            for char in additional:

                if count % cols == 0 and count != 0:
                    table += '</tr><tr>'

                stats = self.scan.kanji[char]
                bgcolor = hsvrgbstr(self.scan.kanji[char]['strength']) if self.scan.kanji[char]['strength'] > 0 else '#ffffff'
                tooltip =  "Character: %s | Cards: %s | Reviews: %s | First Rep: %s | " % (
                    char, 
                    stats['count'], 
                    stats['reviews'], 
                    stats['first']
                )
                tooltip += "Last Rep: %s | Reviews Passed: %s | Reviews Failed: %s | Pass Rate: %s | Time: %s" % (
                    stats['last'], 
                    stats['pass'], 
                    stats['fail'],
                    stats['rate'],
                    stats['time']
                )
                table += '<td align="center" valign="top" style="background:%s;white-space: pre-line;" title="%s"><a href="https://jisho.org/kanji/details/%s">%s</a></td>' % (bgcolor, tooltip, char, char)

                count += 1

            table += '</tr></table>'
            table = table.replace('{stats}', '<h4 style="color:#888;">%d</h4>' % len(additional))


        return table



def hsvrgbstr(h, s=0.8, v=0.9):
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0: return "#%0.2X%0.2X%0.2X" % (v*256,t*256,p*256)
    if i == 1: return "#%0.2X%0.2X%0.2X" % (q*256,v*256,p*256)
    if i == 2: return "#%0.2X%0.2X%0.2X" % (p*256,v*256,t*256)
    if i == 3: return "#%0.2X%0.2X%0.2X" % (p*256,q*256,v*256)
    if i == 4: return "#%0.2X%0.2X%0.2X" % (t*256,p*256,v*256)
    if i == 5: return "#%0.2X%0.2X%0.2X" % (v*256,p*256,q*256)
