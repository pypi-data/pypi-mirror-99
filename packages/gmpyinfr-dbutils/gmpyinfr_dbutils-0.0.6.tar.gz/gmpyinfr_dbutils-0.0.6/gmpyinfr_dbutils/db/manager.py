"""
Manager de conexão com o banco de dados.
"""

import warnings

import turbodbc

from gmpyinfr_dbutils.utils import utils

class Manager:
    """
    Classe Manager

    Cria um objeto responsável por ler o arquivo de configuração de conexão
    e gerir as conexões.
    """

    def __init__(self, filepath, turbodbc_options=None):
        """
        Construtor.

        Params:
            - filepath : str path do arquivo de configuração da conexão
            - turbodbc_options : (std None) estrutura de opções do turbodbc
        """

        # pode lançar vários erros, queremos que estes cheguem até o usuário
        self.__conf = utils.read_conf_file(filepath)
        self.turbodbc_options = turbodbc_options

        # controle
        self.conn = None

    def __get_connection(self):
        """Retorna conexão a partir da configuração."""

        return turbodbc.connect(
            **self.__conf, turbodbc_options=self.turbodbc_options)

    def __test_conn(self):
        """
        Executa qualquer coisa no banco de dados apenas pra ver se a conexão
        ainda está ativa. No caso do primeiro erro, finaliza a conexão ativa
        e tenta novamente. No segundo erro, lança exceção.

        Se a conexão não tiver sido criada, cria.
        """

        def run_cursor():
            with self.conn.cursor() as cursor:
                cursor.execute('SELECT 1')
                return cursor.fetchone()

        if self.conn is None:
            self.conn = self.__get_connection()

        try:
            rtn = run_cursor()
        except turbodbc.exceptions.Error:
            self.conn.close()
            self.conn = self.__get_connection()
            rtn = run_cursor()

        assert rtn[0] == 1, 'Retorno do DB diferente do esperado'

    def get_connection(self):
        """
        Retorna a conexão controlada para ser utilizada independentemente.

        Pode ser utilizada no pandas e em outras ocasiões que necessitam de uma
        conexão válida.
        """

        self.__test_conn()
        return self.conn

    def get_cursor(self):
        """Retorna um cursor."""

        return self.get_connection().cursor()

    def fast_upload(self, tablename, df, identity_insert=False):
        """
        Rotina de fast upload para envio rápido de grandes dataframes.

        Em caso de erro, lança uma exceção. Não há retorno.

        Params:
            - tablename : str apontando o nome completo da tabela a fazer upload
            - df : pandas.DataFrame contendo os dados a serem enviados. É importante
                que o nome das colunas sejam iguais no dataframe e na tabela de destino.
            - identity_insert : bool apontando se o statement de identity insert deve ser
                utilizado.
        """

        # verifica se a banco é postgresql. Caso seja, ignora o identity_insert informado
        if identity_insert and 'postgre' in self.__conf['driver'].lower():
            identity_insert = False
            warnings.warn("PostgreSQL não utiliza identity insert.")

        self.__test_conn()
        utils.fast_upload(self.conn, tablename, df, identity_insert)

    def execute(self, query):
        """
        Executa uma query qualquer.

        Params:
            - query : str consulta ou statement a ser executada.
        """

        with self.get_cursor() as cursor:
            cursor.execute(query)
            rtn = cursor.fetchall()

        return rtn

    def close(self):
        """Encerra conexão."""

        if self.conn is not None:
            self.conn.close()

    def __exit__(self, type, value, traceback):

        self.close()
