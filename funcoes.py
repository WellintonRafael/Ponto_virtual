# def tratador_de_datas_americano(data_a_ser_tratada, splitador):
#     data_tratada = str(data_a_ser_tratada.split(splitador))

#     dia = data_tratada[2]
#     mes = data_tratada[1]
#     ano = data_tratada[0]    
    
#     data_final = f'{dia}/{mes}/{ano}'
#     return data_final

# def validador_de_horas(hora_a_ser_validada):
#     hora_validada = str(hora_a_ser_validada.split(':'))
    
#     if len(hora_validada) < 2:
#         return False

#     hora = int(hora_validada[0])
#     minuto = hora_validada[1]
#     return hora >= 0 and hora <= 23 and minuto >= 0 and minuto <= 59

from  datetime import datetime
from time import strftime


def data_americana_para_brasileira(data_a_ser_tratada: str):
    formato_americano = '%Y-%m-%d'
    formato_brasileiro = '%d/%m/%Y'
    data = datetime.strptime(data_a_ser_tratada, formato_americano)
    d = data.strftime(formato_brasileiro)
    return str(d)


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


def valida_hora(hora_a_ser_validada: str) -> bool:
    hora_validada = str(hora_a_ser_validada).split(":, 0")
    minutos_validados = str(hora_a_ser_validada).split(":, 1")
    hora_validada = int(hora_validada)
    minutos_validados =int(minutos_validados)
    if hora_validada < 0 and hora_validada > 23 and minutos_validados < 0 and minutos_validados > 59:
        return False


if __name__ == '__main__':
    pass