import sys
import os
import subprocess
import PIL
import zbarlight
import configurator
from PySide import QtGui
from PySide.QtGui import QWidget, QApplication, QMainWindow, QStatusBar, QTextEdit, \
    QAction, QIcon, QKeySequence, QMessageBox, QFormLayout, QLabel, QLineEdit,\
    QGridLayout, QPushButton, QDesktopWidget, QFileDialog, QVBoxLayout


class ShowCertWindow(QMainWindow):

    def __init__(self, certText,parent=None):
        try:
            super(ShowCertWindow, self).__init__(parent=parent)
            qWidget = QWidget()
            layout = QVBoxLayout(qWidget)
            textEdit = QTextEdit()
            textEdit.setReadOnly(True)
            textEdit.setPlainText(certText)
            layout.addWidget(textEdit)
            button = QPushButton("OK")
            button.clicked.connect(self.destroy)
            layout.addWidget(button)
            self.setGeometry(300, 300, 500, 300)
            self.setWindowTitle("CA Certificate")
            self.setCentralWidget(qWidget)
            self.show()
        except e:
            print(e)


class MainWindow(QMainWindow):
    """ Our Main Window class
    """

    def __init__(self):
        """ Constructor Function
        """
        super(MainWindow, self).__init__()
        self.initGUI()

    def initGUI(self):
        self.setWindowTitle("Configurator")
        appIcon = QIcon('logo.png')
        self.setWindowIcon(appIcon)
        self.setGeometry(300, 250, 400, 300)
        self.SetLayout()
        self.center()
        self.show()

    def center(self):
        """ Function to center the application
        """
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        # First move the rectangle
        qRect.moveCenter(centerPoint)
        # move my window to the moved rectangle.
        self.move(qRect.topLeft())

    def doQuit(self):
        print("doQuit")
        sys.exit()
        os.exit()

    def doOnboard(self):
        print("doOnboard")
        if self.caCertPath.text() == "" or \
                self.dppUri.text() == "" or \
                self.ssId.text() == "" or \
                self.password.text() == "":
            QMessageBox.information(self, "Information needed", "Please supply all needed information",
                                    QMessageBox.Ok)
        else:
            print("onBoarding")
            configurator.onboard(self.ssId.text(),self.password.text(), self.caCertPath.text(), self.dppUri.text())

    def doViewCertificate(self):
        print("doViewCertificate")
        if self.caCertPath.text() == "":
            QMessageBox.information(self, "CA Cert Path Missing", "Please enter CA Cert Path",
                                    QMessageBox.Ok)
        else:
            caCertPath = self.caCertPath.text()
            cmd = ["openssl", "x509", "-text", "-noout", "-in", caCertPath]
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if stderr != "":
                print(stderr)
                QMessageBox.information(
                    self, "Error decoding certificate", stderr.decode('utf-8'), QMessageBox.Ok)
            else:
                ShowCertWindow(stdout,self)

    def doReadQrCode(self):
        # TODO -- camera scan here
        f = open("/home/pi/dpp-devid/test/qr-codes/dpp-qr-code.png",'rb')
        qr = PIL.Image.open(f)
        qr.load()
        codes = zbarlight.scan_codes('qrcode',qr)
        print(codes[0])
        self.dppUri.setText(codes[0])

    def doScanQrCode(self):
        print 'Taking picture..'
        while True :
            self.camera.start_preview()
            time.sleep(1)
            self.camera.capture("qr-code.jpg")
            self.camera.stop_preview()

            #f = open("../../test/qr-codes/dpp-qr-code.png",'rb')
            f = open("qr-code.jpg",'rb')
            qr = PIL.Image.open(f)
            qr.load()
            codes = zbarlight.scan_codes('qrcode',qr)
            if codes is not None:
                break
        print(codes[0])
        self.dppUri.setText(codes[0])


    def doSelectCaCertPath(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            './', "PEM files (*.pem)")
        self.caCertPath.setText(fname[0])

    def SetLayout(self):
        qWidget = QWidget()
        gridLayout = QGridLayout(qWidget)
        row = 0
        self.setCentralWidget(qWidget)

        row += 1
        ssidLabel = QLabel("SSID: ")
        self.ssId = QLineEdit()
        gridLayout.addWidget(ssidLabel, row, 0)
        gridLayout.addWidget(self.ssId, row, 1)

        row += 1
        passwordLabel = QLabel("Password: ")
        self.password = QLineEdit()
        gridLayout.addWidget(passwordLabel, row, 0)
        gridLayout.addWidget(self.password, row, 1)

        row += 1
        dppUriLabel = QLabel("DPP URI: ")
        self.dppUri = QLineEdit()
        scanPushButton = QPushButton("Scan QR Code", self)
        scanPushButton.clicked.connect(self.doScanQrCode)
        gridLayout.addWidget(dppUriLabel, row, 0)
        gridLayout.addWidget(self.dppUri, row, 1)
        gridLayout.addWidget(scanPushButton, row, 2)

        row += 1
        caCertLabel = QLabel("CA Cert")
        self.caCertPath = QLineEdit()
        certPathButton = QPushButton("Select")
        certPathButton.clicked.connect(self.doSelectCaCertPath)
        gridLayout.addWidget(caCertLabel, row, 0)
        gridLayout.addWidget(self.caCertPath, row, 1)
        gridLayout.addWidget(certPathButton, row, 2)

        row += 1
        onboardButton = QPushButton("Onboard", self)
        onboardButton.clicked.connect(self.doOnboard)
        viewCertButton = QPushButton("View CA Certificate", self)
        viewCertButton.clicked.connect(self.doViewCertificate)
        quitButton = QPushButton("Quit")
        quitButton.clicked.connect(self.doQuit)
        gridLayout.addWidget(onboardButton, row, 0)
        gridLayout.addWidget(viewCertButton, row, 1)
        gridLayout.addWidget(quitButton, row, 2)

        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage("Information Needed")


if __name__ == "__main__":
    try:
        # QApplication.setStyle('plastique')
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
