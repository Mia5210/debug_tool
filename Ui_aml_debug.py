# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'am_debug.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 702)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AmlDebug_tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.AmlDebug_tabWidget.setGeometry(QtCore.QRect(0, 0, 1021, 661))
        self.AmlDebug_tabWidget.setObjectName("AmlDebug_tabWidget")
        self.AmlDebugHome_tab = QtWidgets.QWidget()
        self.AmlDebugHome_tab.setObjectName("AmlDebugHome_tab")
        self.AmlDebug_tabWidget.addTab(self.AmlDebugHome_tab, "")
        self.AmlDebugVideo_tab = QtWidgets.QWidget()
        self.AmlDebugVideo_tab.setObjectName("AmlDebugVideo_tab")
        self.AmlVideo_stackedWidget = QtWidgets.QStackedWidget(self.AmlDebugVideo_tab)
        self.AmlVideo_stackedWidget.setGeometry(QtCore.QRect(180, 10, 821, 391))
        self.AmlVideo_stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.AmlVideo_stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.AmlVideo_stackedWidget.setLineWidth(1)
        self.AmlVideo_stackedWidget.setObjectName("AmlVideo_stackedWidget")
        self.Video_debugInfo_page = QtWidgets.QWidget()
        self.Video_debugInfo_page.setObjectName("Video_debugInfo_page")
        self.label_3 = QtWidgets.QLabel(self.Video_debugInfo_page)
        self.label_3.setGeometry(QtCore.QRect(60, 30, 68, 15))
        self.label_3.setObjectName("label_3")
        self.AmlVideo_stackedWidget.addWidget(self.Video_debugInfo_page)
        self.Video_dumpData_page = QtWidgets.QWidget()
        self.Video_dumpData_page.setObjectName("Video_dumpData_page")
        self.label_4 = QtWidgets.QLabel(self.Video_dumpData_page)
        self.label_4.setGeometry(QtCore.QRect(30, 40, 68, 15))
        self.label_4.setObjectName("label_4")
        self.AmlVideo_stackedWidget.addWidget(self.Video_dumpData_page)
        self.AmlVideo_groupBox = QtWidgets.QGroupBox(self.AmlDebugVideo_tab)
        self.AmlVideo_groupBox.setGeometry(QtCore.QRect(180, 410, 821, 211))
        self.AmlVideo_groupBox.setObjectName("AmlVideo_groupBox")
        self.AmlVideo_textBrowser = QtWidgets.QTextBrowser(self.AmlVideo_groupBox)
        self.AmlVideo_textBrowser.setGeometry(QtCore.QRect(0, 20, 821, 191))
        self.AmlVideo_textBrowser.setObjectName("AmlVideo_textBrowser")
        self.AmlVideo_listWidget = QtWidgets.QListWidget(self.AmlDebugVideo_tab)
        self.AmlVideo_listWidget.setGeometry(QtCore.QRect(10, 10, 161, 611))
        self.AmlVideo_listWidget.setObjectName("AmlVideo_listWidget")
        item = QtWidgets.QListWidgetItem()
        self.AmlVideo_listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.AmlVideo_listWidget.addItem(item)
        self.AmlDebug_tabWidget.addTab(self.AmlDebugVideo_tab, "")
        self.AmlDebugAudio_tab = QtWidgets.QWidget()
        self.AmlDebugAudio_tab.setObjectName("AmlDebugAudio_tab")
        self.AmlAudio_listWidget = QtWidgets.QListWidget(self.AmlDebugAudio_tab)
        self.AmlAudio_listWidget.setGeometry(QtCore.QRect(10, 10, 161, 611))
        self.AmlAudio_listWidget.setObjectName("AmlAudio_listWidget")
        item = QtWidgets.QListWidgetItem()
        self.AmlAudio_listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.AmlAudio_listWidget.addItem(item)
        self.AmlAudio_stackedWidget = QtWidgets.QStackedWidget(self.AmlDebugAudio_tab)
        self.AmlAudio_stackedWidget.setGeometry(QtCore.QRect(180, 10, 821, 391))
        self.AmlAudio_stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.AmlAudio_stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.AmlAudio_stackedWidget.setLineWidth(1)
        self.AmlAudio_stackedWidget.setObjectName("AmlAudio_stackedWidget")
        self.Audio_debugInfo_page = QtWidgets.QWidget()
        self.Audio_debugInfo_page.setObjectName("Audio_debugInfo_page")
        self.label = QtWidgets.QLabel(self.Audio_debugInfo_page)
        self.label.setGeometry(QtCore.QRect(720, 350, 91, 31))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.Audio_debugInfo_page)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 371, 80))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(31, 31, 111, 19))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 30, 72, 19))
        self.radioButton_2.setObjectName("radioButton_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.Audio_debugInfo_page)
        self.groupBox_2.setGeometry(QtCore.QRect(370, 20, 120, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox.setGeometry(QtCore.QRect(20, 30, 45, 22))
        self.spinBox.setObjectName("spinBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.Audio_debugInfo_page)
        self.groupBox_3.setGeometry(QtCore.QRect(0, 110, 491, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox.setGeometry(QtCore.QRect(31, 31, 131, 19))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_2.setGeometry(QtCore.QRect(180, 30, 121, 19))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_3.setGeometry(QtCore.QRect(330, 30, 91, 19))
        self.checkBox_3.setObjectName("checkBox_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.Audio_debugInfo_page)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 200, 491, 80))
        self.groupBox_4.setObjectName("groupBox_4")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_4.setGeometry(QtCore.QRect(180, 40, 151, 19))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_5.setGeometry(QtCore.QRect(31, 41, 131, 19))
        self.checkBox_5.setObjectName("checkBox_5")
        self.AmlAudio_stackedWidget.addWidget(self.Audio_debugInfo_page)
        self.Audio_dumpData_page = QtWidgets.QWidget()
        self.Audio_dumpData_page.setObjectName("Audio_dumpData_page")
        self.label_2 = QtWidgets.QLabel(self.Audio_dumpData_page)
        self.label_2.setGeometry(QtCore.QRect(720, 350, 91, 31))
        self.label_2.setObjectName("label_2")
        self.AmlAudio_stackedWidget.addWidget(self.Audio_dumpData_page)
        self.AmlAudio_groupBox = QtWidgets.QGroupBox(self.AmlDebugAudio_tab)
        self.AmlAudio_groupBox.setGeometry(QtCore.QRect(180, 410, 821, 211))
        self.AmlAudio_groupBox.setObjectName("AmlAudio_groupBox")
        self.AmlAudio_textBrowser = QtWidgets.QTextBrowser(self.AmlAudio_groupBox)
        self.AmlAudio_textBrowser.setGeometry(QtCore.QRect(0, 20, 821, 191))
        self.AmlAudio_textBrowser.setObjectName("AmlAudio_textBrowser")
        self.AmlDebug_tabWidget.addTab(self.AmlDebugAudio_tab, "")
        self.AmlDebugCec_tab = QtWidgets.QWidget()
        self.AmlDebugCec_tab.setObjectName("AmlDebugCec_tab")
        self.AmlDebug_tabWidget.addTab(self.AmlDebugCec_tab, "")
        self.AmlDebugSource_tab = QtWidgets.QWidget()
        self.AmlDebugSource_tab.setObjectName("AmlDebugSource_tab")
        self.AmlDebug_tabWidget.addTab(self.AmlDebugSource_tab, "")
        self.AmlDebugOthers_tab = QtWidgets.QWidget()
        self.AmlDebugOthers_tab.setObjectName("AmlDebugOthers_tab")
        self.AmlDebug_tabWidget.addTab(self.AmlDebugOthers_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.AmlDebug_tabWidget.setCurrentIndex(2)
        self.AmlVideo_stackedWidget.setCurrentIndex(1)
        self.AmlAudio_stackedWidget.setCurrentIndex(0)
        self.AmlAudio_listWidget.currentRowChanged['int'].connect(self.AmlAudio_stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AmlDebug_tabWidget.setTabText(self.AmlDebug_tabWidget.indexOf(self.AmlDebugHome_tab), _translate("MainWindow", "Home"))
        self.label_3.setText(_translate("MainWindow", "page 1"))
        self.label_4.setText(_translate("MainWindow", "page 2"))
        self.AmlVideo_groupBox.setTitle(_translate("MainWindow", "Terminal Log"))
        __sortingEnabled = self.AmlVideo_listWidget.isSortingEnabled()
        self.AmlVideo_listWidget.setSortingEnabled(False)
        item = self.AmlVideo_listWidget.item(0)
        item.setText(_translate("MainWindow", "Debug Info"))
        item = self.AmlVideo_listWidget.item(1)
        item.setText(_translate("MainWindow", "video"))
        self.AmlVideo_listWidget.setSortingEnabled(__sortingEnabled)
        self.AmlDebug_tabWidget.setTabText(self.AmlDebug_tabWidget.indexOf(self.AmlDebugVideo_tab), _translate("MainWindow", "Video"))
        __sortingEnabled = self.AmlAudio_listWidget.isSortingEnabled()
        self.AmlAudio_listWidget.setSortingEnabled(False)
        item = self.AmlAudio_listWidget.item(0)
        item.setText(_translate("MainWindow", "Debug Info"))
        item = self.AmlAudio_listWidget.item(1)
        item.setText(_translate("MainWindow", "Dump Data"))
        self.AmlAudio_listWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "page 1"))
        self.groupBox.setTitle(_translate("MainWindow", "Mode"))
        self.radioButton.setText(_translate("MainWindow", "Auto"))
        self.radioButton_2.setText(_translate("MainWindow", "Manual"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Capture Time"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Options"))
        self.checkBox.setText(_translate("MainWindow", "Debug Info"))
        self.checkBox_2.setText(_translate("MainWindow", "Dump Data"))
        self.checkBox_3.setText(_translate("MainWindow", "Logcat"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Output"))
        self.checkBox_4.setText(_translate("MainWindow", "print Debug"))
        self.checkBox_5.setText(_translate("MainWindow", "Create Zip"))
        self.label_2.setText(_translate("MainWindow", "page 2"))
        self.AmlAudio_groupBox.setTitle(_translate("MainWindow", "Terminal Log"))
        self.AmlDebug_tabWidget.setTabText(self.AmlDebug_tabWidget.indexOf(self.AmlDebugAudio_tab), _translate("MainWindow", "Audio"))
        self.AmlDebug_tabWidget.setTabText(self.AmlDebug_tabWidget.indexOf(self.AmlDebugCec_tab), _translate("MainWindow", "Cec"))
        self.AmlDebug_tabWidget.setTabText(self.AmlDebug_tabWidget.indexOf(self.AmlDebugSource_tab), _translate("MainWindow", "Source"))
        self.AmlDebug_tabWidget.setTabText(self.AmlDebug_tabWidget.indexOf(self.AmlDebugOthers_tab), _translate("MainWindow", "Others"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
