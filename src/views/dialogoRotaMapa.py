from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from urllib.parse import quote
import webbrowser

class DialogoRotaMapa(QDialog):
    def __init__(self, origem: str, destino: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Abrir Rota no Navegador")
        self.setMinimumSize(400, 200)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Texto explicativo
        mensagem = QLabel("Clique no botão abaixo para abrir a rota no Google Maps.")
        mensagem.setWordWrap(True)
        layout.addWidget(mensagem)

        # Botão para abrir no navegador externo
        btn_abrir_navegador = QPushButton("Abrir Rota no Navegador")
        btn_abrir_navegador.clicked.connect(lambda: self._abrir_rota_no_navegador(origem, destino))
        layout.addWidget(btn_abrir_navegador)

        # Botão de fechar
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.close)
        layout.addWidget(btn_fechar)

        self.setLayout(layout)

    def _abrir_rota_no_navegador(self, origem: str, destino: str):
        origem_encoded = quote(origem)
        destino_encoded = quote(destino)
        url = f"https://www.google.com/maps/dir/?api=1&origin={origem_encoded}&destination={destino_encoded}"
        webbrowser.open(url)
