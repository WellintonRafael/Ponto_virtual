# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_pesquisa.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(612, 633)
        MainWindow.setMinimumSize(QtCore.QSize(612, 633))
        MainWindow.setMaximumSize(QtCore.QSize(612, 633))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 571, 141))
        self.groupBox.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 551, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_2.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.lineEdit_2.setPlaceholderText("")
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.horizontalLayout.setStretch(0, 9)
        self.horizontalLayout.setStretch(1, 15)
        self.horizontalLayout.setStretch(2, 5)
        self.horizontalLayout.setStretch(3, 12)
        self.horizontalLayout.setStretch(4, 5)
        self.horizontalLayout.setStretch(5, 12)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 341, 61))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_pesquisa = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_pesquisa.setAutoFillBackground(True)
        self.pushButton_pesquisa.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"")
        self.pushButton_pesquisa.setAutoDefault(False)
        self.pushButton_pesquisa.setDefault(True)
        self.pushButton_pesquisa.setObjectName("pushButton_pesquisa")
        self.horizontalLayout_2.addWidget(self.pushButton_pesquisa)
        self.pushButton_voltar = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_voltar.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";")
        self.pushButton_voltar.setObjectName("pushButton_voltar")
        self.horizontalLayout_2.addWidget(self.pushButton_voltar)
        self.horizontalLayout_2.setStretch(0, 20)
        self.horizontalLayout_2.setStretch(1, 20)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(420, 70, 141, 61))
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 126, 44))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_tudo = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_tudo.setStyleSheet("")
        self.radioButton_tudo.setChecked(True)
        self.radioButton_tudo.setObjectName("radioButton_tudo")
        self.verticalLayout.addWidget(self.radioButton_tudo)
        self.radioButton_por_data = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_por_data.setObjectName("radioButton_por_data")
        self.verticalLayout.addWidget(self.radioButton_por_data)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 160, 571, 431))
        self.groupBox_2.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.groupBox_2.setObjectName("groupBox_2")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 551, 341))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(108)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 531, 21))
        self.label_5.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"\n"
"")
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setIndent(-1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 390, 551, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_corrigir = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_corrigir.setEnabled(False)
        self.pushButton_corrigir.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(80, 80, 255);")
        self.pushButton_corrigir.setObjectName("pushButton_corrigir")
        self.horizontalLayout_3.addWidget(self.pushButton_corrigir)
        self.pushButton_pdf = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_pdf.setEnabled(False)
        self.pushButton_pdf.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(255, 40, 40);")
        self.pushButton_pdf.setObjectName("pushButton_pdf")
        self.horizontalLayout_3.addWidget(self.pushButton_pdf)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 612, 21))
        self.menubar.setObjectName("menubar")
        self.menuArquivo = QtWidgets.QMenu(self.menubar)
        self.menuArquivo.setObjectName("menuArquivo")
        self.menuSair = QtWidgets.QMenu(self.menubar)
        self.menuSair.setObjectName("menuSair")
        self.menuAjuda = QtWidgets.QMenu(self.menubar)
        self.menuAjuda.setObjectName("menuAjuda")
        self.menuSair_2 = QtWidgets.QMenu(self.menubar)
        self.menuSair_2.setObjectName("menuSair_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSalvar = QtWidgets.QAction(MainWindow)
        self.actionSalvar.setObjectName("actionSalvar")
        self.actionImprimir = QtWidgets.QAction(MainWindow)
        self.actionImprimir.setObjectName("actionImprimir")
        self.actionFechar = QtWidgets.QAction(MainWindow)
        self.actionFechar.setObjectName("actionFechar")
        self.actionSair = QtWidgets.QAction(MainWindow)
        self.actionSair.setObjectName("actionSair")
        self.menuArquivo.addAction(self.actionSalvar)
        self.menuArquivo.addAction(self.actionImprimir)
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.actionFechar)
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.actionSair)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuSair.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())
        self.menubar.addAction(self.menuSair_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        MainWindow.setTabOrder(self.lineEdit_3, self.radioButton_tudo)
        MainWindow.setTabOrder(self.radioButton_tudo, self.radioButton_por_data)
        MainWindow.setTabOrder(self.radioButton_por_data, self.pushButton_pesquisa)
        MainWindow.setTabOrder(self.pushButton_pesquisa, self.pushButton_voltar)
        MainWindow.setTabOrder(self.pushButton_voltar, self.pushButton_corrigir)
        MainWindow.setTabOrder(self.pushButton_corrigir, self.pushButton_pdf)
        MainWindow.setTabOrder(self.pushButton_pdf, self.tableWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Relógio de ponto > Consultar marcações"))
        self.groupBox.setTitle(_translate("MainWindow", "Pesquisar"))
        self.label.setText(_translate("MainWindow", "Funcionário nº:"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Cód. funcinário"))
        self.label_3.setText(_translate("MainWindow", "Data inicio:"))
        self.lineEdit_2.setInputMask(_translate("MainWindow", "99/99/9999"))
        self.label_4.setText(_translate("MainWindow", "Data fim:"))
        self.lineEdit_3.setInputMask(_translate("MainWindow", "99/99/9999"))
        self.pushButton_pesquisa.setText(_translate("MainWindow", "Pesquisar"))
        self.pushButton_voltar.setText(_translate("MainWindow", "Voltar"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Filtrar:"))
        self.radioButton_tudo.setText(_translate("MainWindow", "Todas marcações"))
        self.radioButton_por_data.setText(_translate("MainWindow", "Por data"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Resultado da pesquisa"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Data"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Entrada"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Saída"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Entrada"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Saída"))
        self.pushButton_corrigir.setText(_translate("MainWindow", "Corrigir"))
        self.pushButton_pdf.setText(_translate("MainWindow", "Gerar PDF"))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuSair.setTitle(_translate("MainWindow", "Configurações"))
        self.menuAjuda.setTitle(_translate("MainWindow", "Ajuda"))
        self.menuSair_2.setTitle(_translate("MainWindow", "Sair"))
        self.actionSalvar.setText(_translate("MainWindow", "Salvar"))
        self.actionImprimir.setText(_translate("MainWindow", "Imprimir"))
        self.actionFechar.setText(_translate("MainWindow", "Fechar"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
