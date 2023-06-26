from tkinter import ttk

import customtkinter as ctk

from controller.ProductoController import ProductoController
from factory.ConnectionFactory import ConnectionFactory


# Fuente
# https://customtkinter.tomschimansky.com/documentation/windows/toplevel

# controlador_producto = ProductoController()


class ProductoFrame(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Controlador de la tabla Productos
        # controlador_producto = ProductoController()

        # Dando tamaño a la ventana
        self.geometry("650x400")
        # Dando título a la ventana
        self.title("Gestión de productos")

        # Frame contenedor de los widgets
        # self.frame = ctk.CTkFrame(self, width=400, height=300)
        # self.frame.grid(row=0, column=0, pady=20)

        # Widgets para marca, modelo, precio y stock
        # width: Ancho del widget
        # anchor: Posición del texto dentro del widget (n, s, e, w, ne, nw, se, sw)
        # padx: Espacio horizontal entre el texto y el borde del widget
        # pady: Espacio vertical entre el texto y el borde del widget

        # Label = etiqueta
        # Entry = campo de texto
        # Button = botón
        # Treeview = tabla

        self.labelMarca = ctk.CTkLabel(self, text="Marca: ", width=130, anchor="w", padx=10, pady=10)
        self.labelMarca.grid(row=1, column=0)
        self.entryMarca = ctk.CTkEntry(self, width=450)
        self.entryMarca.grid(row=1, column=1)

        self.labelModelo = ctk.CTkLabel(self, text="Modelo: ", width=130, anchor="w", padx=10, pady=10)
        self.labelModelo.grid(row=2, column=0)
        self.entryModelo = ctk.CTkEntry(self, width=450)
        self.entryModelo.grid(row=2, column=1)

        self.labelPrecio = ctk.CTkLabel(self, text="Precio: ", width=130, anchor="w", padx=10, pady=10)
        self.labelPrecio.grid(row=3, column=0)
        self.entryPrecio = ctk.CTkEntry(self, width=450)
        self.entryPrecio.grid(row=3, column=1)

        self.labelStock = ctk.CTkLabel(self, text="Stock: ", width=130, anchor="w", padx=10, pady=10)
        self.labelStock.grid(row=4, column=0)
        self.entryStock = ctk.CTkEntry(self, width=450)
        self.entryStock.grid(row=4, column=1)

        # Botones para agregar, modificar y eliminar
        self.botonModificar = ctk.CTkButton(self, text="Modificar", width=130, anchor="w")
        self.botonModificar.grid(row=5, column=0)
        self.botonEliminar = ctk.CTkButton(self, text="Eliminar", width=130, anchor="w", command=self.eliminar)
        self.botonEliminar.grid(row=5, column=1)

        self.tabla = ttk.Treeview(self,
                                  columns=("Marca", "Modelo", "Precio", "Stock")

                                  )

        # heading: Texto de la cabecera de la columna
        self.tabla.heading("#0", text="ID")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Stock", text="Stock")

        # column: Nombre de la columna
        self.tabla.column("#0", width=50)
        self.tabla.column("Marca", width=200)
        self.tabla.column("Modelo", width=200)
        self.tabla.column("Precio", width=100, anchor="center")
        self.tabla.column("Stock", width=100, anchor="center")

        # Ubicación de la tabla
        self.tabla.grid(row=6, column=0, columnspan=2)

        # Listar los productos en la tabla
        productos = MainFrame.controlador_producto.listar()
        for producto in productos:
            self.tabla.insert("", "end", text=producto.codigo,
                              values=(producto.marca, producto.modelo, producto.precio, producto.stock))

        # Evento al hacer click en una fila de la tabla
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

        # Evento al hacer doble click en una fila de la tabla
        self.tabla.bind("<Double-1>", self.seleccionar_doble_click)

    ###########################################################
    # Acciones de los botones de la ventana ProductoFrame
    # Elimina una fila de la tabla
    def eliminar(self):

        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "":
            print("No hay nada seleccionado")
            return
        # Si hay una fila seleccionada, la guarda en la variable indice
        indice = self.tabla.focus()
        # Devuelve el valor de la columna 0 (ID)
        id = str(self.tabla.item(indice, "text"))
        print("Eliminado el registro con ID: {0}".format(id))

        # TODO: ya funciona, se desabilitó para no borrar la base de datos cada vez q lo probamos
        # controlador_producto.eliminar(str(id))

        # Elimina la fila de la tabla
        self.tabla.delete(indice)

    # Acciones al seleccionar una fila de la tabla
    def seleccionar(self, event):
        item = self.tabla.identify('item', event.x, event.y)
        if item:
            print("Hiciste click simple en: ", self.tabla.item(item, "text"))
        else:
            print("1C: No hay nada seleccionado")

    # Acciones al hacer doble click en una fila de la tabla
    def seleccionar_doble_click(self, event):
        item = self.tabla.identify('item', event.x, event.y)
        if item:
            print("Hiciste doble click en:", self.tabla.item(item, "text"))
        else:
            print("2: No hay nada seleccionado")


class MainFrame(ctk.CTk):
    if not ConnectionFactory.chequearDB():
        ConnectionFactory.crear_tablas()
    ctk.set_appearance_mode("light")

    ctk.set_default_color_theme("blue")
    controlador_producto = ProductoController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("Sistema de Ventas - Grupo: UTN Bs As")
        self.button_1 = ctk.CTkButton(self, text="Gestión de Productos",
                                      command=self.abrir_productos)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.sub_ventana = None

    def abrir_productos(self):
        if self.sub_ventana is None or not self.sub_ventana.winfo_exists():
            self.sub_ventana = ProductoFrame(self)  # create window if its None or destroyed
        else:
            self.sub_ventana.focus()  # if window exists focus it


app = MainFrame()
