SELECT id_mesa, numero, capacidade, localizacao
FROM mesa
WHERE id_mesa = %(id)s;