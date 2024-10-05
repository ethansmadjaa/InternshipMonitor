# windows/add_window.py

from PyQt5 import QtWidgets, QtCore
import csv
from utils.constants import CSV_FILE, CSV_SEPARATOR, CSV_ENCODING
# windows/add_window.py

from utils.data_handler import add_application


class AddWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ajouter une candidature')
        self.setGeometry(150, 150, 500, 400)
        self.initUI()

    def initUI(self):
        # Création des widgets
        self.companyInput = QtWidgets.QLineEdit()
        self.titleInput = QtWidgets.QLineEdit()
        self.dateInput = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.dateInput.setDisplayFormat('dd/MM/yyyy')
        self.statusInput = QtWidgets.QComboBox()
        self.statusInput.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.detailsInput = QtWidgets.QTextEdit()
        self.channelInput = QtWidgets.QLineEdit()

        self.addButton = QtWidgets.QPushButton('Ajouter')
        self.addButton.setFixedHeight(40)
        self.addButton.clicked.connect(self.addApplication)

        # Disposition des widgets
        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow('Nom de l\'entreprise:', self.companyInput)
        formLayout.addRow('Intitulé du stage:', self.titleInput)
        formLayout.addRow('Date de candidature:', self.dateInput)
        formLayout.addRow('Statut de la candidature:', self.statusInput)
        formLayout.addRow('Détails supplémentaires:', self.detailsInput)
        formLayout.addRow('Canal de candidature:', self.channelInput)
        formLayout.addRow(self.addButton)

        self.setLayout(formLayout)

    def addApplication(self):
        # Récupération des données
        company = self.companyInput.text().strip()
        title = self.titleInput.text().strip()
        date = self.dateInput.text()
        status = self.statusInput.currentText()
        details = self.detailsInput.toPlainText().strip()
        channel = self.channelInput.text().strip()

        if company and title and date and status and channel:
            # Écriture dans le fichier CSV
            # Modified code in addApplication method

            try:
                add_application([company, title, date, status, details, channel])
                QtWidgets.QMessageBox.information(self, 'Succès', 'Candidature ajoutée avec succès.')
                self.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'ajout de la candidature : {e}')

        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')
