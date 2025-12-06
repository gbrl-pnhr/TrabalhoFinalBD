SELECT
    p.id_pedido, p.data_pedido, p.valor_total, p.status, p.quantidade_pessoas,
    c.nome as cliente_nome,
    m.numero as mesa_numero,
    g.nome as garcom_nome
FROM pedido p
    JOIN cliente c ON p.id_cliente = c.id_cliente
    JOIN mesa m ON p.id_mesa = m.id_mesa
    JOIN garcom g ON p.id_funcionario = g.id_funcionario
WHERE p.id_pedido = %(order_id)s;