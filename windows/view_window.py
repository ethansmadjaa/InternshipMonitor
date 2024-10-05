from PyQt5 import QtWidgets, QtCore
import csv
from windows.edit_window import EditWindow
from utils.constants import CSV_FILE, CSV_SEPARATOR, CSV_ENCODING
from utils.data_handler import read_applications


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
            applications = read_applications()
            for row_data in applications:
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
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors du chargement des candidatures : {e}')

    def getEditFunction(self, row_data):
        def editApplication():
            self.editWindow = EditWindow(row_data)
            self.editWindow.update_signal.connect(self.loadData)
            self.editWindow.show()

        return editApplication
