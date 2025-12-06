INSERT INTO prato (nome, preco, categoria)
VALUES (%(nome)s, %(preco)s, %(categoria)s)
RETURNING id_prato, nome, preco, categoria;