import mysql.connector # Importando a biblioteca que ajudará na conexão com o DB
from dotenv import load_dotenv # Para carregar o arquivo .env
import os # Para poder conversar com o SO, é usada também no ENV   

# Descobre qual é a pasta exata onde este arquivo (banco.py) está salvo
pasta_atual = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho completo apontando para o .env dentro dessa mesma pasta
caminho_env = os.path.join(pasta_atual, '.env')

# override=True força o Python a priorizar este arquivo .env acima de qualquer configuração do Windows
load_dotenv(caminho_env, override=True)

def conectar():
    #
    #  Buscando as variáveis com os novos nomes blindados
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    
    # Lidando com a senha vazia de forma segura
    password_env = os.getenv("DB_PASSWORD")
    password = "" if password_env in [None, '""', "''"] else password_env
    
    database = os.getenv("DB_NAME")

    # A conexão cirúrgica e à prova de falhas com o XAMPP
    conexao = mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
        use_pure=True # Esta linha é a vacina contra o bug 'Failed raising error'
    )
    return conexao