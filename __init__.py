# NOTE: Add the support directory to the sys path so 
# that dependency modules can be imported
import os,sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "support"))


from .gui.configurator import Configurator
from .gui.kanjigrid import KanjiGrid
from .gui.launcher import Launcher

from aqt import mw
from aqt.qt import QAction

mw.kanjigrid = {
    'configure': Configurator(mw),
    'kanjigrid': KanjiGrid(mw),
    'launcher':  Launcher(mw),
}


launch_action = QAction(mw)
launch_action.setText("Generate Kanji Grid")
mw.form.menuTools.addAction(launch_action)
launch_action.triggered.connect(mw.kanjigrid['launcher'].show)
