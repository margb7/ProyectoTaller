# Form implementation generated from reading ui file 'dlgSalir.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 185)
        Dialog.setMinimumSize(QtCore.QSize(300, 185))
        Dialog.setMaximumSize(QtCore.QSize(485, 209))
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnSalir = QtWidgets.QPushButton(Dialog)
        self.btnSalir.setMinimumSize(QtCore.QSize(70, 50))
        self.btnSalir.setMaximumSize(QtCore.QSize(70, 20))
        self.btnSalir.setObjectName("btnSalir")
        self.horizontalLayout.addWidget(self.btnSalir)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setMinimumSize(QtCore.QSize(70, 50))
        self.pushButton_2.setMaximumSize(QtCore.QSize(70, 20))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(50)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(75, 75))
        self.label_2.setMaximumSize(QtCore.QSize(75, 75))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./img/icono_alerta.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lblSalir = QtWidgets.QLabel(Dialog)
        self.lblSalir.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblSalir.setFont(font)
        self.lblSalir.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblSalir.setObjectName("lblSalir")
        self.horizontalLayout_2.addWidget(self.lblSalir)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Salir"))
        self.btnSalir.setText(_translate("Dialog", "Salir"))
        self.pushButton_2.setText(_translate("Dialog", "No"))
        self.lblSalir.setText(_translate("Dialog", "¿ Desea salir ?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
