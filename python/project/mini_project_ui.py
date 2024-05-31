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
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont, QIcon
from PyQt5.QtCore import Qt, QCoreApplication, QUrl
from PyQt5 import uic, QtWidgets, QtGui, QtCore
import os
from datetime import datetime
from mini_project_main import*
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# Import functions
start = league_start
reload = league_reload
before = statistics_before
next = statistics_next
search = statistics_search
in_file = index_files
count = file_count
search_data = file_search

index = 0
temp = 0

script_dir = os.path.dirname(os.path.abspath(__file__))

# UI 파일 연결
main_ui_path = os.path.join(script_dir, "main", "main.ui")
start_ui_path = os.path.join(script_dir, "main", "start.ui")
statistics_ui_path = os.path.join(script_dir, "main", "Statistics.ui")
error_ui_path = os.path.join(script_dir, "main", "error.ui")
error_2_ui_path = os.path.join(script_dir, "main", "error_2.ui")
error_3_ui_path = os.path.join(script_dir, "main", "error_3.ui")
error_5_ui_path = os.path.join(script_dir, "main", "error_5.ui")
error_6_ui_path = os.path.join(script_dir, "main", "error_6.ui")

form_class_main = uic.loadUiType(main_ui_path)[0]
from_class_start = uic.loadUiType(start_ui_path)[0]
from_class_statistics = uic.loadUiType(statistics_ui_path)[0]
from_class_error = uic.loadUiType(error_ui_path)[0]
from_class_error_2 = uic.loadUiType(error_2_ui_path)[0]
from_class_error_3 = uic.loadUiType(error_3_ui_path)[0]
from_class_error_5 = uic.loadUiType(error_5_ui_path)[0]
from_class_error_6 = uic.loadUiType(error_6_ui_path)[0]
image_path = os.path.join(script_dir, "main", "Main.png")

# 음악 파일 경로 설정
music_file = os.path.join(script_dir, "sound", "pro_sound.mp3").replace("\\", "/")


# 화면을 띄우는데 사용되는 클래스 선언
class Main_UI(QMainWindow, form_class_main):
    def __init__(self, checkbox_state=None):
        super().__init__()
        self.setupUi(self)
        self.set_images()
        self.Exit_Button.clicked.connect(self.exiteFunction)
        self.Start_Button.clicked.connect(self.startFunction)
        self.bgmBox.stateChanged.connect(self.bgmFunction)
        self.bgm_player = QMediaPlayer()  # BGM 재생을 위한 MediaPlayer 설정
        if checkbox_state is not None:  # checkbox_state가 None이 아닌 경우에만 실행
            self.bgm_state = checkbox_state
            if self.bgm_state:
                self.bgmBox.setChecked(True)
        else:
            self.bgm_state = False  # checkbox_state가 None이면 False로 설정
            self.play_bgm()

    def set_images(self):
        label_width = self.Main_Pix.width()
        label_height = self.Main_Pix.height()
        pixmapMainPix = QPixmap(image_path)
        pixmapMainPix = pixmapMainPix.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.Main_Pix.setPixmap(pixmapMainPix)

    def exiteFunction(self):  # 프로그램 종료
        self.bgm_player.stop()  # 프로그램 종료 시 BGM 정지
        exit(0)

    def startFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Start_UI(self.bgm_state)  # start 창 표시
        self.new_window.show()  # start 창 표시

    def play_bgm(self):
        bgm_content = QMediaContent(QUrl.fromLocalFile(music_file))
        self.bgm_player.setMedia(bgm_content)
        self.bgm_player.setVolume(80)  # 볼륨 조절 (0~100)
        # self.bgm_player.setLoopCount(-1)  # 무한 반복 설정
        self.bgm_player.play()  # BGM 재생

    # def play_bgm(self):
    #     bgm_content = QMediaContent(QUrl.fromLocalFile(music_file))
    #     playlist = QMediaPlaylist()
    #     playlist.addMedia(bgm_content)
    #     playlist.setPlaybackMode(QMediaPlaylist.Loop)  # 반복 재생 설정

    #     self.bgm_player.setPlaylist(playlist)
    #     self.bgm_player.setVolume(80)  # 볼륨 조절 (0~100)
    #     self.bgm_player.play()  # BGM 재생

    def bgmFunction(self, state) :
        if state == Qt.Checked:
            self.bgm_player.stop()
            self.bgm_state = True
        else :
            self.play_bgm()
            self.bgm_state = False


class Start_UI(QMainWindow, from_class_start):
    def __init__(self, checkbox_state):
        super().__init__()
        self.setupUi(self)
        self.set_images()
        if temp == 1 :
            self.loadview()
        self.Start_Button.clicked.connect(self.startFunction)
        self.Start_Button_2.clicked.connect(self.reloadFunction)
        self.Start_Button_3.clicked.connect(self.statusFunction)
        self.Start_Button_4.clicked.connect(self.backFunction)
        self.bgmBox.stateChanged.connect(self.bgmFunction)
        self.bgm_state = checkbox_state
        self.bgm_player = QMediaPlayer() # BGM 재생을 위한 MediaPlayer 설정
        if self.bgm_state:
            self.bgmBox.setChecked(True)

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
            self.close()
            self.new_window = Start_UI(self.bgm_state)
            self.new_window.show()
        elif temp == 1:
            self.new_window = Error_UI()  # 에러창 표시
            self.new_window.show()
    
    def loadview(self):
        infor = search_data(0)
        
        if infor is not None:
            for i, data in enumerate(infor, start=1):    
                listView_win = self.findChild(QtWidgets.QListView, f"listView_win_{i}")
                listView_lose = self.findChild(QtWidgets.QListView, f"listView_lose_{i}")
                listView_draw = self.findChild(QtWidgets.QListView, f"listView_draw_{i}")
                listView_gf = self.findChild(QtWidgets.QListView, f"listView_gf_{i}")
                listView_ga = self.findChild(QtWidgets.QListView, f"listView_ga_{i}")
                listView_gd = self.findChild(QtWidgets.QListView, f"listView_gd_{i}")
                listView_points = self.findChild(QtWidgets.QListView, f"listView_points_{i}")
                            
                # 모든 위젯을 찾을 수 있는 경우에만 모델을 설정
                if all(widget is not None for widget in [listView_win, listView_lose, listView_draw, 
                                                        listView_gf, listView_ga, listView_gd, listView_points]):
                    model_win = QtGui.QStandardItemModel()
                    model_lose = QtGui.QStandardItemModel()
                    model_draw = QtGui.QStandardItemModel()
                    model_gf = QtGui.QStandardItemModel()
                    model_ga = QtGui.QStandardItemModel()
                    model_gd = QtGui.QStandardItemModel()
                    model_points = QtGui.QStandardItemModel()
                    
                    # 글씨 설정
                    def create_standard_item(text):
                        item = QtGui.QStandardItem(str(text))
                        item.setEditable(False)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        font = item.font()
                        font.setPointSize(12)  # 글씨 크기
                        item.setFont(font)
                        return item
                    
                    # data는 각 팀의 정보를 담은 리스트라고 가정
                    model_win.appendRow(create_standard_item(data[0]))
                    model_lose.appendRow(create_standard_item(data[1]))
                    model_draw.appendRow(create_standard_item(data[2]))
                    model_gf.appendRow(create_standard_item(data[3]))
                    model_ga.appendRow(create_standard_item(data[4]))
                    model_gd.appendRow(create_standard_item(data[5]))
                    model_points.appendRow(create_standard_item(data[6]))
                    
                    listView_win.setModel(model_win)
                    listView_lose.setModel(model_lose)
                    listView_draw.setModel(model_draw)
                    listView_gf.setModel(model_gf)
                    listView_ga.setModel(model_ga)
                    listView_gd.setModel(model_gd)
                    listView_points.setModel(model_points)
        else:
            print("No data found.")

    def reloadFunction(self):
        global temp
        if temp == 0 :
            self.new_window = Error_UI_6()
            self.new_window.show()
        else :
            temp = 0
            reload()
            self.close()
            self.new_window = Start_UI(self.bgm_state)
            self.new_window.show()
            self.new_window_1 = Error_UI_5()
            self.new_window_1.show()


    def statusFunction(self):
        if count() == 0 :
            self.new_window = Error_UI_3()  # 에러창 표시
            self.new_window.show()
        else :
            self.close()  # 현재 창 닫기
            self.new_window = Statistics_UI(self.bgm_state)  # 통계창 표시
            self.new_window.show()  

    def backFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Main_UI(self.bgm_state)  # 이전 창 생성
        self.new_window.show()

    def play_bgm(self):
        bgm_content = QMediaContent(QUrl.fromLocalFile(music_file))
        self.bgm_player.setMedia(bgm_content)
        self.bgm_player.setVolume(80)  # 볼륨 조절 (0~100)
        # self.bgm_player.setLoopCount(-1)  # 무한 반복 설정
        self.bgm_player.play()  # BGM 재생

    def bgmFunction(self, state):
        if state == Qt.Checked:
            self.bgm_player.stop()
            self.bgm_state = True
        else:
            self.play_bgm()
            self.bgm_state = False 

class Statistics_UI(QMainWindow, from_class_statistics):#
    def __init__(self, checkbox_state):
        super().__init__()
        self.setupUi(self)
        self.set_images()
        self.Start_Button.clicked.connect(self.beforeFunction)
        self.Start_Button_2.clicked.connect(self.nextFunction)
        self.Start_Button_3.clicked.connect(self.backFunction)
        self.loadview(0)
        self.bgmBox.stateChanged.connect(self.bgmFunction)
        self.bgm_player = QMediaPlayer() # BGM 재생을 위한 MediaPlayer 설정
        self.bgm_state = checkbox_state
        if self.bgm_state:
            self.bgmBox.setChecked(True)  # 이전 UI에서 체크된 상태라면 체크박스를 체크함
        

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
        if index >= num:
            self.new_window = Error_UI_2()  # 에러창 표시
            self.new_window.show()
            index -= 1
        else:
            self.loadview(index)

    def nextFunction(self):
        global index
        index -= int(next())
        if index < 0 :
            self.new_window = Error_UI_2()  # 에러창 표시
            self.new_window.show()
            index += 1
        else :
            self.loadview(index)

    def backFunction(self):
        self.close()  # 현재 창 닫기
        self.new_window = Start_UI(self.bgm_state)  # 이전 창 생성
        self.new_window.show()

    def loadview(self, index):

        infor = search_data(index)
        
        if infor is not None:
            for i, data in enumerate(infor, start=1):    
                listView_win = self.findChild(QtWidgets.QListView, f"listView_win_{i}")
                listView_lose = self.findChild(QtWidgets.QListView, f"listView_lose_{i}")
                listView_draw = self.findChild(QtWidgets.QListView, f"listView_draw_{i}")
                listView_gf = self.findChild(QtWidgets.QListView, f"listView_gf_{i}")
                listView_ga = self.findChild(QtWidgets.QListView, f"listView_ga_{i}")
                listView_gd = self.findChild(QtWidgets.QListView, f"listView_gd_{i}")
                listView_points = self.findChild(QtWidgets.QListView, f"listView_points_{i}")
                            
                # 모든 위젯을 찾을 수 있는 경우에만 모델을 설정
                if all(widget is not None for widget in [listView_win, listView_lose, listView_draw, 
                                                        listView_gf, listView_ga, listView_gd, listView_points]):
                    model_win = QtGui.QStandardItemModel()
                    model_lose = QtGui.QStandardItemModel()
                    model_draw = QtGui.QStandardItemModel()
                    model_gf = QtGui.QStandardItemModel()
                    model_ga = QtGui.QStandardItemModel()
                    model_gd = QtGui.QStandardItemModel()
                    model_points = QtGui.QStandardItemModel()
                    
                    # 글씨 설정
                    def create_standard_item(text):
                        item = QtGui.QStandardItem(str(text))
                        item.setEditable(False)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        font = item.font()
                        font.setPointSize(12)  # 글씨 크기
                        item.setFont(font)
                        return item
                    
                    # data는 각 팀의 정보를 담은 리스트라고 가정
                    model_win.appendRow(create_standard_item(data[0]))
                    model_lose.appendRow(create_standard_item(data[1]))
                    model_draw.appendRow(create_standard_item(data[2]))
                    model_gf.appendRow(create_standard_item(data[3]))
                    model_ga.appendRow(create_standard_item(data[4]))
                    model_gd.appendRow(create_standard_item(data[5]))
                    model_points.appendRow(create_standard_item(data[6]))
                    
                    listView_win.setModel(model_win)
                    listView_lose.setModel(model_lose)
                    listView_draw.setModel(model_draw)
                    listView_gf.setModel(model_gf)
                    listView_ga.setModel(model_ga)
                    listView_gd.setModel(model_gd)
                    listView_points.setModel(model_points)
        else:
            print("No data found.")
    
    def play_bgm(self):
        bgm_content = QMediaContent(QUrl.fromLocalFile(music_file))
        self.bgm_player.setMedia(bgm_content)
        self.bgm_player.setVolume(80)  # 볼륨 조절 (0~100)
        # self.bgm_player.setLoopCount(-1)  # 무한 반복 설정
        self.bgm_player.play()  # BGM 재생

    def bgmFunction(self, state):
        if state == Qt.Checked:
            self.bgm_player.stop()
            self.bgm_state = True
        else:
            self.play_bgm()
            self.bgm_state = False 

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

class Error_UI_3(QMainWindow, from_class_error_3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.error3_Button.clicked.connect(self.error3Function)

    def error3Function(self):
        self.close()

class Error_UI_5(QMainWindow, from_class_error_5):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.error5_Button.clicked.connect(self.error5Function)

    def error5Function(self):
        self.close()

class Error_UI_6(QMainWindow, from_class_error_6):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.error6_Button.clicked.connect(self.error6Function)

    def error6Function(self):
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