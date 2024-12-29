import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.toggle_temp_button = QPushButton("Show in Fahrenheit", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.is_celsius = True
        self.temperature_c = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(400, 600)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addWidget(self.city_label)
        hbox.addWidget(self.city_input)

        vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addLayout(hbox)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.toggle_temp_button)
        vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.toggle_temp_button.setObjectName("toggle_temp_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                padding: 20px;
            }
            QLabel, QPushButton {
                font-family: Calibri;
                color: #333;
            }
            QLabel#city_label {
                font-size: 20px;
                font-style: italic;
                color: #555;
            }
            QLineEdit#city_input {
                font-size: 20px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
            }
            QPushButton#get_weather_button, QPushButton#toggle_temp_button {
                font-size: 20px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border: none;
                margin-top: 20px;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel#temperature_label {
                font-size: 50px;
                color: #ff5722;
            }
            QLabel#emoji_label {
                margin-top: 20px;
                font-size: 75px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label {
                margin-top: 20px;
                font-size: 30px;
                color: #777;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
        self.toggle_temp_button.clicked.connect(self.toggle_temperature)

    def get_weather(self):
        api_key = "8707afee902ee19d9a16cd82a2f7a59c"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            if response.status_code == 400:
                self.display_error("Bad request:\nPlease check your input")
            elif response.status_code == 401:
                self.display_error("Unauthorized:\nInvalid API key")
            elif response.status_code == 403:
                self.display_error("Forbidden:\nAccess is denied")
            elif response.status_code == 404:
                self.display_error("Not found:\nCity not found")
            elif response.status_code == 500:
                self.display_error("Internal Server Error:\nPlease try again later")
            elif response.status_code == 502:
                self.display_error("Bad Gateway:\nInvalid response from the server")
            elif response.status_code == 503:
                self.display_error("Service Unavailable:\nServer is down")
            elif response.status_code == 504:
                self.display_error("Gateway Timeout:\nNo response from the server")
            else:
                self.display_error(f"HTTP error occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 20px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 50px;")
        temperature_k = data["main"]["temp"]
        self.temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.update_temperature_label()
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    def update_temperature_label(self):
        if self.is_celsius:
            self.temperature_label.setText(f"{self.temperature_c:.0f}°C")
            self.toggle_temp_button.setText("Show in Fahrenheit")
        else:
            temperature_f = (self.temperature_c * 9/5) + 32
            self.temperature_label.setText(f"{temperature_f:.0f}°F")
            self.toggle_temp_button.setText("Show in Celsius")

    def toggle_temperature(self):
        self.is_celsius = not self.is_celsius
        self.update_temperature_label()

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
