# windows/view_window.py

from PyQt5 import QtWidgets, QtCore, QtGui
from windows.edit_window import EditWindow
from utils.constants import CSV_HEADERS
from utils.data_handler import read_applications
import os


class ViewWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Afficher les candidatures')
        self.setGeometry(200, 200, 1000, 600)
        self.initUI()

    def initUI(self):
        # Création du filtre par statut
        self.statusFilter = QtWidgets.QComboBox()
        self.statusFilter.addItem('Tous les statuts')
        self.statusFilter.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.statusFilter.currentIndexChanged.connect(self.loadData)

        # Création du tableau
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(CSV_HEADERS) + 2)  # Colonnes + boutons "Modifier" et "Documents"
        # Mettre à jour les en-têtes pour remplacer 'Documents' par 'Noms des documents'
        headers = CSV_HEADERS.copy()
        headers[9] = 'Noms des documents'  # Remplacer 'Documents' par 'Noms des documents'
        self.table.setHorizontalHeaderLabels(headers + ['Modifier', 'Documents'])
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
                # Vérifier que la ligne a au moins 4 colonnes pour accéder à row_data[3]
                if len(row_data) >= 4 and (status == 'Tous les statuts' or row_data[3] == status):
                    # Normaliser la longueur de la ligne
                    if len(row_data) < len(CSV_HEADERS):
                        row_data.extend([''] * (len(CSV_HEADERS) - len(row_data)))

                    row = self.table.rowCount()
                    self.table.insertRow(row)

                    # Afficher seulement les noms des documents au lieu des chemins complets
                    display_row_data = row_data.copy()
                    documents_str = display_row_data[9]
                    if documents_str:
                        document_names = [os.path.basename(path) for path in documents_str.split('|')]
                        display_row_data[9] = ', '.join(document_names)
                    else:
                        display_row_data[9] = 'Aucun document'

                    for column, data in enumerate(display_row_data):
                        item = QtWidgets.QTableWidgetItem(data)
                        item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.table.setItem(row, column, item)
                    # Bouton "Modifier"
                    edit_button = QtWidgets.QPushButton('Modifier')
                    edit_button.clicked.connect(self.getEditFunction(row_data))
                    self.table.setCellWidget(row, len(CSV_HEADERS), edit_button)
                    # Bouton "Documents"
                    documents_button = QtWidgets.QPushButton('Ouvrir Documents')
                    documents_button.clicked.connect(self.getDocumentsFunction(row_data[9]))
                    self.table.setCellWidget(row, len(CSV_HEADERS) + 1, documents_button)
                else:
                    continue
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erreur', f'Erreur lors du chargement des candidatures : {e}')

    def getEditFunction(self, row_data):
        def editApplication():
            self.editWindow = EditWindow(row_data)
            self.editWindow.update_signal.connect(self.loadData)
            self.editWindow.show()

        return editApplication

    def getDocumentsFunction(self, documents_str):
        def openDocuments():
            document_paths = documents_str.split('|') if documents_str else []
            if document_paths:
                for path in document_paths:
                    if not os.path.isabs(path):
                        path = os.path.abspath(path)
                    if os.path.exists(path):
                        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))
                    else:
                        QtWidgets.QMessageBox.warning(self, 'Erreur',
                                                      f'Le fichier {os.path.basename(path)} est introuvable.')
            else:
                QtWidgets.QMessageBox.information(self, 'Information', 'Aucun document associé.')

        return openDocuments
