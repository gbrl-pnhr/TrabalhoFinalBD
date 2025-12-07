SELECT
    p.id_pedido,
    p.data_pedido,
    p.valor_total,
    p.status,
    p.quantidade_pessoas,
    p.id_mesa,
    p.id_funcionario as id_garcom,
    c.nome as cliente_nome,
    m.numero as mesa_numero,
    g.nome as garcom_nome,
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'id', ip.id_item_pedido,
                'dish_id', pr.id_prato,
                'quantity', ip.quantidade,
                'notes', ip.observacao,
                'dish_name', pr.nome,
                'unit_price', pr.preco,
                'total_price', (ip.quantidade * pr.preco)
            )
        ) FILTER (WHERE ip.id_item_pedido IS NOT NULL),
        '[]'
    ) as items
FROM pedido p
    JOIN cliente c ON p.id_cliente = c.id_cliente
    JOIN mesa m ON p.id_mesa = m.id_mesa
    JOIN garcom g ON p.id_funcionario = g.id_funcionario
    LEFT JOIN item_pedido ip ON p.id_pedido = ip.id_pedido
    LEFT JOIN prato pr ON ip.id_prato = pr.id_prato
WHERE p.id_pedido = %(order_id)s
GROUP BY
    p.id_pedido,
    p.data_pedido,
    p.valor_total,
    p.status,
    p.quantidade_pessoas,
    p.id_mesa,
    p.id_funcionario,
    c.nome,
    m.numero,
    g.nome;