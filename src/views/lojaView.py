from services.seleniumBusca import buscar_lojas_google_maps
from models.lojaModel import Loja
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QMainWindow,
    QDialog, QProgressBar, QTextEdit, QScrollArea, QMessageBox,
    QInputDialog
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QThread
import sys
import os
import webbrowser
from urllib.parse import quote

class LojaView:
    @staticmethod
    def mostrarLoja(loja: Loja):
        return (
            f"Nome:     {loja.nome}\n"
            f"Endereco: {loja.endereco}\n"
        )

    @staticmethod
    def mostrarVariasLojas(lojas):
        texto = ''
        for i, loja in enumerate(lojas, 1):
            texto += f"\nLoja {i}:\n{LojaView.mostrarLoja(loja)}"
        return texto

# --- Diálogo para Mostrar Lojas Existentes ---
class DialogoMostrarLojas(QDialog):
    def __init__(self, lista_de_lojas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lojas Existentes")
        self.setMinimumSize(450, 550)
        self.lista_de_lojas = lista_de_lojas

        layout = QVBoxLayout(self)

        label_titulo = QLabel("Lojas Cadastradas Atualmente:")
        font_titulo = label_titulo.font()
        font_titulo.setPointSize(11)
        font_titulo.setBold(True)
        label_titulo.setFont(font_titulo)
        layout.addWidget(label_titulo)

        self.label_lojas = QLabel(self)
        self.label_lojas.setWordWrap(True)
        self.label_lojas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        font_label = self.label_lojas.font()
        font_label.setPointSize(10)
        self.label_lojas.setFont(font_label)

        # Adiciona o conteúdo aqui (cuidado para usar self.label_lojas)
        self.label_lojas.setText(
            LojaView.mostrarVariasLojas(lista_de_lojas) 
            if lista_de_lojas 
            else "Nenhuma loja cadastrada no momento."
        )

        # Scroll area contendo a label
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label_lojas)
        scroll_area.setFixedHeight(250)

        layout.addWidget(scroll_area)

        # Layout para botões
        botoes_layout = QHBoxLayout()
        
        # Botão para ver rotas (se houver lojas)
        if lista_de_lojas:
            self.botao_ver_rota = QPushButton("Ver Rota")
            self.botao_ver_rota.setFixedSize(90, 30)
            self.botao_ver_rota.clicked.connect(self._escolher_loja_para_rota)
            botoes_layout.addWidget(self.botao_ver_rota)

        self.botao_ok = QPushButton("OK", self)
        self.botao_ok.clicked.connect(self.accept)
        font_botao = self.botao_ok.font()
        font_botao.setPointSize(10)
        self.botao_ok.setFont(font_botao)
        self.botao_ok.setFixedHeight(35)
        botoes_layout.addWidget(self.botao_ok)
        
        layout.addLayout(botoes_layout)
        self.setLayout(layout)

    def _escolher_loja_para_rota(self):
        """Permite ao usuário escolher uma loja para ver a rota"""
        if not self.lista_de_lojas:
            return
            
        # Cria lista de opções para o usuário escolher
        opcoes = [f"{i+1}. {loja.nome}" for i, loja in enumerate(self.lista_de_lojas)]
        
        opcao_escolhida, ok = QInputDialog.getItem(
            self,
            "Escolher Loja",
            "Selecione uma loja para ver a rota:",
            opcoes,
            0,
            False
        )
        
        if ok and opcao_escolhida:
            # Extrai o índice da opção escolhida
            indice = int(opcao_escolhida.split('.')[0]) - 1
            loja_selecionada = self.lista_de_lojas[indice]
            self._abrir_rota(loja_selecionada.endereco)

    def _abrir_rota(self, destino_loja: str): 
        origem, ok = QInputDialog.getText(self, "Endereço de Origem", "Por favor, insira seu endereço de partida:")
        if ok and origem:
            origem_encoded = quote(origem)
            destino_encoded = quote(destino_loja)
            url = f"https://www.google.com/maps/dir/?api=1&origin={origem_encoded}&destination={destino_encoded}"
            webbrowser.open(url)
        elif ok:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um endereço válido.")

    def _limpar_recursos_rota(self):
        """Limpa recursos após fechar o diálogo de rota"""
        print("Diálogo de rota fechado, recursos liberados")
    

# --- Diálogo para Mostrar Adicionar Loja Manualmente ---
class DialogoAdicionarLojaManual(QDialog):
    loja_adicionada = pyqtSignal(str, str) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Loja Manualmente")
        self.setFixedSize(400, 250) 

        layout = QVBoxLayout(self) 

        
        self.label_nome = QLabel("Nome da Loja:")
        self.input_nome = QLineEdit(self)
        self.input_nome.setPlaceholderText("Digite o nome da loja")
        layout.addWidget(self.label_nome)
        layout.addWidget(self.input_nome)

       
        self.label_endereco = QLabel("Endereço da Loja:")
        self.input_endereco = QLineEdit(self)
        self.input_endereco.setPlaceholderText("Digite o endereço completo da loja")
        layout.addWidget(self.label_endereco)
        layout.addWidget(self.input_endereco)

        
        botoes_layout = QHBoxLayout()
        self.botao_salvar = QPushButton("Salvar", self)
        self.botao_salvar.clicked.connect(self.salvar_loja) 
        self.botao_cancelar = QPushButton("Cancelar", self)
        self.botao_cancelar.clicked.connect(self.reject) 

        botoes_layout.addStretch() 
        botoes_layout.addWidget(self.botao_salvar)
        botoes_layout.addWidget(self.botao_cancelar)
        botoes_layout.addStretch() 

        layout.addLayout(botoes_layout) 

        
        font_label = self.label_nome.font()
        font_label.setPointSize(10)
        self.label_nome.setFont(font_label)
        self.label_endereco.setFont(font_label)

        font_input = self.input_nome.font()
        font_input.setPointSize(10)
        self.input_nome.setFont(font_input)
        self.input_endereco.setFont(font_input)
        self.input_nome.setFixedHeight(30)
        self.input_endereco.setFixedHeight(30)

        font_botao = self.botao_salvar.font()
        font_botao.setPointSize(10)
        self.botao_salvar.setFont(font_botao)
        self.botao_cancelar.setFont(font_botao)
        self.botao_salvar.setFixedHeight(35)
        self.botao_cancelar.setFixedHeight(35)

    def salvar_loja(self):
        """
        Método chamado ao clicar em Salvar. Valida os campos e emite o sinal
        'loja_adicionada' se os dados forem válidos.
        """
        nome = self.input_nome.text().strip()
        endereco = self.input_endereco.text().strip()

        if not nome or not endereco:
            QMessageBox.warning(self, "Campos Vazios", "Por favor, preencha o nome e o endereço da loja.")
            return
        
        if len(nome) > 100:
            QMessageBox.warning(self, "Erro", "Nome muito longo (máx. 100 caracteres)")
            return
    
        self.loja_adicionada.emit(nome, endereco)
        self.accept() 

# --- Diálogo de Progresso para Inserir UMA Loja ---
class DialogoProgressoLojaUnica(QDialog):
    insercao_concluida = pyqtSignal(str)

    def __init__(self, nome_loja_a_inserir, parent=None):
        super().__init__(parent)
        self.nome_loja_a_inserir = nome_loja_a_inserir
        self.setWindowTitle(f"Inserindo Loja: {self.nome_loja_a_inserir[:30]}...")
        self.setMinimumSize(450, 250)

        layout = QVBoxLayout(self)

        self.label_status = QLabel(f"Preparando para inserir: {self.nome_loja_a_inserir}...")
        font_status = self.label_status.font()
        font_status.setPointSize(10)
        self.label_status.setFont(font_status)
        layout.addWidget(self.label_status)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFixedHeight(80)
        font_log = self.log_text_edit.font()
        font_log.setPointSize(9)
        self.log_text_edit.setFont(font_log)
        layout.addWidget(self.log_text_edit)

        self.botao_fechar = QPushButton("OK", self)
        self.botao_fechar.setEnabled(False)
        self.botao_fechar.clicked.connect(self.accept)
        font_botao_fechar = self.botao_fechar.font()
        font_botao_fechar.setPointSize(10)
        self.botao_fechar.setFont(font_botao_fechar)
        self.botao_fechar.setFixedHeight(35)
        layout.addWidget(self.botao_fechar)

        self.setLayout(layout)

        self.timer_insercao = QTimer(self)
        self.timer_insercao.timeout.connect(self.processar_insercao)
        self.passo_atual = 0

    def iniciar_simulacao_insercao(self):
        self.log_text_edit.clear()
        self.log_text_edit.append(f"--- Iniciando inserção da loja: {self.nome_loja_a_inserir} ---\n")
        self.passo_atual = 0
        self.progress_bar.setValue(0)
        self.botao_fechar.setEnabled(False)
        self.label_status.setText(f"Inserindo {self.nome_loja_a_inserir}...")
        self.timer_insercao.start(500)

    def processar_insercao(self):
        self.passo_atual += 1
        progresso = self.passo_atual * 34 

        if self.passo_atual == 1:
            self.log_text_edit.append("➡️ Validando nome da loja...")
            self.log_text_edit.insertPlainText(" ✔️ OK.\n")
            self.progress_bar.setValue(min(progresso, 100))
        elif self.passo_atual == 2:
            self.log_text_edit.append("➡️ Registrando no sistema...")
            self.log_text_edit.insertPlainText(" ✔️ OK.\n")
            self.progress_bar.setValue(min(progresso, 100))
        elif self.passo_atual >= 3:
            self.timer_insercao.stop()
            self.log_text_edit.append("➡️ Finalizando...")
            self.log_text_edit.insertPlainText(" ✔️ OK.\n")
            self.progress_bar.setValue(100)
            self.label_status.setText(f"Loja '{self.nome_loja_a_inserir}' inserida com sucesso!")
            self.log_text_edit.append("\n--- Inserção concluída! ---")
            self.botao_fechar.setEnabled(True)
            self.botao_fechar.setFocus()
            self.insercao_concluida.emit(self.nome_loja_a_inserir)
        
        self.log_text_edit.ensureCursorVisible()

class WorkerBuscarLojasThread(QThread):
    finalizado = pyqtSignal()
    erro = pyqtSignal(str)

    def run(self):
        try:
            buscar_lojas_google_maps()
            self.finalizado.emit()
        except Exception as e:
            self.erro.emit(str(e))

# --- Página 1: Para fazer a pergunta e adicionar lojas ---
class PaginaPergunta(QWidget):
    
    perguntaSubmetida = pyqtSignal(str)
    lojasAtualizadas = pyqtSignal()
    adicionarLojaManualSolicitada = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.rotulo_instrucao = QLabel('Projeto IA uneb - Perguntas e Respostas')
        font_rotulo = self.rotulo_instrucao.font()
        font_rotulo.setPointSize(16)
        self.rotulo_instrucao.setFont(font_rotulo)
        layout.addWidget(self.rotulo_instrucao)

        self.caixa_pergunta = QLineEdit(self)
        self.caixa_pergunta.setPlaceholderText("Sua pergunta aqui...")
        font_caixa = self.caixa_pergunta.font()
        font_caixa.setPointSize(11)
        self.caixa_pergunta.setFont(font_caixa)
        self.caixa_pergunta.setFixedHeight(40)
        layout.addWidget(self.caixa_pergunta)

        self.botao_submeter_pergunta = QPushButton('Submeter Pergunta', self)
        font_botao_pergunta = self.botao_submeter_pergunta.font()
        font_botao_pergunta.setPointSize(12)
        self.botao_submeter_pergunta.setFont(font_botao_pergunta)
        self.botao_submeter_pergunta.setFixedHeight(40)
        layout.addWidget(self.botao_submeter_pergunta)

        self.botao_buscar_google_maps = QPushButton('Adicionar Lojas', self)
        font_botao_buscar = self.botao_buscar_google_maps.font()
        font_botao_buscar.setPointSize(10)
        self.botao_buscar_google_maps.setFont(font_botao_buscar)
        self.botao_buscar_google_maps.setFixedHeight(35)
        layout.addWidget(self.botao_buscar_google_maps)

        linha_botoes = QHBoxLayout()

        self.botao_mostrar_lojas = QPushButton('Mostrar Lojas Existentes', self)
        font_botao_mostrar = self.botao_mostrar_lojas.font()
        font_botao_mostrar.setPointSize(10)
        self.botao_mostrar_lojas.setFont(font_botao_mostrar)
        self.botao_mostrar_lojas.setFixedHeight(35)
        linha_botoes.addWidget(self.botao_mostrar_lojas)

        self.botao_reiniciar = QPushButton('Reiniciar Programa', self)
        font_botao_reiniciar = self.botao_reiniciar.font()
        font_botao_reiniciar.setPointSize(10)
        self.botao_reiniciar.setFont(font_botao_reiniciar)
        self.botao_reiniciar.setFixedHeight(35)
        linha_botoes.addWidget(self.botao_reiniciar)

        layout.addLayout(linha_botoes)

        self.botao_adicionar_manual = QPushButton('Adicionar Loja Manualmente', self)
        font_botao_manual = self.botao_adicionar_manual.font()
        font_botao_manual.setPointSize(10)
        self.botao_adicionar_manual.setFont(font_botao_manual)
        self.botao_adicionar_manual.setFixedHeight(35)
        layout.addWidget(self.botao_adicionar_manual)

        self.setLayout(layout)

        self.botao_submeter_pergunta.clicked.connect(self.submeter_pergunta_slot)
        self.botao_buscar_google_maps.clicked.connect(self.buscar_lojas_google_maps_slot)
        self.botao_mostrar_lojas.clicked.connect(self.abrir_dialogo_mostrar_lojas_slot)
        self.botao_reiniciar.clicked.connect(self.reiniciar_programa_slot)
        self.botao_adicionar_manual.clicked.connect(self.abrir_dialogo_adicionar_loja_manual_slot)

    def submeter_pergunta_slot(self):
        pergunta_usuario = self.caixa_pergunta.text().strip()
        if pergunta_usuario:
            self.perguntaSubmetida.emit(pergunta_usuario)
            self.caixa_pergunta.clear()
            self.rotulo_instrucao.setText("Pergunta enviada! Digite nova pergunta.")
        else:
            self.rotulo_instrucao.setText("Por favor, digite uma pergunta antes de submeter.")

    def abrir_dialogo_adicionar_loja_manual_slot(self):
        dialogo = DialogoAdicionarLojaManual(self.window())
        dialogo.loja_adicionada.connect(self.emitir_loja_manual)
        dialogo.exec()

    def emitir_loja_manual(self, nome, endereco):
        self.adicionarLojaManualSolicitada.emit(nome, endereco)
        self.rotulo_instrucao.setText(f"Processando adição manual de '{nome}'...")

    def ao_finalizar_busca_google(self):
        QApplication.restoreOverrideCursor()
        QMessageBox.information(self, "Busca Finalizada", "A busca por lojas no Google Maps foi concluída com sucesso.")
        self.rotulo_instrucao.setText("Busca finalizada. Digite nova pergunta ou realize outra ação.")
        self.lojasAtualizadas.emit()

    def buscar_lojas_google_maps_slot(self):
        self.rotulo_instrucao.setText("Buscando lojas no Google Maps...")

        self.thread_busca = WorkerBuscarLojasThread()
        self.thread_busca.finalizado.connect(self.ao_finalizar_busca_google)
        self.thread_busca.erro.connect(self.ao_erro_busca_google)

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.thread_busca.start()

    def ao_erro_busca_google(self, erro_msg):
        QApplication.restoreOverrideCursor()
        QMessageBox.critical(self, "Erro", f"Ocorreu um erro durante a busca: {erro_msg}")
        self.rotulo_instrucao.setText("Erro na busca. Tente novamente.")

    def abrir_dialogo_mostrar_lojas_slot(self):
        main_window = self.window() 
        if isinstance(main_window, JanelaPrincipal):
            dialogo = DialogoMostrarLojas(main_window.lojas_cadastradas, self.window())
            dialogo.exec()
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível acessar a lista de lojas.")

    def resetar_pagina(self):
        self.caixa_pergunta.clear()
        self.rotulo_instrucao.setText('Projeto IA uneb - Perguntas e Respostas')
    
    def reiniciar_programa_slot(self):
        resposta = QMessageBox.question(
            self,
            "Confirmação de Reinício",
            "Tem certeza que deseja reiniciar o programa?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if resposta == QMessageBox.StandardButton.Yes:
            QApplication.quit()
            os.execl(sys.executable, sys.executable, *sys.argv)

# --- Página 2: Para mostrar a resposta ---
class PaginaResposta(QWidget):
    voltarParaInicio = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label_titulo_resposta = QLabel("Resposta:")
        font_titulo = self.label_titulo_resposta.font()
        font_titulo.setPointSize(12); font_titulo.setBold(True)
        self.label_titulo_resposta.setFont(font_titulo)
        layout.addWidget(self.label_titulo_resposta)
        self.label_resposta_conteudo = QLabel("A resposta para sua pergunta aparecerá aqui.")
        font_conteudo = self.label_resposta_conteudo.font()
        font_conteudo.setPointSize(11)
        self.label_resposta_conteudo.setFont(font_conteudo)
        self.label_resposta_conteudo.setWordWrap(True)
        layout.addWidget(self.label_resposta_conteudo)
        layout.addStretch(1)
        self.botao_ok = QPushButton('OK', self)
        font_botao_ok = self.botao_ok.font()
        font_botao_ok.setPointSize(11)
        self.botao_ok.setFont(font_botao_ok)
        self.botao_ok.setFixedHeight(40)
        layout.addWidget(self.botao_ok)
        self.setLayout(layout)
        self.botao_ok.clicked.connect(self.voltar_slot)

    def setResposta(self, pergunta, resposta):
        self.label_resposta_conteudo.setText(f"Você perguntou: '{pergunta}'\n\nResposta: {resposta}")

    def voltar_slot(self):
        self.voltarParaInicio.emit()

# --- Janela Principal que gerencia as páginas e a lista de lojas ---
class JanelaPrincipal(QMainWindow):
    def __init__(self, lojaController):
        super().__init__()
        self.controller = lojaController
        self.lojas_cadastradas = lojaController.mostrarLojas()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('IA uneb')
        self.setGeometry(200, 200, 650, 470) 

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal_do_central = QVBoxLayout(widget_central)

        self.stacked_widget = QStackedWidget()
        self.pagina_pergunta = PaginaPergunta()
        self.pagina_resposta = PaginaResposta()

        self.stacked_widget.addWidget(self.pagina_pergunta)
        self.stacked_widget.addWidget(self.pagina_resposta)
        layout_principal_do_central.addWidget(self.stacked_widget)

        self.pagina_pergunta.perguntaSubmetida.connect(self.mostrar_pagina_resposta_slot)
        self.pagina_resposta.voltarParaInicio.connect(self.mostrar_pagina_pergunta_slot)
        self.pagina_pergunta.lojasAtualizadas.connect(self.atualizar_lojas)
        self.pagina_pergunta.adicionarLojaManualSolicitada.connect(self.processar_adicao_manual_loja)

        self.mostrar_pagina_pergunta_slot()

    def processar_adicao_manual_loja(self, nome, endereco):
        nova_loja = Loja(nome=nome, endereco=endereco)

        dialogo_progresso = DialogoProgressoLojaUnica(nome_loja_a_inserir=nome, parent=self)
        
        dialogo_progresso.insercao_concluida.connect(self.ao_insercao_manual_concluida)
        
        dialogo_progresso.iniciar_simulacao_insercao()

        self.controller.criarLoja(nova_loja)

        dialogo_progresso.exec()

    def ao_insercao_manual_concluida(self, nome_loja):
        QMessageBox.information(self, "Loja Adicionada", f"A loja '{nome_loja}' foi adicionada com sucesso!")
        self.atualizar_lojas() 
        self.pagina_pergunta.resetar_pagina() 
        self.stacked_widget.setCurrentWidget(self.pagina_pergunta) 

    def atualizar_lojas(self):
        self.lojas_cadastradas = self.controller.mostrarLojas()

    def mostrar_pagina_resposta_slot(self, pergunta_recebida):
        # Equivalente a: controller.responder_pergunta()
        self.pagina_resposta.setResposta(pergunta_recebida, self.controller.responder_pergunta(pergunta_recebida))
        self.stacked_widget.setCurrentWidget(self.pagina_resposta)

    def mostrar_pagina_pergunta_slot(self):
        self.pagina_pergunta.resetar_pagina()
        self.stacked_widget.setCurrentWidget(self.pagina_pergunta)