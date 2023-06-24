from tkinter import ttk

import customtkinter as ctk


# Fuente
# https://customtkinter.tomschimansky.com/documentation/windows/toplevel

class ProductoFrame(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("650x400")
        # Frame contenedor de los widgets
        # self.frame = ctk.CTkFrame(self, width=400, height=300)
        # self.frame.grid(row=0, column=0, pady=20)
        # Widgets para marca, modelo, precio y stock
        self.labelMarca = ctk.CTkLabel(self, text="Marca: ", width=100)
        self.labelMarca.grid(row=1, column=0)
        self.entryMarca = ctk.CTkEntry(self, width=400)
        self.entryMarca.grid(row=1, column=1)

        self.labelModelo = ctk.CTkLabel(self, text="Modelo: ")
        self.labelModelo.grid(row=2, column=0)
        self.entryModelo = ctk.CTkEntry(self, width=400)
        self.entryModelo.grid(row=2, column=1)

        self.labelPrecio = ctk.CTkLabel(self, text="Precio: ")
        self.labelPrecio.grid(row=3, column=0)
        self.entryPrecio = ctk.CTkEntry(self, width=400)
        self.entryPrecio.grid(row=3, column=1)

        self.labelStock = ctk.CTkLabel(self, text="Stock: ")
        self.labelStock.grid(row=4, column=0)
        self.entryStock = ctk.CTkEntry(self, width=400)
        self.entryStock.grid(row=4, column=1)

        self.tabla = ttk.Treeview(self, columns=("Marca", "Modelo", "Precio", "Stock"))
        self.tabla.heading("#0", text="ID")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Stock", text="Stock")
        self.tabla.column("#0", width=50)
        self.tabla.column("Marca", width=200)
        self.tabla.column("Modelo", width=200)
        self.tabla.column("Precio", width=100)
        self.tabla.column("Stock", width=100)

        self.tabla.grid(row=5, column=0, columnspan=3)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.button_1 = ctk.CTkButton(self, text="Abrir Sub Ventana", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ProductoFrame(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


app = App()
app.mainloop()
