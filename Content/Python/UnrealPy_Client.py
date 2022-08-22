#import unreal
import sys
import json
import os
from datetime import datetime as dt
#My Library
import UtilObserver as uo
import settings

#pip install PySide2
from PySide2 import *
from PySide2.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QInputDialog
from PySide2.QtWidgets import *

#pip install websocket-client
from websocket import create_connection

#perforce vars setting

#describe calls checking umap, uasset.
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
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_update_perforce",
                "parameters": {
                "result" : 'return string'
                }
            }
        }
    }


Server = "ws://"+"localhost:30020"

Json_RequestGetAllShots = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_get_all_shots",
                "parameters": {
                "result" : 'return string'
                }
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
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_set_shot",
                "parameters": {
                "bPar" : True,
                "sMapName" : 'SH0005',
                "sSeqName" : 'SH0005',
                "sShotName" : 'SH0005'
                }
            }
        }
    }

Json_RequestRenderImages = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_render_images",
                "parameters": {
                "sSeqName" : 'SH0005',
                "iQualityPreset" : 3,
                }
            }
        }
    }

#Important!
#Undependency Memory PayLoad 22.05.2022 dcan migrate all principal to this methods
Json_RequestRemoteStaticFunction = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "python_test_bp_action_return",
                "parameters": {
                "result" : 'return string'
                }
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

class input_dialog(QWidget):
    def __init__(self, parent=None):
        super(input_dialog, self).__init__(parent)

        layout = QFormLayout()
        self.lbl = QLabel("Profile Name")
        Name = settings.get_Settings_field('Name')
        self.le = QLineEdit(Name)
        layout.addRow(self.lbl, self.le)

        self.lbl1 = QLabel("User")
        User = settings.get_Settings_field('User')
        self.le1 = QLineEdit(User)
        layout.addRow(self.lbl1, self.le1)

        self.lbl2 = QLabel("Password")
        Pwd = settings.get_Settings_field('Pwd')
        self.le2 = QLineEdit(Pwd)
        layout.addRow(self.lbl2, self.le2)

        self.lbl3 = QLabel("Host")
        Host = settings.get_Settings_field('Host')
        self.le3 = QLineEdit(Host)
        layout.addRow(self.lbl3, self.le3)

        self.lbl4 = QLabel("Depot")
        Depot = settings.get_Settings_field('Depot')
        self.le4 = QLineEdit(Depot)
        layout.addRow(self.lbl4, self.le4)

        self.lbl5 = QLabel("Workspace")
        Workspace = settings.get_Settings_field('Workspace')
        self.le5 = QLineEdit(Workspace)
        layout.addRow(self.lbl5, self.le5)

        self.btn6 = QPushButton("Save")
        self.btn6.clicked.connect(self.saveProfile)
        self.btn7 = QPushButton("Cancel")
        self.btn7.clicked.connect(self.dlg_quit)
        layout.addRow(self.btn6, self.btn7)

        self.setLayout(layout)
        self.setWindowTitle('Settings Perforce')
        self.resize(350, 200)

    def saveProfile(self):
        list = {'Name': self.le.text(), 'User': self.le1.text(), "Pwd": self.le2.text(), 'Host': self.le3.text(), 'Depot': self.le4.text(), 'Workspace': self.le5.text()}
        settings.rewrite_exist_profile(list)

    def dlg_quit(self):
        self.close()

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
            print("Got Server Answer : Getallshots")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            FillShots(feedback)
            progressBar.setValue(100)

        def ServerAnsweredSetShotRender(feedback):
            StatusLabel.setText("Unreal Server Status Online : " + HostServer)
            print("Got Server Answer : SetShotRender")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredImagesRender(feedback):
            StatusLabel.setText("Unreal Server Status Online : " + HostServer)
            print("Got Server Answer : ImagesRenderTool")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredPerforce(feedback):
            StatusLabel.setText("Unreal Server Status Online : " + HostServer)
            print("Got Server Answer : Try Update server")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            PerforceLabel.setText("Perforce Updated : "+tanswer)
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
            tabwidget.setCurrentIndex(0)
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
            listing.clear()
            print('Start Sorting:')
            for i, name in enumerate(res):
                #print('Feedback ['+str(i)+']: '+res[i])
                if res[i].find('_SEQ') > 0: #_ANIM_SEQ
                    comboBox.addItem("" + res[i])
                    listing.addItem("" + res[i])
            listing.setMaximumHeight(200)

        def printItemText(self):
            items = listing.selectedItems()
            x = []
            for i in range(len(items)):
                x.append(str(listing.selectedItems()[i].text()))
            print(x)

        def MakeRenderTool(sequence):
            print("Make Render "+sequence)
            pathbatch ="MakeShotRenderArg.bat"

            opers = sequence
            index = opers.find('_SEQ.')
            argument_Umap = opers[:index]
            print(index)
            print(argument_Umap)

            index = opers.find('"')
            if index == -1 :
                argument_Seq = sequence
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
            tabwidget.setCurrentIndex(0)
            print("SetShotRender ")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestSetShotRender), ServerAnsweredSetShotRender)

        def MakeImagesTool(sequence, iQualityPreset=3, bFtp_transfer=True):
            print('Send Render for ImagesTool Render : '+sequence + ' Quality - '+str(iQualityPreset)+' Ftp transfer - '+str(bFtp_transfer))
            Json_RequestRenderImages["Parameters"]["Body"]["parameters"]["sSeqName"] = sequence
            Json_RequestRenderImages["Parameters"]["Body"]["parameters"]["iQuality"] = iQualityPreset
            Json_RequestRenderImages["Parameters"]["Body"]["parameters"]["bFtp_transfer"] = bFtp_transfer
            progressBar.setValue(0)
            JsonTextEdit.setText(json.dumps(Json_RequestRenderImages))
            tabwidget.setCurrentIndex(0)
            print("Sending....")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestRenderImages), ServerAnsweredImagesRender)

        @QtCore.Slot()
        def RenderImages():
            MakeImagesTool(comboBox.currentText(), comboBoxQ.currentIndex(), CheckTransferToggleBtn.isChecked())
        @QtCore.Slot()
        def RenderMovie(): #arguments
            MakeRenderTool(comboBox.currentText())

        @QtCore.Slot()
        def BatchRenderMovie(): #arguments
            items = listing.selectedItems()
            for i in range(len(items)):
                MakeRenderTool(listing.selectedItems()[i].text())

        @QtCore.Slot()
        def ClearAnswer():
            ServerAnswerTextEdit.clear()

        @QtCore.Slot()
        def CheckServer():
            try:
                progressBar.setValue(0)
                create_connection(HostLineEdit.text(), 5)
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
        def onClickedToggleTransfer():
            print('Set Ftp transfer : '+str(CheckTransferToggleBtn.isChecked()))

        @QtCore.Slot()
        def onOpenFolder():
            print('Open image folder')

        @QtCore.Slot()
        def UpdatePerforce():
            print("Perforce ")
            progressBar.setValue(0)
            JsonTextEdit.setText(json.dumps(Json_UpdatePerforce))
            tabwidget.setCurrentIndex(0)
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_UpdatePerforce), ServerAnsweredPerforce)

        @QtCore.Slot()
        def SetPerforceProfile():
            ex = input_dialog()
            ex.show()
            ex.exec_()

        @QtCore.Slot()
        def ShowDialogs():
            items = ("C", "C++", "Java", "Python")
            item, ok = QInputDialog.getItem(self, "select input dialog", "list of languages", items, 0, False)

            dlg = QDialog(self)
            dlg.resize(400, 400)
            dlg.setWindowTitle("Settings Perforce")
            dlg.exec_()


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


        Groupbox = QtWidgets.QGroupBox("Server Status")
        Groupbox.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
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
        GroupboxCommand.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        vbox2 = QtWidgets.QVBoxLayout()
        GroupboxCommand.setLayout(vbox2)
        layout.addWidget(GroupboxCommand)

        Command = QtWidgets.QPushButton("Send Command")
        Command.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(Command, QtCore.SIGNAL("clicked()"), SendCommand)
        GroupboxCommand.layout().addWidget(Command)

        JsonTextEdit = QtWidgets.QTextEdit(json.dumps(Json_RequestRemoteStaticFunction))
        JsonTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(JsonTextEdit)

        ServerAnswerTextEdit = QtWidgets.QTextEdit('Feedback from server')
        ServerAnswerTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layout.addWidget(ServerAnswerTextEdit)

        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(JsonTextEdit, "Command Client")
        tabwidget.addTab(ServerAnswerTextEdit, "Answer Server")
        GroupboxCommand.layout().addWidget(tabwidget)


        GroupboxAuto = QtWidgets.QGroupBox("Rendering Shots")
        GroupboxAuto.setChecked(True)
        vbox3 = QtWidgets.QHBoxLayout()
        GroupboxAuto.setLayout(vbox3)

        getshot = QtWidgets.QPushButton("Get Server Sequences")
        getshot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(getshot, QtCore.SIGNAL("clicked()"), GetAllServerShots)
        GroupboxAuto.layout().addWidget(getshot)

        render = QtWidgets.QPushButton("Render Movie Sequence")
        render.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(render, QtCore.SIGNAL("clicked()"), RenderMovie)
        GroupboxAuto.layout().addWidget(render)

        render_images = QtWidgets.QPushButton("Render Images Sequence")
        render_images.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(render_images, QtCore.SIGNAL("clicked()"), RenderImages)
        GroupboxAuto.layout().addWidget(render_images)

        GroupboxAuto5 = QtWidgets.QGroupBox("Rendering Settings")
        GroupboxAuto5.setChecked(True)
        vbox4 = QtWidgets.QHBoxLayout()
        GroupboxAuto5.setLayout(vbox4)

        preset = QtWidgets.QLabel("Quality")
        GroupboxAuto5.layout().addWidget(preset)
        comboBoxQ = QtWidgets.QComboBox(self)
        comboBoxQ.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBoxQ.addItem("Preset01")
        comboBoxQ.addItem("Preset02VeryLow")
        comboBoxQ.addItem("Preset02LoW")
        comboBoxQ.addItem("Preset03VeryHigh")
        comboBoxQ.setCurrentIndex(3)
        GroupboxAuto5.layout().addWidget(comboBoxQ)

        CheckTransferToggleBtn = QtWidgets.QCheckBox("Transfer")
        CheckTransferToggleBtn.setChecked(True)
        self.connect(CheckTransferToggleBtn, QtCore.SIGNAL("clicked()"), onClickedToggleTransfer)
        GroupboxAuto5.layout().addWidget(CheckTransferToggleBtn)

        OpenFolderBtn = QtWidgets.QPushButton("Open Folder..")
        OpenFolderBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(OpenFolderBtn, QtCore.SIGNAL("clicked()"), onOpenFolder)
        GroupboxAuto5.layout().addWidget(OpenFolderBtn)

        GroupboxAuto0 = QtWidgets.QGroupBox("Found Sequences")
        GroupboxAuto0.setChecked(True)
        vbox31 = QtWidgets.QHBoxLayout()
        GroupboxAuto0.setLayout(vbox31)

        comboBox = QtWidgets.QComboBox(self)
        comboBox.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBox.addItem("EMPTY")
        GroupboxAuto0.layout().addWidget(comboBox)

        GroupboxAuto2 = QtWidgets.QGroupBox("Perforce")
        vbox4 = QtWidgets.QHBoxLayout()
        GroupboxAuto2.setLayout(vbox4)

        PerforceLabel = QtWidgets.QLabel("Perforce Time updated :")
        PerforceLabel.setGeometry(10, 50, 160, 20)
        PerforceLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        GroupboxAuto2.layout().addWidget(PerforceLabel)

        SetPerforceBtn = QtWidgets.QPushButton("Settings")
        SetPerforceBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(SetPerforceBtn, QtCore.SIGNAL("clicked()"),SetPerforceProfile)
        GroupboxAuto2.layout().addWidget(SetPerforceBtn)


        UpdatePerforceBtn = QtWidgets.QPushButton("Update Perforce")
        UpdatePerforceBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(UpdatePerforceBtn, QtCore.SIGNAL("clicked()"),UpdatePerforce)
        GroupboxAuto2.layout().addWidget(UpdatePerforceBtn)


        GroupboxAuto3 = QtWidgets.QGroupBox("Batch Mode Rendering [Warning: Will Heavy busy server!]")
        GroupboxAuto3.setChecked(True)
        vbox5 = QtWidgets.QVBoxLayout()
        GroupboxAuto3.setLayout(vbox5)
        listing = QtWidgets.QListWidget()
        listing.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Medium))
        listing.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        item = QtWidgets.QListWidgetItem("empty")
        listing.addItem(item)

        listing.itemClicked.connect(printItemText)
        GroupboxAuto3.layout().addWidget(listing)
        BatchRenderBtn = QtWidgets.QPushButton("Start Batch Rendering")
        BatchRenderBtn.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Bold))
        self.connect(BatchRenderBtn, QtCore.SIGNAL("clicked()"), BatchRenderMovie)
        GroupboxAuto3.layout().addWidget(BatchRenderBtn)



        GroupboxMain = QtWidgets.QGroupBox("SERVER: Automation Pipeline")
        GroupboxMain.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        vbox5 = QtWidgets.QVBoxLayout()
        GroupboxMain.setLayout(vbox5)
        GroupboxMain.layout().addWidget(GroupboxAuto)
        GroupboxMain.layout().addWidget(GroupboxAuto5)
        GroupboxMain.layout().addWidget(GroupboxAuto0)

        GroupboxMain.layout().addWidget(GroupboxAuto2)
        GroupboxMain.layout().addWidget(GroupboxAuto3)
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

def unreal_working_dirs():
    print('main dir program')
    prog_dir = unreal.Paths.project_plugins_dir() + 'UnrealPyClient'
    print('Plugin UnrealPyClient Directory: ' + prog_dir)
    root_dir = unreal.Paths.root_dir()
    project_dir = unreal.Paths.project_dir()
    video_capture_dir = unreal.Paths.video_capture_dir()
    project_persistent_download_dir = unreal.Paths.project_persistent_download_dir()
    print('extend dirs...')
    print('Root Directory: ' + root_dir)
    print('Project Directory: ' + project_dir)
    print('Video Capture Directory: ' + video_capture_dir)
    print('Project Download Directory: ' + project_persistent_download_dir)


if __name__ == "__main__":
    print("Start Py App")
if "unreal" not in dir():
    print("Warning: Unreal modules Not Loaded!")
    print('Main Dir program: '+os.getcwd())
    Loaded = True
else:
    unreal.log("Unreal modules Loaded & Ready!")
    unreal_working_dirs()
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()
widget = MyWidget()
widget.show()
print("Py App checking server...")
if app:
    sys.exit(app.exec_())  # for Windows external launch
if "unreal" in dir():
    import unreal
    unreal.parent_external_window_to_slate(widget.winId())

