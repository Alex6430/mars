import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, \
    QLineEdit, QFileDialog, QGroupBox, QRadioButton, QTextEdit, \
    QStatusBar, QLabel, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from main import *


class help(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("help")
        self.resize(600, 500)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.textEdit.setText("Программа предназначена для шифрования и расшифровки документов.\n"
                              " Можно шифровать только документы с раширением txt.\n"
                              "Сначала необходимо выбрать размер открытого текста и размер ключа.\n"
                              " Также необходимо выбрать режим сцепления блоков шифротектса и неприводимые\n "
                              "полиномы для умножения в полях Галуа.\n "
                              "При нажатии на кнопку продолжить, нужно ввести ключ, вектор инициализации (IV)\n "
                              "(вектор инициализации используется в режимах спецпления блоков шифротекста CBC, OFB, CFB)\n "
                              " и выбать файл. Дальше выбрать, что нужно сделать с файлом - зашифровать или расшифровать.\n"
                              "Размер вектора инициализации должен совпадать с размером текста. \n")


class about(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("about")
        self.resize(400, 200)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.textEdit.setText("Студент Таранов Алексей\n"
                              "группа М8О-113М-19")


class file(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Rijndael")
        self.resize(600, 500)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(50, 50, 281, 87))
        self.textEdit.setObjectName("textEdit")
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 30, 181, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Введите ключ")

        if (flagBlok == True):
            self.IVEdit = QTextEdit(self)
            self.IVEdit.setGeometry(QtCore.QRect(50, 250, 281, 87))
            self.IVEdit.setObjectName("IVEdit")
            self.label_4 = QLabel(self)
            self.label_4.setGeometry(QtCore.QRect(50, 230, 181, 16))
            self.label_4.setObjectName("label_4")
            self.label_4.setText("Введите IV")

        self.encript_btn = QPushButton(self)
        self.encript_btn.setGeometry(QtCore.QRect(100, 400, 112, 34))
        self.encript_btn.setObjectName("encript_btn")
        ########### button event
        self.encript_btn.clicked.connect(self.show_encript)
        ############
        self.encript_btn.setText("Зашифровать")

        self.decript_btn = QPushButton(self)
        self.decript_btn.setGeometry(QtCore.QRect(300, 400, 122, 34))
        self.decript_btn.setObjectName("decript_btn")
        ########### button event
        self.decript_btn.clicked.connect(self.show_dicript)
        ############
        self.decript_btn.setText("Расшифровать")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(200, 150, 181, 50))
        self.lineEdit.setObjectName("lineEdit")

        self.file_btn = QPushButton(self)
        self.file_btn.setGeometry(QtCore.QRect(50, 150, 112, 34))
        self.file_btn.setObjectName("file_btn")
        ########### button event
        self.file_btn.clicked.connect(self.openFileNameDialog)
        ############
        self.file_btn.setText("выбрать файл")

        self.lineEdit.setText(fil)

    def show_encript(self):
        if (flagBlok == False):
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            print(text)
            print(filename)
            if ((self.textEdit.toPlainText().replace(" ", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == "")
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == " ")):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                if (key):
                    if (len(self.textEdit.toPlainText()) == key // 8):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        mars_encrypt(filename, blok, text, "")
                        self.showMessageBox("готово", "зашифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть" + str(key // 8) + "байт")
        else:
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            IVtext = self.IVEdit.toPlainText()
            print(text)
            print(filename)
            print(IVtext)
            if (self.textEdit.toPlainText().replace(" ", "") == ""
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or self.lineEdit.text().replace(" ", "") == ""
                    or self.IVEdit.toPlainText().replace("\n", "") == ""
                    or self.IVEdit.toPlainText().replace(" ", "") == ""):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                print(state)
                print(blok)
                print(key)
                if (key):
                    print("зашел в кей")
                    print(len(self.textEdit.toPlainText()))
                    if (len(self.textEdit.toPlainText()) == key//8):
                        print("зашел в кей =="+str(key // 8))
                        if (state):
                            if (len(self.IVEdit.toPlainText()) == state//8):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                # initialization(state, key, mod)
                                mars_encrypt(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть"+ str(state // 8) +"байт")
                    else:
                        print("else")
                        self.showMessageBox("ошибка", "размер ключа должен быть"+ str(key //8) +"байт")
                else:
                    text = self.textEdit.toPlainText()
                    filename = self.lineEdit.text()
                    IVtext = self.IVEdit.toPlainText()
                    print(text)
                    print(filename)
                    print(IVtext)

    def show_dicript(self):
        if (flagBlok == False):
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            print(text)
            print(filename)
            if ((self.textEdit.toPlainText().replace(" ", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == "")
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == " ")):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                if (key):
                    if (len(self.textEdit.toPlainText()) == key//8):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        # initialization(state, key, mod)
                        mars_decrypt(filename, blok, text, "")
                        self.showMessageBox("готово", "расшифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть " + str(key // 8) + "байт")
        else:
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            IVtext = self.IVEdit.toPlainText()
            print(text)
            print(filename)
            print(IVtext)
            if (self.textEdit.toPlainText().replace(" ", "") == ""
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or self.lineEdit.text().replace(" ", "") == ""
                    or self.IVEdit.toPlainText().replace("\n", "") == ""
                    or self.IVEdit.toPlainText().replace(" ", "") == ""):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                print(state)
                print(blok)
                print(key)
                if (key):
                    print("зашел в кей")
                    print(len(self.textEdit.toPlainText()))
                    if (len(self.textEdit.toPlainText()) == key//8):
                        print("зашел в кей == 16")
                        if (state):
                            if (len(self.IVEdit.toPlainText()) == state//8):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                # initialization(state, key, mod)
                                mars_decrypt(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть"+ str(state // 8) +"байт")
                    else:
                        print("else")
                        self.showMessageBox("ошибка", "размер ключа должен быть"+ str(key // 8) +"байт")
                else:
                    text = self.textEdit.toPlainText()
                    filename = self.lineEdit.text()
                    IVtext = self.IVEdit.toPlainText()
                    print(text)
                    print(filename)
                    print(IVtext)

    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        # msgBox.setIcon(QtWidgets.QMessageBox.warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

    def initUI(self):
        # self.setWindowTitle(self.title)

        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt);;Python Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            self.lineEdit.setText(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


class App(QWidget):
    def __init__(self):
        super().__init__()
        global fil
        fil = ""
        self.setObjectName("Mars")
        self.resize(800, 500)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.size_state = QGroupBox(self.centralwidget)
        self.size_state.setGeometry(QtCore.QRect(200, 30, 121, 121))
        self.size_state.setObjectName("size_state")
        self.state128 = QRadioButton(self.size_state)
        self.state128.setGeometry(QtCore.QRect(20, 30, 95, 20))
        self.state128.setObjectName("state128")

        self.blok = QGroupBox(self.centralwidget)
        self.blok.setGeometry(QtCore.QRect(200, 200, 150, 150))
        self.blok.setObjectName("blok")
        self.blok_ECB = QRadioButton(self.blok)
        self.blok_ECB.setGeometry(QtCore.QRect(20, 30, 95, 20))
        self.blok_ECB.setObjectName("blok_ECB")
        self.blok_CBC = QRadioButton(self.blok)
        self.blok_CBC.setGeometry(QtCore.QRect(20, 60, 95, 20))
        self.blok_CBC.setObjectName("blok_CBC")
        self.blok_CFB = QRadioButton(self.blok)
        self.blok_CFB.setGeometry(QtCore.QRect(20, 90, 95, 20))
        self.blok_CFB.setObjectName("blok_CFB")
        self.blok_OFB = QRadioButton(self.blok)
        self.blok_OFB.setGeometry(QtCore.QRect(20, 120, 95, 20))
        self.blok_OFB.setObjectName("blok_OFB")

        self.size_key = QGroupBox(self.centralwidget)
        self.size_key.setGeometry(QtCore.QRect(550, 0, 130, 530))
        self.size_key.setObjectName("size_key")
        self.verticalLayout = QVBoxLayout(self.size_key)
        self.verticalLayout.setObjectName("verticalLayout")
        self.key128 = QRadioButton(self.size_key)
        self.key128.setObjectName("key128")
        self.verticalLayout.addWidget(self.key128)
        self.key160 = QRadioButton(self)
        self.key160.setObjectName("key160")
        self.verticalLayout.addWidget(self.key160)
        self.key192 = QRadioButton(self)
        self.key192.setObjectName("key192")
        self.verticalLayout.addWidget(self.key192)
        self.key224 = QRadioButton(self)
        self.key224.setObjectName("key192")
        self.verticalLayout.addWidget(self.key224)
        self.key256 = QRadioButton(self)
        self.key256.setObjectName("key256")
        self.verticalLayout.addWidget(self.key256)
        self.key288 = QRadioButton(self)
        self.key288.setObjectName("key288")
        self.verticalLayout.addWidget(self.key288)
        self.key320 = QRadioButton(self)
        self.key320.setObjectName("key320")
        self.verticalLayout.addWidget(self.key320)
        self.key352 = QRadioButton(self)
        self.key352.setObjectName("key352")
        self.verticalLayout.addWidget(self.key352)
        self.key384 = QRadioButton(self)
        self.key384.setObjectName("key384")
        self.verticalLayout.addWidget(self.key384)
        self.key416 = QRadioButton(self)
        self.key416.setObjectName("key416")
        self.verticalLayout.addWidget(self.key416)
        self.key448 = QRadioButton(self)
        self.key448.setObjectName("key448")
        self.verticalLayout.addWidget(self.key448)

        self.helpBox = QComboBox(self)
        self.helpBox.addItems(["help", "about"])
        self.helpBox.activated.connect(self.selectionchangehelp)
        self.helpBox.setGeometry(QtCore.QRect(700, 0, 100, 25))
        self.helpBox.setObjectName("helpBox")

        # self.comboBox.setGeometry(QtCore.QRect(500, 200, 300, 25))
        # self.comboBox.setObjectName("comboBox")

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 30, 100, 16))
        self.label.setObjectName("label")
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(390, 30, 100, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 200, 100, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(390, 200, 100, 16))
        self.label_4.setObjectName("label_4")
        self.press_btn = QPushButton(self)
        self.press_btn.setGeometry(QtCore.QRect(300, 400, 112, 34))
        self.press_btn.setObjectName("press_btn")
        ########### button event
        self.press_btn.clicked.connect(self.show_file)
        ############

        # self.setCentralWidget(self)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self)

        self.size_state.setTitle("size state")
        self.state128.setText("128 bits")
        self.blok.setTitle("blok")
        self.blok_CBC.setText("blok_CBC")
        self.blok_CFB.setText("blok_CFB")
        self.blok_ECB.setText("blok_ECB")
        self.blok_OFB.setText("blok_OFB")
        self.size_key.setTitle("size key")
        self.key128.setText("128 bits")
        self.key160.setText("160 bits")
        self.key192.setText("192 bits")
        self.key224.setText("224 bits")
        self.key256.setText("256 bits")
        self.key288.setText("288 bits")
        self.key320.setText("320 bits")
        self.key352.setText("352 bits")
        self.key384.setText("384 bits")
        self.key416.setText("416 bits")
        self.key448.setText("448 bits")
        self.label.setText("Размер текста")
        self.label_2.setText("Размер ключа")
        self.label_3.setText("Режим блока")

        self.press_btn.setText("продолжить")
        # self.initUI()

        self.show()

    def selectionchangehelp(self, i):
        if i == 0:
            self.h = help()
            self.h.show()
        if i == 1:
            self.a = about()
            self.a.show()

    def show_file(self):
        global state, blok, key, flagBlok
        if (self.blok_ECB.isChecked() == True):
            flagBlok = False
        else:
            flagBlok = True

        if (self.state128.isChecked() == False):
            self.showMessageBox("ошибка", "выберите размер текста")
        elif (self.key128.isChecked() == False) and (self.key160.isChecked() == False) and (
                self.key192.isChecked() == False) and (self.key224.isChecked() == False) and (
                self.key256.isChecked() == False) \
                and (self.key288.isChecked() == False) and (self.key320.isChecked() == False) and (
                self.key352.isChecked() == False) \
                and (self.key384.isChecked() == False) and (self.key416.isChecked() == False) and (
                self.key448.isChecked() == False):
            self.showMessageBox("ошибка", "выберите размер ключа")
        elif (self.blok_OFB.isChecked() == False) and (self.blok_ECB.isChecked() == False) and \
                (self.blok_CFB.isChecked() == False) and (self.blok_CBC.isChecked() == False):
            self.showMessageBox("ошибка", "выберите режим шифрования")
        else:
            if (self.state128.isChecked() == True):
                state = 128
            if (self.key128.isChecked() == True):
                key = 128
            if (self.key160.isChecked() == True):
                key = 160
            if (self.key192.isChecked() == True):
                key = 192
            if (self.key224.isChecked() == True):
                key = 224
            if (self.key256.isChecked() == True):
                key = 256
            if (self.key288.isChecked() == True):
                key = 288
            if (self.key320.isChecked() == True):
                key = 320
            if (self.key352.isChecked() == True):
                key = 352
            if (self.key384.isChecked() == True):
                key = 384
            if (self.key416.isChecked() == True):
                key = 416
            if (self.key448.isChecked() == True):
                key = 448
            if (self.blok_OFB.isChecked() == True):
                blok = 3
            if (self.blok_ECB.isChecked() == True):
                blok = 1
            if (self.blok_CFB.isChecked() == True):
                blok = 4
            if (self.blok_CBC.isChecked() == True):
                blok = 2

            # mod = 0
            print(state)
            print(blok)
            print(key)
            self.w1 = file()
            self.w1.show()

        # self.close()

    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        # msgBox.setIcon(QtWidgets.QMessageBox.warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
