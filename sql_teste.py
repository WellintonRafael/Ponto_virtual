import run_sql
import funcoes
from datetime import datetime





saida = 'saida'

table = 'marcacao_ponto'

cpf = '00000000000'

nome = 'TESTE'


cargo = 'ADMINISTRADOR'

depto = 15

# a = 1

# run_sql.update_database(table, saida, funcoes.mostra_hora(), a, '2022-05-07')

# run_sql.insert_into_database(cpf, nome, cargo, depto)

# a = run_sql.select_2('WELLINTON RAFAEL DOS SANTOS INOCENCIO')


# lista_de_nomes = run_sql.select_todos_nomes()


# nova_lista = list()
# for item in lista_de_nomes:
#     item = item[0]
#     nova_lista.append(item)

# print(nova_lista)

nome = 'WELLINTON RAFAEL DOS SANTOS INOCENCIO'

di = '2022-05-01'

df = '2022-05-31'

# a = run_sql.busca_senha_login('WELL')

# b = run_sql.busca_marcacoes(funcoes.mostra_data())
# b = run_sql.busca_marcacoes('12/05/2022')

# if b:
    # print(b)


# print(b is None)


# for item in b:
#     print(item)
# print(b)



# print(b[0] is None)




# x = run_sql.insert_into_marcacoes('entrada', 'WELL', '01/05/2022', '09:00')






def mostra_hora() -> str:
    hora_atual = datetime.now()
    hora_formatada: str = hora_atual.strftime('%H:%M')
    return str(hora_formatada)



lista = tuple('REJANE MARIA DOS SANTOS')



# a = run_sql.select_id_ponto(lista)

print(lista)
