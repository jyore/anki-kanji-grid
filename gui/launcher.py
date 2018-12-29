
from aqt.qt import *
from .base import Dialog
from ..kanji import KanjiSets


class Launcher(Dialog):

    def __init__(self, mw):
        self.mw = mw
        self.sets = KanjiSets()
        super(Launcher, self).__init__("Generate", self.mw)


    def ui(self):
        layout = super(Launcher, self).ui()
        layout.addLayout(self.panel())
        layout.addWidget(self.ui_buttons())

        return layout


    def panel(self):
        layout = QGridLayout()
        self.group_by = QComboBox()


        # row 0:
        layout.addWidget(QLabel("Group Results By:"), 0, 0, 1, 2)
        layout.addWidget(self.group_by, 0, 2, 1, 6)

        return layout



    def show(self):
        self.sets.load()        

        self.group_by.clear()
        self.group_by.addItems(self.sets.set_names())
        super(Launcher, self).show()


    def accept(self):
        self.mw.kanjigrid['kanjigrid'].show(self.group_by.currentText())
        super(Launcher, self).accept()
