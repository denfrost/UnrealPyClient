import unreal
import sys

from PySide2 import QtWidgets, QtUiTools, QtGui

#Import UE python lib
#import ui.qwidget_import_asset as q_import_asset

# RELOAD MODULE
import importlib

sys.path.append('C:/UE4JOB/M2Animation/SCRIPTS_UNREAL')
sys.path.append('C:/UE4JOB/M2Animation/SCRIPTS_UNREAL/m2_unreal')
sys.path.append('C:/UE4JOB/M2Animation/SCRIPTS_UNREAL/ui')

WINDOW_NAME = 'M2 - Menu'
UI_FILE_FULLNAME = __file__.replace('.py', '.ui')

class QtWindowImport(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWindowImport, self).__init__(parent)
        self.aboutToClose = None  # This is used to stop the tick when the window is closed
        self.widget = QtUiTools.QUiLoader().load(UI_FILE_FULLNAME)
        self.widget.setParent(self)
        self.setWindowTitle(WINDOW_NAME)
        self.setGeometry(100, 100, self.widget.width(), self.widget.height())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)
        
        # importAssetButton
        self.widget.importAssetButton.clicked.connect(self.importAssetButton)

        # importAnimsButton
        self.widget.importAnimsButton.clicked.connect(self.importAnimButton)

        # setShotButton
        self.widget.setShotButton.clicked.connect(self.setShotButton)
        
        # make render jobs button
        self.widget.sendRenderButton.clicked.connect(self.makeRenderJobsButton)


        # export to meme
        self.widget.exportMemeButton.clicked.connect(self.exportMemeButton)

        # importLodButton
        self.widget.importLodButton.clicked.connect(self.importLodButton)

        # export set button
        self.widget.exportSetButton.clicked.connect(self.exportSetButton)

        # turntable button
        self.widget.makeTurntableButton.clicked.connect(self.makeTurntableButton)



    def importAssetButton(self):
        #import ui.qwidget_import_asset as q_import_asset
        #importlib.reload(q_import_asset)
        import ui.q_global_import_asset as q_import_asset
        importlib.reload(q_import_asset)

    def importAnimButton(self):
        import ui.q_import_anim as q_import_anim
        importlib.reload(q_import_anim)

    def setShotButton(self):
        import ui.q_set_shot as q_setShot
        importlib.reload(q_setShot)


    def makeRenderJobsButton(self):
        import ui.q_send_render_jobs as q_render
        importlib.reload(q_render)

    def exportMemeButton(self):
        import ui.q_export_to_meme as q_exp_meme
        importlib.reload(q_exp_meme)
    
    def importLodButton(self):
        import ui.q_import_lods as q_importlod
        importlib.reload(q_importlod)

    def exportSetButton(self):
        import ui.q_export_set as q_export_set
        importlib.reload(q_export_set)

    def makeTurntableButton(self):
        import ui.q_make_turntable as q_make_turntable
        importlib.reload(q_make_turntable)

app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

widget = QtWindowImport()
widget.show()
unreal.parent_external_window_to_slate(widget.winId())
