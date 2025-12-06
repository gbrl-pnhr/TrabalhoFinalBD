SELECT
    ip.id_item_pedido, ip.quantidade, ip.observacao,
    pr.id_prato, pr.nome as nome_prato, pr.preco
FROM item_pedido ip
    JOIN prato pr ON ip.id_prato = pr.id_prato
WHERE ip.id_pedido = %(order_id)s;