-- 001_seed_infrastructure.sql
-- Tables (Mesa), Staff (Garcom/Cozinheiro), and Menu (Prato)
-- Using RESTART IDENTITY to reset IDs to 1

TRUNCATE TABLE mesa, garcom, cozinheiro, prato RESTART IDENTITY CASCADE;

INSERT INTO mesa (numero, capacidade, localizacao) VALUES
(1, 2, 'Interna'),
(2, 6, 'Interna'),
(3, 4, 'Interna'),
(4, 2, 'Varanda'),
(5, 2, 'Varanda'),
(6, 8, 'Interna'),
(7, 2, 'Interna'),
(8, 4, 'Interna'),
(9, 2, 'Varanda'),
(10, 4, 'Varanda');

INSERT INTO garcom (nome, cpf, salario, turno, comissao) VALUES
('Brenda Alves', '43815092698', 2000.0, 'Noite', 5.0),
('Arthur Borges', '39041687548', 1500.0, 'Noite', 5.0),
('Lara Abreu', '26591780386', 2000.0, 'Noite', 5.0),
('Aylla Fogaça', '54093871639', 1500.0, 'Manhã', 5.0),
('Laís Pires', '95380617484', 2000.0, 'Noite', 5.0);

INSERT INTO cozinheiro (nome, cpf, salario, especialidade) VALUES
('Carlos Eduardo Garcia', '47512869355', 3200.0, 'Grelhados'),
('Dra. Ana Sophia Pereira', '28317594041', 2500.0, 'Massas'),
('Lunna Vargas', '03962857400', 3200.0, 'Massas'),
('Luara Cunha', '76912845355', 2500.0, 'Grelhados'),
('Dra. Mariane Pacheco', '65314708280', 2500.0, 'Grelhados');

INSERT INTO prato (nome, preco, categoria) VALUES
('Bruschetta Clássica', 25.0, 'Entrada'),
('Carpaccio de Carne', 32.0, 'Entrada'),
('Dadinhos de Tapioca', 22.0, 'Entrada'),
('Salada Caprese', 28.0, 'Entrada'),
('Filé Mignon ao Poivre', 85.0, 'Prato Principal'),
('Risoto de Camarão', 78.0, 'Prato Principal'),
('Salmão Grelhado', 72.0, 'Prato Principal'),
('Espaguete à Carbonara', 55.0, 'Prato Principal'),
('Nhoque ao Sugo', 48.0, 'Prato Principal'),
('Bife de Chorizo', 89.0, 'Prato Principal'),
('Petit Gâteau', 24.0, 'Sobremesa'),
('Tiramisu', 26.0, 'Sobremesa'),
('Pudim de Leite', 18.0, 'Sobremesa'),
('Mousse de Chocolate', 20.0, 'Sobremesa'),
('Água com Gás', 6.0, 'Bebida'),
('Refrigerante Lata', 8.0, 'Bebida'),
('Suco Natural', 12.0, 'Bebida'),
('Cerveja Artesanal', 18.0, 'Bebida'),
('Vinho Tinto Taça', 25.0, 'Bebida'),
('Caipirinha', 22.0, 'Bebida');

