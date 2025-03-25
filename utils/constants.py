# utils/constants.py

import os

CSV_FILE = 'candidatures.csv'
CSV_SEPARATOR = ';'
CSV_ENCODING = 'utf-8'

CSV_HEADERS = [
    'Entreprise',
    'Intitulé',
    'Date',
    'Statut',
    'Détails',
    'Canal',
    'Nom du contact',
    'Email du contact',
    'Téléphone du contact',
    'Documents'
]

DOCUMENTS_DIR = os.path.join(os.getcwd(), 'documents')
