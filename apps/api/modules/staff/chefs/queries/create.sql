INSERT INTO cozinheiro (nome, cpf, salario, especialidade)
VALUES (%(name)s, %(cpf)s, %(salary)s, %(specialty)s)
RETURNING id_funcionario, nome, cpf, salario, especialidade;