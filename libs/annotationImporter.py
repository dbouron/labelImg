import sys
import traceback

try:
    from PyQt5.QtCore import QRunnable
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtCore import *

from libs.pascal_voc_io import PascalVocReader
from libs.yolo_io import YoloReader
from libs.create_ml_io import CreateMLReader
from libs.labelFile import LabelFileFormat
from libs.utils import read_image
from libs.annotationSignals import AnnotationSignals
from libs.lockedCounter import LockedCounter

class AnnotationImporter(QRunnable):
    def __init__(self, img, annotation_file, label_file_format, annotation_count):
        super().__init__()
        self.img = img
        self.annotation_file = annotation_file
        self.label_file_format = label_file_format
        self.signals = AnnotationSignals()
        self.annotation_count = annotation_count

    def run(self):
        try:
            if self.label_file_format == LabelFileFormat.PASCAL_VOC:
                t_voc_parse_reader = PascalVocReader(self.annotation_file)
                shapes = t_voc_parse_reader.get_shapes()
            elif self.label_file_format == LabelFileFormat.YOLO:
                image = read_image(self.img, None)
                t_yolo_parse_reader = YoloReader(self.annotation_file, image)
                shapes = t_yolo_parse_reader.get_shapes()
            else:
                t_ml_parse_reader = CreateMLReader(self.annotation_file)
                shapes = t_ml_parse_reader.get_shapes()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit((self.img, shapes))
        finally:
            self.signals.progress.emit((LockedCounter.get_and_inc() + 1) / self.annotation_count * 100)
            self.signals.finished.emit()