import selectors
from PyQt6 import QtCore, QtGui, QtWidgets, uic
import matplotlib.image as mpimg
import pyqtgraph as pg
from PyQt6.QtWidgets import QMessageBox 
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3
from sqlite3 import Error
import sys
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
 
class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#ffffbf')
        #d8ffdb
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
 
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        uic.loadUi('PySQLite_Designer_4.ui', self)
        self.table = self.table
        # database ="/Users/renjie/Documents/碩班課程/class/SQL/database-sample/database.sqlite"
        database = "/Users/renjie/Documents/碩班課程/class/SQL/database-711036104/test.sqlite"
        # create a database connect
        self.conn = create_connection(database)
        # self.conn=sqlite3.connect('example.db')

        self.setWindowTitle('A Conference Paper Query System')
 
        #tab1 Signals
        self.actionEXIT.clicked.connect(self.appEXIT)
        self.lineEdit_title.returnPressed.connect(self.searchByTitle)
        self.lineEdit_Authors.returnPressed.connect(self.searchByAuthors)
        self.p_But_by_title.clicked.connect(self.searchByTitle)
        self.p_But_by_titlesta.clicked.connect(self.stat_title)
        self.p_But_by_Authors.clicked.connect(self.searchByAuthors)
        self.p_But_by_authorsta.clicked.connect(self.stat_authors)
        self.table.doubleClicked.connect(self.rowSelected)
        self.actionSave_Data.clicked.connect(self.saveData)
        type = ['Poster','Oral','Spotlight']
        self.comboBox_type.addItems(type)
        self.comboBox_type.currentIndexChanged.connect(self.searchBytype) 
        self.p_But_by_type.clicked.connect(self.searchBytype)
        self.p_But_by_type_sta.clicked.connect(self.stat_searchBytype) 
        page = ['1','2','3','4','5']  
        self.comboBox_page.addItems(page)
        self.comboBox_page.currentIndexChanged.connect(self.showTable)
        self.p_But_nextpage.clicked.connect(self.nextpage)
        self.p_But_prepage.clicked.connect(self.prepage)
        self.next_pushButton.clicked.connect(self.picpage)
        #tab2 Signals
        self.pre_pushButton.clicked.connect(self.searchpage)


        
         
    #tab1 Slots
    def picpage(self):
        self.tabWidget.setCurrentIndex(1)
    def searchpage(self):
        self.tabWidget.setCurrentIndex(0)

    def searchByTitle(self,s):
        img_dir = "/Users/renjie/Documents/碩班課程/class/SQL/database-711036104/NIP2015_Images/"
        title_key = self.lineEdit_title.text()            
        # sql = "select id, title, eventtype, abstract from papers where title like '%"+title_key+"%'"
        sql = "select id,imgfile"         
        if self.checkBox_title.isChecked():
            sql = sql + ",title"
        if self.checkBox_type.isChecked():
            sql = sql + ",eventtype"
        if self.checkBox_abstract.isChecked():
            sql = sql + ",abstract"   
        if self.checkBox_text.isChecked():
            sql = sql + ", papertext"       
        sql = sql + " from papers where title like '%"+title_key+"%'"
        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0:
                ToTableView(self, self.rows)                                                 
                
        
            
    def searchByAuthors(self):
        authors_key = self.lineEdit_Authors.text()
        # sql = "select id, title, eventtype, abstract from papers where title like '%"+title_key+"%'"
        sql = "select papers.id,papers.imgfile"
         
        if self.checkBox_title.isChecked():
            sql = sql + ",papers.title"
        if self.checkBox_type.isChecked():
            sql = sql + ",papers.eventtype"
        if self.checkBox_abstract.isChecked():
            sql = sql + ",papers.abstract"   
        if self.checkBox_text.isChecked():
            sql = sql + ",papers.papertext"
         #重寫語法
        sql = sql + " from papers JOIN PaperAuthors ON Papers.Id = PaperAuthors.PaperId JOIN Authors ON PaperAuthors.AuthorId = Authors.Id WHERE Authors.Name like '%"+authors_key+"%'"
        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)

    def searchBytype(self):
        authors_key = self.lineEdit_Authors.text()
        title_key = self.lineEdit_title.text()
        type = self.comboBox_type.currentText() 
        sql = "select papers.id,papers.imgfile"
         
        if self.checkBox_title.isChecked():
            sql = sql + ",papers.title"
        if self.checkBox_type.isChecked():
            sql = sql + ",papers.eventtype"
        if self.checkBox_abstract.isChecked():
            sql = sql + ",papers.abstract"   
        if self.checkBox_text.isChecked():
            sql = sql + ",papers.papertext"
         #重寫語法
        sql = sql + " from papers JOIN PaperAuthors ON Papers.Id = PaperAuthors.PaperId JOIN Authors ON PaperAuthors.AuthorId = Authors.Id WHERE Authors.Name like '%"+authors_key+"%' and EventType like '%"+type+"%'"
        # sql = sql + " from papers JOIN PaperAuthors ON Papers.Id = PaperAuthors.PaperId JOIN Authors ON PaperAuthors.AuthorId = Authors.Id WHERE Authors.Name like '%"+authors_key+"%' and EventType like '%"+type+"%'"
        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)   

    def stat_authors(self):
        authors_key = self.lineEdit_Authors.text()
        sql = "SELECT Authors.Name, COUNT(DISTINCT Papers.Id) AS PaperCount, COUNT(DISTINCT Authors.Id) AS AuthorCount,COUNT(DISTINCT Papers.EventType) AS EventTypeCount"+" FROM Papers"+" JOIN PaperAuthors ON Papers.Id = PaperAuthors.PaperId"+" JOIN Authors ON PaperAuthors.AuthorId = Authors.Id"+" WHERE Authors.Name like '%"+authors_key+"%' GROUP BY Authors.Name"
        self.rows = SQLExecute(self, sql)
        with self.conn:
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)

    def stat_title(self):
        title_key = self.lineEdit_title.text()
        sql = "SELECT Authors.Name, COUNT(DISTINCT Papers.Id) AS PaperCount, COUNT(DISTINCT Authors.Id) AS AuthorCount,COUNT(DISTINCT Papers.EventType) AS EventTypeCount"+" FROM Papers"+" JOIN PaperAuthors ON Papers.Id = PaperAuthors.PaperId"+" JOIN Authors ON PaperAuthors.AuthorId = Authors.Id"+" WHERE Authors.Name like '%"+title_key+"%' GROUP BY Authors.Name"
        self.rows = SQLExecute(self, sql)
        with self.conn:
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)

    def stat_searchBytype(self):
        authors_key = self.lineEdit_Authors.text()
        title_key = self.lineEdit_title.text()
        type = self.comboBox_type.currentText()         
        sql = "SELECT Authors.Name, COUNT(DISTINCT Papers.Id) AS PaperCount, COUNT(DISTINCT Authors.Id) AS AuthorCount,COUNT(DISTINCT Papers.EventType) AS EventTypeCount"+" FROM Papers"+" JOIN PaperAuthors ON Papers.Id = PaperAuthors.PaperId"+" JOIN Authors ON PaperAuthors.AuthorId = Authors.Id"+" WHERE Authors.Name like '%"+authors_key+"%' and EventType like '%"+type+"%' and title like'%"+title_key+"%' GROUP BY Authors.Name"
        self.rows = SQLExecute(self, sql)
        with self.conn:
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)
       
     
    def rowSelected(self, mi):
        # print([mi.row(), mi.column()])
        if 'Abstract' in self.df.columns:
            col_list = list(self.df.columns)
        else:
            print('No Abstract from the Query')
            return
        # display Abstract on TextBrowser, then go fetch author name        
        self.textBrowser_abstract.setText(self.df.iloc[mi.row(), col_list.index('Abstract')])
        show_authors(self, self.df.iloc[mi.row(), 0]) 
        self.textBrowser_title.setText(self.df.iloc[mi.row(), col_list.index('Title')])
        # show_title(self, self.df.iloc[mi.row(), 0])
        img=self.df.iloc[mi.row(), col_list.index('imgfile')]
        img_dir = "/Users/renjie/Documents/碩班課程/class/SQL/database-711036104/NIP2015_Images"
        img_path = os.path.join(img_dir, img)
        self.label_Img.setPixmap(QPixmap(img_path))
      
       

    
    def showTable(self):       
        page=int(self.comboBox_page.currentText())
        start_idx =(page-1)*10
        end_idx=start_idx+10
        data =self.df.iloc[start_idx:end_idx, :]
        self.model=TableModel(data)
        self.table.setModel(self.model)

    def nextpage(self):       
        page=int(self.comboBox_page.currentText())
        start_idx =(page)*10
        end_idx=start_idx+10
        data =self.df.iloc[start_idx:end_idx, :]
        self.model=TableModel(data)
        self.table.setModel(self.model)
        page=self.comboBox_page.setCurrentText(str(int(self.comboBox_page.currentText())+1))

    def prepage(self):       
        page=int(self.comboBox_page.currentText())
        start_idx =(page)*10
        end_idx=start_idx+10
        data =self.df.iloc[start_idx:end_idx, :]
        self.model=TableModel(data)
        self.table.setModel(self.model)
        page=self.comboBox_page.setCurrentText(str(int(self.comboBox_page.currentText())-1))    
 
    def saveData(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            "", "EXCEL files (*.xlsx)")
        if len(fname) != 0:
            self.df.to_excel(fname)
 
    def appEXIT(self):
        self.conn.close() # close database
        self.close() # close app

          


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
def SQLExecute(self, SQL):
    """
    Execute a SQL command
    :param conn: SQL command
    :return: None
    """
    self.cur = self.conn.cursor()
    self.cur.execute(SQL)
    rows = self.cur.fetchall()
 
    if len(rows) == 0: # nothing found
        # raise a messageBox here
        dlg = QMessageBox(self)
        dlg.setWindowTitle("SQL Information: ")
        dlg.setText("No data match the query !!!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('OK')
        dlg.setIcon(QMessageBox.Icon.Information)
        button = dlg.exec()
        # return
    return rows
 
def ToTableView(self, rows):
    """
    Display rows on the TableView in pandas format
    """
    names = [description[0] for description in self.cur.description]# extract column names
    self.df = pd.DataFrame(rows)
    self.model = TableModel(self.df)
    self.table.setModel(self.model)
    self.df.columns = names
    self.df.index = range(1, len(rows)+1)
     
def show_authors(self, paperid):
    sql = "select name from authors A, paperauthors B where B.paperid="+str(paperid)+" and A.id=B.authorid"
    with self.conn:
        self.rows = SQLExecute(self, sql)
        names =""
        for row in self.rows:
            names = names + row[0] +"; "
        self.textBrowser_authors.setText(names)


 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()