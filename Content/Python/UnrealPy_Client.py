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
from PySide2.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QInputDialog, QVBoxLayout
from PySide2.QtWidgets import *

#pip install websocket-client
from websocket import create_connection

import unreal_worker

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

#SuperMessage Remote tool
Json_RequestRemoteAllRenderingInfo = \
    {
        "MessageName": "http",
        "Parameters": {
            "Url": "/remote/object/call",
            "Verb": "PUT",
            "Body": {
                "objectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
                "functionName": "unreal_python_get_all_rendering_info",
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
        Name = settings.get_PerforceSettingsByName('Name')
        self.le = QLineEdit(Name)
        layout.addRow(self.lbl, self.le)

        self.lbl1 = QLabel("User")
        User = settings.get_PerforceSettingsByName('User')
        self.le1 = QLineEdit(User)
        layout.addRow(self.lbl1, self.le1)

        self.lbl2 = QLabel("Password")
        Pwd = settings.get_PerforceSettingsByName('Pwd')
        self.le2 = QLineEdit(Pwd)
        layout.addRow(self.lbl2, self.le2)

        self.lbl3 = QLabel("Host")
        Host = settings.get_PerforceSettingsByName('Host')
        self.le3 = QLineEdit(Host)
        layout.addRow(self.lbl3, self.le3)

        self.lbl4 = QLabel("Depot")
        Depot = settings.get_PerforceSettingsByName('Depot')
        self.le4 = QLineEdit(Depot)
        layout.addRow(self.lbl4, self.le4)

        self.lbl5 = QLabel("Workspace")
        Workspace = settings.get_PerforceSettingsByName('Workspace')
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
        settings.rewrite_perforce_settings(list)
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
            TabWidgetCommans.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredGetAllShots(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : Getallshots")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            TabWidgetCommans.setCurrentIndex(1)
            FillShots(feedback)
            progressBar.setValue(70)
            progressBar.setValue(100)
            # Ask about Rendering Movie  status
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()


        def ServerAnsweredSetShotRender(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : SetShotRender")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            TabWidgetCommans.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredMakeRenderJob(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : MakeRenderJob")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            TabWidgetCommans.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredPerforce(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : Try Update server")
            tanswer =dt.now().strftime("%H:%M:%S")
            tused = dt.now()-trequest
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            TabWidgetCommans.setCurrentIndex(1)
            PerforceLabel.setText("Perforce Updated : "+tanswer + '[' +str(tused) + ']')
            progressBar.setValue(100)

        def ServerAnsweredGetAllQueueJobs(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : GetAllQueueJobs")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommans.setCurrentIndex(1)
            #Fill Queue Combobox
            FillQueueJobs(feedback)
            comboBoxQueue.setCurrentIndex(0)
            progressBar.setValue(70)
            progressBar.setValue(100)
            #Ask about Rendering Movie  status
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()

        def ServerAnsweredDeleteRenderJob(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : DeleteRenderJob")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommans.setCurrentIndex(1)
            progressBar.setValue(70)
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('DeleteRenderJob Clean Data :'+cleandata)
            progressBar.setValue(100)
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()


        def ServerAnsweredDeleteAllRenderJobs(feedback):
            UpdateStatusOnline(HostLineEdit.text())
            print("Got Server Answer : DeleteAllRenderJobs")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommans.setCurrentIndex(1)
            progressBar.setValue(70)
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('DeleteRenderJob Clean Data :'+cleandata)
            progressBar.setValue(100)
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()

        def ServerAnsweredGetRemoteInfo(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean Data :'+cleandata)
            cleandata = cleandata.replace('\\', '')
            print("Clean feedback :"+cleandata)
            json_remote_data = json.loads(cleandata)

            print("Got Server Answer : GetRemoteInfo")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.setText(ServerAnswerTextEdit.toPlainText() + '  ' + tanswer+" : "+feedback)
            TabWidgetCommans.setCurrentIndex(1)
            #Parse super json from server
            print(type(json_remote_data))
            print('Movie Rendering Working : ' +json_remote_data["MoviePipelineRendering"])
            if json_remote_data["MoviePipelineRendering"] == 'True':
                GroupboxStatus.setTitle('Server Status : Rendering Movie ')
            else:
                GroupboxStatus.setTitle('Server Status : Available for Render ')
            print('Movie Rendering Working 2 : ' + json_remote_data["MoviePipelineRendering2"])

            progressBar.setValue(100)


        def UpdatePresets(cleandata):
            if len(cleandata) == 0:
                comboBoxQueue.clear()
                comboBoxQueue.addItem("EMPTY")
                return
            tanswer =dt.now().strftime("%H:%M:%S")
            TabWidgetCommans.setCurrentIndex(1)
            list_presets = cleandata.split(',')
            work_list_presets = []
            comboBoxQ.clear()
            for p in  list_presets:
                if 'Render' in p:
                    work_list_presets.append(p)
                    comboBoxQ.addItem(p)

        def UpdateQueueJobs(cleandata):
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

        def ServerAnsweredGetAllRenderingInfo(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean Data :'+cleandata)
            cleandata = cleandata.replace('\\', '')
            print("Clean feedback :"+cleandata)
            json_remote_data = json.loads(cleandata)

            print("Got Server Answer : GetAllRenderingInfo")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(ServerAnswerTextEdit.toPlainText() + '  ' + tanswer+" : "+feedback)
            TabWidgetCommans.setCurrentIndex(1)

            #Parse super json from server
            print(type(json_remote_data))

            print('Movie Rendering Working : ' +json_remote_data["MoviePipelineRendering"])
            if json_remote_data["MoviePipelineRendering"] == 'True':
                GroupboxStatus.setTitle('Server Status : Rendering Movie ')
            else:
                GroupboxStatus.setTitle('Server Status : Available for Render ')

            PresetsRenderingList = json_remote_data["PresetsRenderingList"]
            print('Presets Rendering Quality List : ' + PresetsRenderingList)
            UpdatePresets(PresetsRenderingList)

            QueueRenderJobsList = json_remote_data["QueueRenderJobsList"]
            print('Queue RenderJobs List : ' + QueueRenderJobsList)
            UpdateQueueJobs(QueueRenderJobsList)

            AllShotsList = json_remote_data["AllShotsList"]
            print('All Shots List : ' + AllShotsList)
            FillShots(AllShotsList)

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
            TabWidgetCommans.setCurrentIndex(1)
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
            TabWidgetCommans.setCurrentIndex(0)
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
            TabWidgetCommans.setCurrentIndex(0)
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
            TabWidgetCommans.setCurrentIndex(0)
            print("Sending....")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestMakeRenderJob), ServerAnsweredMakeRenderJob)

        def StartRenderJobs(job_name):
            Json_RequestStartRenderJob["Parameters"]["Body"]["parameters"]["sJobName"] = job_name
            JsonTextEdit.setText(json.dumps(Json_RequestStartRenderJob))
            TabWidgetCommans.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestStartRenderJob), ServerAnsweredStartRenderJobs)

        def Get_Render_Presets():
            JsonTextEdit.setText(json.dumps(Json_RequestGetRenderPresets))
            TabWidgetCommans.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestGetRenderPresets), ServerAnsweredGetRenderPresets)

        @QtCore.Slot()
        def MakeRenderJob():
            MakeImagesTool(comboBox.currentText(), comboBoxQ.currentText(), CheckTransferToggleBtn.isChecked())
            if (RefreshQueueToggleBtn.isChecked()):
                GetQueueJobs()
            else:
                GetRemoteInfo()

        @QtCore.Slot()
        def StartRendering():
            job_name = comboBoxQueue.currentText().split('-')[0]
            print('split - '+job_name)
            StartRenderJobs(job_name)
            if (RefreshQueueToggleBtn.isChecked()):
                GetQueueJobs()
            else:
                GetRemoteInfo()

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
                settings.set_ClientSettingsByName('HostServer', HostLineEdit.text())
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
            TabWidgetCommans.setCurrentIndex(0)
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

        def OnChangeProject():
            ShowProjectsDialog()

        @QtCore.Slot()
        def ShowProjectsDialog():
            items = unreal_worker.M2_get_projects_dict()
            print('Items:'+str('items')+' '+str(len(items)))
            if len(items) == 0:
                items = settings.settings_m2_project_default['AvailableProjects']
            item, ok = QInputDialog.getItem(self, "Select Project", "list of Projects", items, 0, False)
            if (ok):
                settings.set_ClientM2ProjectByName('DefaultProject', item)
            print(str(item))
            current_project.setText("Current Project : "+settings.get_Current_project()+'                    ')

        @QtCore.Slot()
        def ShowSimpleDialogs():
            items = ("C", "C++", "Java", "Python")
            item, ok = QInputDialog.getItem(self, "select input dialog", "list of languages", items, 0, False)
            print(str(item))
            #dlg = QDialog(self)
            #dlg.resize(400, 400)
            #dlg.setWindowTitle("Settings Perforce")
            #dlg.exec_()


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
        def onRefreshQueueToggle():
            settings.set_ClientSettingsByName('RefreshQueueBool', RefreshQueueToggleBtn.isChecked())

        @QtCore.Slot()
        def onAdvancedRenderToggle():
            if AdvancedRenderToggleBtn.isChecked():
                GroupboxMain.setFixedHeight(770)
                OpenLogImagesBtn.show()
                OpenFolderImagesBtn.show()
                GroupboxBatchMakeJobs.show()
                GroupboxSendCommands.show()
                GetQueueBtn.show()
                GetServerShots.show()
                RenderMovieDisabled.show()
                GetRenderPresetsBtn.show()
                RefreshQueueToggleBtn.setEnabled(AdvancedRenderToggleBtn.isChecked())
            else:
                GroupboxMain.setFixedHeight(660)
                OpenLogImagesBtn.hide()
                OpenFolderImagesBtn.hide()
                GroupboxBatchMakeJobs.hide()
                GroupboxSendCommands.hide()
                GetQueueBtn.hide()
                GetServerShots.hide()
                RenderMovieDisabled.hide()
                GetRenderPresetsBtn.hide()
                RefreshQueueToggleBtn.setEnabled(AdvancedRenderToggleBtn.isChecked())

            settings.set_ClientSettingsByName('AdvancedRenderBool', AdvancedRenderToggleBtn.isChecked())

        @QtCore.Slot()
        def DeleteRenderJob():
            selected_job_name = comboBoxQueue.currentText().split('-')[0]
            print('DeleteRenderJob :'+selected_job_name)
            Delete_Render_Job(selected_job_name)


        def Delete_Render_Job(job_name):
            Json_RequestDeleteRenderJob["Parameters"]["Body"]["parameters"]["sJobName"] = job_name
            JsonTextEdit.setText(json.dumps(Json_RequestDeleteRenderJob))
            TabWidgetCommans.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            progressBar.setValue(0)
            progressBar.setValue(50)
            SendSocket(ClearAnswer, HostServer, json.dumps(Json_RequestDeleteRenderJob), ServerAnsweredDeleteRenderJob)

        @QtCore.Slot()
        def DeleteAllRenderJobs():
            JsonTextEdit.setText(json.dumps(Json_RequestDeleteAllRenderJobs))
            TabWidgetCommans.setCurrentIndex(0)
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
        def GetAllRenderingInfo():
            print('GetAllRenderingInfo')
            JsonTextEdit.setText(json.dumps(Json_RequestRemoteAllRenderingInfo))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(ClearAnswer, HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllRenderingInfo) #Send Json to Unreal


        @QtCore.Slot()
        def MyQuit():
            app.quit()

        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Unreal Websocket Client")

        layoutWindow = QtWidgets.QVBoxLayout()
        self.setLayout(layoutWindow)

        GroupboxLabel = QtWidgets.QGroupBox("")
        hboxLabel = QtWidgets.QHBoxLayout()
        StatusLabel = QtWidgets.QLabel("Unreal Server Status:")
        StatusLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        StatusLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")
        StatusLabel.setFixedHeight(40)
        GroupboxLabel.setFixedHeight(60)
        GroupboxLabel.setLayout(hboxLabel)

        GroupboxLabel.layout().addWidget(StatusLabel)
        layoutWindow.addWidget(GroupboxLabel)

        GroupboxStatus = QtWidgets.QGroupBox("Server Status")
        GroupboxStatus.setAlignment(100)
        GroupboxStatus.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        hboxStatus = QtWidgets.QHBoxLayout()
        GroupboxStatus.setFixedHeight(80)

        GroupboxStatus.setLayout(hboxStatus)
        layoutWindow.addWidget(GroupboxStatus)

        AdvancedRenderToggleBtn = QtWidgets.QCheckBox("Advanced Render Control")
        AdvancedRenderToggleBtn.setChecked(True)
        self.connect(AdvancedRenderToggleBtn, QtCore.SIGNAL("clicked()"), onAdvancedRenderToggle)
        GroupboxStatus.layout().addWidget(AdvancedRenderToggleBtn)

        Check = QtWidgets.QPushButton("Check Server")
        Check.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(Check, QtCore.SIGNAL("clicked()"), CheckServer)
        GroupboxStatus.layout().addWidget(Check)

        HostLineEdit = QtWidgets.QLineEdit(Server)
        HostLineEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        HostServer = "ws://" + HostLineEdit.text()+":30020"
        HostLineEdit = QtWidgets.QLineEdit(Server)
        GroupboxStatus.layout().addWidget(HostLineEdit)

        ServerToggleBtn = QtWidgets.QCheckBox("Change Server")
        ServerToggleBtn.setChecked(False)
        self.connect(ServerToggleBtn, QtCore.SIGNAL("clicked()"), onClickedToggle)
        Check.setEnabled(ServerToggleBtn.isChecked())
        HostLineEdit.setEnabled(ServerToggleBtn.isChecked())
        GroupboxStatus.layout().addWidget(ServerToggleBtn)

        GroupboxSendCommands = QtWidgets.QGroupBox("Send Custom Commands")
        GroupboxSendCommands.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        vbox2 = QtWidgets.QVBoxLayout()
        GroupboxSendCommands.setLayout(vbox2)
        layoutWindow.addWidget(GroupboxSendCommands)

        GetInfoBtn = QtWidgets.QPushButton("Get Info")
        GetInfoBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(GetInfoBtn, QtCore.SIGNAL("clicked()"), GetRemoteInfo)
        GroupboxSendCommands.layout().addWidget(GetInfoBtn)

        GetInfoBtn2 = QtWidgets.QPushButton("Get All Rendering Info")
        GetInfoBtn2.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(GetInfoBtn2, QtCore.SIGNAL("clicked()"), GetAllRenderingInfo)
        GroupboxSendCommands.layout().addWidget(GetInfoBtn2)


        CommandBtn = QtWidgets.QPushButton("Send Command")
        CommandBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(CommandBtn, QtCore.SIGNAL("clicked()"), SendCommand)
        GroupboxSendCommands.layout().addWidget(CommandBtn)

        JsonTextEdit = QtWidgets.QTextEdit(json.dumps(Json_RequestRemoteStaticFunction))
        JsonTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layoutWindow.addWidget(JsonTextEdit)

        ServerAnswerTextEdit = QtWidgets.QTextEdit('Feedback from server')
        ServerAnswerTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layoutWindow.addWidget(ServerAnswerTextEdit)

        TabWidgetCommans = QtWidgets.QTabWidget()
        TabWidgetCommans.addTab(JsonTextEdit, "Command Client")
        TabWidgetCommans.addTab(ServerAnswerTextEdit, "Answer Server")
        GroupboxSendCommands.layout().addWidget(TabWidgetCommans)

        GroupboxQueue = QtWidgets.QGroupBox("Rendering Jobs Queue")
        GroupboxQueue.setChecked(True)
        vbox50 = QtWidgets.QHBoxLayout()
        GroupboxQueue.setFixedHeight(80)
        GroupboxQueue.setLayout(vbox50)

        GetQueueBtn = QtWidgets.QPushButton("Get Queue Jobs")
        GetQueueBtn.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        GetQueueBtn.setFixedWidth(150)
        self.connect(GetQueueBtn, QtCore.SIGNAL("clicked()"), GetQueueJobs)
        GroupboxQueue.layout().addWidget(GetQueueBtn)

        comboBoxQueue = QtWidgets.QComboBox(self)
        comboBoxQueue.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBoxQueue.setFixedWidth(750)
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


        GroupboxRenderJobs = QtWidgets.QGroupBox("Rendering Shots")
        GroupboxRenderJobs.setChecked(True)
        vbox3 = QtWidgets.QHBoxLayout()
        GroupboxRenderJobs.setFixedHeight(80)
        GroupboxRenderJobs.setLayout(vbox3)

        GetServerShots = QtWidgets.QPushButton("Get Server Sequences")
        GetServerShots.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(GetServerShots, QtCore.SIGNAL("clicked()"), Get_All_Server_Shots)
        GroupboxRenderJobs.layout().addWidget(GetServerShots)

        RenderMovieDisabled = QtWidgets.QPushButton("Render Movie")
        RenderMovieDisabled.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        RenderMovieDisabled.setEnabled(False)
        self.connect(RenderMovieDisabled, QtCore.SIGNAL("clicked()"), RenderMovie)
        GroupboxRenderJobs.layout().addWidget(RenderMovieDisabled)

        start_render_jobs_btn = QtWidgets.QPushButton("Start Render")
        start_render_jobs_btn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(start_render_jobs_btn, QtCore.SIGNAL("clicked()"), StartRendering)
        GroupboxRenderJobs.layout().addWidget(start_render_jobs_btn)

        GroupboxRenderingSettings = QtWidgets.QGroupBox("Project Rendering Settings")
        GroupboxRenderingSettings.setChecked(True)
        vboxRenderingSettings = QtWidgets.QHBoxLayout()
        GroupboxRenderingSettings.setFixedHeight(80)
        GroupboxRenderingSettings.setLayout(vboxRenderingSettings)

        ChangeProjectBtn = QtWidgets.QPushButton("Change Project")
        ChangeProjectBtn.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.connect(ChangeProjectBtn, QtCore.SIGNAL("clicked()"), OnChangeProject)
        GroupboxRenderingSettings.layout().addWidget(ChangeProjectBtn)

        current_project = QtWidgets.QLabel("Current Project : "+settings.get_Current_project()+'                    ')
        GroupboxRenderingSettings.layout().addWidget(current_project)

        preset = QtWidgets.QLabel("Quality")
        GroupboxRenderingSettings.layout().addWidget(preset)

        GetRenderPresetsBtn = QtWidgets.QPushButton("GetRenderPresets")
        GetRenderPresetsBtn.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.connect(GetRenderPresetsBtn, QtCore.SIGNAL("clicked()"), GetRenderPresets)
        GroupboxRenderingSettings.layout().addWidget(GetRenderPresetsBtn)

        comboBoxQ = QtWidgets.QComboBox(self)
        comboBoxQ.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBoxQ.setFixedWidth(200)
        comboBoxQ.addItem("Epmty")
        GroupboxRenderingSettings.layout().addWidget(comboBoxQ)

        CheckTransferToggleBtn = QtWidgets.QCheckBox("Transfer")
        CheckTransferToggleBtn.setChecked(False)
        self.connect(CheckTransferToggleBtn, QtCore.SIGNAL("clicked()"), onClickedToggleTransfer)
        GroupboxRenderingSettings.layout().addWidget(CheckTransferToggleBtn)

        OpenFolderImagesBtn = QtWidgets.QPushButton("Open Images Folder..")
        OpenFolderImagesBtn.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.connect(OpenFolderImagesBtn, QtCore.SIGNAL("clicked()"), onOpenFolder)
        GroupboxRenderingSettings.layout().addWidget(OpenFolderImagesBtn)

        OpenLogImagesBtn = QtWidgets.QPushButton("Open Log..")
        OpenLogImagesBtn.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.connect(OpenLogImagesBtn, QtCore.SIGNAL("clicked()"), onOpenFolder)
        GroupboxRenderingSettings.layout().addWidget(OpenLogImagesBtn)

        GroupboxFilterSequences  = QtWidgets.QGroupBox("")
        hboxFilterSequences = QtWidgets.QHBoxLayout()
        hboxFilterSequences.addStretch()
        GroupboxFilterSequences.setLayout(hboxFilterSequences)

        GroupboxFoundSequences = QtWidgets.QGroupBox("Server Sequences")
        GroupboxFoundSequences.setChecked(True)
        vboxSequences = QtWidgets.QVBoxLayout()
        GroupboxFoundSequences.setFixedHeight(160)
        GroupboxFoundSequences.setLayout(vboxSequences)


        FilterToggleBtn = QtWidgets.QCheckBox("Filter")
        FilterLineEdit = QtWidgets.QLineEdit('Name')
        FilterLineEdit.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        FilterToggleBtn.setChecked(False)
        FilterToggleBtn.setFixedWidth(80)
        FilterLineEdit.setFixedWidth(150)
        self.connect(FilterToggleBtn, QtCore.SIGNAL("clicked()"), onClickedFilter)
        self.connect(FilterLineEdit, QtCore.SIGNAL("returnPressed()"), onEnterFilterLine)

        GroupboxFoundSequences.layout().addWidget(GroupboxFilterSequences)


        GroupboxFilterSequences.layout().addWidget(FilterToggleBtn)
        GroupboxFilterSequences.layout().addWidget(FilterLineEdit)

        comboBox = QtWidgets.QComboBox(self)
        comboBox.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Medium))
        comboBox.addItem("EMPTY")

        GroupboxFoundSequences.layout().addWidget(comboBox)

        make_render_job_btn = QtWidgets.QPushButton("Make Render Job")
        make_render_job_btn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(make_render_job_btn, QtCore.SIGNAL("clicked()"), MakeRenderJob)
        GroupboxFoundSequences.layout().addWidget(make_render_job_btn)

        GroupboxPerforce = QtWidgets.QGroupBox("Perforce Control")
        vboxRenderingSettings = QtWidgets.QHBoxLayout()
        GroupboxPerforce.setFixedHeight(80)
        GroupboxPerforce.setLayout(vboxRenderingSettings)

        PerforceLabel = QtWidgets.QLabel("Perforce Time updated :")
        PerforceLabel.setGeometry(10, 50, 160, 20)
        PerforceLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        GroupboxPerforce.layout().addWidget(PerforceLabel)

        SetPerforceBtn = QtWidgets.QPushButton("Settings")
        SetPerforceBtn.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.connect(SetPerforceBtn, QtCore.SIGNAL("clicked()"),SetPerforceProfile)
        GroupboxPerforce.layout().addWidget(SetPerforceBtn)


        UpdatePerforceBtn = QtWidgets.QPushButton("Update Perforce")
        UpdatePerforceBtn.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.connect(UpdatePerforceBtn, QtCore.SIGNAL("clicked()"), UpdatePerforce)
        GroupboxPerforce.layout().addWidget(UpdatePerforceBtn)

        OpenLogPerforceBtn = QtWidgets.QPushButton("Open Log..")
        OpenLogPerforceBtn.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.connect(OpenLogPerforceBtn, QtCore.SIGNAL("clicked()"), onOpenLogPerforce)
        GroupboxPerforce.layout().addWidget(OpenLogPerforceBtn)


        GroupboxBatchMakeJobs = QtWidgets.QGroupBox("Make Batch Rendering Jobs")
        GroupboxBatchMakeJobs.setChecked(True)
        vboxMain = QtWidgets.QVBoxLayout()
        GroupboxBatchMakeJobs.setLayout(vboxMain)
        listing = QtWidgets.QListWidget()
        listing.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Medium))
        listing.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        item = QtWidgets.QListWidgetItem("empty")
        listing.addItem(item)

        listing.itemClicked.connect(printItemText)
        GroupboxBatchMakeJobs.layout().addWidget(listing)
        BatchRenderBtn = QtWidgets.QPushButton("Start Batch Rendering")
        BatchRenderBtn.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Bold))
        BatchRenderBtn.setEnabled(False)
        self.connect(BatchRenderBtn, QtCore.SIGNAL("clicked()"), BatchRenderMovie)
        GroupboxBatchMakeJobs.layout().addWidget(BatchRenderBtn)

        GroupboxMain = QtWidgets.QGroupBox("SERVER: Automation Pipeline")
        GroupboxMain.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        vboxMain = QtWidgets.QVBoxLayout()
        GroupboxMain.setFixedHeight(770)
        GroupboxMain.setLayout(vboxMain)

        GroupboxAdvancedRender = QtWidgets.QGroupBox("Rendering Control")
        GroupboxAdvancedRender.setChecked(True)
        hboxAd = QtWidgets.QHBoxLayout()
        GroupboxAdvancedRender.setLayout(hboxAd)
        GroupboxAdvancedRender.setFixedHeight(60)

        RefreshQueueToggleBtn = QtWidgets.QCheckBox("Auto refresh all rendering info")
        RefreshQueueToggleBtn.setChecked(True)
        self.connect(RefreshQueueToggleBtn, QtCore.SIGNAL("clicked()"), onRefreshQueueToggle)
        GroupboxAdvancedRender.layout().addWidget(RefreshQueueToggleBtn)

        GroupboxMain.layout().addWidget(GroupboxAdvancedRender)


        GroupboxMain.layout().addWidget(GroupboxRenderingSettings)
        GroupboxMain.layout().addWidget(GroupboxFoundSequences)
        GroupboxMain.layout().addWidget(GroupboxQueue)
        GroupboxMain.layout().addWidget(GroupboxRenderJobs)

        GroupboxMain.layout().addWidget(GroupboxBatchMakeJobs)

        GroupboxMain.layout().addWidget(GroupboxPerforce)
        layoutWindow.addWidget(GroupboxMain)

        GroupboxTech = QtWidgets.QGroupBox("")
        vboxTech = QtWidgets.QVBoxLayout()
        GroupboxTech.setFixedHeight(80)
        GroupboxTech.setLayout(vboxTech)

        progressBar = QtWidgets.QProgressBar(self)
        progressBar.minimum = 0
        progressBar.maximum = 100
        GroupboxTech.layout().addWidget(progressBar)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"), MyQuit)

        GroupboxTech.layout().addWidget(quit)

        layoutWindow.addWidget(GroupboxTech)

        #get last server save cfg
        host_text = settings.get_ClientSettingsByName('HostServer')
        if host_text:
            HostLineEdit.setText(host_text)

        bAutorefresh = settings.get_ClientSettingsByName('RefreshQueueBool')
        RefreshQueueToggleBtn.setChecked(bAutorefresh)

        bAdvancedRender = settings.get_ClientSettingsByName('AdvancedRenderBool')
        AdvancedRenderToggleBtn.setChecked(bAdvancedRender)
        onAdvancedRenderToggle()

        if Check_Server():
            GetAllRenderingInfo()
            #Get_Render_Presets()
            #Get_All_Server_Shots()
            #GetQueueJobs()

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
    settings.print_log("Start Py App")
    settings.setup_all_configs_if_need()
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

