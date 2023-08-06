from cxwidgets.aQt.QtWidgets import QPushButton
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda
from .common_mixin import CommonMixin


class CXPushButton(QPushButton, CommonMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.cs_send)

    # def cx_connect(self):
    #     if self._cname == '':
    #         self.chan = None
    #         return
    #     self.chan = cda.IChan(self._cname, private=True, on_update=True)

    @pyqtSlot()
    def cs_send(self):
        if self.chan is None:
            return
        self.chan.setValue(1)


