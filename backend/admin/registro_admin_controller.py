class RegistroAdminController():
    


    def ejecutar_registro(self):
        # Este método servirá de puente para que el RegistroAdminController capture los datos
        pass

    def al_cerrar(self):
        # Al cerrar, devolvemos la opacidad total (1.0) a la ventana de gestión
        self.ventana_padre.attributes("-alpha", 1.0)
        self.destroy()