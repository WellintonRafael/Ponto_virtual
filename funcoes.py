from datetime import datetime
import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import gerenciador_de_telas
import run_sql
import funcoes

# from main import(
#     primeira_tela,
#     tela_cadastro,
#     tela_pesquisa,
#     tela_editar_dados,
#     tela_login_admin
# )


def data_brasileira_para_americana(data_a_ser_tratada: str):
    formato_americano = '%Y-%m-%d'
    formato_brasileiro = '%d/%m/%Y'
    data = datetime.strptime(data_a_ser_tratada, formato_brasileiro)
    d = data.strftime(formato_americano)
    return str(d)


def mostra_hora() -> str:
    hora_atual = datetime.now()
    hora_formatada: str = hora_atual.strftime('%H:%M')
    return str(hora_formatada)



def mostra_data() -> str:
    data_atual = datetime.now()
    data_formatada: str = data_atual.strftime('%Y-%m-%d')
    return str(data_formatada)


def validar_hora(hora_a_ser_validada: str):
    hora_validada = str(hora_a_ser_validada).split(":")[0]
    minutos_validados = str(hora_a_ser_validada).split(":")[1]
    hora_validada = str(hora_validada)
    minutos_validados = str(minutos_validados)
    try:
        if hora_a_ser_validada != ':':
            hora_validada = int(hora_validada)
            minutos_validados = int(minutos_validados)
            if hora_validada > 23 or minutos_validados > 59:
                return False
        if hora_a_ser_validada == ':':
            return True
        else:
            return True
    except:
        return False


def abrir_tutorial():
    url = 'https://drive.google.com/file/d/18Dm20N1W4lKg65jxZXqPQl21vhS5Se8L/view?usp=sharing'
    webbrowser.open(url, 0)


def marca_entrada() -> None:
    """ 
        Faz a marcação de "Entrada" e "Ent_almoco" no banco de dados.
        Caso o mesmo usuário já tenha feito as duas marcações no mesmo dia,
        é impresso uma mensagem na tela informando que não é possivel
        realizar a marcação.
    """
    gerenciador_de_telas.primeira_tela.show()
    gerenciador_de_telas.primeira_tela.label_2.setText('')
    login_usuario: str = gerenciador_de_telas.primeira_tela.lineEdit_3.text()
    senha_login: str = gerenciador_de_telas.primeira_tela.lineEdit_2.text()
    # Se conecta com o database e faz a verificação da senha.
    try:
        senha_bd = run_sql.busca_senha_login(login_usuario)
    except(Exception) as e:
        gerenciador_de_telas.primeira_tela.label_2.setText('Aconteceu um erro! Tente novamente!')
    if senha_bd != senha_login:
        msg_de_dados_invalidos()
    else:
        confirmar_entrada = QMessageBox()
        confirmar_entrada.setWindowTitle('Entrada')
        confirmar_entrada.setText('Tem certeza que deseja marcar ENTRADA?')
        confirmar_entrada.setIcon(QMessageBox.Question)
        confirmar_entrada.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resposta = confirmar_entrada.exec_()
        
        if resposta == QMessageBox.No:
            gerenciador_de_telas.primeira_tela.show()
            gerenciador_de_telas.primeira_tela.label_2.setText(mostra_hora())
        elif resposta == QMessageBox.Yes:
        # Se a senha estiver correta,
        # faz a conexão com o database e efetua a marcação.
            try:
                marcacoes = run_sql.busca_marcacoes(funcoes.mostra_data(), login_usuario)
                """Esta variável procura alguma marcação no database
                    que contenha o dia que está sendo
                    efetuada a marcação e o nome de quem está efetuando a marcação.
                    Caso não encontre, inicia uma nova tupla."""

                if marcacoes is None: 
                    coluna_marcacao = 'entrada'
                    try:
                        run_sql.insert_into_marcacoes(coluna_marcacao, login_usuario, funcoes.mostra_data(), funcoes.mostra_hora())
                        mostra_msg_de_sucesso_entrada()

                    except(Exception) as e:
                        print(e)
                        gerenciador_de_telas.primeira_tela.label_2.setText
                        ("Aconteceu um erro! Tente novamente!")
                elif marcacoes is not None and marcacoes[2] is None:
                    coluna_marcacao = 'ent_almoco'

                    try:
                        run_sql.update_marcacao_ponto(coluna_marcacao, funcoes.mostra_hora(), funcoes.mostra_data(), login_usuario)
                        mostra_msg_de_sucesso_entrada()
                    except(Exception) as e:
                        print(e)
                        gerenciador_de_telas.primeira_tela.label_2.setText
                        ("Aconteceu um erro! Tente novamente!")
                elif marcacoes[4] is not None:
                    gerenciador_de_telas.primeira_tela.label_2.setText(
                        'Você já marcou entrada. Agora, marque saída'
                    )
                elif marcacoes[4] is None:
                    coluna_marcacao = 'ent_extra'
                    try:
                        run_sql.update_marcacao_ponto(coluna_marcacao, funcoes.mostra_hora(), funcoes.mostra_data(), login_usuario)
                        mostra_msg_de_sucesso_entrada()
                    except(Exception) as e:
                        print(e)
                        gerenciador_de_telas.primeira_tela.label_2.setText
                        ("Aconteceu um erro! Tente novamente!")

            except(Exception) as e:
                print(e)
                gerenciador_de_telas.primeira_tela.label_2.setText(
                    "Aconteceu um erro! Tente novamente!")


def marca_saida() -> None:
    """
        Faz a marcação de Sai_almoço e Fim do expdiente.
    """
    gerenciador_de_telas.primeira_tela.show()
    gerenciador_de_telas.primeira_tela.label_2.setText("")
    login_usuario = gerenciador_de_telas.primeira_tela.lineEdit_3.text()
    senha_login = gerenciador_de_telas.primeira_tela.lineEdit_2.text()
    # Se conecta com o database e faz a verificação da senha.
    try:
        senha_bd = run_sql.busca_senha_login(login_usuario)   
    except(Exception):
        gerenciador_de_telas.primeira_tela.label_2.setText("Aconteceu um erro! Tente novamente!")
    if senha_bd != senha_login:
        msg_de_dados_invalidos()
    # Se a senha estiver Ok, faz a conexão com o database e efetua a marcação
    else:
        confirmar_saida = QMessageBox()
        confirmar_saida.setWindowTitle('Entrada')
        confirmar_saida.setText('Tem certeza que deseja marcar SAÍDA?')
        confirmar_saida.setIcon(QMessageBox.Question)
        confirmar_saida.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resposta = confirmar_saida.exec_()
        if resposta == QMessageBox.No:
            gerenciador_de_telas.primeira_tela.show()
            gerenciador_de_telas.primeira_tela.label_2.setText(mostra_hora())
        elif resposta == QMessageBox.Yes:
            try:
                marcacoes = run_sql.busca_marcacoes(funcoes.mostra_data(), login_usuario)
                """Esta variável procura alguma marcação no database
                    que contenha o dia que está sendo
                    efetuada a marcação e o nome de quem está efetuando a marcação.
                    Caso não encontre, inicia uma nova tupla."""
                if marcacoes is None: 
                    gerenciador_de_telas.primeira_tela.label_2.setText(
                       "Ops!!! Você ainda NÃO MARCOU A ENTRADA!!!"
                    )   

                elif marcacoes is not None and marcacoes[1] is None:
                    coluna_marcacao = 'sai_almoco'
                    try:
                        run_sql.update_marcacao_ponto(coluna_marcacao, funcoes.mostra_hora(), funcoes.mostra_data(), login_usuario)
                        mostra_msg_de_sucesso_saida()
                    except(Exception) as e:
                        print(e)
                        gerenciador_de_telas.primeira_tela.label_2.setText
                        ("Aconteceu um erro! Tente novamente!")

                elif marcacoes is not None and marcacoes[3] is None: 
                    coluna_marcacao = 'saida'
                    try:
                        run_sql.update_marcacao_ponto(coluna_marcacao, funcoes.mostra_hora(), funcoes.mostra_data(), login_usuario)
                        mostra_msg_de_sucesso_saida()
                    except(Exception) as e:
                        print(e)
                        gerenciador_de_telas.primeira_tela.label_2.setText
                        ("Aconteceu um erro! Tente novamente!")

                elif marcacoes[5] is not None:
                    gerenciador_de_telas.primeira_tela.label_2.setText(
                        'Você já realizou todas as marcações hoje!'
                    )

                elif marcacoes is not None and marcacoes[5] is None:
                    coluna_marcacao = 'sai_extra'
                    try:
                        run_sql.update_marcacao_ponto(coluna_marcacao, funcoes.mostra_hora(), funcoes.mostra_data(), login_usuario)
                        mostra_msg_de_sucesso_saida()
                    except(Exception) as e:
                        print(e)
                        gerenciador_de_telas.primeira_tela.label_2.setText
                        ("Aconteceu um erro! Tente novamente!")
                
            except(Exception) as e:
                print(e)
                gerenciador_de_telas.primeira_tela.label_2.setText(
                    "Aconteceu um erro! Tente novamente!")


def abre_tela_admin():
    gerenciador_de_telas.tela_login_admin.show()


def abre_tela_editar_dados():
    gerenciador_de_telas.tela_editar_dados.show()


def sair_da_tela_editar_dados() -> None:
    gerenciador_de_telas.tela_editar_dados.close()


# Funções para abertura e fechamento de telas.
# Também limpa as labels e os campos de input.
def abre_tela_pesquisa() -> None:
    gerenciador_de_telas.primeira_tela.close()
    gerenciador_de_telas.tela_pesquisa.show()
    gerenciador_de_telas.tela_pesquisa.label_5.setText('')
    gerenciador_de_telas.tela_pesquisa.lineEdit_2.setText('')
    gerenciador_de_telas.tela_pesquisa.lineEdit_3.setText('')
    gerenciador_de_telas.tela_pesquisa.pushButton_corrigir.setEnabled(False)
    gerenciador_de_telas.tela_pesquisa.pushButton_pdf.setEnabled(False)
    gerenciador_de_telas.tela_pesquisa.radioButton_tudo.setChecked(True)
    gerenciador_de_telas.tela_pesquisa.tableWidget.setRowCount(0)
    gerenciador_de_telas.tela_pesquisa.tableWidget.setColumnCount(8)
    lista_de_nomes = run_sql.select_todos_nomes()
    nova_lista = list()
    for item in lista_de_nomes:
        item = item[0]
        nova_lista.append(item)
    gerenciador_de_telas.tela_pesquisa.comboBox.addItems(nova_lista)
    # Iterador que lista os dados em uma "table" da tela pesquisa:
    for i in range(0):
        for c in range(0, 8):
            gerenciador_de_telas.tela_pesquisa.tableWidget.setItem
            (i, c, QtWidgets.QTableWidgetItem(''[i][c]))


def sair_da_tela_de_pesquisa() -> None:
    gerenciador_de_telas.tela_editar_dados.close()
    gerenciador_de_telas.tela_pesquisa.close()
    gerenciador_de_telas.primeira_tela.show()
    gerenciador_de_telas.primeira_tela.label_2.setText(mostra_hora())
    gerenciador_de_telas.primeira_tela.lineEdit_3.setText("")
    gerenciador_de_telas.primeira_tela.lineEdit_2.setText("")


# Funções que escrevem mensagens no label da tela principal.
def msg_de_dados_invalidos() -> None:
    gerenciador_de_telas.primeira_tela.label_2.setText('Usuário ou senha inválidos !!!')
    gerenciador_de_telas.primeira_tela.lineEdit_3.setText('')
    gerenciador_de_telas.primeira_tela.lineEdit_2.setText('')


def mostra_msg_de_sucesso_entrada() -> None:
    gerenciador_de_telas.primeira_tela.label_2.setText(f'Entrada efetuada às {mostra_hora()}')
    gerenciador_de_telas.primeira_tela.lineEdit_3.setText("")
    gerenciador_de_telas.primeira_tela.lineEdit_2.setText("")


def mostra_msg_de_sucesso_saida() -> None:
    gerenciador_de_telas.primeira_tela.label_2.setText(f'Saída efetuada às {mostra_hora()}')
    gerenciador_de_telas.primeira_tela.lineEdit_3.setText("")
    gerenciador_de_telas.primeira_tela.lineEdit_2.setText("")


def fechar_programa() -> None:
    gerenciador_de_telas.tela_editar_dados.close()
    gerenciador_de_telas.tela_cadastro.close()
    gerenciador_de_telas.tela_pesquisa.close()
    gerenciador_de_telas.primeira_tela.close()


def habilitar_campos_de_datas():
    gerenciador_de_telas.tela_pesquisa.lineEdit_2.setEnabled(True)
    gerenciador_de_telas.tela_pesquisa.lineEdit_3.setEnabled(True)
    gerenciador_de_telas.tela_pesquisa.label_3.setEnabled(True)
    gerenciador_de_telas.tela_pesquisa.label_4.setEnabled(True)


def desabilitar_campos_de_datas():
    gerenciador_de_telas.tela_pesquisa.lineEdit_2.setEnabled(False)
    gerenciador_de_telas.tela_pesquisa.lineEdit_3.setEnabled(False)
    gerenciador_de_telas.tela_pesquisa.label_3.setEnabled(False)
    gerenciador_de_telas.tela_pesquisa.label_4.setEnabled(False)
