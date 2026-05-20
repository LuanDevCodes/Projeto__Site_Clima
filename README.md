# Projeto - Site de Monitoramento Meteorológico com API ☔

Um projeto acadêmico de aplicação web para registro e monitoramento do histórico climático de cidades brasileiras. Este sistema foi desenvolvido como parte de um estudo prático sobre **Sistemas Distribuídos** e comunicação de APIs.

A aplicação permite cadastrar cidades (com validação em tempo real através da API pública do IBGE) e registrar dados de temperatura, exibindo um ranking interativo. O foco principal do desenvolvimento foi a criação de uma arquitetura limpa, separando a responsabilidade do Back-end (API REST) e do Front-end.

## 🛠️ Tecnologias Utilizadas

**Back-end:**
* **Python 3**
* **Flask**                   (Microframework para criação da API REST)
* **MySQL / XAMPP**           (Banco de dados relacional)
* **mysql-connector-python**  (Comunicação segura com o banco)
* **python-dotenv**           (Gerenciamento de variáveis de ambiente)

**Front-end:**
* **HTML5 e CSS3**           (Estrutura e estilização limpa e responsiva)
* **JavaScript (Vanilla)**   (Consumo assíncrono da API local e da API do IBGE via `fetch`)

## ⚙️ Funcionalidades

* [x] Formulário de cadastro de novas cidades
* [x] Integração com a API de Localidades do IBGE para popular listas e validar se a cidade existe no Brasil
* [x] Proteção contra cadastro de cidades duplicadas no banco de dados
* [ ] Registro de novas temperaturas atreladas às cidades cadastradas (Em desenvolvimento)
* [ ] Dashboard interativo exibindo o Top 10 cidades mais quentes (Em desenvolvimento)
* [ ] Exibição de um Dashboard de barras com os dados de temperatura de determinada cidade (Em desenvolvimento)

##

Projeto em desenvolvimento como parte da graduação em Ciência da Computação
