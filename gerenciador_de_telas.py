from PyQt5 import uic

import funcoes
import cadastro
import gerenciador_de_marcacoes


def load_screens():
    global primeira_tela
    global tela_cadastro
    global tela_pesquisa
    global tela_editar_dados
    global tela_login_admin

    primeira_tela = uic.loadUi("primeira_tela.ui")
    tela_cadastro = uic.loadUi("tela_cadastro.ui")
    tela_pesquisa = uic.loadUi("tela_pesquisa.ui")
    tela_editar_dados = uic.loadUi("tela_editar_dados.ui")
    tela_login_admin = uic.loadUi('tela_login_admin.ui')

# Botões e labels da tela de login.

def load_actions():
    primeira_tela.button_cadastrar_novo_usuario.clicked.connect(cadastro.abre_tela_cadastro)
    primeira_tela.button_pesquisar.clicked.connect(funcoes.abre_tela_pesquisa)
    primeira_tela.pushButton_admin.clicked.connect(funcoes.abre_tela_admin)
    primeira_tela.button_entrada.clicked.connect(funcoes.marca_entrada)
    primeira_tela.button_saida.clicked.connect(funcoes.marca_saida)

    # primeira_tela.button_editar_cadastro.clicked.connect(corrigir_marcacoes) - Futura tela de admin

    # Botões e labels da tela de cadastro.

    tela_cadastro.pushButton_2.clicked.connect(cadastro.sair_da_tela_de_cadastro)
    tela_cadastro.pushButton.clicked.connect(cadastro.cadastrar_usuarios)

    # Botões e labels da tela de pesquisa de dados

    tela_pesquisa.pushButton_voltar.clicked.connect(funcoes.sair_da_tela_de_pesquisa)
    tela_pesquisa.actionFechar.triggered.connect(funcoes.fechar_programa)
    tela_pesquisa.pushButton_pesquisa.clicked.connect(gerenciador_de_marcacoes.consultar_marcacoes)
    tela_pesquisa.pushButton_corrigir.clicked.connect(gerenciador_de_marcacoes.corrigir_marcacoes)
    tela_pesquisa.pushButton_pdf.clicked.connect(gerenciador_de_marcacoes.gerador_de_pdf)
    tela_pesquisa.actionSalvar.triggered.connect(gerenciador_de_marcacoes.gerador_de_pdf)
    tela_pesquisa.actionTutorial.triggered.connect(funcoes.abrir_tutorial)
    tela_pesquisa.radioButton_tudo.toggled.connect(funcoes.desabilitar_campos_de_datas)
    tela_pesquisa.radioButton_por_data.toggled.connect(funcoes.habilitar_campos_de_datas)

    # tela_pesquisa.actionSair.triggered.connect(fechar_programa)

    # Botões e labels da tela de edição de dados.
    tela_editar_dados.pushButton_Voltar.clicked.connect(funcoes.sair_da_tela_editar_dados)
    tela_editar_dados.pushButton_Salvar.clicked.connect(gerenciador_de_marcacoes.salvar_dados_editados)
