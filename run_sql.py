import connect_db


def select_nome(nome):
    sql = f"SELECT nome_funcionario FROM funcionario\
        WHERE nome_funcionario = '{nome}'"
    dados = connect_db.run_sql_select(sql)
    try:
        connect_db.run_sql_select(sql)
        return dados
    except Exception as e:
        print(e)


def select_todos_nomes():
    sql = "SELECT nome_funcionario FROM funcionario"
    try:
        dados = connect_db.run_sql_select(sql)
        return dados
    except Exception as e:
        print(e)


def select_dados_marcacao_ponto_com_filtro(nome, data_inicio, data_fim):
    sql = f"SELECT to_char(mp.data_ponto, 'DD/MM/YYYY'), \
    mp.entrada, mp.sai_almoco, mp.ent_almoco, mp.saida, \
    mp.ent_extra, mp.sai_extra, mp.observacao \
    FROM funcionario AS f INNER JOIN marcacao_ponto AS mp \
    USING(id_funcionario) \
    WHERE f.nome_funcionario = '{nome}' \
    AND data_ponto BETWEEN '{data_inicio}' AND '{data_fim}'"
    try:
        dados = connect_db.run_sql_select(sql)
        return dados
    except Exception as e:
        print(e)


def select_dados_marcacao_ponto(nome):
    sql = f"SELECT to_char(mp.data_ponto, 'DD/MM/YYYY'), \
    mp.entrada, mp.sai_almoco, mp.ent_almoco, mp.saida, \
    mp.ent_extra, mp.sai_extra, mp.observacao \
    FROM funcionario AS f INNER JOIN marcacao_ponto AS mp \
    USING(id_funcionario) \
    WHERE f.nome_funcionario = '{nome}'"
    try:
        dados = connect_db.run_sql_select(sql)
        return dados
    except Exception as e:
        print(e)


def update_marcacao_ponto(coluna_a_ser_atualizada, valor, condicao_1, condicao_2):
    sql = f"UPDATE marcacao_ponto \
        SET {coluna_a_ser_atualizada} = '{valor}' \
        WHERE data_ponto = '{condicao_1}' \
        AND id_funcionario = (select id_funcionario  \
		FROM login where login = '{condicao_2}')"

    try:
        connect_db.run_sql_general(sql)
        return True
    except Exception as e:
        print(e)


def insert_into_tb_funcionario(cpf_funcionario, nome_funcionario, cargo, id_depto):
    sql = f"INSERT INTO funcionario (CPF_FUNCIONARIO, NOME_FUNCIONARIO, CARGO, ID_DEPTO) \
    VALUES ({cpf_funcionario}, '{nome_funcionario}', '{cargo}', {id_depto})"
    try:
        connect_db.run_sql_general(sql)
        return True
    except Exception as e:
        print(e)


def insert_into_login(login, senha, nome):
    sql = f"INSERT INTO login (LOGIN, SENHA_LOGIN, ID_FUNCIONARIO) \
    VALUES ('{login}', '{senha}', (select id_funcionario from funcionario where nome_funcionario = '{nome}'))"
    try:
        connect_db.run_sql_general(sql)
        return True
    except Exception as e:
        print(e)


def insert_into_marcacoes(marcacao, login, data, hora):
    sql = f"insert into marcacao_ponto \
    (id_funcionario, data_ponto, {marcacao}) values((select id_funcionario from funcionario \
    where id_funcionario = \
    (select l.id_funcionario from login as l\
    where l.login = '{login}')),\
    '{data}', '{hora}')"
    try:
        connect_db.run_sql_general(sql)
        return True
    except Exception as e:
        print(e)


def busca_senha_login(login):
    sql = f"SELECT senha_login FROM login WHERE login = '{login}'"
    try:
        dados = connect_db.run_sql_select(sql)
        return dados[0][0]
    except Exception as e:
        print(e)


def busca_marcacoes(data, login):
    # sql = f"select sai_almoco, saida, sai_extra from marcacao_ponto where data_ponto = ''"
    sql = f"SELECT mp.entrada, mp.sai_almoco, mp.ent_almoco, mp.saida, mp.ent_extra, mp.sai_extra \
    FROM marcacao_ponto AS mp \
    INNER JOIN login AS l \
    USING (id_funcionario) \
    WHERE data_ponto = '{data}' AND l.login = '{login}'"


    try:
        dados = connect_db.run_sql_select(sql)
        return dados[0]
    except Exception as e:
        print(e)


def select_id_ponto(nome):
    sql = f"select * from alteracoes_ponto \
        where id_ponto = (select mp.id_ponto \
        from funcionario as f \
        inner join marcacao_ponto as mp \
        USING(id_funcionario) \
        where f.nome_funcionario = {nome})"
    try:
        dados = connect_db.run_sql_select(sql)
        return dados[0]
    except Exception as e:
        print(e)





def query_geral_de_1_item(item, tabela, primeira_condição, segunda_condição):
    sql = f"SELECT {item} FROM {tabela} WHERE {primeira_condição} = {segunda_condição}"
    try:
        dados = connect_db.run_sql_select(sql)
    except Exception as e:
        print(e)