UPDATE avaliacao
SET
    nota = COALESCE(%(rating)s, nota),
    comentario = COALESCE(%(comment)s, comentario)
WHERE id_avaliacao = %(review_id)s
RETURNING id_avaliacao;