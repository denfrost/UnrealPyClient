#import unreal
import sys
import sys

from PySide2 import QtWidgets, QtCore, QtGui


print("Start")
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()



class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(800, 400)
        self.setWindowTitle("Unreal Websocket Client")

    @QtCore.Slot()
    def shoot(self):
     print("Call Func!")

window = QtWidgets.QWidget()
window.resize(800, 400)
window.setWindowTitle("Unreal Websocket Client")

quit = QtWidgets.QPushButton("Quit", window)
quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
quit.setGeometry(370, 350, 100, 40)
QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),
                       app, QtCore.SLOT("quit()"))

Command = QtWidgets.QPushButton("Send Command", window)
Command.setGeometry(10, 10, 200, 40)
Command.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
QtCore.QObject.connect(Command, QtCore.SIGNAL("clicked()"),
                       app, QtCore.SLOT("MyWidget.shoot()"))

LineEdit = QtWidgets.QLineEdit('Localhost',window)
LineEdit.setGeometry(230, 10, 200, 40)
LineEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))

Command = QtWidgets.QLabel("Command Body Json", window)
Command.setGeometry(10, 50, 160, 20)
Command.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))

TextEdit = QtWidgets.QTextEdit('Json Request',window)
TextEdit.setGeometry(10, 70, 350, 200)
TextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))

TextEdit = QtWidgets.QTextEdit('Feedback from server',window)
TextEdit.setGeometry(400, 70, 350, 200)
TextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))

window.show()
sys.exit(app.exec_())

