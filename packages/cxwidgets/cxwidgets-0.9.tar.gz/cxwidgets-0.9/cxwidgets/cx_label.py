from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
from cxwidgets.aQt.QtWidgets import QLabel
import pycx4.qcda as cda
from .menus.general_cm import CXGeneralCM


class CXIntLabel(QLabel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.context_menu = None
        if self.chan is None:
            self.setText('No cname')

    def contextMenuEvent(self, event):
        self.context_menu = CXGeneralCM(self)
        self.context_menu.popup(event.globalPos())

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.IChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        self.setText(str(chan.val))

    @pyqtSlot(float)
    def setCname(self, cname):
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = pyqtProperty(str, getCname, setCname)


class CXDoubleLabel(CXIntLabel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._decimals = 0 # init stored
        self.decimals = 3 # default value

    def cs_update(self, chan):
        self.setText(format(chan.val, self.format_spec))

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    def setDecimals(self, n: int):
        self._decimals = n
        self.format_spec = '.' + str(self._decimals) + 'f'

    def getDecimals(self) -> int:
        return self._decimals

    decimals = pyqtProperty(int, getDecimals, setDecimals)


class CXStrLabel(QLabel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._cname = kwargs.get('cname', None)
        self._max_len = kwargs.get('max_len', 100)
        self.chan = None
        self.cx_connect()
        self.context_menu = None
        if self.chan is None:
            self.setText('No cname')

    def contextMenuEvent(self, event):
        self.context_menu = CXGeneralCM(self)
        self.context_menu.popup(event.globalPos())

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.StrChan(self._cname, private=True, max_nelems=self._max_len, on_update=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        self.setText(str(chan.val))

    @pyqtSlot(float)
    def setCname(self, cname):
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = pyqtProperty(str, getCname, setCname)

    @pyqtSlot(float)
    def set_max_len(self, max_len):
        self._max_len = max_len
        self.cx_connect()

    def get_max_len(self):
        return self._max_len

    max_len = pyqtProperty(int, get_max_len, set_max_len)