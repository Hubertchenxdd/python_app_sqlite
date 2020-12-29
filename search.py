from PyQt5.QtWidgets import QFrame, QLabel, QComboBox, QGridLayout, QPushButton, QLineEdit, QTableWidget, QInputDialog, QTableWidgetItem


class Search(QFrame):
    """
    variables:
        self.db_search: defines the database used in the class
        self.grid: defines the layout of the class
        self.t1: defines the input text box for name
        self.c2: defines the combo box for academic institution
        self.c3: defines the combo box for city of residence
        self.c4: defines the combo box for year of birth
        self.c5: defines the combo box for city of birth
        self.c6: defines the combo box for region of birth
        self.search_btn: defines the search button
        self.reset_btn: defines the clear button to reset search condition
        self.people_table: defines the table which shows people data
        self.education_table: defines the table which shows education data
    method:
        def __init__(self, parent=None, db=None): defines the database and call the function to generate UI
        def initUI(self): generate UI
        def update_people_table(self): a function to regenerate self.people_table based on searching condition
        def update_education_table(self): a function to regenerate self.education_table based on searching condition
        def get_Name(self): return a list of name in the database
        def get_CiOB(self): return a list of city appeared in city of birth in the database
        def get_YOB(self): return a list of YOB appeared in the database
        def get_CiOR(self): return a list of city appeared in city of residence in the database
        def get_ReOB(self): return a list of region appeared in region of birth in the database
        def get_AcaInst(self): return a list of institution in the database
        def regenerate(self): regenerate self.people_table and self.education_table
        def clear(self): reset search condition
        def connectDB(self): connect to a database
    """

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.connectDB(db)
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout(self)

        self.grid.addWidget(QLabel("Name:"), 0, 0)
        self.grid.addWidget(QLabel("Academic Institution:"), 1, 0)
        self.grid.addWidget(QLabel("City of Residence:"), 2, 0)
        self.grid.addWidget(QLabel("Year of Birth:"), 0, 2)
        self.grid.addWidget(QLabel("City of Birth:"), 1, 2)
        self.grid.addWidget(QLabel("Region of Birth:"), 2, 2)

        self.t1 = QLineEdit(self)
        self.c2 = QComboBox(self)
        self.c3 = QComboBox(self)
        self.c4 = QComboBox(self)
        self.c5 = QComboBox(self)
        self.c6 = QComboBox(self)

        self.c2.addItems([''] + self.get_AcaInst())
        self.c3.addItems([''] + self.get_CiOR())
        self.c4.addItems([''] + self.get_YOB())
        self.c5.addItems([''] + self.get_CiOB())
        self.c6.addItems([''] + self.get_ReOB())

        self.grid.addWidget(self.t1, 0, 1)
        self.grid.addWidget(self.c2, 1, 1)
        self.grid.addWidget(self.c3, 2, 1)
        self.grid.addWidget(self.c4, 0, 3)
        self.grid.addWidget(self.c5, 1, 3)
        self.grid.addWidget(self.c6, 2, 3)

        self.search_btn = QPushButton("Search")
        self.grid.addWidget(self.search_btn, 3, 2)
        self.reset_btn = QPushButton("Reset")
        self.grid.addWidget(self.reset_btn, 3, 3)

        self.people_table = QTableWidget()
        self.update_people_table()
        self.people_table.resizeColumnsToContents()
        self.people_table.resizeRowsToContents()

        self.education_table = QTableWidget()
        self.update_education_table()
        self.education_table.resizeColumnsToContents()
        self.education_table.resizeRowsToContents()

        self.grid.addWidget(self.people_table, 4, 0, 1, 2)
        self.grid.addWidget(self.education_table, 4, 2, 1, 2)

        self.search_btn.clicked.connect(self.regenerate)
        self.reset_btn.clicked.connect(self.clear)

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(2, 2)
        self.grid.setColumnStretch(3, 2)

    def update_people_table(self):
        self.people_table.clear()
        if self.db_search:
            cur1 = self.db_search.cursor()
            self.search1_query = """select ppl.First_Name,
                                           ppl.Last_Name,
                                           ci1.City,
                                           ppl.Year_of_Birth,
                                           ci2.City,
                                           co.Country_Region
                                    from People ppl, City ci1, City ci2, Country_Region co
                                    where ppl.City_of_Residence = ci1.id
                                    and ppl.City_of_Birth = ci2.id
                                    and ppl.Region_of_Birth = co.id
                                    {}"""
            self.people_data = {}
            cond = '' # need to add conditions
            if self.t1.text() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) like "%{}%" '.format(str(self.t1.text()))
            if self.c2.currentText() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) in ' \
                        '(select (ppl.First_Name || " " || ppl.Last_Name) ' \
                        'from People ppl, Education edu, School sch, Degree deg ' \
                        'where ppl.id = edu.PeopleID ' \
                        'and edu.SchoolID = sch.id ' \
                        'and edu.DegreeID = deg.id ' \
                        'and sch.School_Name = "{}") '.format(str(self.c2.currentText()))
            if self.c3.currentText() != '':
                cond += 'and ci1.City = "{}" '.format(str(self.c3.currentText()))
            if self.c4.currentText() != '':
                cond += 'and ppl.Year_of_Birth = "{}" '.format(str(self.c4.currentText()))
            if self.c5.currentText() != '':
                cond += 'and ci2.City = "{}" '.format(str(self.c5.currentText()))
            if self.c6.currentText() != '':
                cond += 'and co.Country_Region = "{}" '.format(str(self.c6.currentText()))
            people_col = ['First_Name', 'Last Name', 'Residence City', 'YOB', 'City of Birth', 'Region of Birth']
            for c in people_col:
                self.people_data[c] = []
            cur1.execute(self.search1_query.format(cond))

            row_cnt = 0
            for d in cur1:
                row_cnt += 1
                for i in range(len(self.people_data.keys())):
                    self.people_data[list(self.people_data.keys())[i]].append(d[i])

            self.people_table.setRowCount(row_cnt)
            self.people_table.setColumnCount(len(self.people_data))

            for n in range(len(people_col)):
                for m in range(row_cnt):
                    item = self.people_data[people_col[n]][m]
                    self.people_table.setItem(m, n, QTableWidgetItem(str(item)))
            self.people_table.setHorizontalHeaderLabels(people_col)

    def update_education_table(self):
        self.education_table.clear()
        if self.db_search:
            cur2 = self.db_search.cursor()
            self.search2_query = """select (ppl.First_Name || ' ' || ppl.Last_Name), 
                                           sch.School_Name, 
                                           deg.Degree
                                    from People ppl, Education edu, School sch, Degree deg
                                    where ppl.id = edu.PeopleID
                                    and edu.SchoolID = sch.id
                                    and edu.DegreeID = deg.id
                                    {}"""
            self.education_data = {}
            cond = ''  # need to add conditions
            if self.t1.text() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) like "%{}%" '.format(str(self.t1.text()))
            if self.c2.currentText() != '':
                cond += 'and sch.School_Name = "{}" '.format(str(self.c2.currentText()))
            if self.c3.currentText() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) in ' \
                        '(select  (ppl.First_Name || " " || ppl.Last_Name) ' \
                        'from People ppl, City ci1, City ci2, Country_Region co ' \
                        'where ppl.City_of_Residence = ci1.id ' \
                        'and ppl.City_of_Birth = ci2.id ' \
                        'and ppl.Region_of_Birth = co.id ' \
                        'and ci1.City = "{}") '.format(str(self.c3.currentText()))
            if self.c4.currentText() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) in ' \
                        '(select  (ppl.First_Name || " " || ppl.Last_Name) ' \
                        'from People ppl, City ci1, City ci2, Country_Region co ' \
                        'where ppl.City_of_Residence = ci1.id ' \
                        'and ppl.City_of_Birth = ci2.id ' \
                        'and ppl.Region_of_Birth = co.id ' \
                        'and ppl.Year_of_Birth = "{}") '.format(str(self.c4.currentText()))
            if self.c5.currentText() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) in ' \
                        '(select  (ppl.First_Name || " " || ppl.Last_Name) ' \
                        'from People ppl, City ci1, City ci2, Country_Region co ' \
                        'where ppl.City_of_Residence = ci1.id ' \
                        'and ppl.City_of_Birth = ci2.id ' \
                        'and ppl.Region_of_Birth = co.id ' \
                        'and ci2.City = "{}") '.format(str(self.c5.currentText()))
            if self.c6.currentText() != '':
                cond += 'and (ppl.First_Name || " " || ppl.Last_Name) in ' \
                        '(select  (ppl.First_Name || " " || ppl.Last_Name) ' \
                        'from People ppl, City ci1, City ci2, Country_Region co ' \
                        'where ppl.City_of_Residence = ci1.id ' \
                        'and ppl.City_of_Birth = ci2.id ' \
                        'and ppl.Region_of_Birth = co.id ' \
                        'and co.Country_Region = "{}") '.format(str(self.c6.currentText()))

            education_col = ['Full Name', 'School_Name', 'Degree']
            for c in education_col:
                self.education_data[c] = []
            cur2.execute(self.search2_query.format(cond))

            row_cnt = 0
            for d in cur2:
                row_cnt += 1
                for i in range(len(self.education_data.keys())):
                    self.education_data[list(self.education_data.keys())[i]].append(d[i])

            self.education_table.setRowCount(row_cnt)
            self.education_table.setColumnCount(len(self.education_data))

            for n in range(len(education_col)):
                for m in range(row_cnt):
                    item = self.education_data[education_col[n]][m]
                    self.education_table.setItem(m, n, QTableWidgetItem(str(item)))
            self.education_table.setHorizontalHeaderLabels(education_col)

    def get_Name(self):
        name = []
        if self.db_search:
            cur = self.db_search.cursor()
            cur.execute("""select (First_Name || ' ' ||Last_Name) name from People
                           order by name""")

            for city in cur:
                name.append(city[0])
        return name

    def get_CiOB(self):
        CiOB = []
        if self.db_search:
            cur = self.db_search.cursor()
            cur.execute("""select city from city
                           where id in (select City_of_Birth from People)
                           order by city""")
            for city in cur:
                CiOB.append(city[0])
        return CiOB

    def get_YOB(self):
        YOB = []
        if self.db_search:
            cur = self.db_search.cursor()
            cur.execute("""select Year_of_Birth from People
                           order by Year_of_Birth""")
            for year in cur:
                YOB.append(str(year[0]))
        return YOB

    def get_CiOR(self):
        CiOR = []
        if self.db_search:
            cur = self.db_search.cursor()
            cur.execute("""select city from city
                           where id in (select City_of_Residence from People)
                           order by city""")
            for city in cur:
                CiOR.append(city[0])
        return CiOR

    def get_ReOB(self):
        ReOB = []
        if self.db_search:
            cur = self.db_search.cursor()
            cur.execute("""select country_region from country_region
                           order by country_region""")
            for region in cur:
                ReOB.append(region[0])
        return ReOB

    def get_AcaInst(self):
        AcaInst = []
        if self.db_search:
            cur = self.db_search.cursor()
            cur.execute("""select School_Name from school
                           order by School_Name""")
            for school in cur:
                AcaInst.append(school[0])
        return AcaInst

    def regenerate(self):
        if self.db_search:
            self.update_people_table()
            self.people_table.resizeColumnsToContents()
            self.people_table.resizeRowsToContents()

            self.update_education_table()
            self.education_table.resizeColumnsToContents()
            self.education_table.resizeRowsToContents()

    def clear(self):
        self.t1.clear()
        self.c2.setCurrentText('')
        self.c3.setCurrentText('')
        self.c4.setCurrentText('')
        self.c5.setCurrentText('')
        self.c6.setCurrentText('')
        self.regenerate()

    def connectDB(self, db):
        self.db_search = db
