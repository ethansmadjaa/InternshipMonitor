from PyQt5 import QtWidgets, QtCore, QtGui
from windows.edit_window import EditWindow
from utils.constants import CSV_HEADERS
from utils.data_handler import read_applications
import os


class ViewWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Afficher les candidatures')
        self.setGeometry(200, 200, 1000, 600)  # Augmenter la largeur pour les nouvelles colonnes
        self.initUI()

    def initUI(self):
        # Création du filtre par statut
        self.statusFilter = QtWidgets.QComboBox()
        self.statusFilter.addItem('Tous les statuts')
        self.statusFilter.addItems(['Candidature envoyée', 'Candidature refusée', 'Candidature acceptée'])
        self.statusFilter.currentIndexChanged.connect(self.loadData)

        # Création du tableau
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(CSV_HEADERS) + 2)  # Nombre de colonnes + bouton "Modifier"
        self.table.setHorizontalHeaderLabels(CSV_HEADERS + ['Modifier', 'Documents'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.setWordWrap(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
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
                    # Bouton "Modifier"
                    edit_button = QtWidgets.QPushButton('Modifier')
                    edit_button.clicked.connect(self.getEditFunction(row_data))
                    self.table.setCellWidget(row, len(CSV_HEADERS), edit_button)
                    # Bouton "Documents"
                    documents_button = QtWidgets.QPushButton('Ouvrir Documents')
                    documents_button.setFixedSize(100, 50)
                    documents_button.clicked.connect(self.getDocumentsFunction(row_data[9]))
                    self.table.setCellWidget(row, len(CSV_HEADERS) + 1, documents_button)
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
                        QtWidgets.QMessageBox.warning(self, 'Erreur', f'Le fichier {path} est introuvable.')
            else:
                QtWidgets.QMessageBox.information(self, 'Information', 'Aucun document associé.')

        return openDocuments
