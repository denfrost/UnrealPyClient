import sys
import os
import pathlib

import unreal

from PySide2 import QtWidgets, QtUiTools, QtGui

#Import UE python lib
import m2_unreal.observer as observer
import m2_unreal.movie_render as mr
import m2_unreal.config as config


#RELOAD MODULE
import importlib
importlib.reload(observer)
importlib.reload(mr)

WINDOW_NAME = 'M2 - Send Render Job'
UI_FILE_FULLNAME = __file__.replace('.py', '.ui')

class QtWindowSendRenderJobs(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWindowSendRenderJobs, self).__init__(parent)
        self.aboutToClose = None # This is used to stop the tick when the window is closed
        self.widget = QtUiTools.QUiLoader().load(UI_FILE_FULLNAME)
        self.widget.setParent(self)
        self.setWindowTitle(WINDOW_NAME)
        self.setGeometry(100, 100, self.widget.width(), self.widget.height())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)
        #Extend list asset to allow multiple selection
        self.widget.list_shots.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.widget.asset_filter.textChanged.connect(self.filter_asset)
        
        #QComboBox project_comboBox
        self.combobox1 = self.widget.project_comboBox
        self.make_projects_list()
        self.combobox1.currentIndexChanged.connect(self.combo_sel_change)
        self.combobox1.setCurrentIndex(-1)
        
        self.shotsDict = {}

        self.preset_combobox = self.widget.preset_comboBox
        self.make_presets_list()
        
        self.render_checkbox = self.widget.render_checkBox
        self.transfer_checkbox = self.widget.transfer_checkBox

        #send render jobs button
        self.widget.makeJobsButton.clicked.connect(self.send_render_jobs)

        self.widget.episode_list_widget.itemSelectionChanged.connect(self.episode_list_sel_change)

    def send_render_jobs(self):
        
        # clean up th queue
        mr.cleanup_queue()

        self.preset = self.preset_combobox.currentText()
        
        preset_address = f'{config.mp_presets}/{self.preset}.{self.preset}'
        
        user_home_address = os.path.expanduser('~')
        
        self.list = self.widget.list_shots.selectedItems()
        output_folders = []
        for i in self.list:
            
            shot_name = i.text()
            
            sequencer_name = f'{config.shots_path}/{self.episode}/{shot_name}/{shot_name}_SEQ.{shot_name}_SEQ'
            map_name = f'{config.shots_path}/{self.episode}/{shot_name}/{shot_name}.{shot_name}'
            
            # make output folder
            output_folder = user_home_address + f'\LIVE\{self.project}\{self.episode}\COMMON\RENDER\{self.project}_{self.episode}_{shot_name}'
            folder = pathlib.Path(output_folder)
            if not folder.exists ():
                os.makedirs(folder)
            
            
            output_folders.append(output_folder)

            mr.make_render_job(shot_name,sequencer_name, map_name,output_folder,preset_address)

    
        # after making the jobs now render them
        
        do_render = self.render_checkbox.isChecked()
        do_transfer = self.transfer_checkbox.isChecked()

        if do_render:
            mr.render_jobs(output_folders,do_transfer)


    def filter_asset(self):
        text = self.widget.asset_filter.text()
        self.widget.list_shots.clear()
        for key, value in sorted(self.shotsDict.items()):
            if text in key:
                self.widget.list_shots.addItem(key)

    def make_list_shots(self):
        self.shotsDict = observer.make_shot_list(self.project, self.episode)
        self.widget.list_shots.clear()
        for key, value in sorted(self.shotsDict.items()):
            self.widget.list_shots.addItem(key)

    def make_projects_list(self):
        proj_list = observer.make_project_dict()
        
        for proj in proj_list:
            self.combobox1.addItem(proj)

    
    def make_episode_list(self):
        
        if self.project != None:
            episode_list = observer.make_episodes_list(self.project)
        
        self.widget.episode_list_widget.clear()

        for epl in episode_list:
            self.widget.episode_list_widget.addItem(epl)

    
    def combo_sel_change(self):
        self.project = self.combobox1.currentText()
        self.episode = self.widget.episode_list_widget.currentItem()

        if self.project != '':
            unreal.log('Import shot list of project : ' + self.project)
            self.make_episode_list()
            self.make_list_shots()


    def episode_list_sel_change(self):        
        self.project = self.combobox1.currentText()
        selected_items = self.episode = self.widget.episode_list_widget.selectedItems()
        
        if len(selected_items) > 0:
            self.episode = self.widget.episode_list_widget.selectedItems()[0].text()
        else:
            self.episode = ''
        
        self.make_list_shots()


    def make_presets_list(self):
        presets_list = observer.get_presets_list()
        print(presets_list)
        
        self.preset_combobox.addItems(presets_list)

app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

widget = QtWindowSendRenderJobs()
widget.show()
unreal.parent_external_window_to_slate(widget.winId())
