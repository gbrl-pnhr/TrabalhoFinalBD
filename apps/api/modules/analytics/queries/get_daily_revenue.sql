SELECT
    DATE(data_pedido) as data,
    COUNT(id_pedido) as total_pedidos,
    SUM(valor_total) as receita_total
FROM pedido
WHERE status != 'CANCELADO'
GROUP BY DATE(data_pedido)
ORDER BY DATE(data_pedido) DESC
LIMIT 30;