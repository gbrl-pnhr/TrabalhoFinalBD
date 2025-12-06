INSERT INTO cliente (nome, telefone, email)
VALUES (%(name)s, %(phone)s, %(email)s)
RETURNING id_cliente, nome, telefone, email;