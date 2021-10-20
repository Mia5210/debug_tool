import os,sys
from pathlib import Path
from am_debug import *
from src.common.aml_ini_parser import amlParserIniContainer
from src.common.aml_common_utils  import AmlCommonUtils
from src.common.aml_debug_base_ui import AmlDebugModule
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox



class AmlDebugUi(Ui_MainWindow, QMainWindow):
    terminalLogSignal = pyqtSignal(str, str, int)

    def __init__(self):
        super(AmlDebugUi, self).__init__()
        super().setupUi(self)
        AmlDebugModule.initModule(self)

        #help info ui
        self.terminalLogSignal.connect(self.terminalLog)
        AmlCommonUtils.set_log_func(self.terminalLogSignal.emit)
        self.AmlDebug_tabWidget.currentChanged.connect(self.__tabChange)

    def __tabChange(self):
        AmlCommonUtils.set_current_tab_index(self.AmlDebug_tabWidget.currentIndex())

    def terminalLog(self,log, level = AmlCommonUtils.AML_DEBUG_LOG_LEVEL_D, moduleId=-1):
        AML_MODULE_TEXTBROWSER = {
            AmlCommonUtils.AML_DEBUG_MODULE_HOME: self.AmlHome_textBrowser,
            AmlCommonUtils.AML_DEBUG_MODULE_AUDIO: self.AmlAudio_textBrowser,
            AmlCommonUtils.AML_DEBUG_MODULE_VIDEO: self.AmlVideo_textBrowser,
            AmlCommonUtils.AML_DEBUG_MODULE_CEC: self.AmlCec_textBrowser,
            AmlCommonUtils.AML_DEBUG_MODULE_SYS_OPERATION: self.AmlSysop_textBrowser,
        }
        log = AmlCommonUtils.get_current_time() + ' ' + level + ' ' + log
        #test: when log fail, set the log's color red
        if "Failed," in log :
            log = '<span style=\" color: #ff0000;\">%s</span>' % log
        if moduleId in AML_MODULE_TEXTBROWSER.keys():
            AML_MODULE_TEXTBROWSER[moduleId].append(log)
        else:
            print("[Error] cant not find the module id [" + moduleId + "] \'s textBrowser")

    def closeEvent(self,event):
        print("close event")
        reply = QMessageBox.question(self, 'Amlogic Tips',"Confirm exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            AmlDebugModule.closeEvent()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not Path(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT).exists():
        print(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + "folder does not exist, create it.")
        os.makedirs(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT, 777)
    amlParserIniContainer.initParser()
    ui = AmlDebugUi()
    ui.setWindowIcon(QIcon('res/tool/debug.ico'))
    ui.setWindowTitle("Amlogic Debug Tool")
    ui.show()
    sys.exit(app.exec_())