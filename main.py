import tkinter as tk
from view.login import LoginVentana, GestionUsuarios

def iniciar_app():
    ventana = tk.Tk()
    app = LoginVentana(ventana)

    # Mantener la ventana abierta
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_app()

