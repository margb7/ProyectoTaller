# Form implementation generated from reading ui file 'ventCalendario.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ventCalendar(object):
    def setupUi(self, ventCalendar):
        ventCalendar.setObjectName("ventCalendar")
        ventCalendar.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        ventCalendar.resize(521, 375)
        ventCalendar.setMinimumSize(QtCore.QSize(320, 230))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/icono_calendario.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventCalendar.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ventCalendar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setMinimumSize(QtCore.QSize(320, 190))
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 1, 0, 1, 1)
        self.lblFechaCalendario = QtWidgets.QLabel(self.centralwidget)
        self.lblFechaCalendario.setMinimumSize(QtCore.QSize(0, 50))
        self.lblFechaCalendario.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblFechaCalendario.setObjectName("lblFechaCalendario")
        self.gridLayout.addWidget(self.lblFechaCalendario, 0, 0, 1, 1)
        ventCalendar.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ventCalendar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 521, 30))
        self.menubar.setObjectName("menubar")
        ventCalendar.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ventCalendar)
        self.statusbar.setObjectName("statusbar")
        ventCalendar.setStatusBar(self.statusbar)

        self.retranslateUi(ventCalendar)
        QtCore.QMetaObject.connectSlotsByName(ventCalendar)

    def retranslateUi(self, ventCalendar):
        _translate = QtCore.QCoreApplication.translate
        ventCalendar.setWindowTitle(_translate("ventCalendar", "Fecha Alta"))
        self.lblFechaCalendario.setText(_translate("ventCalendar", "Selecciona la fecha de alta"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventCalendar = QtWidgets.QMainWindow()
    ui = Ui_ventCalendar()
    ui.setupUi(ventCalendar)
    ventCalendar.show()
    sys.exit(app.exec())
