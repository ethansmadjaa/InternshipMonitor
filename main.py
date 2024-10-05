import sys
from PyQt5 import QtWidgets
from windows.main_window import InternshipMonitor


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InternshipMonitor()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
