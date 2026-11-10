-- Migracao para bancos criados antes da inclusao da distancia da corrida.
-- Este comando preserva os registros existentes; a nova coluna aceita NULL.

ALTER TABLE corridas
ADD COLUMN IF NOT EXISTS distancia_km NUMERIC(8, 2)
    CHECK (distancia_km > 0);
