# windows/edit_window.py

from PyQt5 import QtWidgets, QtCore
from utils.data_handler import update_application
from utils.constants import CSV_HEADERS  # Import CSV_HEADERS

class EditWindow(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal()

    def __init__(self, application_data):
        super().__init__()
        self.setWindowTitle('Modifier une candidature')
        self.setGeometry(300, 300, 500, 500)  # Augmenter la hauteur pour les nouveaux champs
        self.application_data = application_data
        self.initUI()

    def initUI(self):
        # Création des widgets avec les données pré-remplies
        self.companyInput = QtWidgets.QLineEdit(self.application_data[0])
        self.titleInput = QtWidgets.QLineEdit(self.application_data[1])
        self.dateInput = QtWidgets.QDateEdit(QtCore.QDate.fromString(self.application_data[2], 'dd/MM/yyyy'))
        self.dateInput.setDisplayFormat('dd/MM/yyyy')
        self.statusInput = QtWidgets.QComboBox()
        self.statusInput.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.statusInput.setCurrentText(self.application_data[3])
        self.detailsInput = QtWidgets.QTextEdit(self.application_data[4])
        self.channelInput = QtWidgets.QLineEdit(self.application_data[5])

        # Champs pour les informations de contact
        self.contactNameInput = QtWidgets.QLineEdit(self.application_data[6])
        self.contactEmailInput = QtWidgets.QLineEdit(self.application_data[7])
        self.contactPhoneInput = QtWidgets.QLineEdit(self.application_data[8])

        self.saveButton = QtWidgets.QPushButton('Enregistrer les modifications')
        self.saveButton.setFixedHeight(40)
        self.saveButton.clicked.connect(self.saveChanges)

        # Disposition des widgets
        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow('Nom de l\'entreprise:', self.companyInput)
        formLayout.addRow('Intitulé du stage:', self.titleInput)
        formLayout.addRow('Date de candidature:', self.dateInput)
        formLayout.addRow('Statut de la candidature:', self.statusInput)
        formLayout.addRow('Détails supplémentaires:', self.detailsInput)
        formLayout.addRow('Canal de candidature:', self.channelInput)
        formLayout.addRow('Nom du contact:', self.contactNameInput)
        formLayout.addRow('Email du contact:', self.contactEmailInput)
        formLayout.addRow('Téléphone du contact:', self.contactPhoneInput)
        formLayout.addRow(self.saveButton)

        self.setLayout(formLayout)

    def saveChanges(self):
        # Récupération des données modifiées
        company = self.companyInput.text().strip()
        title = self.titleInput.text().strip()
        date = self.dateInput.text()
        status = self.statusInput.currentText()
        details = self.detailsInput.toPlainText().strip()
        channel = self.channelInput.text().strip()
        contact_name = self.contactNameInput.text().strip()
        contact_email = self.contactEmailInput.text().strip()
        contact_phone = self.contactPhoneInput.text().strip()

        if company and title and date and status and channel:
            # Créer la liste des données dans l'ordre des en-têtes
            new_data = [
                company,
                title,
                date,
                status,
                details,
                channel,
                contact_name,
                contact_email,
                contact_phone
            ]
            try:
                updated = update_application(self.application_data, new_data)
                if updated:
                    QtWidgets.QMessageBox.information(self, 'Succès', 'Candidature mise à jour avec succès.')
                    self.update_signal.emit()
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, 'Erreur', 'Erreur lors de la mise à jour.')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors de la mise à jour : {e}')
        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')
