INSERT INTO pedido (id_cliente, id_mesa, id_funcionario, quantidade_pessoas, status)
VALUES (%(customer_id)s, %(table_id)s, %(waiter_id)s, %(people_count)s, 'ABERTO')
RETURNING id_pedido, data_pedido, valor_total, id_cliente, id_mesa, id_funcionario, quantidade_pessoas, status;