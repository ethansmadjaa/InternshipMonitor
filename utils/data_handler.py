# utils/data_handler.py

import csv
import os
from utils.constants import CSV_FILE, CSV_SEPARATOR, CSV_ENCODING, CSV_HEADERS


def initialize_csv():
    """Initializes the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding=CSV_ENCODING) as file:
            writer = csv.writer(file, delimiter=CSV_SEPARATOR)
            writer.writerow(CSV_HEADERS)


def read_applications():
    """Reads the applications from the CSV file and returns a list of applications."""
    applications = []
    try:
        with open(CSV_FILE, 'r', encoding=CSV_ENCODING) as file:
            reader = csv.reader(file, delimiter=CSV_SEPARATOR)
            headers = next(reader, None)  # Skip headers
            for row in reader:
                applications.append(row)
    except FileNotFoundError:
        initialize_csv()
    except Exception as e:
        raise e
    return applications


def add_application(application_data):
    """Adds a new application to the CSV file."""
    try:
        initialize_csv()
        with open(CSV_FILE, 'a', newline='', encoding=CSV_ENCODING) as file:
            writer = csv.writer(file, delimiter=CSV_SEPARATOR)
            writer.writerow(application_data)
    except Exception as e:
        raise e


def update_application(old_data, new_data):
    """Updates an existing application in the CSV file."""
    try:
        applications = read_applications()
        updated = False
        for i, row in enumerate(applications):
            if row == old_data:
                applications[i] = new_data
                updated = True
                break
        if updated:
            with open(CSV_FILE, 'w', newline='', encoding=CSV_ENCODING) as file:
                writer = csv.writer(file, delimiter=CSV_SEPARATOR)
                writer.writerow(CSV_HEADERS)  # Write headers
                writer.writerows(applications)
            return True
        else:
            return False
    except Exception as e:
        raise e
