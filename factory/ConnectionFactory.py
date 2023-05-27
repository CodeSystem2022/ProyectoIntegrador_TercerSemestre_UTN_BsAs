import psycopg2  # Librería para conectar con PostgreSQL


class ConnectionFactory:
    listado_conexiones = []
    dbname = 'proyecto_integrador'
    user = 'postgres'
    password = 'admin'
    host = '127.0.0.1'
    port = '5432'

    def __init__(self):
        ConnectionFactory.listado_conexiones.append(self)

    @staticmethod
    def get_connection(desde_donde):
        print(f'Creando conexión desde {desde_donde}...')
        dns = f'dbname={ConnectionFactory.dbname} user={ConnectionFactory.user} password={ConnectionFactory.password} host={ConnectionFactory.host} port={ConnectionFactory.port}'
        return psycopg2.connect(dns)
