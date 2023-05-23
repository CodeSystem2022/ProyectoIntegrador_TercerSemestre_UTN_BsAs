from modelo.Cliente import Cliente
from modelo.Pedido import Pedido
from modelo.Producto import Producto
from modelo.Vendedor import Vendedor


def test():
    producto1: Producto = Producto(1, 'Botella Coca Cola 2 Lts', 350, 50)
    producto2: Producto = Producto(2, 'Botella Pepsi 2 Lts', 300, 50)

    cliente1: Cliente = Cliente('Juan', 'Calle Falsa 123', 1, 0.15)
    cliente2: Cliente = Cliente('Maria', 'Charlone 456', 2, 0.10)

    vendedor1: Vendedor = Vendedor('Lucas', 'Francia 231', 1, 0, 0.10)

    pedido1: Pedido = Pedido(vendedor1, cliente1)
    pedido1.agregar_producto(producto1, 2)
    pedido1.agregar_producto(producto1, 4)
    pedido1.agregar_producto(producto2, 10)


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
    print("9 -> Salir")
    print("Seleccione una opción: ")


def ingresar_int():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")


def listar_productos():
    Producto.listar_productos()


def listar_vendedores():
    Vendedor.listar_vendedores()


def agregar_productos():
    print("Ingresar código de Producto: ", end="")
    codigo = ingresar_int()
    descripcion = input("Ingrese descripción: ")
    print("Ingresar precio de Producto: ", end="")
    precio = ingresar_int()
    print("Ingresar stock inicial: ", end="")
    stock = ingresar_int()
    Producto(codigo, descripcion, precio, stock)


def agregar_vendedores():
    # Lógica para agregar vendedores
    pass


def generar_venta():
    # Lógica para generar una venta
    pass


def pausar():
    input("Presione Enter para continuar...")


if __name__ == '__main__':
    test()
    main()
