import tkinter
from tkinter import ttk, messagebox, simpledialog

import customtkinter as ctk

from controller.ClienteController import ClienteController
from controller.ProductoController import ProductoController
from controller.UsuarioController import UsuarioController
from controller.VentaController import VentaController
from controller.VentaItemController import VentaItemController
from factory.ConnectionFactory import ConnectionFactory
from modelo.Cliente import Cliente
from modelo.Producto import Producto
from modelo.Usuario import Usuario
from modelo.Venta import Venta
from modelo.VentaItem import VentaItem


# Fuente
# https://customtkinter.tomschimansky.com/documentation/windows/toplevel

##############################################################
# Clase para la ventana de listado de ventas
class ListadoVentasFrame(ctk.CTkToplevel):
    venta_seleccionada: Venta = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus_set()
        self.grab_set()
        # Dando tamaño a la ventana
        self.geometry("650x500")

        # Dando título a la ventana
        self.title("Listado de ventas")

        # Creamos un label para mostrar el listado
        self.labelListadoVentas = ctk.CTkLabel(self, text="Listado de ventas", text_color="#03396c",
                                               font=("Helvetica", 16), width=650)
        self.labelListadoVentas.grid(column=0, row=0, sticky="we", pady=10, columnspan=4)

        # Creamos un label para mostrar el usuario
        self.labelUsuario = ctk.CTkLabel(self, text="Usuario", text_color="#03396c", font=("Helvetica", 14),
                                         anchor="center", width=300)
        self.labelUsuario.grid(column=0, row=5, sticky="nswe")

        # Creamos un label para mostrar detalle de usuario
        self.labelDetalleUsuario = ctk.CTkLabel(self, text="\n\n\n\n", font=("Helvetica", 10), anchor="center",
                                                width=300)
        self.labelDetalleUsuario.grid(column=0, row=6, sticky="nswe", pady=5)

        # Creamos un label para mostrar el cliente
        self.labelCliente = ctk.CTkLabel(self, text="Cliente", text_color="#03396c", font=("Helvetica", 14),
                                         anchor="center", width=300)
        self.labelCliente.grid(column=2, row=5, sticky="nswe")

        # Creamos un label para mostrar detalle de cliente
        self.labelDetalleCliente = ctk.CTkLabel(self, text="\n\n\n\n", font=("Helvetica", 10), anchor="center",
                                                width=300)
        self.labelDetalleCliente.grid(column=2, row=6, sticky="nswe", pady=5)

        # Creamos un listbox para mostrar las ventas
        self.listaVentas = tkinter.Listbox(self, height=4, width=5)

        # Agregamos un scrollbar a la lista
        self.scrollbarListadoVentas = tkinter.Scrollbar(self, orient="vertical", borderwidth=0)
        self.listaVentas.config(yscrollcommand=self.scrollbarListadoVentas.set)
        self.scrollbarListadoVentas.config(command=self.listaVentas.yview)
        self.scrollbarListadoVentas.grid(sticky="NSE", column=3, row=1, rowspan=2)

        # Insertamos los clientes en la lista, contador_cliente es para el indice de la lista
        contador_ventas = 0
        for venta in MainFrame.controlador_ventas.listar():
            contador_ventas += 1
            self.listaVentas.insert(contador_ventas,
                                    '({}) [{}] -> $ {}'.format(venta.codigo, venta.fecha_alta, venta.importe))

        # Agregamos un evento para cuando se seleccione un cliente
        self.listaVentas.bind("<<ListboxSelect>>", self.OnSelectVenta)

        # Insertamos la lista en el frame
        self.listaVentas.grid(row=1, column=0, columnspan=4, sticky="we")

        # Creamos una lista para mostrar los productos de la venta
        self.listaProductos = ttk.Treeview(self, columns=("Marca", "Modelo", "Precio", "Cantidad", "Subtotal"))

        # heading: Texto de la cabecera de la columna
        self.listaProductos.heading("#0", text="ID")
        self.listaProductos.heading("Marca", text="Marca")
        self.listaProductos.heading("Modelo", text="Modelo")
        self.listaProductos.heading("Precio", text="Precio Unitario")
        self.listaProductos.heading("Cantidad", text="Cantidad")
        self.listaProductos.heading("Subtotal", text="Subtotal")

        # column: Nombre de la columna
        self.listaProductos.column("#0", width=55)
        self.listaProductos.column("Marca", width=150)
        self.listaProductos.column("Modelo", width=150)
        self.listaProductos.column("Precio", width=90, anchor="center")
        self.listaProductos.column("Cantidad", width=55, anchor="center")
        self.listaProductos.column("Subtotal", width=90, anchor="center")

        # Agregamos un scrollbar a la lista
        self.scrollbarListaProductos = tkinter.Scrollbar(self, orient="vertical", borderwidth=0)
        self.listaProductos.config(yscrollcommand=self.scrollbarListaProductos.set)
        self.scrollbarListaProductos.config(command=self.listaProductos.yview)
        self.scrollbarListaProductos.grid(sticky="NSE", column=3, row=7, rowspan=2)
        self.listaProductos.grid(row=7, column=0, columnspan=4, sticky="wes")

    def OnSelectVenta(self, event):
        # Borramos la lista de productos
        self.listaProductos.delete(*self.listaProductos.get_children())

        seleccion = self.listaVentas.curselection()
        if seleccion:
            # Obtenemos el índice del elemento seleccionado
            index = self.listaVentas.curselection()[0]
            # Obtenemos el texto del elemento seleccionado
            venta_elegida = self.listaVentas.get(index)
            # Separamos el codigo
            codigo_venta = venta_elegida.split(")")[0].replace("(", "")
            # Buscamos la venta por id, lo guardamos en la variable venta
            listado_venta_item: list = MainFrame.controlador_ventas_items.buscar_por_id_venta(codigo_venta)

            for venta_item in listado_venta_item:
                producto = MainFrame.controlador_producto.buscar_por_id(venta_item.id_producto)
                ListadoVentasFrame.venta_seleccionada = MainFrame.controlador_ventas.buscar_por_id(venta_item.id_venta)
                cliente = MainFrame.controlador_cliente.buscar_por_id(ListadoVentasFrame.venta_seleccionada.id_cliente)
                usuario = MainFrame.controlador_usuario.buscar_por_id(ListadoVentasFrame.venta_seleccionada.id_usuario)

                self.labelDetalleUsuario.configure(
                    text="Nombre y Apellido: {} {}\n Documento: {}\n Porcentual de Comisión: %{} \nComisión Acumulada: ${}".format(
                        usuario.nombre, usuario.apellido, usuario.documento, int(usuario.porcentualcomision),
                        usuario.comision))
                self.labelDetalleCliente.configure(
                    text="Nombre y Apellido: {} {}\n Documento: {}\n Email: {} \nDescuento: %{}".format(
                        cliente.nombre, cliente.apellido, cliente.documento, cliente.email,
                        int(cliente.descuento)))
                self.listaProductos.insert("", tkinter.END, text=producto.codigo, values=(
                    producto.marca, producto.modelo, venta_item.precio_unitario, venta_item.cantidad,
                    venta_item.cantidad * venta_item.precio_unitario))


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
                        text="No se puede eliminar el producto [{} - {}] porque tiene ventas asociadas"
                        .format(marca, modelo),
                        text_color="red")
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


###############################################################
# Clase para la ventana de gestión de ventas
class VentaFrame(ctk.CTkToplevel):
    # Usuario y cliente para generar la venta
    usuario: Usuario = None
    cliente: Cliente = None
    producto: Producto = None
    venta: Venta = None

    # TODO: se borra?
    producto_pedido: Producto = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: se borra ?
        # MainFrame.controlador_ventas.id_ultima_venta()

        # Dando focus a la ventana
        self.focus_set()
        self.grab_set()

        # Dando tamaño a la ventana
        self.geometry("740x550")
        # Dando título a la ventana
        self.title("Realizar una venta")
        # Cambiamos el color de la ventana
        self.config(bg="#b3cde0")
        self.config(background="#b3cde0")

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
        self.tablaItemsProductos.heading("Precio", text="Precio Unitario")
        self.tablaItemsProductos.heading("Cantidad", text="Cantidad")
        self.tablaItemsProductos.heading("PrecioFinal", text="Precio Final")

        # column: Nombre de la columna
        self.tablaItemsProductos.column("#0", width=55)
        self.tablaItemsProductos.column("Marca", width=200)
        self.tablaItemsProductos.column("Modelo", width=200)
        self.tablaItemsProductos.column("Precio", width=90, anchor="center")
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
        self.labelTotalVenta = ctk.CTkLabel(self, text="Monto total: $ 0", anchor="center",
                                            text_color="#011f4b",
                                            bg_color="#b3cde0")
        self.labelTotalVenta.grid(row=7, column=1)

        # Colocamos un separador
        self.separador3 = ttk.Separator(self, orient="horizontal")
        self.separador3.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=15)

        # Colocamos un boton para cancelar la venta
        self.botonCancelarVenta = ctk.CTkButton(self, text="Cancelar venta", command=self.cancelarVenta)
        self.botonCancelarVenta.grid(row=9, column=0)

        # Colocamos un boton para finalizar la venta
        self.botonFinalizarVenta = ctk.CTkButton(self, text="Finalizar venta", command=self.finalizarVenta)
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
            texto = 'Cliente: {} {} - Descuento: %{}'.format(VentaFrame.cliente.nombre, VentaFrame.cliente.apellido,
                                                             VentaFrame.cliente.descuento)
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
            texto = 'Usuario: {} {} - Comisión: %{}'.format(VentaFrame.usuario.nombre, VentaFrame.usuario.apellido,
                                                            VentaFrame.usuario.porcentualcomision)
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
                    self.actualizarPrecioTotal()
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

            # Reseteamos el listado
            self.listaDesplegableProductos.set("")

            # Actualizamos el precio total de la venta
            self.actualizarPrecioTotal()

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

    def actualizarPrecioTotal(self):
        # Obtenemos los items de la tabla
        items = self.tablaItemsProductos.get_children()
        descuento = float(VentaFrame.cliente.descuento)
        print("Descuento: ", descuento)
        # Inicializamos el precio total
        precio_total = 0

        # Recorremos los items de la tabla
        for item in items:
            # Obtenemos el precio total del producto
            precio_total += float(self.tablaItemsProductos.item(item)["values"][4])
        precio_final = precio_total - precio_total * descuento / 100
        # Actualizamos el label de precio total de la venta y lo mostramos tambien con descuento
        self.labelTotalVenta.configure(text="Monto total: $ " + str(precio_total) + " - Descuento: $ " + str(
            precio_total * descuento / 100) + " = $ " + str(precio_final))

        # self.labelTotalVenta.configure(text="Monto total: $ " + str(precio_total))

    def finalizarVenta(self):
        # Creamos un with para manejar la transaccion

        listado_items_para_insert = []
        listado_items_para_update = []

        # if VentaFrame.producto is None:
        #     messagebox.showerror("Error", "Debe seleccionar un producto", parent=self)
        #     return
        if VentaFrame.cliente is None:
            messagebox.showerror("Error", "Debe seleccionar un cliente", parent=self)
            return
        if VentaFrame.usuario is None:
            messagebox.showerror("Error", "Debe seleccionar un usuario", parent=self)
            return
        # Verifica que existan items en la tabla
        if not self.tablaItemsProductos.get_children():
            messagebox.showerror("Error", "Debe agregar al menos un producto", parent=self)
            return

        try:
            # Creamos el objeto venta
            venta: Venta = Venta(cliente=VentaFrame.cliente, usuario=VentaFrame.usuario)

            MainFrame.controlador_ventas.guardar(venta)
            venta.codigo = MainFrame.controlador_ventas.id_ultima_venta()
            print("Id ultima venta:")
            print(MainFrame.controlador_ventas.id_ultima_venta())

            # recorremos los items de la tabla para crear una lista de venta items
            for item in self.tablaItemsProductos.get_children():
                # Obtenemos el codigo del producto
                codigo_producto = self.tablaItemsProductos.item(item)["text"]
                producto: Producto = MainFrame.controlador_producto.buscar_por_id(codigo_producto)

                # Obtenemos la cantidad del producto
                cantidad = int(self.tablaItemsProductos.item(item)["values"][3])

                # Obtenemos el precio del producto
                precio = float(self.tablaItemsProductos.item(item)["values"][2])

                # Creamos el objeto venta item
                item = VentaItem(id_venta=venta.codigo, id_producto=producto.codigo, cantidad=cantidad,
                                 producto=producto,
                                 precio_unitario=producto.precio)

                listado_items_para_update.append(item)
                # listado_items_para_insert.append(item)

                # Agregamos una lista de valores de venta items al listado para ejecutar el insert
                listado_items_para_insert.append(
                    [item.id_venta, item.id_producto, item.cantidad, item.precio_unitario])
                print("Item: ", item)

            print("Listado items para insert: ", listado_items_para_insert)
            MainFrame.controlador_ventas_items.guardar_varios(listado_items_para_insert)
            monto_final = 0
            # Recorremos la lista de items para actualizar el stock
            for item in listado_items_para_update:
                # monto final de la venta
                monto_final += float(item.cantidad) * float(item.precio_unitario)
                # calculamos el nuevo stock
                nuevo_stock = item.producto.stock - item.cantidad
                # actualizamos el stock del producto
                item.producto.stock = nuevo_stock
                # actualizamos el producto en la base de datos
                MainFrame.controlador_producto.actualizar(item.producto)

            # Actualizamos la comision del usuario sobre el monto final
            VentaFrame.usuario.comision += monto_final * float(VentaFrame.usuario.porcentualcomision) / 100
            # Actualizamos el usuario en la base de datos
            MainFrame.controlador_usuario.actualizar(VentaFrame.usuario)
            venta.importe = monto_final
            venta.comision = float(monto_final) * float(VentaFrame.usuario.porcentualcomision) / 100
            venta.descuento = float(monto_final) * float(VentaFrame.cliente.descuento) / 100
            MainFrame.controlador_ventas.actualizar(venta)
            messagebox.showinfo("Venta", "Venta realizada con éxito", parent=self)
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", "No se pudo guardar la venta", parent=self)
            print(e)
            return

            # Creamos el objeto venta item

            # Agregamos el objeto venta item a la lista de venta items
            # VentaFrame.ventaItem.append(venta_item)

        # Actualiza el producto en la base de datos
        # MainFrame.controlador_producto.actualizar(producto)

        # Actualiza la tabla
        # self.listar_productos()


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
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Apellido", "Documento", "Email", "Descuento"), height=8)

        # heading: Texto de la cabecera de la columna
        self.tabla.heading("#0", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Documento", text="Documento")
        self.tabla.heading("Email", text="Email")
        self.tabla.heading("Descuento", text="% Descuento")

        # column: Nombre de la columna
        self.tabla.column("#0", width=50)
        self.tabla.column("Nombre", width=130)
        self.tabla.column("Apellido", width=130)
        self.tabla.column("Documento", width=100)
        self.tabla.column("Email", width=130)
        self.tabla.column("Descuento", width=100, anchor="center")

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
            textoDescuento = "% {}".format(int(cliente.descuento))
            self.tabla.insert("", "end",
                              text=cliente.codigo, values=(
                    cliente.nombre, cliente.apellido, cliente.documento, cliente.email, textoDescuento))

    # Elimina una fila
    def eliminar(self):
        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "" or self.tabla.focus() is None:
            print("No hay nada seleccionado")
            return

        if messagebox.askyesno("Eliminar", "¿Está seguro que desea eliminar el cliente seleccionado?", parent=self):
            # Si hay una fila seleccionada, la guarda en la variable indice
            indice = self.tabla.focus()
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

            try:
                int(resultado)
                self.tabla.delete(indice)
                self.labelStatus.configure(
                    text="Cliente Id: {} [{} - {}] eliminado".format(id_cliente, nombre, apellido))
            except ValueError as e:
                # Si resultado devuelve un mensaje de error por llave foránea
                if "foreign key" in resultado:
                    # Muestra un mensaje de error
                    self.labelStatus.configure(
                        text="No se puede eliminar el cliente [{} - {}] porque tiene ventas asociadas".format(nombre,
                                                                                                              apellido),
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
            nombre = self.tabla.item(fila, "values")[0]
            apellido = self.tabla.item(fila, "values")[1]
            documento = self.tabla.item(fila, "values")[2]
            email = self.tabla.item(fila, "values")[3]
            # Removemos el simbolo de porcentaje del descuento
            descuento = int(self.tabla.item(fila, "values")[4].replace("%", ""))

            # Si la columna es 0, es porque se seleccionó el ID, no se hace nada
            # Si la columna es 1, es porque se hizo doble click en la columna nombre
            if columna == 1:
                nombre = simpledialog.askstring("Modificar Nombre", "Nombre:", initialvalue=nombre, parent=self)
            # Si la columna es 2, es porque se hizo doble click en la columna apellido
            elif columna == 2:
                apellido = simpledialog.askstring("Modificar Apellido", "Apellido:", initialvalue=apellido, parent=self)
            # Si la columna es 3, es porque se hizo doble click en la columna documento
            elif columna == 3:
                documento = simpledialog.askinteger("Modificar Documento", "Documento:", initialvalue=documento,
                                                    parent=self)
            # Si la columna es 4, es porque se hizo doble click en la columna email
            elif columna == 4:
                email = simpledialog.askstring("Email", "Email:", initialvalue=email, parent=self)
            # Si la columna es 5, es porque se hizo doble click en la columna descuento
            elif columna == 5:
                descuento = simpledialog.askinteger("Descuento", "Descuento:", initialvalue=descuento, parent=self)

            # Chequeamos que no haya un valor null
            # cuando se modifica el cliente y se aprieta cancelar
            if nombre is None or apellido is None or documento is None or email is None or descuento is None:
                return
            # Chequeamos que el descuento sea un valor entre 0 y 100

            # BORRAR EL ELSE ?
            else:
                if descuento > 0 and descuento < 100:
                    pass
                else:
                    messagebox.showwarning("Error", "Debe ingresar un descuento entre 0 y 100", parent=self)
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
            messagebox.showwarning("Error", "Debe ingresar un nombre", parent=self)
            self.entryNombre.focus()
            return False

        # Valida que el campo de texto Apellido no esté vacío
        if self.entryApellido.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un apellido", parent=self)
            self.entryApellido.focus()
            return False

        # Valida que el campo de texto Documento no esté vacío
        if self.entryDocumento.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el documento", parent=self)
            self.entryDocumento.focus()
            return False
        else:
            # Valida que el valor ingresado en Documento sea un número
            try:
                float(self.entryDocumento.get())
            except ValueError:
                messagebox.showwarning("Error", "El documento debe ser un número", parent=self)
                self.entryDocumento.focus()
                return False

        # Valida que el campo de texto email no esté vacío
        if self.entryEmail.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el email", parent=self)
            self.entryEmail.focus()
            return False

        # Valida que el campo de texto descuento no esté vacío
        if self.entryDescuento.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el porcentaje de descuento", parent=self)
            self.entryDescuento.focus()
            return False
        else:
            # Valida que el valor ingresado en Descuento sea un número
            try:
                descuento_ingresado = int(self.entryDescuento.get())
            except ValueError:
                messagebox.showwarning("Error", "El descuento debe ser un número", parent=self)
                self.entryDescuento.focus()
                return False
            if descuento_ingresado > 0 and descuento_ingresado < 100:
                pass
            else:
                messagebox.showwarning("Error", "El descuento debe ser un número entre 0 y 100", parent=self)
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

        self.labelNombre = ctk.CTkLabel(self, text="Nombre: ", width=160, anchor="w", padx=10, pady=10)
        self.labelNombre.grid(row=1, column=0)
        self.entryNombre = ctk.CTkEntry(self, width=450)
        self.entryNombre.grid(row=1, column=1)

        self.labelApellido = ctk.CTkLabel(self, text="Apellido: ", width=160, anchor="w", padx=10, pady=10)
        self.labelApellido.grid(row=2, column=0)
        self.entryApellido = ctk.CTkEntry(self, width=450)
        self.entryApellido.grid(row=2, column=1)

        self.labelDocumento = ctk.CTkLabel(self, text="Documento: ", width=160, anchor="w", padx=10, pady=10)
        self.labelDocumento.grid(row=3, column=0)
        self.entryDocumento = ctk.CTkEntry(self, width=450)
        self.entryDocumento.grid(row=3, column=1)

        self.labelPorcentualComision = ctk.CTkLabel(self, text="Porcentaje de comisión: ", width=160, anchor="w",
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
        self.tabla.heading("Porcentual Comision", text="% Comision")
        self.tabla.heading("Comision", text="$ Comision")

        # column: Nombre de la columna
        self.tabla.column("#0", width=50)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Apellido", width=150)
        self.tabla.column("Documento", width=100)
        self.tabla.column("Porcentual Comision", width=100)
        self.tabla.column("Comision", width=100, anchor="center")

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
            textoPorcentualComision = "% {}".format(int(usuario.porcentualcomision))
            textoComision = "$ {}".format(usuario.comision)
            self.tabla.insert("", "end",
                              text=usuario.codigo,
                              values=(
                                  usuario.nombre, usuario.apellido, usuario.documento, textoPorcentualComision,
                                  textoComision))

    # Elimina una fila
    def eliminar(self):
        # Si no hay nada seleccionado, no hace nada
        if self.tabla.focus() == "" or self.tabla.focus() is None:
            print("No hay nada seleccionado")
            return
        if messagebox.askyesno("Eliminar", "¿Está seguro que desea eliminar el usuario seleccionado?", parent=self):
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
            try:
                int(resultado)
                self.tabla.delete(indice)
                self.labelStatus.configure(
                    text="Usuario Id: {} [{} - {}] eliminado".format(id_usuario, nombre, apellido))
            except ValueError as e:
                # Si resultado devuelve un mensaje de error por llave foránea
                if "foreign key" in resultado:
                    # Muestra un mensaje de error
                    self.labelStatus.configure(
                        text="No se puede eliminar el cliente [{} - {}] "
                             "porque tiene ventas asociadas".format(nombre, apellido),
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
            nombre = self.tabla.item(fila, "values")[0]
            apellido = self.tabla.item(fila, "values")[1]
            documento = int(self.tabla.item(fila, "values")[2])
            # removemos el % del porcentual de comision
            porcentualComision = int(self.tabla.item(fila, "values")[3].replace("%", ""))

            # removemos el $ de la comision

            comision = self.tabla.item(fila, "values")[4].replace("$", "")

            # Si la columna es 0, es porque se seleccionó el ID, no se hace nada
            # Si la columna es 1, es porque se hizo doble click en la columna nombre
            if columna == 1:
                nombre = simpledialog.askstring("Modificar Nombre", "Nombre:", initialvalue=nombre, parent=self)
            # Si la columna es 2, es porque se hizo doble click en la columna apellido
            elif columna == 2:
                apellido = simpledialog.askstring("Modificar Apellido", "Apellido:", initialvalue=apellido, parent=self)
            # Si la columna es 3, es porque se hizo doble click en la columna documento
            elif columna == 3:
                documento = simpledialog.askinteger("Modificar Documento", "Documento:", initialvalue=documento,
                                                    parent=self)
            # Si la columna es 4, es porque se hizo doble click en la columna porcentualComision
            elif columna == 4:
                porcentualComision = simpledialog.askinteger("Modificar Porcentual Comisión", "Porcentual Comisión:",
                                                             initialvalue=porcentualComision, parent=self)
            # Si la columna es 5, es porque se hizo doble click en la columna comision, no se hace nada

            # Chequeamos que no haya un valor null
            # cuando se modifica el usuario y se aprieta cancelar
            if nombre is None or apellido is None or documento is None or porcentualComision is None:
                return
            # chequeamos que el porcentual de comision sea un valor entre 0 y 100
            # ACAAAAAA
            if porcentualComision < 0 or porcentualComision > 100:
                messagebox.showwarning("Error", "El porcentual de comisión debe ser un valor entre 0 y 100",
                                       parent=self)
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
            messagebox.showwarning("Error", "Debe ingresar un nombre", parent=self)
            self.entryNombre.focus()
            return False

        # Valida que el campo de texto Apellido no esté vacío
        if self.entryApellido.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un apellido", parent=self)
            self.entryApellido.focus()
            return False

        # Valida que el campo de texto Documento no esté vacío
        if self.entryDocumento.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el documento", parent=self)
            self.entryDocumento.focus()
            return False
        else:
            # Valida que el valor ingresado en Documento sea un número
            try:
                float(self.entryDocumento.get())
            except ValueError:
                messagebox.showwarning("Error", "El documento debe ser un número", parent=self)
                self.entryDocumento.focus()
                return False

        # Valida que el campo de texto Porcentual Comision no esté vacío
        if self.entryPorcentualComision.get() == "":
            messagebox.showwarning("Error", "Debe ingresar un valor para el porcentual comisión", parent=self)
            self.entryPorcentualComision.focus()
            return False
        else:
            # Valida que el valor ingresado en Porcentual comision sea un número entero
            try:
                comision_ingresada: int = int(self.entryPorcentualComision.get())
            except ValueError:
                messagebox.showwarning("Error", "El valor de porcentual comisión debe ser un número", parent=self)
                self.entryPorcentualComision.focus()
                return False
            # Chequeamos que el valor ingresado sea mayor a 0 y menor a 100
            print(comision_ingresada)
            if comision_ingresada > 0 and comision_ingresada < 100:
                print("entro")
                print(comision_ingresada)
                pass
            else:
                messagebox.showwarning("Error", "El valor de porcentual comisión debe ser mayor a 0 y menor a 100",
                                       parent=self)
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

    # Crea el controlador de items de venta
    controlador_ventas_items = VentaItemController()

    # Crea ventana principal
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configura la ventana
        self.geometry("500x500")

        # Agrega un título a la ventana
        self.title("Sistema de Ventas - Grupo: UTN Bs As")

        # Agrega boton para abrir la ventana de productos
        self.buttonProductos = ctk.CTkButton(self,
                                             text="Gestión de Productos",
                                             command=self.abrir_productos,
                                             height=90
                                             )
        self.buttonProductos.pack(anchor="center", padx=5, pady=5, fill="both")

        # Agrega boton para abrir la ventana de usuarios
        self.buttonUsuarios = ctk.CTkButton(self,
                                            text="Gestión de Usuarios",
                                            command=self.abrir_usuarios,
                                            height=90
                                            )
        self.buttonUsuarios.pack(anchor="center", padx=5, pady=5, fill="both")

        # Agrega boton para abrir la ventana de clientes
        self.buttonClientes = ctk.CTkButton(self,
                                            text="Gestión de Clientes",
                                            command=self.abrir_clientes,
                                            height=90
                                            )
        self.buttonClientes.pack(anchor="center", padx=5, pady=5, fill="both")

        # Agrega boton para abrir la ventana de ventas
        self.buttonVentas = ctk.CTkButton(self,
                                          text="Realizar una Venta",
                                          command=self.abrir_ventas,
                                          height=90
                                          )
        self.buttonVentas.pack(anchor="center", padx=5, pady=5, fill="both")

        self.buttonListadoVentas = ctk.CTkButton(self,
                                                 text="Listado de Ventas",
                                                 command=self.abrir_listado_ventas,
                                                 height=90
                                                 )
        self.buttonListadoVentas.pack(anchor="center", padx=5, pady=5, fill="both")

        # Setea la ventana de productos como None para controlar si existe
        self.ventanaProductos = None

        # Setea la ventana de usuarios como None para controlar si existe
        self.ventanaUsuarios = None

        # Setea la ventana de clientes como None para controlar si existe
        self.ventanaClientes = None

        # Setea la ventana de ventas como None para controlar si existe
        self.ventanaVentas = None

        # Setea la ventana de listado de ventas como None para controlar si existe
        self.ventanaListadoVentas = None

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

    def abrir_listado_ventas(self):
        # chequeamos que existan ventas realizadas
        if self.controlador_ventas.listar():
            print("Existen ventas realizadas")
        else:
            messagebox.showwarning("Error", "No existen ventas realizadas", parent=self)
            print("No existen ventas realizadas")
            return

        # Si la ventana no existe o fue destruida, la crea
        if self.ventanaListadoVentas is None or not self.ventanaListadoVentas.winfo_exists():
            # Crea la ventana de ventas
            self.ventanaListadoVentas = ListadoVentasFrame(self)
        else:
            # Si la ventana existe, la enfoca
            self.ventanaListadoVentas.deiconify()
            # self.ventanaVentas.focus()


###############################################################
# Crea la ventana principal
app = MainFrame()
