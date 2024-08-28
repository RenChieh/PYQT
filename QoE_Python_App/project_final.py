from PyQt6 import QtWidgets, uic
import matplotlib.image as mpimg
import pyqtgraph as pg
import sys
import os
from PyQt6 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import numpy as np
import pandas as pd 
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
import pandas as pd



class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight # vertical + horizontal
 
        if role == Qt.ItemDataRole.BackgroundRole and index.column() / 1 != 0 and role == Qt.ItemDataRole.BackgroundRole and index.column() / 1 != 1: # change background color on even column
            return QtGui.QColor('#d8ffdb')
        

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section]) 
            
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('project2.ui', self)  

        #tab1       
        self.setWindowTitle('Cloud Gaming of Quality of Experience')

        self.tabWidget.setCurrentIndex(0)
        # file location
        self.file_src = "/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/0/"
        self.picName = os.listdir(self.file_src)
        self.picName.sort(key = lambda x:x.split('.')[0][16:50].replace('_','').replace('(','').replace(')','').replace('-',''))
        self.comboBox_ImgName.addItems(self.picName)

        self.showImg(0)
        self.first_pic(0)
        self.last_pic(0) 
        self.next_pic()
        self.previous_pic() 

        #tab2       
        #Add Background colour to white
        self.graphWidget_2.setBackground('w')
        # Add Axis Labels
        styles = {"color": "#000", "font-size": "15px"}
        self.graphWidget_2.setLabel("bottom", "file", **styles)
        #Add legend
        self.graphWidget_2.addLegend()
        #Add grid
        self.graphWidget_2.showGrid(x=True, y=True)       
        project_file = pd.read_csv("/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/project_file.csv")
        

        #tab3
        self.table = self.tableView_2
        data=pd.read_csv("/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/mos_user_file.csv")
        data = data.drop(['Unnamed: 0'],axis=1)

        # Signal1-1
        self.comboBox_ImgName.currentIndexChanged.connect(self.showImg)
        self.first_pushButton.clicked.connect(self.first_pic)
        self.pre_pushButton.clicked.connect(self.previous_pic)
        self.next_pushButton.clicked.connect(self.next_pic)
        self.last_pushButton.clicked.connect(self.last_pic) 
        self.pBut_exit.clicked.connect(self.close)

        # Signals1-2
        user_names = project_file['user'].unique()
        self.comboBox_user.addItems(user_names)
        self.comboBox_user.currentIndexChanged.connect(self.plot_data)     
        self.pushButton_update.clicked.connect(self.close)
        self.checkBox_Grid.stateChanged.connect(self.gridon)
        self.plot_data()

        #Signals1-3
        user_names = data['user'].unique()
        self.comboBox_user_3.addItems(user_names)
        self.comboBox_user_3.currentIndexChanged.connect(self.table_data)
        self.table_data()
        self.clear_button_2.clicked.connect(self.clear_table)
     
    # Slots1-1
    def first_pic(self, s):
        self.graphWidget.clear()
        img_dir = "/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/0/"      
        img_name = "Engine_Evolution_2022_(1871990)_10-13-22_21-27-50_Screenshot.png"
        image = mpimg.imread(img_dir + img_name)
        img_item = pg.ImageItem(image, axisOrder='row-major')        
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=False, ratio=0.5)
        self.label_cap.setText(img_name) # set Label text
        self.comboBox_ImgName.setCurrentIndex(0)
        

    def last_pic(self, s):
        self.graphWidget.clear()
        img_dir = "/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/0/"      
        img_name = "Engine_Evolution_2022_(1871990)_11-16-22_09-58-20_Screenshot.png"
        image = mpimg.imread(img_dir + img_name)
        img_item = pg.ImageItem(image, axisOrder='row-major')         
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=False, ratio=1)
        self.label_cap.setText(img_name) # set Label text
        self.comboBox_ImgName.setCurrentIndex(len(self.picName)-1)

    def next_pic(self):
        self.graphWidget.clear()
        # Get current index of the image name
        current_index = self.comboBox_ImgName.currentIndex()
        # Get the total number of images
        total_num_images = len(self.picName)
        # Calculate the index of the next image
        next_index = (current_index + 1) % total_num_images
        # Get the name of the next image
        next_image_name = self.picName[next_index]
        # Load the image and display it
        image = mpimg.imread(os.path.join(self.file_src, next_image_name))
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=False, ratio=1)
        self.label_cap.setText(next_image_name)
        # Set the current index of the image name to the next index
        self.comboBox_ImgName.setCurrentIndex(next_index)

    def previous_pic(self):
        # self.graphWidget.clear()
        # Get current index of the image name
        current_index = self.comboBox_ImgName.currentIndex()
        # Get the total number of images
        total_num_images = len(self.picName)
        # Calculate the index of the next image
        next_index = (current_index - 1) % total_num_images
        # Get the name of the next image
        next_image_name = self.picName[next_index]
        # Load the image and display it
        image = mpimg.imread(os.path.join(self.file_src, next_image_name))
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=False, ratio=1)
        self.label_cap.setText(next_image_name)
        # Set the current index of the image name to the next index
        self.comboBox_ImgName.setCurrentIndex(next_index)
 
       
    def showImg(self, s):
        self.graphWidget.clear()
        img_dir = "/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/0/"      
        img_name = self.comboBox_ImgName.currentText()
        image = mpimg.imread(img_dir + img_name)
        img_item = pg.ImageItem(image, axisOrder='row-major')         
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        self.label_cap.setText(img_name) # set Label text

    # Slots1-2
    def gridon(self, s):
        if s == 2: # 0 : unchecked; 2 : checked
            self.graphWidget_2.showGrid(x = True, y = True)   
        else:
            self.graphWidget_2.showGrid(x = False, y = False)

    def plot_data(self):
        self.graphWidget_2.clear()
        project_file = pd.read_csv("/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/project_file.csv")
        comboBox_name = self.comboBox_user.currentText() 
        # Add Title
        self.graphWidget_2.setTitle(comboBox_name, color="b", size="25pt")
        # Get selected user name
        user = project_file[project_file['user'].isin([comboBox_name])]
        # columns2 = ['Avg.pingTime','Avg.packetloss', 'Avg.FrameAge']
        x = range(len(user))
        y1 = user['Avg.pingTime'].values
        y2 = user['Avg.packetloss'].values
        y3 = user['Avg.FrameAge'].values
        
        self.graphWidget_2.plot(x, y1, pen=pg.mkPen(color='r', width=5),name='Avg.pingTime')
        self.graphWidget_2.plot(x, y2, pen=pg.mkPen(color='b', width=5),name='Avg.packetloss')
        self.graphWidget_2.plot(x, y3, pen=pg.mkPen(color='g', width=5),name='Avg.FrameAge')

        # Add Axis Labels
        styles = {"color": "#000", "font-size": "20px"}
        self.graphWidget_2.setLabel("bottom", "StreamVideoTrace.txt" , **styles)
        #Set Range
        self.graphWidget_2.setXRange(0, len(user), padding=0)

    # Slots1-3
    def table_data(self):
        comboBox_name = self.comboBox_user_3.currentText() 
        data=pd.read_csv("/Users/renjie/Desktop/github/PYQT/QoE_Python_App_final/mos_user_file.csv")
        data = data.drop(['Unnamed: 0'],axis=1)
        user = data[data['user'].isin([comboBox_name])]
        self.model = TableModel(user)
        self.table.setModel(self.model)
    def clear_table(self):
        self.table.setModel(None)
        
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()    
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()