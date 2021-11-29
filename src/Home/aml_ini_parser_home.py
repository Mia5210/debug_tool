from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager


def instance(parser):
    return AmlParserIniHome(parser)


class AmlParserIniHome(AmlParserIniBase):
    # Modules
    AML_PARSER_HOME_AUDIO_ENABLE = "audio_enable"
    AML_PARSER_HOME_VIDEO_ENABLE = "video_enable"
    AML_PARSER_HOME_CEC_ENABLE = "cec_enable"
    # Options
    AML_PARSER_HOME_LOGCAT = "logcat_enable"
    AML_PARSER_HOME_BUGREPORT = "bugreport_enable"
    AML_PARSER_HOME_DMESG = "dmesg_enable"

    AML_PARSER_HOME_CAPTRUE_MODE = "captrue_mode"
    AML_PARSER_HOME_CAPTURE_TIME = "captrue_time"

    AML_PARSER_HOME_IP_ADDRESS = "ip_address"

    DEBUG_CAPTURE_MODE_AUTO = 0
    DEBUG_CAPTURE_MODE_MUNUAL = 1
    DEFAULT_CAPTURE_MODE = DEBUG_CAPTURE_MODE_AUTO

    #Uart
    AML_PARSER_HOME_COM_BAUDRATE = "com_baudrate"
    AML_PARSER_HOME_COM_DATABITS = "com_databits"
    AML_PARSER_HOME_COM_PARITY   = "com_parity"
    AML_PARSER_HOME_COM_STOPBITS = "com_stopbits"
    AML_PARSER_HOME_COM_DTRDSR   = "com_dtrdsr"
    AML_PARSER_HOME_COM_RTSCTS   = "com_rtscts"
    AML_PARSER_HOME_COM_XONXOFF  = "com_xonxoff"

    def __init__(self, parser):
        super(AmlParserIniHome, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_HOME

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE: 'False',
            AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE: 'False',
            AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE: 'False',
            AmlParserIniHome.AML_PARSER_HOME_LOGCAT: 'False',
            AmlParserIniHome.AML_PARSER_HOME_BUGREPORT: 'False',
            AmlParserIniHome.AML_PARSER_HOME_DMESG: 'False',

            AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE: str(AmlParserIniHome.DEFAULT_CAPTURE_MODE),
            AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME: '6',
            AmlParserIniHome.AML_PARSER_HOME_IP_ADDRESS: '',
            AmlParserIniHome.AML_PARSER_HOME_COM_BAUDRATE: '115200',
            AmlParserIniHome.AML_PARSER_HOME_COM_DATABITS: '8',
            AmlParserIniHome.AML_PARSER_HOME_COM_PARITY: 'N',
            AmlParserIniHome.AML_PARSER_HOME_COM_STOPBITS: '1',
            AmlParserIniHome.AML_PARSER_HOME_COM_DTRDSR: 'False',
            AmlParserIniHome.AML_PARSER_HOME_COM_RTSCTS: 'False',
            AmlParserIniHome.AML_PARSER_HOME_COM_XONXOFF: 'False',
        }
        return self.__dictionary_default_value

    def getValueByKey(self, key):
        if key == AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE or \
                key == AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME or \
                key == AmlParserIniHome.AML_PARSER_HOME_COM_BAUDRATE or \
                key == AmlParserIniHome.AML_PARSER_HOME_COM_DATABITS or \
                key == AmlParserIniHome.AML_PARSER_HOME_COM_STOPBITS:
            return self.getIntValueByKey(key)
        elif key == AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE or \
                key == AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE or \
                key == AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE or \
                key == AmlParserIniHome.AML_PARSER_HOME_LOGCAT or \
                key == AmlParserIniHome.AML_PARSER_HOME_BUGREPORT or \
                key == AmlParserIniHome.AML_PARSER_HOME_DMESG or \
                key == AmlParserIniHome.AML_PARSER_HOME_COM_DTRDSR or \
                key == AmlParserIniHome.AML_PARSER_HOME_COM_RTSCTS or \
                key == AmlParserIniHome.AML_PARSER_HOME_COM_XONXOFF:
            return self.getBoolValueByKey(key)
        else:
            return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        print('--debug')
        self.setStrValueByKey(key, str(value))