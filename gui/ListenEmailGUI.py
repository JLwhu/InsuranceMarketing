# Form implementation generated from reading ui file 'maingui.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication

from util.backthread import BackThread


class Ui_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(534, 534)
        self.email = QtWidgets.QLineEdit(parent=Dialog)
        self.email.setGeometry(QtCore.QRect(170, 30, 301, 22))
        self.email.setObjectName("lineEdit")
        self.email.setText('info@dadaosolutions.com')
        #self.email.setText('jliudadao@gmail.com')
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(90, 40, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 90, 55, 16))
        self.label_2.setObjectName("label_2")
        self.password = QtWidgets.QLineEdit(parent=Dialog)
        self.password.setGeometry(QtCore.QRect(170, 80, 301, 22))
        self.password.setObjectName("lineEdit_2")
        self.password.setText('Leon030303!')
        #self.password.setText('tpww hafr dycf xxqh')
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setGeometry(QtCore.QRect(80, 130, 81, 16))
        self.label_3.setObjectName("label_3")
        self.IMAP_server = QtWidgets.QLineEdit(parent=Dialog)
        self.IMAP_server.setGeometry(QtCore.QRect(170, 130, 301, 22))
        self.IMAP_server.setObjectName("lineEdit_3")
        self.IMAP_server.setText('secure320.inmotionhosting.com') #imap.gmail.com
        #self.IMAP_server.setText('imap.gmail.com') #
        self.label_smpt = QtWidgets.QLabel(parent=Dialog)
        self.label_smpt.setGeometry(QtCore.QRect(80, 170, 81, 16))
        self.label_smpt.setObjectName("label_smpt")
        self.SMTP_server = QtWidgets.QLineEdit(parent=Dialog)
        self.SMTP_server.setGeometry(QtCore.QRect(170, 170, 301, 22))
        self.SMTP_server.setObjectName("lineEdit_smpt")
        self.SMTP_server.setText('secure320.inmotionhosting.com') #imap.gmail.com
        #self.SMTP_server.setText('imap.gmail.com') #
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setGeometry(QtCore.QRect(80, 210, 81, 16))
        self.label_4.setObjectName("label_4")
        self.keyword = QtWidgets.QLineEdit(parent=Dialog)
        self.keyword.setGeometry(QtCore.QRect(170, 210, 301, 22))
        self.keyword.setObjectName("lineEdit_4")
        self.keyword.setText('New Prospect Quote Notification')
        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 480, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.clicked.connect(self.start_auditing)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 480, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.end_auditing)
        self.textBrowser = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(70, 260, 411, 211))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "邮箱："))
        self.label_2.setText(_translate("Dialog", "密码："))
        self.label_3.setText(_translate("Dialog", "IMAP服务器："))
        self.label_smpt.setText(_translate("Dialog", "SMTP服务器："))
        self.label_4.setText(_translate("Dialog", "关键字："))
        self.pushButton.setText(_translate("Dialog", "开始监控"))
        self.pushButton_2.setText(_translate("Dialog", "停止监控"))

    def start_auditing(self):

        imap_ssl_host = self.IMAP_server.text()#'imap.gmail.com'
        smtp_host = self.SMTP_server.text()#'imap.gmail.com'
        imap_ssl_port = 993
        username = self.email.text()#'jliudadao@gmail.com'
        password = self.password.text() #'tpww hafr dycf xxqh'
        subject_string = self.keyword.text() #'New Prospect Quote Notification'

        print('Starting function')
        self.bt = BackThread(imap_ssl_host, smtp_host, username, password, subject_string)
        self.bt.start()
        self.textBrowser.appendPlainText("Start Listening.....................")
        self.bt.return_progress.connect(self.onProgChanged)

        #p = multiprocessing.Process(target=readNewEmail_IMAP, args=(imap_ssl_host, username, password, subject_string,))
        #self.process = p

        # #print('Process before execution:', p, p.is_alive())
        #p.start()
        #print('Process running:', p, p.is_alive())

        #readNewEmail_IMAP(imap_ssl_host, username, password, subject_string)


    def end_auditing(self):
        print("end")
        self.bt.raise_exception()
        self.textBrowser.appendPlainText("Stop Listening.....................")
        #self.bt.join()

        # p = self.process
        # p.terminate()
        # print('Process terminated:', p, p.is_alive())
        #p.join()
        #print('Process joined:', p, p.is_alive())
        #print('Process exit code:', p.exitcode)

    def onProgChanged(self, value):
        print("result from:")
        self.textBrowser.appendPlainText(value)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = Ui_Dialog()
    gallery.show()
    sys.exit(app.exec())