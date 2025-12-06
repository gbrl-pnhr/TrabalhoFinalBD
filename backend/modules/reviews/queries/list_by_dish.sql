SELECT
    a.id_avaliacao,
    a.nota,
    a.comentario,
    a.data_avaliacao,
    c.nome as nome_cliente,
    p.nome as nome_prato
FROM avaliacao a
JOIN cliente c ON a.id_cliente = c.id_cliente
JOIN prato p ON a.id_prato = p.id_prato
WHERE a.id_prato = %(dish_id)s
ORDER BY a.data_avaliacao DESC;