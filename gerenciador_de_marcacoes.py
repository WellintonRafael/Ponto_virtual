import gerenciador_de_telas
import run_sql
import sqlite3
import funcoes

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

from reportlab.pdfgen import canvas


def consultar_marcacoes() -> None:
    """
        Função que busca os dados de um funcionário através do
        'Cod_funcionario' e os exibe na 'tela_pesquisa':
    """
    global nome_pesquisado
    global nome_selecionado
    global data_inicio
    global data_fim
    try:
        nome_selecionado = gerenciador_de_telas.tela_pesquisa.comboBox.currentText()
        nome_pesquisado = run_sql.select_nome(nome_selecionado)
        nome_pesquisado.sort()
        if gerenciador_de_telas.tela_pesquisa.radioButton_tudo.isChecked():
            dados_bd = run_sql.select_dados_marcacao_ponto(nome_selecionado)
            gerenciador_de_telas.tela_pesquisa.label_5.setText(f'Nome:  {nome_selecionado}')
        if gerenciador_de_telas.tela_pesquisa.radioButton_por_data.isChecked():
            try:
                data_inicio = gerenciador_de_telas.tela_pesquisa.lineEdit_2.text()
                data_fim = gerenciador_de_telas.tela_pesquisa.lineEdit_3.text()
                dados_bd = run_sql.select_dados_marcacao_ponto_com_filtro(nome_selecionado, data_inicio, data_fim)
                gerenciador_de_telas.tela_pesquisa.pushButton_pdf.setEnabled(True)
                gerenciador_de_telas.tela_pesquisa.label_5.setText(
                    f'Nome: {nome_selecionado} - Período:  {data_inicio} - {data_fim}'
                    )
            except(Exception) as e:
                print(e)
                box = QMessageBox()
                box.setWindowTitle('Filtrar por data')
                box.setText(
                    'Não foram encontrados registros com as datas informadas!'
                )
                box.setInformativeText(
                    'Preencha os campos "Data inicial" e "Data final" com o período a ser consultado.'
                )
                box.setIcon(QMessageBox.Warning)
                box.setStandardButtons(QMessageBox.Ok)
                box.exec_()
        gerenciador_de_telas.tela_pesquisa.tableWidget.setRowCount(len(dados_bd))
        gerenciador_de_telas.tela_pesquisa.tableWidget.setColumnCount(8)
        gerenciador_de_telas.tela_pesquisa.pushButton_corrigir.setEnabled(True)
        # Iterador q lista os dados na table da tela_pesquisa
        for i in range(0, len(dados_bd)):
            for c in range(0, 8):
                gerenciador_de_telas.tela_pesquisa.tableWidget.setItem(
                    i, c, QtWidgets.QTableWidgetItem
                    (str(dados_bd[i][c])))
    except(Exception) as e:
        box = QMessageBox()
        box.setWindowTitle('Ops, aconteceu um erro!')
        box.setText(
            f'{e}'
        )
        box.setIcon(QMessageBox.Warning)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()
        funcoes.abre_tela_pesquisa()


def corrigir_marcacoes() -> None:
    """
        Função que pega os dados de uma linha selecionada na tela de pesquisa
        e os coloca na tela de edição de dados
    """
    global entrada_antiga
    global sai_almoco_antiga
    global ent_almoco_antiga
    global saida_antiga
    global ent_extra_antiga
    global sai_extra_antiga
    global alteracoes_list
    try:
        if gerenciador_de_telas.tela_pesquisa.radioButton_por_data.isChecked():
            linha = gerenciador_de_telas.tela_pesquisa.tableWidget.currentRow()
            dados_a_serem_editados = run_sql.select_dados_marcacao_ponto_com_filtro(nome_selecionado, data_inicio, data_fim)
            dados_da_linha = dados_a_serem_editados[linha]

        if gerenciador_de_telas.tela_pesquisa.radioButton_tudo.isChecked():
            linha = gerenciador_de_telas.tela_pesquisa.tableWidget.currentRow()
            dados_a_serem_editados = run_sql.select_dados_marcacao_ponto(nome_selecionado)
            dados_da_linha = dados_a_serem_editados[linha]

        # Busca os dados em cada posição da tupla selecionada no database,
        # e os armazena em suas respectivas variáveis
        data = str(dados_da_linha[0])
        entrada_antiga = str(dados_da_linha[1])
        sai_almoco_antiga = str(dados_da_linha[2])
        ent_almoco_antiga = str(dados_da_linha[3])
        saida_antiga = str(dados_da_linha[4])
        ent_extra_antiga = str(dados_da_linha[5])
        sai_extra_antiga = str(dados_da_linha[6])

        # alteracoes_list = str(dados_da_linha[0])
        # alteracoes_list = list(alteracoes_list)

        # A partir daqui a tela de edição de dados é aberta
        gerenciador_de_telas.tela_editar_dados.show()
        gerenciador_de_telas.tela_editar_dados.label.setText(f'Corrigir marcações de: {nome_selecionado}')

        # As linhas de edição recebem os dados,
        # armazenados em variáveis, da linha selecionada na tela_pesquisa
        gerenciador_de_telas.tela_editar_dados.lineEdit.setText(data)
        gerenciador_de_telas.tela_editar_dados.lineEdit_2.setText(entrada_antiga)
        gerenciador_de_telas.tela_editar_dados.lineEdit_3.setText(sai_almoco_antiga)
        gerenciador_de_telas.tela_editar_dados.lineEdit_4.setText(ent_almoco_antiga)
        gerenciador_de_telas.tela_editar_dados.lineEdit_5.setText(saida_antiga)
        gerenciador_de_telas.tela_editar_dados.lineEdit_6.setText(ent_extra_antiga)
        gerenciador_de_telas.tela_editar_dados.lineEdit_7.setText(sai_extra_antiga)

    except(Exception):
        box = QMessageBox()
        box.setWindowTitle('Corrigir marcações')
        box.setText('Não foi possível editar os dados!')
        box.setInformativeText('Preencha corretamente todos os campos e faça uma pesquisa.')
        box.setIcon(QMessageBox.Warning)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()


def salvar_dados_editados() -> None:
    """
        Função que é chamada quando é pressionado o botão "Salvar" na tela de edição
        Faz a alteração no database.
    """
    box = QMessageBox()
    box.setWindowTitle('Salvar dados')
    box.setText(f'Salvar alterações de {nome_selecionado}?')
    box.setIcon(QMessageBox.Question)
    box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    resposta = box.exec_()
    if resposta == QMessageBox.No:
        funcoes.sair_da_tela_editar_dados()
    elif resposta == QMessageBox.Yes:
        # Cada variável recebe de volta as linhas já alteradas na tela de edição
        entrada = str(gerenciador_de_telas.tela_editar_dados.lineEdit_2.text())
        sai_almoco = str(gerenciador_de_telas.tela_editar_dados.lineEdit_3.text())
        ent_almoco = str(gerenciador_de_telas.tela_editar_dados.lineEdit_4.text())
        saida = str(gerenciador_de_telas.tela_editar_dados.lineEdit_5.text())
        ent_extra = str(gerenciador_de_telas.tela_editar_dados.lineEdit_6.text())
        sai_extra = str(gerenciador_de_telas.tela_editar_dados.lineEdit_7.text())

        lista_de_horas = [entrada, sai_almoco, ent_almoco, saida, ent_extra, sai_extra] 

        lista_de_horas_validadas = []
        for item in lista_de_horas:
            lista_de_horas_validadas.append(funcoes.validar_hora(item))
        print(lista_de_horas_validadas)

        if False in lista_de_horas_validadas:
            box = QMessageBox()
            box.setWindowTitle('Corrigir marcações')
            box.setText('Não foi possível editar os dados!')
            box.setInformativeText('O formato de horas está incorreto.')
            box.setIcon(QMessageBox.Warning)
            box.setStandardButtons(QMessageBox.Ok)
            box.exec_() 
            funcoes.abre_tela_editar_dados()
            return
        else:
            variaveis = [entrada, sai_almoco, ent_almoco, saida, ent_extra, sai_extra]
            correspondentes = [entrada_antiga, sai_almoco_antiga, ent_almoco_antiga, saida_antiga, ent_extra_antiga, sai_extra_antiga]
            for i in range(0, len(variaveis)):
                if variaveis[i] == correspondentes[i]:
                    pass
                else: 
                    correspondentes[i] = variaveis[i] + '*'
            print(correspondentes)
            
        # # Se conecta com o database e faz o commit das alterações realizadas
        #     gerenciador_de_telas.tela_editar_dados.close()
        #     consultar_marcacoes()
        #     box = QMessageBox()
        #     box.setWindowTitle('Correção de dados')
        #     box.setText('Dados editados com sucesso!')
        #     box.setIcon(QMessageBox.Information)
        #     box.setStandardButtons(QMessageBox.Ok)
        #     box.exec_()
        # except(Exception):
        #     box = QMessageBox()
        #     box.setWindowTitle('Correção de dados')
        #     box.setText('Não foi possível salvar a edição! Tente novamente')
        #     box.setIcon(QMessageBox.Critical)
        #     box.setStandardButtons(QMessageBox.Ok)
        #     box.exec_()


def gerador_de_pdf() -> None:
    try:
        endereco_salvar_pdf = (
            f"C:/Users/PC/OneDrive/Área de Trabalho/Folhas ponto/{nome_selecionado}.PDF"
        )
        if gerenciador_de_telas.tela_pesquisa.radioButton_por_data.isChecked():
            box = QMessageBox()
            box.setWindowTitle('Gerar PDF')
            box.setText(
                f'Salvar dados de {nome_selecionado}? Período: {data_inicio} - {data_fim}'
            )
            box.setInformativeText(f'Salvar como: {endereco_salvar_pdf}')
            box.setIcon(QMessageBox.Question)
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            resposta = box.exec_()
            if resposta == QMessageBox.No:
                funcoes.abre_tela_pesquisa()

            elif resposta == QMessageBox.Yes:
                # banco = sqlite3.connect('database_ponto_digital.db')
                # cursor = banco.cursor()
                # cursor.execute(
                #     "SELECT STRFTIME('%d/%m/%Y',Data), Entrada, Sai_almoco, Ent_almoco, \
                #     Saida FROM Marcacao_ponto WHERE Data \
                #     BETWEEN '"+data_inicio+"' AND \
                #     '"+data_fim+"' AND \
                #     Cod_funcionario = '"+nome_selecionado+"'"
                # )
                # dados_bd = cursor.fetchall()
                # banco.close()

                # Cria uma lista com as datas formatadas
                lista_de_datas_tratadas = []


                



                for item in range(0, len(dados_bd)):
                    for c in range(0, 1):
                        datas = str(dados_bd[item][c])
                        lista_de_datas_tratadas.append(datas)

                # Cria uma lista com a SOMA das horas
                banco = sqlite3.connect('database_ponto_digital.db')
                cursor = banco.cursor()
                cursor.execute(
                    "SELECT Id FROM Marcacao_ponto WHERE Data \
                    BETWEEN '"+data_inicio+"' AND \
                    '"+data_fim+"' AND \
                    Cod_funcionario = '"+nome_selecionado+"'"
                )
                dados_bd_6 = cursor.fetchall()
                banco.close()
                lista_somar_hora = []
                contador = -1
                for _ in dados_bd_6:
                    contador += 1
                    i = str(dados_bd_6[contador][0])
                    try:
                        banco = sqlite3.connect('database_ponto_digital.db')
                        cursor = banco.cursor()
                        cursor.execute(
                            "SELECT Entrada,Sai_almoco,Ent_almoco, \
                            Saida,Foi_Editado FROM Marcacao_ponto WHERE Id = '"+i+"'"
                        )
                        dados_bd_5 = cursor.fetchall()
                        entrada = dados_bd_5[0][0]
                        sai_almoco = dados_bd_5[0][1]
                        ent_almoco = dados_bd_5[0][2]
                        saida = dados_bd_5[0][3]
                        banco.close()
                        # Entrada
                        entrada = entrada.split(':')
                        entrada_h = int(entrada[0])
                        entrada_m = int(entrada[1])
                        hora_entrada = funcoes.datetime(
                            2022, 1, 29, entrada_h, entrada_m
                        )
                        hora_entrada.time()
                        # Sai_almoco
                        sai_almoco = sai_almoco.split(':')
                        sai_almoco_h = int(sai_almoco[0])
                        sai_almoco_m = int(sai_almoco[1])
                        hora_sai_almoco = funcoes.datetime(
                            2022, 1, 29, sai_almoco_h, sai_almoco_m
                        )
                        hora_sai_almoco.time()

                        resultado_1 = hora_sai_almoco - hora_entrada
                        resultado_geral_1 = str(resultado_1)
                    except(Exception):
                        resultado_geral_1 = 'Primeiro_erro'
                    try:
                        # Ent_almoco
                        ent_almoco = ent_almoco.split(':')
                        ent_almoco_h = int(ent_almoco[0])
                        ent_almoco_m = int(ent_almoco[1])
                        hora_ent_almoco = funcoes.datetime(
                            2022, 1, 29, ent_almoco_h, ent_almoco_m
                        )
                        hora_ent_almoco.time()
                        # Saída
                        saida = saida.split(':')
                        saida_h = int(saida[0])
                        saida_m = int(saida[1])
                        hora_saida = funcoes.datetime(2022, 1, 29, saida_h, saida_m)
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
                pdf.drawString(50, 730, f'Nome: {nome_selecionado}')
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
                contador_2 = 0
                for i in range(0, len(dados_bd)):
                    y += 16
                    pdf.drawString(45, 680 - y, str(lista_de_datas_tratadas[contador_2]))
                    pdf.drawString(145, 680 - y, str(dados_bd[i][1]))
                    pdf.drawString(220, 680 - y, str(dados_bd[i][2]))
                    pdf.drawString(295, 680 - y, str(dados_bd[i][3]))
                    pdf.drawString(370, 680 - y, str(dados_bd[i][4]))
                    pdf.drawString(445, 680 - y, str(lista_somar_hora[contador_2]))
                    contador_2 += 1

                pdf.save()
                box = QMessageBox()
                box.setWindowTitle('Gerar PDF')
                box.setText('Documento salvo com sucesso!')
                box.setIcon(QMessageBox.Information)
                box.setStandardButtons(QMessageBox.Ok)
                box.exec_()

        elif gerenciador_de_telas.tela_pesquisa.radioButton_tudo.isChecked():
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
