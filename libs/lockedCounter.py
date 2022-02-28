try:
    from PyQt5.QtCore import QMutex
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtCore import *

class LockedCounter(object):
    __counter = 0
    __mutex = QMutex()

    pass


    @classmethod
    def __safe_get_and_process(cls, fn):
        cls.__mutex.lock()
        ret = cls.__counter
        cls.__counter = fn(cls.__counter)
        cls.__mutex.unlock()
        return ret

    @staticmethod
    def get():
        return LockedCounter.__safe_get_and_process(lambda x: x)

    @staticmethod
    def get_and_inc():
        return LockedCounter.__safe_get_and_process(lambda x: x + 1)

    @staticmethod
    def get_and_dec():
        return LockedCounter.__safe_get_and_process(lambda x: x - 1)

    @staticmethod
    def reset():
        __counter = 0