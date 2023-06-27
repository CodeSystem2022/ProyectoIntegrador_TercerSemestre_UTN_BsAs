from controller.ClienteController import ClienteController
from controller.UsuarioController import UsuarioController
from controller.VentaController import VentaController
from view.MainFrame import app

if __name__ == '__main__':
    # TODO: borrar los controladores cuando se vayan implementando
    # Crea conexiones a los controller's de las tablas
    controlador_usuario = UsuarioController()
    controlador_cliente = ClienteController()
    controlador_ventas = VentaController()

    # Llama la interfaz gráfica
    app.mainloop()
