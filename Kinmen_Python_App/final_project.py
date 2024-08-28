from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6 import QtWidgets, uic
import folium # pip install folium
import sys
import io
from bs4 import BeautifulSoup

from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pandas as pd
import requests
import os

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

"""
Folium in PyQt6
"""

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:          
            # return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
        
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#ffffbf')

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

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        uic.loadUi('final_project.ui', self)
        self.setWindowTitle('金門好好玩')

        #Map
        c1 = (24.432630, 118.317780) # 邱良功古厝
        c2 = (24.431530, 118.317730) # 陳詩吟洋樓
        c3 = (24.434540, 118.317280) # 朱子祠
        c4 = (24.478300, 118.410670) # 黃偉墓
        c5 = (24.487060, 118.414710) # 黃宣顯六路大厝
        c6 = (24.424970, 118.319000) # 莒光樓
        c7 = (24.431330, 118.317800) # 奎閣(魁星樓)
        c8 = (24.454440, 118.373990) # 瓊林蔡氏家廟
        c9 = (24.432300, 118.318410) # 清金門鎮總兵署
        c10 = (24.422280, 118.229580) # 吳秀才厝
        

        c11 = (24.486020, 118.412510) # 慈德宮
        c12 = (24.431410, 118.318520) # 邱良功母節孝坊
        c13 = (24.433070, 118.318100) # 將軍第
        c14 = (24.398390, 118.305620) # 虛江嘯臥碣群
        c15 = (24.481110, 118.430260) # 陳禎恩榮坊
        c16 = (24.462640, 118.418550) # 海印寺
        c17 = (24.449890, 118.385930) # 邱良功墓園
        c18 = (24.420730, 118.322390) # 豐蓮山牧馬侯祠
        c19 = (24.398790, 118.306000) # 文臺寶塔
        c20 = (24.393820, 118.312640) # 漢影雲根碣

        c21 = (24.453920, 118.370400) # 瓊林一門三節坊
        c22 = (24.462800, 118.417830) # 石門關
        c23 = (24.485640, 118.441120) # 睿友學校
        c24 = (24.456920, 118.306130) # 楊華故居
        c25 = (24.462850, 118.444440) # 金門縣林務所
        c26 = (24.427010, 118.223740) # 貴山海灘
        c27 = (24.442610, 118.468500) # 溪邊海水浴場
        c28 = (24.428610, 118.226250) # 上林海灘
        c29 = (24.452640, 118.248600) # 貓公石濱海休憩區
        c30 = (24.403350, 118.308050) # 金門城

        c31 = (24.408610, 118.288340) # 茅山塔
        c32 = (24.438450, 118.235140) # 國姓井
        c33 = (24.436760, 118.239780) # 北風爺、風雞
        c34 = (24.478840, 118.307590) # 三眼井
        c35 = (24.415100, 118.288880) # 吳稚暉紀念公園
        c36 = (24.409340, 118.297900) # 金水國小
        c37 = (24.507050, 118.405310) # 西園鹽場
        c38 = (24.435070, 118.314070) # 金門高中中正堂
        c39 = (24.427520, 118.249450) # 東林東井
        c40 = (24.413130, 118.327010) # 小西門模範廁

        c41 = (24.471920, 118.293000) # 南山林道
        c42 = (24.447730, 118.466550) # 復國墩觀景台
        c43 = (24.403710, 118.308830) # 明遺老街
        c44 = (24.460510, 118.410160) # 石兔
        c45 = (24.459300, 118.409790) # 劉玉章雕像
        c46 = (24.399320, 118.305820) # 葉華成故居
        c47 = (24.458210, 118.405190) # 玉章路牌坊
        c48 = (24.463520, 118.410150) # 斗門古道
        c49 = (24.459860, 118.382220) # 欽旌節牌坊
        c50 = (24.451100, 118.389750) # 無愧亭

        c51 = (24.462710, 118.414120) # 倒影塔
        c52 = (24.499630, 118.434610) # 五虎山
        c53 = (24.436320, 118.389820) # 擎天山莊公園
        c54 = (24.417490, 118.433500) # 料羅海濱公園
        c55 = (24.412650, 118.434400) # 金門媽祖公園
        c56 = (24.416930, 118.344330) # 后湖海濱公園
        c57 = (24.425080, 118.251770) # 東林海濱公園
        c58 = (24.436960, 118.370360) # 環保公園低碳教育館
        c59 = (24.436610, 118.426710) # 中正公園
        c60 = (24.427310, 118.315620) # 金門石雕公園

        c61 = (24.429080, 118.317650) # 莒光公園
        c62 = (24.411490, 118.438460) # 南石滬公園
        c63 = (24.462690, 118.413970) # 鄭成功觀兵奕棋處
        c64 = (24.463540, 118.416710) # 梅園
        c65 = (24.465720, 118.421860) # 頑石點頭勒石群
        c66 = (24.441320, 118.430150) # 中正紀念林
        c67 = (24.394270, 118.315580) # 古崗樓
        c68 = (24.443930, 118.432010) # 榕園
        c69 = (24.457020, 118.404330) # 太武山風景區
        c70 = (24.493300, 118.443020) # 楓香林

        c71 = (24.485940, 118.411600) # 榮湖
        c72 = (24.487820, 118.407840) # 金沙水庫
        c73 = (24.459210, 118.431760) # 陽明湖
        c74 = (24.452000, 118.382900) # 蘭湖
        c75 = (24.439820, 118.426290) # 太湖遊憩區
        c76 = (24.468970, 118.306750) # 慈湖
        c77 = (24.477520, 118.310300) # 雙鯉湖/雙鯉溼地中心
        c78 = (24.423020, 118.225210) # 陵水湖
        c79 = (24.395950, 118.314710) # 古崗湖風景區
        c80 = (24.427390, 118.316470) # 莒光湖

        
        c81 = (24.401480, 118.320580) # 珠山聚落
        c82 = (24.411470, 118.299960) # 水頭聚落
        c83 = (24.463640, 118.416110) # 毋忘在莒
        c84 = (24.455140, 118.373070) # 瓊林民防館
        c85 = (24.464790, 118.436690) # 八二三戰役勝利紀念碑
        c86 = (24.446110, 118.231120) # 湖井頭戰史館
        c87 = (24.476520, 118.315420) # 古寧頭牌樓
        c88 = (24.429980, 118.245730) # 八達樓子
        c89 = (24.426990, 118.258660) # 勝利門
        c90 = (24.427020, 118.258870) # 八二三砲戰勝利紀念碑

        c91 = (24.443040, 118.431530) # 俞大維先生紀念館
        c92 = (24.437110, 118.352480) # 乳山故壘
        c93 = (24.488900, 118.314200) # 北山斷崖
        c94 = (24.527710, 118.408870) # 馬山觀測所
        c95 = (24.456240, 118.304550) # 湖下三間樓仔
        c96 = (24.485670, 118.440320) # 陳德幸洋樓
        c97 = (24.409670, 118.298880) # 水頭57地號洋樓(僑鄉文化展示館)
        c98 = (24.402630, 118.320690) # 薛永南兄弟大樓
        c99 = (24.437270, 118.390090) # 陳景蘭洋樓
        c100 = (24.479210, 118.312560) # 北山古洋樓

        self.loc_coordinate = {"邱良功古厝":c1,"陳詩吟洋樓":c2,"朱子祠":c3,"黃偉墓":c4,"黃宣顯六路大厝":c5,"莒光樓":c6,"奎閣(魁星樓)":c7,"瓊林蔡氏家廟":c8,"清金門鎮總兵署":c9,"吳秀才厝":c10, \
                               "慈德宮":c11,"邱良功母節孝坊":c12,"將軍第":c13,"虛江嘯臥碣群":c14,"陳禎恩榮坊":c15,"海印寺":c16,"邱良功墓園":c17,"豐蓮山牧馬侯祠":c18,"文臺寶塔":c19,"漢影雲根碣":c20, \
                               "瓊林一門三節坊":c21,"石門關":c22,"睿友學校":c23,"楊華故居":c24,"金門縣林務所":c25,"貴山海灘":c26,"溪邊海水浴場":c27,"上林海灘":c28,"貓公石濱海休憩區":c29,"金門城":c30, \
                               "茅山塔":c31,"國姓井":c32,"北風爺、風雞":c33,"三眼井":c34,"吳稚暉紀念公園":c35,"金水國小":c36,"西園鹽場":c37,"金門高中中正堂":c38,"東林東井":c39,"小西門模範廁":c40, \
                               "南山林道":c41,"復國墩觀景台":c42,"明遺老街":c43,"石兔":c44,"劉玉章雕像":c45,"葉華成故居":c46,"玉章路牌坊":c47,"斗門古道":c48,"欽旌節牌坊":c49,"無愧亭":c50, \
                               "倒影塔":c51,"五虎山":c52,"擎天山莊公園":c53,"料羅海濱公園":c54,"金門媽祖公園":c55,"后湖海濱公園":c56,"東林海濱公園":c57,"環保公園低碳教育館":c58,"中正公園":c59,"金門石雕公園":c60, \
                               "莒光公園":c61,"南石滬公園":c62,"鄭成功觀兵奕棋處":c63,"梅園":c64,"頑石點頭勒石群":c65,"中正紀念林":c66,"古崗樓":c67,"榕園":c68,"太武山風景區":c69,"楓香林":c70, \
                               "榮湖":c71,"金沙水庫":c72,"陽明湖":c73,"蘭湖":c74,"太湖遊憩區":c75,"慈湖":c76,"雙鯉湖/雙鯉溼地中心":c77,"陵水湖":c78,"古崗湖風景區":c79,"莒光湖":c80, \
                               "珠山聚落":c81,"水頭聚落":c82,"毋忘在莒":c83,"瓊林民防館":c84,"八二三戰役勝利紀念碑":c85,"湖井頭戰史館":c86,"古寧頭牌樓":c87,"八達樓子":c88,"勝利門":c89,"八二三砲戰勝利紀念碑":c90, \
                               "俞大維先生紀念館":c91,"乳山故壘":c92,"北山斷崖":c93,"馬山觀測所":c94,"湖下三間樓仔":c95,"陳德幸洋樓":c96,"水頭57地號洋樓(僑鄉文化展示館)":c97,"薛永南兄弟大樓":c98,"陳景蘭洋樓":c99,"北山古洋樓":c100
                               }

        loc = self.comboBox_campus.currentText()
        self.show_map(self.loc_coordinate[loc])

        # Map signals
        self.comboBox_campus.currentIndexChanged.connect(self.which_campus)

        #Food
        self.newsSearch()
        page = ['廣東粥','石蚵料理','牛肉麵','鍋貼','金門宴菜','燒餅','油炸粿(油條)','炒泡麵','酒釀蛋','芋頭冰']  
        self.comboBox_title.addItems(page)
        self.showImg(0)
        self.file_src = "/Users/renjie/Desktop/github/PYQT/Kinmen_Python_App/image/"
        self.picName = os.listdir(self.file_src)
        
        #Food Signals
        self.comboBox_title.currentIndexChanged.connect(self.newsSearch)
        self.comboBox_title.currentIndexChanged.connect(self.showImg)
        self.pre_pushButton.clicked.connect(self.previous_pic)
        self.next_pushButton.clicked.connect(self.next_pic)


        #view
        self.tableSearch()
        
        # view Signals
        self.tableView.doubleClicked.connect(self.rowSelected)
        self.comboBox_page.currentIndexChanged.connect(self.tableSearch)
        self.p_But_nextpage.clicked.connect(self.nextpage)
        self.p_But_prepage.clicked.connect(self.prepage)

        #Map slot
    def show_map(self, coordinate):
        m = folium.Map(
        	tiles='Stamen Terrain',
        	zoom_start=13,
        	location=coordinate
        )  # tiles = Stamen Toner, CartoDB positron, Cartodb dark_matter, Stamen Watercolor or Stamen Terrain
        # save map data to data object
        data = io.BytesIO()
        # folium.Marker(location = coordinate).add_to(m)
        # folium.CircleMarker(location = coordinate, \
        #             radius = 50, popup = ' FRI ').add_to(m)
        folium.CircleMarker(location = coordinate, \
                    radius = 20, fill_color='red').add_to(m)

        m.save(data, close_file = False)

        webView = QWebEngineView()  # a QWidget
        webView.setHtml(data.getvalue().decode())

        # clear the current widget in the verticalLayout before adding one
        if self.verticalLayout.itemAt(0) : # if any existing widget
            self.verticalLayout.itemAt(0).widget().setParent(None)
        # add a widget with webview inside the vertivalLayout component
        self.verticalLayout.addWidget(webView, 0) # at position 0
    
    def which_campus(self):
        loc = self.comboBox_campus.currentText()
        self.show_map(self.loc_coordinate[loc])
    #food slot
    def newsSearch(self):
        url = "https://kinmen.travel/zh-tw/shop/cuisines"
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, "html.parser")
        self.titleSearch()  
 

    def titleSearch(self):
        self.description.setWordWrap(True)  # 自動換行
        url = "https://kinmen.travel/zh-tw/shop/cuisines"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find_all("p", class_="article-text2", limit=10)
        index = self.comboBox_title.currentIndex()
        

        if index < len(content):
            description = content[index].text
            self.description.setText(description)
            
        else:
            self.description.setText("No description available.")


    def showImg(self, s):
        # img_name = self.comboBox_title.currentText()
        img_num=self.comboBox_title.currentIndex()
        img_dir="/Users/renjie/Desktop/github/PYQT/Kinmen_Python_App/image/"+str(img_num)+".jpg"
        self.img.setPixmap(QPixmap(img_dir))

    def next_pic(self):
        current_index = self.comboBox_title.currentIndex()
        total_num_images = 10
        next_index = (current_index + 1) % total_num_images
        next_image_name = self.picName[next_index]
        img_dir="/Users/renjie/Desktop/github/PYQT/Kinmen_Python_App/image/"+next_image_name
        self.img.setPixmap(QPixmap(img_dir))
        self.comboBox_title.setCurrentIndex(next_index)
    def previous_pic(self):
        current_index = self.comboBox_title.currentIndex()
        total_num_images = 10
        next_index = (current_index - 1) % total_num_images
        next_image_name = self.picName[next_index]
        img_dir="/Users/renjie/Desktop/github/PYQT/Kinmen_Python_App/image/"+next_image_name
        self.img.setPixmap(QPixmap(img_dir))
        self.comboBox_title.setCurrentIndex(next_index)


    #view slot
    # Slots
    def tableSearch(self):
        path = "/Users/renjie/Desktop/github/PYQT/Kinmen_Python_App/AttractionList.csv"
        df = pd.read_csv(path) 
        user=df[['Name','Tel','Add']].iloc[834:934]       
        user = user.reset_index()    #恢復原本設置
        self.df  = user.drop(['index'],axis=1)
        self.df=self.df.rename(columns={'Name': '景點名稱','Tel': '聯絡電話','Add': '地址'})
        page=int(self.comboBox_page.currentText())
        start_idx =(page-1)*15
        end_idx=start_idx+15
        data =self.df.iloc[start_idx:end_idx, :]
        self.model = TableModel(data)
        self.tableView.setModel(self.model)  
        self.tableView.setColumnWidth(0, 120)
        self.tableView.setColumnWidth(1, 120)
        self.tableView.setColumnWidth(2, 285)

    def nextpage(self):       
        page=int(self.comboBox_page.currentText())
        start_idx =(page)*15
        end_idx=start_idx+15
        data =self.df.iloc[start_idx:end_idx, :]
        self.model=TableModel(data)
        self.tableView.setModel(self.model)
        page=self.comboBox_page.setCurrentText(str(int(self.comboBox_page.currentText())+1))

    def prepage(self):       
        page=int(self.comboBox_page.currentText())
        start_idx =(page)*15
        end_idx=start_idx+15
        data =self.df.iloc[start_idx:end_idx, :]
        self.model=TableModel(data)
        self.tableView.setModel(self.model)
        page=self.comboBox_page.setCurrentText(str(int(self.comboBox_page.currentText())-1)) 
        
        
    def rowSelected(self, mi):
        current_page = self.comboBox_page.currentIndex()
        idx = current_page *15 + mi.row()      
        file_path = '/Users/renjie/Desktop/github/PYQT/Kinmen_Python_App/AttractionList.csv'
        df = pd.read_csv(file_path)       
        user=df[['Toldescribe']].iloc[834:934]       
        user = user.reset_index()    #恢復原本設置
        self.df = user.drop(['index'],axis=1)  
        self.df=self.df.rename(columns={'Name': '景點名稱','Tel': '聯絡電話','Add': '地址'})
        self.textBrowser_summary.setText(user['Toldescribe'].iloc[idx])
        
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()