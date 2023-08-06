# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtDesigner/main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from multiprocessing import cpu_count


def font(font_size=12, font_file="Ubuntu.ttf"):
    """e.g. MainWindow.setFont(font(10))"""
    font_id = QtGui.QFontDatabase.addApplicationFont(font_file)
    font_name = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
    return QtGui.QFont(font_name, font_size)


class MyQLineEdit(QtWidgets.QLineEdit):
    # clicked = QtCore.pyqtSignal(str)
    FocusInSignal = QtCore.pyqtSignal(str)
    FocusOutSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent, default_value=""):
        super(MyQLineEdit, self).__init__(parent)
        self.default = default_value

    def focusInEvent(self, event):
        self.FocusInSignal.emit(self.default)

    def focusOutEvent(self, event):
        self.FocusOutSignal.emit(self.default)

    # def mousePressEvent(self, event):
    #     self.clicked.emit(self.default)


class MyQPlainTextEdit(QtWidgets.QPlainTextEdit):
    FocusInSignal = QtCore.pyqtSignal(str)
    FocusOutSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent, default_value=""):
        super(MyQPlainTextEdit, self).__init__(parent)
        self.default = default_value

    def focusInEvent(self, event):
        self.FocusInSignal.emit(self.default)

    def focusOutEvent(self, event):
        self.FocusOutSignal.emit(self.default)

    def text(self):
        return self.toPlainText()

    def setText(self, value):
        self.setPlainText(value)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1060, 840)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1060, 840))
        MainWindow.setMaximumSize(QtCore.QSize(1060, 840))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        MainWindow.setFont(font)
        logo = QtGui.QIcon()
        logo.addPixmap(QtGui.QPixmap("./images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(logo)
        MainWindow.setStyleSheet("")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.aligning_box = QtWidgets.QGroupBox(self.centralwidget)
        self.aligning_box.setEnabled(True)
        self.aligning_box.setGeometry(QtCore.QRect(20, 10, 471, 431))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.aligning_box.setFont(font)
        self.aligning_box.setObjectName("aligning_box")
        self.line_4 = QtWidgets.QFrame(self.aligning_box)
        self.line_4.setGeometry(QtCore.QRect(20, 690, 431, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.query_file = MyQLineEdit(self.aligning_box)
        self.query_file.setGeometry(QtCore.QRect(20, 210, 341, 23))
        self.query_file.setObjectName("query_file")
        self.query_file.setFont(font)
        self.sra = QtWidgets.QLineEdit(self.aligning_box)
        self.sra.setGeometry(QtCore.QRect(20, 300, 431, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.sra.setFont(font)
        self.sra.setObjectName("sra")
        self.query = MyQPlainTextEdit(self.aligning_box, ">Gene_1\nATGCATGC")
        self.query.setGeometry(QtCore.QRect(20, 60, 431, 111))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(10)
        self.query.setFont(font)
        self.query.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.query.setMouseTracking(True)
        self.query.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.query.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.query.setTabChangesFocus(True)
        self.query.setOverwriteMode(False)
        self.query.setObjectName("query")
        self.program = QtWidgets.QComboBox(self.aligning_box)
        self.program.setGeometry(QtCore.QRect(20, 380, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.program.setFont(font)
        self.program.setObjectName("program")
        self.program.addItem("")
        self.program.addItem("")
        self.program.addItem("")
        self.program.addItem("")
        self.program.addItem("")
        self.line_1 = QtWidgets.QFrame(self.aligning_box)
        self.line_1.setGeometry(QtCore.QRect(20, 330, 431, 16))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.lbl_sra = QtWidgets.QLabel(self.aligning_box)
        self.lbl_sra.setGeometry(QtCore.QRect(20, 270, 431, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_sra.setFont(font)
        self.lbl_sra.setObjectName("lbl_sra")
        self.line_0 = QtWidgets.QFrame(self.aligning_box)
        self.line_0.setGeometry(QtCore.QRect(20, 250, 431, 16))
        self.line_0.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_0.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_0.setObjectName("line_0")
        self.lbl_program = QtWidgets.QLabel(self.aligning_box)
        self.lbl_program.setGeometry(QtCore.QRect(20, 350, 431, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_program.setFont(font)
        self.lbl_program.setObjectName("lbl_program")
        self.lbl_queryfile = QtWidgets.QLabel(self.aligning_box)
        self.lbl_queryfile.setGeometry(QtCore.QRect(20, 180, 301, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_queryfile.setFont(font)
        self.lbl_queryfile.setObjectName("lbl_queryfile")
        self.browse_file_button = QtWidgets.QToolButton(self.aligning_box)
        self.browse_file_button.setGeometry(QtCore.QRect(377, 210, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.browse_file_button.setFont(font)
        self.browse_file_button.setObjectName("browser_file_button")
        self.lbl_query = QtWidgets.QLabel(self.aligning_box)
        self.lbl_query.setGeometry(QtCore.QRect(20, 30, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_query.setFont(font)
        self.lbl_query.setObjectName("lbl_query")
        self.lbl_query_len = QtWidgets.QLabel(self.aligning_box)
        self.lbl_query_len.setGeometry(QtCore.QRect(248, 34, 201, 21))
        self.lbl_query_len.setText("")
        self.lbl_query_len.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_query_len.setObjectName("lbl_query_len")
        self.submit = QtWidgets.QPushButton(self.centralwidget)
        self.submit.setGeometry(QtCore.QRect(950, 760, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setItalic(True)
        start_icon = QtGui.QIcon()
        start_icon.addPixmap(QtGui.QPixmap("./images/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.submit.setFont(font)
        self.submit.setAccessibleName("")
        self.submit.setStyleSheet("")
        self.submit.setIcon(start_icon)
        self.submit.setDefault(False)
        self.submit.setFlat(False)
        self.submit.setObjectName("submit")
        self.assembling_box = QtWidgets.QGroupBox(self.centralwidget)
        self.assembling_box.setGeometry(QtCore.QRect(20, 450, 471, 331))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.assembling_box.setFont(font)
        self.assembling_box.setObjectName("assembling_box")
        self.cut = MyQLineEdit(self.assembling_box, "70,20")
        self.cut.setGeometry(QtCore.QRect(260, 30, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setItalic(False)
        self.cut.setFont(font)
        self.cut.setInputMask("")
        self.cut.setMaxLength(5)
        self.cut.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cut.setObjectName("cut")
        self.min_contig = MyQLineEdit(self.assembling_box, "200")
        self.min_contig.setGeometry(QtCore.QRect(260, 180, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setItalic(False)
        self.min_contig.setFont(font)
        self.min_contig.setInputMask("")
        self.min_contig.setMaxLength(5)
        self.min_contig.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.min_contig.setObjectName("min_contig")
        self.lbl_gb = QtWidgets.QLabel(self.assembling_box)
        self.lbl_gb.setGeometry(QtCore.QRect(400, 290, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_gb.setFont(font)
        self.lbl_gb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_gb.setObjectName("lbl_gb")
        self.stage = QtWidgets.QComboBox(self.assembling_box)
        self.stage.setGeometry(QtCore.QRect(260, 240, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.stage.setFont(font)
        self.stage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stage.setObjectName("stage")
        self.stage.addItem("")
        self.stage.addItem("")
        self.stage.addItem("")
        self.stage.addItem("")
        self.stage.addItem("")
        self.trim_para = QtWidgets.QLineEdit(self.assembling_box)
        self.trim_para.setGeometry(QtCore.QRect(260, 210, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setItalic(False)
        self.trim_para.setFont(font)
        self.trim_para.setInputMask("")
        self.trim_para.setText("")
        self.trim_para.setMaxLength(5)
        self.trim_para.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.trim_para.setObjectName("trim_para")
        self.lbl_maxtarget = QtWidgets.QLabel(self.assembling_box)
        self.lbl_maxtarget.setGeometry(QtCore.QRect(20, 60, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_maxtarget.setFont(font)
        self.lbl_maxtarget.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_maxtarget.setObjectName("lbl_maxtarget")
        self.evalue = MyQLineEdit(self.assembling_box, "1e-3")
        self.evalue.setGeometry(QtCore.QRect(260, 90, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.evalue.setFont(font)
        self.evalue.setAutoFillBackground(False)
        self.evalue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.evalue.setObjectName("evalue")
        self.lbl_stage = QtWidgets.QLabel(self.assembling_box)
        self.lbl_stage.setGeometry(QtCore.QRect(160, 240, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_stage.setFont(font)
        self.lbl_stage.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_stage.setObjectName("lbl_stage")
        self.lbl_trimpara = QtWidgets.QLabel(self.assembling_box)
        self.lbl_trimpara.setGeometry(QtCore.QRect(70, 210, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_trimpara.setFont(font)
        self.lbl_trimpara.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_trimpara.setObjectName("lbl_trimpara")
        self.filter = QtWidgets.QCheckBox(self.assembling_box)
        self.filter.setEnabled(True)
        self.filter.setGeometry(QtCore.QRect(260, 120, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.filter.setFont(font)
        self.filter.setChecked(True)
        self.filter.setObjectName("filter")
        self.cpu = MyQLineEdit(self.assembling_box, str(cpu_count()))
        self.cpu.setGeometry(QtCore.QRect(90, 290, 71, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setItalic(False)
        self.cpu.setFont(font)
        self.cpu.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.cpu.setInputMask("99999")
        self.cpu.setText(str(cpu_count()))
        self.cpu.setMaxLength(5)
        self.cpu.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cpu.setObjectName("cpu")
        self.line_3 = QtWidgets.QFrame(self.assembling_box)
        self.line_3.setGeometry(QtCore.QRect(20, 150, 431, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.max_memory = MyQLineEdit(self.assembling_box, "4")
        self.max_memory.setGeometry(QtCore.QRect(350, 290, 71, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setItalic(False)
        self.max_memory.setFont(font)
        self.max_memory.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.max_memory.setInputMask("99999")
        self.max_memory.setText("4")
        self.max_memory.setMaxLength(5)
        self.max_memory.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_memory.setObjectName("max_memory")
        self.trim = QtWidgets.QCheckBox(self.assembling_box)
        self.trim.setGeometry(QtCore.QRect(40, 210, 16, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.trim.setFont(font)
        self.trim.setText("")
        self.trim.setChecked(True)
        self.trim.setObjectName("trim")
        self.lbl_evalue = QtWidgets.QLabel(self.assembling_box)
        self.lbl_evalue.setGeometry(QtCore.QRect(60, 90, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_evalue.setFont(font)
        self.lbl_evalue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_evalue.setObjectName("lbl_evalue")
        self.lbl_cut = QtWidgets.QLabel(self.assembling_box)
        self.lbl_cut.setGeometry(QtCore.QRect(50, 30, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_cut.setFont(font)
        self.lbl_cut.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cut.setObjectName("lbl_cut")
        self.lbl_cpu = QtWidgets.QLabel(self.assembling_box)
        self.lbl_cpu.setGeometry(QtCore.QRect(20, 290, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_cpu.setFont(font)
        self.lbl_cpu.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_cpu.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cpu.setObjectName("lbl_cpu")
        self.lbl_mem = QtWidgets.QLabel(self.assembling_box)
        self.lbl_mem.setGeometry(QtCore.QRect(210, 290, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_mem.setFont(font)
        self.lbl_mem.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_mem.setObjectName("lbl_mem")
        self.max_num_seq = MyQLineEdit(self.assembling_box, "500")
        self.max_num_seq.setGeometry(QtCore.QRect(260, 60, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setItalic(False)
        self.max_num_seq.setFont(font)
        self.max_num_seq.setInputMask("")
        self.max_num_seq.setMaxLength(5)
        self.max_num_seq.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_num_seq.setObjectName("max_num_seq")
        self.lbl_filter = QtWidgets.QLabel(self.assembling_box)
        self.lbl_filter.setGeometry(QtCore.QRect(170, 120, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_filter.setFont(font)
        self.lbl_filter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_filter.setObjectName("lbl_filter")
        self.lbl_mincontig = QtWidgets.QLabel(self.assembling_box)
        self.lbl_mincontig.setGeometry(QtCore.QRect(20, 180, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_mincontig.setFont(font)
        self.lbl_mincontig.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_mincontig.setObjectName("lbl_mincontig")
        self.output_box = QtWidgets.QGroupBox(self.centralwidget)
        self.output_box.setEnabled(False)
        self.output_box.setGeometry(QtCore.QRect(520, 200, 521, 541))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.output_box.setFont(font)
        self.output_box.setObjectName("output_box")
        self.output_log = QtWidgets.QTextBrowser(self.output_box)
        self.output_log.setEnabled(False)
        self.output_log.setGeometry(QtCore.QRect(20, 40, 481, 481))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(10)
        self.output_log.setFont(font)
        self.output_log.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.output_log.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_log.setOpenExternalLinks(True)
        self.output_log.setObjectName("output_log")
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(520, 760, 71, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.reset.setFont(font)
        self.reset.setObjectName("reset")
        self.reset.setEnabled(False)
        self.undo = QtWidgets.QPushButton(self.centralwidget)
        self.undo.setGeometry(QtCore.QRect(600, 760, 71, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        self.undo.setFont(font)
        self.undo.setObjectName("undo")
        self.undo.setHidden(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionExport_parameters = QtWidgets.QAction(MainWindow)
        # self.actionExport_parameters.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionExport_parameters.setFont(font)
        self.actionExport_parameters.setObjectName("actionExport_parameters")
        self.actionImport_parameters = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionImport_parameters.setFont(font)
        self.actionImport_parameters.setObjectName("actionImport_parameters")
        self.actionExit = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionExit.setFont(font)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_r2g = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionAbout_r2g.setFont(font)
        self.actionAbout_r2g.setObjectName("actionAbout_r2g")
        self.actionRestore_to_defaults = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionRestore_to_defaults.setFont(font)
        self.actionRestore_to_defaults.setObjectName("actionRestore_to_defaults")
        self.actionRestore_to_defaults.setEnabled(False)
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        self.actionUndo.setFont(font)
        self.actionUndo.setObjectName("actionUndo")
        self.menuFile.addAction(self.actionExport_parameters)
        self.menuFile.addAction(self.actionImport_parameters)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRestore_to_defaults)
        self.menuFile.addAction(self.actionUndo)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_r2g)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.results_box = QtWidgets.QGroupBox(self.centralwidget)
        self.results_box.setGeometry(QtCore.QRect(520, 10, 521, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.results_box.setFont(font)
        self.results_box.setObjectName("results_box")
        self.browse_outputdir_button = QtWidgets.QToolButton(self.results_box)
        self.browse_outputdir_button.setGeometry(QtCore.QRect(430, 130, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.browse_outputdir_button.setFont(font)
        self.browse_outputdir_button.setObjectName("browser_outputdir_button")
        self.outputdir = QtWidgets.QLineEdit(self.results_box)
        self.outputdir.setGeometry(QtCore.QRect(20, 130, 391, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.outputdir.setFont(font)
        self.outputdir.setObjectName("outputdir")
        self.lbl_outputdir = QtWidgets.QLabel(self.results_box)
        self.lbl_outputdir.setGeometry(QtCore.QRect(20, 100, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_outputdir.setFont(font)
        self.lbl_outputdir.setObjectName("lbl_outputdir")
        self.results = QtWidgets.QLineEdit(self.results_box)
        self.results.setGeometry(QtCore.QRect(20, 60, 481, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.results.setFont(font)
        self.results.setObjectName("results")
        self.lbl_results = QtWidgets.QLabel(self.results_box)
        self.lbl_results.setGeometry(QtCore.QRect(20, 30, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_results.setFont(font)
        self.lbl_results.setObjectName("lbl_results")
        self.lbl_mode = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.lbl_mode)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reads to Genes"))
        self.aligning_box.setTitle(_translate("MainWindow", "Aligning"))
        self.query.setPlainText(_translate("MainWindow", ">Gene_1\nATGCATGC"))
        self.program.setItemText(0, _translate("MainWindow", "blastn - megablast (highly similar sequences)"))
        self.program.setItemText(1, _translate("MainWindow", "blastn - discontiguous megablast (more dissimiliar sequences)"))
        self.program.setItemText(2, _translate("MainWindow", "blastn (nucleotide against nucleotide, return somewhat similar sequences)"))
        self.program.setItemText(3, _translate("MainWindow", "tblastn (protein against nucleotide)"))
        self.program.setItemText(4, _translate("MainWindow", "tblastx (translated nucleotide against translated nucleotide)"))
        self.lbl_sra.setText(_translate("MainWindow", "SRA Experiments (SRX) or SRA runs (SRR):"))
        self.lbl_program.setText(_translate("MainWindow", "Program:"))
        self.lbl_queryfile.setText(_translate("MainWindow", "Or, upload a file in FASTA format:"))
        self.browse_file_button.setText(_translate("MainWindow", "browse"))
        self.lbl_query.setText(_translate("MainWindow", "Enter FASTA sequence(s):"))
        self.submit.setText(_translate("MainWindow", "Start!"))
        self.assembling_box.setTitle(_translate("MainWindow", "Assembling"))
        self.cut.setText(_translate("MainWindow", "70,20"))
        self.min_contig.setText(_translate("MainWindow", "200"))
        self.lbl_gb.setText(_translate("MainWindow", "Gb"))
        self.stage.setItemText(0, _translate("MainWindow", "butterfly"))
        self.stage.setItemText(1, _translate("MainWindow", "chrysalis"))
        self.stage.setItemText(2, _translate("MainWindow", "inchworm"))
        self.stage.setItemText(3, _translate("MainWindow", "jellyfish"))
        self.stage.setItemText(4, _translate("MainWindow", "no trinity"))
        self.lbl_maxtarget.setText(_translate("MainWindow", "Max target sequences:"))
        self.evalue.setText(_translate("MainWindow", "1e-3"))
        self.lbl_stage.setText(_translate("MainWindow", "Stage:"))
        self.lbl_trimpara.setText(_translate("MainWindow", "Trim parameters:"))
        self.filter.setText(_translate("MainWindow", "Low complexity regions"))
        self.lbl_evalue.setText(_translate("MainWindow", "Expect threshold:"))
        self.lbl_cut.setText(_translate("MainWindow", "Fragment, overlap:"))
        self.lbl_cpu.setText(_translate("MainWindow", "CPU:"))
        self.lbl_mem.setText(_translate("MainWindow", "Max memory:"))
        self.max_num_seq.setText(_translate("MainWindow", "500"))
        self.lbl_filter.setText(_translate("MainWindow", "Filter:"))
        self.lbl_mincontig.setText(_translate("MainWindow", "Min contig length (bp):"))
        self.output_box.setTitle(_translate("MainWindow", "Output logs"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.undo.setText(_translate("MainWindow", "Undo"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExport_parameters.setText(_translate("MainWindow", "Export parameters..."))
        self.actionImport_parameters.setText(_translate("MainWindow", "Import parameters..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "R2g help"))
        self.actionAbout_r2g.setText(_translate("MainWindow", "About r2g"))
        self.actionRestore_to_defaults.setText(_translate("MainWindow", "Restore to defaults"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.results_box.setTitle(_translate("MainWindow", "Results"))
        self.browse_outputdir_button.setText(_translate("MainWindow", "browse"))
        self.lbl_outputdir.setText(_translate("MainWindow", "The directory where stores results:"))
        self.results.setText(_translate("MainWindow", "r2g_results"))
        self.lbl_results.setText(_translate("MainWindow", "The name of results:"))


import os
import sys
from copy import deepcopy
import re
import json
import subprocess
import random
import string

from PyQt5 import QtCore, QtWidgets, QtGui


class R2gMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    closeSignal = QtCore.pyqtSignal()

    def __init__(self):
        self.start_icon = QtGui.QIcon()
        self.start_icon.addPixmap(QtGui.QPixmap("./images/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_icon = QtGui.QIcon()
        self.stop_icon.addPixmap(QtGui.QPixmap("./images/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        super(R2gMainWindow, self).__init__()
        self.setupUi(self)
        self.default = self.obtain_parameters()
        self.user_param = {}
        self.tmp = ""
        self.cwd = os.getcwd()
        self.log = ""
        self.r2g_backend = R2gThread()
        self.connecter()
        self.show()

    def error_box(self, msg):
        QtWidgets.QMessageBox.critical(
            self,
            "Error!",
            msg,
            QtWidgets.QMessageBox.Abort
        )

    def info_box(self, msg):
        QtWidgets.QMessageBox.information(
            self,
            "Info",
            msg,
            QtWidgets.QMessageBox.Ok
        )

    def warning_box(self, msg):
        option = QtWidgets.QMessageBox.warning(
            self,
            "Warning",
            msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        return option

    def closeEvent(self, event):
        self.closeSignal.emit()

    def value_changed(self):
        user_param = self.obtain_parameters()
        if user_param != self.default:
            self.undo.setHidden(True)
            self.actionUndo.setEnabled(False)
            self.reset.setEnabled(True)
            self.actionRestore_to_defaults.setEnabled(True)
        else:
            self.undo.setVisible(True)
            self.actionUndo.setEnabled(True)
            self.reset.setEnabled(False)
            self.actionRestore_to_defaults.setEnabled(False)
        if len(self.sender().styleSheet()) > 0:
            self.sender().setStyleSheet("")
            self.submit.setEnabled(True)

    def obtain_parameters(self):
        """obtain parameters from the UI windows, and then transfer them to r2g input format:
        r2g parameters:
        {'verbose': True, 'retry': 5, 'cleanup': False, 'outdir': 'S6K_q-aae_s-SRX885420_c-80.50_p-blastn',
        'browser': 'http://139.59.216.78:4444/wd/hub', 'proxy': None, 'sra': 'SRX885420',
        'query': 'AAEL018120-RE.S6K.fasta', 'program': 'blastn', 'max_num_seq': 1000, 'evalue': 0.001, 'cut': '80,50',
        'CPU': 16, 'max_memory': '4G', 'min_contig_length': 150, 'trim': False, 'stage': 'butterfly', 'docker': False,
        'chrome_proxy': None, 'firefox_proxy': None}
        """
        parameters = {
            "query": deepcopy(self.query.toPlainText()),
            "query_file": deepcopy(self.query_file.text()),  # not the r2g parameters
            "sra": deepcopy(self.sra.text()),
            "program": deepcopy(self.program.currentText()),  # needs to be re-formatted
            "cut": deepcopy(self.cut.text()),
            "max_num_seq": deepcopy(self.max_num_seq.text()),
            "evalue": deepcopy(self.evalue.text()),
            "filter": deepcopy(self.filter.checkState()),
            "min_contig": deepcopy(self.min_contig.text()),
            "trim": deepcopy(self.trim.checkState()),
            "trim_param": deepcopy(self.trim_para.text()),  # not the r2g parameters
            "stage": deepcopy(self.stage.currentText()),
            "CPU": deepcopy(self.cpu.text()),
            "max_memory": deepcopy(self.max_memory.text()),
            "results": deepcopy(self.results.text()),  # not the r2g parameters
            "outdir": deepcopy(self.outputdir.text()),  # needs to be re-formatted
            "verbose": False,
            "retry": 5,
            "cleanup": False,
            "browser": None,
            "proxy": None,
            "docker": False,
            'chrome_proxy': None,
            'firefox_proxy': None,
            'path_json': None,
        }
        return parameters

    def set_parameters(self, parameters):
        self.query.setPlainText(parameters.get('query', ""))
        self.query_file.setText(parameters.get('query_file', ""))
        self.sra.setText(parameters.get('sra', ""))
        self.program.setCurrentText(parameters.get('program', "blastn - megablast (highly similar sequences"))
        self.cut.setText(parameters.get('cut', ""))
        self.max_num_seq.setText(parameters.get('max_num_seq', ""))
        self.evalue.setText(parameters.get('evalue', ""))
        self.filter.setChecked(parameters.get('filter', True))
        self.min_contig.setText(parameters.get('min_contig', ""))
        self.trim.setChecked(parameters.get("trim", True))
        self.trim_para.setText(parameters.get('trim_para', ""))
        self.stage.setCurrentText(parameters.get("stage", "butterfly"))
        self.cpu.setText(parameters.get("CPU", ""))
        self.max_memory.setText(parameters.get("max_memory", ""))
        self.results.setText(parameters.get("results", ""))
        self.outputdir.setText(parameters.get("outdir", ""))

    def openfile(self):
        opendir = self.cwd
        query_file = self.query_file.text()
        if len(query_file) > 0:
            if os.path.isfile(query_file):
                opendir = os.path.split(query_file)[0]
            elif os.path.isdir(query_file):
                opendir = query_file
        # filename, filetype
        openfile_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Please choose a sequence file in FASTA format",
            opendir,
            "FASTA Files (*.fasta *.fa *.fna *.faa *.txt);;All Files (*)"
        )
        if len(openfile_name) > 0:
            self.query_file.setText(openfile_name)
            with open(openfile_name, 'r') as inf:
                self.query.setPlainText(inf.read())
            self.cwd = os.path.split(openfile_name)[0]

    def select_dir(self):
        outdir = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Please select a directory to store results",
            self.cwd
        )
        if len(outdir) > 0:
            self.outputdir.setText(outdir)
            self.cwd = outdir

    def load_param_file(self):
        param_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Load parameters from a json file",
            self.cwd,
            "JSON Files (*.json *.txt);;All Files (*)"
        )
        if len(param_file) > 0:
            with open(param_file, 'r') as inf:
                try:
                    param_json = json.load(inf)
                except Exception as err:
                    self.error_box("Couldn't load parameters from the file \"{}\". {}".format(param_file, err))
                else:
                    self.set_parameters(param_json)
            self.cwd = os.path.split(param_file)[0]

    def save_param(self):
        param_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save parameters as...",
            self.cwd,
            "JSON Files (*.json *.txt);;All Files (*)"
        )
        if len(param_file) > 0:
            extension = os.path.splitext(param_file)[-1]
            if len(extension) == 0:
                param_file += ".json"
            try:
                with open(param_file, 'w') as outf:
                    self.user_param = self.obtain_parameters()
                    json.dump(self.user_param, outf, indent=4, separators=(",", ": "))
            except Exception as err:
                self.error_box("Couldn't save parameters as the file \"{}\". {}".format(param_file, err),)
            else:
                self.info_box("Saved parameters as the file \"{}\".".format(param_file))
            self.cwd = os.path.split(param_file)[0]

    def enable_trim(self):
        if self.trim.isChecked():
            self.lbl_trimpara.setEnabled(True)
            self.trim_para.setEnabled(True)
        else:
            self.lbl_trimpara.setEnabled(False)
            self.trim_para.setEnabled(False)

    def exit_(self):
        if self.submit.text() == "Stop!":
            warning = self.warning_box("The job is running. Are you sure about exiting?")
            if warning == QtWidgets.QMessageBox.Yes:
                sys.exit(0)
        else:
            sys.exit(0)

    def check_query(self):
        def _pl(w):
            if len(w) > 1:
                return "s"
            else:
                return ""
        query = self.query.toPlainText()
        # Show the length of the query:
        seq = query.strip().splitlines()
        if len(seq) > 0:
            if seq[0][0] == ">":
                seq = ''.join(seq[1:])
            else:
                seq = ''.join(seq)
            seq = ''.join(seq.strip().split())
            is_seq = self.check_sequences(seq)
            if is_seq == [True, False, False]:
                seq_type = "{} amino acid".format(len(seq)) + _pl(seq)
                self.cut.setText("24,7")
                self.program.setCurrentText("tblastn (protein against nucleotide)")
                for i in [0, 1, 2, 4]:
                    self.program.model().item(i).setEnabled(False)
            else:
                seq_type = "{} ambiguous sequence".format(len(seq)) + _pl(seq)
                self.cut.setText("70,20")
                self.program.setCurrentText("blastn - megablast (highly similar sequences)")
                if is_seq == [False, True, True]:
                    seq_type = "{} base".format(len(seq)) + _pl(seq)
                    self.program.model().item(3).setEnabled(False)
                elif is_seq == [False, False, False]:
                    self.change_bg_color(self.query, 'pink')
                    self.submit.setEnabled(False)
                    seq_type = "invalid sequence" + _pl(seq)
        if len(seq) == 0:
            seq_type = ""
        self.lbl_query_len.setText(seq_type)

    def activate_boxes(self, panel):
        if panel == "output":
            self.aligning_box.setEnabled(False)
            self.assembling_box.setEnabled(False)
            self.reset.setEnabled(False)
            self.results_box.setEnabled(False)
            self.query.setEnabled(False)
            self.output_box.setEnabled(True)
            self.output_log.setEnabled(True)
            self.output_log.clear()
            self.submit.setText("Stop!")
            self.submit.setIcon(self.stop_icon)
        elif panel == "input":
            self.submit.setText("Start!")
            self.submit.setIcon(self.start_icon)
            # self.output_log.setText("Stopped.")
            self.aligning_box.setEnabled(True)
            self.assembling_box.setEnabled(True)
            self.reset.setEnabled(True)
            # self.reset.setEnabled(True)
            self.results_box.setEnabled(True)
            self.query.setEnabled(True)
            # self.output_box.setEnabled(False)
            self.lbl_mode.setText("Stopped.")

    def check_sequences(self, seq):
        is_seq = [True, True, True]
        if len(seq) > 0:
            alphabets = [
                "ACDEFGHIKLMNPQRSTVWYBXZJUO",  # ambiguous protein
                "GATCRYWSMKHBVDNU",  # ambiguous nucleotide (DNA & RNA)
                "ATGCUN",  # relatively accurate nucleotide (DNA & RNA)
            ]
            # convert to dict:
            for i in range(len(alphabets)):
                alphabet = {}
                for chr in alphabets[i]:
                    alphabet[chr] = None
                alphabets[i] = deepcopy(alphabet)
            if seq.strip()[0] == ">":
                seq = ''.join(seq.strip().splitlines()[1:]).upper()
            else:
                seq = ''.join(seq.strip().splitlines()).upper()
            seq = ''.join(seq.strip().split())  # remove blanks
            for i in range(len(alphabets)):
                for letter in seq:
                    if letter not in alphabets[i]:
                        is_seq[i] = False
                        break
            # If sequences only contain ATGCUN, it is very possible that they are nuleotides:
            if is_seq[2] is True:
                is_seq[0] = False
        return is_seq

    def prompt_value_error(self, widgets, err_msg=""):
        if type(widgets) != list and type(widgets) != tuple:
            widgets = [widgets, ]
        self.error_box(err_msg)
        for w in widgets:
            self.change_bg_color(w, "pink")
        return False

    def change_bg_color(self, widget, color="white"):
        # warning-pink: 255, 196, 197
        color_dict = {
            "pink": "255, 196, 197",
            "white": "255, 255, 255",
        }
        widget.setStyleSheet("background-color: rgb({});".format(color_dict.get(color, "255, 255, 255")))

    def check_parameters(self, parameters):
        passed = True
        # check outdir:
        if len(parameters["results"].strip()) == 0:
            passed = self.prompt_value_error(
                self.results,
                "Please specify a directory to store results."
            )
        if len(parameters['outdir'].strip()) == 0:
            parameters['outdir'] = self.cwd
        if not (
                os.path.isdir(parameters['outdir']) and
                os.access(parameters['outdir'], os.X_OK) and
                os.access(parameters['outdir'], os.W_OK)
        ):
            passed = self.prompt_value_error(
                self.outputdir,
                "Please specify a valid directory to store results."
            )
        else:
            self.cwd = deepcopy(parameters['outdir'])
            parameters['outdir'] = os.path.join(parameters['outdir'].strip(), parameters['results'].strip())
        # check query and query_file
        if len(parameters["query_file"].strip()) == 0:
            if len(parameters["query"].strip()) == 0:
                passed = self.prompt_value_error(
                    [self.query, self.query_file],
                    "Please either input sequences or specify a file."
                )
            else:
                # sometimes the query is too long to be passed to r2g cmd:
                self.tmp = os.path.join(
                    parameters['outdir'],
                    "r2g_query.{}-{}.tmp.fasta".format(
                        os.getpid(), ''.join(random.sample(string.ascii_letters + string.digits, 8))
                    )
                )
                try:
                    with open(self.tmp, 'w') as outf:
                        outf.write(parameters['query'])
                except Exception:
                    passed = self.prompt_value_error(
                        [self.outputdir, self.results],
                        "Couldn't write files in the directory: \"{}\".".format(parameters['outdir'])
                    )
                else:
                    # directly pass the parameter to r2g cmd:
                    parameters['query'] = deepcopy(self.tmp)
        else:
            try:
                with open(parameters["query_file"], 'r') as inf:
                    seq = inf.read()
                if True in self.check_sequences(seq):
                    self.query.setPlainText(seq)
                    # directly pass the parameter to r2g cmd:
                    parameters["query"] = deepcopy(parameters['query_file'].strip())
                else:
                    raise ValueError
            except Exception as err:
                passed = self.prompt_value_error(
                    self.query_file,
                    "The query file doesn't exist or contain valid sequences: \"{}\". "
                    "{}".format(parameters["query_file"], err)
                )
        # check sra:
        try:
            re.search(r'^(\w{3}\d+)$', parameters.get("sra", "")).group(1)
        except Exception:
            passed = self.prompt_value_error(
                self.sra,
                "Please input a valid SRA accession number."
            )
        else:
            parameters['sra'] = deepcopy(parameters['sra'].strip().upper())
        # check cut:
        try:
            cut = parameters['cut'].strip().split(',')
            frag = int(cut[0].strip())
            ovlp = int(cut[-1].strip())
            assert frag > ovlp
        except Exception:
            passed = self.prompt_value_error(
                self.cut,
                'Please input a valid "Fragment,overlap" value.'
            )
        else:
            parameters['cut'] = "{},{}".format(frag, ovlp)
        # check max_num_seq:
        try:
            _ = int(parameters["max_num_seq"])
        except Exception:
            passed = self.prompt_value_error(
                self.max_num_seq,
                'Please input a valid "Max target sequences" value.'
            )
        else:
            parameters["max_num_seq"] = deepcopy(parameters["max_num_seq"].strip())
        # check evalue:
        try:
            _ = float(parameters["evalue"])
        except Exception:
            passed = self.prompt_value_error(
                self.evalue,
                'Please input a valid "Expect threshold" value.'
            )
        else:
            parameters["evalue"] = deepcopy(parameters["evalue"].strip())
        # check min_contig:
        try:
            _ = int(parameters["min_contig"])
        except Exception:
            passed = self.prompt_value_error(
                self.min_contig,
                'Please input a valid "Min contig length" value.'
            )
        else:
            parameters["min_contig"] = deepcopy(parameters["min_contig"].strip())
        # check cpu:
        try:
            cpu = int(parameters["CPU"])
            assert cpu <= cpu_count()
        except Exception:
            passed = self.prompt_value_error(
                self.cpu,
                'Please input a valid "CPU" value.'
            )
        else:
            parameters["CPU"] = deepcopy(parameters["CPU"].strip())
        # check max_memory:
        try:
            _ = int(parameters["max_memory"])
        except Exception:
            passed = self.prompt_value_error(
                self.max_memory,
                'Please input a valid "Max memory" value.'
            )
        else:
            parameters["max_memory"] = deepcopy(parameters["max_memory"].strip())
        # reformat program:
        if parameters["program"][:10] == "blastn - m":
            parameters['program'] = "megablast"
        elif parameters["program"][:10] == "blastn - d":
            parameters['program'] = "discomegablast"
        elif parameters["program"][:10] == "blastn (pr":
            parameters['program'] = "blastn"
        elif parameters["program"][:7] == "tblastn":
            parameters['program'] = "tblastn"
        elif parameters["program"][:7] == "tblastx":
            parameters['program'] = "tblastx"
        if not passed:
            self.submit.setEnabled(False)
        return passed, parameters

    def call_r2g(self):
        if self.submit.text() == "Start!":
            parameters = self.obtain_parameters()
            # self.output_log.append(str(parameters))
            passed, parameters = self.check_parameters(parameters)
            if passed:
                self.activate_boxes("output")
                self.r2g_backend.construct_cmd(parameters)
                self.r2g_backend.start()
        elif self.submit.text() == "Stop!":
            warning = self.warning_box("Are you sure about stopping the running job?")
            if warning == QtWidgets.QMessageBox.Yes:
                self.r2g_backend.quit()
                self.output_log.append("Aborted.")
                self.activate_boxes("input")

    def clear_default(self, default_value):
        self.sender().setReadOnly(False)
        if self.sender().text() == default_value:
            self.sender().clear()

    def set_default(self, default_value):
        self.sender().setReadOnly(True)
        if len(self.sender().text().strip()) < 1:
            self.sender().setText(default_value)

    def reset_para(self):
        self.user_param = self.obtain_parameters()
        if self.user_param != self.default:
            self.undo.setVisible(True)
            self.actionUndo.setEnabled(True)
            self.reset.setEnabled(False)
            self.actionRestore_to_defaults.setEnabled(False)
            self.set_parameters(self.default)

    def undo_para(self):
        self.undo.setHidden(True)
        self.actionUndo.setEnabled(False)
        self.set_parameters(self.user_param)

    def print_log(self, log):
        """transfer bash color to html color:
        """
        # TODO
        # log = '<font color="#FF0000">' + "warning" + "</font> " + " ???"
        # light_palette = {
        #     "32": "#ABEBC6",  # green
        #     "37": "#EAEDED",  # white
        #     "33": "#F9E79F",  # yellow
        #     "31": "#F5B7B1",  # red
        #     "36": "#AED6F1",  # light blue
        #     "34": "#5499C7",  # blue
        # }
        # dark_palette = {
        #     "32": "#196F3D",  # green
        #     "37": "#2E4053",  # white
        #     "33": "#F1C40F",  # yellow
        #     "31": "#CB4335",  # red
        #     "36": "#3498DB",  # light blue
        #     "34": "#1F618D",  # blue
        # }
        # for p in dark_palette.items():
        #     p_pattern = re.compile(r'\\033\[{}m'.format(p[0]))
        #     log = p_pattern.sub(r'<font color="{}">'.format(p[-1]), log)
        self.output_log.setText(log)

    def print_mode(self, mode):
        self.lbl_mode.setText("Running in the {} mode...".format(mode))

    def housekeeping(self, done_msg):
        if done_msg != "0":
            self.error_box("Calling r2g failed. {}".format(done_msg))
        else:
            self.info_box("Calling r2g done.")
        self.activate_boxes("input")
        os.remove(self.tmp)

    def connecter(self):
        # value changed:
        self.query.textChanged.connect(self.value_changed)
        self.query_file.textChanged.connect(self.value_changed)
        self.sra.textChanged.connect(self.value_changed)
        self.cut.textChanged.connect(self.value_changed)
        self.max_num_seq.textChanged.connect(self.value_changed)
        self.evalue.textChanged.connect(self.value_changed)
        self.min_contig.textChanged.connect(self.value_changed)
        self.trim_para.textChanged.connect(self.value_changed)
        self.stage.currentTextChanged.connect(self.value_changed)
        self.cpu.textChanged.connect(self.value_changed)
        self.max_memory.textChanged.connect(self.value_changed)
        self.results.textChanged.connect(self.value_changed)
        self.outputdir.textChanged.connect(self.value_changed)
        self.program.currentTextChanged.connect(self.value_changed)
        self.trim.stateChanged.connect(self.value_changed)
        # choose a query file:
        self.browse_file_button.clicked.connect(self.openfile)
        # select an output dir:
        self.browse_outputdir_button.clicked.connect(self.select_dir)
        # trim or not:
        self.trim.stateChanged.connect(self.enable_trim)
        # submit to run or stop:
        self.submit.clicked.connect(self.call_r2g)
        # exit:
        self.actionExit.triggered.connect(self.exit_)
        self.closeSignal.connect(self.exit_)
        # check the query sequence:
        self.query.textChanged.connect(self.check_query)
        # clear the default value:
        self.query.FocusInSignal.connect(self.clear_default)
        # self.query.FocusOutSignal.connect(self.set_default)
        self.cut.FocusInSignal.connect(self.clear_default)
        self.cut.FocusOutSignal.connect(self.set_default)
        self.max_num_seq.FocusInSignal.connect(self.clear_default)
        self.max_num_seq.FocusOutSignal.connect(self.set_default)
        self.evalue.FocusInSignal.connect(self.clear_default)
        self.evalue.FocusOutSignal.connect(self.set_default)
        self.min_contig.FocusInSignal.connect(self.clear_default)
        self.min_contig.FocusOutSignal.connect(self.set_default)
        self.cpu.FocusInSignal.connect(self.clear_default)
        self.cpu.FocusOutSignal.connect(self.set_default)
        self.max_memory.FocusInSignal.connect(self.clear_default)
        self.max_memory.FocusOutSignal.connect(self.set_default)
        # restore and undo parameters:
        self.reset.clicked.connect(self.reset_para)
        self.actionRestore_to_defaults.triggered.connect(self.reset_para)
        self.undo.clicked.connect(self.undo_para)
        self.actionUndo.triggered.connect(self.undo_para)
        # save and load parameters from files:
        self.actionImport_parameters.triggered.connect(self.load_param_file)
        self.actionExport_parameters.triggered.connect(self.save_param)
        # return logs from the r2g backend thread:
        self.r2g_backend.outputSignal.connect(self.print_log)
        self.r2g_backend.modeSignal.connect(self.print_mode)
        self.r2g_backend.doneSignal.connect(self.housekeeping)


class R2gThread(QtCore.QThread):
    outputSignal = QtCore.pyqtSignal(str)
    modeSignal = QtCore.pyqtSignal(str)
    doneSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(R2gThread, self).__init__(parent)
        self.backend_mode = ""
        # try:
        #     import r2g
        #     self.backend_mode = "local"
        # except ModuleNotFoundError:
        #     self.backend_mode = "docker"
        self.parameters = {}
        # self.cmd = ["r2g", "--help"]
        self.cmd = ["r2g", ]
        self.log = ""

    def construct_cmd(self, parameters):
        # parse trim:
        if parameters['trim'] is True:
            self.cmd += ['--trim', ]
            if len(parameters["trim_para"]) > 0:
                self.cmd += [parameters["trim_para"], ]
        # integrate other parameters:
        self.cmd += [
            "--query", parameters["query"],
            "--outdir", parameters["outdir"],
            "--program", parameters["program"],
            "--sra", parameters["sra"],
            "--max_num_seq", parameters["max_num_seq"],
            "--evalue", parameters["evalue"],
            "--cut", parameters["cut"],
            "--CPU", parameters["CPU"],
            "--max_memory", parameters["max_memory"],
            "--min_contig_length", parameters["min_contig"],
            "--stage", parameters["stage"],
        ]

    def run(self):
        self.modeSignal.emit(self.backend_mode)
        print(' '.join(self.cmd))
        try:
            with subprocess.Popen(
                self.cmd,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                text=True
            ) as p:
                for line in iter(p.stdout.readline, b""):
                    if len(line) == 0:
                        break
                    self.log += line
                    self.outputSignal.emit(self.log)
                p.wait()
                self.doneSignal.emit(str(p.returncode))
        except Exception as err:
            self.doneSignal.emit(err)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _ = R2gMainWindow()
    sys.exit(app.exec_())
