from tkinter import ttk, messagebox, simpledialog

import customtkinter as ctk

from modelo.Producto import Producto


# Fuente
# https://customtkinter.tomschimansky.com/documentation/windows/toplevel

###############################################################
# Clase para la ventana de gestión de productos
class ProductoFrame(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus_set()
        self.grab_set()
        # Dando tamaño a la ventana
        self.geometry("650x500")

        # Dando título a la ventana
        self.title("Gestión de productos")

        # Widgets para marca, modelo, precio y stock
        # width: Ancho del widget
        # anchor: Posición del texto dentro del widget (n, s, e, w, ne, nw, se, sw)
        # padx: Espacio horizontal entre el texto y el borde del widget
        # pady: Espacio vertical entre el texto y el borde del widget

        # Label = etiqueta
        # Entry = campo de texto
        # Button = botón
        # Treeview = tabla
        # Scrollbar = barra de desplazamiento

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

        # Botón para agregar un producto
        self.botonAgregar = ctk.CTkButton(self, text="Agregar", width=600, anchor='W', command=self.agregar)
        self.botonAgregar.grid(row=5, column=0, columnspan=2, sticky='WE', padx=10, pady=10)

        # Tabla para mostrar los productos
        self.tabla = ttk.Treeview(self, columns=("Marca", "Modelo", "Precio", "Stock"))

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

        # Generamos un Scrollbar para la tabla
        self.tabla.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        # Seteamos opciones del scrollbar
        self.tabla.configure(yscrollcommand=self.tabla.scrollbar.set)
        # Ubicamos el scrollbar
        self.tabla.scrollbar.grid(columnspan=2, sticky="NSE")

        # Ubicamos la tabla
        self.tabla.grid(row=6, column=0, columnspan=2)

        # Botón para eliminar un producto
        self.botonEliminar = ctk.CTkButton(self, text="Eliminar", width=600, anchor="w", command=self.eliminar)
        self.botonEliminar.grid(row=7, column=0, columnspan=2, sticky='WE', padx=10, pady=10)

        # Etiqueta para mostrar mensajes de status
        self.labelStatus = ctk.CTkLabel(self, text="", width=600, anchor="w", padx=10, pady=10, text_color="red")
        self.labelStatus.grid(row=8, column=0, columnspan=2)

        # Listar los productos en la tabla
        self.listar_productos()

        # Eventos de la tabla
        # Evento al hacer click en una fila de la tabla
        # self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

        # Evento al hacer doble click en una fila de la tabla
        self.tabla.bind("<Double-1>", self.seleccionar_doble_click)

    ###########################################################
    # Acciones de los botones de la ventana ProductoFrame
    # Agregar un producto
    def agregar(self):
        # Valida los campos de texto
        validacion = self.validar_campos()
        if validacion:
            # Obtiene los valores de los campos de texto
            marca = self.entryMarca.get()
            modelo = self.entryModelo.get()
            precio = self.entryPrecio.get()
            stock = self.entryStock.get()

            # Crea un producto con los valores de los campos de texto
            producto = Producto(marca, modelo, precio, stock)

            # Guarda el producto en la base de datos
            MainFrame.controlador_producto.guardar(producto)
            # Muestra un mensaje de status
            self.labelStatus.configure(
                text="Producto [{} - {}] agregado correctamente".format(producto.marca, producto.modelo),
                text_color="green")
            # Limpia los campos de texto
            self.entryMarca.delete(0, "end")
            self.entryModelo.delete(0, "end")
            self.entryPrecio.delete(0, "end")
            self.entryStock.delete(0, "end")

            # Pone el foco en el campo de texto de marca
            self.entryMarca.focus()

            # Actualiza la tabla
            self.listar_productos()

    # Listar los productos en la tabla
    def listar_productos(self):
        # Elimina todos los registros de la tabla
        self.tabla.delete(*self.tabla.get_children())
        # Obtiene todos los productos de la base de datos
        productos: list = MainFrame.controlador_producto.listar()
        # Agrega los productos a la tabla
        for producto in productos:
            texto_precio = "$ {}".format(producto.precio)
            self.tabla.insert("", "end",
                              text=producto.codigo,
                              values=(producto.marca, producto.modelo, texto_precio, producto.stock))

    # Elimina una fila
    def eliminar(self):
        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "" or self.tabla.focus() is None:
            print("No hay nada seleccionado")
            return

        if messagebox.askyesno("Eliminar", "¿Desea eliminar el producto seleccionado?", parent=self):
            # Si hay una fila seleccionada, la guarda en la variable indice
            indice = self.tabla.focus()
            # print(indice)
            # Devuelve el valor de la columna 0 (ID)
            id_producto = str(self.tabla.item(indice, "text"))
            # devuelve el valor de la columna 1 (Marca)
            marca = str(self.tabla.item(indice, "values")[0])
            # devuelve el valor de la columna 2 (Modelo)
            modelo = str(self.tabla.item(indice, "values")[1])
            # devuelve el valor de la columna 3 (Precio)
            precio = str(self.tabla.item(indice, "values")[2])
            # devuelve el valor de la columna 4 (Stock)
            stock = str(self.tabla.item(indice, "values")[3])

            # print(id_producto)

            # Elimina el registro de la base de datos y
            # guarda en resultado la cantidad de registros eliminados
            resultado = MainFrame.controlador_producto.eliminar(id_producto)

            # Si resultado existe, es porque se eliminó el registro
            # de la base de datos, entonces la borramos de la tabla

            try:
                int(resultado)

                self.tabla.delete(indice)
                self.labelStatus.configure(

                    text="Producto Id: {} [{} - {}] eliminado".format(id_producto, marca, modelo))

            except ValueError as e:
                # Si resultado devuelve un mensaje de error por llave foránea
                if "foreign key" in resultado:
                    # Muestra un mensaje de error
                    self.labelStatus.configure(
                        text="No se puede eliminar el producto [{} - {}] porque tiene ventas asociadas".format(marca,
                                                                                                               modelo),
                        text_color="red")
                    return
                else:
                    return

    # Acciones al seleccionar una fila de la tabla
    # TODO: Borrar ?
    def seleccionar(self, event):
        item = self.tabla.identify('item', event.x, event.y)
        if item:
            print("Hiciste click simple en: ", self.tabla.item(item, "text"))
        else:
            print("1C: No hay nada seleccionado")
            self.tabla.selection_clear()

    # Modificar al hacer doble click en una fila de la tabla
    # Funcional OK
    def seleccionar_doble_click(self, event):
        # Guarda el nombre de las columnas
        # columnas = ["Codigo", "Marca", "Modelo", "Precio", "Stock"]

        # Obtiene el indice de la fila seleccionada
        fila = self.tabla.identify('item', event.x, event.y)
        # print("Fila Seleccionada:", fila)

        # Obtiene el indice de la columna seleccionada
        columna = int(self.tabla.identify_column(event.x).replace("#", ""))
        # print("Columna Seleccionada:", columnas[columna])

        # Si fila y columna son distintos de 0, es porque se seleccionó una celda
        # Si fila es 0, es porque se seleccionó el encabezado de la tabla
        # Si columna es 0, es porque se seleccionó el ID

        if fila and columna:  # Si fila y columna son distintos de 0
            # Obtiene los valores de la fila seleccionada
            codigo = self.tabla.item(fila, "text")
            marca = self.tabla.item(fila, "values")[0]
            modelo = self.tabla.item(fila, "values")[1]
            precio = self.tabla.item(fila, "values")[2].replace("$ ", "")
            stock = self.tabla.item(fila, "values")[3]

            # Si la columna es 0, es porque se seleccionó el ID, no se hace nada
            # Si la columna es 1, es porque se hizo doble click en la columna marca
            if columna == 1:
                marca = simpledialog.askstring("Modificar Marca", "Marca:", initialvalue=marca, parent=self)
            # Si la columna es 2, es porque se hizo doble click en la columna modelo
            elif columna == 2:
                modelo = simpledialog.askstring("Modificar Modelo", "Modelo:", initialvalue=modelo, parent=self)
            # Si la columna es 3, es porque se hizo doble click en la columna precio
            elif columna == 3:
                precio = simpledialog.askfloat("Modificar Precio", "Precio:", initialvalue=precio, parent=self)
            # Si la columna es 4, es porque se hizo doble click en la columna stock
            elif columna == 4:
                stock = simpledialog.askinteger("Modificar Stock", "Stock:", initialvalue=stock, parent=self)

            # Chequeamos que no haya un valor null
            # cuando se modifica el producto y se aprieta cancelar
            if marca is None or modelo is None or precio is None or stock is None:
                return

            # Crea un producto con los valores modificados
            producto = Producto(codigo=codigo, marca=marca, modelo=modelo, precio=precio, stock=stock)

            # Actualiza el producto en la base de datos
            MainFrame.controlador_producto.actualizar(producto)

            # Actualiza la tabla
            self.listar_productos()

    # Valida los campos de texto
    def validar_campos(self):
        # Valida que el campo de texto Marca no esté vacío
        if self.entryMarca.get() == "":
            messagebox.showwarning("Error", "Debe ingresar una marca", parent=self)
            self.entryMarca.focus()
            return False

        # Valida que el campo de texto Modelo no esté vacío
        if self.entryModelo.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un modelo", parent=self)
            self.entryModelo.focus()
            return False

        # Valida que el campo de texto Precio no esté vacío
        if self.entryPrecio.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el precio", parent=self)
            self.entryPrecio.focus()
            return False
        else:
            # Valida que el valor ingresado en Precio sea un número
            try:
                float(self.entryPrecio.get())
            except ValueError:
                messagebox.showwarning("Error", "El precio debe ser un número", parent=self)
                self.entryPrecio.focus()
                return False

        # Valida que el campo de texto Stock no esté vacío
        if self.entryStock.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el stock", parent=self)
            self.entryStock.focus()
            return False
        else:
            # Valida que el valor ingresado en Stock sea un número entero
            try:
                int(self.entryStock.get())
            except ValueError:
                messagebox.showwarning("Error", "El valor de stock debe ser un número entero", parent=self)
                self.entryStock.focus()
                return False
        # Si pasó todas las validaciones, devuelve True
        return True
