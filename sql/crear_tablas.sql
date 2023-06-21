CREATE TABLE IF NOT EXISTS public.clientes
(
    idcliente integer NOT NULL,
    apellido  "char",
    nombre    "char",
    documento integer,
    "email "  "char",
    descuento numeric(15, 2),
    CONSTRAINT clientes_pkey PRIMARY KEY (idcliente)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.clientes
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.productos
(
    idproducto integer NOT NULL,
    marca      "char",
    modelo     "char",
    precio     numeric(15, 2),
    stock      numeric(6, 0),
    CONSTRAINT productos_pkey PRIMARY KEY (idproducto)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.productos
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.usuarios
(
    idusuario integer NOT NULL,
    apellido  "char"  NOT NULL,
    nombre    "char",
    documento integer,
    login     "char"  NOT NULL,
    clave     "char",
    comision  double precision,
    CONSTRAINT usuarios_pkey PRIMARY KEY (idusuario)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.usuarios
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.ventas
(
    idventa     numeric(10, 0) NOT NULL,
    "fechaAlta" date,
    idcliente   numeric(10, 0) NOT NULL,
    idusuario   numeric(10, 0) NOT NULL,
    importe     numeric(15, 2),
    comision    numeric(15, 2),
    descuento   numeric(15, 2),
    CONSTRAINT ventas_pkey PRIMARY KEY (idventa)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ventas
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public."ventasItems"
(
    "idventaItem"    numeric(10, 0) NOT NULL,
    idventa          numeric(10, 0) NOT NULL,
    idproducto       numeric(10, 0) NOT NULL,
    cantidad         numeric(10, 0),
    "precioUnitario" numeric(15, 2)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."ventasItems"
    OWNER to postgres;

COMMENT ON TABLE public."ventasItems"
    IS 'Detalle de todos los productos que se incluyen en una venta';