import unreal
import sys

from PySide2 import QtWidgets, QtUiTools, QtGui

#Import UE python lib
import m2_unreal.observer as observer
import m2_unreal.set_shot as set_shot


#RELOAD MODULE
import importlib
importlib.reload(observer)
importlib.reload(set_shot)

WINDOW_NAME = 'M2 - Set Shots'
UI_FILE_FULLNAME = __file__.replace('.py', '.ui')

class QtWindowSetShot(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWindowSetShot, self).__init__(parent)
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
        #Set project index to -1, forcing user to select project. Replace by stored current proj (TO DO)
        self.combobox1.setCurrentIndex(-1)
        
        
        #self.project = ''
        #self.episode = ''
        
        #Declare shots dict
        self.shotsDict = {}

        #Make list asset (call asset observer)
        #self.make_list_shots()
        
        #setShotButton
        self.widget.setShotButton.clicked.connect(self.pushButton)

        #update cam Button
        self.widget.updateCamButton.clicked.connect(self.updateCamButton)

        #update anim Button
        self.widget.updateAnimButton.clicked.connect(self.updateAnimButton)

        #update setdress Button
        self.widget.updateSetdressButton.clicked.connect(self.updateSetdressButton)

        self.widget.episode_list_widget.itemSelectionChanged.connect(self.episode_list_sel_change)



    def pushButton(self):
        self.list = self.widget.list_shots.selectedItems()
        for i in self.list:
            shot = i.text()
            #IMPORT ANIM
            #print('Set shot %s / Cut duration : %s' % (shot, self.shotsDict[shot]))
            set_shot.set_shot(self.project, self.episode, shot, cut_duration=self.shotsDict[shot])

    def updateCamButton(self):
        self.list = self.widget.list_shots.selectedItems()
        for i in self.list:
            shot = i.text()
            #Update cam
            print('Update shot %s / Cut duration : %s' % (shot, self.shotsDict[shot]))
            set_shot.update_cam(self.project, self.episode, shot)

    def updateAnimButton(self):
        self.list = self.widget.list_shots.selectedItems()
        for i in self.list:
            shot = i.text()
            
            set_shot.update_anims(self.project, self.episode,shot)

    def updateSetdressButton(self):
        self.list = self.widget.list_shots.selectedItems()
        for i in self.list:
            shot = i.text()

            set_shot.update_setdress(self.project, self.episode, shot)


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



app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

widget = QtWindowSetShot()
widget.show()
unreal.parent_external_window_to_slate(widget.winId())
