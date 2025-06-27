from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6.QtCore import Qt

class DialogoRotaMapa(QDialog):
    """
    Diálogo para exibir uma rota no Google Maps usando QWebEngineView.
    """
    def __init__(self, origem: str, destino: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rota no Google Maps")
        self.setMinimumSize(800, 600) 

        layout = QVBoxLayout(self)

        # Título do diálogo
        label_titulo = QLabel("Rota no Google Maps:")
        font_titulo = label_titulo.font()
        font_titulo.setPointSize(12)
        font_titulo.setBold(True)
        label_titulo.setFont(font_titulo)
        layout.addWidget(label_titulo)

        # Informação de Origem e Destino
        label_info = QLabel(f"<b>Origem:</b> {origem}<br><b>Destino:</b> {destino}")
        label_info.setWordWrap(True)
        label_info.setFont(label_titulo.font()) 
        layout.addWidget(label_info)

        # Widget para exibir o conteúdo web (o mapa do Google)
        self.web_view = QWebEngineView(self)
        
        url = f"https://www.google.com/maps/dir/?api=1&origin={origem}&destination={destino}"
        
        self.web_view.setUrl(url)
        layout.addWidget(self.web_view)

        # Botão para fechar o diálogo
        botao_fechar = QPushButton("Fechar")
        botao_fechar.clicked.connect(self.accept) 
        botao_fechar.setFixedHeight(35)
        layout.addWidget(botao_fechar)

        self.setLayout(layout)