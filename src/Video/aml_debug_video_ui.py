import sys
from am_debug import *
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugVideoUi(aml_ui)

#Table: "Video Debug"
class AmlDebugVideoUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugVideoUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_VIDEO)

    def init_display_ui(self):
        self.m_mainUi.xxx.setText(self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH))

    def signals_connect_slots(self):
        self.m_mainUi.Video_btn1.clicked.connect(self.__click_btn1)
        self.m_mainUi.pushButton.clicked.connect(self.__click_btn)

    def __click_btn1(self):
        self.log.d('click button 1')

    def __click_btn(self):
        self.log.d('click button')


    def closeEvent(self):
        pass