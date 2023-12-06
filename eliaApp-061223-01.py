import sys
import requests
import os

# Define o caminho base como o diretório onde o executável está localizado
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# Agora você usa base_path para criar caminhos absolutos para os recursos
icon_path = os.path.join(base_path, 'img', 'icon_usuario.png')
icon_path = os.path.join(base_path, 'img', 'icon_assistente.png')
icon_path = os.path.join(base_path, 'img', 'logo_ELITEACO_150px.png')
icon_path = os.path.join(base_path, 'img', 'logo_ELITEACO_500px.png')
icon_path = os.path.join(base_path, 'img', 'logo_ELITEACO_OR.png')
icon_path = os.path.join(base_path, 'img', 'logo_eliaApp_500x166.png')
icon_path = os.path.join(base_path, 'img', 'icone_ELITEACO.ico')

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QWidget,
)
from PyQt6.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QFont,
    QPixmap,
    QIcon,  # Importação correta adicionada aqui
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize

# Substitua pela sua chave de API e Organization ID reais da OpenAI
API_KEY = "XXXXXXXXXXXXXXXXXX"
ORGANIZATION_ID = "org-4GGvTGan5YuCScHmLKDtIGt8"


class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        try:
            response = self.query_openai_api(self.user_input)
            self.finished.emit(response)
        except Exception as e:
            self.finished.emit(f"Erro ao se comunicar com a API da OpenAI: {e}")

    def query_openai_api(self, user_input):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente útil. Responda sempre em Português (Brasil).",
                },
                {"role": "user", "content": user_input},
            ],
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Organization": ORGANIZATION_ID,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]


class EliaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicação ELIA - Inteligência Artificial da Elite Aço")
        self.setWindowIcon(QIcon(os.path.join(base_path, "img/icon_usuario.png")))

        self.chat_history = QTextEdit()
        self.processing_label = QLabel()
        self.input_area = QLineEdit()
        self.send_button = QPushButton("Enviar")
        self.current_worker = None

        # Garantindo que self.layout é um QVBoxLayout antes de prosseguir.
        self.layout = QVBoxLayout()  # Aqui é onde definimos self.layout como um layout.

        self.init_ui()
        
        # Define o tamanho e posição iniciais da janela
        self.setGeometry(300, 300, 800, 600)

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel, QPushButton {
                font-family: 'Arial';
                font-size: 15px;
            }
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #D3D3D3;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #005FA3;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
        """)

        # Configuração do layout principal
        self.layout = QVBoxLayout()

        # Configuração da logo existente
        self.logo = QLabel()
        self.logo_pixmap = QPixmap(os.path.join(base_path, "img/logo_ELITEACO_500px.png"))
        self.logo.setPixmap(
            self.logo_pixmap.scaled(QSize(400, 100), Qt.AspectRatioMode.KeepAspectRatio)
        )

        # Configuração da nova logo
        self.new_logo = QLabel()
        self.new_logo_pixmap = QPixmap(os.path.join(base_path, "img/logo-eliaApp_500px166.png"))
        self.new_logo.setPixmap(
            self.new_logo_pixmap.scaled(QSize(400, 100), Qt.AspectRatioMode.KeepAspectRatio)
        )

        # Layout horizontal para as logos
        self.logo_layout = QHBoxLayout()
        self.logo_layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.logo_layout.addWidget(self.new_logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Adicionando o layout das logos ao layout principal
        self.layout.addLayout(self.logo_layout)

        # Configuração da área de histórico de conversas
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet(
            "QTextEdit { padding: 10px; }"
        )  # Adicionar padding interno
        self.chat_history.setFont(QFont("Arial", 12))  # Configurar o tamanho da fonte
        self.layout.addWidget(self.chat_history)

        # Mensagem de boas-vindas
        self.append_message_to_chat(
            "Assistente",
            "Olá, me chamo ELIA! Sou a IA da Elite Aço. Seja bem-vindo(a)! Como posso ajudar?",
        )

        # Configuração da área de entrada de texto
        self.input_area.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.input_area)

        # Configuração do botão de envio
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Configuração do label de processamento
        self.layout.addWidget(self.processing_label)

        # Configuração do widget central da janela
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        
        # Adicione esta linha no final do método init_ui
        self.input_area.setFocus()

    def send_message(self):
        user_message = self.input_area.text()
        if user_message:
            self.append_message_to_chat("Você", user_message)
            self.input_area.clear()
            self.processing_label.setText("Processando...")
            self.worker = Worker(user_message)
            self.worker.finished.connect(self.handle_response)  # Conexão correta
            self.worker.start()

    def handle_response(self, message):
        self.processing_label.clear()
        self.append_message_to_chat("Assistente", message)

    def append_message_to_chat(self, sender, message):
        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)
        icon_path = os.path.join(base_path, "img/icon_usuario.png" if sender == "Você" else "img/icon_assistente.png")


        # Usar HTML para formatar a mensagem com menor margem
        message_html = f"""
        <div style='text-align: left; margin-bottom: 2px;'>
            <img src='{icon_path}' width='15' height='15' style='vertical-align: middle;'>
            <b>{sender}:</b>
        </div>
        <p style='text-align: left; margin-left: 20px; margin-top: 2px;'>{message}</p><br>
        """

        self.chat_history.insertHtml(message_html)
        self.chat_history.ensureCursorVisible()

# Rodar a aplicação
def main():
    app = QApplication(sys.argv)
    elia_app = EliaApp()
    elia_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
