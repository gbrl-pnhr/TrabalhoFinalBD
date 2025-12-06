SELECT
    m.id_mesa,
    m.numero,
    m.capacidade,
    m.localizacao,
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM pedido p
            WHERE p.id_mesa = m.id_mesa
            AND p.status = 'OPEN'
        ) THEN true
        ELSE false
    END as is_occupied
FROM mesa m
WHERE m.id_mesa = %(id)s;