def test():
    print('Hola grupo! ')


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
    # Lógica para listar productos
    pass

def listar_vendedores():
    # Lógica para listar vendedores
    pass

def agregar_productos():
    # Lógica para agregar productos
    pass

def agregar_vendedores():
    # Lógica para agregar vendedores
    pass

def generar_venta():
    # Lógica para generar una venta
    pass

def pausar():
    input("Presione Enter para continuar...")


if __name__ == '__main__':
    main()
    test()
