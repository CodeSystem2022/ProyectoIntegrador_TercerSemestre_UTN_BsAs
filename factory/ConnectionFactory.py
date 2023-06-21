import psycopg2  # Librería para conectar con PostgreSQL


class ConnectionFactory:
    listado_conexiones = []
    dbname = 'ventas'
    user = 'postgres'
    password = 'admin'
    host = '127.0.0.1'
    port = '5432'

    def __init__(self):
        ConnectionFactory.listado_conexiones.append(self)

    @staticmethod
    def chequearDB():
        dns = f"dbname='postgres' user={ConnectionFactory.user} password={ConnectionFactory.password} host={ConnectionFactory.host} port={ConnectionFactory.port}"
        conn = psycopg2.connect(dns)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='ventas'")
        exists = cursor.fetchone()
        if not exists:
            fd = open('sql/crear_base_de_datos.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            sqlCommands = sqlFile.split(';')
            for command in sqlCommands:
                print(command)
                if command.strip() != '':
                    cursor.execute(command)
            conn.commit()
            conn.close()
            print("Base de datos creada.")
            return False
        else:
            print("Base de datos ya existe.")
            return True

    @staticmethod
    def crear_tablas():
        conn = ConnectionFactory.get_connection('crear_tablas')
        conn.autocommit = True
        cursor = conn.cursor()
        fd = open('sql/crear_tablas.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            print(command)
            if command.strip() != '':
                cursor.execute(command)
        conn.commit()
        conn.close()
        print("Tablas creadas.")

    @staticmethod
    def get_connection(desde_donde):
        print(f'Creando conexión desde {desde_donde}...')
        dns = f'dbname={ConnectionFactory.dbname} user={ConnectionFactory.user} password={ConnectionFactory.password} host={ConnectionFactory.host} port={ConnectionFactory.port}'
        return psycopg2.connect(dns)
