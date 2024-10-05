import sys
import csv
from PyQt5 import QtWidgets, QtCore, QtGui

CSV_FILE = 'candidatures.csv'
CSV_SEPARATOR = ';'
CSV_ENCODING = 'utf-8'


class InternshipMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('InternshipMonitor')
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        # Création du label pour le logo
        logo_label = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap('./img/logo.png')
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
            try:
                with open(CSV_FILE, 'a', newline='', encoding=CSV_ENCODING) as file:
                    writer = csv.writer(file, delimiter=CSV_SEPARATOR)
                    writer.writerow([company, title, date, status, details, channel])
                QtWidgets.QMessageBox.information(self, 'Succès', 'Candidature ajoutée avec succès.')
                self.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'ajout de la candidature : {e}')
        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')


class ViewWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Afficher les candidatures')
        self.setGeometry(200, 200, 900, 600)
        self.initUI()

    def initUI(self):
        # Création du filtre par statut
        self.statusFilter = QtWidgets.QComboBox()
        self.statusFilter.addItem('Tous les statuts')
        self.statusFilter.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.statusFilter.currentIndexChanged.connect(self.loadData)

        # Création du tableau
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)  # Ajout d'une colonne pour le bouton "Modifier"
        self.table.setHorizontalHeaderLabels(
            ['Entreprise', 'Intitulé', 'Date', 'Statut', 'Détails', 'Canal', 'Modifier'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.setWordWrap(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Empêche l'édition directe
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Ajustement de la hauteur des lignes automatiquement
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.horizontalHeader().setMinimumSectionSize(100)

        # Disposition des widgets
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
                            item = QtWidgets.QTableWidgetItem(data)
                            item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                            self.table.setItem(row, column, item)
                        # Ajouter le bouton "Modifier"
                        edit_button = QtWidgets.QPushButton('Modifier')
                        edit_button.clicked.connect(self.getEditFunction(row_data))
                        self.table.setCellWidget(row, 6, edit_button)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Aucune candidature trouvée.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors de la lecture du fichier CSV : {e}')

    def getEditFunction(self, row_data):
        def editApplication():
            self.editWindow = EditWindow(row_data)
            self.editWindow.update_signal.connect(self.loadData)
            self.editWindow.show()

        return editApplication


class EditWindow(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal()

    def __init__(self, application_data):
        super().__init__()
        self.setWindowTitle('Modifier une candidature')
        self.setGeometry(300, 300, 500, 400)
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

        if company and title and date and status and channel:
            try:
                # Chargement de toutes les candidatures
                with open(CSV_FILE, 'r', encoding=CSV_ENCODING) as file:
                    reader = csv.reader(file, delimiter=CSV_SEPARATOR)
                    applications = list(reader)

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
                    self.update_signal.emit()
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, 'Erreur', 'Erreur lors de la mise à jour.')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors de la mise à jour : {e}')
        else:
            QtWidgets.QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs obligatoires.')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InternshipMonitor()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
