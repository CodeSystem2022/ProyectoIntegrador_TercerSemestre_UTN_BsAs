CREATE DATABASE ventas
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE ventas
    IS 'Sistema de Ventas. Proyecto integrador';