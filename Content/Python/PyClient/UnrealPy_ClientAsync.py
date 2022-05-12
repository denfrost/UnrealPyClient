#import unreal
import sys
import json
import asyncio
import websockets

from PySide2 import QtWidgets, QtCore, QtGui

Json_Data = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/Test.Test:PersistentLevel.NewBlueprint_2",
                "functionName": "NewFunction_0"
            }
        }
    }

Server = "ws://localhost:30020"
Online = False
class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):

        @QtCore.Slot()
        def SendCommand():
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            SendSocket(JsonTextEdit.toPlainText(), ServerAnswered) #Send Json to Unreal

        def ServerAnswered(feedback):
            print("Got Server Answer")
            ServerTextEdit.setText(feedback) #JsonTextEdit.toPlainText()

        @QtCore.Slot()
        def StatusUpdate(status):
            StatusLabel.setText("Unreal Server Status "+status)

        @QtCore.Slot()
        def MyQuit():
            app.quit()

        QtWidgets.QWidget.__init__(self, parent)
        self.resize(800, 800)
        self.setWindowTitle("Unreal Websocket Client")

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        StatusLabel = QtWidgets.QLabel("Unreal Server Status:")
        StatusLabel.setGeometry(10, 50, 160, 20)
        StatusLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        StatusLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")
        layout.addWidget(StatusLabel)
        try:
            create_connection(Server)
            StatusLabel.setText("Unreal Server Status Online")
            StatusLabel.setStyleSheet("QLabel { color : green; }")
        except:
            StatusLabel.setStyleSheet("QLabel { background-color : yellow; color : red; }")
            StatusLabel.setText("Unreal Server Status Offline: Pls start RemoteWebControl")
        Command = QtWidgets.QPushButton("Send Command")
        Command.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(Command, QtCore.SIGNAL("clicked()"), SendCommand)
        layout.addWidget(Command)
        LineEdit = QtWidgets.QLineEdit('localhost')
        LineEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(LineEdit)
        JsonLabel = QtWidgets.QLabel("Command Body Json")
        JsonLabel.setGeometry(10, 50, 160, 20)
        JsonLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(JsonLabel)

        JsonTextEdit = QtWidgets.QTextEdit(json.dumps(Json_Data))
        JsonTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(JsonTextEdit)
        ServerTextEdit = QtWidgets.QTextEdit('Feedback from server')
        ServerTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(ServerTextEdit)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"), MyQuit)
        #QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),app, QtCore.SLOT("quit()"))
        layout.addWidget(quit)

from websocket import create_connection

def SendSocket(Json_request, ServerAnswered):
    ws = create_connection(Server)
    print("Sending Command to Server")
    ws.send(Json_request)
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received from Server '%s'" % result)
    server_str = "'%s'" % result
    ServerAnswered(server_str)
    ws.close()

async def ws_endcommand(uri,command):
    async with websockets.connect(uri) as websocket:
        await websocket.send(command)
        await asyncio.sleep(0)
        print(await websocket.recv())  # Starts receive things, not only once

if __name__ == "__main__":
    print("Start Py App")
if "unreal" not in dir():
    print("Warning: Unreal modules Not Loaded!")
    Loaded = True
else:
    unreal.log("Unreal modules ready!");
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()
widget = MyWidget()
widget.show()
print("Py App checking server...")
sys.exit(app.exec_())  # for Windows external launch
unreal.parent_external_window_to_slate(widget.winId())