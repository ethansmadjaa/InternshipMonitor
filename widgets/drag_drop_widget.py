# widgets/drag_drop_widget.py
import os

from PyQt5 import QtWidgets, QtCore, QtGui
import shutil
from utils.constants import DOCUMENTS_DIR


class DragDropWidget(QtWidgets.QWidget):
    files_dropped = QtCore.pyqtSignal(list)
    ALLOWED_EXTENSIONS = ['.pdf']

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel('Glissez et déposez des fichiers ici\n(Types acceptés : PDF, DOC, DOCX)')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('''
            border: 2px dashed #aaa;
            padding: 20px;
        ''')

        # Liste pour afficher les fichiers
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.addItem('Aucun fichier sélectionné.')

        # Bouton pour supprimer un fichier
        self.removeButton = QtWidgets.QPushButton('Supprimer le fichier sélectionné')
        self.removeButton.clicked.connect(self.removeSelectedFile)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.removeButton)
        self.setLayout(self.layout)

        self.document_paths = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if file_path:
                    # Vérifier l'extension du fichier
                    _, ext = os.path.splitext(file_path)
                    if ext.lower() in self.ALLOWED_EXTENSIONS:
                        # Copier le fichier dans DOCUMENTS_DIR
                        if not os.path.exists(DOCUMENTS_DIR):
                            os.makedirs(DOCUMENTS_DIR)

                        # Éviter les conflits de noms
                        original_file_name = os.path.basename(file_path)
                        base_name, extension = os.path.splitext(original_file_name)
                        dest_file_name = original_file_name
                        counter = 1
                        while os.path.exists(os.path.join(DOCUMENTS_DIR, dest_file_name)):
                            dest_file_name = f"{base_name}_{counter}{extension}"
                            counter += 1

                        dest_path = os.path.join(DOCUMENTS_DIR, dest_file_name)
                        try:
                            shutil.copy(file_path, dest_path)
                            if dest_path not in self.document_paths:
                                self.document_paths.append(dest_path)
                        except Exception as e:
                            QtWidgets.QMessageBox.warning(self, 'Erreur',
                                                          f'Impossible de copier le fichier {original_file_name} : {e}')
                    else:
                        QtWidgets.QMessageBox.warning(self, 'Type de fichier non autorisé',
                                                      f'Le fichier "{os.path.basename(file_path)}" n\'est pas autorisé.')
            self.updateLabel()
            self.files_dropped.emit(self.document_paths)
        else:
            event.ignore()

    def updateLabel(self):
        self.listWidget.clear()
        if self.document_paths:
            for path in self.document_paths:
                self.listWidget.addItem(os.path.basename(path))
        else:
            self.listWidget.addItem('Aucun fichier sélectionné.')

    def getDocumentPaths(self):
        return self.document_paths

    def removeSelectedFile(self):
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, 'Information', 'Veuillez sélectionner un fichier à supprimer.')
            return
        for item in selected_items:
            index = self.listWidget.row(item)
            path_to_remove = self.document_paths.pop(index)
            self.listWidget.takeItem(index)
            # Supprimer physiquement le fichier
            try:
                os.remove(path_to_remove)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, 'Erreur', f'Impossible de supprimer le fichier : {e}')
        if not self.document_paths:
            self.listWidget.addItem('Aucun fichier sélectionné.')
