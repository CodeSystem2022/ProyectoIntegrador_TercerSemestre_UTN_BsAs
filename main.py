from controller.ClienteController import ClienteController
from controller.UsuarioController import UsuarioController
from controller.VentaController import VentaController
from modelo.Cliente import Cliente
from modelo.Producto import Producto
from modelo.Usuario import Usuario
from view.MainFrame import app


def test():
    # producto1: Producto = Producto('Botella Coca Cola 2 Lts', 350, 50)
    # productodao1 = ProductoDao()
    # productodao1.guardar(producto1)
    # productodao1.guardar2(producto1)
    #
    #
    # producto2: Producto = Producto('Botella Pepsi 2 Lts', 300, 50)
    # ProductoDao().guardar(producto2)
    cliente1: Cliente = Cliente('Juan', 'Calle Falsa 123', 1, 0.15)
    cliente2: Cliente = Cliente('Maria', 'Charlone 456', 2, 0.10)

    vendedor1: Usuario = Usuario('Lucas', 'Francia 231', 1, 0, 0.10)

    # pedido1: Pedido = Pedido(vendedor1, cliente1)
    # pedido1.agregar_producto(producto1, 2)
    # pedido1.agregar_producto(producto1, 4)
    # pedido1.agregar_producto(producto2, 10)


def main():
    # TODO: va en el view
    programa_corriendo = True
    while programa_corriendo:

        mostrar_menu()
        opcion_elegida = ingresar_int()
        if opcion_elegida == 1:
            listar_productos()
        elif opcion_elegida == 2:
            listar_usuarios()
        elif opcion_elegida == 3:
            agregar_productos()
        elif opcion_elegida == 4:
            agregar_usuario()
        elif opcion_elegida == 5:
            generar_venta()
        elif opcion_elegida == 6:
            eliminar_producto()
        elif opcion_elegida == 9:
            print("Gracias por utilizar nuestro programa!\nUTN Bs As @ FRSR")
            programa_corriendo = False
        else:
            print("La opción elegida no es válida")
            pausar()


# TODO: va en el view
def mostrar_menu():
    print("Menú principal @ Sistema de ventas")
    print("")
    print("1 -> Listar productos")
    print("2 -> Listar usuarios")
    print("3 -> Agregar productos")
    print("4 -> Agregar usuarios")
    print("5 -> Generar venta")
    print("6 -> Eliminar producto")

    print("9 -> Salir")
    print("Seleccione una opción: ")


# TODO: va en el view
def ingresar_int():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")


# # TODO: va en el view
# def listar_productos():
#     controlador_producto.listar()


# TODO: va en el view
def listar_usuarios():
    controlador_usuario.listar()


# # TODO: va en el view
# def eliminar_producto():
#     print("Ingrese código de producto a eliminar: ", end="")
#     codigo: int = ingresar_int()
#     producto: Producto = ProductoDao.seleccionar_producto(codigo)
#     if producto is None:
#         print("No se encontró el producto")
#     else:
#         controlador_producto.eliminar(producto)


# TODO: va en el view
def agregar_productos():
    marca = input("Ingrese marca del producto: ")
    modelo = input("Ingrese modelo del producto: ")
    print("Ingresar precio del producto: ", end="")
    precio = ingresar_int()
    print("Ingresar stock inicial: ", end="")
    stock = ingresar_int()
    producto = Producto(marca=marca, modelo=modelo, precio=precio, stock=stock)
    controlador_producto.guardar(producto)


# TODO: va en el view
def agregar_usuario():
    # Lógica para agregar vendedores
    apellido = input("Ingrese apellido del usuario: ")
    nombre = input("Ingrese nombre del usuario: ")
    print("Ingresar dni del usuario: ", end="")
    documento = ingresar_int()
    porcentualcomision = 1
    while 0 < porcentualcomision <= 1:
        porcentualcomision = float(input("Ingrese porcentaje de comisión del usuario: "))
        usuario = Usuario(apellido=apellido, nombre=nombre, documento=documento, porcentualcomision=porcentualcomision)
        controlador_usuario.guardar(usuario)
        return
    else:
        print('ERROR! El valor debe estar expresado en decimales (Ej: 0.1 para 10%)')


# TODO: va en el DAO VENTA
def generar_venta():
    # Lógica para generar una venta
    pass


def pausar():
    input("Presione Enter para continuar...")


if __name__ == '__main__':
    # Chequea si la base de datos existe

    # Crea conexiones a los controller's de las tablas
    # controlador_producto = ProductoController()
    controlador_usuario = UsuarioController()
    controlador_cliente = ClienteController()
    controlador_ventas = VentaController()

    # controlador_producto.listar()

    # Llama la interfaz gráfica
    app.mainloop()

# test()
# main()
