SELECT
    c.id_cliente,
    c.nome,
    c.telefone,
    c.email,
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'id', p.id_pedido,
                'id_cliente', c.id_cliente,
                'criado_em', p.data_pedido,
                'valor_total', p.valor_total,
                'status', p.status,
                'quantidade_cliente', p.quantidade_pessoas,
                'nome_cliente', c.nome,
                'id_mesa', p.id_mesa,
                'id_garcom', p.id_funcionario,
                'numero_mesa', m.numero,
                'nome_garcom', g.nome,
                'itens', COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'id', ip.id_item_pedido,
                                'id_prato', pr.id_prato,
                                'quantidade', ip.quantidade,
                                'observacoes', ip.observacao,
                                'nome_prato', pr.nome,
                                'preco_unitario', pr.preco,
                                'preco_total', (ip.quantidade * pr.preco)
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
    ) as pedidos
FROM cliente c
LEFT JOIN pedido p ON c.id_cliente = p.id_cliente
LEFT JOIN mesa m ON p.id_mesa = m.id_mesa
LEFT JOIN garcom g ON p.id_funcionario = g.id_funcionario
GROUP BY c.id_cliente, c.nome, c.telefone, c.email
ORDER BY c.nome;