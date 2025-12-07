-- 001_seed_infrastructure.sql
-- Tables (Mesa), Staff (Garcom/Cozinheiro), and Menu (Prato)

TRUNCATE TABLE mesa, garcom, cozinheiro, prato CASCADE;

INSERT INTO mesa (id_mesa, numero, capacidade, localizacao) VALUES
(1, 1, 2, 'Interna'),
(2, 2, 6, 'Interna'),
(3, 3, 4, 'Interna'),
(4, 4, 2, 'Varanda'),
(5, 5, 2, 'Varanda'),
(6, 6, 8, 'Interna'),
(7, 7, 2, 'Interna'),
(8, 8, 4, 'Interna'),
(9, 9, 2, 'Varanda'),
(10, 10, 4, 'Varanda'),
(11, 11, 8, 'Interna'),
(12, 12, 8, 'Varanda'),
(13, 13, 6, 'Interna'),
(14, 14, 4, 'Varanda'),
(15, 15, 8, 'Externa'),
(16, 16, 6, 'Interna'),
(17, 17, 4, 'Externa'),
(18, 18, 2, 'Interna'),
(19, 19, 8, 'Interna'),
(20, 20, 6, 'Externa'),
(21, 21, 6, 'Interna'),
(22, 22, 8, 'Varanda'),
(23, 23, 2, 'Externa'),
(24, 24, 2, 'Varanda'),
(25, 25, 6, 'Varanda'),
(26, 26, 6, 'Varanda'),
(27, 27, 4, 'Varanda'),
(28, 28, 2, 'Interna'),
(29, 29, 4, 'Externa'),
(30, 30, 2, 'Interna');

INSERT INTO garcom (id_funcionario, nome, cpf, salario, turno, comissao) VALUES
(1, 'Brenda Alves', '43815092698', 1500.0, 'Noite', 5.0),
(2, 'Arthur Borges', '39041687548', 1800.0, 'Noite', 5.0),
(3, 'Lara Abreu', '26591780386', 2000.0, 'Noite', 5.0),
(4, 'Aylla Fogaça', '54093871639', 1500.0, 'Noite', 5.0),
(5, 'Laís Pires', '95380617484', 1800.0, 'Manhã', 5.0);

INSERT INTO cozinheiro (id_funcionario, nome, cpf, salario, especialidade) VALUES
(1, 'Carlos Eduardo Garcia', '47512869355', 4000.0, 'Grelhados'),
(2, 'Dra. Ana Sophia Pereira', '28317594041', 4000.0, 'Sobremesas'),
(3, 'Lunna Vargas', '03962857400', 4000.0, 'Massas');

INSERT INTO prato (id_prato, nome, preco, categoria) VALUES
(1, 'Bruschetta Clássica', 25.0, 'Entrada'),
(2, 'Carpaccio de Carne', 32.0, 'Entrada'),
(3, 'Dadinhos de Tapioca', 22.0, 'Entrada'),
(4, 'Salada Caprese', 28.0, 'Entrada'),
(5, 'Filé Mignon ao Poivre', 85.0, 'Prato Principal'),
(6, 'Risoto de Camarão', 78.0, 'Prato Principal'),
(7, 'Salmão Grelhado', 72.0, 'Prato Principal'),
(8, 'Espaguete à Carbonara', 55.0, 'Prato Principal'),
(9, 'Nhoque ao Sugo', 48.0, 'Prato Principal'),
(10, 'Bife de Chorizo', 89.0, 'Prato Principal'),
(11, 'Petit Gâteau', 24.0, 'Sobremesa'),
(12, 'Tiramisu', 26.0, 'Sobremesa'),
(13, 'Pudim de Leite', 18.0, 'Sobremesa'),
(14, 'Mousse de Chocolate', 20.0, 'Sobremesa'),
(15, 'Água com Gás', 6.0, 'Bebida'),
(16, 'Refrigerante Lata', 8.0, 'Bebida'),
(17, 'Suco Natural', 12.0, 'Bebida'),
(18, 'Cerveja Artesanal', 18.0, 'Bebida'),
(19, 'Vinho Tinto Taça', 25.0, 'Bebida'),
(20, 'Caipirinha', 22.0, 'Bebida');

