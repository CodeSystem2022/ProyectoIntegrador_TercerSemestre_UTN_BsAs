CREATE TABLE IF NOT EXISTS public.clientes
(
    id_cliente INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    nombre     VARCHAR(40)     NOT NULL,
    apellido   VARCHAR(40)     NOT NULL,
    documento  INT             NOT NULL UNIQUE,
    email      VARCHAR(40)     NOT NULL UNIQUE,
    descuento  NUMERIC(15, 2)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.clientes
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.productos
(
    id_producto INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    marca       VARCHAR(40)     NOT NULL,
    modelo      VARCHAR(40)     NOT NULL,
    precio      NUMERIC(15, 2)  NOT NULL,
    stock       NUMERIC(6, 0)   NOT NULL
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.productos
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.usuarios
(
    id_usuario         INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    nombre             VARCHAR(40)     NOT NULL,
    apellido           VARCHAR(40)     NOT NULL,
    documento          INT             NOT NULL UNIQUE,
    porcentualcomision DOUBLE PRECISION,
    comision           DOUBLE PRECISION
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.usuarios
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.ventas
(
    id_venta   INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    fecha_alta date,
    id_cliente INT             NOT NULL,
    id_usuario INT             NOT NULL,
    importe    numeric(15, 2),
    comision   numeric(15, 2),
    descuento  numeric(15, 2),
    CONSTRAINT fk_id_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT fk_id_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ventas
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.ventas_items
(
    id_venta_item   INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    id_venta        INT,
    id_producto     INT,
    cantidad        NUMERIC(10, 0),
    precio_unitario NUMERIC(15, 2),
    CONSTRAINT fk_id_venta FOREIGN KEY (id_venta) REFERENCES ventas (id_venta),
    CONSTRAINT fk_id_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ventas_items
    OWNER to postgres;

COMMENT ON TABLE public.ventas_items
    IS 'Detalle de todos los productos que se incluyen en una venta';