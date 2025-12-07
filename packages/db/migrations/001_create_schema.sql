CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    telefone VARCHAR(20),
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS mesa (
    id_mesa INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidade INT NOT NULL,
    localizacao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prato (
    id_prato INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    categoria TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_prato_categoria ON prato(categoria);

CREATE TABLE IF NOT EXISTS garcom (
    id_funcionario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    turno VARCHAR(20),
    comissao DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS cozinheiro (
    id_funcionario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    especialidade TEXT
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'ABERTO' CHECK (status IN ('ABERTO', 'FECHADO', 'CANCELADO')),
    quantidade_pessoas INT DEFAULT 1 CHECK (quantidade_pessoas > 0),
    id_cliente INT NOT NULL,
    id_mesa INT NOT NULL,
    id_funcionario INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa),
    FOREIGN KEY (id_funcionario) REFERENCES garcom(id_funcionario)
);

CREATE INDEX IF NOT EXISTS idx_pedido_cliente ON pedido(id_cliente);
CREATE INDEX IF NOT EXISTS idx_pedido_mesa ON pedido(id_mesa);
CREATE INDEX IF NOT EXISTS idx_pedido_funcionario ON pedido(id_funcionario);
CREATE INDEX IF NOT EXISTS idx_pedido_status ON pedido(status);
CREATE INDEX IF NOT EXISTS idx_pedido_data ON pedido(data_pedido);

CREATE TABLE IF NOT EXISTS item_pedido (
    id_item_pedido INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_prato INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    observacao TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato)
);

CREATE INDEX IF NOT EXISTS idx_item_pedido_pedido ON item_pedido(id_pedido);
CREATE INDEX IF NOT EXISTS idx_item_pedido_prato ON item_pedido(id_prato);

CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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

CREATE INDEX IF NOT EXISTS idx_avaliacao_prato ON avaliacao(id_prato);
CREATE INDEX IF NOT EXISTS idx_avaliacao_cliente ON avaliacao(id_cliente);