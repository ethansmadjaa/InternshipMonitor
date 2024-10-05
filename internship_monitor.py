import sys
import csv
from PyQt5 import QtWidgets, QtCore

CSV_FILE = 'candidatures.csv'
CSV_SEPARATOR = ';'
CSV_ENCODING = 'utf-8'


class InternshipMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('InternshipMonitor')
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        # Création des boutons
        self.addButton = QtWidgets.QPushButton('Ajouter une candidature')
        self.viewButton = QtWidgets.QPushButton('Afficher les candidatures')
        self.updateButton = QtWidgets.QPushButton('Mettre à jour une candidature')

        # Disposition des boutons
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.viewButton)
        layout.addWidget(self.updateButton)

        # Configuration du widget central
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Connexion des signaux aux slots
        self.addButton.clicked.connect(self.showAddWindow)
        self.viewButton.clicked.connect(self.showViewWindow)
        self.updateButton.clicked.connect(self.showUpdateWindow)

    def showAddWindow(self):
        self.addWindow = AddWindow()
        self.addWindow.show()

    def showViewWindow(self):
        self.viewWindow = ViewWindow()
        self.viewWindow.show()

    def showUpdateWindow(self):
        self.updateWindow = UpdateWindow()
        self.updateWindow.show()


class AddWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ajouter une candidature')
        self.setGeometry(150, 150, 400, 300)
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
        company = self.companyInput.text()
        title = self.titleInput.text()
        date = self.dateInput.text()
        status = self.statusInput.currentText()
        details = self.detailsInput.toPlainText()
        channel = self.channelInput.text()

        if company and title and date and status and channel:
            # Écriture dans le fichier CSV
            with open(CSV_FILE, 'a', newline='', encoding=CSV_ENCODING) as file:
                writer = csv.writer(file, delimiter=CSV_SEPARATOR)
                writer.writerow([company, title, date, status, details, channel])
            QtWidgets.QMessageBox.information(self, 'Succès', 'Candidature ajoutée avec succès.')
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')


class ViewWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Afficher les candidatures')
        self.setGeometry(200, 200, 800, 400)
        self.initUI()

    def initUI(self):
        self.statusFilter = QtWidgets.QComboBox()
        self.statusFilter.addItem('Tous les statuts')
        self.statusFilter.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.statusFilter.currentIndexChanged.connect(self.loadData)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)  # Ajout d'une colonne pour le bouton "Modifier"
        self.table.setHorizontalHeaderLabels(
            ['Entreprise', 'Intitulé', 'Date', 'Statut', 'Détails', 'Canal', 'Modifier'])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.statusFilter)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.loadData()

    def loadData(self):
        status = self.statusFilter.currentText()
        self.table.setRowCount(0)

        try:
            with open(CSV_FILE, 'r', encoding=CSV_ENCODING) as file:
                reader = csv.reader(file, delimiter=CSV_SEPARATOR)
                for row_data in reader:
                    if status == 'Tous les statuts' or row_data[3] == status:
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        for column, data in enumerate(row_data):
                            self.table.setItem(row, column, QtWidgets.QTableWidgetItem(data))
                        # Ajouter le bouton "Modifier"
                        edit_button = QtWidgets.QPushButton('Modifier')
                        edit_button.clicked.connect(self.getEditFunction(row_data))
                        self.table.setCellWidget(row, 6, edit_button)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Aucune candidature trouvée.')

    def getEditFunction(self, row_data):
        def editApplication():
            self.editWindow = EditWindow(row_data)
            self.editWindow.show()

        return editApplication


class UpdateWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mettre à jour une candidature')
        self.setGeometry(250, 250, 400, 200)
        self.initUI()

    def initUI(self):
        self.companyInput = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton('Rechercher')
        self.searchButton.clicked.connect(self.searchApplication)

        self.statusInput = QtWidgets.QComboBox()
        self.statusInput.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.updateButton = QtWidgets.QPushButton('Mettre à jour')
        self.updateButton.clicked.connect(self.updateApplication)
        self.updateButton.setEnabled(False)

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow('Nom de l\'entreprise:', self.companyInput)
        formLayout.addRow(self.searchButton)
        formLayout.addRow('Nouveau statut:', self.statusInput)
        formLayout.addRow(self.updateButton)

        self.setLayout(formLayout)

    def searchApplication(self):
        self.companyName = self.companyInput.text()
        self.applications = []
        self.found = False

        try:
            with open(CSV_FILE, 'r', encoding=CSV_ENCODING) as file:
                reader = csv.reader(file, delimiter=CSV_SEPARATOR)
                for row in reader:
                    self.applications.append(row)
                    if row[0].lower() == self.companyName.lower():
                        self.found = True
            if self.found:
                QtWidgets.QMessageBox.information(self, 'Succès', 'Candidature trouvée.')
                self.updateButton.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self, 'Erreur', 'Candidature non trouvée.')
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Aucune candidature trouvée.')

    def updateApplication(self):
        newStatus = self.statusInput.currentText()
        updated = False

        for i, row in enumerate(self.applications):
            if row[0].lower() == self.companyName.lower():
                self.applications[i][3] = newStatus
                updated = True

        if updated:
            with open(CSV_FILE, 'w', newline='', encoding=CSV_ENCODING) as file:
                writer = csv.writer(file, delimiter=CSV_SEPARATOR)
                writer.writerows(self.applications)
            QtWidgets.QMessageBox.information(self, 'Succès', 'Statut mis à jour avec succès.')
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Erreur lors de la mise à jour.')


class EditWindow(QtWidgets.QWidget):
    def __init__(self, application_data):
        super().__init__()
        self.setWindowTitle('Modifier une candidature')
        self.setGeometry(300, 300, 400, 300)
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

        self.saveButton = QtWidgets.QPushButton('Enregistrer les modifications')
        self.saveButton.clicked.connect(self.saveChanges)

        # Disposition des widgets
        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow('Nom de l\'entreprise:', self.companyInput)
        formLayout.addRow('Intitulé du stage:', self.titleInput)
        formLayout.addRow('Date de candidature:', self.dateInput)
        formLayout.addRow('Statut de la candidature:', self.statusInput)
        formLayout.addRow('Détails supplémentaires:', self.detailsInput)
        formLayout.addRow('Canal de candidature:', self.channelInput)
        formLayout.addRow(self.saveButton)

        self.setLayout(formLayout)

    def saveChanges(self):
        # Récupération des données modifiées
        company = self.companyInput.text()
        title = self.titleInput.text()
        date = self.dateInput.text()
        status = self.statusInput.currentText()
        details = self.detailsInput.toPlainText()
        channel = self.channelInput.text()

        # Chargement de toutes les candidatures
        applications = []
        try:
            with open(CSV_FILE, 'r', encoding=CSV_ENCODING) as file:
                reader = csv.reader(file, delimiter=CSV_SEPARATOR)
                applications = list(reader)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Aucune candidature trouvée.')
            return

        # Mise à jour de la candidature spécifique
        updated = False
        for i, row in enumerate(applications):
            if row == self.application_data:
                applications[i] = [company, title, date, status, details, channel]
                updated = True
                break

        if updated:
            # Écriture des candidatures mises à jour dans le fichier CSV
            with open(CSV_FILE, 'w', newline='', encoding=CSV_ENCODING) as file:
                writer = csv.writer(file, delimiter=CSV_SEPARATOR)
                writer.writerows(applications)
            QtWidgets.QMessageBox.information(self, 'Succès', 'Candidature mise à jour avec succès.')
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Erreur lors de la mise à jour.')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InternshipMonitor()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
