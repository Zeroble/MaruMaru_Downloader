from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
mangaUrls = ""
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)
        Dialog.setMinimumSize(QtCore.QSize(700, 500))
        Dialog.setMaximumSize(QtCore.QSize(700, 500))
        Dialog.setWindowOpacity(1)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.Tagalog, QtCore.QLocale.Philippines))

        self.Search = QtWidgets.QPushButton(Dialog)
        self.Search.setGeometry(QtCore.QRect(620, 10, 70, 30))
        self.Search.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.Search.clicked.connect(self.StartSearch)

        self.magaName = QtWidgets.QLineEdit(Dialog)
        self.magaName.setGeometry(QtCore.QRect(95, 10, 515, 30))

        self.sText = QtWidgets.QLabel(Dialog)
        self.sText.setGeometry(QtCore.QRect(10, 0, 100, 50))

        self.fires = QtWidgets.QListWidget(Dialog)
        self.fires.setGeometry(QtCore.QRect(370, 50, 240, 420))

        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(620, 50, 70, 30))
        self.ok.clicked.connect(self.showFires)

        self.downlaod = QtWidgets.QPushButton(Dialog)
        self.downlaod.setGeometry(QtCore.QRect(620, 440, 70, 30))

        self.selectAll = QtWidgets.QPushButton(Dialog)
        self.selectAll.setGeometry(QtCore.QRect(620, 400, 70, 30))

        self.mangas = QtWidgets.QListWidget(Dialog)
        self.mangas.setGeometry(QtCore.QRect(10, 50, 350, 420))

        self.status = QtWidgets.QLabel(Dialog)
        self.status.setGeometry(QtCore.QRect(10, 470, 500, 30))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MaruMaru"))
        self.Search.setText(_translate("Dialog", "검색"))
        self.sText.setText(_translate("Dialog", "만화 제목 : "))
        self.ok.setText(_translate("Dialog", "확인"))
        self.downlaod.setText(_translate("Dialog", "다운로드"))
        self.selectAll.setText(_translate("Dialog", "전체 선택"))
        self.status.setText(_translate("Dialog", "준비"))

    def StartSearch(self):
        global mangaUrls
        URL = "http://marumaru.in/?r=home&mod=search&keyword=" + self.magaName.text()
        req = requests.get(URL)
        html = req.text
        searchData = BeautifulSoup(html, "html.parser")
        mangaUrls = searchData.select("a.subject")

        selectedData = searchData.select("div.sbjbox > b")
        self.mangas.clear()
        j = 0;
        for i in selectedData:
            j += 1
            self.mangas.addItem(str(j) + ". " + i.get_text())
        self.status.setText("검색완료!")

    def showFires(self):
        print(self.mangas.selectedItems())
        if self.mangas.selectedItems() == []:
            self.dialog = QtWidgets.QDialog()
            self.dialog.resize(300,100)
            self.dialog.setWindowTitle("경고")
            self.text = QtWidgets.QLabel("선택한 만화가 없습니다.",self.dialog).move(10,10)
            self.okbut = QtWidgets.QPushButton("확인", self.dialog)
            self.okbut.move(105, 60)
            self.okbut.clicked.connect(self.dialog.accept)
            self.dialog.exec()
        else:
            self.fires.clear()
            global mangaUrls
            print(self.mangas.currentRow()+1)
            self.status.setText(str(self.mangas.currentRow()+1)+"번 선택됨")
            URL = "http://marumaru.in" + mangaUrls[self.mangas.currentRow()].get('href')
            req = requests.get(URL)
            html = req.text


            mangafires = BeautifulSoup(html, "html.parser")
            #firesData = mangafires.select("div.content a")
            print(html+"\n\n\n")
            firesData = mangafires.find_all("a",{"target":"_blank"})
            print(firesData)
            j=0;
            for i in firesData:
                if i.get_text() == "":
                    del firesData[j]
                j+=1
            print("dfhjhgf")

            for i in firesData:
                print(i.get_text())
                self.fires.addItem(i.get_text())
  #          print("asdf")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

'''
class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # 윈도우 특성 설정
        self.setWindowTitle('MaruMaru Downloader')  # 윈도우 타이클 지정
        self.setGeometry(50, 80, 400, 500)  # 윈도우 위치/크기 설정
        #self.setWindowIcon(QIcon('umbrella.png'))  # 아이콘 지정
        self.statusBar().showMessage('준비')

        #글씨
        self.sText = QLabel("만화 제목 : ",self)
        self.sText.resize(240,50)
        self.sText.move(10,0)

        #검색창 추가
        self.search = QLineEdit("",self)
        self.search.resize(225,30)
        self.search.move(95,10)

        # 버튼1 추가
        self.btn1 = QPushButton('검색', self)
        #btn1.setToolTip('이 버튼을 누르면 <b>메시지 박스</b>가 나옴')
        self.btn1.resize(60,30)
        self.btn1.move(330, 10)
        self.btn1.clicked.connect(self.btnClicked)
        
        # 종료 버튼 추가
        self.btnQuit = QPushButton('종료', self)
        self.btnQuit.resize(10)
        self.btnQuit.move(50, 100)
        self.btnQuit.clicked.connect(QCoreApplication.instance().quit)
        
        # 윈도우 화면에 표시
        self.show()

    def btnClicked(self):
        QMessageBox.information(self, "버튼", "버튼 클릭!")


def main():
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    '''