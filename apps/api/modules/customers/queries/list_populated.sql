SELECT
    c.id_cliente,
    c.nome,
    c.telefone,
    c.email,
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'id', p.id_pedido,
                'customer_id', c.id_cliente,
                'created_at', p.data_pedido,
                'total_value', p.valor_total,
                'status', p.status,
                'customer_count', p.quantidade_pessoas,
                'customer_name', c.nome,
                'table_id', p.id_mesa,
                'waiter_id', p.id_funcionario,
                'table_number', m.numero,
                'waiter_name', g.nome,
                'items', COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'id', ip.id_item_pedido,
                                'dish_id', pr.id_prato,
                                'quantity', ip.quantidade,
                                'notes', ip.observacao,
                                'dish_name', pr.nome,
                                'unit_price', pr.preco,
                                'total_price', (ip.quantidade * pr.preco)
                            )
                        )
                        FROM item_pedido ip
                        JOIN prato pr ON ip.id_prato = pr.id_prato
                        WHERE ip.id_pedido = p.id_pedido
                    ),
                    '[]'::jsonb
                )
            ) ORDER BY p.data_pedido DESC
        ) FILTER (WHERE p.id_pedido IS NOT NULL),
        '[]'
    ) as orders
FROM cliente c
LEFT JOIN pedido p ON c.id_cliente = p.id_cliente
LEFT JOIN mesa m ON p.id_mesa = m.id_mesa
LEFT JOIN garcom g ON p.id_funcionario = g.id_funcionario
GROUP BY c.id_cliente, c.nome, c.telefone, c.email
ORDER BY c.nome;