#import unreal
import sys
import json
import os
from datetime import datetime as dt
#My Library
import UtilObserver as uo
import settings as settings

#pip install PySide2
from PySide2 import *
from PySide2.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QInputDialog
from PySide2.QtWidgets import *

#pip install websocket-client
from websocket import create_connection

import settings as settings

Server = "ws://"+"10.66.7.80:30020"

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

Json_RequestMakeRenderJob = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_make_render_job",
                "parameters": {
                    "sSeqName" : 'SH0005',
                    "sQualityPreset" : '',
                    "result" : 'return string'
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

Json_RequestRemoteQueueJobs = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_get_queue_jobs",
                "parameters": {
                    "result": 'return string'
                }
            }
        }
    }

Json_RequestStartRenderJob = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_start_render_job",
                "parameters": {
                    "sJobName": 'SH0005',
                    "result": 'return string'
                }
            }
        }
    }

Json_RequestDeleteRenderJob = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_delete_render_job",
                "parameters": {
                    "sJobName": 'SH0005',
                    "result": 'return string'
                }
            }
        }
    }

Json_RequestGetRenderPresets = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_get_render_presets",
                "parameters": {
                    "result": 'return string'
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

Json_RequestDeleteAllRenderJobs = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_delete_all_render_jobs",
                "parameters": {
                    "result": 'return string'
                }
            }
        }
    }

#SuperMessage Remote tool
Json_RequestRemoteInfo = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_get_info_remote",
                "parameters": {
                    "result": 'return string'
                }
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
        print(type(list))
        print(list)
        settings.rewrite_exist_profile(list)
        self.close()

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
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredGetAllShots(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : Getallshots")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            FillShots(feedback)
            progressBar.setValue(70)
            #Ask about Rendering Movie  status
            GetRemoteInfo()
            progressBar.setValue(100)

        def ServerAnsweredSetShotRender(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : SetShotRender")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredMakeRenderJob(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : MakeRenderJob")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredPerforce(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : Try Update server")
            tanswer =dt.now().strftime("%H:%M:%S")
            tused = dt.now()-trequest
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            tabwidget.setCurrentIndex(1)
            PerforceLabel.setText("Perforce Updated : "+tanswer + '[' +str(tused) + ']')
            progressBar.setValue(100)

        def ServerAnsweredGetAllQueueJobs(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : GetAllQueueJobs")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            tabwidget.setCurrentIndex(1)
            #Fill Queue Combobox
            FillQueueJobs(feedback)
            comboBoxQueue.setCurrentIndex(0)
            progressBar.setValue(70)
            #Ask about Rendering Movie  status
            GetRemoteInfo()
            progressBar.setValue(100)

        def ServerAnsweredDeleteRenderJob(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : DeleteRenderJob")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(70)
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('DeleteRenderJob Clean Data :'+cleandata)
            progressBar.setValue(100)

        def ServerAnsweredDeleteAllRenderJobs(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : DeleteAllRenderJobs")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            tabwidget.setCurrentIndex(1)
            progressBar.setValue(70)
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('DeleteRenderJob Clean Data :'+cleandata)
            progressBar.setValue(100)

        def ServerAnsweredGetRemoteInfo(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean Data :'+cleandata)
            cleandata = cleandata.replace('\\', '')
            print("Clean feedback :"+cleandata)
            json_remote_data = json.loads(cleandata)

            print("Got Server Answer : GetRemoteInfo")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.setText(ServerAnswerTextEdit.toPlainText() + '  ' + tanswer+" : "+feedback)
            tabwidget.setCurrentIndex(1)
            #Parse super json from server
            print(type(json_remote_data))
            print('Movie Rendering Working : ' +json_remote_data["MoviePipelineRendering"])
            if json_remote_data["MoviePipelineRendering"] == 'True':
                Groupbox.setTitle('Server Status : Rendering Movie ')
            else:
                Groupbox.setTitle('Server Status : Available for Render ')
            print('Movie Rendering Working 2 : ' + json_remote_data["MoviePipelineRendering2"])

            progressBar.setValue(100)

        def ServerAnsweredStartRenderJobs(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('RenderJobs Clean Data :' + cleandata)

        def ServerAnsweredGetRenderPresets(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('GetRenderPresets Clean Data :' + cleandata)
            if len(cleandata) == 0:
                comboBoxQueue.clear()
                comboBoxQueue.addItem("EMPTY")
                return
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            tabwidget.setCurrentIndex(1)
            list_presets = cleandata.split(',')
            work_list_presets = []
            comboBoxQ.clear()
            for p in  list_presets:
                if 'Render' in p:
                    work_list_presets.append(p)
                    comboBoxQ.addItem(p)


        def UpdateStatusOnline(server_str):
            StatusLabel.setStyleSheet("QLabel { color : green; }")
            StatusLabel.setText("Unreal Server Status Online : " + server_str)

        def UpdateStatusOffline(server_str):
            StatusLabel.setStyleSheet("QLabel { background-color : yellow; color : red; }")
            StatusLabel.setText("Unreal Server Status Offline : " + server_str)

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

        def Get_All_Server_Shots():
            FilterToggleBtn.setChecked(False)
            tabwidget.setCurrentIndex(0)
            JsonTextEdit.setText(json.dumps(Json_RequestGetAllShots))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllShots) #Send Json to Unreal


        def FillShots(feedback):
            res = feedback.split(",")
            res.sort()
            print(res[1])
            comboBox.clear()
            listing.clear()
            print('Start Sorting:')
            for i, name in enumerate(res):
                #print('Feedback ['+str(i)+']: '+res[i])
                if (res[i].find('_SEQ') > 0) & (res[i].find('Game/SHOTS') > 0):
                    mlist = res[i].split('.')[-1].split('_')
                    if len(mlist) == 2:
                        #if 'ANIM_SEQ' not in res[i]: #_Anim_SEQ ignore
                        comboBox.addItem("" + res[i])
                        listing.addItem("" + res[i])
            listing.setMaximumHeight(200)

        def FillQueueJobs(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean :'+cleandata)
            print(len(cleandata))
            if len(cleandata) == 0:
                comboBoxQueue.clear()
                comboBoxQueue.addItem("EMPTY")
                return
            res = cleandata.split(",")
            res.sort()
            comboBoxQueue.clear()
            current_project = settings.get_Current_project()
            print('Start Sorting for Project :'+current_project)
            for i, name in enumerate(res):
                print('Feedback ['+str(i)+']: '+res[i])
                if (res[i].find(current_project) > -1):
                    comboBoxQueue.addItem("" + res[i])

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

        def MakeImagesTool(sequence, sQualityPreset='', bFtp_transfer=True):
            if sequence == 'EMPTY':
                print("Wrong sequence name!")
                return
            print('Send Render for ImagesTool Render : '+sequence + ' Quality - '+str(sQualityPreset)+' Ftp transfer - '+str(bFtp_transfer))
            Json_RequestMakeRenderJob["Parameters"]["Body"]["parameters"]["sSeqName"] = sequence
            Json_RequestMakeRenderJob["Parameters"]["Body"]["parameters"]["sQuality"] = sQualityPreset
            Json_RequestMakeRenderJob["Parameters"]["Body"]["parameters"]["bFtp_transfer"] = bFtp_transfer
            progressBar.setValue(0)
            JsonTextEdit.setText(json.dumps(Json_RequestMakeRenderJob))
            tabwidget.setCurrentIndex(0)
            print("Sending....")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestMakeRenderJob), ServerAnsweredMakeRenderJob)

        def StartRenderJobs(job_name):
            Json_RequestStartRenderJob["Parameters"]["Body"]["parameters"]["sJobName"] = job_name
            JsonTextEdit.setText(json.dumps(Json_RequestStartRenderJob))
            tabwidget.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestStartRenderJob), ServerAnsweredStartRenderJobs)

        def Get_Render_Presets():
            JsonTextEdit.setText(json.dumps(Json_RequestGetRenderPresets))
            tabwidget.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestGetRenderPresets), ServerAnsweredGetRenderPresets)

        @QtCore.Slot()
        def MakeRenderJob():
            MakeImagesTool(comboBox.currentText(), comboBoxQ.currentText(), CheckTransferToggleBtn.isChecked())

        @QtCore.Slot()
        def StartRendering():
            job_name = comboBoxQueue.currentText().split('-')[0]
            print('split - '+job_name)
            StartRenderJobs(job_name)

        @QtCore.Slot()
        def GetRenderPresets():
            print('GetRenderPresets')
            Get_Render_Presets()

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
            print("Connect to Unreal websocket : " + HostLineEdit.text())
            Check_Server()

        def Check_Server():
            try:
                progressBar.setValue(0)
                create_connection(HostLineEdit.text(), 5)
                ChangeStatus(True)
                settings.set_HostServer(HostLineEdit.text())
                return True
            except:
                ChangeStatus(False)
            return False

        @QtCore.Slot()
        def ChangeStatus(check):
            tm = dt.now().strftime("%H:%M:%S")
            if check:
                UpdateStatusOnline(HostLineEdit.text() + ' ' + tm)
                progressBar.setValue(100)
            else:
                UpdateStatusOffline(HostLineEdit.text() + ' ' + tm)

        @QtCore.Slot()
        def onClickedToggle():
            Check.setEnabled(ServerToggleBtn.isChecked())
            HostLineEdit.setEnabled(ServerToggleBtn.isChecked())

        @QtCore.Slot()
        def onClickedToggleTransfer():
            print('Set Ftp transfer : '+str(CheckTransferToggleBtn.isChecked()))

        @QtCore.Slot()
        def onOpenFolder():
            import subprocess
            print('Open image folder ')
            #PyClientMovie.OpenFolderImages()
            print('Images directories : ')
            dir ='C:\\Users'
            if PyClientMovie.image_directories:
                subprocess.Popen(f'explorer "{PyClientMovie.image_directories}"')
            else:
                subprocess.Popen(f'explorer "{dir}"')

        @QtCore.Slot()
        def onClickedFilter():
            if FilterToggleBtn.isChecked():
                print('filter = '+FilterLineEdit.text())
                index = comboBox.findText(FilterLineEdit.text(), QtCore.Qt.MatchRegularExpression)
                print(index)
                if index > -1:
                    comboBox.setCurrentIndex(index)
            else:
                comboBox.setCurrentIndex(0)
        @QtCore.Slot()
        def onEnterFilterLine():
            onClickedFilter()

        @QtCore.Slot()
        def UpdatePerforce():
            global trequest
            trequest = dt.now()
            print("Perforce ")
            progressBar.setValue(0)
            JsonTextEdit.setText(json.dumps(Json_UpdatePerforce))
            tabwidget.setCurrentIndex(0)
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_UpdatePerforce), ServerAnsweredPerforce)

        @QtCore.Slot()
        def onOpenLogPerforce():
            settings.OpenLogPerforce()
            print()

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
        def GetQueueJobs():
            print('GetQueueJobs')
            JsonTextEdit.setText(json.dumps(Json_RequestRemoteQueueJobs))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllQueueJobs) #Send Json to Unreal

        @QtCore.Slot()
        def DeleteRenderJob():
            selected_job_name = comboBoxQueue.currentText().split('-')[0]
            print('DeleteRenderJob :'+selected_job_name)
            Delete_Render_Job(selected_job_name)


        def Delete_Render_Job(job_name):
            Json_RequestDeleteRenderJob["Parameters"]["Body"]["parameters"]["sJobName"] = job_name
            JsonTextEdit.setText(json.dumps(Json_RequestDeleteRenderJob))
            tabwidget.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            progressBar.setValue(0)
            progressBar.setValue(50)
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestDeleteRenderJob), ServerAnsweredDeleteRenderJob)

        @QtCore.Slot()
        def DeleteAllRenderJobs():
            JsonTextEdit.setText(json.dumps(Json_RequestDeleteAllRenderJobs))
            tabwidget.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            progressBar.setValue(0)
            progressBar.setValue(50)
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestDeleteAllRenderJobs), ServerAnsweredDeleteAllRenderJobs)

        @QtCore.Slot()
        def GetRemoteInfo():
            print('GetRemoteInfo')
            JsonTextEdit.setText(json.dumps(Json_RequestRemoteInfo))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetRemoteInfo) #Send Json to Unreal

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
        Groupbox.setAlignment(100)
        Groupbox.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        vbox = QtWidgets.QHBoxLayout()
        Groupbox.setLayout(vbox)
        layout.addWidget(Groupbox)


        Check = QtWidgets.QPushButton("Check Server")
        Check.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(Check, QtCore.SIGNAL("clicked()"), CheckServer)
        Groupbox.layout().addWidget(Check)

        HostLineEdit = QtWidgets.QLineEdit(Server)
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

        GetInfoBtn = QtWidgets.QPushButton("Get Info")
        GetInfoBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(GetInfoBtn, QtCore.SIGNAL("clicked()"), GetRemoteInfo)
        GroupboxCommand.layout().addWidget(GetInfoBtn)

        CommandBtn = QtWidgets.QPushButton("Send Command")
        CommandBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(CommandBtn, QtCore.SIGNAL("clicked()"), SendCommand)
        GroupboxCommand.layout().addWidget(CommandBtn)

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

        GroupboxQueue = QtWidgets.QGroupBox("Manager Movie Rendering Queue")
        GroupboxQueue.setChecked(True)
        vbox50 = QtWidgets.QHBoxLayout()
        GroupboxQueue.setLayout(vbox50)

        get_queue = QtWidgets.QPushButton("Get Queue Jobs")
        get_queue.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        get_queue.setFixedWidth(150)
        self.connect(get_queue, QtCore.SIGNAL("clicked()"), GetQueueJobs)
        GroupboxQueue.layout().addWidget(get_queue)

        comboBoxQueue = QtWidgets.QComboBox(self)
        comboBoxQueue.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBoxQueue.addItem("EMPTY")
        GroupboxQueue.layout().addWidget(comboBoxQueue)

        delete_queue = QtWidgets.QPushButton("Delete Job")
        delete_queue.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        delete_queue.setFixedWidth(100)
        self.connect(delete_queue, QtCore.SIGNAL("clicked()"), DeleteRenderJob)
        GroupboxQueue.layout().addWidget(delete_queue)

        delete_all_queue = QtWidgets.QPushButton("Delete All Jobs!")
        delete_all_queue.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        delete_all_queue.setFixedWidth(150)
        self.connect(delete_all_queue, QtCore.SIGNAL("clicked()"), DeleteAllRenderJobs)
        GroupboxQueue.layout().addWidget(delete_all_queue)


        GroupboxAuto = QtWidgets.QGroupBox("Rendering Shots")
        GroupboxAuto.setChecked(True)
        vbox3 = QtWidgets.QHBoxLayout()
        GroupboxAuto.setLayout(vbox3)

        getshot = QtWidgets.QPushButton("Get Server Sequences")
        getshot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(getshot, QtCore.SIGNAL("clicked()"), Get_All_Server_Shots)
        GroupboxAuto.layout().addWidget(getshot)

        render = QtWidgets.QPushButton("Render Movie Sequence")
        render.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        render.setEnabled(False)
        self.connect(render, QtCore.SIGNAL("clicked()"), RenderMovie)
        GroupboxAuto.layout().addWidget(render)

        make_render_job_btn = QtWidgets.QPushButton("Make Render Job")
        make_render_job_btn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(make_render_job_btn, QtCore.SIGNAL("clicked()"), MakeRenderJob)
        GroupboxAuto.layout().addWidget(make_render_job_btn)

        start_render_jobs_btn = QtWidgets.QPushButton("Start Render Jobs")
        start_render_jobs_btn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(start_render_jobs_btn, QtCore.SIGNAL("clicked()"), StartRendering)
        GroupboxAuto.layout().addWidget(start_render_jobs_btn)

        GroupboxAuto5 = QtWidgets.QGroupBox("Rendering Settings")
        GroupboxAuto5.setChecked(True)
        vbox4 = QtWidgets.QHBoxLayout()
        GroupboxAuto5.setLayout(vbox4)

        current_project = QtWidgets.QLabel("Current Project : "+settings.get_Current_project()+'                    ')
        GroupboxAuto5.layout().addWidget(current_project)

        preset = QtWidgets.QLabel("Quality")
        GroupboxAuto5.layout().addWidget(preset)

        GetRenderPresetsBtn = QtWidgets.QPushButton("GetRenderPresets")
        GetRenderPresetsBtn.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.connect(GetRenderPresetsBtn, QtCore.SIGNAL("clicked()"), GetRenderPresets)
        GroupboxAuto5.layout().addWidget(GetRenderPresetsBtn)

        comboBoxQ = QtWidgets.QComboBox(self)
        comboBoxQ.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBoxQ.setFixedWidth(200)
        comboBoxQ.addItem("Epmty")
        GroupboxAuto5.layout().addWidget(comboBoxQ)

        CheckTransferToggleBtn = QtWidgets.QCheckBox("Transfer")
        CheckTransferToggleBtn.setChecked(False)
        self.connect(CheckTransferToggleBtn, QtCore.SIGNAL("clicked()"), onClickedToggleTransfer)
        GroupboxAuto5.layout().addWidget(CheckTransferToggleBtn)

        OpenFolderImagesBtn = QtWidgets.QPushButton("Open Images Folder..")
        OpenFolderImagesBtn.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        OpenFolderImagesBtn.setEnabled(False)
        self.connect(OpenFolderImagesBtn, QtCore.SIGNAL("clicked()"), onOpenFolder)
        GroupboxAuto5.layout().addWidget(OpenFolderImagesBtn)

        OpenLogImagesBtn = QtWidgets.QPushButton("Open Log..")
        OpenLogImagesBtn.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        OpenLogImagesBtn.setEnabled(False)
        self.connect(OpenLogImagesBtn, QtCore.SIGNAL("clicked()"), onOpenFolder)
        GroupboxAuto5.layout().addWidget(OpenLogImagesBtn)

        GroupboxAuto0 = QtWidgets.QGroupBox("Found Sequences")
        GroupboxAuto0.setChecked(True)
        vbox31 = QtWidgets.QHBoxLayout()
        GroupboxAuto0.setLayout(vbox31)

        FilterToggleBtn = QtWidgets.QCheckBox("Filter")
        FilterLineEdit = QtWidgets.QLineEdit('Name')
        FilterLineEdit.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        FilterToggleBtn.setChecked(False)
        FilterToggleBtn.setFixedWidth(80)
        FilterLineEdit.setFixedWidth(150)
        self.connect(FilterToggleBtn, QtCore.SIGNAL("clicked()"), onClickedFilter)
        self.connect(FilterLineEdit, QtCore.SIGNAL("returnPressed()"), onEnterFilterLine)

        GroupboxAuto0.layout().addWidget(FilterToggleBtn)
        GroupboxAuto0.layout().addWidget(FilterLineEdit)

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
        SetPerforceBtn.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.connect(SetPerforceBtn, QtCore.SIGNAL("clicked()"),SetPerforceProfile)
        GroupboxAuto2.layout().addWidget(SetPerforceBtn)


        UpdatePerforceBtn = QtWidgets.QPushButton("Update Perforce")
        UpdatePerforceBtn.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.connect(UpdatePerforceBtn, QtCore.SIGNAL("clicked()"), UpdatePerforce)
        GroupboxAuto2.layout().addWidget(UpdatePerforceBtn)

        OpenLogPerforceBtn = QtWidgets.QPushButton("Open Log..")
        OpenLogPerforceBtn.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.connect(OpenLogPerforceBtn, QtCore.SIGNAL("clicked()"), onOpenLogPerforce)
        GroupboxAuto2.layout().addWidget(OpenLogPerforceBtn)


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
        BatchRenderBtn.setEnabled(False)
        self.connect(BatchRenderBtn, QtCore.SIGNAL("clicked()"), BatchRenderMovie)
        GroupboxAuto3.layout().addWidget(BatchRenderBtn)



        GroupboxMain = QtWidgets.QGroupBox("SERVER: Automation Pipeline")
        GroupboxMain.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        vbox5 = QtWidgets.QVBoxLayout()
        GroupboxMain.setLayout(vbox5)

        GroupboxMain.layout().addWidget(GroupboxQueue)
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

        #get last server save cfg
        h = settings.get_HostServer()
        if h:
            HostLineEdit.setText(h)

        if Check_Server():
            GetRemoteInfo()
            Get_Render_Presets()
            Get_All_Server_Shots()
            GetQueueJobs()

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
    import unreal
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
    print('Current Project : '+settings.get_Current_project())
if "unreal" not in dir():
    print("Warning: Unreal modules Not Loaded!")
    print('Main Dir program: '+os.getcwd())
    Loaded = True
else:
    unreal.log("Unreal modules Loaded & Ready!")
    unreal_working_dirs()

print("Connect to Unreal websocket : "+Server)
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

