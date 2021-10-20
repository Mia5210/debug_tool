from threading import Thread
import time
import traceback
from src.System_operation.aml_ini_parser_sys_operation import AmlParserIniSysOperation
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugSystemOperationUi(aml_ui)


# Table: "System Operation"
class AmlDebugSystemOperationUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugSystemOperationUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_SYS_OPERATION)
        self.__m_stop_thread = False

    def init_display_ui(self):
        self.m_mainUi.System_PushDolbySrc_lineEdit.setText(
            self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH))
        self.m_mainUi.System_PushDtsSrc_lineEdit.setText(
            self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH))
        self.m_mainUi.System_PushMs12Src_lineEdit.setText(
            self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH))
        self.m_mainUi.System_PushDolbyDtsDst_lineEdit.setText(
            self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH))
        self.m_mainUi.System_PushMs12Dst_lineEdit.setText(
            self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH))
        for i in range(1, 5):
            eval('self.m_mainUi.System_PushCustom' + str(i) + 'Src_lineEdit'). \
                setText(self.m_iniPaser.getValueByKey(
                eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_SRC_PATH')))
            eval('self.m_mainUi.System_PushCustom' + str(i) + 'Dst_lineEdit'). \
                setText(self.m_iniPaser.getValueByKey(
                eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_DST_PATH')))
        for i in range(1, 5):
            eval('self.m_mainUi.System_PullCustom' + str(i) + 'Src_lineEdit'). \
                setText(self.m_iniPaser.getValueByKey(
                eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_SRC_PATH')))
            eval('self.m_mainUi.System_PullCustom' + str(i) + 'Dst_lineEdit'). \
                setText(self.m_iniPaser.getValueByKey(
                eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_DST_PATH')))

    def signals_connect_slots(self):
        self.m_mainUi.System_PushDolbyDtsPush_Button.clicked.connect(self.__click_push_dst_dolby)
        self.m_mainUi.System_PushMs12Push_Button.clicked.connect(self.__click_push_ms12)
        self.m_mainUi.Sys_Push_remount_btn.clicked.connect(self.__click_remount)
        self.m_mainUi.Sys_Pull_remount_btn.clicked.connect(self.__click_remount)
        self.m_mainUi.Sys_Push_reboot_btn.clicked.connect(AmlCommonUtils.adb_reboot)
        self.m_mainUi.Sys_Pull_reboot_btn.clicked.connect(AmlCommonUtils.adb_reboot)
        self.m_mainUi.Sys_Push_closeAVB_btn.clicked.connect(self.__click_close_avb)
        self.m_mainUi.Sys_Pull_closeAVB_btn.clicked.connect(self.__click_close_avb)
        self.m_mainUi.System_PushDolbySrc_lineEdit.editingFinished.connect(self.__finished_PushDolbySrc)
        self.m_mainUi.System_PushDtsSrc_lineEdit.editingFinished.connect(self.__finished_PushDtsSrc)
        self.m_mainUi.System_PushMs12Src_lineEdit.editingFinished.connect(self.__finished_PushMs12Src)
        self.m_mainUi.System_PushDolbyDtsDst_lineEdit.editingFinished.connect(self.__finished_PushDolbyDtsDst)
        self.m_mainUi.System_PushMs12Dst_lineEdit.editingFinished.connect(self.__finished_PushMs12Dst)
        for i in range(1, 5):
            self.__custom_connect_slots('Push', 'Src', i)
            self.__custom_connect_slots('Push', 'Dst', i)
            self.__custom_connect_slots('Push', 'Button', i)
        for i in range(1, 5):
            self.__custom_connect_slots('Pull', 'Src', i)
            self.__custom_connect_slots('Pull', 'Dst', i)
            self.__custom_connect_slots('Pull', 'Button', i)

    def __custom_connect_slots(self, direct, type, i):
        if direct == 'Push':
            if type == 'Src':
                eval('self.m_mainUi.System_PushCustom' + str(i) + 'Src_lineEdit').editingFinished.connect(
                    lambda: self.__finished_PushCustomSrc(i))
            elif type == 'Dst':
                eval('self.m_mainUi.System_PushCustom' + str(i) + 'Dst_lineEdit').editingFinished.connect(
                    lambda: self.__finished_PushCustomDst(i))
            elif type == 'Button':
                eval('self.m_mainUi.System_PushCustom' + str(i) + 'Push_Button').clicked.connect(
                    lambda: self.__click_push_custom(i))
            else:
                self.log.d('not support direct:' + direct + ', type:' + type)
        elif direct == 'Pull':
            if type == 'Src':
                eval('self.m_mainUi.System_PullCustom' + str(i) + 'Src_lineEdit').editingFinished.connect(
                    lambda: self.__finished_PullCustomSrc(i))
            elif type == 'Dst':
                eval('self.m_mainUi.System_PullCustom' + str(i) + 'Dst_lineEdit').editingFinished.connect(
                    lambda: self.__finished_PullCustomDst(i))
            elif type == 'Button':
                eval('self.m_mainUi.System_PullCustom' + str(i) + 'Pull_Button').clicked.connect(
                    lambda: self.__click_pull_custom(i))
            else:
                self.log.d('not support direct:' + direct + ', type:' + type)

    def closeEvent(self):
        self.__m_stop_thread = True

    def __pushFilesToSoc(self, src, dst):
        self.log.d('push src: ' + src);
        self.log.d('push dst: ' + dst);
        AmlCommonUtils.exe_adb_cmd('push "' + src + '" "' + dst + '"', True)

    def __pullFilesToSoc(self, src, dst):
        AmlCommonUtils.exe_adb_cmd('pull "' + src + '" "' + dst + '"', True)
        self.m_mainUi.System_PushDolbySrc_lineEdit.text()

    def __click_push_dst_dolby(self):
        self.log.d('click dolbydst pushButton')
        if self.m_mainUi.System_PushDolbySrc_lineEdit.text() != "":
            self.__pushFilesToSoc(self.m_mainUi.System_PushDolbySrc_lineEdit.text() + '\\libHwAudio_dcvdec.so',
                              self.m_mainUi.System_PushDolbyDtsDst_lineEdit.text())
        if self.m_mainUi.System_PushDtsSrc_lineEdit.text() != "":
            self.__pushFilesToSoc(self.m_mainUi.System_PushDtsSrc_lineEdit.text() + '\\libHwAudio_dtshd.so',
                              self.m_mainUi.System_PushDolbyDtsDst_lineEdit.text())

    def __click_push_ms12(self):
        self.log.d('click ms12 pushButton')
        if self.m_mainUi.System_PushMs12Src_lineEdit.text() != "":
            self.__pushFilesToSoc(self.m_mainUi.System_PushMs12Src_lineEdit.text() + '\\libdolbyms12.so',
                              self.m_mainUi.System_PushMs12Dst_lineEdit.text())

    def __click_push_custom(self, i):
        self.log.i('push custom:' + str(i))
        self.__pushFilesToSoc(eval('self.m_mainUi.System_PushCustom' + str(i) + 'Src_lineEdit').text(),
                              eval('self.m_mainUi.System_PushCustom' + str(i) + 'Dst_lineEdit').text())

    def __click_pull_custom(self, i):
        self.log.i('pull custom:' + str(i))
        self.__pullFilesToSoc(eval('self.m_mainUi.System_PullCustom' + str(i) + 'Src_lineEdit').text(),
                              eval('self.m_mainUi.System_PullCustom' + str(i) + 'Dst_lineEdit').text())

    def __click_remount(self):
        self.log.i('click remount')
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()


    def __click_close_avb(self):
        self.log.i('click close avb')
        self.m_mainUi.Sys_CloseAvb_Button.setEnabled(False)
        thread = Thread(target=self.__closeAvbProc)
        thread.start()

    def __closeAvbProc(self):
        AmlCommonUtils.exe_adb_cmd('reboot bootloader', True)
        AmlCommonUtils.exe_sys_cmd('fastboot flashing unlock_critical', True)
        AmlCommonUtils.exe_sys_cmd('fastboot flashing unlock', True)
        AmlCommonUtils.exe_sys_cmd('fastboot reboot', True)
        timeCntS = 40
        self.log.d('__closeAvbProc: flashing unlock reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False:
            time.sleep(1)
            timeCntS -= 1
        AmlCommonUtils.adb_root()
        AmlCommonUtils.exe_adb_cmd('disable-verity', True)
        AmlCommonUtils.adb_reboot()
        timeCntS = 40
        self.log.d('__closeAvbProc: disable-verity reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False:
            time.sleep(1)
            timeCntS -= 1
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()
        self.m_mainUi.AmlSystemCloseAvb_Button.setEnabled(True)

    def __finished_PushDolbySrc(self):
        self.log.d('finish push dolby by Src')
        try:
            self.m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH,
                                      self.m_mainUi.System_PushDolbySrc_lineEdit.text())

        except Exception as e:
            traceback.print_exc()


    def __finished_PushDtsSrc(self):
        self.log.d('finish push dts Src')
        self.m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH,
                                      self.m_mainUi.System_PushDtsSrc_lineEdit.text())

    def __finished_PushMs12Src(self):
        self.log.d('finish push ms12 by Src')
        self.m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH,
                                      self.m_mainUi.System_PushMs12Src_lineEdit.text())

    def __finished_PushDolbyDtsDst(self):
        self.log.d('finish push dolby by dst')
        self.m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH,
                                      self.m_mainUi.System_PushDolbyDtsDst_lineEdit.text())


    def __finished_PushMs12Dst(self):
        self.log.d('finish push ms12 by dst')
        self.m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH,
                                      self.m_mainUi.System_PushMs12Dst_lineEdit.text())

    def __finished_PushCustomSrc(self, i):
        self.log.d('finish push custom'+ str(i)+' src')
        self.m_iniPaser.setValueByKey(
            eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_SRC_PATH'), \
            eval('self.m_mainUi.System_PushCustom' + str(i) + 'Src_lineEdit').text())

    def __finished_PushCustomDst(self, i):
        self.log.d('finish push custom' + str(i) + ' dst')
        self.m_iniPaser.setValueByKey(
            eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_DST_PATH'), \
            eval('self.m_mainUi.System_PushCustom' + str(i) + 'Dst_lineEdit').text())

    def __finished_PullCustomSrc(self, i):
        self.log.d('finish pull custom' + str(i) + ' src')
        self.m_iniPaser.setValueByKey(
            eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_SRC_PATH'), \
            eval('self.m_mainUi.System_PullCustom' + str(i) + 'Src_lineEdit').text())

    def __finished_PullCustomDst(self, i):
        self.log.d('finish pull custom' + str(i) + ' dst')
        self.m_iniPaser.setValueByKey(
            eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_DST_PATH'), \
            eval('self.m_mainUi.System_PullCustom' + str(i) + 'Dst_lineEdit').text())
