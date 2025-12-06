-- 006_reset_sequences.sql
-- Reset auto-increment sequences after manual ID insertion

SELECT setval(pg_get_serial_sequence('cliente', 'id_cliente'), (SELECT MAX(id_cliente) FROM cliente));
SELECT setval(pg_get_serial_sequence('mesa', 'id_mesa'), (SELECT MAX(id_mesa) FROM mesa));
SELECT setval(pg_get_serial_sequence('prato', 'id_prato'), (SELECT MAX(id_prato) FROM prato));
SELECT setval(pg_get_serial_sequence('garcom', 'id_funcionario'), (SELECT MAX(id_funcionario) FROM garcom));
SELECT setval(pg_get_serial_sequence('cozinheiro', 'id_funcionario'), (SELECT MAX(id_funcionario) FROM cozinheiro));
SELECT setval(pg_get_serial_sequence('pedido', 'id_pedido'), (SELECT MAX(id_pedido) FROM pedido));
SELECT setval(pg_get_serial_sequence('item_pedido', 'id_item_pedido'), (SELECT MAX(id_item_pedido) FROM item_pedido));
SELECT setval(pg_get_serial_sequence('avaliacao', 'id_avaliacao'), (SELECT MAX(id_avaliacao) FROM avaliacao));
