SELECT
    p.id_prato,
    p.nome,
    p.preco,
    p.categoria,
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'id', a.id_avaliacao,
                'rating', a.nota,
                'comment', a.comentario,
                'created_at', a.data_avaliacao,
                'customer_name', c.nome,
                'dish_name', p.nome
            ) ORDER BY a.data_avaliacao DESC
        ) FILTER (WHERE a.id_avaliacao IS NOT NULL),
        '[]'
    ) as reviews
FROM prato p
LEFT JOIN avaliacao a ON p.id_prato = a.id_prato
LEFT JOIN cliente c ON a.id_cliente = c.id_cliente
GROUP BY p.id_prato, p.nome, p.preco, p.categoria
ORDER BY p.nome;