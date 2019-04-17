# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import operator
from bitstring import BitArray

from execute1 import execute
import syntax
from assemulator import mc_generator

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit_as = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_as.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_as.setSizePolicy(sizePolicy)
        self.plainTextEdit_as.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.plainTextEdit_as.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit_as.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_as.setPlainText("")
        self.plainTextEdit_as.setObjectName("plainTextEdit_as")
        self.highlight = syntax.AssemblyHighlighter(self.plainTextEdit_as.document())    #-----------
        MainWindow.setStyleSheet('''QPlainTextEdit{font-size: 20px;font-weight: 400;}''')#-----------
        self.gridLayout.addWidget(self.plainTextEdit_as, 2, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.mc_assemble = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mc_assemble.sizePolicy().hasHeightForWidth())
        self.mc_assemble.setSizePolicy(sizePolicy)
        self.mc_assemble.setObjectName("mc_assemble")
        self.horizontalLayout_4.addWidget(self.mc_assemble)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 3, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_2.setContentsMargins(-1, -1, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.step = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step.sizePolicy().hasHeightForWidth())
        self.step.setSizePolicy(sizePolicy)
        self.step.setObjectName("step")
        self.gridLayout_2.addWidget(self.step, 0, 3, 1, 1)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)
        self.reset.setObjectName("reset")
        self.gridLayout_2.addWidget(self.reset, 0, 4, 1, 1)
        self.run = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run.sizePolicy().hasHeightForWidth())
        self.run.setSizePolicy(sizePolicy)
        self.run.setObjectName("run")
        self.gridLayout_2.addWidget(self.run, 0, 2, 1, 1)
        self.plainTextEdit_console = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_console.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_console.setSizePolicy(sizePolicy)
        self.plainTextEdit_console.setMinimumSize(QtCore.QSize(0, 100))
        self.plainTextEdit_console.setDocumentTitle("")
        self.plainTextEdit_console.setReadOnly(True)
        self.plainTextEdit_console.setPlainText("")
        self.plainTextEdit_console.setObjectName("plainTextEdit_console")
        self.gridLayout_2.addWidget(self.plainTextEdit_console, 1, 0, 2, 5)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 5, 2, 2, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setIndent(5)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.as_assemble = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.as_assemble.sizePolicy().hasHeightForWidth())
        self.as_assemble.setSizePolicy(sizePolicy)
        self.as_assemble.setObjectName("as_assemble")
        self.horizontalLayout_2.addWidget(self.as_assemble)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.plainTextEdit_mc = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_mc.setObjectName("plainTextEdit_mc")
        self.gridLayout.addWidget(self.plainTextEdit_mc, 2, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 8, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(378, 0))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView_2 = QtWidgets.QTableView(self.tab_2)
        self.tableView_2.setObjectName("tableView_2")
        self.verticalLayout_2.addWidget(self.tableView_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 8, 5, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 17))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuFIle.addAction(self.actionExit)
        self.menuFIle.addAction(self.actionEixt)
        self.menuAbout.addAction(self.actionHelp)
        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #populate
        self.comboIndex = 0
        self.pc_temp = 0
        self.Execute = execute()
        self.populate()
        self.run.clicked.connect(self.Run)
        self.as_assemble.clicked.connect(self.assemble_as)
        self.mc_assemble.clicked.connect(self.assemble_mc)
        self.reset.clicked.connect(self.assemble_mc)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.step.clicked.connect(self.Step)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label_2.setText(_translate("MainWindow", "Machine Code"))
        self.mc_assemble.setText(_translate("MainWindow", "Assemble"))
        self.step.setText(_translate("MainWindow", "Step"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.run.setText(_translate("MainWindow", "Run"))
        self.label_3.setText(_translate("MainWindow", "Console Output"))
        self.label.setText(_translate("MainWindow", "Assembly Code"))
        self.as_assemble.setText(_translate("MainWindow", "Assemble"))
        self.comboBox.setItemText(0, _translate("MainWindow", "HEX"))
        self.comboBox.setItemText(1, _translate("MainWindow", "DECIMAL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Register"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Memory"))
        self.menuFIle.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Open"))
        self.actionEixt.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))


    def populate(self):
        regs = self.Execute.returnRegisters()
        reglist = []
        for i in range(len(regs)):
            value = regs['{0:05b}'.format(i)]
            if self.comboIndex == 0:
                b = BitArray(int = value, length=32)
                value = '0x' + b.hex
            reglist.append(["x"+str(i),value])

        if len(reglist)>0:
            table_model = MyTableModel(self, reglist, ["Register",'value'])
            self.tableView.setModel(table_model)
            header = self.tableView.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        mem = self.Execute.returnMemory()
        memlist = []
        for key, value in mem.items():
            if key %4 == 0:
                content = ["0x"+'{:08x}'.format(key),self.Execute.readbyteMemory(key),
                self.Execute.readbyteMemory(key+1),
                self.Execute.readbyteMemory(key+2),
                self.Execute.readbyteMemory(key+3)]
                if self.comboIndex == 0:
                    content = ["0x"+'{:08x}'.format(key),
                        BitArray(int=self.Execute.readbyteMemory(key), length = 8).hex,
                        BitArray(int=self.Execute.readbyteMemory(key+1), length = 8).hex,
                        BitArray(int=self.Execute.readbyteMemory(key+2), length = 8).hex,
                        BitArray(int=self.Execute.readbyteMemory(key+3), length = 8).hex]
                memlist.append(content)

        if len(memlist)>0:
            table_model = MyTableModel(self, memlist, ["Address",'+0','+1','+2','+3'])
            self.tableView_2.setModel(table_model)
            header = self.tableView_2.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        self.highlightline(self.Execute.PC/4,True)
        

    def assemble(self):
        self.Execute.assemble("code.mc")
        self.populate()
        MC = open("code.mc","r")
        self.plainTextEdit_mc.setPlainText(MC.read())
    
    def assemble_mc(self):
        self.highlightline(self.pc_temp,False)
        mc_code = self.plainTextEdit_mc.toPlainText()
        self.Execute.assemble(mc_code)
        self.populate()
        self.run.setEnabled(True)
        self.step.setEnabled(True)

    def assemble_as(self):
        as_code = self.plainTextEdit_as.toPlainText()
        mc_code = mc_generator(as_code)
        self.plainTextEdit_mc.setPlainText(mc_code)
        self.Execute.assemble(mc_code)
        self.populate()
        self.run.setEnabled(True)
        self.step.setEnabled(True)


    def Run(self):
        self.Execute.runPipeLine()
        self.populate()
        self.run.setEnabled(False)
        self.step.setEnabled(False)
        self.plainTextEdit_console.appendPlainText("No. of Cycles taken to execute : "+str(self.Execute.cycle))
        self.plainTextEdit_console.appendPlainText("No. of Stalls : "+str(self.Execute.stalls))

    def Step(self):
        self.highlightline(self.Execute.PC/4,False)
        self.Execute.runPipeLineStep()
        self.populate()
        if self.Execute.stopPipeLine:
            self.Execute.stopPipeLine = False
            self.run.setEnabled(False)
            self.step.setEnabled(False)
            self.plainTextEdit_console.appendPlainText("No. of Cycles taken to execute : "+str(self.Execute.cycle))
            self.plainTextEdit_console.appendPlainText("No. of Stalls : "+str(self.Execute.stalls))

        self.pc_temp = self.Execute.PC/4

        

    def on_combobox_changed(self, value):
        self.comboIndex = value
        self.populate()

    def highlightline(self,linino,color):
        fmt = QtGui.QTextCharFormat()
        if color:
            fmt.setBackground(QtCore.Qt.blue)
            fmt.setForeground(QtCore.Qt.white)
        else:
            fmt.setBackground(QtCore.Qt.white)

        block = self.plainTextEdit_mc.document().findBlockByLineNumber(linino)
        blockPos = block.position()

        cursor = QtGui.QTextCursor(self.plainTextEdit_mc.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.setCharFormat(fmt)

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtWidgets.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtWidgets.SIGNAL("layoutChanged()"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
