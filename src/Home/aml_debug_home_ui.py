from threading import Thread
import time, os

from PyQt5.QtCore import QStringListModel

from src.Home.aml_ini_parser_home import AmlParserIniHome
from src.common.aml_debug_base_ui import AmlDebugBaseUi, AmlDebugModule
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugHomeUi(aml_ui)

#Tab:"Home"
class AmlDebugHomeUi(AmlDebugBaseUi):
    class AmlDebugHomeCfg():
        def __init__(self):
            self.m_ModuleEnableArray = dict()
            self.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_HOME] = True
            for index in range(AmlCommonUtils.AML_DEBUG_MODULE_AUDIO, AmlCommonUtils.AML_DEBUG_MODULE_MAX):
                self.m_ModuleEnableArray[index] = False
            self.m_logcatEnable = False
            self.m_bugreportEnable = False
            self.m_dmesgEnable = False
            self.m_captureMode = 0
            self.m_debugTime = 0

    def __init__(self, aml_ui):
        self.__m_debugCfg = AmlDebugHomeUi.AmlDebugHomeCfg()
        super(AmlDebugHomeUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_HOME)
        self.__startFinishCnt = dict()
        self.__stopFinishCnt = dict()
        self.__nowPullPcTimePath = ''
        self.__curTimeName = ''

    def init_display_ui(self):
        captureMode = self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE)
        if captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.Home_menuMode_radioButton.setChecked(True)
            self.m_mainUi.Home_captureTime_groupBox.setEnabled(False)
        elif captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.Home_autoMode_radioButton.setChecked(True)
            self.m_mainUi.Home_captureTime_groupBox.setEnabled(True)
        else:
            self.log.e('init_display_ui: Not supported capture mode:' + str(captureMode) + ' !!!')
        self.m_mainUi.Home_audioModule_checkBox.setChecked(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE))
        self.m_mainUi.Home_videoModule_checkBox.setChecked(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE))
        self.m_mainUi.Home_cecModule_checkBox.setChecked(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE))
        self.m_mainUi.Home_logcatOption_checkBox.setChecked(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_LOGCAT))
        self.m_mainUi.Home_bugreportOption_checkBox.setChecked(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_BUGREPORT))
        self.m_mainUi.Home_dmsgOption_checkBox.setChecked(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_DMESG))
        self.m_mainUi.Home_adbIpAdress_lineEdit.setInputMask('000.000.000.000;_')
        self.m_mainUi.Home_adbIpAdress_lineEdit.setText(
            self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_IP_ADDRESS))
        # others ui setting
        self.m_mainUi.Home_otherModule1_checkBox.setEnabled(False)
        self.m_mainUi.Home_otherModule1_checkBox.setChecked(True)
        self.m_mainUi.Home_otherModule2_checkBox.setEnabled(False)
        self.m_mainUi.Home_otherModule2_checkBox.setChecked(True)
        self.m_mainUi.Home_otherModule3_checkBox.setEnabled(False)
        self.m_mainUi.Home_otherModule3_checkBox.setChecked(True)
        self.m_mainUi.Home_otherModule4_checkBox.setEnabled(False)
        self.m_mainUi.Home_otherModule4_checkBox.setChecked(True)
        self.m_mainUi.Home_allModule_checkBox.setEnabled(False)
        self.m_mainUi.Home_allModule_checkBox.setChecked(True)
        self.m_mainUi.Home_otherOption1_checkBox.setEnabled(False)
        self.m_mainUi.Home_otherOption1_checkBox.setChecked(True)
        self.m_mainUi.Home_otherOption2_checkBox.setEnabled(False)
        self.m_mainUi.Home_otherOption2_checkBox.setChecked(True)
        self.m_mainUi.Home_sourceModule_checkBox.setEnabled(False)
        self.m_mainUi.Home_sourceModule_checkBox.setChecked(True)
        self.m_mainUi.Home_menuMode_radioButton.setEnabled(False)
        self.m_mainUi.Home_captureTime_spinBox.setEnabled(False)
        self.m_mainUi.Home_captureTime_spinBox.setProperty("value", 6)
        self.m_mainUi.Home_stopCapture_btn.setEnabled(False)

    def signals_connect_slots(self):
        #adb device
        self.m_mainUi.Home_adbDevSelect_comboBox.currentTextChanged[str].connect(self.__textChanged_selectAdbDev)
        self.m_mainUi.Home_adbDevRefresh_btn.clicked.connect(self.__click_adbRefresh)
        self.m_mainUi.Home_adbIpConnect_btn.clicked.connect(self.__click_adbConnect)
        self.m_mainUi.Home_adbIpAdress_lineEdit.textChanged.connect(self.__textChanged_adbIpAdress)
        # multi Modules
        self.m_mainUi.Home_audioModule_checkBox.clicked[bool].connect(self.__click_modulesAudio)
        self.m_mainUi.Home_videoModule_checkBox.clicked[bool].connect(self.__click_modulesVideo)
        self.m_mainUi.Home_cecModule_checkBox.clicked[bool].connect(self.__click_modulesCec)
        #self.m_mainUi.Home_allModule_checkBox.clicked[bool].connect(self.__click_modulesAll)
        self.m_mainUi.Home_logcatOption_checkBox.stateChanged[int].connect(self.__changed_optionsLogcat)
        self.m_mainUi.Home_bugreportOption_checkBox.stateChanged[int].connect(self.__changed_optionsBugreport)
        self.m_mainUi.Home_dmsgOption_checkBox.stateChanged[int].connect(self.__changed_optionsDmesg)
        self.m_mainUi.Home_captureTime_spinBox.editingFinished.connect(self.__editingFinished_CaptureTime)
        self.m_mainUi.Home_autoMode_radioButton.clicked.connect(self.__click_auto_mode)
        self.m_mainUi.Home_menuMode_radioButton.clicked.connect(self.__click_manual_mode)
        self.m_mainUi.Home_startCapture_btn.clicked.connect(self.__click_start_capture)
        self.m_mainUi.Home_stopCapture_btn.clicked.connect(self.__click_stop_capture)
        self.m_mainUi.Home_outputDir_btn.clicked.connect(self.__click_open_output)

    def __click_adbRefresh(self):
        self.log.i('refresh btn clicked')
        dev_list = self.__adb_dev_ui_refresh()
        if len(dev_list) > 0:
            cur_dev = self.m_mainUi.Home_adbDevSelect_comboBox.currentText()
            AmlCommonUtils.set_adb_cur_device(cur_dev)
        else:
            AmlCommonUtils.set_adb_cur_device('')

    def __textChanged_selectAdbDev(self, value):
        self.log.d("adbDev textchanged")
        AmlCommonUtils.set_adb_cur_device(value)

    def __textChanged_adbIpAdress(self, value):
        self.log.d("ip adress change : " + value)
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_IP_ADDRESS, value)

    def __click_adbConnect(self):
        self.log.d("adb connect")
        ip = self.m_mainUi.Home_adbIpAdress_lineEdit.text()
        dev_name = AmlCommonUtils.adb_connect_by_ip(ip)
        if dev_name == '':
            return
        self.__adb_dev_ui_refresh()
        self.m_mainUi.Home_adbDevSelect_comboBox.setCurrentText(dev_name)

    def __click_modulesAudio(self, enable):
        self.log.d("click audio module")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE, enable)
    def __click_modulesVideo(self, enable):
        self.log.d("click video module")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE, enable)
    def __click_modulesCec(self, enable):
        self.log.d("click Cec module")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE, enable)
    def __changed_optionsLogcat(self, state):
        self.log.d("change Logcat")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_LOGCAT, self.state_to_bool(state))
    def __changed_optionsBugreport(self, state):
        self.log.d("change Bugreport")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_BUGREPORT, self.state_to_bool(state))
    def __changed_optionsDmesg(self, state):
        self.log.d("change dmesg")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_DMESG, self.state_to_bool(state))
    def __click_auto_mode(self):
        self.log.d("click auto mode")
        self.m_mainUi.Home_captureTime_groupBox.setEnabled(True)
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE, AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO)
    def __click_manual_mode(self):
        self.log.d("click manual mode")
        self.m_mainUi.Home_captureTime_groupBox.setEnabled(False)
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE, AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL)

    def __editingFinished_CaptureTime(self):
        self.log.d("eidt capture time")
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME, self.m_mainUi.Home_captureTime_spinBox.value())

    def __click_start_capture(self):
        self.log.d("start capture time")
        self.m_mainUi.Home_startCapture_btn.setEnabled(False)
        self.m_mainUi.Home_modules_groupBox.setEnabled(False)
        self.m_mainUi.Home_debugOptions_groupBox.setEnabled(False)
        self.m_mainUi.Home_debugMode_groupBox.setEnabled(False)
        self.m_mainUi.Home_captureTime_groupBox.setEnabled(False)
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()
        self.__pre_debug_cfg()
        for module in AmlDebugModule.moduleList:
            self.__startFinishCnt[module.m_moduleId] = False
        for module in AmlDebugModule.moduleList:
            if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                module.start_capture(self.__curTimeName, self.__callback_startFinish, True)



    def __click_stop_capture(self):
        self.log.d("stop capture time")
        self.m_mainUi.Audio_debugStop_btn.setEnabled(False)
        for module in AmlDebugModule.moduleList:
            self.__stopFinishCnt[module.m_moduleId] = False
        for module in AmlDebugModule.moduleList:
            module.stop_capture(self.__callback_stopFinish, True)



    def __click_open_output(self):
        self.log.d("open output")
        os.startfile(self.check_output_path(self.__nowPullPcTimePath))

    def closeEvent(self):
        self.__m_stop_thread = True

    def start_capture(self, curTimeName, homeCallbackFinish, homeClick):
        self.log.i('start_capture')
        self.__curTimeName = AmlCommonUtils.pre_create_directory(self.m_moduleId, self.__m_debugCfg.m_ModuleEnableArray)
        self.__nowPullPcTimePath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__curTimeName
        thread = Thread(target = self.__start_capture_thread, args=(homeCallbackFinish,))
        thread.start()

    def stop_capture(self, homeCallbackFinish):
        self.log.i('stop_capture')
        AmlCommonUtils.logcat_stop()
        AmlCommonUtils.pull_logcat_to_pc(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_dmesgEnable:
            AmlCommonUtils.exe_adb_cmd('pull "' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_DMESG + '" ' + self.__nowPullPcTimePath, True)
        self.log.i('stop_capture')
        homeCallbackFinish(self.m_moduleId)

    def __start_capture_thread(self, homeCallbackFinish):
        if self.__m_debugCfg.m_logcatEnable:
            timeS = self.m_mainUi.Home_captureTime_spinBox.value()
            self.log.i('start_capture logcat start, please wait ' + str(timeS) + 's for logcat...')
            for module in AmlDebugModule.moduleList:
                if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True and module.get_logcat_enable() == True:
                    module.open_logcat()
            if self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
                AmlCommonUtils.logcat_start()
                time.sleep(timeS)
                self.log.i('AmlDebugHomeUi::start_capture logcat stop ++++')
                for module in AmlDebugModule.moduleList:
                    if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True and module.get_logcat_enable() == True:
                        module.close_logcat()
                AmlCommonUtils.logcat_stop()
                AmlCommonUtils.pull_logcat_to_pc(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_bugreportEnable:
            AmlCommonUtils.bugreport(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_dmesgEnable:
            AmlCommonUtils.dmesg()
            AmlCommonUtils.exe_adb_cmd('pull "' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_DMESG + '" ' + self.__nowPullPcTimePath, True)
        self.log.i('-------- [Home] Auto mode capture Finish !!! --------')
        homeCallbackFinish(self.m_moduleId)

    def __callback_startFinish(self, moduleId):
        if moduleId not in self.AML_MODULE_NAME_ARRAY.keys():
            self.log.w(str(moduleId) + ' is invalid...')
            return
        self.__startFinishCnt[moduleId] = True
        self.log.i('__callback_startFinish ' + self.AML_MODULE_NAME_ARRAY[moduleId] + '[' + str(moduleId) + ']')
        for module in AmlDebugModule.moduleList:
            if self.__startFinishCnt[module.m_moduleId] == False and self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                return
        self.log.i('[Home] Please send folder ' + self.__nowPullPcTimePath + ' to RD colleagues! Thank You!')
        if self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.Home_modules_groupBox.setEnabled(True)
            self.m_mainUi.Home_debugOptions_groupBox.setEnabled(True)
            self.m_mainUi.Home_debugMode_groupBox.setEnabled(True)
            self.m_mainUi.Home_captureTime_groupBox.setEnabled(True)
            self.m_mainUi.Home_startCapture_btn.setEnabled(True)
            AmlCommonUtils.generate_snapshot(self.__nowPullPcTimePath)
            self.log.i('######## [All Module] Auto mode capture Finish !!! ############')
        elif self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.Home_stopCapture_btn.setEnabled(True)
            self.log.i('######## [All Module] Manual mode Start capture finish !!! ############')

    def __callback_stopFinish(self, moduleId):
        self.log.i('__callback_stopFinish ' + self.AML_MODULE_NAME_ARRAY[moduleId] + '[' + str(moduleId) + ']')
        self.__stopFinishCnt[moduleId] = True
        for module in AmlDebugModule.moduleList:
            if self.__stopFinishCnt[module.m_moduleId] == False and self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                self.log.i('__callback_stopFinish: return m_moduleId:' + str(module.m_moduleId))
                return
        AmlCommonUtils.generate_snapshot(self.__nowPullPcTimePath)
        self.log.i('######## [All Module] Manual mode capture Finish !!! ############')
        self.m_mainUi.Home_modules_groupBox.setEnabled(True)
        self.m_mainUi.Home_debugOptions_groupBox.setEnabled(True)
        self.m_mainUi.Home_debugMode_groupBox.setEnabled(True)
        self.m_mainUi.Home_startCapture_btn.setEnabled(True)

    def __pre_debug_cfg(self):
        if self.m_mainUi.Home_autoMode_radioButton.isChecked() == True:
            self.__m_debugCfg.m_captureMode = AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_mainUi.Home_menuMode_radioButton.isChecked() == True:
            self.__m_debugCfg.m_captureMode = AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.log.e('__pre_debug_cfg: Not supported capture mode!!!')
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_AUDIO] = self.m_mainUi.Home_audioModule_checkBox.isChecked()
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_VIDEO] = self.m_mainUi.Home_videoModule_checkBox.isChecked()
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_CEC] = self.m_mainUi.Home_cecModule_checkBox.isChecked()
        self.__m_debugCfg.m_logcatEnable = self.m_mainUi.Home_logcatOption_checkBox.isChecked()
        self.__m_debugCfg.m_bugreportEnable = self.m_mainUi.Home_bugreportOption_checkBox.isChecked()
        self.__m_debugCfg.m_dmesgEnable = self.m_mainUi.Home_dmsgOption_checkBox.isChecked()
        self.__m_debugCfg.m_debugTime = self.m_mainUi.Home_captureTime_spinBox.value()

    def __adb_dev_ui_refresh(self):
        dev_list = AmlCommonUtils.get_adb_devices()
        self.m_mainUi.Home_adbDevSelect_comboBox.clear()
        if len(dev_list) > 0:
            self.m_mainUi.Home_adbDevSelect_comboBox.addItems(dev_list)
        listModel = QStringListModel()
        listModel.setStringList(dev_list)
        self.m_mainUi.Home_adbDev_listView.setModel(listModel)
        return dev_list