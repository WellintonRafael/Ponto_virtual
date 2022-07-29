import sqlite3

from PyQt5.QtCore import QTime
from PyQt5 import QtWidgets
import time

import gerenciador_de_telas
import funcoes

import schedule

padrao_hora = '  :  '

def getFormatTime():

    # getting current time
    current_time = QTime.currentTime()

    # converting QTime object to string
    label_time = current_time.toString('hh:mm:ss')

    # showing it to the label
    return label_time


def startTimeUpdate():
    schedule.every(1).seconds.do(show_hour)
    schedule.run_all()
    while not StopIteration:
        schedule.run_pending()
        time.sleep(1)

        
def show_hour():
    gerenciador_de_telas.primeira_tela.label_2.setText(getFormatTime())


def criar_tabelas():
    banco = sqlite3.connect("database_ponto_digital.db")
    cursor = banco.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Marcacao_ponto_2 ( \
            Id INTEGER PRIMARY KEY AUTOINCREMENT, \
            Cod_funcionario text, \
            Nome text,Data DATE,Entrada text default '  :  ', Sai_almoco text default '  :  ', \
            Ent_almoco text default '  :  ', Saida text default '  :  ', \
            Verificar_alteracao text default '    ' \
        )"
    )
    banco.commit()
    banco.close()


app = QtWidgets.QApplication([])


# gerenciador_de_telas.primeira_tela.label_2.setText(showTime())

criar_tabelas()

if __name__ == '__main__':
    gerenciador_de_telas.load_screens()
    gerenciador_de_telas.load_actions()
    gerenciador_de_telas.primeira_tela.show()
    gerenciador_de_telas.primeira_tela.label_2.setText(funcoes.mostra_hora())

    app.exec()
