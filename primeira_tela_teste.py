# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'primeira_tela.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PontoDigital(object):
    def setupUi(self, PontoDigital):
        PontoDigital.setObjectName("PontoDigital")
        PontoDigital.resize(441, 442)
        PontoDigital.setStyleSheet("background-color: rgb(255, 205, 210);")
        PontoDigital.setSizeGripEnabled(False)
        self.lineEdit_3 = QtWidgets.QLineEdit(PontoDigital)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 60, 341, 31))
        self.lineEdit_3.setStyleSheet("border-radius: 5px;\n"
"font: 11pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width:2px;")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(PontoDigital)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 110, 341, 31))
        self.lineEdit_2.setStyleSheet("border-radius: 5px;\n"
"background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width:2px;\n"
"font: 11pt \"MS Shell Dlg 2\";")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(PontoDigital)
        self.label_2.setGeometry(QtCore.QRect(80, 150, 341, 21))
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 11pt \"MS Shell Dlg 2\";")
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.icone_cadeado = QtWidgets.QLabel(PontoDigital)
        self.icone_cadeado.setGeometry(QtCore.QRect(20, 110, 31, 31))
        self.icone_cadeado.setText("")
        self.icone_cadeado.setPixmap(QtGui.QPixmap("icon_cadeado.png"))
        self.icone_cadeado.setObjectName("icone_cadeado")
        self.icone_usuario = QtWidgets.QLabel(PontoDigital)
        self.icone_usuario.setGeometry(QtCore.QRect(20, 60, 31, 31))
        self.icone_usuario.setText("")
        self.icone_usuario.setPixmap(QtGui.QPixmap("icon_usuario.png"))
        self.icone_usuario.setObjectName("icone_usuario")
        self.button_cadastrar_novo_usuario = QtWidgets.QPushButton(PontoDigital)
        self.button_cadastrar_novo_usuario.setGeometry(QtCore.QRect(20, 410, 191, 21))
        self.button_cadastrar_novo_usuario.setStyleSheet("background-color: rgb(220, 90, 110);\n"
"\n"
"")
        self.button_cadastrar_novo_usuario.setObjectName("button_cadastrar_novo_usuario")
        self.calendarWidget = QtWidgets.QCalendarWidget(PontoDigital)
        self.calendarWidget.setGeometry(QtCore.QRect(20, 230, 401, 171))
        self.calendarWidget.setStyleSheet("border-style: outset;\n"
"border-width:2px;\n"
"border-radius: 5px;\n"
"")
        self.calendarWidget.setObjectName("calendarWidget")
        self.label_5 = QtWidgets.QLabel(PontoDigital)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 401, 41))
        self.label_5.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.button_entrada = QtWidgets.QPushButton(PontoDigital)
        self.button_entrada.setGeometry(QtCore.QRect(100, 180, 141, 31))
        self.button_entrada.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(220, 90, 110);\n"
"")
        self.button_entrada.setObjectName("button_entrada")
        self.button_saida = QtWidgets.QPushButton(PontoDigital)
        self.button_saida.setGeometry(QtCore.QRect(270, 180, 131, 31))
        self.button_saida.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(200, 100, 150);\n"
"\n"
"")
        self.button_saida.setObjectName("button_saida")
        self.button_pesquisar = QtWidgets.QPushButton(PontoDigital)
        self.button_pesquisar.setGeometry(QtCore.QRect(230, 410, 191, 21))
        self.button_pesquisar.setStyleSheet("background-color: rgb(220, 90, 110);\n"
"")
        self.button_pesquisar.setObjectName("button_pesquisar")

        self.retranslateUi(PontoDigital)
        QtCore.QMetaObject.connectSlotsByName(PontoDigital)
        PontoDigital.setTabOrder(self.lineEdit_3, self.lineEdit_2)
        PontoDigital.setTabOrder(self.lineEdit_2, self.button_entrada)
        PontoDigital.setTabOrder(self.button_entrada, self.button_saida)
        PontoDigital.setTabOrder(self.button_saida, self.button_cadastrar_novo_usuario)
        PontoDigital.setTabOrder(self.button_cadastrar_novo_usuario, self.button_pesquisar)
        PontoDigital.setTabOrder(self.button_pesquisar, self.calendarWidget)

    def retranslateUi(self, PontoDigital):
        _translate = QtCore.QCoreApplication.translate
        PontoDigital.setWindowTitle(_translate("PontoDigital", "Relógio de ponto"))
        self.lineEdit_3.setPlaceholderText(_translate("PontoDigital", "Digite seu login"))
        self.lineEdit_2.setPlaceholderText(_translate("PontoDigital", "Digite sua senha"))
        self.button_cadastrar_novo_usuario.setText(_translate("PontoDigital", "Cadastrar usuário"))
        self.label_5.setText(_translate("PontoDigital", "Ponto Digital"))
        self.button_entrada.setText(_translate("PontoDigital", "Entrada"))
        self.button_saida.setText(_translate("PontoDigital", "Saida"))
        self.button_pesquisar.setText(_translate("PontoDigital", "Consultar marcações"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PontoDigital = QtWidgets.QDialog()
    ui = Ui_PontoDigital()
    ui.setupUi(PontoDigital)
    PontoDigital.show()
    sys.exit(app.exec_())