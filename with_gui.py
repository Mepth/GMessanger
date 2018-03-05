import sys, socket, threading, base64, os
try:
    from PyQt5.QtWidgets import *
    from PyQt5 import QtCore, QtWidgets
except:
    print('You do not have the following components installed:\n - PyQT5\nIf you want to set, then enter Y')
    question = input('[Y/n] ')
    if question.lower() == 'y':
        os.system('pip3 install pyqt5')
        print('OK! Restart app')
        sys.exit(0)
    else:
        print('Install modules independently to use the application')
        sys.exit(0)

room_ip, room_port = '127.0.0.1', 48004
debug = True

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(450, 525)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.input = QtWidgets.QLineEdit(self)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.clear = QtWidgets.QPushButton(self.centralWidget)
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)

        self.input.setGeometry(QtCore.QRect(15, 350, 300, 65))
        self.pushButton.setGeometry(QtCore.QRect(325, 337, 115, 67))
        self.clear.setGeometry(QtCore.QRect(15, 415, 425, 75))
        self.textEdit.setGeometry(QtCore.QRect(15, 20, 425, 300))
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 469, 21))

        self.input.setObjectName('InputMessageBox')
        self.pushButton.setObjectName('pushButton')
        self.clear.setObjectName('clearButton')
        self.textEdit.setObjectName('textEdit')
        self.menuBar.setObjectName('menuBar')

        MainWindow.setStyleSheet('background: #4d4d4d;')
        self.pushButton.setStyleSheet('background: #bebebe; border-radius: 10px; font-size: 13pt;')
        self.input.setStyleSheet('background: #bebebe;')
        self.textEdit.setStyleSheet('background: #bebebe;')
        self.clear.setStyleSheet('background: rgb(212,75,56); border-radius: 25px; font-size: 25pt;')

        MainWindow.setCentralWidget(self.centralWidget)
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName('statusBar')
        MainWindow.setStatusBar(self.statusBar)
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate('MainWindow', 'GMessanger - New age Build #666'))
        self.pushButton.setText(QtCore.QCoreApplication.translate('MainWindow', 'Send message'))
        self.clear.setText(QtCore.QCoreApplication.translate('MainWindow', 'Clear history'))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((room_ip, room_port))
            print('You has bees successfulled connected to a chat room, get kaef')
            super().__init__()
            self.setupUi(self)
            threading.Thread(target=self.message_recv).start()
            self.clear.clicked.connect(self.buttonClear)
            self.pushButton.clicked.connect(self.buttonClicked)
            self.pushButton.setAutoDefault(True)
            self.input.returnPressed.connect(self.pushButton.click)
        except:
            print('Sorry, but this room is not working ((')
            sys.exit(0)
            exit(0)

    def buttonClear(self):
        self.textEdit.clear()

    def buttonClicked(self):
        if not self.input.text() == '':
            self.sock.send(self.encode(self.input.text()))
            self.input.setText('')

    def message_recv(self):
        while True:
            try:
                msg = self.sock.recv(4096)
                if msg == b'': break
                if debug: print(self.decode(msg))
                self.textEdit.append(self.decode(msg))
            except:
                print('P2P server has been offed')
                sys.exit(0)
                exit()

    def encode(self, message):
        msg = base64.b64encode(bytes(message, 'utf-8')) + b'()' + base64.b64encode(bytes(message, 'utf-8'))
        msg = msg.decode('utf-8').replace('a', 'а').replace('b', 'б').replace('c', 'с').replace('p', 'р').replace('t', 'т').replace('o', 'о').replace('=', '*')
        msg = msg.encode()
        return msg

    def decode(self, message):
        msg = message.decode('utf-8').split('()')[0].replace('а', 'a').replace('б', 'b').replace('с', 'c').replace('р', 'p').replace('т', 't').replace('о', 'o').replace('*', '=')
        msg1 = base64.b64decode(msg).decode('utf-8')
        return msg1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec()
