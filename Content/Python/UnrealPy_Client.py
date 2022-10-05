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

#Repeater on Threading
import threading
stopFlag_MyThread = threading.Event()

Server = "ws://"+"10.66.7.80:30020"

#describe calls checking umap, uasset.
Json_RequestServerRemoteFunctions =\
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/describe",
        "Verb": "PUT",
        "Body": {
            "ObjectPath": "/Engine/PythonTypes.Default__SamplePythonBlueprintLibrary",
            "functionName": "python_test_bp_action_return",
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

        def SendSocket(HostServer, Json_request, ServerAnswered):
            try:
                ws = create_connection(HostServer)
            except:
                print('')
                print('WS Server offline : ' + HostLineEdit.text())
                return
            print("Sending Command to Server : " + HostServer)
            ws.send(Json_request)
            print("Sent")
            print("Receiving...")
            result = ws.recv()
            print("Received from Server '%s'" % result)
            server_str = "'%s'" % result
            ServerAnswered(server_str)
            ws.close()

        @QtCore.Slot()
        def SendCommand():
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, JsonTextEdit.toPlainText(), ServerAnswered) #Send Json to Unreal

        def ServerAnswered(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'ServerAnswered')
            print("Got Server Answer")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            TabWidgetCommands.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredGetAllShots(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'GetAllShots')
            print("Got Server Answer : Getallshots")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            TabWidgetCommands.setCurrentIndex(1)
            FillShots(feedback)
            progressBar.setValue(70)
            progressBar.setValue(100)
            # Ask about Rendering Movie  status
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()


        def ServerAnsweredSetShotRender(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'SetShotRender')
            print("Got Server Answer : SetShotRender")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            TabWidgetCommands.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredMakeRenderJob(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'MakeRenderJob')
            print("Got Server Answer : MakeRenderJob")
            tanswer = dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer + " : " + feedback)  # JsonTextEdit.toPlainText()
            TabWidgetCommands.setCurrentIndex(1)
            progressBar.setValue(100)

        def ServerAnsweredPerforce(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'AnsweredPerforce')
            print("Got Server Answer : Try Update server")
            tanswer =dt.now().strftime("%H:%M:%S")
            tused = dt.now()-trequest
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback) #JsonTextEdit.toPlainText()
            TabWidgetCommands.setCurrentIndex(1)
            PerforceLabel.setText("Perforce Updated : "+tanswer + '[' +str(tused) + ']')
            progressBar.setValue(100)

        def ServerAnsweredGetAllQueueJobs(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'GetAllQueueJobs')
            print("Got Server Answer : GetAllQueueJobs")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)
            #Fill Queue Combobox
            FillQueueJobs(feedback)
            comboBoxQueue.setCurrentIndex(0)
            progressBar.setValue(70)
            progressBar.setValue(100)
            #Ask about Rendering Movie  status
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()

        def ServerAnsweredDeleteRenderJob(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'DeleteRenderJob')
            print("Got Server Answer : DeleteRenderJob")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)
            progressBar.setValue(70)
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('DeleteRenderJob Clean Data :'+cleandata)
            progressBar.setValue(100)
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()


        def ServerAnsweredDeleteAllRenderJobs(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'DeleteAllRenderJobs')
            print("Got Server Answer : DeleteAllRenderJobs")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)
            progressBar.setValue(70)
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('DeleteRenderJob Clean Data :'+cleandata)
            progressBar.setValue(100)
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()

        def ServerAnsweredGetRemoteInfo(feedback):
            r_code = feedback.split('"ResponseCode":')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'GetRemoteInfo')
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean Data :'+cleandata)
            cleandata = cleandata.replace('\\', '')
            print("Clean feedback :"+cleandata)
            json_remote_data = json.loads(cleandata)

            print("Got Server Answer : GetRemoteInfo")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.setText(ServerAnswerTextEdit.toPlainText() + '  ' + tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)
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
            currentIndex = comboBoxQ.currentIndex()
            tanswer =dt.now().strftime("%H:%M:%S")
            TabWidgetCommands.setCurrentIndex(1)
            list_presets = cleandata.split(',')
            work_list_presets = []
            comboBoxQ.clear()
            for p in  list_presets:
                if 'Render' in p:
                    work_list_presets.append(p)
                    comboBoxQ.addItem(p)
            comboBoxQ.setCurrentIndex(currentIndex)

        def UpdateQueueJobs(cleandata):
            if len(cleandata) == 0:
                comboBoxQueue.clear()
                comboBoxQueue.addItem("EMPTY")
                return
            currentIndex = comboBoxQueue.currentIndex()
            res = cleandata.split(",")
            res.sort()
            comboBoxQueue.clear()
            current_project = settings.get_Current_project()
            print('Start Sorting for Project :'+current_project)
            for i, name in enumerate(res):
                print('Feedback ['+str(i)+']: '+res[i])
                if (res[i].find(current_project) > -1):
                    comboBoxQueue.addItem("" + res[i])
            if currentIndex < 0:
                comboBoxQueue.setCurrentIndex(0)
            else:
                comboBoxQueue.setCurrentIndex(currentIndex)

        def ServerAnsweredGetAllRenderingInfo(feedback):
            r_code = feedback.split('"ResponseCode": ')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'GetAllRenderingInfo')
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean Data :'+cleandata)
            cleandata = cleandata.replace('\\', '')
            print("Clean feedback :"+cleandata)
            json_remote_data = json.loads(cleandata)

            print("Got Server Answer : GetAllRenderingInfo")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(ServerAnswerTextEdit.toPlainText() + '  ' + tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)

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

        def ServerAnsweredGetMyRenderingInfo(feedback):
            print('ServerAnsweredGetMyRenderingInfo')
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean Data :'+cleandata)
            cleandata = cleandata.replace('\\', '')
            print("Clean feedback :"+cleandata)
            json_remote_data = json.loads(cleandata)
            print("Got Server Answer : GetAllRenderingInfo")
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(ServerAnswerTextEdit.toPlainText() + '  ' + tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)

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
            #progressBar.setValue(100)


        def ServerAnsweredStartRenderJobs(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            r_code = feedback.split('"ResponseCode": ')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code+':'+cleandata, 'StartRenderJobs')
            print('RenderJobs Clean Data :' + cleandata)
            GetAllRenderingInfo()

        def ServerAnsweredGetRenderPresets(feedback):
            r_code = feedback.split('"ResponseCode": ')[-1].split(',')[0]
            UpdateStatusOnline(HostLineEdit.text(), r_code, 'GetRenderPresets')
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('GetRenderPresets Clean Data :' + cleandata)
            currentIndex = comboBoxQ.currentIndex()
            if len(cleandata) == 0:
                comboBoxQueue.clear()
                comboBoxQueue.addItem("EMPTY")
                return
            tanswer =dt.now().strftime("%H:%M:%S")
            ServerAnswerTextEdit.clear()
            ServerAnswerTextEdit.setText(tanswer+" : "+feedback)
            TabWidgetCommands.setCurrentIndex(1)
            list_presets = cleandata.split(',')
            work_list_presets = []
            comboBoxQ.clear()
            for p in  list_presets:
                if 'Render' in p:
                    work_list_presets.append(p)
                    comboBoxQ.addItem(p)
            comboBoxQ.setCurrentIndex(currentIndex)


        def UpdateStatusOnline(server_str, response_code, func_name):
            StatusLabel.setStyleSheet("QLabel { color : green; }")
            StatusLabel.setText("Unreal Server Status Online : " + server_str)
            if '200' in response_code:
                if 'Error.' not in response_code:
                    Result = func_name+" - Succes[" + response_code+"]"
                    AnswerServerLabel.setText("Answer Server : " + Result)
                    print("Answer Server : "+Result)
                    AnswerServerLabel.setStyleSheet("QLabel { color : green; }")
                    settings.set_ClientSettingsByName('HostServer', HostLineEdit.text())
                else:
                    AnswerServerLabel.setText("Answer Server : "+func_name+" - Failed[" + response_code+"]")
                    print("Answer Server : "+func_name+" - Failed[" + response_code+"]")
                    AnswerServerLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")
            else:
                StatusLabel.setText("Unreal Server Status Online : " + server_str+" Failed communicated")

        def UpdateStatusOffline(server_str, response_code, func_name):
            StatusLabel.setStyleSheet("QLabel { background-color : yellow; color : red; }")
            StatusLabel.setText("Unreal Server Status Offline : " + server_str)
            AnswerServerLabel.setText("Answer Server : Failed[" + response_code + "]")
            AnswerServerLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")

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
            TabWidgetCommands.setCurrentIndex(0)
            JsonTextEdit.setText(json.dumps(Json_RequestGetAllShots))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllShots) #Send Json to Unreal


        def FillShots(feedback):
            res = feedback.split(",")
            res.sort()
            print(res[1])
            currentIndex = comboBox.currentIndex()
            print('FillShots: Filtered and Sorted.')
            comboBox.clear()
            listing.clear()
            for i, name in enumerate(res):
                #print('Feedback ['+str(i)+']: '+res[i])
                if (res[i].find('_SEQ') > 0) & (res[i].find('Game/SHOTS') > 0):
                    mlist = res[i].split('.')[-1].split('_')
                    if len(mlist) == 2:
                        #if 'ANIM_SEQ' not in res[i]: #_Anim_SEQ ignore
                        comboBox.addItem("" + res[i])
                        listing.addItem("" + res[i])
            comboBox.setCurrentIndex(currentIndex)
            listing.setMaximumHeight(200)

        def FillQueueJobs(feedback):
            cleandata = feedback.split('"ReturnValue": "')[-1].split('"\\r\\n}\\r\\n}''')[0]
            print('Clean :'+cleandata)
            print(len(cleandata))
            if len(cleandata) == 0:
                comboBoxQueue.clear()
                comboBoxQueue.addItem("EMPTY")
                return
            currentIndex = comboBoxQueue.currentIndex()
            res = cleandata.split(",")
            res.sort()
            comboBoxQueue.clear()
            current_project = settings.get_Current_project()
            print('Start Sorting for Project :'+current_project)
            for i, name in enumerate(res):
                print('Feedback ['+str(i)+']: '+res[i])
                if (res[i].find(current_project) > -1):
                    comboBoxQueue.addItem("" + res[i])
            if currentIndex < 0:
                comboBoxQueue.setCurrentIndex(0)
            else:
                comboBoxQueue.setCurrentIndex(currentIndex)

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
            TabWidgetCommands.setCurrentIndex(0)
            print("SetShotRender ")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, json.dumps(Json_RequestSetShotRender), ServerAnsweredSetShotRender)

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
            TabWidgetCommands.setCurrentIndex(0)
            print("Sending....")
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, json.dumps(Json_RequestMakeRenderJob), ServerAnsweredMakeRenderJob)

        def StartRenderJobs(job_name):
            Json_RequestStartRenderJob["Parameters"]["Body"]["parameters"]["sJobName"] = job_name
            JsonTextEdit.setText(json.dumps(Json_RequestStartRenderJob))
            TabWidgetCommands.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, json.dumps(Json_RequestStartRenderJob), ServerAnsweredStartRenderJobs)

        def Get_Render_Presets():
            JsonTextEdit.setText(json.dumps(Json_RequestGetRenderPresets))
            TabWidgetCommands.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, json.dumps(Json_RequestGetRenderPresets), ServerAnsweredGetRenderPresets)

        @QtCore.Slot()
        def MakeRenderJob():
            MakeImagesTool(comboBox.currentText(), comboBoxQ.currentText(), CheckTransferToggleBtn.isChecked())
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()

        @QtCore.Slot()
        def StartRendering():
            job_name = comboBoxQueue.currentText().split('-')[0]
            print('Try Start Rednering : '+job_name)
            StartRenderJobs(job_name)
            if (RefreshQueueToggleBtn.isChecked()): GetAllRenderingInfo()

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
            #SendJsonSocket(Json_RequestServerRemoteFunctions)
            #SendJsonSocket(Json_RequestRemoteInfo)

        def Check_Server():
            progressBar.setValue(0)
            try:
                conn = create_connection(HostLineEdit.text(), 5)
            except:
                conn = False
            if not conn:
                    print('WS Server offline : ' + HostLineEdit.text())
            ChangeStatus(bool(conn))
            return conn

        def SendJsonSocket(hostServer, json_string):
            progressBar.setValue(0)
            print("Sending Command to Server : " + hostServer)
            conn = create_connection(HostLineEdit.text(), 5)
            if not conn:
                print('WS Server offline : '+HostLineEdit.text())
                return
            print('WS Connected : '+str(conn))
            conn.send(json.dumps(json_string))
            print('WS Send : ' + str(json.dumps(json_string)))
            print("Receiving...")
            answer = str(conn.recv())
            print("Received from Server '%s'" % answer)
            UrlType = json_string['Parameters']['Url']
            if UrlType == "/remote/object/describe":
                RawJsonDescribeAnswer(answer)
            elif UrlType == "/remote/object/call":
                TypeFunction =  json_string['Parameters']['Body']['functionName']
                if TypeFunction == 'unreal_python_get_info_remote':
                    ServerAnsweredGetRemoteInfo(answer)
                elif TypeFunction == 'unreal_python_get_all_rendering_info':
                    ServerAnsweredGetAllRenderingInfo(answer)


        def RawJsonDescribeAnswer(feedback):
            clean1 = feedback.replace('\\r\\n\\t', '')
            clean2 = clean1.replace('\\t', '')
            clean2 = clean2.replace('\\r\\n', '')
            clean2data = clean2.replace("b'{", '{')
            clean2data = clean2data[:-1:]
            print('Json_data_ready :' +clean2data)
            json_remote_data = json.loads(clean2data)
            print('ResponseCode : '+str(json_remote_data['ResponseCode']))
            ClassName = json_remote_data['ResponseBody']['Class']
            BodyData = json_remote_data['ResponseBody']
            FuncList = json_remote_data['ResponseBody']['Functions']
            print('ResponseBody : %s ' % BodyData)
            settings.print_log('Available Unreal Python Function for Remote :')
            print('Available Unreal Python Function for Remote :')
            for d in FuncList:
                print(d)
                settings.print_log(d['Name'])


        @QtCore.Slot()
        def ChangeStatus(check):
            tm = dt.now().strftime("%H:%M:%S")
            print('Change Status : '+str(check))
            if check:
                UpdateStatusOnline(HostLineEdit.text() + ' ' + tm, '200', 'CheckServer')
                progressBar.setValue(100)
            else:
                UpdateStatusOffline(HostLineEdit.text() + ' ' + tm, '-1', 'CheckServer')

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
            TabWidgetCommands.setCurrentIndex(0)
            progressBar.setValue(50)
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, json.dumps(Json_UpdatePerforce), ServerAnsweredPerforce)

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
            SendSocket(HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllQueueJobs) #Send Json to Unreal

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
            TabWidgetCommands.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            progressBar.setValue(0)
            progressBar.setValue(50)
            SendSocket(HostServer, json.dumps(Json_RequestDeleteRenderJob), ServerAnsweredDeleteRenderJob)

        @QtCore.Slot()
        def DeleteAllRenderJobs():
            JsonTextEdit.setText(json.dumps(Json_RequestDeleteAllRenderJobs))
            TabWidgetCommands.setCurrentIndex(0)
            HostServer = HostLineEdit.text()
            progressBar.setValue(0)
            progressBar.setValue(50)
            SendSocket(HostServer, json.dumps(Json_RequestDeleteAllRenderJobs), ServerAnsweredDeleteAllRenderJobs)

        @QtCore.Slot()
        def GetRemoteInfo():
            print('GetRemoteInfo')
            JsonTextEdit.setText(json.dumps(Json_RequestRemoteInfo))
            progressBar.setValue(0)
            progressBar.setValue(50)
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            SendSocket(HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetRemoteInfo) #Send Json to Unreal

        @QtCore.Slot()
        def GetAllRenderingInfo():
            print('GetAllRenderingInfo')
            BeforeSendClearUI()
            #AnswerServerLabel.setText("Answer Server : waiting...")
            JsonTextEdit.setText(json.dumps(Json_RequestRemoteAllRenderingInfo))
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            #SendJsonSocket(HostServer, Json_RequestRemoteAllRenderingInfo)
            SendSocket(HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetAllRenderingInfo) #Send Json to Unreal

        def BeforeSendClearUI():
            progressBar.setValue(0)
            progressBar.setValue(50)

        def GetMyRenderingInfo():
            print('GetMyRenderingInfo')
            JsonTextEdit.setText(json.dumps(Json_RequestRemoteAllRenderingInfo))
            print("Send Command To Server :"+JsonTextEdit.toPlainText())
            HostServer = HostLineEdit.text()
            #SendJsonSocket(HostServer, Json_RequestRemoteAllRenderingInfo)
            SendSocket(HostServer, JsonTextEdit.toPlainText(), ServerAnsweredGetMyRenderingInfo) #Send Json to Unreal

        @QtCore.Slot()
        def StartThread():
            stopFlag_MyThread.clear()
            thread = MyThread(stopFlag_MyThread)
            thread.start()

        def StopThread():
            print('Thread Stop work')
            stopFlag_MyThread.set()

        @QtCore.Slot()
        def MyQuit():
            stopFlag_MyThread.set()
            app.quit()

        QtWidgets.QWidget.__init__(self, parent)
        versiondate = settings.get_ClientSettingsByName('ClientRevisionDate')
        self.setWindowTitle("Unreal Websocket Client version:"+versiondate)

        layoutVerticalWindow = QtWidgets.QVBoxLayout()
        self.setLayout(layoutVerticalWindow)


        GroupboxLabel = QtWidgets.QGroupBox("")
        hboxLabel = QtWidgets.QHBoxLayout()
        StatusLabel = QtWidgets.QLabel("Unreal Server Status:")
        StatusLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        StatusLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")
        StatusLabel.setFixedHeight(40)
        GroupboxLabel.setFixedHeight(60)
        GroupboxLabel.setLayout(hboxLabel)

        AnswerServerLabel = QtWidgets.QLabel("AnswerServer: Failed")
        AnswerServerLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        AnswerServerLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")

        GroupboxLabel.layout().addWidget(StatusLabel)
        GroupboxLabel.layout().addWidget(AnswerServerLabel)
        layoutVerticalWindow.addWidget(GroupboxLabel)

        GroupboxStatus = QtWidgets.QGroupBox("Server Status")
        GroupboxStatus.setAlignment(100)
        GroupboxStatus.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        hboxStatus = QtWidgets.QHBoxLayout()
        GroupboxStatus.setFixedHeight(80)

        GroupboxStatus.setLayout(hboxStatus)
        layoutVerticalWindow.addWidget(GroupboxStatus)

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
        layoutVerticalWindow.addWidget(GroupboxSendCommands)

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
        layoutVerticalWindow.addWidget(JsonTextEdit)

        ServerAnswerTextEdit = QtWidgets.QTextEdit('Feedback from server')
        ServerAnswerTextEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Medium))
        layoutVerticalWindow.addWidget(ServerAnswerTextEdit)

        TabWidgetCommands = QtWidgets.QTabWidget()
        TabWidgetCommands.addTab(JsonTextEdit, "Command Client")
        TabWidgetCommands.addTab(ServerAnswerTextEdit, "Answer Server")
        GroupboxSendCommands.layout().addWidget(TabWidgetCommands)

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
        hboxRenderingSettings = QtWidgets.QHBoxLayout()
        hboxRenderingSettings.setAlignment(QtCore.Qt.AlignLeft)
        GroupboxRenderingSettings.setFixedHeight(80)
        GroupboxRenderingSettings.setLayout(hboxRenderingSettings)

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
        hboxFilterSequences.setAlignment(QtCore.Qt.AlignLeft)
        GroupboxFilterSequences.setLayout(hboxFilterSequences)

        GroupboxFoundSequences = QtWidgets.QGroupBox("Server Sequences")
        GroupboxFoundSequences.setChecked(True)
        vboxSequences = QtWidgets.QVBoxLayout()
        GroupboxFoundSequences.setFixedHeight(180)
        GroupboxFoundSequences.setLayout(vboxSequences)


        FilterToggleBtn = QtWidgets.QCheckBox("Filter")
        #FilterToggleBtn.setStyleSheet("QCheckBox{spacing: 5px;}")
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
        hboxRenderingSettings = QtWidgets.QHBoxLayout()
        GroupboxPerforce.setFixedHeight(80)
        GroupboxPerforce.setLayout(hboxRenderingSettings)

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
        GroupboxAdvancedRender.setFixedHeight(80)

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

        def renderTabUI(self):
            renderTab = QWidget()
            genlayout = QVBoxLayout()
            GetInfoBtn3 = QtWidgets.QPushButton("Get All Rendering Info")
            GetInfoBtn3.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
            self.connect(GetInfoBtn3, QtCore.SIGNAL("clicked()"), GetAllRenderingInfo)
            genlayout.addWidget(GetInfoBtn3)
            genlayout.addWidget(GroupboxMain)
            renderTab.setLayout(genlayout)
            return renderTab
        def importTabUI(self):
            importTab = QWidget()
            return importTab
        def clientTabUI(self):
            clientTab = QWidget()
            return clientTab

        TabsMain = QTabWidget()
        TabsMain.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        renderTab = TabsMain.addTab(renderTabUI(self), "Rendering pipeline")
        importTab = TabsMain.addTab(importTabUI(self), "Importing pipeline")

        #experimentTabUI
        experimentTab = QWidget()
        ThreadHlayout = QHBoxLayout()
        StartThreadBtn = QtWidgets.QPushButton("Start Thread timer")
        StartThreadBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(StartThreadBtn, QtCore.SIGNAL("clicked()"), StartThread)
        IntervalTimeLabel = QtWidgets.QLabel('IntervalTime')
        IntervalTimeLineEdit = QtWidgets.QLineEdit('15')
        StopThreadBtn = QtWidgets.QPushButton("Stop Thread")
        StopThreadBtn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(StopThreadBtn, QtCore.SIGNAL("clicked()"), StopThread)
        ThreadHlayout.addWidget(StartThreadBtn)
        ThreadHlayout.addWidget(IntervalTimeLabel)
        ThreadHlayout.addWidget(IntervalTimeLineEdit)
        ThreadHlayout.addWidget(StopThreadBtn)
        experimentTab.setLayout(ThreadHlayout)

        TabsMain.addTab(experimentTab, "Experimental pipeline")

        clientTab = TabsMain.addTab(clientTabUI(self), "Client")
        TabsMain.setTabEnabled(1, False)
        #TabsMain.setTabEnabled(2, False)
        TabsMain.setCurrentIndex(0)

        layoutVerticalWindow.addWidget(TabsMain)

        #layoutVerticalWindow.addWidget(GroupboxMain)

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

        layoutVerticalWindow.addWidget(GroupboxTech)

        #get last server save cfg
        host_text = settings.get_ClientSettingsByName('HostServer')
        if host_text:
            HostLineEdit.setText(host_text)
        print('Set IP from config: '+host_text)

        bAutorefresh = settings.get_ClientSettingsByName('RefreshQueueBool')
        RefreshQueueToggleBtn.setChecked(bAutorefresh)

        bAdvancedRender = settings.get_ClientSettingsByName('AdvancedRenderBool')
        AdvancedRenderToggleBtn.setChecked(bAdvancedRender)
        onAdvancedRenderToggle()

        AnsweredServerList = ['empty', 'empty']
        Check_Server()
        GetAllRenderingInfo()
            #Get_Render_Presets()
            #Get_All_Server_Shots()
            #GetQueueJobs()

        print('First StartUp Py App Done!')
        print('Make Thread Timer for HeartBeat App')

        class MyThread(threading.Thread):
            global startuptime
            startuptime = dt.now()
            def __init__(self, event):
                threading.Thread.__init__(self)
                self.stopped = event
                print("my thread work ["+IntervalTimeLineEdit.text()+"]: " + str(dt.now()))
            def run(self):
                while not self.stopped.wait(int(IntervalTimeLineEdit.text())):
                    print("Unreal Py App working : " + str(dt.now()-startuptime))
                    # call a function
                    #GetAllRenderingInfo()
                    GetMyRenderingInfo()

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

def Checkgitversion():
    import subprocess
    Major_version = 'cl 1.0.0'
    #process = subprocess.Popen(['git', 'rev-parse', 'HEAD'], shell=False, stdout=subprocess.PIPE)
    try:
        output = subprocess.check_output(["git", "log", '-n 1'])
        outputall = subprocess.check_output(["git", "log"])
    except Exception as e:
        print('Failed. Reason: %s' % e)
        return ''
    cl_rev = len(str(outputall).split('commit'))
    #git_head = process.communicate()
    #print(output.strip().decode())
    strOut = output.strip().decode()
    version_date = ' Revision [' + Major_version +str(cl_rev)+']'+strOut.split('Date:')[-1].split('\n\n')[0]
    return version_date

def stop_MyThread():
    stopFlag_MyThread.set()

if __name__ == "__main__":
    print("Start Py App")
    RevisionDate = Checkgitversion()
    if len(RevisionDate) > 0:
        print('Revision version:'+RevisionDate)
        settings.set_ClientSettingsByName('ClientRevisionDate', RevisionDate)
    else:
        RevisionDate = settings.get_ClientSettingsByName('ClientRevisionDate')
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

print("Connect to Unreal websocket : "+settings.get_ClientSettingsByName('HostServer'))
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()

app.aboutToQuit.connect(stop_MyThread) #for force quit app by user stop Thread

widget = MyWidget()
widget.show()
print("Py App done...")

if app:
    sys.exit(app.exec_())  # for Windows external launch
if "unreal" in dir():
    import unreal
    unreal.parent_external_window_to_slate(widget.winId())

