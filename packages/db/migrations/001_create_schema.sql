DROP TABLE IF EXISTS avaliacao CASCADE;
DROP TABLE IF EXISTS item_pedido CASCADE;
DROP TABLE IF EXISTS pedido CASCADE;
DROP TABLE IF EXISTS cozinheiro CASCADE;
DROP TABLE IF EXISTS garcom CASCADE;
DROP TABLE IF EXISTS prato CASCADE;
DROP TABLE IF EXISTS mesa CASCADE;
DROP TABLE IF EXISTS cliente CASCADE;

CREATE TABLE cliente (
    id_cliente INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    telefone VARCHAR(20),
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE mesa (
    id_mesa INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidade INT NOT NULL,
    localizacao TEXT NOT NULL
);

CREATE TABLE prato (
    id_prato INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    categoria TEXT NOT NULL
);

CREATE TABLE garcom (
    id_funcionario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    turno VARCHAR(20),
    comissao DECIMAL(5, 2)
);

CREATE TABLE cozinheiro (
    id_funcionario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    especialidade TEXT
);

CREATE TABLE pedido (
    id_pedido INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'ABERTO' CHECK (status IN ('ABERTO', 'FECHADO', 'CANCELADO')),
    quantidade_pessoas INT DEFAULT 1 CHECK (quantidade_pessoas > 0),
    id_cliente INT NOT NULL,
    id_mesa INT NOT NULL,
    id_funcionario INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa) ON DELETE CASCADE,
    FOREIGN KEY (id_funcionario) REFERENCES garcom(id_funcionario) ON DELETE CASCADE
);

CREATE TABLE item_pedido (
    id_item_pedido INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_prato INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    observacao TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE CASCADE
);

CREATE TABLE avaliacao (
    id_avaliacao INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nota INT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT NOT NULL,
    id_prato INT NOT NULL,
    id_pedido INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE CASCADE,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    UNIQUE (id_cliente, id_pedido, id_prato)
);

CREATE INDEX idx_prato_categoria ON prato(categoria);
CREATE INDEX idx_pedido_cliente ON pedido(id_cliente);
CREATE INDEX idx_pedido_mesa ON pedido(id_mesa);
CREATE INDEX idx_pedido_funcionario ON pedido(id_funcionario);
CREATE INDEX idx_item_pedido_pedido ON item_pedido(id_pedido);
CREATE INDEX idx_item_pedido_prato ON item_pedido(id_prato);

CREATE OR REPLACE FUNCTION check_empty_order()
RETURNS TRIGGER AS $$
DECLARE
    remaining_items INT;
BEGIN
    SELECT COUNT(*) INTO remaining_items
    FROM item_pedido
    WHERE id_pedido = OLD.id_pedido;
    IF remaining_items = 0 THEN
        DELETE FROM pedido WHERE id_pedido = OLD.id_pedido;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_delete_empty_order
AFTER DELETE ON item_pedido
FOR EACH ROW
EXECUTE FUNCTION check_empty_order();