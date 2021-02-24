from Code import AppWidget
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class Final_Project(QMainWindow):
    def __init__(self):
        super(Final_Project, self).__init__()
        self.setCentralWidget(AppWidget(self))
        self.setWindowTitle('Final Project')
        self.resize(800, 400)

        bar = self.menuBar()
        # File menu
        file_menu = bar.addMenu('File')
        # adding actions to file menu
        open_action = QAction('&Open database', self)
        disconnect_action = QAction('&Disconnect to database', self)
        close_action = QAction('&Close application', self)

        file_menu.addAction(open_action)
        file_menu.addAction(disconnect_action)
        file_menu.addAction(close_action)

        open_action.triggered.connect(self.centralWidget().openCall)
        close_action.triggered.connect(self.close)
        disconnect_action.triggered.connect(self.centralWidget().disconnect)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Final_Project()
    widget.show()
    sys.exit(app.exec_())