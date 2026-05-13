import customtkinter as ctk # Customtkinter para usar metodos para diseños con Tkinter
from view.login import LoginVentana

def iniciar_app():
    ventana = ctk.CTk() 
    app = LoginVentana(ventana)

    # Mantener la ventana abierta
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_app()

 