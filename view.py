from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QTableWidget, QComboBox, QTableWidgetItem


class View(QFrame):
    """
    variables:
        self.db: defines the database used in the class
        self.layout: defines the layout of the class
        self.hbox: defines the layout of the table list
        self.table_list: defines the combo box of the table list
        self.cur: defines the cursor of the database
        self.result: defines the result of selecting table name
        self.table_names: defines the list of table names
        self.tableWidget: defines a table widget
        self.current_table: defines the table name that is selected
        self.current_data: defines the data in the current table

    method:
        def __init__(self, parent=None, db=None): defines the database and call the function to generate UI
        def initUI(self): generate UI
        def select_list(self): a motion triggered by changing a table
        def setData(self): select data from database and demonstrate in a table
        def connectDB(self, db): connect to a database
    """

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout(self)

        self.hbox = QHBoxLayout()
        self.table_list = QComboBox(self)

        self.db.text_factory = str
        self.cur = self.db.cursor()
        self.result = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        self.table_names = sorted(list(zip(*self.result))[0])

        self.table_list.addItems(self.table_names)
        self.table_list.setCurrentText('People')
        self.hbox.addWidget(self.table_list)

        self.tableWidget = QTableWidget()
        self.setData()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        self.layout.addLayout(self.hbox)
        self.layout.addWidget(self.tableWidget)

        self.table_list.currentTextChanged.connect(self.select_list)

    def select_list(self):
        self.tableWidget.clear()
        if self.db:
            self.setData()
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()

    def setData(self):
        self.current_table = self.table_list.currentText()
        view_query = """select * from {}""".format(self.current_table)
        view = self.db.cursor()
        view.execute(view_query)

        col_name_query = """select name FROM pragma_table_info('{}')""".format(self.current_table)
        col_name = self.db.cursor()
        col_name.execute(col_name_query)

        self.current_data = {}
        header = []
        for c in col_name:
            header.append(c[0])
            self.current_data[c[0]] = []
        row_cnt = 0
        for d in view:
            row_cnt += 1
            for i in range(len(self.current_data.keys())):
                self.current_data[list(self.current_data.keys())[i]].append(d[i])

        self.tableWidget.setRowCount(row_cnt)
        self.tableWidget.setColumnCount(len(self.current_data))

        for n in range(len(header)):
            for m in range(row_cnt):
                item = self.current_data[header[n]][m]
                self.tableWidget.setItem(m, n, QTableWidgetItem(str(item)))
        self.tableWidget.setHorizontalHeaderLabels(header)

    def connectDB(self, db):
        self.db = db
        self.select_list()
