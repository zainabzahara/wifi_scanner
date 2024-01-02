import sys
import hashlib
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QCheckBox
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

class WifiScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.passwords_file = 'passwords.json'
        self.last_connected_network = None
        self.loadPasswords()

    def initUI(self):
        # Set the size of the GUI
        self.resize(220, 300)  # You can adjust the size as needed
        # Set the window title
        self.setWindowTitle('WiFi')
        # Set the window icon
        self.setWindowIcon(QIcon('download (1).png'))
        # Set the background color
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(132, 126, 130))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.wifiToggle = QCheckBox("Enable WiFi", self)
        self.wifiToggle.stateChanged.connect(self.toggleWifi)
        layout.addWidget(self.wifiToggle)

        self.wifiWidget = QWidget(self)
        wifiLayout = QVBoxLayout()

        self.comboBox = QComboBox(self.wifiWidget)
        wifiLayout.addWidget(self.comboBox)

        self.refreshButton = QPushButton('Refresh', self.wifiWidget)
        self.refreshButton.clicked.connect(self.refreshNetworks)
        wifiLayout.addWidget(self.refreshButton)

        self.passwordInput = QLineEdit(self.wifiWidget)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        wifiLayout.addWidget(self.passwordInput)

        self.connectButton = QPushButton('Connect', self.wifiWidget)
        self.connectButton.clicked.connect(self.connectWifi)
        wifiLayout.addWidget(self.connectButton)

        self.wifiWidget.setLayout(wifiLayout)
        layout.addWidget(self.wifiWidget)
        layout.addStretch(1)  # Add a stretchable space at the bottom

        self.setLayout(layout)

    def toggleWifi(self, state):
        if state == Qt.Checked:
            self.wifiWidget.show()
            self.refreshNetworks()
        else:
            self.wifiWidget.hide()
            self.comboBox.clear()

    def refreshNetworks(self):
        self.comboBox.clear()
        networks = self.get_networks()
        for network in networks:
            ssid = network.split(': ')[-1]
            self.comboBox.addItem(ssid)

    def connectWifi(self):
        selectedNetwork = str(self.comboBox.currentText())
        if selectedNetwork in self.passwords:
            stored_password = self.passwords[selectedNetwork]
            self.tryConnecting(selectedNetwork, stored_password)
        else:
            password = self.passwordInput.text()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.tryConnecting(selectedNetwork, hashed_password)
        self.passwordInput.clear()

    def tryConnecting(self, selectedNetwork, hashed_password):
        try:
            result = subprocess.run(['netsh', 'wlan', 'connect', 'name=' + selectedNetwork], check=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.passwords[selectedNetwork] = hashed_password
                self.savePasswords()
                self.last_connected_network = selectedNetwork
            self.showConnectionStatusMessage("Connected", QMessageBox.Information)
        except subprocess.CalledProcessError as e:
            self.showConnectionStatusMessage("Connection failed", QMessageBox.Critical)

    def showConnectionStatusMessage(self, message, icon):
        msg = QMessageBox()
        msg.setStyleSheet("QLabel{min-width: 200px;}")
        msg.setIcon(icon)
        msg.setText(message)
        msg.setWindowTitle("Connection Status")
        msg.exec_()

    def loadPasswords(self):
        try:
            with open(self.passwords_file, 'r') as file:
                self.passwords = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.passwords = {}

    def savePasswords(self):
        with open(self.passwords_file, 'w') as file:
            json.dump(self.passwords, file)

    def get_networks(self):
        networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
        networks = networks.decode('ascii').replace('\r', '').split('\n')
        networks = networks[4:]
        ssids = []
        x = 0
        while x < len(networks):
            if x % 5 == 0:
                ssids.append(networks[x])
            x += 1
        return ssids

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wifiScanner = WifiScanner()
    wifiScanner.show()
    sys.exit(app.exec_())
