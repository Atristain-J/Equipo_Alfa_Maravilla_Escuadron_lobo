import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QLineEdit, QDialog, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import QTimer, Qt, QRect, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush

class MonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('icon.png'))
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        traffic_light_layout = QVBoxLayout()

        red_label = QLabel()
        red_label.setPixmap(self.create_circle_pixmap(50, Qt.GlobalColor.red))
        traffic_light_layout.addWidget(red_label)

        yellow_label = QLabel()
        yellow_label.setPixmap(self.create_circle_pixmap(50, Qt.GlobalColor.yellow))
        traffic_light_layout.addWidget(yellow_label)

        green_label = QLabel()
        green_label.setPixmap(self.create_circle_pixmap(50, Qt.GlobalColor.green))
        traffic_light_layout.addWidget(green_label)

        main_layout.addLayout(traffic_light_layout)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(20, 0, 0, 0)

        title_layout = QHBoxLayout()
        title_layout.addStretch(1)
        label_monitor = QLabel("Monitor")
        label_monitor.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(label_monitor)
        title_layout.addStretch(1)

        right_layout.addLayout(title_layout)

        puerto_layout = QHBoxLayout()
        self.puerto_combo = QComboBox()
        self.puerto_combo.addItems(["Puerto", "COM1", "COM2", "COM3"])
        puerto_layout.addWidget(self.puerto_combo)

        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["Baudrate", "9600", "115200", "4800"])
        puerto_layout.addWidget(self.baudrate_combo)

        right_layout.addLayout(puerto_layout)

        settings_layout = QHBoxLayout()
        
        self.bits_datos_combo = QComboBox()
        self.bits_datos_combo.addItems(["Bits de datos", "5", "6", "7", "8"])
        settings_layout.addWidget(self.bits_datos_combo)

        self.bits_parada_combo = QComboBox()
        self.bits_parada_combo.addItems(["Bits parada", "1", "1.5", "2"])
        settings_layout.addWidget(self.bits_parada_combo)

        self.paridad_combo = QComboBox()
        self.paridad_combo.addItems(["Paridad", "Ninguna", "Par", "Impar"])
        settings_layout.addWidget(self.paridad_combo)

        right_layout.addLayout(settings_layout)

        send_layout = QHBoxLayout()
        self.text_input = QLineEdit()
        send_layout.addWidget(self.text_input)

        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        send_layout.addWidget(send_button)

        right_layout.addLayout(send_layout)

        self.text_output = QLineEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Cambiado para ser más grande
        self.text_output.setMinimumHeight(200)  # Ajustamos el tamaño mínimo
        right_layout.addWidget(self.text_output)

        right_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.status_label = QLabel("")
        right_layout.addWidget(self.status_label)

        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.toggle_connection)
        right_layout.addWidget(self.connect_button)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def create_circle_pixmap(self, size, color):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QBrush(color))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawEllipse(QRect(0, 0, size, size))
        painter.end()
        return pixmap

    def toggle_connection(self):
        if self.connect_button.text() == "Conectar":
            self.connect_button.setText("Desconectar")
            self.show_notification("Se ha conectado con éxito")
        else:
            self.connect_button.setText("Conectar")
            self.show_notification("Se ha desconectado correctamente")

    def send_message(self):
        message = self.text_input.text()
        if message:
            self.status_label.setText(f"Enviado: {message}")
            self.text_output.setText(message)
        else:
            self.status_label.setText("Nada para enviar")

    def show_notification(self, message):
        notification = QDialog(self)
        notification.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        notification.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        notification_layout = QVBoxLayout(notification)
        notification_label = QLabel(message)
        notification_layout.addWidget(notification_label)
        notification.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 10px;")
        
        notification.move(self.geometry().topRight() - notification.rect().topRight() - QPoint(20, 20))
        notification.show()
        QTimer.singleShot(2000, notification.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonitorApp()
    window.show()
    sys.exit(app.exec())

