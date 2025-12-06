INSERT INTO mesa (numero, capacidade, localizacao)
VALUES (%(number)s, %(capacity)s, %(location)s)
RETURNING id_mesa, numero, capacidade, localizacao;