import os,sys
import traceback
from am_debug import *
from threading import Thread

from src.Audio.aml_debug_audio import AmlAudioDebug, AudioDebugCfg
from src.Audio.aml_ini_parser_audio import AmlParserIniAudio
from src.common.aml_common_utils import AmlCommonUtils
from src.common.aml_debug_base_ui import AmlDebugBaseUi

def instance(aml_ui):
    return AmlDebugAudioUi(aml_ui)

#Table: "Audio Debug"
class AmlDebugAudioUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugAudioUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_AUDIO)
        self.audioDebug = AmlAudioDebug(self.log)
        self.audioDebugcfg = AudioDebugCfg()
        self.__homeCallbackStartFinish = print
        self.__homeCallbackStopFinish = print
        self.__homeStartClick = False
        self.__homeStopClick = False

    def init_display_ui(self):
        mode = self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE)
        if mode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.log.i("mode menu")
            self.m_mainUi.AudioMode_Menu_radioBtn.setChecked(True)
            self.m_mainUi.Audio_captureTime_groupBox.setEnabled(False)
        elif mode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.log.i("mode Auto")
            self.m_mainUi.AudioMode_Auto_radioBtn.setChecked(True)
            self.m_mainUi.Audio_captureTime_groupBox.setEnabled(True)
        else:
            self.log.e('E init_display_ui: Not supported capture mode:' + str(mode) + ' !!!')

        self.m_mainUi.Audio_debugInfo_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO))
        self.m_mainUi.Audio_dumpData_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA))
        self.m_mainUi.Audio_Logcat_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT))
        self.m_mainUi.Audio_printDebug_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG))
        self.m_mainUi.Audio_captureTime_spinBox.setValue(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME))
        self.m_mainUi.Audio_createZip_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP))
        # pcm audio play ui
        support_channel_array = ['1', '2', '4', '6', '8']
        support_byte_array = ['1', '2', '4']
        support_rate_array = ['8000', '16000', '32000', '44100', '48000', '64000', '88200', '96000', '192000']
        self.m_mainUi.Audio_playChannel_comboBox.addItems(support_channel_array)
        self.m_mainUi.Audio_playChannel_comboBox.setCurrentText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL))
        self.m_mainUi.Audio_playByte_comboBox.addItems(support_byte_array)
        self.m_mainUi.Audio_playByte_comboBox.setCurrentText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE))
        self.m_mainUi.Audio_playRate_comboBox.addItems(support_rate_array)
        self.m_mainUi.Audio_playRate_comboBox.setCurrentText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE))
        self.__refresh_PlayAudioSelectChannelUi()
        self.m_mainUi.Audio_dataFile_lineEdit.setText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH))

    def signals_connect_slots(self):
        self.m_mainUi.AudioMode_Auto_radioBtn.clicked.connect(self.__click_auto_mode)
        self.m_mainUi.AudioMode_Menu_radioBtn.clicked.connect(self.__click_menu_mode)
        self.m_mainUi.Audio_debugStart_btn.clicked.connect(self.start_capture)
        self.m_mainUi.Audio_debugStop_btn.clicked.connect(self.stop_capture)
        self.m_mainUi.Audio_debugInfo_checkBox.clicked[bool].connect(self.__click_DebugInfo)
        self.m_mainUi.Audio_dumpData_checkBox.clicked[bool].connect(self.__click_DumpData)
        self.m_mainUi.Audio_Logcat_checkBox.clicked[bool].connect(self.__click_Logcat)
        self.m_mainUi.Audio_captureTime_spinBox.valueChanged[int].connect(self.__changed_captureTime)
        self.m_mainUi.Audio_printDebug_checkBox.clicked[bool].connect(self.__click_PrintDebugEnable)
        self.m_mainUi.Audio_createZip_checkBox.clicked[bool].connect(self.__click_CreateZipEnable)
        self.m_mainUi.Audio_dataFile_play_btn.clicked.connect(self.__click_play_toggle)
        self.m_mainUi.Audio_playChannel_comboBox.currentTextChanged.connect(self.__textChanged_PlayAudioChannel)
        self.m_mainUi.Audio_playByte_comboBox.currentTextChanged.connect(self.__textChanged_PlayAudioByte)
        self.m_mainUi.Audio_playRate_comboBox.currentTextChanged.connect(self.__textChanged_PlayAudioRate)
        self.m_mainUi.Audio_dataFile_lineEdit.editingFinished.connect(self.__editing_PlayAudioPath)
        self.m_mainUi.Audio_dataFile_Open_btn.clicked.connect(self.__click_playAudioRateFileOpen)
        #self.m_mainUi.AmlDebugAudioOpenOutput_pushButton.clicked.connect(self.__click_open_output)


    def __click_auto_mode(self):
        self.m_mainUi.Audio_captureTime_spinBox.setEnabled(True)
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE, AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO)
        self.log.i('click auto')

    def __click_menu_mode(self):
        self.m_mainUi.Audio_captureTime_spinBox.setEnabled(False)
        self.m_iniPaser.setValueByKey("captrue_mode", 1)
        self.log.i('click menu')

    def start_capture(self, curTimeName='', homeCallbackFinish=print, homeClick=False):
        self.log.i('start capture')
        self.__homeCallbackStartFinish = homeCallbackFinish
        self.__homeStartClick = homeClick
        self.m_mainUi.Audio_debugMode_groupBox.setEnabled(False)
        self.m_mainUi.Audio_captureTime_groupBox.setEnabled(False)
        self.m_mainUi.Audio_debugOptions_groupBox.setEnabled(False)
        self.m_mainUi.Audio_debugOutput_groupBox.setEnabled(False)
        self.m_mainUi.Audio_debugStart_btn.setEnabled(False)
        self.__pre_audio_debug_config()
        self.audioDebugcfg.m_homeClick = homeClick;
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        thread = Thread(target=self.__startCaptureInfo, args=(curTimeName,))
        thread.start()

    def stop_capture(self, homeCallbackFinish=print, homeClick=False):
        self.log.i('stop capture')
        self.__homeCallbackStopFinish = homeCallbackFinish
        self.__homeStopClick = homeClick
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.log.i('stop_capture: auto mode not need stop.')
            if self.__homeStopClick == True:
                self.__homeCallbackStopFinish(self.m_moduleId)
            return
        self.m_mainUi.Audio_debugStop_btn.setEnabled(False)
        thread = Thread(target=self.__stopCaptureInfo)
        thread.start()

    def __click_DebugInfo(self, enable):
        self.log.d('click debug info')
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO, enable)

    def __click_DumpData(self, enable):
        self.log.d('click Dump data')
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA, enable)

    def __click_Logcat(self, enable):
        self.log.d('click Logcat')
        if enable:
            self.m_mainUi.Home_logcatOption_checkBox.setChecked(True)
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT, enable)

    def __changed_captureTime(self, value):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME, value)
        self.log.i('change capture time: '+ str(value))

    def __click_CreateZipEnable(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP, enable)
        self.log.w('create zip')

    def __click_PrintDebugEnable(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG, enable)
        self.log.d('print Debug')

    def __textChanged_PlayAudioChannel(self, value):
        self.log.i('audio channel change')
        self.__refresh_PlayAudioSelectChannelUi()
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL, value)

    def __textChanged_PlayAudioByte(self, value):
        self.log.i('change audio byte')
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE, value)

    def __textChanged_PlayAudioRate(self, value):
        self.log.i('change audio rate')
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE, value)

    def __editing_PlayAudioPath(self):
        self.log.i('change audio path')
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH, self.m_mainUi.AmlAudioDebugPlayAudioPath_lineEdit.text())

    def __click_playAudioRateFileOpen(self):
        self.log.i('file open')
        curPath = self.audioDebug.getCurDebugPath()
        openPath = self.check_output_path(curPath)
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self.m_mainUi, "Open File", openPath, "All Files(*);;Text Files(*.txt)")
        if not fileName == '':
            self.m_mainUi.Audio_dataFile_lineEdit.setText(fileName)
            self.__editing_PlayAudioPath()

    def __click_play_toggle(self):
        self.log.i('click play toggle')
        channel = int(self.m_mainUi.Audio_playChannel_comboBox.currentText())
        selChn = self.m_mainUi.Audio_SelectChannel_comboBox.currentIndex()
        byte = int(self.m_mainUi.Audio_playByte_comboBox.currentText())
        rate = int(self.m_mainUi.Audio_playRate_comboBox.currentText())
        fileName = self.m_mainUi.Audio_dataFile_lineEdit.text()
        isPlaying = self.audioDebug.start_play_toggle(fileName, channel, byte, rate, selChn,
                                                      self.__callback_audioPlayFinish)
        if isPlaying == True:
            self.m_mainUi.Audio_dataFile_play_btn.setText('Stop(playing)')
        else:
            self.m_mainUi.Audio_dataFile_play_btn.setText('Play')
    '''
    def __click_open_output(self):
        curPath = self.audioDebug.getCurDebugPath()
        os.startfile(self.check_output_path(curPath))
    '''

    def get_logcat_enable(self):
        return self.m_mainUi.Audio_Logcat_checkBox.isChecked()

    def open_logcat(self):
        self.__pre_audio_debug_config()
        self.audioDebugcfg.m_homeClick = True;
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        self.audioDebug.open_logcat()

    def close_logcat(self):
        self.audioDebug.close_logcat()

    def __startCaptureInfo(self, curTimeName):
        if self.__homeStartClick == False:
            AmlCommonUtils.adb_root()
            AmlCommonUtils.adb_remount()
        self.audioDebug.start_capture(curTimeName, self.__callback_startCaptureFinish)

    def __callback_startCaptureFinish(self):
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.Audio_debugMode_groupBox.setEnabled(True)
            self.m_mainUi.Audio_debugOptions_groupBox.setEnabled(True)
            self.m_mainUi.Audio_captureTime_groupBox.setEnabled(True)
            self.m_mainUi.Audio_debugOutput_groupBox.setEnabled(True)
            self.m_mainUi.Audio_debugStart_btn.setEnabled(True)
            self.log.i('------ Auto mode capture Finish !!! ------')
        elif self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.Audio_debugStop_btn.setEnabled(True)
            self.log.i('Manual mode Start capture finish')
        if self.__homeStartClick == True:
            self.__homeCallbackStartFinish(self.m_moduleId)

    def __stopCaptureInfo(self):
        self.audioDebug.stop_capture(self.__callback_stopCaptureFinish)
        if self.__homeStopClick == True:
            self.__homeCallbackStopFinish(self.m_moduleId)

    def __callback_stopCaptureFinish(self):
        self.log.i('------ Manual mode capture Finish !!! ------')
        self.m_mainUi.Audio_debugMode_groupBox.setEnabled(True)
        self.m_mainUi.Audio_debugOptions_groupBox.setEnabled(True)
        self.m_mainUi.Audio_debugOutput_groupBox.setEnabled(True)
        self.m_mainUi.Audio_debugStart_btn.setEnabled(True)

    def closeEvent(self):
        pass

    def __pre_audio_debug_config(self):
        if self.m_mainUi.AudioMode_Auto_radioBtn.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_mainUi.AudioMode_Menu_radioBtn.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.log.w('__pre_audio_debug_config: Not supported capture mode!!!')
        self.audioDebugcfg.m_debugInfoEnable = self.m_mainUi.Audio_debugInfo_checkBox.isChecked()
        self.audioDebugcfg.m_dumpDataEnable = self.m_mainUi.Audio_dumpData_checkBox.isChecked()
        self.audioDebugcfg.m_logcatEnable = self.m_mainUi.Audio_Logcat_checkBox.isChecked()
        self.audioDebugcfg.m_autoDebugTimeS = self.m_mainUi.Audio_captureTime_spinBox.value()
        self.audioDebugcfg.m_printDebugEnable = self.m_mainUi.Audio_printDebug_checkBox.isChecked()
        self.audioDebugcfg.m_createZipFile = self.m_mainUi.Audio_createZip_checkBox.isChecked()

    def __callback_audioPlayFinish(self):
        self.m_mainUi.Audio_dataFile_play_btn.setText('Play')

    def __refresh_PlayAudioSelectChannelUi(self):
        support_sel_ch_array = ['1_2', '3_4', '5_6', '7_8']
        self.m_mainUi.Audio_SelectChannel_comboBox.clear()
        channels = int(self.m_mainUi.Audio_playChannel_comboBox.currentText())
        self.m_mainUi.Audio_SelectChannel_comboBox.addItem(support_sel_ch_array[0])
        if channels >= 4:
            self.m_mainUi.Audio_SelectChannel_comboBox.addItem(support_sel_ch_array[1])
        if channels >= 6:
            self.m_mainUi.Audio_SelectChannel_comboBox.addItem(support_sel_ch_array[2])
        if channels == 8:
            self.m_mainUi.Audio_SelectChannel_comboBox.addItem(support_sel_ch_array[3])
