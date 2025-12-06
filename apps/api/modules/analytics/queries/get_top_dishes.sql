SELECT
    p.nome as nome_prato,
    p.categoria,
    SUM(ip.quantidade) as total_vendido,
    SUM(ip.quantidade * p.preco) as receita_estimada
FROM item_pedido ip
JOIN prato p ON ip.id_prato = p.id_prato
JOIN pedido ped ON ip.id_pedido = ped.id_pedido
WHERE ped.status != 'CANCELLED'
GROUP BY p.id_prato, p.nome, p.categoria, p.preco
ORDER BY total_vendido DESC
LIMIT 10;