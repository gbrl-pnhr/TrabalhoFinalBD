CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS mesa (
    id_mesa SERIAL PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidade INT NOT NULL,
    localizacao VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS prato (
    id_prato SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS garcom (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    turno VARCHAR(20),
    comissao DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS cozinheiro (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    especialidade VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido SERIAL PRIMARY KEY,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED', 'CANCELLED')),
    quantidade_pessoas INT DEFAULT 1 CHECK (quantidade_pessoas > 0),
    id_cliente INT NOT NULL,
    id_mesa INT NOT NULL,
    id_funcionario INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa),
    FOREIGN KEY (id_funcionario) REFERENCES garcom(id_funcionario)
);

CREATE TABLE IF NOT EXISTS item_pedido (
    id_item_pedido SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_prato INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    observacao TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato)
);

CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao SERIAL PRIMARY KEY,
    nota INT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT NOT NULL,
    id_prato INT NOT NULL,
    id_pedido INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    UNIQUE (id_cliente, id_pedido, id_prato)
);