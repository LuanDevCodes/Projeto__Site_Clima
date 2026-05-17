-- Um arquivo apenas para deixar registrados os comandos usados na criação do DB em MySQl (XAMPP)

-- Cria o banco de dados
CREATE DATABASE clima_db;
USE clima_db;

-- Tabela para guardar os nomes das cidades
CREATE TABLE cidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE -- UNIQUE para evitar cadastrar a mesma cidade duas vezes
);

-- Tabela para guardar o histórico de temperaturas
CREATE TABLE temperaturas (
    id INT AUTO_INCREMENT PRIMARY KEY, -- auto increment pra ela ir se redimencionando sozinha sem precisar ser passada como parâmetro
    cidade_id INT, -- coluna que liga a temperatura com a cidade correspondente
    data DATE NOT NULL,
    temperatura DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (cidade_id) REFERENCES cidades(id) -- foreign key pra ser possível linkar a cidade com o clima
);