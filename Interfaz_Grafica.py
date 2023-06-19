import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app1 = customtkinter.CTk()  # create CTk window like you do with the Tk window
app1.geometry("400x300")
app1.title("Proyecto Integrador (UTN Bs As @ FRSR)")

app2 = customtkinter.CTk()  # create CTk window like you do with the Tk window
app2.geometry("400x240")

app3 = customtkinter.CTk()  # create CTk window like you do with the Tk window
app3.geometry("400x240")

app4 = customtkinter.CTk()  # create CTk window like you do with the Tk window
app4.geometry("400x240")

label1 = customtkinter.CTkLabel(master=app1, text="Sistema de ventas @ UTN Bs As", font=("Arial", 20))
label1.pack(pady=10, padx=10)

label2 = customtkinter.CTkLabel(master=app1, text="UTN Facultad Regional de San Rafael", font=("Arial", 15))
label2.pack(pady=10, padx=10)


# Funciones de botones en menu principal
def button1_function():
    app2.mainloop()


def button2_function():
    app3.mainloop()


def button3_function():
    app4.mainloop()


# Botones en menu principal
button1 = customtkinter.CTkButton(master=app1, text="Gestion de productos", command=button1_function)
button1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

button2 = customtkinter.CTkButton(master=app1, text="Gestion de vendedores", command=button2_function)
button2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

button3 = customtkinter.CTkButton(master=app1, text="Realizar venta", command=button3_function)
button3.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)


# Funciones de botones en menu Gestion de Productos
def button1_GestionP():
    print("button pressed")


def button2_GestionP():
    print("button pressed")


def button3_GestionP():
    print("button pressed")


# Botones en menu Gestion de productos
button4 = customtkinter.CTkButton(master=app2, text="Opcion 1", command=button1_GestionP)
button4.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

button5 = customtkinter.CTkButton(master=app2, text="Opcion 2", command=button2_GestionP)
button5.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button6 = customtkinter.CTkButton(master=app2, text="Opcion 3", command=button3_GestionP)
button6.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)


# Funciones de botones en menu Gestion de Vendedores
def button1_GestionV():
    print("button pressed")


def button2_GestionV():
    print("button pressed")


def button3_GestionV():
    print("button pressed")


# Botones en menu Gestion de vendedores
button7 = customtkinter.CTkButton(master=app3, text="Opcion 1", command=button1_GestionV)
button7.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

button8 = customtkinter.CTkButton(master=app3, text="Opcion 2", command=button2_GestionV)
button8.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button9 = customtkinter.CTkButton(master=app3, text="Opcion 3", command=button3_GestionV)
button9.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

app1.mainloop()