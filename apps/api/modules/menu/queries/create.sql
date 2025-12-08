INSERT INTO prato (nome, preco, categoria)
VALUES (%(name)s, %(price)s, %(category)s)
RETURNING id_prato, nome, preco, categoria;