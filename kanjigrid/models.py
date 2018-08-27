import os,re,random
from aqt import mw
from aqt.qt import *
from anki.utils import ids2str

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

    def __init__(self, mw, cfg_path=UI_PATH, cfg_defaults=UI_DEFAULTS, default_sets=DEFAULT_SETS, custom_sets=CUSTOM_SETS):

        self.config_action = QAction("Generate Kanji Grid 2", mw)
        mw.connect(self.config_action, SIGNAL("triggered()"), self.setup)
        mw.form.menuTools.addAction(self.config_action)
        menu = mw.form.menuTools.addMenu("Kanji Grid")

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
            #TODO: Show grid
            mw.progress.finish()


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
