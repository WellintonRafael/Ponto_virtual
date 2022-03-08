from datetime import datetime
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from reportlab.pdfgen import canvas


# Funções que escrevem mensagens no label da tela principal.
def mostra_msg_de_dados_invalidos() -> None:
    primeira_tela.label_2.setText('Usuário ou senha inválidos !!!')
    primeira_tela.lineEdit_3.setText('')
    primeira_tela.lineEdit_2.setText('')


def mostra_msg_de_sucesso_entrada() -> None:
    primeira_tela.label_2.setText(f'Entrada efetuada às {mostra_hora()}')
    primeira_tela.lineEdit_3.setText("")
    primeira_tela.lineEdit_2.setText("")


def mostra_msg_de_sucesso_saida() -> None:
    primeira_tela.label_2.setText(f'Saída efetuada às {mostra_hora()}')
    primeira_tela.lineEdit_3.setText("")
    primeira_tela.lineEdit_2.setText("")


# Funções que formatam hora e data.
def mostra_data() -> str:
    data_atual = datetime.now()
    data_formatada: str = data_atual.strftime('%Y-%m-%d')
    return data_formatada


data_exata: str = mostra_data()


def mostra_hora() -> str:
    hora_atual = datetime.now()
    hora_formatada: str = hora_atual.strftime('%H:%M')
    return hora_formatada

hora_exata: str = mostra_hora()


# Faz a marcação de Entrada e Ent_almoco no banco de dados.
# Caso o mesmo usuário já tenha feito as duas marcações no mesmo dia,
# é impresso uma mensagem na tela informando que não é possivel
# realizar a marcação.
def marca_entrada() -> None:
    primeira_tela.show()
    primeira_tela.label_2.setText('')
    nome_usuario: str = primeira_tela.lineEdit_3.text()
    senha_login: str = primeira_tela.lineEdit_2.text()
    # Se conecta com o database e faz a verificação da senha.
    try:
        banco = sqlite3.connect('database_ponto_digital.db')
        cursor = banco.cursor()
        cursor.execute("SELECT Senha FROM TB_FUNCIONARIOS \
                WHERE Login = '"+nome_usuario+"'")
        senha_bd = cursor.fetchall()
        senha_bd = senha_bd[0][0]
        banco.close()
    except(Exception):
        primeira_tela.label_2.setText('Aconteceu um erro! Tente novamente!')
    if senha_bd != senha_login:
        mostra_msg_de_dados_invalidos()
    # Se a senha estiver correta, \
    # faz a conexão com o database e efetua a marcação.
    else:
        hora_exata: str = mostra_hora()
        data_exata: str = mostra_data()
        confirmar_entrada = QMessageBox()
        confirmar_entrada.setWindowTitle('Entrada')
        confirmar_entrada.setText('Tem certeza que deseja marcar ENTRADA?')
        confirmar_entrada.setIcon(QMessageBox.Question)
        confirmar_entrada.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        resposta = confirmar_entrada.exec_()
        if resposta == QMessageBox.No:
            primeira_tela.show()
            primeira_tela.label_2.setText(hora_exata)
            primeira_tela.label_2.setText(f'{mostra_hora()}')
        elif resposta == QMessageBox.Yes:
            try:
                banco = sqlite3.connect('database_ponto_digital.db')
                cursor = banco.cursor()
                cursor.execute("SELECT Nome FROM TB_FUNCIONARIOS \
                    WHERE Login = '"+nome_usuario+"'")
                nome_cadastrado_no_bd = cursor.fetchall()
                nome_cadastrado_no_bd = nome_cadastrado_no_bd[0][0]
                cursor.execute("CREATE TABLE IF NOT EXISTS Marcacao_Ponto \
                    (Id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    Cod_funcionario text, \
                    Nome text,Data DATE,Entrada text, Sai_almoco text, \
                    Ent_almoco text, Saida text)")
            except(Exception):
                primeira_tela.label_2.setText(
                    "Aconteceu um erro! Tente novamente!")

            # Função que procura alguma marcação no database\
            # que contenha o dia que está sendo
            # efetuada a marcação e o nome de quem está efetuando a marcação.
            # Caso não encontre, inicia uma nova tupla.
            def buscador() -> None:
                try:
                    cursor.execute("SELECT Entrada FROM Marcacao_Ponto \
                        WHERE (Nome = '"+nome_cadastrado_no_bd+"') and \
                        (Data = '"+data_exata+"')")
                    entrada = cursor.fetchall()
                    entrada = entrada[0][0]
                    return True
                except(Exception):
                    return False
            if buscador() is False:
                try:
                    cursor.execute("SELECT Cod_funcionario FROM TB_FUNCIONARIOS \
                        WHERE Login = '"+nome_usuario+"'")
                    cod_funcionario_bd = cursor.fetchall()
                    cod_funcionario_bd = cod_funcionario_bd[0][0]
                    cursor.execute("INSERT INTO Marcacao_Ponto \
                        (Cod_funcionario, Nome ,Data,Entrada) VALUES \
                        ('"+cod_funcionario_bd+"', '"+nome_cadastrado_no_bd+"', \
                        '"+data_exata+"', '"+hora_exata+"')")
                    banco.commit()
                    banco.close()
                    mostra_msg_de_sucesso_entrada()
                except(Exception):
                    primeira_tela.label_2.setText
                    ("Aconteceu um erro! Tente novamente!")

            # Continuação da função buscador.
            # Se já estiver iniciado esta tupla,\
            # é atualizada o campo Ent_almoco.
            def buscador_2() -> None:
                try:
                    cursor.execute("SELECT Ent_almoco FROM Marcacao_Ponto \
                        WHERE (Nome = '"+nome_cadastrado_no_bd+"') and \
                        (Data = '"+data_exata+"')")
                    entrada_almoco = cursor.fetchall()
                    entrada_almoco = entrada_almoco[0][0]
                    if len(entrada_almoco) == 5:
                        return True
                except(Exception):
                    return False
            if buscador_2() is True:
                primeira_tela.label_2.setText(
                    'Você já marcou entrada! Agora, marque saída')
            elif buscador_2() is False:
                try:
                    cursor.execute("UPDATE Marcacao_Ponto SET \
                        Ent_almoco = '"+hora_exata+"' WHERE \
                        (Nome = '"+nome_cadastrado_no_bd+"') and \
                        (Data = '"+data_exata+"')")
                    banco.commit()
                    banco.close()
                    print()
                    mostra_msg_de_sucesso_entrada()
                except(Exception):
                    pass


# Faz a marcação de Sai_almoço e Fim do expdiente.
def marca_saida() -> None:
    primeira_tela.show()
    primeira_tela.label_2.setText("")
    nome_usuario = primeira_tela.lineEdit_3.text()
    senha_login = primeira_tela.lineEdit_2.text()
    # Se conecta com o database e faz a verificação da senha.
    try:
        banco = sqlite3.connect('database_ponto_digital.db')
        cursor = banco.cursor()
        cursor.execute("SELECT Senha FROM TB_FUNCIONARIOS WHERE \
            Login = '{}'".format(nome_usuario))
        senha_bd = cursor.fetchall()
        senha_bd = senha_bd[0][0]
        banco.close()
    except(Exception):
        primeira_tela.label_2.setText("Aconteceu um erro! Tente novamente!")
    if senha_bd != senha_login:
        mostra_msg_de_dados_invalidos()
    # Se a senha estiver Ok, faz a conexão com o database e efetua a marcação
    else:
        hora_exata = mostra_hora()
        data_exata = mostra_data()
        confirmar_saida = QMessageBox()
        confirmar_saida.setWindowTitle('Entrada')
        confirmar_saida.setText('Tem certeza que deseja marcar SAÍDA?')
        confirmar_saida.setIcon(QMessageBox.Question)
        confirmar_saida.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        resposta = confirmar_saida.exec_()
        if resposta == QMessageBox.No:
            primeira_tela.show()
            primeira_tela.label_2.setText(hora_exata)
            primeira_tela.label_2.setText(f'{mostra_hora()}')
        elif resposta == QMessageBox.Yes:
            try:
                banco = sqlite3.connect('database_ponto_digital.db')
                cursor = banco.cursor()
                cursor.execute("SELECT Nome FROM TB_FUNCIONARIOS WHERE \
                    Login = '"+nome_usuario+"'")
                nome_cadastrado_no_bd = cursor.fetchall()
                nome_cadastrado_no_bd = nome_cadastrado_no_bd[0][0]
                cursor.execute("SELECT Sai_almoco, Saida FROM Marcacao_Ponto \
                    WHERE (Nome = '"+nome_cadastrado_no_bd+"') and \
                    (Data = '"+data_exata+"')")
                select = cursor.fetchall()
                saida_almoco = select[0][0]
                saida = select[0][1]
                hora_exata = mostra_hora()
                data_exata = mostra_data()
                if saida_almoco is None:
                    cursor.execute("UPDATE Marcacao_Ponto SET Sai_almoco  = \
                        '"+hora_exata+"' WHERE \
                        (Nome = '"+nome_cadastrado_no_bd+"') and \
                        (Data = '"+data_exata+"')")
                    banco.commit()
                    banco.close()
                    mostra_msg_de_sucesso_saida()
                elif saida is None:
                    cursor.execute("UPDATE Marcacao_Ponto SET \
                        Saida  = '"+hora_exata+"' \
                        WHERE (Nome = '"+nome_cadastrado_no_bd+"') and \
                        (Data = '"+data_exata+"')")
                    banco.commit()
                    banco.close()
                    primeira_tela.lineEdit_3.setText('')
                    primeira_tela.lineEdit_2.setText('')
                    primeira_tela.label_2.setText(
                        'Fim do Expediente! Bom descanso!   :)')
                else:
                    primeira_tela.label_2.setText(
                        'Você já fez todas as marcações hoje!')
            except(Exception):
                primeira_tela.label_2.setText(
                    "Ops!!! Você ainda NÃO MARCOU A ENTRADA!!!")


# Verifica se os dados são suficientes para cadastrar um novo usuário,
# e se a condição for True, insere esse usuário como uma tupla no database.
def cadastrar_usuarios() -> None:
    cod_funcionario = tela_cadastro.lineEdit_5.text()
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha_cadastro = tela_cadastro.lineEdit_3.text()
    confirma_senha = tela_cadastro.lineEdit_4.text()
    if ((senha_cadastro == confirma_senha) and
            (senha_cadastro != '') and
            (login != '') and
            (nome != '')):
        try:
            banco = sqlite3.connect('database_ponto_digital.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS TB_FUNCIONARIOS \
                (Cod_funcionario text,Nome text,Login text,Senha text)")
            cursor.execute("INSERT INTO TB_FUNCIONARIOS VALUES \
                ('"+cod_funcionario+"','"+nome+"','"+login+"', \
                '"+senha_cadastro+"')")
            banco.commit()
            banco.close()
            box = QMessageBox()
            box.setWindowTitle('Cadastrar')
            box.setText('Cadastro realizado com sucesso!')
            box.setIcon(QMessageBox.Information)
            box.setStandardButtons(QMessageBox.Ok)
            box.exec_()
            cod_funcionario = tela_cadastro.lineEdit_5.text()
            tela_cadastro.lineEdit.setText('')
            tela_cadastro.lineEdit_2.setText('')
            tela_cadastro.lineEdit_3.setText('')
            tela_cadastro.lineEdit_4.setText('')
            tela_cadastro.lineEdit_5.setText('')
        except(Exception):
            tela_cadastro.label_11.setText(
                "Erro ao inserir dados! Refaça a operação!")
    elif senha_cadastro != confirma_senha:
        tela_cadastro.label_11.setText("As duas senhas devem ser iguais!!!")
    else:
        tela_cadastro.label_11.setText(
            "Preencha corretamente todos os campos obrigatórios!!!")


# Função que busca os dados de um funcionário através do
# "Cod_funcionario" e os exibe na "tela_pesquisa":
def consultar_marcacoes() -> None:
    global cod_pesquisado
    global nome
    global data_inicio
    global data_fim
    global data_inicio_tratada
    global data_fim_tratada
    # Se conecta com o database e faz a verificação do "Cod_funcionario".
    try:
        cod_pesquisado = tela_pesquisa.lineEdit.text()
        banco = sqlite3.connect("database_ponto_digital.db")
        cursor = banco.cursor()
        cursor.execute("SELECT Cod_funcionario FROM Marcacao_Ponto WHERE \
            Cod_funcionario = '"+cod_pesquisado+"'")
        dados_bd = cursor.fetchall()
        dados_bd = dados_bd[0][0]
        banco.close()
        # Se o código pesquisado for válido, faz a conexão com o database
        # e exibe na tela os dados pesquisados
        if cod_pesquisado == dados_bd:
            try:
                banco = sqlite3.connect("database_ponto_digital.db")
                cursor = banco.cursor()
                cursor.execute("SELECT Nome FROM Marcacao_ponto WHERE \
                    Cod_funcionario = '"+cod_pesquisado+"'")
                nome = cursor.fetchall()
                nome = nome[0][0]
                if tela_pesquisa.radioButton_tudo.isChecked():
                    cursor.execute("SELECT Data, Entrada, Sai_almoco, \
                        Ent_almoco, Saida FROM Marcacao_Ponto WHERE \
                        Cod_funcionario = '"+cod_pesquisado+"'")
                    dados_bd_2 = cursor.fetchall()
                    lista_de_datas_tratadas = []
                    contador = 0
                    for item in range(0, len(dados_bd_2)):
                        for c in range(0, 1):
                            datas: str = dados_bd_2[item][c]
                            datas = str(datas)
                            d_0 = datas[0]
                            d_1 = datas[1]
                            d_2 = datas[2]
                            d_3 = datas[3]
                            d_5 = datas[5]
                            d_6 = datas[6]
                            d_8 = datas[8]
                            d_9 = datas[9]
                            data_tratada = str(
                                f"{d_8}{d_9}/{d_5}{d_6}/{d_0}{d_1}{d_2}{d_3}")
                            lista_de_datas_tratadas.append(data_tratada)
                    tela_pesquisa.tableWidget.setRowCount(len(dados_bd_2))
                    tela_pesquisa.tableWidget.setColumnCount(5)
                    # Iterador q lista os dados em uma table da tela_pesquisa
                    for i in range(0, len(dados_bd_2)):
                        for c in range(0, 5):
                            tela_pesquisa.tableWidget.setItem(
                                i, c, QtWidgets.QTableWidgetItem
                                (str(dados_bd_2[i][c])))
                            tela_pesquisa.tableWidget.setItem(
                                i, 0, QtWidgets.QTableWidgetItem
                                (str(lista_de_datas_tratadas[contador])))
                        contador += 1
                    banco.close()
                    tela_pesquisa.label_5.setText(f'Nome:  {nome}')
                    tela_pesquisa.pushButton_corrigir.setEnabled(True)
                if tela_pesquisa.radioButton_por_data.isChecked():
                    data_inicio = tela_pesquisa.lineEdit_2.text()
                    data_fim = tela_pesquisa.lineEdit_3.text()

                    di_0 = data_inicio[0]
                    di_1 = data_inicio[1]
                    di_3 = data_inicio[3]
                    di_4 = data_inicio[4]
                    di_6 = data_inicio[6]
                    di_7 = data_inicio[7]
                    di_8 = data_inicio[8]
                    di_9 = data_inicio[9]
                    data_inicio_tratada = str(
                        f"{di_6}{di_7}{di_8}{di_9}-{di_3}{di_4}-{di_0}{di_1}")
                    df_0 = data_fim[0]
                    df_1 = data_fim[1]
                    df_3 = data_fim[3]
                    df_4 = data_fim[4]
                    df_6 = data_fim[6]
                    df_7 = data_fim[7]
                    df_8 = data_fim[8]
                    df_9 = data_fim[9]
                    data_fim_tratada = str(
                        f"{df_6}{df_7}{df_8}{df_9}-{df_3}{df_4}-{df_0}{df_1}")
                    cursor.execute("SELECT Data, Entrada, Sai_almoco, \
                        Ent_almoco, Saida FROM \
                        Marcacao_Ponto WHERE Data BETWEEN \
                        '"+data_inicio_tratada+"' AND '"+data_fim_tratada+"'\
                        AND Cod_funcionario = '"+cod_pesquisado+"'")
                    dados_bd_3 = cursor.fetchall()
                    lista_de_datas_tratadas: list = []
                    contador: int = 0
                    for item_2 in range(0, len(dados_bd_3)):
                        for c in range(0, 1):
                            datas = dados_bd_3[item_2][c]
                            datas = str(datas)
                            d_0 = datas[0]
                            d_1 = datas[1]
                            d_2 = datas[2]
                            d_3 = datas[3]
                            d_5 = datas[5]
                            d_6 = datas[6]
                            d_8 = datas[8]
                            d_9 = datas[9]
                            data_tratada = str(
                                f"{d_8}{d_9}/{d_5}{d_6}/{d_0}{d_1}{d_2}{d_3}")
                            lista_de_datas_tratadas.append(data_tratada)
                    tela_pesquisa.tableWidget.setRowCount(len(dados_bd_3))
                    tela_pesquisa.tableWidget.setColumnCount(5)
                    # Iterador que lista os dados e as datas
                    # formatadas em uma table da "tela_pesquisa":
                    for i in range(0, len(dados_bd_3)):
                        for c in range(0, 5):
                            tela_pesquisa.tableWidget.setItem(
                                i, c, QtWidgets.QTableWidgetItem
                                (str(dados_bd_3[i][c]))
                                )
                            tela_pesquisa.tableWidget.setItem(
                                i, 0, QtWidgets.QTableWidgetItem
                                (str(lista_de_datas_tratadas[contador]))
                                )
                        contador += 1
                    banco.close()
                    tela_pesquisa.label_5.setText(
                        f'Nome: {nome} - Período:  {data_inicio} - {data_fim}'
                        )
                    tela_pesquisa.pushButton_corrigir.setEnabled(True)
                    tela_pesquisa.pushButton_pdf.setEnabled(True)
            except(Exception):
                box = QMessageBox()
                box.setWindowTitle('Filtrar por data')
                box.setText
                ('Não foram encontrados registros com as datas informadas!')
                box.setInformativeText('Preencha os campos \"Data inicial" e \
                    "Data final" com o período a ser consultado.')
                box.setIcon(QMessageBox.Warning)
                box.setStandardButtons(QMessageBox.Ok)
                box.exec_()

    except(Exception):
        if cod_pesquisado != dados_bd:
            box = QMessageBox()
            box.setWindowTitle('Código inválido!')
            box.setText
            ('O código pesquisado NÃO É VÁLIDO! Tente novamente!')
            box.setIcon(QMessageBox.Warning)
            box.setStandardButtons(QMessageBox.Ok)
            box.exec_()
            abre_tela_pesquisa()


def gerador_de_pdf() -> None:
    global endereco_salvar_pdf
    try:
        endereco_salvar_pdf = (f"C:/Users/PC/OneDrive/Área de Trabalho\
            /Folhas ponto/{nome}.PDF")
        if tela_pesquisa.radioButton_por_data.isChecked():
            box = QMessageBox()
            box.setWindowTitle('Gerar PDF')
            box.setText
            (f'Salvar dados de {nome}? Período: {data_inicio} - {data_fim}')
            box.setInformativeText(f'Salvar como: {endereco_salvar_pdf}')
            box.setIcon(QMessageBox.Question)
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            resposta = box.exec_()
            if resposta == QMessageBox.No:
                abre_tela_pesquisa()

            elif resposta == QMessageBox.Yes:
                banco = sqlite3.connect('database_ponto_digital.db')
                cursor = banco.cursor()
                cursor.execute("SELECT Data, Entrada, Sai_almoco, Ent_almoco, \
                    Saida FROM Marcacao_Ponto WHERE Data \
                    BETWEEN '"+data_inicio_tratada+"' AND \
                    '"+data_fim_tratada+"' AND \
                    Cod_funcionario = '"+cod_pesquisado+"'")
                dados_bd_4 = cursor.fetchall()
                banco.close()

                # Cria uma lista com as datas formatadas
                lista_de_datas_tratadas_2 = []
                contador_2 = 0
                for item in range(0, len(dados_bd_4)):
                    for c in range(0, 1):
                        datas_2 = dados_bd_4[item][c]
                        datas_2 = str(datas_2)
                        d00 = datas_2[0]
                        d10 = datas_2[1]
                        d20 = datas_2[2]
                        d30 = datas_2[3]
                        d50 = datas_2[5]
                        d60 = datas_2[6]
                        d80 = datas_2[8]
                        d90 = datas_2[9]
                        data_tratada_2 = str(
                            f"{d80}{d90}/{d50}{d60}/{d00}{d10}{d20}{d30}"
                            )
                        lista_de_datas_tratadas_2.append(data_tratada_2)

                # Cria uma lista com a SOMA das horas
                banco = sqlite3.connect('database_ponto_digital.db')
                cursor = banco.cursor()
                cursor.execute("SELECT Id FROM Marcacao_Ponto WHERE Data \
                    BETWEEN '"+data_inicio_tratada+"' AND \
                    '"+data_fim_tratada+"' AND \
                    Cod_funcionario = '"+cod_pesquisado+"'")
                dados_bd_6 = cursor.fetchall()
                banco.close()
                lista_somar_hora = []
                contador = -1
                for id in dados_bd_6:
                    contador += 1
                    i = str(dados_bd_6[contador][0])
                    try:
                        banco = sqlite3.connect('database_ponto_digital.db')
                        cursor = banco.cursor()
                        cursor.execute("SELECT Entrada,Sai_almoco,Ent_almoco, \
                            Saida FROM Marcacao_Ponto WHERE Id = '"+i+"'")
                        dados_bd_5 = cursor.fetchall()
                        entrada = dados_bd_5[0][0]
                        sai_almoco = dados_bd_5[0][1]
                        ent_almoco = dados_bd_5[0][2]
                        saida = dados_bd_5[0][3]
                        banco.close()
                        # Entrada
                        e0 = entrada[0]
                        e1 = entrada[1]
                        e3 = entrada[3]
                        e4 = entrada[4]
                        entrada_h = e0 + e1
                        entrada_h = int(entrada_h)
                        entrada_m = e3 + e4
                        entrada_m = int(entrada_m)
                        hora_entrada = datetime(
                            2022, 1, 29, entrada_h, entrada_m
                            )
                        hora_entrada.time()
                        # Sai_almoco
                        s_a0 = sai_almoco[0]
                        s_a1 = sai_almoco[1]
                        s_a3 = sai_almoco[3]
                        s_a4 = sai_almoco[4]
                        sai_almoco_h = s_a0 + s_a1
                        sai_almoco_h = int(sai_almoco_h)
                        sai_almoco_m = s_a3 + s_a4
                        sai_almoco_m = int(sai_almoco_m)
                        hora_sai_almoco = datetime(
                            2022, 1, 29, sai_almoco_h, sai_almoco_m
                            )
                        hora_sai_almoco.time()

                        resultado_1 = hora_sai_almoco - hora_entrada
                        resultado_geral_1 = str(resultado_1)
                    except(Exception):
                        resultado_geral_1 = 'Primeiro_erro'
                    try:
                        # Ent_almoco
                        e_a0 = ent_almoco[0]
                        e_a1 = ent_almoco[1]
                        e_a3 = ent_almoco[3]
                        e_a4 = ent_almoco[4]
                        ent_almoco_h = e_a0 + e_a1
                        ent_almoco_h = int(ent_almoco_h)
                        ent_almoco_m = e_a3 + e_a4
                        ent_almoco_m = int(ent_almoco_m)
                        hora_ent_almoco = datetime(
                            2022, 1, 29, ent_almoco_h, ent_almoco_m
                            )
                        hora_ent_almoco.time()
                        # Saída
                        s0 = saida[0]
                        s1 = saida[1]
                        s3 = saida[3]
                        s4 = saida[4]
                        saida_h = s0 + s1
                        saida_h = int(saida_h)
                        saida_m = s3 + s4
                        saida_m = int(saida_m)
                        hora_saida = datetime(2022, 1, 29, saida_h, saida_m)
                        hora_saida.time()

                        resultado_2 = hora_saida - hora_ent_almoco
                        resultado_3 = resultado_1 + resultado_2
                        resultado_geral_2 = str(resultado_3)
                    except(Exception):
                        resultado_geral_2 = 'SegundoErro'
                    if resultado_geral_2 != 'SegundoErro':
                        lista_somar_hora.append(str(resultado_geral_2))
                    elif (resultado_geral_1 != 'Primeiro_erro') and\
                         (resultado_geral_2 == 'SegundoErro'):
                        lista_somar_hora.append(str(resultado_geral_1))
                    elif resultado_geral_2 == 'SegundoErro':
                        lista_somar_hora.append('Incompleto!')

                pdf = canvas.Canvas(endereco_salvar_pdf)

                # Cabeçalho
                pdf.setFont("Helvetica", 18)
                pdf.drawString(250, 770, "Folha ponto")
                pdf.setFont("Helvetica", 12)
                pdf.drawString(50, 730, f'Nome: {nome}')
                pdf.drawString(50, 714, f"Período:  \
                    {data_inicio} - {data_fim}")

                # Colunas
                pdf.setFont("Courier", 12)
                pdf.drawString(45, 680, "DATA")
                pdf.drawString(145, 680, "ENTRADA")
                pdf.drawString(220, 680, "SAÍDA")
                pdf.drawString(295, 680, "ENTRADA")
                pdf.drawString(370, 680, "SAÍDA")
                pdf.drawString(445, 680, "SOMA")

                y = 0
                for i in range(0, len(dados_bd_4)):
                    y += 16
                    pdf.drawString
                    (45, 680 - y, str(lista_de_datas_tratadas_2[contador_2]))
                    pdf.drawString(145, 680 - y, str(dados_bd_4[i][1]))
                    pdf.drawString(220, 680 - y, str(dados_bd_4[i][2]))
                    pdf.drawString(295, 680 - y, str(dados_bd_4[i][3]))
                    pdf.drawString(370, 680 - y, str(dados_bd_4[i][4]))
                    pdf.drawString
                    (445, 680 - y, str(lista_somar_hora[contador_2]))
                    contador_2 += 1

                pdf.save()
                box = QMessageBox()
                box.setWindowTitle('Gerar PDF')
                box.setText('Documento salvo com sucesso!')
                box.setIcon(QMessageBox.Information)
                box.setStandardButtons(QMessageBox.Ok)
                box.exec_()

        elif tela_pesquisa.radioButton_tudo.isChecked():
            box = QMessageBox()
            box.setWindowTitle('Gerar PDF')
            box.setText('Não foi possível gerar o PDF!')
            box.setInformativeText('É necessário pesquisar com o campo \
                "Filtrar por data" selecionado.')

            box.setIcon(QMessageBox.Warning)
            box.setStandardButtons(QMessageBox.Ok)
            box.exec_()

    except(Exception):
        box = QMessageBox()
        box.setWindowTitle('Gerar PDF')
        box.setText('Não foi possível gerar o PDF!')
        box.setInformativeText('Preencha corretamente todos os campos.')
        box.setIcon(QMessageBox.Warning)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()


# Função que pega os dados de uma linha selecionada na tela de pesquisa
# e os coloca na tela de edição de dados
def corrigir_marcacoes() -> None:
    try:
        if tela_pesquisa.radioButton_por_data.isChecked():
            banco = sqlite3.connect("database_ponto_digital.db")
            cursor = banco.cursor()
            cursor.execute("SELECT Nome FROM Marcacao_Ponto WHERE \
                 Data BETWEEN '"+data_inicio_tratada+"' \
                AND '"+data_fim_tratada+"' \
                AND Cod_funcionario = '"+cod_pesquisado+"'")
            nome = cursor.fetchall()
            nome = nome[0][0]

            linha = tela_pesquisa.tableWidget.currentRow()
            # Se conecta com o database e resgata todos os "Id's" de marcações
            # de seu respectivo "Cod_funcionario"
            # Depois busca o restante dos dados
            banco = sqlite3.connect("database_ponto_digital.db")
            cursor = banco.cursor()
            cursor.execute("SELECT Id FROM Marcacao_Ponto WHERE \
                Data BETWEEN '"+data_inicio_tratada+"' AND \
                '"+data_fim_tratada+"' \
                AND Cod_funcionario = '"+cod_pesquisado+"'")
            dados_lidos = cursor.fetchall()
            valor_id = str(dados_lidos[linha][0])
            global numero_id
            numero_id = valor_id
            cursor.execute("SELECT Data, Entrada, Sai_almoco, Ent_almoco, \
                Saida FROM Marcacao_Ponto WHERE Id = '"+valor_id+"'")
            dados_bd = cursor.fetchall()
            banco.close()

            # Busca os dados em cada posição da tupla selecionada no database
            # e os armazena em suas respectivas variáveis
            data = dados_bd[0][0]
            entrada = dados_bd[0][1]
            sai_almoco = dados_bd[0][2]
            ent_almoco = dados_bd[0][3]
            saida = dados_bd[0][4]
            d_0 = data[0]
            d_1 = data[1]
            d_2 = data[2]
            d_3 = data[3]
            d_5 = data[5]
            d_6 = data[6]
            d_8 = data[8]
            d_9 = data[9]
            data_tratada = str(
                f"{d_8}{d_9}/{d_5}{d_6}/{d_0}{d_1}{d_2}{d_3}"
                )
            entrada = str(entrada)
            sai_almoco = str(sai_almoco)
            ent_almoco = str(ent_almoco)
            saida = str(saida)
            entrada = entrada.replace('None', '')
            sai_almoco = sai_almoco.replace('None', '')
            ent_almoco = ent_almoco.replace('None', '')
            saida = saida.replace('None', '')

            # A partir daqui a tela de edição de dados é aberta
            tela_editar_dados.show()
            tela_editar_dados.label.setText(f'Corrigir marcações de: {nome}')

            # As linhas de edição recebem os dados,
            # armazenados em variáveis, da linha selecionada na tela_pesquisa
            tela_editar_dados.lineEdit.setText(str(data_tratada))
            tela_editar_dados.lineEdit_2.setText(str(entrada))
            tela_editar_dados.lineEdit_3.setText(str(sai_almoco))
            tela_editar_dados.lineEdit_4.setText(str(ent_almoco))
            tela_editar_dados.lineEdit_5.setText(str(saida))

        if tela_pesquisa.radioButton_tudo.isChecked():
            banco = sqlite3.connect("database_ponto_digital.db")
            cursor = banco.cursor()
            cursor.execute("SELECT Nome FROM Marcacao_Ponto WHERE \
                Cod_funcionario = '"+cod_pesquisado+"'")
            nome = cursor.fetchall()
            nome = nome[0][0]

            linha = tela_pesquisa.tableWidget.currentRow()
            # Se conecta com o database e resgata todos os "Id's" de marcações
            # de seu respectivo "Cod_funcionario"
            # Depois busca o restante dos dados
            banco = sqlite3.connect("database_ponto_digital.db")
            cursor = banco.cursor()
            cursor.execute("SELECT Id FROM Marcacao_Ponto WHERE \
                Cod_funcionario = '"+cod_pesquisado+"'")
            dados_lidos = cursor.fetchall()
            valor_id = str(dados_lidos[linha][0])
            numero_id = valor_id
            cursor.execute("SELECT Data, Entrada, Sai_almoco, Ent_almoco, \
                Saida FROM Marcacao_Ponto WHERE Id = '"+valor_id+"'")
            dados_bd = cursor.fetchall()
            banco.close()

            # Busca os dados em cada posição da tupla selecionada no database,
            # e os armazena em suas respectivas variáveis
            data = dados_bd[0][0]
            entrada = dados_bd[0][1]
            sai_almoco = dados_bd[0][2]
            ent_almoco = dados_bd[0][3]
            saida = dados_bd[0][4]
            d_0 = data[0]
            d_1 = data[1]
            d_2 = data[2]
            d_3 = data[3]
            d_5 = data[5]
            d_6 = data[6]
            d_8 = data[8]
            d_9 = data[9]
            data_tratada = str(
                f"{d_8}{d_9}/{d_5}{d_6}/{d_0}{d_1}{d_2}{d_3}"
                )

            entrada = str(entrada)
            sai_almoco = str(sai_almoco)
            ent_almoco = str(ent_almoco)
            saida = str(saida)
            entrada = entrada.replace('None', '')
            sai_almoco = sai_almoco.replace('None', '')
            ent_almoco = ent_almoco.replace('None', '')
            saida = saida.replace('None', '')

            # A partir daqui a tela de edição de dados é aberta
            tela_editar_dados.show()
            tela_editar_dados.label.setText(f'Corrigir marcações de: {nome}')

            # As linhas de edição recebem os dados,
            # armazenados em variáveis, da linha selecionada na tela_pesquisa
            tela_editar_dados.lineEdit.setText(str(data_tratada))
            tela_editar_dados.lineEdit_2.setText(str(entrada))
            tela_editar_dados.lineEdit_3.setText(str(sai_almoco))
            tela_editar_dados.lineEdit_4.setText(str(ent_almoco))
            tela_editar_dados.lineEdit_5.setText(str(saida))
    except(Exception):
        box = QMessageBox()
        box.setWindowTitle('Corrigir marcações')
        box.setText('Não foi possível editar os dados!')
        box.setInformativeText
        ('Preencha corretamente todos os campos e faça uma pesquisa.')
        box.setIcon(QMessageBox.Warning)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()


# Função que é chamada quando é pressionado o botão "Salvar" na tela de edição
# Faz a alteração no database.
def salvar_dados_editados() -> None:
    box = QMessageBox()
    box.setWindowTitle('Salvar dados')
    box.setText(f'Salvar alterações de {nome}?')
    box.setIcon(QMessageBox.Question)
    box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    resposta = box.exec_()
    # Cada variável recebe de volta as linhas já alteradas na tela de edição
    entrada = str(tela_editar_dados.lineEdit_2.text())
    sai_almoco = str(tela_editar_dados.lineEdit_3.text())
    ent_almoco = str(tela_editar_dados.lineEdit_4.text())
    saida = str(tela_editar_dados.lineEdit_5.text())
    if resposta == QMessageBox.No:
        sair_da_tela_editar_dados()
    elif resposta == QMessageBox.Yes:
        # Se conecta com o database e faz o commit das alterações realizadas
        try:
            banco = sqlite3.connect("database_ponto_digital.db")
            cursor = banco.cursor()
            cursor.execute("UPDATE Marcacao_Ponto SET \
                Entrada = '"+entrada+"', \
                Sai_almoco = '"+sai_almoco+"', \
                Ent_almoco = '"+ent_almoco+"', \
                Saida = '"+saida+"' WHERE Id = '"+numero_id+"'")
            banco.commit()
            banco.close()
            tela_editar_dados.close()
            consultar_marcacoes()
            box = QMessageBox()
            box.setWindowTitle('Correção de dados')
            box.setText('Dados editados com sucesso!')
            box.setIcon(QMessageBox.Information)
            box.setStandardButtons(QMessageBox.Ok)
            box.exec_()
        except(Exception):
            box = QMessageBox()
            box.setWindowTitle('Correção de dados')
            box.setText(
                'Não foi possível salvar a edição realizada! Tente novamente'
                )
            box.setIcon(QMessageBox.Critical)
            box.setStandardButtons(QMessageBox.Ok)
            box.exec_()


def sair_da_tela_editar_dados() -> None:
    tela_editar_dados.close()


# Funções para abertura e fechamento de telas.
# Também limpa as labels e os campos de input.
def abre_tela_pesquisa() -> None:
    primeira_tela.close()
    tela_pesquisa.show()
    tela_pesquisa.label_5.setText('')
    tela_pesquisa.lineEdit.setText('')
    tela_pesquisa.lineEdit_2.setText('')
    tela_pesquisa.lineEdit_3.setText('')
    tela_pesquisa.pushButton_corrigir.setEnabled(False)
    tela_pesquisa.pushButton_pdf.setEnabled(False)
    tela_pesquisa.radioButton_tudo.setChecked(True)
    tela_pesquisa.tableWidget.setRowCount(0)
    tela_pesquisa.tableWidget.setColumnCount(5)
    # Iterador que lista os dados em uma "table" da tela pesquisa:
    for i in range(0):
        for c in range(0, 5):
            tela_pesquisa.tableWidget.setItem
            (i, c, QtWidgets.QTableWidgetItem(''[i][c]))


def sair_da_tela_de_pesquisa() -> None:
    tela_editar_dados.close()
    tela_pesquisa.close()
    primeira_tela.show()
    primeira_tela.label_2.setText(f'{mostra_hora()}')
    primeira_tela.lineEdit_3.setText("")
    primeira_tela.lineEdit_2.setText("")


def abre_tela_cadastro() -> None:
    tela_cadastro.lineEdit.setText('')
    tela_cadastro.lineEdit_2.setText('')
    tela_cadastro.lineEdit_3.setText('')
    tela_cadastro.lineEdit_4.setText('')
    tela_cadastro.lineEdit_5.setText('')
    primeira_tela.close()
    tela_cadastro.show()


def sair_da_tela_de_cadastro() -> None:
    tela_cadastro.lineEdit.setText('')
    tela_cadastro.lineEdit_2.setText('')
    tela_cadastro.lineEdit_3.setText('')
    tela_cadastro.lineEdit_4.setText('')
    tela_cadastro.lineEdit_5.setText('')
    tela_cadastro.label_11.setText('')
    tela_cadastro.close()
    primeira_tela.show()


def fechar_programa() -> None:
    tela_editar_dados.close()
    tela_cadastro.close()
    tela_pesquisa.close()
    primeira_tela.close()


app = QtWidgets.QApplication([])

# variáveis recebem os arquivos de cada tela
primeira_tela = uic.loadUi("primeira_tela.ui")
tela_cadastro = uic.loadUi("tela_cadastro.ui")
tela_pesquisa = uic.loadUi("tela_pesquisa.ui")
tela_editar_dados = uic.loadUi("tela_editar_dados.ui")

# Botões e labels da tela de login.
primeira_tela.button_entrada.clicked.connect(marca_entrada)
primeira_tela.button_saida.clicked.connect(marca_saida)
primeira_tela.button_cadastrar_novo_usuario.clicked.connect(abre_tela_cadastro)
primeira_tela.button_pesquisar.clicked.connect(abre_tela_pesquisa)
# primeira_tela.button_editar_cadastro.clicked.connect(corrigir_marcacoes)

# Botões e labels da tela de cadastro.
tela_cadastro.pushButton.clicked.connect(cadastrar_usuarios)
tela_cadastro.pushButton_2.clicked.connect(sair_da_tela_de_cadastro)

# Botões e labels da tela de pesquisa de dados
tela_pesquisa.pushButton_pesquisa.clicked.connect(consultar_marcacoes)
tela_pesquisa.pushButton_voltar.clicked.connect(sair_da_tela_de_pesquisa)
tela_pesquisa.pushButton_corrigir.clicked.connect(corrigir_marcacoes)
tela_pesquisa.pushButton_pdf.clicked.connect(gerador_de_pdf)
tela_pesquisa.actionSalvar.triggered.connect(gerador_de_pdf)
tela_pesquisa.actionFechar_programa.triggered.connect(sair_da_tela_de_pesquisa)
# tela_pesquisa.actionSair.triggered.connect(fechar_programa)

# Botões e labels da tela de edição de dados.
tela_editar_dados.pushButton_Salvar.clicked.connect(salvar_dados_editados)
tela_editar_dados.pushButton_Voltar.clicked.connect(sair_da_tela_editar_dados)

# Início do programa.
primeira_tela.show()
primeira_tela.label_2.setText(f'{mostra_hora()}')
app.exec()
