from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from style import combo_style, date_edit_style, calendar_style
from download import obs_list, gen_text
from datetime import datetime as dt, timedelta

class TideProcessingApp(QWidget):
    """
    바다 해양누리집 자료 처리 프로그램 UI
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.now = dt.now().strftime("%Y-%m-%d")

        self.setWindowTitle("실시간 조위 처리")
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(400,400, 500, 400)
        self.setFixedSize(500,400)
        self.setStyleSheet("background-color: #f0f0f0;")  # 연한 회색 배경
        
        # ✅ 둥근 모서리를 가진 흰색 배경 프레임
        bg_frame = QFrame(self)
        bg_frame.setStyleSheet("""
            background-color: white;
            border-radius: 20px; /* 모서리를 둥글게 */
        """)
        bg_frame.setGeometry(20, 20, 460, 360)  # 부모 위젯에서 여백을 두고 배치

        # ✅ 메인 레이아웃
        main_layout = QVBoxLayout(bg_frame)  # bg_frame에 레이아웃 적용

        # ✅ 개별 프레임 (레이아웃 포함)
        frame_1 = QFrame();empty = QFrame()
        frame_2 = QFrame(); frame_3 = QFrame()
        frame_4 = QFrame(); frame_5 = QFrame()
        frame_6 = QFrame(); frame_7 = QFrame()

        title_layout = QVBoxLayout(); obs_layout = QVBoxLayout(); use_layout = QVBoxLayout(); notend_layout=QHBoxLayout()
        str_layout = QVBoxLayout(); end_layout = QVBoxLayout(); setbtn_layout = QVBoxLayout(); chkbtn_layout = QVBoxLayout()

        # title
        title_label = QLabel("실시간 조위 처리 프로그램입니다 😊")
        title_label.setFont(QFont("한컴산뜻돋움", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0,0,0,0)
        title_layout.addWidget(title_label)

        # obs
        obs_label = QLabel("조위관측소")
        obs_label.setFont(QFont("한컴산뜻돋움", 12, QFont.Bold))
        obs_label.setAlignment(Qt.AlignLeft)
        
        self.fin_selected_obs = "가덕도"
        self.combo_station = QComboBox()
        observation_name = obs_list()["observation_name"]
        for obs_name in observation_name:
            self.combo_station.addItem(obs_name)  
        self.combo_station.setStyleSheet(combo_style)
        self.combo_station.setView(QListView()) 
        self.combo_station.view().setStyleSheet("QListView::item { min-height: 35px; }")
        self.combo_station.setFixedSize(200, 30) 
        obs_layout.addWidget(obs_label)
        obs_layout.addWidget(self.combo_station)

        # use
        use_label = QLabel("용도")
        use_label.setFont(QFont("한컴산뜻돋움", 12, QFont.Bold))
        use_label.setAlignment(Qt.AlignLeft)

        self.fin_selected_use = "CARIS"
        self.combo_use = QComboBox()
        self.combo_use.addItems(["CARIS", "TIDEBED"])
        self.combo_use.setStyleSheet(combo_style)
        self.combo_use.setView(QListView()) 
        self.combo_use.view().setStyleSheet("QListView::item { min-height: 35px; }")
        self.combo_use.setFixedSize(200, 30)  
        use_layout.addWidget(use_label)
        use_layout.addWidget(self.combo_use)

        # start date
        str_label = QLabel("시작 날짜")
        str_label.setFont(QFont("한컴산뜻돋움", 12, QFont.Bold))
        str_label.setAlignment(Qt.AlignLeft)

        self.fin_selected_str_text = self.now
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setStyleSheet(date_edit_style)
        self.start_date.setFixedSize(200, 30)
        self.start_date.setMaximumDate(QDate.currentDate()) 
        self.start_date.calendarWidget().setStyleSheet(calendar_style)

        self.start_date.dateChanged.connect(self.on_str_date_changed)

        str_layout.addWidget(str_label)
        str_layout.addWidget(self.start_date)

        # end date  notend_layout
        end_label = QLabel("종료 날짜")
        end_label.setFont(QFont("한컴산뜻돋움", 12, QFont.Bold))
        end_label.setAlignment(Qt.AlignLeft)
        
        self.chk_end_date = QCheckBox()  # 체크박스 추가
        self.chk_end_date.setText("비활성화")  # 체크박스 텍스트 설정
        self.chk_end_date.setFont(QFont("한컴산뜻돋움", 10))
        self.chk_end_date.setStyleSheet("margin-left: auto;")  # 오른쪽 정렬
        self.chk_end_date.setChecked(False)  # 기본값 체크
        self.selected_state = 0
        self. chk_end_date.stateChanged.connect(self.on_chk_end_changed)


        help_label = QLabel("?")
        help_label.setFont(QFont("Arial", 12, QFont.Bold))
        # help_label.setStyleSheet("""
        #     color: blue;
        #     border: 1px solid gray;
        #     border-radius: 50%;
        #     padding: 0.px;
        #     width: 2px;
        #     height: 2px;
        #     font-size: 5px;
        #     text-align: center;
        # """)
        help_label.setAlignment(Qt.AlignCenter)
        help_label.setToolTip("일일 데이터(1일치)를 생산하고자 한다면 비활성화를 체크해주세요! ")  # 마우스 올리면 도움말 표시

        self.fin_selected_end_text = self.now
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(date_edit_style)
        self.end_date.setFixedSize(200, 30)
        self.end_date.setMaximumDate(QDate.currentDate()) 
        self.end_date.calendarWidget().setStyleSheet(calendar_style)

        self.end_date.dateChanged.connect(self.on_end_date_changed)
        
        notend_layout.addWidget(end_label)
        notend_layout.addWidget(self.chk_end_date)
        notend_layout.addWidget(help_label)
        end_layout.addLayout(notend_layout)
        end_layout.addWidget(self.end_date)

        # setting_button
        self.btn_reset = QPushButton("초기화", self)
        self.btn_reset.setFont(QFont("한컴산뜻돋움", 12))
        self.btn_reset.setFixedSize(100, 30)
        self.btn_reset.setStyleSheet("background-color: #dcdcdc; padding: 8px; border-radius: 5px;")
        self.btn_reset.clicked.connect(self.all_setting_btn_click)

        setbtn_layout.addWidget(self.btn_reset, alignment=Qt.AlignLeft)
        
        #check_button
        self.btn_confirm = QPushButton("확인", self)
        self.btn_confirm.setFont(QFont("한컴산뜻돋움", 12))
        self.btn_confirm.setFixedSize(100, 30)
        self.btn_confirm.setStyleSheet("background-color: #007BFF; color: white; padding: 1px; border-radius: 5px;")
        chkbtn_layout.setContentsMargins(0, 0, 20, 0)  # (좌, 상, 우, 하) 마진 설정
        chkbtn_layout.addWidget(self.btn_confirm, alignment=Qt.AlignRight)
        self.btn_confirm.clicked.connect(self.chk_element)

        frame_1.setLayout(title_layout)
        frame_2.setLayout(obs_layout);frame_3.setLayout(use_layout)
        frame_4.setLayout(str_layout);frame_5.setLayout(end_layout)
        frame_6.setLayout(setbtn_layout);frame_7.setLayout(chkbtn_layout)

        frame_1.setFixedSize(460, 50); empty.setFixedSize(230, 5)
        frame_2.setFixedSize(230, 80); frame_3.setFixedSize(230, 80)
        frame_4.setFixedSize(230, 80); frame_5.setFixedSize(230, 80)
        frame_6.setFixedSize(230, 70); frame_7.setFixedSize(230, 70)
        
        spliter_1 = QSplitter(Qt.Horizontal)
        spliter_1.addWidget(frame_2);spliter_1.addWidget(frame_3)

        spliter_2 = QSplitter(Qt.Horizontal)
        spliter_2.addWidget(frame_4);spliter_2.addWidget(frame_5)

        spliter_3 = QSplitter(Qt.Horizontal)
        spliter_3.addWidget(frame_6);spliter_3.addWidget(frame_7)

        main_layout.addWidget(frame_1)
        main_layout.addWidget(spliter_1)
        main_layout.addWidget(empty)
        main_layout.addWidget(spliter_2)
        main_layout.addWidget(spliter_3)

        self.resize(500, 400)
        self.show()

    def on_chk_end_changed(self, state):
        self.selected_state = state
        # self.end_date.setEnabled(state == Qt.Checked)
        if self.selected_state == Qt.Checked:
            self.end_date.setEnabled(False)
        else:
            self.end_date.setEnabled(True)

    def on_str_date_changed(self, date):
        self.fin_selected_str_text = date.toString('yyyy-MM-dd')
        
    def on_end_date_changed(self, date):
        self.fin_selected_end_text = date.toString('yyyy-MM-dd')

    def all_setting_btn_click(self):
        self.fin_selected_obs = "가덕도"
        self.combo_station.setCurrentText(self.fin_selected_obs)

        self.fin_selected_use = "CARIS"
        self.combo_use.setCurrentText(self.fin_selected_use)

        self.fin_selected_str_text = self.now
        self.start_date.setDate(QDate.currentDate())

        self.fin_selected_end_text = self.now
        self.end_date.setDate(QDate.currentDate())

    def chk_element(self, state):
        if self.selected_state == Qt.Checked:
            self.fin_selected_end_text = self.fin_selected_str_text
        err_result = self.chk_date(self.fin_selected_str_text, self.fin_selected_end_text)
        if err_result == "error":
            self.all_setting_btn_click()
        else:
            if (self.fin_selected_str_text == self.fin_selected_end_text):
                period = f"{self.fin_selected_str_text}"
            else:
                period = f"{self.fin_selected_str_text} ~ {self.fin_selected_str_text}"

            msg = QMessageBox.question(self, "최종 확인",\
                f"\n선택하신 내용이 맞나요?\n\n조위관측소: {self.fin_selected_obs}\n용도: {self.fin_selected_use}\n기간: {period}")

            if msg == QMessageBox.Yes:
                fin_result = gen_text(self.fin_selected_str_text, self.fin_selected_end_text, self.fin_selected_obs, self.fin_selected_use)
            else:
                self.all_setting_btn_click()

    def chk_date(self, str, end):     
        
        str_chk = dt(int(str.split("-")[0]), int(str.split("-")[1]), int(str.split("-")[2]))
        end_chk = dt(int(end.split("-")[0]), int(end.split("-")[1]), int(end.split("-")[2]))

        if end_chk < str_chk:
            QMessageBox.warning(self,"경고", "\n기간 오류 :\n\n종료 날짜가 시작 날짜보다 이전일 수 없습니다.  \n다시 선택해주세요.")
            return "error"
        else:
            return "non-error"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TideProcessingApp()
    window.show()
    sys.exit(app.exec_())
