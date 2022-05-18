#import unreal
import datetime
import sys
import json
import os
from datetime import datetime as dt
#My Library
import UtilObserver as uo


#pip install PySide2
from PySide2 import QtWidgets, QtCore, QtGui

#pip install websocket-client
from websocket import create_connection
Json_RequestCheckMap =\
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/describe",
        "Verb": "PUT",
        "Body": {
            "ObjectPath": "/Game/Remote/Test1.Test1",
        }
    }
    }

Json_UpdatePerforce = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/Test1.Test1:PersistentLevel.Remoter_2",
                "functionName": "UpdatePerforce"
            }
        }
    }


Server = "ws://"+"10.66.7.80:30020"

Json_RequestGetAllShots = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/Test1.Test1:PersistentLevel.Remoter_2",
                "functionName": "GetAllShots",
            }
        }
    }

Json_RequestSetShotRender = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/Test1.Test1:PersistentLevel.Remoter_2",
                "functionName": "SetShot",
                "parameters": {
                "bPar" : True,
                "sMapName" : 'SH0005',
                "sSeqName" : 'SH0005',
                "sShotName" : 'SH0005'
                }
            }
        }
    }

Json_RequestStaticFunction = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/BPL_Remote.BPL_Remote",
                "functionName": "HelloWorld",
                "parameters": {
                "bPar" : True,
                "sShotName" : 'SH0005'
                }
            }
        }
    }

Json_RequestDescribeTest =\
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/describe",
        "Verb": "PUT",
        "Body": {
            "ObjectPath": "/Game/Remote/Test.Test:PersistentLevel.NewBlueprint_2",
        }
    }
    }

Json_RequestDescribe =\
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/describe",
        "Verb": "PUT",
        "Body": {
            "ObjectPath": "/Game/Remote/Test.Test",
        }
    }
    }

Json_RequestDescribeUtil =\
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/describe",
        "Verb": "PUT",
        "Body": {
            "ObjectPath": "/Game/Remote/EditUtilityWP/EUW_Test.EUW_Test",
        }
    }
    }


Json_RequestStaticFunctionHelloWorld = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/BPL_Remote.BPL_Remote",
                "functionName": "HelloWorld"
            }
        }
    }

Json_RequestObjectCallTest = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Game/Remote/Test.Test:PersistentLevel.NewBlueprint_2",
                "functionName": "CallTest",
                "parameters": {
                    "sString": 'Call Test Succes'
                }
            }
        }
    }

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):

        @QtCore.Slot()
        def SendCommand():
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, JsonTextEdit.toPlainText(), ServerAnswered) #Send Json to Unreal

        def ServerAnswered(feedback):
            StatusLabel.setText("Unreal Server Status Online : " + HostServer)
            print("Got Server Answer")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredGetAllShots(feedback):
            StatusLabel.setText("Unreal Server Status Online : " + HostServer)
            print("Got Server Answer")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            FillShots(feedback)
            progressBar.setValue(100)

        def ServerAnsweredSetShotRender(feedback):
            StatusLabel.setText("Unreal Server Status Online : " + HostServer)
            print("Got Server Answer")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            FillShots(feedback)
            progressBar.setValue(100)

        @QtCore.Slot()
        def StatusUpdate(status):
            StatusLabel.setText("Unreal Server Status "+status)

        @QtCore.Slot()
        def GetUtilObserverShots():
            names = uo.UtilObserver('E:/GIT/ProjectOazis', '/**/*.umap')
            print(len(names))
            comboBox.clear()
            for i, name in enumerate(names):
                comboBox.addItem(""+names[i])

        @QtCore.Slot()
        def GetShots():
            names = "Make sequences list only test!"
            print(len(names))
            comboBox.clear()
            for i, name in enumerate(names):
                comboBox.addItem("" + names[i])

        def ParsedShots(feedback):
            print('Json string : '+feedback)
            res = feedback.replace("\\", '').replace('rnt', '').replace('rn', '').replace('b', '').replace('t"', '"') #clean json string
            json_str = res[2:len(res) - 2]
            print(json_str)
            dict = json.loads(json_str)
            print('Dict:')
            type(dict)
            for key, value in dict.items():
                print(key, ":", value)
            print(dict['ResponseBody'])
            tanswer = dt.now().strftime("%H:%M:%S")
            s1 ='' + json.dumps(dict['ResponseCode'])
            ServerAnswerTextEdit.setText(tanswer + " : " +s1)
            ServerAnswerTextEdit.append(json.dumps(dict['ResponseBody']))

        def GetAllServerShots():
            JsonTextEdit.setText(json.dumps(Json_RequestGetAllShots))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllShots) #Send Json to Unreal


        def FillShots(feedback):
            res = feedback.split(",")
            print(res[1])
            comboBox.clear()
            for i, name in enumerate(res):
                if res[i].find('_SEQ.') > 0:
                    index = res[i].find('"')
                    if index == -1:
                        comboBox.addItem("" + res[i])
                    else:
                        comboBox.addItem("" + res[i][:index])




        @QtCore.Slot()
        def MakeRender(): #arguments
            print("Make Render "+comboBox.currentText())
            pathbatch ="MakeShotRenderArg.bat"

            opers = comboBox.currentText()
            index = opers.find('_SEQ.')
            argument_Umap = opers[:index]
            print(index)
            print(argument_Umap)

            index = opers.find('"')
            if index == -1 :
                argument_Seq = comboBox.currentText()
            else:
                argument_Seq = opers[:index]
            print(index)
            print(argument_Seq)

            index1 = argument_Seq.find('.')
            argument_Shotname = argument_Seq[index1+1:]
            print(argument_Shotname)
            print(index1)
            index2 = argument_Shotname.find('_SEQ')
            print(index2)
            argument_Shotname = argument_Shotname[:index2]
            print(argument_Shotname)
            Json_RequestSetShotRender["Parameters"]["Body"]["parameters"]["sMapName"] = argument_Umap
            Json_RequestSetShotRender["Parameters"]["Body"]["parameters"]["sSeqName"] = argument_Seq
            Json_RequestSetShotRender["Parameters"]["Body"]["parameters"]["sShotName"] = argument_Shotname

            print(Json_RequestSetShotRender["Parameters"]["Body"]["parameters"])
            #os.system(pathbatch+" "+argument_Umap+" "+argument_Seq+" "+argument_Shotname)

            progressBar.setValue(0)
            JsonTextEdit.setText(json.dumps(Json_RequestSetShotRender))
            print("SetShotRender ")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestSetShotRender), ServerAnsweredSetShotRender)


        @QtCore.Slot()
        def ClearAnswer():
            ServerAnswerTextEdit.clear()

        @QtCore.Slot()
        def CheckServer():
            try:
                progressBar.setValue(0)
                create_connection(HostLineEdit.text())
                ChangeStatus(True)
            except:
                ChangeStatus(False)

        @QtCore.Slot()
        def ChangeStatus(check):
            if check:
                StatusLabel.setText("Unreal Server Status Online : " + HostLineEdit.text())
                StatusLabel.setStyleSheet("QLabel { color : green; }")
                progressBar.setValue(100)
            else:
                StatusLabel.setStyleSheet("QLabel { background-color : yellow; color : red; }")
                StatusLabel.setText("Unreal Server Status Offline: Pls start RemoteWebControl")

        @QtCore.Slot()
        def onClickedToggle():
            Check.setEnabled(ServerToggleBtn.isChecked())
            HostLineEdit.setEnabled(ServerToggleBtn.isChecked())

        @QtCore.Slot()
        def UpdatePerforce():
            progressBar.setValue(0)
            JsonTextEdit.setText(json.dumps(Json_UpdatePerforce))
            print("Perforce ")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_UpdatePerforce), ServerAnswered)

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


        Groupbox = QtWidgets.QGroupBox("Server")
        vbox = QtWidgets.QHBoxLayout()
        Groupbox.setLayout(vbox)
        layout.addWidget(Groupbox)


        Check = QtWidgets.QPushButton("Check Server")
        Check.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(Check, QtCore.SIGNAL("clicked()"), CheckServer)
        Groupbox.layout().addWidget(Check)

        HostLineEdit = QtWidgets.QLineEdit('localhost')
        HostLineEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        HostServer = "ws://" + HostLineEdit.text()+":30020"
        HostLineEdit = QtWidgets.QLineEdit(Server)
        Groupbox.layout().addWidget(HostLineEdit)

        ServerToggleBtn = QtWidgets.QCheckBox("Change Server")
        ServerToggleBtn.setChecked(False)
        self.connect(ServerToggleBtn, QtCore.SIGNAL("clicked()"), onClickedToggle)
        Check.setEnabled(ServerToggleBtn.isChecked())
        HostLineEdit.setEnabled(ServerToggleBtn.isChecked())
        Groupbox.layout().addWidget(ServerToggleBtn)

        GroupboxCommand = QtWidgets.QGroupBox("Send Custom Commands")
        vbox2 = QtWidgets.QVBoxLayout()
        GroupboxCommand.setLayout(vbox2)
        layout.addWidget(GroupboxCommand)

        Command = QtWidgets.QPushButton("Send Command")
        Command.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(Command, QtCore.SIGNAL("clicked()"), SendCommand)
        GroupboxCommand.layout().addWidget(Command)

        JsonTextEdit = QtWidgets.QTextEdit(json.dumps(Json_RequestCheckMap))
        JsonTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(JsonTextEdit)

        ServerAnswerTextEdit = QtWidgets.QTextEdit('Feedback from server')
        ServerAnswerTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(ServerAnswerTextEdit)

        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(JsonTextEdit, "Command Client")
        tabwidget.addTab(ServerAnswerTextEdit, "Answer Server")
        GroupboxCommand.layout().addWidget(tabwidget)


        GroupboxAuto = QtWidgets.QGroupBox("Unreal")
        GroupboxAuto.setChecked(True)
        vbox3 = QtWidgets.QHBoxLayout()
        GroupboxAuto.setLayout(vbox3)


        getshot = QtWidgets.QPushButton("Check Server Shots")
        getshot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(getshot, QtCore.SIGNAL("clicked()"), GetAllServerShots)
        GroupboxAuto.layout().addWidget(getshot)

        render = QtWidgets.QPushButton("Start Render Shot")
        render.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(render, QtCore.SIGNAL("clicked()"), MakeRender)
        GroupboxAuto.layout().addWidget(render)

        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItem("EMPTY")
        GroupboxAuto.layout().addWidget(comboBox)

        GroupboxAuto2 = QtWidgets.QGroupBox("Perforce")
        vbox4 = QtWidgets.QHBoxLayout()
        GroupboxAuto2.setLayout(vbox4)

        PerforceLabel = QtWidgets.QLabel("Perforce")
        PerforceLabel.setGeometry(10, 50, 160, 20)
        PerforceLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        GroupboxAuto2.layout().addWidget(PerforceLabel)

        UpdatePerforceBtn = QtWidgets.QPushButton("Start Update Perforce")
        UpdatePerforceBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(UpdatePerforceBtn, QtCore.SIGNAL("clicked()"),UpdatePerforce)
        GroupboxAuto2.layout().addWidget(UpdatePerforceBtn)

        GroupboxMain = QtWidgets.QGroupBox("SERVER: Automation Pipeline")
        vbox5 = QtWidgets.QVBoxLayout()
        GroupboxMain.setLayout(vbox5)
        GroupboxMain.layout().addWidget(GroupboxAuto)

        GroupboxMain.layout().addWidget(GroupboxAuto2)
        layout.addWidget(GroupboxMain)

        progressBar = QtWidgets.QProgressBar(self)
        progressBar.minimum = 0
        progressBar.maximum = 100
        layout.addWidget(progressBar)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"), MyQuit)
        layout.addWidget(quit)

        CheckServer()



def SendSocket(ClearAnswer, HostServer,Json_request, ServerAnswered):
    ws = create_connection(HostServer)
    print("Sending Command to Server : "+HostServer)
    ws.send(Json_request)
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received from Server '%s'" % result)
    server_str = "'%s'" % result
    ServerAnswered(server_str)
    ws.close()

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
#unreal.parent_external_window_to_slate(widget.winId())


