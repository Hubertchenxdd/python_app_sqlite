from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton
from datetime import date


class Add(QFrame):
    """
    variables:
        self.db_add: defines the database used in the class
        self.grid: defines the layout grid
        self.txtIn1: the input textbox for first name
        self.txtIn2: the input textbox for last name
        self.combo3: the combo box for city of residence
        self.combo4: the combo box for year of birth
        self.combo5: the combo box for city of birth
        self.combo6: the combo box for region of birth
        self.btn3: the button to add city if city of residence doesn't exist in the provided list
        self.btn5: the button to add city if city of birth doesn't exist in the provided list
        self.btn6: the button to add region if region of birth doesn't exist in the provided list
        self.year 1 through 4: select graduate year
        self.degree 1 through 4: select degree
        self.school 1 through 4: select institution attended
        self.add_school 1 through 4: the button to add school if school attended doesn't exist in the provided list
        self.submit: the button to submit the input data

    method:
        def __init__(self, parent=None, db=None): defines the database and call the function to generate UI
        def initUI(self): initializes UI
        def academic_setting(self, year, degree, school): defines the parameter for year, degree, school, and add_school
        def get_all_cities(self): returns the cities in the database
        def get_all_regions(self): returns the regions in the database
        def get_all_schools(self): returns the schools in the database
        def get_all_names(self): returns the names in the database
        def connectDB(self, db): connect to a database and calls a function to refresh items in combo boxes
        def refreshCB(self): refresh items in combo boxes
    """


    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db_add = db
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout(self)

        self.grid.addWidget(QLabel("First name:"), 0, 0)
        self.grid.addWidget(QLabel("Family name:"), 1, 0)
        self.grid.addWidget(QLabel("City of Residence:"), 2, 0)
        self.grid.addWidget(QLabel("Year of Birth:"), 3, 0)
        self.grid.addWidget(QLabel("City of Birth:"), 4, 0)
        self.grid.addWidget(QLabel("Region/Country of Birth:"), 5, 0)
        self.grid.addWidget(QLabel("Academic Degree Earned:"), 6, 0)

        self.txtIn1 = QLineEdit(self)
        self.txtIn2 = QLineEdit(self)
        self.combo3 = QComboBox(self)
        self.combo4 = QComboBox(self)
        self.combo5 = QComboBox(self)
        self.combo6 = QComboBox(self)

        self.refreshCB()

        self.grid.addWidget(self.txtIn1, 0, 1, 1, 4)
        self.grid.addWidget(self.txtIn2, 1, 1, 1, 4)
        self.grid.addWidget(self.combo3, 2, 1, 1, 3)
        self.grid.addWidget(self.combo4, 3, 1, 1, 4)
        self.grid.addWidget(self.combo5, 4, 1, 1, 3)
        self.grid.addWidget(self.combo6, 5, 1, 1, 3)

        self.btn3 = QPushButton("New City")
        self.btn5 = QPushButton("New City")
        self.btn6 = QPushButton("New Region/Country")

        self.grid.addWidget(self.btn3, 2, 4)
        self.grid.addWidget(self.btn5, 4, 4)
        self.grid.addWidget(self.btn6, 5, 4)

        self.setLayout(self.grid)

        self.year1 = QComboBox(self)
        self.degree1 = QComboBox(self)
        self.school1 = QComboBox(self)
        self.add_school1 = QPushButton("School not in list")
        self.academic_setting(self.year1, self.degree1, self.school1)
        self.grid.addWidget(self.year1, 7, 0)
        self.grid.addWidget(self.degree1, 7, 1)
        self.grid.addWidget(self.school1, 7, 2, 1, 2)
        self.grid.addWidget(self.add_school1, 7, 4)

        self.year2 = QComboBox(self)
        self.degree2 = QComboBox(self)
        self.school2 = QComboBox(self)
        self.add_school2 = QPushButton("School not in list")
        self.academic_setting(self.year2, self.degree2, self.school2)
        self.grid.addWidget(self.year2, 8, 0)
        self.grid.addWidget(self.degree2, 8, 1)
        self.grid.addWidget(self.school2, 8, 2, 1, 2)
        self.grid.addWidget(self.add_school2, 8, 4)

        self.year3 = QComboBox(self)
        self.degree3 = QComboBox(self)
        self.school3 = QComboBox(self)
        self.add_school3 = QPushButton("School not in list")
        self.academic_setting(self.year3, self.degree3, self.school3)
        self.grid.addWidget(self.year3, 9, 0)
        self.grid.addWidget(self.degree3, 9, 1)
        self.grid.addWidget(self.school3, 9, 2, 1, 2)
        self.grid.addWidget(self.add_school3, 9, 4)

        self.year4 = QComboBox(self)
        self.degree4 = QComboBox(self)
        self.school4 = QComboBox(self)
        self.add_school4 = QPushButton("School not in list")
        self.academic_setting(self.year4, self.degree4, self.school4)
        self.grid.addWidget(self.year4, 10, 0)
        self.grid.addWidget(self.degree4, 10, 1)
        self.grid.addWidget(self.school4, 10, 2, 1, 2)
        self.grid.addWidget(self.add_school4, 10, 4)

        self.submit = QPushButton("Submit")
        self.grid.addWidget(self.submit, 11, 4)

    def academic_setting(self, year, degree, school):
        year.addItems(['Graduate Year'] + [str(i) for i in range(1990, date.today().year+6)])
        degree.addItems(['Degree', 'Bachelor', 'Master', 'Doctor'])
        school.addItems(['Institution Name'] + self.get_all_schools())

    def get_all_cities(self):
        all_city = []
        if self.db_add:
            cur = self.db_add.cursor()
            cur.execute("""select city from city""")
            for city in cur:
                all_city.append(city[0])
        return all_city

    def get_all_regions(self):
        all_region = []
        if self.db_add:
            cur = self.db_add.cursor()
            cur.execute("""select country_region from country_region""")
            for city in cur:
                all_region.append(city[0])
        return all_region

    def get_all_schools(self):
        all_school = []
        if self.db_add:
            cur = self.db_add.cursor()
            cur.execute("""select School_Name from school""")
            for school in cur:
                all_school.append(school[0])
        return all_school

    def get_all_names(self):
        all_name = []
        if self.db_add:
            cur = self.db_add.cursor()
            cur.execute("""select (First_Name || ' ' || Last_Name) from People""")
            for name in cur:
                all_name.append(name[0])
        return all_name

    def connectDB(self, db):
        self.db_add = db
        self.refreshCB()

    def refreshCB(self):
        self.combo3.clear()
        self.combo4.clear()
        self.combo5.clear()
        self.combo6.clear()

        self.combo3.addItems([''] + self.get_all_cities())
        self.combo4.addItems([''] + [str(i) for i in range(1950, date.today().year+6)])
        self.combo5.addItems([''] + self.get_all_cities())
        self.combo6.addItems([''] + self.get_all_regions())
