import psycopg2  # Librería para conectar con PostgreSQL


# Una fábrica de conexiones, con sus respectivas opciones
class ConnectionFactory:
    listado_conexiones = []
    dbname = 'ventas'
    user = 'postgres'
    password = 'admin'
    host = '127.0.0.1'
    port = '5432'

    # Al inicializar una nueva conexion, la guarda en una lista
    def __init__(self):
        ConnectionFactory.listado_conexiones.append(self)

    # Chequea si existe la base de datos en la computadora
    # Si existe, no hace nada más, sino, la crea
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
            conn.close()
            print("Base de datos ya existe.")
            return True

    # Si crea la base de datos, llama a la función para crear las tablas necesarias
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

    # Este método devuelve una conexion creada
    @staticmethod
    def get_connection(desde_donde):
        print(f'Creando conexión desde {desde_donde}...')
        dns = f'dbname={ConnectionFactory.dbname} user={ConnectionFactory.user} password={ConnectionFactory.password} host={ConnectionFactory.host} port={ConnectionFactory.port}'
        return psycopg2.connect(dns)
