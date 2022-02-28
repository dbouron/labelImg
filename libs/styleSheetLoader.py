import sys
from libs.ustr import ustr

try:
    from PyQt5.QtCore import *
except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtCore import *

class StyleSheetLoader(object):
    @classmethod
    def load_style_sheet(cls, path):
        ret = None
        f = QFile(f":/qss/{path}")
        if f.exists():
            if f.open(QIODevice.ReadOnly | QFile.Text):
                text = QTextStream(f)
                text.setCodec("UTF-8")
                ret = text.readAll()
            f.close()
        return ret