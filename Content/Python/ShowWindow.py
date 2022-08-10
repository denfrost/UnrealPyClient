import unreal
import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        @QtCore.Slot()
        def MyQuit():
            app.quit()

        QtWidgets.QWidget.__init__(self, parent)
        self.resize(300, 300)
        self.setWindowTitle("Unreal Window")

if __name__ == "__main__":
    print("Start Py App")
if "unreal" not in dir():
    print("Warning: Unreal modules Not Loaded!")
    print('Main Dir program: '+os.getcwd())
    Loaded = True
else:
    unreal.log("Unreal modules Loaded & Ready!")
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()
widget = MyWidget()
widget.show()

if app:
    sys.exit(app.exec_())  # for Windows external launch
unreal.parent_external_window_to_slate(widget.winId())
