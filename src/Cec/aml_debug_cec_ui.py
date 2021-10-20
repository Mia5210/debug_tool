from threading import Thread

from src.Cec.aml_ini_parser_cec import AmlParserIniCec
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugCecUi(aml_ui)

#Table: "Cec Debug"
class AmlDebugCecUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugCecUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_CEC)
        self.__adbSetDebugPropList = [
            'echo log.tag.AudioService=DEBUG >> vendor/build.prop',
            'echo log.tag.volume=DEBUG >> vendor/build.prop',
            'echo log.tag.HDMI=DEBUG >> vendor/build.prop',
        ]
        self.__m_logcatEnable = False
        self.__m_bugreportEnable = False

    def init_display_ui(self):
        self.__m_logcatEnable = self.m_iniPaser.getValueByKey(AmlParserIniCec.AML_PARSER_CEC_LOGCAT)
        self.__m_bugreportEnable = self.m_iniPaser.getValueByKey(AmlParserIniCec.AML_PARSER_CEC_BUGREPORT)
        self.m_mainUi.Cec_option_logcat_checkBox.setChecked(self.__m_logcatEnable)
        self.m_mainUi.Cec_option_bugreport_checkBox.setChecked(self.__m_bugreportEnable)

    def signals_connect_slots(self):
        self.m_mainUi.Cec_setprop_btn.clicked.connect(self.__click_setprop)
        self.m_mainUi.Cec_reboot_btn.clicked.connect(AmlCommonUtils.adb_reboot)
        self.m_mainUi.Cec_startDebug_btn.clicked.connect(self.start_capture)
        self.m_mainUi.Cec_StopDebug_btn.clicked.connect(self.stop_capture)
        self.m_mainUi.Cec_option_logcat_checkBox.clicked[bool].connect(self.__click_optionsLogcat)
        self.m_mainUi.Cec_option_bugreport_checkBox.clicked.connect(self.__click_optionsBugreport)

    def closeEvent(self):
        pass

    def __click_optionsLogcat(self, enable):
        self.log.d('logcat')
        if enable:
            self.m_mainUi.Home_logcatOption_checkBox.setChecked(True)
        self.m_iniPaser.setValueByKey(AmlParserIniCec.AML_PARSER_CEC_LOGCAT, enable)

    def __click_optionsBugreport(self, enable):
        self.log.d('check bug report')
        if enable:
            self.m_mainUi.Home_bugreportOption_checkBox.setChecked(True)
        self.m_iniPaser.setValueByKey(AmlParserIniCec.AML_PARSER_CEC_BUGREPORT, enable)

    def __click_setprop(self):
        self.log.d('setprop')
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()
        for cmd in self.__adbSetDebugPropList:
            AmlCommonUtils.exe_adb_shell_cmd(cmd, True)

    def start_capture(self, curTimeName='', homeCallbackFinish='', homeClick=False):
        self.log.d('start capture')
        self.m_mainUi.Cec_startDebug_btn.setEnabled(False)
        self.__m_logcatEnable = self.m_mainUi.Cec_option_logcat_checkBox.isChecked()
        self.__m_bugreportEnable = self.m_mainUi.Cec_option_bugreport_checkBox.isChecked()
        if homeClick:
            self.__nowPullPcTime = curTimeName
            homeCallbackFinish(self.m_moduleId)
        else:
            print('debug')
            self.m_mainUi.Cec_debugOptions_groupBox.setEnabled(False)
            self.__nowPullPcTime = AmlCommonUtils.pre_create_directory(self.m_moduleId)
            self.__nowPullPcPath = AmlCommonUtils.get_path_by_module(self.__nowPullPcTime, self.m_moduleId)
            if self.__m_logcatEnable:
                AmlCommonUtils.adb_root()
                AmlCommonUtils.adb_remount()
                AmlCommonUtils.logcat_start()
        self.m_mainUi.Cec_StopDebug_btn.setEnabled(True)

    def stop_capture(self, homeCallbackFinish='', homeClick=False):
        self.log.d('stop capture')
        self.m_mainUi.Cec_StopDebug_btn.setEnabled(False)
        self.m_mainUi.Cec_operation_groupBox.setEnabled(False)
        self.m_mainUi.Cec_debugOptions_groupBox.setEnabled(False)
        if homeClick:
            AmlCommonUtils.generate_snapshot(self.__nowPullPcPath)
            homeCallbackFinish()
        else:
            thread = Thread(target=self.__stop_capture_thread)
            thread.start()

    def __stop_capture_thread(self):
        self.log.d('stop capture thread')
        if self.__m_logcatEnable:
            AmlCommonUtils.logcat_stop()
            AmlCommonUtils.pull_logcat_to_pc(self.__nowPullPcPath)
        if self.__m_bugreportEnable:
            AmlCommonUtils.bugreport(self.__nowPullPcPath)
        AmlCommonUtils.generate_snapshot(self.__nowPullPcPath)
        self.m_mainUi.Cec_startDebug_btn.setEnabled(True)
        self.m_mainUi.Cec_operation_groupBox.setEnabled(True)
        self.m_mainUi.Cec_debugOptions_groupBox.setEnabled(True)