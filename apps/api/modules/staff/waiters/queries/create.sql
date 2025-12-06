INSERT INTO garcom (nome, cpf, salario, turno, comissao)
VALUES (%(name)s, %(cpf)s, %(salary)s, %(shift)s, %(commission)s)
RETURNING id_funcionario, nome, cpf, salario, turno, comissao;