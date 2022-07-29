import gerenciador_de_telas
import run_sql

from PyQt5.QtWidgets import QMessageBox


def abre_tela_cadastro() -> None:
    gerenciador_de_telas.tela_cadastro.lineEdit_nome.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_cpf.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_cargo.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_depto.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_login.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_senha.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_confirmar_senha.setText('')
    gerenciador_de_telas.primeira_tela.close()
    gerenciador_de_telas.tela_cadastro.show()


def sair_da_tela_de_cadastro() -> None:
    gerenciador_de_telas.tela_cadastro.lineEdit_nome.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_cpf.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_cargo.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_depto.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_login.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_senha.setText('')
    gerenciador_de_telas.tela_cadastro.lineEdit_confirmar_senha.setText('')
    gerenciador_de_telas.tela_cadastro.label_11.setText('')
    gerenciador_de_telas.tela_cadastro.close()
    gerenciador_de_telas.primeira_tela.show()


def cadastrar_usuarios() -> None:
    """
        Verifica se os dados são suficientes para cadastrar um novo usuário,
        e se a condição for True, insere esse usuário como uma tupla no database.
    """
    cpf = gerenciador_de_telas.tela_cadastro.lineEdit_cpf.text()
    nome = gerenciador_de_telas.tela_cadastro.lineEdit_nome.text()
    cargo = gerenciador_de_telas.tela_cadastro.lineEdit_cargo.text()
    login = gerenciador_de_telas.tela_cadastro.lineEdit_login.text()
    senha = gerenciador_de_telas.tela_cadastro.lineEdit_senha.text()
    confirmar_senha = gerenciador_de_telas.tela_cadastro.lineEdit_confirmar_senha.text()

    cargo = cargo.upper()
    lista_de_cargos = ['RECEPCIONISTA', 'ADMINISTRADOR', 'CAMAREIRA', 'GERENTE']

    if nome != '' and cpf.isnumeric() == True and cargo in lista_de_cargos and len(cpf) == 11:
        if ((senha == confirmar_senha) and
        (senha != '') and
        (login != '')):

            try:

                # Talvez haja a necessidade de criar tabela
                # cursor.execute(
                #     "CREATE TABLE IF NOT EXISTS TB_FUNCIONARIOS \
                #     (Cod_funcionario text,Nome text,Login text,Senha text)"
                # )
 
                deparatamento = 15


                dados_cadastrais = run_sql.insert_into_tb_funcionario(cpf, nome, cargo, deparatamento)
                if dados_cadastrais:
                    dados_de_login = run_sql.insert_into_login(login, senha, nome)
                    if dados_de_login:
                        box = QMessageBox()
                        box.setWindowTitle('Cadastrar')
                        box.setText('Cadastro realizado com sucesso!')
                        box.setIcon(QMessageBox.Information)
                        box.setStandardButtons(QMessageBox.Ok)
                        box.exec_()
                        gerenciador_de_telas.tela_cadastro.label_11.setText('')
                        gerenciador_de_telas.tela_cadastro.lineEdit_nome.setText('')
                        gerenciador_de_telas.tela_cadastro.lineEdit_cpf.setText('')
                        gerenciador_de_telas.tela_cadastro.lineEdit_cargo.setText('')
                        gerenciador_de_telas.tela_cadastro.lineEdit_login.setText('')
                        gerenciador_de_telas.tela_cadastro.lineEdit_senha.setText('')
                        gerenciador_de_telas.tela_cadastro.lineEdit_confirmar_senha.setText('')
            except(Exception):
                gerenciador_de_telas.tela_cadastro.label_11.setText(
                    "Erro ao inserir dados! Refaça a operação!")
        if senha != confirmar_senha:
            gerenciador_de_telas.tela_cadastro.label_11.setText("As duas senhas devem ser iguais")
    else:
        gerenciador_de_telas.tela_cadastro.label_11.setText("Dados incorretos")
