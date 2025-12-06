SELECT 1
FROM item_pedido ip
JOIN pedido p ON ip.id_pedido = p.id_pedido
WHERE p.id_pedido = %(order_id)s
  AND p.id_cliente = %(customer_id)s
  AND ip.id_prato = %(dish_id)s
LIMIT 1;