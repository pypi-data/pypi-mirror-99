"""
Funções úteis à comunicação com o banco de dados.
"""

import re

import turbodbc
import pandas as pd
from datetime import date
from numpy.ma import MaskedArray

def read_conf_file(filepath):
    """
    Faz a leitura do arquivo de configuração.

    Arquivo deve ter a seguinte configuração:
        driver=<driver>
        server=<server>
        port=<port>
        database=<databasename>
        uid=<user>
        pwd=<pwd>

    Por favor, mantenha esta configuração. Separe as linhas apenas por quebras.
    Linhas em branco serão ignoradas. Linhas iniciadas por # também são ignoradas.

    Params:
        - filepath : str path do arquivo de configuração da conexão

    Returns:
        tuple contendo as configurações de conexão
    """

    must = set(['driver', 'server', 'uid', 'pwd'])

    with open(filepath, 'r') as _f:
        confs = map(lambda x: x.strip(), _f.read().split('\n'))

    confs = [x for x in confs if x and not x.startswith('#')]
    if not confs:
        raise ValueError("Arquivo de configuração deve conter configurações.")

    regex = re.compile(r'^(\w+)\s*=\s*(.+)$')
    confs = {k.lower(): v for k, v in [regex.findall(c)[0] for c in confs]}
    missing = must - set(confs.keys())
    if missing:  # uma config obrigatória está faltando
        raise ValueError("Arquivo de configuração não contém os campos: '{}'".format(
            "', '".join(missing)))

    return confs

def fast_upload(conn, tablename, df, identity_insert=False):
    """
    Faz upload de um dataframe.

    Em caso de erro, lança uma exceção. Não há retorno.

    Caso no parâmetro 'conn' seja informado um turbodbc.cursor.Cursor, o usuário deve
    realizar commit ou rollback ao final da execução e fechar o cursor, manualmente.
    Caso no parâmetro seja informado um objeto turbodbc.connection.Connection, a rotina
    irá realizar o commit no cursor e o fechará ao final.

    Não faz controle de utilização do identity insert. Utilize apenas se souber o que
    está fazendo e se o SGBD tiver suporte para o statement.

    Params:
        - conn : turbodbc.connection.Connection ou turbodbc.cursor.Cursor para conectar
            no banco de dados
        - tablename : str apontando o nome completo da tabela a fazer upload
        - df : pandas.DataFrame contendo os dados a serem enviados. É importante
            que o nome das colunas sejam iguais no dataframe e na tabela de destino.
        - identity_insert : bool apontando se o statement de identity insert deve ser
            utilizado.
    """

    def test_type_conn():
        
        _is_conn = False
        if isinstance(conn, turbodbc.connection.Connection):
            _is_conn = True
        elif not isinstance(conn, turbodbc.cursor.Cursor):
            raise ValueError(
                "Esperava param 'conn' sendo 'Connection' ou 'Cursor' do 'turbodbc'")
        return _is_conn

    def convert_t(x):
        """Faz a conversão para os tipos esperados."""

        if x.dtype == 'object' and isinstance(x[0], date):
            return pd.to_datetime(x).values
        elif x.dtype == 'datetime64[ns]':
            return x
        return MaskedArray(x, pd.isnull(x))

    is_conn =  test_type_conn()

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Esperava param 'dataframe' sendo 'pandas.DataFrame'")

    if not isinstance(tablename, str):
        raise ValueError("Esperava param 'tablename' sendo 'str'")

    if df.shape[0] <= 0:  # sem dados para fazer upload
        return

    ins = 'INSERT INTO {} ({}) VALUES ({})'.format(
        tablename, ','.join(df.columns),
        ','.join(['?'] * df.columns.shape[0]))
    qii = 'SET IDENTITY_INSERT {} {}'

    if is_conn:
        cursor = conn.cursor()
    else:
        cursor = conn

    val = [convert_t(df[x].values) for x in df.columns]

    try:
        if identity_insert:
            cursor.execute(qii.format(tablename, 'ON'))

        cursor.executemanycolumns(ins, val)

        if identity_insert:
            cursor.execute(qii.format(tablename, 'OFF'))

        if is_conn:
            conn.commit()
    except:
        if is_conn:
            conn.rollback()
        raise
    finally:
        if is_conn:
            cursor.close()
