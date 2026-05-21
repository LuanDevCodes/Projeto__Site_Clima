from flask import Flask, jsonify, request # Ela vai ajudar na criação de um servidor local para rodar a API
# O jsonify padroniza converte os dicionários do python pro padrão JSON
# Request é o objeto para abrir pacote e ler o que tem dentro dele, como o POST com os dados empacotados
from flask_cors import CORS

import requests # Faz as requisições para fora, com ela que eu consigo trazer os dados da API do IBGE
import mysql.connector # Ela vai ajudar na conexão com o DB do XAMPP, 
import banco # Importanto o arquivo do banco de dados que virá com as informações necessárias para a conexão

# Instancia o servidor Flask e o atribui à variável 'app'
app = Flask(__name__)
CORS(app) # Essa linha destranca a porta do servidor para o Front-End HTML, precisei dela pq estava dando erro

# Define o "endereço" (endpoint) e diz que essa função só responde se o método for POST (envio de dados)
@app.route('/cidades', methods=['POST'])

def cadastrar_cidade():
    # O request.get_json() abre o pacote enviado pelo Front-end e extrai o corpo da requisição
    dados = request.get_json()
    nome_cidade = dados.get('nome')

    if not nome_cidade:
        return jsonify({"erro": "O nome da cidade é obrigatório"}), 400

    # inicio da validação com a lista da API do IBGE
    try:
        # Bate na API pública do IBGE para pegar as cidades do país
        url_ibge = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        resposta_ibge = requests.get(url_ibge)
        
        # Cria uma lista com os nomes das cidades (em letras minúsculas para não dar erro de maiúscula/minúscula)
        # Isso é um "List Comprehension", um jeito "Pythonico" e rápido de criar listas extraindo dados do JSON
        cidades_validas = [cidade['nome'].lower() for city in resposta_ibge.json()]

        # Se a cidade digitada não estiver na lista oficial (é mais pro caso de testes via Postman e envio direto)
        if nome_cidade.lower() not in cidades_validas:
            
            # Retorna o código 404 (Not Found)
            return jsonify({
                "erro": "Cidade não encontrada",
                "mensagem": f"A cidade '{nome_cidade}' não existe no Brasil"
            }), 404

    except Exception:
        return jsonify({"erro": "Falha na comunicação com o serviço de validação"}), 500

    # Realizando a comunicação com o DB para a inserção das informações
    try:
        conexao = banco.conectar()

        # O cursor é o objeto que navega dentro do banco e executa os comandos SQL
        cursor = conexao.cursor()
        
        # Usamos o '%s' como um placeholder para evitar ataques de SQL Injection. O Python substitui de forma segura.
        comando_sql = "INSERT INTO cidades (nome) VALUES (%s)"

        # A vírgula depois de 'nome_cidade' é obrigatória para o Python entender que é uma tupla (lista imutável)
        cursor.execute(comando_sql, (nome_cidade,))
        conexao.commit() # Commitando a alteração, como num salvamento de uma transação no SQL Server 
        
        cursor.close()
        conexao.close()

        return jsonify({"status": "sucesso", "mensagem": f"A cidade '{nome_cidade}' foi cadastrada com sucesso"}), 201 

    # Captura o erro de duplicação do MySQL, o unique colocado lá na criação ajuda justamente nisso pra exibir pro usuário o erro
    except mysql.connector.IntegrityError:
        return jsonify({"erro": "duplicada", "mensagem": "A cidade já está cadastrada no sistema"}), 409 # 409 significa 'Conflito'
    
    except Exception as erro:
        return jsonify({"erro": f"Falha ao cadastrar no banco: {str(erro)}"}), 500

# Rota para buscar todas as cidades (usada para preencher o dropdown no Front-end)
@app.route('/cidades', methods=['GET'])

def listar_cidades():
    try:
        # Estabelece a conexão usando o módulo do banco.py
        conexao = banco.conectar()
        
        # O cursor com 'dictionary=True' já transforma os dados em dicionários (chave: valor)
        # Isso facilita muito o retorno para o Front-end
        cursor = conexao.cursor(dictionary=True)
        
        # Executa o comando SQL para selecionar tudo da tabela cidades
        cursor.execute("SELECT * FROM cidades")
        
        # fetchall() captura todas as linhas retornadas pelo banco
        lista_cidades = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        # Retorna a lista para o Front-end em formato JSON com Status 200 (Sucesso)
        return jsonify(lista_cidades), 200

    except Exception as erro:
        # Em caso de qualquer falha, retorna o erro com Status 500 (Erro Interno)
        return jsonify({"erro": f"Falha ao buscar cidades: {str(erro)}"}), 500

# Rota para cadastrar a temperatura de uma cidade em uma data específica
@app.route('/temperaturas', methods=['POST'])

def cadastrar_temperatura():
    dados = request.get_json()

    # Captura os dados do JSON enviado Front-end
    cidade_id = dados.get('cidade_id')
    data = dados.get('data')
    temperatura = dados.get('temperatura')

    # Validação simples: verifica se todos os campos obrigatórios foram preenchidos
    if not cidade_id or not data or temperatura is None:
        return jsonify({"erro": "Os campos cidade_id, data e temperatura são obrigatórios"}), 400

    try:
        conexao = banco.conectar()
        cursor = conexao.cursor()

        # Comando SQL para inserção na tabela temperaturas
        comando_sql = "INSERT INTO temperaturas (cidade_id, data, temperatura) VALUES (%s, %s, %s)"
        valores = (cidade_id, data, temperatura)

        cursor.execute(comando_sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({"status": "sucesso", "mensagem": "Temperatura cadastrada com sucesso"}), 201

    # Tratamento específico para erro de duplicidade
    except mysql.connector.IntegrityError:
        return jsonify({
            "erro": "duplicada", 
            "mensagem": "Já existe uma temperatura registrada para esta cidade nesta data"
        }), 409

    # Tratamento para qualquer outro erro inesperado no banco
    except Exception as erro:
        return jsonify({"erro": f"Falha ao cadastrar temperatura: {str(erro)}"}), 500

# Essa linha garante que o servidor só suba se eu rodar o arquivo diretamente (não sobe se for apenas importado)
if __name__ == '__main__':
    
    # O debug=True reinicia o servidor sozinho sempre que salvar uma alteração no código
    app.run(port=5000, debug=True)