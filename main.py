from controller.ProductoController import ProductoController
from dao.ProductoDao import ProductoDao
from modelo.Cliente import Cliente
from modelo.Producto import Producto
from modelo.Vendedor import Vendedor


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

    vendedor1: Vendedor = Vendedor('Lucas', 'Francia 231', 1, 0, 0.10)

    # pedido1: Pedido = Pedido(vendedor1, cliente1)
    # pedido1.agregar_producto(producto1, 2)
    # pedido1.agregar_producto(producto1, 4)
    # pedido1.agregar_producto(producto2, 10)


def main():
    programa_corriendo = True
    while programa_corriendo:

        mostrar_menu()
        opcion_elegida = ingresar_int()
        if opcion_elegida == 1:
            listar_productos()
        elif opcion_elegida == 2:
            listar_vendedores()
        elif opcion_elegida == 3:
            agregar_productos()
        elif opcion_elegida == 4:
            agregar_vendedores()
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


def mostrar_menu():
    print("Menú principal @ Sistema de ventas")
    print("")
    print("1 -> Listar productos")
    print("2 -> Listar vendedores")
    print("3 -> Agregar productos")
    print("4 -> Agregar vendedores")
    print("5 -> Generar venta")
    print("6 -> Eliminar producto")
    print("9 -> Salir")
    print("Seleccione una opción: ")


def ingresar_int():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")


def listar_productos():
    controlador_producto.listar()


def listar_vendedores():
    Vendedor.listar_vendedores()


def eliminar_producto():
    print("Ingrese código de producto a eliminar: ", end="")
    codigo: int = ingresar_int()
    producto: Producto = ProductoDao.seleccionar_producto(codigo)
    if producto is None:
        print("No se encontró el producto")
    else:
        controlador_producto.eliminar(producto)



def agregar_productos():
    descripcion = input("Ingrese descripción: ")
    print("Ingresar precio de Producto: ", end="")
    precio = ingresar_int()
    print("Ingresar stock inicial: ", end="")
    stock = ingresar_int()
    producto = Producto(descripcion, precio, stock)
    controlador_producto.guardar(producto)


def agregar_vendedores():
    # Lógica para agregar vendedores
    pass


def generar_venta():
    # Lógica para generar una venta
    pass


def pausar():
    input("Presione Enter para continuar...")


if __name__ == '__main__':
    controlador_producto = ProductoController()
    controlador_producto.listar()
    # test()
    main()
