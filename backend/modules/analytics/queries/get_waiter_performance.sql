SELECT
    g.nome as nome_garcom,
    COUNT(p.id_pedido) as total_pedidos,
    COALESCE(SUM(p.valor_total), 0) as total_vendas
FROM garcom g
LEFT JOIN pedido p ON g.id_funcionario = p.id_funcionario AND p.status != 'CANCELLED'
GROUP BY g.id_funcionario, g.nome
ORDER BY total_vendas DESC;