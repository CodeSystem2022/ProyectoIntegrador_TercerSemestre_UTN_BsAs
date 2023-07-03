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


###############################################################
# Clase para la ventana de gestión de ventas
class VentaFrame(ctk.CTkToplevel):
    # Usuario y cliente para generar la venta
    usuario: Usuario = None
    cliente: Cliente = None
    producto: Producto = None

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
                item = VentaItem(venta, producto, cantidad=cantidad)

                listado_items_para_update.append(item)
                # listado_items_para_insert.append(item)

                # Agregamos una lista de valores de venta items al listado para ejecutar el insert
                listado_items_para_insert.append(
                    [item.id_venta, item.id_producto, item.cantidad, item.precio_unitario])

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
