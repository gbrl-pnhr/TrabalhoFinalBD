INSERT INTO item_pedido (id_pedido, id_prato, quantidade, observacao)
VALUES (%(order_id)s, %(dish_id)s, %(quantity)s, %(notes)s)
RETURNING id_item_pedido;