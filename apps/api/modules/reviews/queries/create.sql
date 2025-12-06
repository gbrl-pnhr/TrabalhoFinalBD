INSERT INTO avaliacao (nota, comentario, id_cliente, id_prato, id_pedido)
VALUES (%(rating)s, %(comment)s, %(customer_id)s, %(dish_id)s, %(order_id)s)
RETURNING id_avaliacao, nota, comentario, data_avaliacao, id_cliente, id_prato, id_pedido;