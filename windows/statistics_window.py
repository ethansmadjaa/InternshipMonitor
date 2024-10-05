# windows/statistics_window.py

from PyQt5 import QtWidgets, QtCore
from utils.data_handler import read_applications
from utils.constants import CSV_HEADERS
import matplotlib.pyplot as plt
from collections import Counter


class StatisticsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Statistiques des candidatures')
        self.setGeometry(250, 250, 600, 400)
        self.initUI()

    def initUI(self):
        # Boutons pour afficher les statistiques
        self.totalAppsButton = QtWidgets.QPushButton('Nombre total de candidatures')
        self.statusDistButton = QtWidgets.QPushButton('Répartition par statut')
        self.companyDistButton = QtWidgets.QPushButton('Top 5 entreprises (par nombre de candidatures)')
        self.channelDistButton = QtWidgets.QPushButton('Top 5 canaux de candidature')

        # Disposition des boutons
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.totalAppsButton)
        layout.addWidget(self.statusDistButton)
        layout.addWidget(self.companyDistButton)
        layout.addWidget(self.channelDistButton)
        layout.addStretch()

        self.setLayout(layout)

        # Connexion des boutons aux méthodes
        self.totalAppsButton.clicked.connect(self.showTotalApplications)
        self.statusDistButton.clicked.connect(self.showStatusDistribution)
        self.companyDistButton.clicked.connect(self.showCompanyDistribution)
        self.channelDistButton.clicked.connect(self.showChannelDistribution)

    def showTotalApplications(self):
        applications = read_applications()
        total = len(applications)
        QtWidgets.QMessageBox.information(self, 'Total des candidatures', f'Nombre total de candidatures : {total}')

    def showStatusDistribution(self):
        applications = read_applications()
        statuses = [app[3] for app in applications]  # Statut est à l'index 3
        status_counts = Counter(statuses)

        # Préparation des données pour le graphique
        labels = status_counts.keys()
        sizes = status_counts.values()

        # Création du graphique
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Répartition des candidatures par statut')
        plt.axis('equal')  # Assure que le pie chart est un cercle
        plt.show()

    def showCompanyDistribution(self):
        applications = read_applications()
        companies = [app[0] for app in applications]  # Entreprise est à l'index 0
        company_counts = Counter(companies)
        top_companies = company_counts.most_common(5)

        # Préparation des données pour le graphique
        labels, counts = zip(*top_companies)

        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts, color='skyblue')
        plt.xlabel('Entreprises')
        plt.ylabel('Nombre de candidatures')
        plt.title('Top 5 des entreprises (par nombre de candidatures)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def showChannelDistribution(self):
        applications = read_applications()
        channels = [app[5] for app in applications]  # Canal de candidature est à l'index 5
        channel_counts = Counter(channels)
        top_channels = channel_counts.most_common(5)

        # Préparation des données pour le graphique
        labels, counts = zip(*top_channels)

        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts, color='lightgreen')
        plt.xlabel('Canaux de candidature')
        plt.ylabel('Nombre de candidatures')
        plt.title('Top 5 des canaux de candidature')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
