# 축구 리그 관리 프로그램.
# 입력 팀의 수, 경기 수
# 출력이 총 경기 수, 승, 무, 패, 득실, 득실차, 승점.
# 만약 득실차랑 승점이 모두 같다면 가위바위보로 공정하게.     모두 gui로 구현.
# 시즌별로 팀 이름을 저장 시켜놓기.
# 시즌별로 경기 결과 볼 수 있게.

# 자료구조  필수
# 알고리즘  필수

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListView, QVBoxLayout, QWidget, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
from datetime import datetime
from mini_project_main import league_start, league_reload, statistics_before, statistics_next, statistics_search, index_files, file_count

# Import functions
start = league_start
reload = league_reload
before = statistics_before
next = statistics_next
search = statistics_search
in_file = index_files
count = file_count

index = 0
temp = 0

script_dir = os.path.dirname(os.path.abspath(__file__))

# UI 파일 연결
main_ui_path = os.path.join(script_dir, "main", "main.ui")
start_ui_path = os.path.join(script_dir, "main", "start.ui")
statistics_ui_path = os.path.join(script_dir, "main", "Statistics.ui")
error_ui_path = os.path.join(script_dir, "main", "error.ui")
error_2_ui_path = os.path.join(script_dir, "main", "error_2.ui")

form_class_main = uic.loadUiType(main_ui_path)[0]
from_class_start = uic.loadUiType(start_ui_path)[0]
from_class_statistics = uic.loadUiType(statistics_ui_path)[0]
from_class_error = uic.loadUiType(error_ui_path)[0]
from_class_error_2 = uic.loadUiType(error_2_ui_path)[0]
image_path = os.path.join(script_dir, "main", "Main.png")


# 화면을 띄우는데 사용되는 클래스 선언
class Main_UI(QMainWindow, form_class_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_images()
        self.Exit_Button.clicked.connect(self.exiteFunction)
        self.Start_Button.clicked.connect(self.startFunction)

    def set_images(self):
        label_width = self.Main_Pix.width()
        label_height = self.Main_Pix.height()
        pixmapMainPix = QPixmap(image_path)
        pixmapMainPix = pixmapMainPix.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.Main_Pix.setPixmap(pixmapMainPix)

    def exiteFunction(self):  # 프로그램 종료
        exit(0)

    def startFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Start_UI()  # start 창 표시
        self.new_window.show()  # start 창 표시

class Start_UI(QMainWindow, from_class_start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_images()
        self.Start_Button.clicked.connect(self.startFunction)
        self.Start_Button_2.clicked.connect(self.reloadFunction)
        self.Start_Button_3.clicked.connect(self.statusFunction)
        self.Start_Button_4.clicked.connect(self.backFunction)

    def set_images(self):
        label_width = self.Main_Pix.width()
        label_height = self.Main_Pix.height()
        pixmapStartPix = QPixmap(image_path)
        pixmapStartPix = pixmapStartPix.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.Main_Pix.setPixmap(pixmapStartPix)

    def startFunction(self):
        global temp
        if temp == 0:
            temp = 1
            start()
        elif temp == 1:
            self.new_window = Error_UI()  # 에러창 표시
            self.new_window.show()

    def reloadFunction(self):
        global temp
        temp = 0
        reload()

    def statusFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Statistics_UI()  # 통계창 표시
        self.new_window.show()  

    def backFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Main_UI()  # 이전 창 생성
        self.new_window.show()

class Statistics_UI(QMainWindow, from_class_statistics):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_images()
        self.Start_Button.clicked.connect(self.beforeFunction)
        self.Start_Button_2.clicked.connect(self.nextFunction)
        self.Start_Button_3.clicked.connect(self.backFunction)
        self.load_statistics()
        self.checkBox.stateChanged.connect(self.checkFunction)

    def set_images(self):
        label_width = self.Main_Pix.width()
        label_height = self.Main_Pix.height()
        pixmapStartPix = QPixmap(image_path)
        pixmapStartPix = pixmapStartPix.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.Main_Pix.setPixmap(pixmapStartPix)

    def beforeFunction(self):
        global index
        index += int(before())
        num = count()
        if index >= num :
            self.new_window = Error_UI_2()  # 에러창 표시
            self.new_window.show()
            index -= 1
        else :
            if self.checkBox.isChecked():
                self.checkFunction(Qt.Checked)
            else:  
                self.checkFunction(Qt.Unchecked)

    def nextFunction(self):
        global index
        index -= int(next())
        if index < 0 :
            self.new_window = Error_UI_2()  # 에러창 표시
            self.new_window.show()
            index += 1
        else :
            if self.checkBox.isChecked():
                self.checkFunction(Qt.Checked)
            else:
                self.checkFunction(Qt.Unchecked)

    def backFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Start_UI()  # 이전 창 생성
        self.new_window.show()

    def load_statistics(self):
        # UI 파일에 정의된 QListView 가져오기
        self.listView = self.listView

        # 데이터 모델 생성
        self.model = QStandardItemModel()

        # 텍스트 파일 경로 설정
        output_dir = os.path.join(script_dir, "league")
        txt_files = index_files()

        if txt_files:
            # 가장 최신 파일 읽기
            latest_file = txt_files[index]
            file_path = os.path.join(output_dir, latest_file)

        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        item = QStandardItem(line.strip())
                        font = QFont()
                        font.setPointSizeF(14)  # 글씨 크기 설정
                        item.setFont(font)
                        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # 읽기 전용으로 설정
                        self.model.appendRow(item)
            except Exception as e:
                print(f"Error reading file: {e}")

        # 모델을 QListView에 설정
        self.listView.setModel(self.model)
    
    def checkFunction(self, state) :
        if state == Qt.Checked:
            sort_index = search()
            # UI 파일에 정의된 QListView 가져오기
            self.listView = self.listView

            # 데이터 모델 생성
            self.model = QStandardItemModel()

            output_dir = os.path.join(script_dir, "league")
            txt_files = in_file()

            if txt_files:
                last_integer = []
                # 가장 최신 파일 읽기
                latest_file = txt_files[index]
                file_path = os.path.join(output_dir, latest_file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    for i in sort_index :
                        item = QStandardItem(lines[i].strip())
                        font = QFont()
                        font.setPointSizeF(14)  # 글씨 크기 설정
                        item.setFont(font)
                        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # 읽기 전용으로 설정
                        self.model.appendRow(item)
                        
                except Exception as e:
                    print(f"Error reading file: {e}")

            self.listView.setModel(self.model)
            
        else :
            self.load_statistics()

class Error_UI(QMainWindow, from_class_error):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.error_Button.clicked.connect(self.errorFunction)

    def errorFunction(self):
        self.close()  # 현재 창 닫기

class Error_UI_2(QMainWindow, from_class_error_2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.error2_Button.clicked.connect(self.error2Function)

    def error2Function(self):
        self.close()

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = Main_UI()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트 루프로 진입시키는(프로그램을 작동시키는) 코드
    sys.exit(app.exec_())