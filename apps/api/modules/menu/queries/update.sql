UPDATE prato
SET
    nome = COALESCE(%(name)s, nome),
    preco = COALESCE(%(price)s, preco),
    categoria = COALESCE(%(category)s, categoria)
WHERE id_prato = %(id)s
RETURNING id_prato, nome, preco, categoria;