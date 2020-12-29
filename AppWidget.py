from view import *
from add import *
from search import *
import sqlite3 as LDBI

from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QTabWidget,
    QVBoxLayout,
    QMessageBox
)

class AppWidget(QFrame):
    """
    variables:
        self.db: defines the database used in the class
        self.layout: defines the layout of the class
        self.tabs: defines the tab wib widget
        self.Vtab: defines the View tab
        self.Atab: defines the Add tab
        self.Stab: defines the Search tab
    methods:
        def __init__(self, parent=None):defines the database and call the function to generate UI
        def initUI(self): generate UI
        def disconnect(self): disconnect to all the database
        def openCall(self): open a new database
        def submit_data(self): submit data and insert into the database
        def academic_insert(self, year, degree, school, ppl_id): insert new institution into the database
        def newCity(self): insert new City into the database
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = LDBI.connect('Academic.db')
        self.initUi()

    def initUi(self):
        
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.Vtab = View(self, self.db)
        self.Atab = Add(self, self.db)
        self.Stab = Search(self, self.db)

        self.tabs.addTab(self.Vtab, "View Tables")
        self.tabs.addTab(self.Atab, "Add Data")
        self.tabs.addTab(self.Stab, "Search DB")
        self.tabs.setCurrentWidget(self.Atab)

        self.tabs.setTabPosition(QTabWidget.South)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.Atab.btn3.clicked.connect(self.newCity1)
        self.Atab.btn5.clicked.connect(self.newCity2)
        self.Atab.btn6.clicked.connect(self.newRegion)

        self.Atab.add_school1.clicked.connect(self.newSchool1)
        self.Atab.add_school2.clicked.connect(self.newSchool2)
        self.Atab.add_school3.clicked.connect(self.newSchool3)
        self.Atab.add_school4.clicked.connect(self.newSchool4)

        self.Atab.submit.clicked.connect(self.submit_data)

    def disconnect(self):
        self.Vtab.db.close()
        self.Stab.db_search.close()
        self.Atab.db_add.close()
        self.db.close()
        self.db = None

    def openCall(self):
        dlg = QFileDialog()
        name = dlg.getOpenFileName(self, 'Open File', ".", "*.db")
        if name[0]:
            self.db = LDBI.connect(name[0])
            self.Stab.connectDB(self.db)
            self.Atab.connectDB(self.db)
            self.Vtab.connectDB(self.db)

    def submit_data(self):

        if self.db:
            fn = self.Atab.txtIn1.text()
            ln = self.Atab.txtIn2.text()
            cior = self.Atab.combo3.currentText()
            yob = self.Atab.combo4.currentText()
            ciob = self.Atab.combo5.currentText()
            coob = self.Atab.combo6.currentText()

            if fn == '' or ln == '' or cior == '' or yob == '' or ciob == '' or coob == '':
                msg = QMessageBox()
                msg.setWindowTitle("Missing Value")
                msg.setText("Please fill in all the blanks. Thank you.")
                msg.exec_()

            else:
                if (fn + ' ' + ln) not in self.Atab.get_all_names():
                    if cior not in self.Atab.get_all_cities():
                        cior_insert_query = """insert into City 
                                               values ((select max(ID) + 1 from City), '{}')""".format(cior)
                        cior_insert = self.db.cursor()
                        cior_insert.execute(cior_insert_query)
                    if cior not in self.Stab.get_CiOR():
                        self.Stab.c3.addItem(str(cior))
                        self.Stab.c3.model().sort(0)
                    cior_id_query = """select id from City where city = '{}'""".format(cior)
                    cior_id_cur = self.db.cursor()
                    cior_id_cur.execute(cior_id_query)
                    for i in cior_id_cur:
                        cior_id = i[0]

                    if yob not in self.Stab.get_YOB():
                        self.Stab.c4.addItem(str(yob))
                        self.Stab.c4.model().sort(0)

                    if ciob not in self.Atab.get_all_cities():
                        ciob_insert_query = """insert into City 
                                               values ((select max(ID) + 1 from City), '{}')""".format(ciob)
                        ciob_insert = self.db.cursor()
                        ciob_insert.execute(ciob_insert_query)
                    if ciob not in self.Stab.get_CiOB():
                        self.Stab.c5.addItem(str(ciob))
                        self.Stab.c5.model().sort(0)
                    ciob_id_query = """select id from City where city = '{}'""".format(ciob)
                    ciob_id_cur = self.db.cursor()
                    ciob_id_cur.execute(ciob_id_query)
                    for i in ciob_id_cur:
                        ciob_id = i[0]

                    if coob not in self.Atab.get_all_regions():
                        coob_insert_query = """insert into Country_Region 
                                               values ((select max(ID) + 1 from Country_Region), '{}')""".format(coob)
                        coob_insert = self.db.cursor()
                        coob_insert.execute(coob_insert_query)
                        self.Stab.c6.addItem(str(coob))
                        self.Stab.c6.model().sort(0)
                    coob_id_query = """select id from Country_Region where Country_Region = '{}'""".format(coob)
                    coob_id_cur = self.db.cursor()
                    coob_id_cur.execute(coob_id_query)
                    for i in coob_id_cur:
                        coob_id = i[0]

                    ppl_insert_query = """insert into People
                                          values ((select max(ID)+1 from People), 
                                          '{}', '{}', {}, {}, {}, {})""".format(fn, ln, cior_id, yob, ciob_id, coob_id)

                    people_insert = self.db.cursor()
                    people_insert.execute(ppl_insert_query)

                    self.Atab.txtIn1.clear()
                    self.Atab.txtIn2.clear()
                    self.Atab.combo3.setCurrentText('')
                    self.Atab.combo4.setCurrentText('')
                    self.Atab.combo5.setCurrentText('')
                    self.Atab.combo6.setCurrentText('')

                ppl_id_query = """select id from People where First_Name = '{}' and Last_Name = '{}'""".format(fn, ln)
                ppl_id_cur = self.db.cursor()
                ppl_id_cur.execute(ppl_id_query)
                for i in ppl_id_cur:
                    ppl_id = i[0]

                self.academic_insert(self.Atab.year1, self.Atab.degree1, self.Atab.school1, ppl_id)
                self.academic_insert(self.Atab.year2, self.Atab.degree2, self.Atab.school2, ppl_id)
                self.academic_insert(self.Atab.year3, self.Atab.degree3, self.Atab.school3, ppl_id)
                self.academic_insert(self.Atab.year4, self.Atab.degree4, self.Atab.school4, ppl_id)

                self.Stab.update_people_table()
                self.Stab.people_table.resizeColumnsToContents()
                self.Stab.people_table.resizeRowsToContents()

                self.Stab.update_education_table()
                self.Stab.education_table.resizeColumnsToContents()
                self.Stab.education_table.resizeRowsToContents()

                self.Vtab.select_list()

                self.db.commit()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Database disconnected")
            msg.setText("Please connect to a database. Thank you.")
            msg.exec_()

    def academic_insert(self, year, degree, school, ppl_id):
        y = year.currentText()
        d = degree.currentText()
        s = school.currentText()

        if y != 'Graduate Year' and d != 'Degree' and s != 'Institution Name':
            if s not in self.Atab.get_all_schools():
                school_insert_query = """insert into School values ((select max(ID) + 1 from School), '{}')""".format(s)
                insert = self.db.cursor()
                insert.execute(school_insert_query)
                self.Stab.c2.addItem(str(s))
                self.Stab.c2.model().sort(0)
            school_id_query = """select id from School where School_Name = '{}'""".format(s)
            school_id_cur = self.db.cursor()
            school_id_cur.execute(school_id_query)
            for i in school_id_cur:
                school_id = i[0]

            edu_insert_query = """insert into Education
                                  values ((select max(ID)+1 from Education), {}, {}, 
                                  (select id from Degree where degree = '{}'), {})""".format(ppl_id, school_id, d, y)
            edu_cur = self.db.cursor()
            edu_cur.execute(edu_insert_query)

        year.setCurrentText('Graduate Year')
        degree.setCurrentText('Degree')
        school.setCurrentText('Institution Name')

    def newCity1(self):
        text, okPressed = QInputDialog.getText(self, "Type in new city", "City:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_cities():
            self.Atab.combo3.addItem(text)
            self.Atab.combo5.addItem(text)
            self.Atab.combo3.setCurrentText(text)
        else:
            self.Atab.combo3.setCurrentText(text)

    def newCity2(self):
        text, okPressed = QInputDialog.getText(self, "Type in new city", "City:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_cities():
            self.Atab.combo3.addItem(text)
            self.Atab.combo5.addItem(text)
            self.Atab.combo5.setCurrentText(text)
        else:
            self.Atab.combo5.setCurrentText(text)

    def newRegion(self):
        text, okPressed = QInputDialog.getText(self, "Type in new region/country", "Region/Country:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_regions():
            self.Atab.combo6.addItem(text)
            self.Atab.combo6.setCurrentText(text)
        else:
            self.Atab.combo6.setCurrentText(text)

    def newSchool1(self):
        text, okPressed = QInputDialog.getText(self, "Type in new school", "School name:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_schools():
            self.Atab.school1.addItem(text)
            self.Atab.school2.addItem(text)
            self.Atab.school3.addItem(text)
            self.Atab.school4.addItem(text)
            self.Atab.school1.setCurrentText(text)
        else:
            self.Atab.school1.setCurrentText(text)

    def newSchool2(self):
        text, okPressed = QInputDialog.getText(self, "Type in new school", "School name:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_schools():
            self.Atab.school1.addItem(text)
            self.Atab.school2.addItem(text)
            self.Atab.school3.addItem(text)
            self.Atab.school4.addItem(text)
            self.Atab.school2.setCurrentText(text)
        else:
            self.Atab.school2.setCurrentText(text)

    def newSchool3(self):
        text, okPressed = QInputDialog.getText(self, "Type in new school", "School name:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_schools():
            self.Atab.school1.addItem(text)
            self.Atab.school2.addItem(text)
            self.Atab.school3.addItem(text)
            self.Atab.school4.addItem(text)
            self.Atab.school3.setCurrentText(text)
        else:
            self.Atab.school3.setCurrentText(text)

    def newSchool4(self):
        text, okPressed = QInputDialog.getText(self, "Type in new school", "School name:", QLineEdit.Normal, "")
        if okPressed and text != '' and text not in self.Atab.get_all_schools():
            self.Atab.school1.addItem(text)
            self.Atab.school2.addItem(text)
            self.Atab.school3.addItem(text)
            self.Atab.school4.addItem(text)
            self.Atab.school4.setCurrentText(text)
        else:
            self.Atab.school4.setCurrentText(text)


