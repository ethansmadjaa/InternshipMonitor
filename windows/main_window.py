# windows/main_window.py

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from windows.add_window import AddWindow
from windows.view_window import ViewWindow
from utils.constants import CSV_FILE

class InternshipMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('InternshipMonitor')
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        # Création du label pour le logo
        logo_label = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap('img/logo.png')
        logo_pixmap = logo_pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)

        # Création du label pour le titre
        title_label = QtWidgets.QLabel('InternshipMonitor')
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont('Arial', 24, QtGui.QFont.Bold))

        # Création des boutons
        self.addButton = QtWidgets.QPushButton('Ajouter une candidature')
        self.viewButton = QtWidgets.QPushButton('Afficher les candidatures')

        # Configuration de la taille des boutons
        self.addButton.setFixedHeight(40)
        self.viewButton.setFixedHeight(40)

        # Disposition des boutons
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.viewButton)
        button_layout.setSpacing(20)  # Espace entre les boutons

        # Ajout des boutons dans un widget
        button_widget = QtWidgets.QWidget()
        button_widget.setLayout(button_layout)

        # Disposition principale
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(logo_label)
        main_layout.addWidget(title_label)
        main_layout.addStretch()  # Espace flexible
        main_layout.addWidget(button_widget)
        main_layout.addStretch()  # Espace flexible

        # Configuration du widget central
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(main_layout)
        self.setCentralWidget(centralWidget)

        # Connexion des signaux aux slots
        self.addButton.clicked.connect(self.showAddWindow)
        self.viewButton.clicked.connect(self.showViewWindow)

    def showAddWindow(self):
        self.addWindow = AddWindow()
        self.addWindow.show()

    def showViewWindow(self):
        self.viewWindow = ViewWindow()
        self.viewWindow.show()
