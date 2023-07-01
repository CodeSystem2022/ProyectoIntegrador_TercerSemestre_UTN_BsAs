import tkinter
from builtins import int
from tkinter import ttk, messagebox, simpledialog

import customtkinter as ctk

from controller.ClienteController import ClienteController
from controller.ProductoController import ProductoController
from controller.UsuarioController import UsuarioController
from controller.VentaController import VentaController
from factory.ConnectionFactory import ConnectionFactory
from modelo.Cliente import Cliente
from modelo.Producto import Producto
from modelo.Usuario import Usuario


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
            self.tabla.insert("", "end",
                              text=producto.codigo,
                              values=(producto.marca, producto.modelo, producto.precio, producto.stock))

    # Elimina una fila
    def eliminar(self):
        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "" or self.tabla.focus() is None:
            print("No hay nada seleccionado")
            return
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
        if resultado:
            self.tabla.delete(indice)
            self.labelStatus.configure(text="Producto Id: {} [{} - {}] eliminado".format(id_producto, marca, modelo))

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
            precio = self.tabla.item(fila, "values")[2]
            stock = self.tabla.item(fila, "values")[3]

            # Si la columna es 0, es porque se seleccionó el ID, no se hace nada
            # Si la columna es 1, es porque se hizo doble click en la columna marca
            if columna == 1:
                marca = simpledialog.askstring("Modificar Marca", "Marca:", initialvalue=marca)
            # Si la columna es 2, es porque se hizo doble click en la columna modelo
            elif columna == 2:
                modelo = simpledialog.askstring("Modificar Modelo", "Modelo:", initialvalue=modelo)
            # Si la columna es 3, es porque se hizo doble click en la columna precio
            elif columna == 3:
                precio = simpledialog.askfloat("Modificar Precio", "Precio:", initialvalue=precio)
            # Si la columna es 4, es porque se hizo doble click en la columna stock
            elif columna == 4:
                stock = simpledialog.askinteger("Modificar Stock", "Stock:", initialvalue=stock)

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
            messagebox.showwarning("Error", "Debe ingresar una marca")
            self.entryMarca.focus()
            return False

        # Valida que el campo de texto Modelo no esté vacío
        if self.entryModelo.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un modelo")
            self.entryModelo.focus()
            return False

        # Valida que el campo de texto Precio no esté vacío
        if self.entryPrecio.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el precio")
            return False
        else:
            # Valida que el valor ingresado en Precio sea un número
            try:
                float(self.entryPrecio.get())
            except ValueError:
                messagebox.showwarning("Error", "El precio debe ser un número")
                self.entryPrecio.focus()
                return False

        # Valida que el campo de texto Stock no esté vacío
        if self.entryStock.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el stock")
            return False
        else:
            # Valida que el valor ingresado en Stock sea un número entero
            try:
                int(self.entryStock.get())
            except ValueError:
                messagebox.showwarning("Error", "El valor de stock debe ser un número entero")
                self.entryStock.focus()
                return False
        # Si pasó todas las validaciones, devuelve True
        return True


###############################################################
# Clase para la ventana de gestión de ventas
class VentaFrame(ctk.CTkToplevel):
    # Usuario y cliente para generar la venta
    usuario: Usuario = None
    cliente: Cliente = None
    producto: Producto = None
    producto_pedido: Producto = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: se borra ?
        MainFrame.controlador_ventas.ultima_venta()

        # Dando focus a la ventana
        self.focus_set()
        self.grab_set()

        # Dando tamaño a la ventana
        self.geometry("740x550")
        # Dando título a la ventana
        self.title("Gestión de ventas")
        # Cambiamos el color de la ventana
        self.config(bg="#b3cde0")

        # Creamos un frame para los clientes
        self.frameCliente = ctk.CTkFrame(self, corner_radius=0, border_width=0)
        # Cambiamos colores del frame
        self.frameCliente.configure(fg_color="#b3cde0")
        # Insertamos el frame en la ventana
        self.frameCliente.grid(row=0, column=0, sticky="we")

        # Creamos un label para el cliente
        self.labelCliente = ctk.CTkLabel(self.frameCliente, text="  Cliente: ", anchor="w", text_color="#011f4b",
                                         width=350)
        self.labelCliente.grid(row=0, column=0, sticky="we")

        # Creamos un listbox para mostrar los clientes
        self.listaCliente = tkinter.Listbox(self.frameCliente, width=50, height=4)

        # Agregamos un scrollbar a la lista
        self.scrollbarCliente = tkinter.Scrollbar(self.frameCliente, orient="vertical", borderwidth=0)
        self.listaCliente.config(yscrollcommand=self.scrollbarCliente.set)
        self.scrollbarCliente.config(command=self.listaCliente.yview)
        self.scrollbarCliente.grid(sticky="NSE", column=1)

        # Insertamos los clientes en la lista, contador_cliente es para el indice de la lista
        contador_cliente = 0
        for cliente in MainFrame.controlador_cliente.listar():
            contador_cliente += 1
            self.listaCliente.insert(contador_cliente,
                                     '({}) - {} {}'.format(cliente.codigo, cliente.nombre, cliente.apellido))

        # Agregamos un evento para cuando se seleccione un cliente
        self.listaCliente.bind("<<ListboxSelect>>", self.OnSelectCliente)

        # Insertamos la lista en el frame
        self.listaCliente.grid(row=1, column=0, sticky="we")

        # Creamos un label para status de cliente
        self.labelStatusCliente = ctk.CTkLabel(self.frameCliente, text="", anchor="center",
                                               text_color="#005b96")
        self.labelStatusCliente.grid(row=2, column=0, sticky="ns")

        # Creamos un frame para los usuarios
        self.frameUsuario = ctk.CTkFrame(self, corner_radius=0, border_width=0)
        # Cambiamos colores del frame
        self.frameUsuario.configure(fg_color="#b3cde0")
        # Insertamos el frame en la ventana
        self.frameUsuario.grid(row=0, column=1, sticky="we")

        # Creamos un label para el usuario
        self.labelUsuario = ctk.CTkLabel(self.frameUsuario, text="  Usuario: ", anchor="w", text_color="#011f4b",
                                         width=350)
        self.labelUsuario.grid(row=0, column=0, sticky="we")

        # Creamos un listbox para mostrar los usuarios
        self.listaUsuario = tkinter.Listbox(self.frameUsuario, width=50, height=4)

        # Agregamos un scrollbar a la lista
        self.scrollbarUsuario = tkinter.Scrollbar(self.frameUsuario, orient="vertical")
        self.listaUsuario.config(yscrollcommand=self.scrollbarUsuario.set)
        self.scrollbarUsuario.config(command=self.listaUsuario.yview)
        self.scrollbarUsuario.grid(sticky="NSE", column=1)

        # Insertamos los usuarios en la lista, contador_usuario es para el indice de la lista
        contador_usuario = 0
        for usuario in MainFrame.controlador_usuario.listar():
            contador_usuario += 1
            self.listaUsuario.insert(contador_usuario,
                                     '({}) - {} {}'.format(usuario.codigo, usuario.nombre, usuario.apellido))

        # Agregamos un evento para cuando se seleccione un cliente
        self.listaUsuario.bind("<<ListboxSelect>>", self.OnSelectUsuario)

        # Insertamos la lista en el frame
        self.listaUsuario.grid(row=1, column=0, sticky="we")

        # Creamos un label para status de usuario
        self.labelStatusUsuario = ctk.CTkLabel(self.frameUsuario, text="", anchor="center",
                                               text_color="#005b96")
        self.labelStatusUsuario.grid(row=2, column=0, sticky="ns")

        # Colocamos un separador
        self.separador = ttk.Separator(self, orient="horizontal")
        self.separador.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Creamos un menu para los productos
        self.listaDesplegableProductos = ttk.Combobox(self, state="readonly", width=50)

        # Insertamos los productos en la lista
        self.listaDesplegableProductos["values"] = MainFrame.controlador_producto.listar()
        self.listaDesplegableProductos.bind("<<ComboboxSelected>>", self.OnSelectProducto)
        self.listaDesplegableProductos.grid(row=2, column=0, sticky="ns")

        self.labelListaProductos = ctk.CTkLabel(self, text="\n\n\n", anchor="center", text_color="#011f4b",
                                                bg_color="#b3cde0")
        self.labelListaProductos.grid(row=2, column=1, sticky="sn", rowspan=2)

        # Colocamos un boton para agregar productos a la lista
        self.botonAgregarProductos = ctk.CTkButton(self, text="Agregar producto", command=self.agregarProducto)
        self.botonAgregarProductos.grid(row=3, column=0)

        # Colocamos un separador
        self.separador2 = ttk.Separator(self, orient="horizontal")
        self.separador2.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Tabla para mostrar los productos en la orden de compra
        self.tablaItemsProductos = ttk.Treeview(self, columns=("Marca", "Modelo", "Precio", "Cantidad", "PrecioFinal"))

        # heading: Texto de la cabecera de la columna
        self.tablaItemsProductos.heading("#0", text="ID")
        self.tablaItemsProductos.heading("Marca", text="Marca")
        self.tablaItemsProductos.heading("Modelo", text="Modelo")
        self.tablaItemsProductos.heading("Precio", text="Precio")
        self.tablaItemsProductos.heading("Cantidad", text="Cantidad")
        self.tablaItemsProductos.heading("PrecioFinal", text="Precio Final")

        # column: Nombre de la columna
        self.tablaItemsProductos.column("#0", width=55)
        self.tablaItemsProductos.column("Marca", width=200)
        self.tablaItemsProductos.column("Modelo", width=200)
        self.tablaItemsProductos.column("Precio", width=90)
        self.tablaItemsProductos.column("Cantidad", width=55, anchor="center")
        self.tablaItemsProductos.column("PrecioFinal", width=90, anchor="center")

        # Generamos un Scrollbar para la tabla
        self.tablaItemsProductos.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                                           command=self.tablaItemsProductos.yview)
        # Seteamos opciones del scrollbar
        self.tablaItemsProductos.configure(yscrollcommand=self.tablaItemsProductos.scrollbar.set)
        # Ubicamos el scrollbar
        self.tablaItemsProductos.scrollbar.grid(columnspan=2, sticky="NSE", rowspan=2)

        # Ubicamos la tabla
        self.tablaItemsProductos.grid(row=5, column=0, columnspan=2, pady=5)

        # Colocamos un boton para eliminar productos a la lista
        self.botonEliminarProductos = ctk.CTkButton(self, text="Eliminar producto", command=self.eliminarProducto)
        self.botonEliminarProductos.grid(row=7, column=0)

        # Colocamos una label para mostrar el total de la venta
        self.labelTotalVenta = ctk.CTkLabel(self, text="Total de la venta: ", anchor="center", text_color="#011f4b",
                                            bg_color="#b3cde0")
        self.labelTotalVenta.grid(row=7, column=1)

        # Colocamos un separador
        self.separador3 = ttk.Separator(self, orient="horizontal")
        self.separador3.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=15)

        # Colocamos un boton para cancelar la venta
        self.botonCancelarVenta = ctk.CTkButton(self, text="Cancelar venta", command=self.cancelarVenta)
        self.botonCancelarVenta.grid(row=9, column=0)

        # Colocamos un boton para finalizar la venta
        self.botonFinalizarVenta = ctk.CTkButton(self, text="Finalizar venta")  # , command=self.finalizarVenta)
        self.botonFinalizarVenta.grid(row=9, column=1)

    def OnSelectCliente(self, event):
        seleccion = self.listaCliente.curselection()
        if seleccion:
            VentaFrame.cliente = None
            # Chequeamos que haya un elemento seleccionado
            # if (!self.listaCliente.curselection()) or (!self.listaUsuario.curselection()):
            #     return
            # Obtenemos el índice del elemento seleccionado
            index = self.listaCliente.curselection()[0]
            # Obtenemos el texto del elemento seleccionado
            cliente_elegido = self.listaCliente.get(index)
            # Separamos el codigo del nombre y apellido
            codigo_cliente = cliente_elegido.split(")")[0].replace("(", "")
            # Buscamos el cliente por id, lo guardamos en la variable cliente
            VentaFrame.cliente = MainFrame.controlador_cliente.buscar_por_id(codigo_cliente)
            # Insertamos el texto en el label de status
            texto = 'Cliente seleccionado: {} {}'.format(VentaFrame.cliente.nombre, VentaFrame.cliente.apellido)
            self.labelStatusCliente.configure(text=texto)

    def OnSelectUsuario(self, event):
        seleccion = self.listaUsuario.curselection()
        if seleccion:
            VentaFrame.usuario = None
            # Chequeamos que haya un elemento seleccionado
            # if (!self.listaCliente.curselection()) or (!self.listaUsuario.curselection()):
            #     return
            # Obtenemos el índice del elemento seleccionado
            index = self.listaUsuario.curselection()[0]
            # Obtenemos el texto del elemento seleccionado
            usuario_elegido = self.listaUsuario.get(index)
            # Separamos el codigo del nombre y apellido
            codigo_usuario = usuario_elegido.split(")")[0].replace("(", "")
            # Buscamos el usuario por id, lo guardamos en la variable cliente
            VentaFrame.usuario = MainFrame.controlador_usuario.buscar_por_id(codigo_usuario)
            # Insertamos el texto en el label de status
            texto = 'Usuario seleccionado: {} {}'.format(VentaFrame.usuario.nombre, VentaFrame.usuario.apellido)
            self.labelStatusUsuario.configure(text=texto)

    def OnSelectProducto(self, event):
        producto_elegido = self.listaDesplegableProductos.get()
        codigo_producto = producto_elegido.split(" ->")[0]
        VentaFrame.producto = None
        # Buscamos el usuario por id, lo guardamos en la variable cliente
        print("Codigo de producto: {}".format(codigo_producto))
        VentaFrame.producto = MainFrame.controlador_producto.buscar_por_id(codigo_producto)

        for item in self.tablaItemsProductos.get_children():

            # Si coinciden los codigos de producto
            if self.tablaItemsProductos.item(item)["text"] == VentaFrame.producto.codigo:
                VentaFrame.producto.stock -= int(self.tablaItemsProductos.item(item)["values"][3])

        # Insertamos el texto en el label de status
        texto = '''Código Producto: {}
        Marca: {}   Modelo: {}
        Precio: $ {}    Stock: {}
        '''.format(VentaFrame.producto.codigo, VentaFrame.producto.marca, VentaFrame.producto.modelo,
                   VentaFrame.producto.precio, VentaFrame.producto.stock)
        self.labelListaProductos.configure(text=texto)

    def agregarProducto(self):
        print("Producto: {}".format(VentaFrame.producto))

        # Si hay un producto seleccionado, un cliente y un usuario
        if VentaFrame.producto and VentaFrame.cliente and VentaFrame.usuario:
            print("Producto Stock: {}".format(VentaFrame.producto.stock))

            # stockdisponible = VentaFrame.producto.stock

            # Si el stock del producto es mayor a 1
            if VentaFrame.producto.stock >= 1:

                # Pedimos al usuario ingrese la cantidad de productos a agregar

                cantidad = simpledialog.askinteger("Cantidad",
                                                   "Ingrese la cantidad de productos a agregar\nMin:01 - Max:{}".format(
                                                       VentaFrame.producto.stock), minvalue=1,
                                                   maxvalue=VentaFrame.producto.stock, parent=self)

                # Validacion al apretar cancelar en el cuadro de dialogo
                if cantidad is not None:

                    # Si el producto ya esta en la lista, sumamos la cantidad
                    for item in self.tablaItemsProductos.get_children():

                        # Si coinciden los codigos de producto
                        if self.tablaItemsProductos.item(item)["text"] == VentaFrame.producto.codigo:

                            # Obtenemos la cantidad actual en la lista
                            cantidad_actual = int(self.tablaItemsProductos.item(item)["values"][3])

                            # cantidad_total = cantidad_actual + cantidad
                            print(cantidad_actual)
                            if cantidad <= VentaFrame.producto.stock:
                                # Sumamos la cantidad actual con la nueva
                                cantidad += cantidad_actual
                                # Eliminamos el item de la tabla
                                self.tablaItemsProductos.delete(item)
                                break
                            else:
                                messagebox.showerror("Error", "No hay suficiente stock para esa cantidad", parent=self)
                                return

                                # Si la cantidad es válida, agregamos el producto a la tabla
                    self.tablaItemsProductos.insert("", "end", text=VentaFrame.producto.codigo,
                                                    values=(VentaFrame.producto.marca, VentaFrame.producto.modelo,
                                                            VentaFrame.producto.precio, cantidad,
                                                            VentaFrame.producto.precio * cantidad))

                    # Restamos la cantidad de productos al stock del producto
                    VentaFrame.producto.stock -= cantidad
                    # TODO: en este punto se podria crear la tabla de ventas
                    # Desabilitamos la lista de clientes
                    self.listaCliente.configure(state="disabled")

                    # Desabilitamos la lista de usuarios
                    self.listaUsuario.configure(state="disabled")

                    # Reseteamos la seleccion de la lista de productos
                    self.listaDesplegableProductos.set("")

                    # Reseteamos el label de la lista de productos
                    self.labelListaProductos.configure(text="\n\n\n")

                    # Reseteamos el producto seleccionado
                    VentaFrame.producto = None

                    # MainFrame.controlador_producto.actualizar(VentaFrame.producto)
                    # Actualizamos la lista de productos

                    # # Actualizamos el precio total de la venta
                    # self.actualizarPrecioTotal()
                else:
                    messagebox.showerror("Error", "Debe ingresar una cantidad válida", parent=self)
            else:
                messagebox.showerror("Error", "No hay stock disponible", parent=self)
        else:
            messagebox.showerror("Error", "Debe seleccionar un cliente, un usuario y un producto", parent=self)

    def eliminarProducto(self):
        # Obtenemos el item seleccionado
        item_seleccionado = self.tablaItemsProductos.selection()

        # Si hay un item seleccionado
        if item_seleccionado:
            # Obtenemos la cantidad del producto seleccionado
            cantidad = int(self.tablaItemsProductos.item(item_seleccionado)["values"][3])

            # Obtenemos el codigo del producto seleccionado
            codigo_producto = self.tablaItemsProductos.item(item_seleccionado)["text"]

            # Buscamos el producto por id, lo guardamos en la variable producto
            # producto = MainFrame.controlador_producto.buscar_por_id(codigo_producto)

            # Sumamos la cantidad de productos al stock del producto
            # producto.stock += cantidad

            # Actualizamos el producto
            # MainFrame.controlador_producto.actualizar(producto)

            # Eliminamos el item de la tabla
            self.tablaItemsProductos.delete(item_seleccionado)

            # Actualizamos el precio total de la venta
            # self.actualizarPrecioTotal()

            # Si no hay items en la tabla
            if not self.tablaItemsProductos.get_children():
                # Habilitamos la lista de clientes
                self.listaCliente.configure(state="normal")

                # # Borramos el texto de status cliente
                # self.labelStatusCliente.configure(text="")

                # Habilitamos la lista de usuarios
                self.listaUsuario.configure(state="normal")

                # # Borramos el texto de status usuario
                # self.labelStatusUsuario.configure(text="")


        else:
            messagebox.showerror("Error", "Debe seleccionar un producto de la lista", parent=self)

    def cancelarVenta(self):
        if messagebox.askyesno("Cancelar venta", "¿Está seguro que desea cancelar la venta?", parent=self):
            self.destroy()
            #
            # # Eliminamos los items de la tabla
            # self.tablaItemsProductos.delete(*self.tablaItemsProductos.get_children())
            #
            # # Habilitamos la lista de clientes
            # self.listaCliente.configure(state="normal")
            #
            # # Borramos el texto de status cliente
            # self.labelStatusCliente.configure(text="")
            #
            # # Habilitamos la lista de usuarios
            # self.listaUsuario.configure(state="normal")
            #
            # # Borramos el texto de status usuario
            # self.labelStatusUsuario.configure(text="")
            #
            # VentaFrame.cliente = None
            # VentaFrame.usuario = None
            #
            # # Reseteamos la seleccion de la lista de productos
            # self.listaDesplegableProductos.set("")
            #
            # # Reseteamos el label de la lista de productos
            # self.labelListaProductos.configure(text="\n\n\n")
            #
            # # Reseteamos el producto seleccionado
            # VentaFrame.producto = None
            #
            # # Actualizamos el precio total de la venta
            # self.actualizarPrecioTotal()


###############################################################
# Clase para la ventana de gestión de clientes
class ClienteFrame(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.focus_set()
        self.grab_set()

        # Dando tamaño a la ventana
        self.geometry("650x500")

        # Dando título a la ventana
        self.title("Gestión de clientes")

        # Widgets para nombre, apellido, documento, email, descuento
        # width: Ancho del widget
        # anchor: Posición del texto dentro del widget (n, s, e, w, ne, nw, se, sw)
        # padx: Espacio horizontal entre el texto y el borde del widget
        # pady: Espacio vertical entre el texto y el borde del widget

        # Label = etiqueta
        # Entry = campo de texto
        # Button = botón
        # Treeview = tabla
        # Scrollbar = barra de desplazamiento

        self.labelNombre = ctk.CTkLabel(self, text="Nombre: ", width=130, anchor="w", padx=10, pady=10)
        self.labelNombre.grid(row=1, column=0)
        self.entryNombre = ctk.CTkEntry(self, width=450)
        self.entryNombre.grid(row=1, column=1)

        self.labelApellido = ctk.CTkLabel(self, text="Apellido: ", width=130, anchor="w", padx=10, pady=10)
        self.labelApellido.grid(row=2, column=0)
        self.entryApellido = ctk.CTkEntry(self, width=450)
        self.entryApellido.grid(row=2, column=1)

        self.labelDocumento = ctk.CTkLabel(self, text="Documento: ", width=130, anchor="w", padx=10, pady=10)
        self.labelDocumento.grid(row=3, column=0)
        self.entryDocumento = ctk.CTkEntry(self, width=450)
        self.entryDocumento.grid(row=3, column=1)

        self.labelEmail = ctk.CTkLabel(self, text="Email: ", width=130, anchor="w",
                                       padx=10, pady=10)
        self.labelEmail.grid(row=4, column=0)
        self.entryEmail = ctk.CTkEntry(self, width=450)
        self.entryEmail.grid(row=4, column=1)

        self.labelDescuento = ctk.CTkLabel(self, text="Descuento: ", width=130, anchor="w",
                                           padx=10, pady=10)
        self.labelDescuento.grid(row=5, column=0)
        self.entryDescuento = ctk.CTkEntry(self, width=450)
        self.entryDescuento.grid(row=5, column=1)

        # Botón para agregar un cliente
        self.botonAgregar = ctk.CTkButton(self, text="Agregar", width=600, anchor='W', command=self.agregar)
        self.botonAgregar.grid(row=6, column=0, columnspan=2, sticky='WE', padx=10, pady=10)

        # Tabla para mostrar los clientes
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Apellido", "Documento", "Email", "Descuento"))

        # heading: Texto de la cabecera de la columna
        self.tabla.heading("#0", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Documento", text="Documento")
        self.tabla.heading("Email", text="Email")
        self.tabla.heading("Descuento", text="Descuento")

        # column: Nombre de la columna
        self.tabla.column("#0", width=50)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Apellido", width=150)
        self.tabla.column("Documento", width=100, anchor="center")
        self.tabla.column("Email", width=150, anchor="center")
        self.tabla.column("Descuento", width=50, anchor="center")

        # Generamos un Scrollbar para la tabla
        self.tabla.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        # Seteamos opciones del scrollbar
        self.tabla.configure(yscrollcommand=self.tabla.scrollbar.set)
        # Ubicamos el scrollbar
        self.tabla.scrollbar.grid(columnspan=2, sticky="NSE")

        # Ubicamos la tabla
        self.tabla.grid(row=7, column=0, columnspan=2)

        # Botón para eliminar un cliente
        self.botonEliminar = ctk.CTkButton(self, text="Eliminar", width=600, anchor="w", command=self.eliminar)
        self.botonEliminar.grid(row=8, column=0, columnspan=2, sticky='WE', padx=10, pady=10)

        # Etiqueta para mostrar mensajes de status
        self.labelStatus = ctk.CTkLabel(self, text="", width=600, anchor="w", padx=10, pady=10, text_color="red")
        self.labelStatus.grid(row=9, column=0, columnspan=2)

        # Listar los clientes en la tabla
        self.listar_clientes()

        # Eventos de la tabla
        # Evento al hacer click en una fila de la tabla
        # self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

        # Evento al hacer doble click en una fila de la tabla
        self.tabla.bind("<Double-1>", self.seleccionar_doble_click)

    ###########################################################
    # Acciones de los botones de la ventana ClienteFrame
    # Agregar un cliente
    def agregar(self):
        # Valida los campos de texto
        validacion = self.validar_campos()
        if validacion:
            # Obtiene los valores de los campos de texto
            nombre = self.entryNombre.get()
            apellido = self.entryApellido.get()
            documento = self.entryDocumento.get()
            email = self.entryEmail.get()
            descuento = self.entryDescuento.get()

            # Crea un cliente con los valores de los campos de texto
            cliente = Cliente(nombre=nombre, apellido=apellido, documento=documento, email=email, descuento=descuento)

            # Guarda el cliente en la base de datos
            MainFrame.controlador_cliente.guardar(cliente)
            # Muestra un mensaje de status
            self.labelStatus.configure(
                text="Cliente [{} - {}] agregado correctamente".format(cliente.nombre, cliente.apellido),
                text_color="green")
            # Limpia los campos de texto
            self.entryNombre.delete(0, "end")
            self.entryApellido.delete(0, "end")
            self.entryDocumento.delete(0, "end")
            self.entryEmail.delete(0, "end")
            self.entryDescuento.delete(0, "end")

            # Pone el foco en el campo de texto de nombre
            self.entryNombre.focus()

            # Actualiza la tabla
            self.listar_clientes()

    # Listar los clientes en la tabla
    def listar_clientes(self):
        # Elimina todos los registros de la tabla
        self.tabla.delete(*self.tabla.get_children())
        # Obtiene todos los clientes de la base de datos
        clientes: list = MainFrame.controlador_cliente.listar()
        # Agrega los clientes a la tabla
        for cliente in clientes:
            self.tabla.insert("", "end",
                              text=cliente.codigo, values=(
                    cliente.nombre, cliente.apellido, cliente.documento, cliente.email, cliente.descuento))

    # Elimina una fila
    def eliminar(self):
        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "" or self.tabla.focus() is None:
            print("No hay nada seleccionado")
            return
        # Si hay una fila seleccionada, la guarda en la variable indice
        indice = self.tabla.focus()
        # print(indice)
        # Devuelve el valor de la columna 0 (ID)
        id_cliente = str(self.tabla.item(indice, "text"))
        # devuelve el valor de la columna 1 (Nombre)
        nombre = str(self.tabla.item(indice, "values")[0])
        # devuelve el valor de la columna 2 (Apellido)
        apellido = str(self.tabla.item(indice, "values")[1])
        # devuelve el valor de la columna 3 (Documento)
        documento = str(self.tabla.item(indice, "values")[2])
        # devuelve el valor de la columna 4 (Email)
        email = str(self.tabla.item(indice, "values")[3])
        # devuelve el valor de la columna 5 (Descuento)
        descuento = str(self.tabla.item(indice, "values")[4])

        # Elimina el registro de la base de datos y
        # guarda en resultado la cantidad de registros eliminados
        resultado = MainFrame.controlador_cliente.eliminar(id_cliente)

        # Si resultado existe, es porque se eliminó el registro
        # de la base de datos, entonces la borramos de la tabla
        if resultado:
            self.tabla.delete(indice)
            self.labelStatus.configure(text="Cliente Id: {} [{} - {}] eliminado".format(id_cliente, nombre, apellido))

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
            nombre = self.tabla.item(fila, "values")[0]
            apellido = self.tabla.item(fila, "values")[1]
            documento = self.tabla.item(fila, "values")[2]
            email = self.tabla.item(fila, "values")[3]
            descuento = self.tabla.item(fila, "values")[4]

            # Si la columna es 0, es porque se seleccionó el ID, no se hace nada
            # Si la columna es 1, es porque se hizo doble click en la columna nombre
            if columna == 1:
                nombre = simpledialog.askstring("Modificar Nombre", "Nombre:", initialvalue=nombre)
            # Si la columna es 2, es porque se hizo doble click en la columna apellido
            elif columna == 2:
                apellido = simpledialog.askstring("Modificar Apellido", "Apellido:", initialvalue=apellido)
            # Si la columna es 3, es porque se hizo doble click en la columna documento
            elif columna == 3:
                documento = simpledialog.askinteger("Modificar Documento", "Documento:", initialvalue=documento)
            # Si la columna es 4, es porque se hizo doble click en la columna email
            elif columna == 4:
                email = simpledialog.askstring("Email", "Email:", initialvalue=email)
            # Si la columna es 5, es porque se hizo doble click en la columna descuento
            elif columna == 5:
                descuento = simpledialog.askfloat("Descuento", "Descuento:", initialvalue=descuento)

            # Chequeamos que no haya un valor null
            # cuando se modifica el cliente y se aprieta cancelar
            if nombre is None or apellido is None or documento is None or email is None or descuento is None:
                return

            # Crea un cliente con los valores modificados
            cliente = Cliente(codigo=codigo, nombre=nombre, apellido=apellido, documento=documento, email=email,
                              descuento=descuento)

            # Actualiza el cliente en la base de datos
            MainFrame.controlador_cliente.actualizar(cliente)

            # Actualiza la tabla
            self.listar_clientes()

    # Valida los campos de texto
    def validar_campos(self):
        # Valida que el campo de texto Nombre no esté vacío
        if self.entryNombre.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un nombre")
            self.entryNombre.focus()
            return False

        # Valida que el campo de texto Apellido no esté vacío
        if self.entryApellido.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un apellido")
            self.entryApellido.focus()
            return False

        # Valida que el campo de texto Documento no esté vacío
        if self.entryDocumento.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el documento")
            self.entryDocumento.focus()
            return False
        else:
            # Valida que el valor ingresado en Documento sea un número
            try:
                int(self.entryDocumento.get())
            except ValueError:
                messagebox.showwarning("Error", "El documento debe ser un entero")
                self.entryDocumento.focus()
                return False

        # Valida que el campo de texto email no esté vacío
        if self.entryEmail.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el email")
            self.entryEmail.focus()
            return False

        # Valida que el campo de texto descuento no esté vacío
        if self.entryDescuento.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el descuento")
            self.entryDescuento.focus()
            return False
        else:
            # Valida que el valor ingresado en Descuento sea un número
            try:
                float(self.entryDescuento.get())
            except ValueError:
                messagebox.showwarning("Error", "El descuento debe ser un número")
                self.entryDescuento.focus()
                return False

        # Si pasó todas las validaciones, devuelve True
        return True


###############################################################
# Clase para la ventana de gestión de usuarios
class UsuarioFrame(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.focus_set()
        self.grab_set()

        # Dando tamaño a la ventana
        self.geometry("650x500")

        # Dando título a la ventana
        self.title("Gestión de usuarios")

        # Widgets para nombre, apellido, documento, porcentualcomision, comision
        # width: Ancho del widget
        # anchor: Posición del texto dentro del widget (n, s, e, w, ne, nw, se, sw)
        # padx: Espacio horizontal entre el texto y el borde del widget
        # pady: Espacio vertical entre el texto y el borde del widget

        # Label = etiqueta
        # Entry = campo de texto
        # Button = botón
        # Treeview = tabla
        # Scrollbar = barra de desplazamiento

        self.labelNombre = ctk.CTkLabel(self, text="Nombre: ", width=130, anchor="w", padx=10, pady=10)
        self.labelNombre.grid(row=1, column=0)
        self.entryNombre = ctk.CTkEntry(self, width=450)
        self.entryNombre.grid(row=1, column=1)

        self.labelApellido = ctk.CTkLabel(self, text="Apellido: ", width=130, anchor="w", padx=10, pady=10)
        self.labelApellido.grid(row=2, column=0)
        self.entryApellido = ctk.CTkEntry(self, width=450)
        self.entryApellido.grid(row=2, column=1)

        self.labelDocumento = ctk.CTkLabel(self, text="Documento: ", width=130, anchor="w", padx=10, pady=10)
        self.labelDocumento.grid(row=3, column=0)
        self.entryDocumento = ctk.CTkEntry(self, width=450)
        self.entryDocumento.grid(row=3, column=1)

        self.labelPorcentualComision = ctk.CTkLabel(self, text="Porcentaje de comisión: ", width=130, anchor="w",
                                                    padx=10, pady=10)
        self.labelPorcentualComision.grid(row=4, column=0)
        self.entryPorcentualComision = ctk.CTkEntry(self, width=450)
        self.entryPorcentualComision.grid(row=4, column=1)

        # Botón para agregar un usuario
        self.botonAgregar = ctk.CTkButton(self, text="Agregar", width=600, anchor='W', command=self.agregar)
        self.botonAgregar.grid(row=5, column=0, columnspan=2, sticky='WE', padx=10, pady=10)

        # Tabla para mostrar los usuarios
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Apellido", "Documento", "Porcentual Comision", "Comision"))

        # heading: Texto de la cabecera de la columna
        self.tabla.heading("#0", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Documento", text="Documento")
        self.tabla.heading("Porcentual Comision", text="Porcentual Comision")
        self.tabla.heading("Comision", text="Comision")

        # column: Nombre de la columna
        self.tabla.column("#0", width=50)
        self.tabla.column("Nombre", width=200)
        self.tabla.column("Apellido", width=200)
        self.tabla.column("Documento", width=100, anchor="center")
        self.tabla.column("Porcentual Comision", width=50, anchor="center")
        self.tabla.column("Comision", width=50, anchor="center")

        # Generamos un Scrollbar para la tabla
        self.tabla.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        # Seteamos opciones del scrollbar
        self.tabla.configure(yscrollcommand=self.tabla.scrollbar.set)
        # Ubicamos el scrollbar
        self.tabla.scrollbar.grid(columnspan=2, sticky="NSE")

        # Ubicamos la tabla
        self.tabla.grid(row=6, column=0, columnspan=2)

        # Botón para eliminar un usuario
        self.botonEliminar = ctk.CTkButton(self, text="Eliminar", width=600, anchor="w", command=self.eliminar)
        self.botonEliminar.grid(row=7, column=0, columnspan=2, sticky='WE', padx=10, pady=10)

        # Etiqueta para mostrar mensajes de status
        self.labelStatus = ctk.CTkLabel(self, text="", width=600, anchor="w", padx=10, pady=10, text_color="red")
        self.labelStatus.grid(row=8, column=0, columnspan=2)

        # Listar los usuarios en la tabla
        self.listar_usuarios()

        # Eventos de la tabla
        # Evento al hacer click en una fila de la tabla
        # self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

        # Evento al hacer doble click en una fila de la tabla
        self.tabla.bind("<Double-1>", self.seleccionar_doble_click)

    ###########################################################
    # Acciones de los botones de la ventana UsuarioFrame
    # Agregar un usuario
    def agregar(self):
        # Valida los campos de texto
        validacion = self.validar_campos()
        if validacion:
            # Obtiene los valores de los campos de texto
            nombre = self.entryNombre.get()
            apellido = self.entryApellido.get()
            documento = self.entryDocumento.get()
            porcentualcomision = self.entryPorcentualComision.get()

            # Crea un usuario con los valores de los campos de texto
            usuario = Usuario(nombre=nombre, apellido=apellido, documento=documento,
                              porcentualcomision=porcentualcomision)

            # Guarda el usuario en la base de datos
            MainFrame.controlador_usuario.guardar(usuario)
            # Muestra un mensaje de status
            self.labelStatus.configure(
                text="Usuario [{} - {}] agregado correctamente".format(usuario.nombre, usuario.apellido),
                text_color="green")
            # Limpia los campos de texto
            self.entryNombre.delete(0, "end")
            self.entryApellido.delete(0, "end")
            self.entryDocumento.delete(0, "end")
            self.entryPorcentualComision.delete(0, "end")

            # Pone el foco en el campo de texto de nombre
            self.entryNombre.focus()

            # Actualiza la tabla
            self.listar_usuarios()

    # Listar los usuarios en la tabla
    def listar_usuarios(self):
        # Elimina todos los registros de la tabla
        self.tabla.delete(*self.tabla.get_children())
        # Obtiene todos los usuarios de la base de datos
        usuarios: list = MainFrame.controlador_usuario.listar()
        # Agrega los usuarios a la tabla
        for usuario in usuarios:
            self.tabla.insert("", "end",
                              text=usuario.codigo,
                              values=(usuario.nombre, usuario.apellido, usuario.documento, usuario.porcentualcomision,
                                      usuario.comision))

    # Elimina una fila
    def eliminar(self):
        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "" or self.tabla.focus() is None:
            print("No hay nada seleccionado")
            return
        # Si hay una fila seleccionada, la guarda en la variable indice
        indice = self.tabla.focus()
        # print(indice)
        # Devuelve el valor de la columna 0 (ID)
        id_usuario = str(self.tabla.item(indice, "text"))
        # devuelve el valor de la columna 1 (Nombre)
        nombre = str(self.tabla.item(indice, "values")[0])
        # devuelve el valor de la columna 2 (Apellido)
        apellido = str(self.tabla.item(indice, "values")[1])
        # devuelve el valor de la columna 3 (Documento)
        documento = str(self.tabla.item(indice, "values")[2])
        # devuelve el valor de la columna 4 (PorcentualComision)
        porcentualcomision = str(self.tabla.item(indice, "values")[3])
        # devuelve el valor de la columna 5 (Comision)
        comision = str(self.tabla.item(indice, "values")[4])

        # Elimina el registro de la base de datos y
        # guarda en resultado la cantidad de registros eliminados
        resultado = MainFrame.controlador_usuario.eliminar(id_usuario)

        # Si resultado existe, es porque se eliminó el registro
        # de la base de datos, entonces la borramos de la tabla
        if resultado:
            self.tabla.delete(indice)
            self.labelStatus.configure(text="Usuario Id: {} [{} - {}] eliminado".format(id_usuario, nombre, apellido))

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
            nombre = self.tabla.item(fila, "values")[0]
            apellido = self.tabla.item(fila, "values")[1]
            documento = self.tabla.item(fila, "values")[2]
            porcentualComision = self.tabla.item(fila, "values")[3]
            comision = self.tabla.item(fila, "values")[4]

            # Si la columna es 0, es porque se seleccionó el ID, no se hace nada
            # Si la columna es 1, es porque se hizo doble click en la columna nombre
            if columna == 1:
                print("columna 1")
                print("Modificar Nombre")
                nombre = simpledialog.askstring("Modificar Nombre", "Nombre:", initialvalue=nombre)
                print(nombre)
            # Si la columna es 2, es porque se hizo doble click en la columna apellido
            elif columna == 2:
                print("Modificar Apellido")
                apellido = simpledialog.askstring("Modificar Apellido", "Apellido:", initialvalue=apellido)
            # Si la columna es 3, es porque se hizo doble click en la columna documento
            elif columna == 3:
                print("Modificar Documento")
                documento = simpledialog.askinteger("Modificar Documento", "Documento:", initialvalue=documento)
            # Si la columna es 4, es porque se hizo doble click en la columna porcentualComision
            elif columna == 4:
                porcentualComision = simpledialog.askfloat("Modificar Porcentual Comision", "Porcentual Comision:",
                                                           initialvalue=porcentualComision)
            # Si la columna es 5, es porque se hizo doble click en la columna comision, no se hace nada

            # Chequeamos que no haya un valor null
            # cuando se modifica el usuario y se aprieta cancelar
            if nombre is None or apellido is None or documento is None or porcentualComision is None:
                return

            # Crea un usuario con los valores modificados
            usuario = Usuario(codigo=codigo, nombre=nombre, apellido=apellido, documento=documento,
                              porcentualcomision=porcentualComision, comision=comision)

            # Actualiza el usuario en la base de datos
            MainFrame.controlador_usuario.actualizar(usuario)

            # Actualiza la tabla
            self.listar_usuarios()

    # Valida los campos de texto
    def validar_campos(self):
        # Valida que el campo de texto Nombre no esté vacío
        if self.entryNombre.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un nombre")
            self.entryNombre.focus()
            return False

        # Valida que el campo de texto Apellido no esté vacío
        if self.entryApellido.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un apellido")
            self.entryApellido.focus()
            return False

        # Valida que el campo de texto Documento no esté vacío
        if self.entryDocumento.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el documento")
            return False
        else:
            # Valida que el valor ingresado en Documento sea un número
            try:
                int(self.entryDocumento.get())
            except ValueError:
                messagebox.showwarning("Error", "El documento debe ser un entero")
                self.entryDocumento.focus()
                return False

        # Valida que el campo de texto Porcentual Comision no esté vacío
        if self.entryPorcentualComision.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el porcentual comision")
            return False
        else:
            # Valida que el valor ingresado en Porcentual comision sea un número entero
            try:
                float(self.entryPorcentualComision.get())
            except ValueError:
                messagebox.showwarning("Error", "El valor de porcentual comision debe ser un número")
                self.entryPorcentualComision.focus()
                return False
        # Si pasó todas las validaciones, devuelve True
        return True


###############################################################
# Clase principal de la aplicación
class MainFrame(ctk.CTk):
    # Crea la base de datos y las tablas si no existen
    if not ConnectionFactory().chequearDB():
        ConnectionFactory().crear_tablas()

    # Configura la apariencia de la ventana
    ctk.set_appearance_mode("light")

    # Configura el tema de colores
    ctk.set_default_color_theme("blue")

    # Crea el controlador de productos
    controlador_producto = ProductoController()

    # Crea el controlador de usuarios
    controlador_usuario = UsuarioController()

    # Crea el controlador de clientes
    controlador_cliente = ClienteController()

    # Crea el controlador de ventas
    controlador_ventas = VentaController()

    # Crea ventana principal
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configura la ventana
        self.geometry("500x400")

        # Agrega un título a la ventana
        self.title("Sistema de Ventas - Grupo: UTN Bs As")

        # Agrega boton para abrir la ventana de productos
        self.buttonProductos = ctk.CTkButton(self,
                                             text="Gestión de Productos",
                                             command=self.abrir_productos
                                             )
        self.buttonProductos.pack(side="top", padx=20, pady=20)

        # Agrega boton para abrir la ventana de usuarios
        self.buttonUsuarios = ctk.CTkButton(self,
                                            text="Gestión de Usuarios",
                                            command=self.abrir_usuarios
                                            )
        self.buttonUsuarios.pack(side="top", padx=20, pady=20)

        # Agrega boton para abrir la ventana de clientes
        self.buttonClientes = ctk.CTkButton(self,
                                            text="Gestión de Clientes",
                                            command=self.abrir_clientes
                                            )
        self.buttonClientes.pack(side="top", padx=20, pady=20)

        # Agrega boton para abrir la ventana de ventas
        self.buttonVentas = ctk.CTkButton(self,
                                          text="Gestión de Ventas",
                                          command=self.abrir_ventas
                                          )
        self.buttonVentas.pack(side="top", padx=20, pady=20)

        # Setea la ventana de productos como None para controlar si existe
        self.ventanaProductos = None

        # Setea la ventana de usuarios como None para controlar si existe
        self.ventanaUsuarios = None

        # Setea la ventana de clientes como None para controlar si existe
        self.ventanaClientes = None

        # Setea la ventana de ventas como None para controlar si existe
        self.ventanaVentas = None

    # Abre la ventana de productos
    def abrir_productos(self):
        # Si la ventana no existe o fue destruida, la crea
        if self.ventanaProductos is None or not self.ventanaProductos.winfo_exists():
            # Crea la ventana de productos
            self.ventanaProductos = ProductoFrame(self)
        else:
            # Si la ventana existe, la enfoca
            self.ventanaProductos.focus()

    def abrir_usuarios(self):
        # Si la ventana no existe o fue destruida, la crea
        if self.ventanaUsuarios is None or not self.ventanaUsuarios.winfo_exists():
            # Crea la ventana de usuarios
            self.ventanaUsuarios = UsuarioFrame(self)
        else:
            # Si la ventana existe, la enfoca
            self.ventanaUsuarios.focus()

    def abrir_clientes(self):
        # Si la ventana no existe o fue destruida, la crea
        if self.ventanaClientes is None or not self.ventanaClientes.winfo_exists():
            # Crea la ventana de clientes
            self.ventanaClientes = ClienteFrame(self)
        else:
            # Si la ventana existe, la enfoca
            self.ventanaClientes.focus()

    def abrir_ventas(self):
        # Si la ventana no existe o fue destruida, la crea
        if self.ventanaVentas is None or not self.ventanaVentas.winfo_exists():
            # Crea la ventana de ventas
            self.ventanaVentas = VentaFrame(self)
        else:
            # Si la ventana existe, la enfoca
            self.ventanaVentas.deiconify()
            # self.ventanaVentas.focus()


###############################################################
# Crea la ventana principal
app = MainFrame()
