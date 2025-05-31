import sys
import os
import requests
import folium
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QWidget, QLabel, QFrame, QListWidget, QListWidgetItem,
    QToolButton, QGraphicsDropShadowEffect
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation, QRect, QSize, QEasingCurve
from PyQt5.QtGui import QColor


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pothole Map')
        self.setFixedSize(405, 720)

        self.lat, self.lon = 37.5665, 126.9780
        self.map_file = os.path.abspath('map.html')
        self.pothole_data_file = os.path.abspath('내비샘플데이터.csv')
        self.pothole_df = pd.DataFrame()
        self.menu_visible = False

        self.initUI()
        self.update_map()

    def create_shadow(self, blur_radius=14, offset_x=3, offset_y=3, color=QColor(0, 0, 0, 120)):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(offset_x, offset_y)
        shadow.setColor(color)
        return shadow

    def initUI(self):
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        self.menu_list = QListWidget(self)
        self.menu_list.setGeometry(-200, 60, 200, 300)
        self.menu_list.itemClicked.connect(self.on_menu_item_clicked)
        self.menu_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        search_frame = QFrame(self)
        search_frame.setGeometry(10, 10, self.width() - 80, 42)
        search_frame.setStyleSheet("""
            QFrame {
                border-radius: 8px;
                background-color: white;
            }
        """)
        search_frame.setGraphicsEffect(self.create_shadow())

        layout = QHBoxLayout(search_frame)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        self.menu_button = QToolButton()
        self.menu_button.setText('☰')
        self.menu_button.setFixedSize(30, 30)
        self.menu_button.setStyleSheet("""
            QToolButton {
                border: none;
                font-size: 18px;
                font-weight: bold;
                color: #666;
            }
            QToolButton:pressed {
                padding-top: 0px;
                padding-left: 0px;
            }
        """)
        self.menu_button.clicked.connect(self.toggle_menu)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('장소, 버스, 지하철, 주소 검색')
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 14px;
                padding-left: 5px;
                background-color: transparent;
                font-family: '맑은 고딕';
            }
        """)
        self.search_input.setAlignment(Qt.AlignVCenter)

        layout.addWidget(self.menu_button)
        layout.addWidget(self.search_input)

        self.search_button = QPushButton('🡆\n길찾기', self)
        self.search_button.setGeometry(self.width() - 60, 10, 50, 42)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #03c75a;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                font-family: '맑은 고딕';
            }
            QPushButton:hover {
                background-color: #02b152;
            }
        """)
        self.search_button.setGraphicsEffect(self.create_shadow())
        self.search_button.clicked.connect(self.on_search)

        self.bottom_menu = self.create_bottom_menu()
        self.bottom_menu.setParent(self)
        self.bottom_menu.setGeometry(0, self.height() - 50, self.width(), 50)

        self.recenter_button = QPushButton('📍', self)
        self.recenter_button.setGeometry(10, self.height() - 110, 40, 40)
        self.recenter_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 0.3px solid #888;
                border-radius: 20px;
                font-size: 18px;
                font-family: '맑은 고딕';
            }
        """)
        self.recenter_button.setGraphicsEffect(self.create_shadow())
        self.recenter_button.clicked.connect(self.on_recenter)

    def create_bottom_menu(self):
        frame = QFrame()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for name in ['주변', '저장', '대중교통', '내비게이션', 'MY']:
            btn = QPushButton(name)
            btn.setFixedHeight(48)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 13px;
                    color: #444;
                    background-color: #f9f9f9;
                    font-family: '맑은 고딕';
                }
                QPushButton:hover {
                    background-color: #eee;
                }
            """)
            layout.addWidget(btn)

        frame.setLayout(layout)
        frame.setStyleSheet('border-top: 1px solid #ccc;')
        return frame

    def toggle_menu(self):
        end_x = 10 if not self.menu_visible else -self.menu_list.width()
        self.menu_animation = QPropertyAnimation(self.menu_list, b'geometry')
        self.menu_animation.setDuration(300)
        self.menu_animation.setStartValue(self.menu_list.geometry())
        self.menu_animation.setEndValue(QRect(end_x, 60, 200, 300))
        self.menu_animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.menu_animation.start()
        self.menu_visible = not self.menu_visible

    def update_map(self):
        m = folium.Map(location=[self.lat, self.lon], zoom_start=15, zoom_control=False, control_scale=True)

        scale_control_css = """
        <style>
        .leaflet-control-scale {
            bottom: 60px !important;
            left: 60px !important;
        }
        </style>
        """
        m.get_root().header.add_child(folium.Element(scale_control_css))
        
        folium.Marker([self.lat, self.lon], tooltip='현재 위치').add_to(m)

        try:
            df = pd.read_csv(self.pothole_data_file)
            self.pothole_df = df[df['감지여부'] == 1].reset_index(drop=True)
            self.menu_list.clear()

            for idx, row in self.pothole_df.iterrows():
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    icon=folium.Icon(icon='exclamation-sign', color='red'),
                    tooltip='포트홀 발생 지점'
                ).add_to(m)

                folium.CircleMarker(
                    location=[row['위도'], row['경도']],
                    radius=10, fill=True, fill_color='orange', fill_opacity=0.3,
                    color='red',
                    tooltip=f"감지됨: {row['감지시간']}"
                ).add_to(m)

                item = QListWidgetItem()
                item.setSizeHint(QSize(200, 46))
                item.setData(Qt.UserRole, (row['위도'], row['경도']))
                self.menu_list.addItem(item)

                container = QWidget()
                layout = QVBoxLayout()
                layout.setContentsMargins(8, 2, 8, 2)

                detected_at = datetime.strptime(str(int(row['감지시간'])), '%Y%m%d%H%M%S')
                label = QLabel(f"{detected_at}\n({row['위도']:.4f}, {row['경도']:.4f})")
                label.setStyleSheet("""
                    font-size: 13px;
                    font-family: '맑은 고딕';
                    border-bottom: 1px solid #ccc;             
                """)
                layout.addWidget(label)
                container.setLayout(layout)
                self.menu_list.setItemWidget(item, container)

        except Exception as e:
            print(f'CSV ex: {e}')

        m.save(self.map_file)
        self.web_view.load(QUrl.fromLocalFile(self.map_file))

    def on_menu_item_clicked(self, item):
        lat, lon = item.data(Qt.UserRole)
        self.lat, self.lon = lat, lon
        self.update_map()

    def on_search(self):
        keyword = self.search_input.text()
        result = self.get_coordinate_from_keyword(keyword)
        if result:
            self.lat, self.lon = result
        else:
            print(f'알 수 없는 장소: {keyword}')
        self.update_map()

    def on_recenter(self):
        self.lat, self.lon = 37.5665, 126.9780
        self.update_map()


    def get_coordinate_from_keyword(self, keyword):
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': keyword,
            'format': 'json'
        }
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            )
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
        return None



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapApp()
    win.show()
    sys.exit(app.exec_())
