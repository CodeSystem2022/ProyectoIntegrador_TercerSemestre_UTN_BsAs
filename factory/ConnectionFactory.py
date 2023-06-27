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
        print("Se ha creado una nueva conexión.")
        # Lista de conexiones
        for conexion in ConnectionFactory.listado_conexiones:
            print(conexion)

    def __str__(self):
        return f"dbname={self.dbname} user={self.user} password={self.password} host={self.host} port={self.port}"

    # Chequea si existe la base de datos en la computadora
    # Si existe, no hace nada más, sino, la crea
    @staticmethod
    def chequearDB():
        dns = f"dbname='postgres' user={ConnectionFactory.user} password={ConnectionFactory.password} host={ConnectionFactory.host} port={ConnectionFactory.port}"
        conexion = psycopg2.connect(dns)
        conexion.autocommit = True
        with conexion.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname='ventas'")
            exists = cursor.fetchone()
            if not exists:
                with open('sql/crear_base_de_datos.sql', 'r') as fd:
                    sqlFile = fd.read()

                sqlCommands = sqlFile.split(';')
                for command in sqlCommands:
                    # print(command)
                    if command.strip() != '':
                        cursor.execute(command)
                print("Base de datos creada.")
                conexion.close()
                return False
            else:
                conexion.close()
                # print("Base de datos ya existe.")
                return True

    # Si crea la base de datos, llama a la función para crear las tablas necesarias
    @staticmethod
    def crear_tablas():
        # Crea la conexión
        conexion = ConnectionFactory.get_connection('crear_tablas')
        # Activa el autocommit
        conexion.autocommit = True
        # Crea el cursor
        with conexion.cursor() as cursor:
            # Abre el archivo con los comandos sql
            with open('sql/crear_tablas.sql', 'r') as fd:
                # Lee el archivo y lo guarda en una variable
                sqlFile = fd.read()

            # Separa los comandos a ejecutar
            sqlCommands = sqlFile.split(';')
            # Recorre los comandos
            for command in sqlCommands:
                # print(command)
                # Si el comando no está vacío, lo ejecuta
                if command.strip() != '':
                    cursor.execute(command)
        # Cierra la conexión
        conexion.close()

    # Este método devuelve una conexion creada
    @staticmethod
    def get_connection(desde_donde):
        # TODO: Borrar print al terminar
        print(f'Creando conexión desde {desde_donde}...')
        dns = f'dbname={ConnectionFactory.dbname} user={ConnectionFactory.user} password={ConnectionFactory.password} host={ConnectionFactory.host} port={ConnectionFactory.port}'
        return psycopg2.connect(dns)
