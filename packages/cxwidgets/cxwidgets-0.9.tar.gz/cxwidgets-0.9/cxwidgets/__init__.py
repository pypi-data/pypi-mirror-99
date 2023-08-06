from .auxwidgets import HLine, VLine, BaseGridW, BaseFrameGridW
from .pcheckbox import PCheckBox
from .pcombobox import PComboBox
from .pdoublespinbox import PDoubleSpinBox
from .plcdnumber import PLCDNumber
from .pspinbox import PSpinBox
from .pledwidget import LedWidget
from .pswitch import PSwitch

from .cx_doublespinbox import CXDoubleSpinBox
from .cx_spinbox import CXSpinBox
from .cx_lcdnumber import CXLCDNumber
from .cx_checkbox import CXCheckBox
from .cx_combobox import CXTextComboBox, CXIntComboBox
from .cx_pushbutton import CXPushButton
from .cx_lineedit import CXLineEdit
from .cx_progressbar import CXProgressBar
from .cx_switch import CXSwitch, CXDevSwitch
from .cx_label import CXIntLabel, CXDoubleLabel, CXStrLabel
from .cx_led import CXEventLed, CXStateLed

# colors from bolkhov's apps
#FFC0CB  - red
#EDED6D  - yellow
#0000FF  - wierd
#4682B4  - old
#B03060  - hardware problem
#8B8B00  - software problem
#FFA500  - changed by other op
#C0E6E6  - data never read
#00FF00  - alarm just gone
#D8E3D5  - was changed programmatically
#404040  - not found


from .cx_bpm_plot import BPMWidget, K500BPMWidget

from .cx_plot import CXProcPlot, CXPlotDataItem, CXScrollPlotDataItem

__all__ = [HLine, VLine, BaseGridW, BaseFrameGridW, PCheckBox, PComboBox, PDoubleSpinBox, PLCDNumber,
           PSpinBox, LedWidget, PSwitch,
           CXCheckBox, CXTextComboBox, CXIntComboBox, CXDoubleSpinBox, CXLCDNumber, CXLineEdit, CXProgressBar,
           CXPushButton, CXSpinBox, BPMWidget, K500BPMWidget,
           CXSwitch, CXDevSwitch, CXEventLed, CXStateLed,
           CXIntLabel, CXDoubleLabel, CXStrLabel,
           CXProcPlot, CXPlotDataItem, CXScrollPlotDataItem
           ]

