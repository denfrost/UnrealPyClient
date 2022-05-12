import unreal
import sys

from PySide2 import QtWidgets, QtUiTools, QtGui

#Import UE python lib
#import ui.qwidget_import_asset as q_import_asset

# RELOAD MODULE
import importlib

sys.path.append('C:/UE4JOB/M2Animation/SCRIPTS_UNREAL')
sys.path.append('C:/UE4JOB/M2Animation/SCRIPTS_UNREAL/m2_unreal')
sys.path.append('C:/UE4JOB/M2Animation/SCRIPTS_UNREAL/ui')

WINDOW_NAME = 'M2 - Menu'
UI_FILE_FULLNAME = __file__.replace('.py', '.ui')

class QtWindowImport(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWindowImport, self).__init__(parent)
        self.aboutToClose = None  # This is used to stop the tick when the window is closed
        self.widget = QtUiTools.QUiLoader().load(UI_FILE_FULLNAME)
        self.widget.setParent(self)
        self.setWindowTitle(WINDOW_NAME)
        self.setGeometry(100, 100, self.widget.width(), self.widget.height())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)
        
        # importAssetButton
        self.widget.convertToMi.clicked.connect(self.convert_to_mi)



    def convert_to_mi(self):
        #import m2_unreal.convert_to_mi as convert_to_mi
        #importlib.reload(convert_to_mi)
        #convert_to_mi.convert_to_mi()
        print()




app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

widget = QtWindowImport()
widget.show()
unreal.parent_external_window_to_slate(widget.winId())
