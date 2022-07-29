import psycopg2 as db

connection = db.connect(user="postgres", password="welL2801", host="localhost", port="5432", database="teste")


def run_sql_general(sql):
    """
    Função que faz a conexão com o database da variável connection.
    Não retorna nada.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def run_sql_select(sql):
    """
    Função que faz a conexão com o database da variável connection.
    Retorna os dados encontrados pelo cursor.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()
        return cursor.fetchall()
        