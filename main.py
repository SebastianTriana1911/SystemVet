import customtkinter as ctk # Customtkinter para usar metodos para diseños con Tkinter
from view.login_view import LoginVentana

def iniciar_app():
    ventana_login = ctk.CTk() 

    # Abre una ventana usando las proporciones de la pantalla
    ventana_login.after(0, lambda: ventana_login.state('zoomed'))
    app = LoginVentana(ventana_login)

    # Mantener la ventana abierta
    ventana_login.mainloop()

if __name__ == "__main__":
    iniciar_app()

