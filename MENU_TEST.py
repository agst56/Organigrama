import customtkinter as ctk
import os
from PIL import Image, ImageTk
from OrganigramaNodo import OrganigramaNodo
from functions import ConstruirOrganigrama
from functions.OrganigramaGrafico import OrganigramaGrafico
from database.access import DataAccess

class FrameBotonOrganigramas(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray10", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="ew")

        for i, org in enumerate(self.values):
            print("cod_org: "+org.COD_ORG)
            radiobutton = ctk.CTkRadioButton(self, text=org.ORG, value=org.ORG, variable=self.variable, command=lambda org=org:graficarOrganigrama(org.COD_ORG))
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 20), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)
        

    def spawn_opciones(self):
        ...



def Agregar_Organigramas():
    ventana_organigrama = ctk.CTkInputDialog(text="Ingrese el nombre de su Organigrama", title=" ORGANIPLANNER ")
    nom = ventana_organigrama.get_input()
    if nom=="" or nom==None:
        return
    cod_org = ConstruirOrganigrama.crearOrganigrama(nom)
    graficarOrganigrama(cod_org)


def graficarOrganigrama(cod_org:str):
    print("graficar: "+cod_org)
    organigrama = ConstruirOrganigrama.construir(cod_org)
    app = OrganigramaGrafico(organigrama)
    app.mainloop()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ORGANIPLANNER - Menu")
        self.geometry("800x650+250+20")  # 800x450
        self.iconbitmap('logo3.ico')
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Imagenes en Version Light y Dark
        self.usuario_image = ctk.CTkImage(light_image=Image.open(os.path.join("images\\usuario_light.png")),
                                          dark_image=Image.open(os.path.join("images\\usuario_dark.png")))
        self.name_image = ctk.CTkImage(light_image=Image.open(os.path.join("images\\nombre_light.png")),
                                       size=(300, 150),
                                       dark_image=Image.open(os.path.join("images\\nombre_dark.png")))
        self.crear_image = ctk.CTkImage(light_image=Image.open(os.path.join("images\\mas_light.png")),
                                        dark_image=Image.open(os.path.join("images\\mas_dark.png")),
                                        size=(20, 20))

        # creacion del frame para navegar (usuario, apariencia y crear)
        self.navigation_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=2)

        # Estaría mejor guardar el frame del usuario en una clase, pero no tengo idea de como hacer eso
        # usuario = self.registrar_usuario() <- Crear funcion para ingresar un usuario a la BdD
        # y mostrar su user como texto en la ventana del menu. (esa ventanita donde dice usuario)
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text=" Usuario ",
                                                   image=self.usuario_image,
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Boton de Crear Usuario
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=1, height=40, border_spacing=10,
                                         text=" Crear Organigrama ",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.crear_image, anchor="w", command=Agregar_Organigramas)
        self.home_button.grid(row=1, column=0, sticky="ew")

        # Menu de Light y Dark
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # creacion del frame para el logo (donde están el icono y nombre de la aplicacion
        self.home_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.name_image = ctk.CTkLabel(self.home_frame, text="", image=self.name_image)
        self.name_image.grid(row=1, column=0, padx=160, pady=(20, 0), sticky="ew")

        # creacion del frame radiobutton (donde están los archivos)
        # al activar un boton tienen que poppear las funciones a realizar
        self.botones_frame = FrameBotonOrganigramas(self, " ARCHIVOS RECIENTES ",
                                                    values=DataAccess.retrieveOrganigramas())
        self.botones_frame.grid(row=1, column=1, padx=(90, 100), pady=(20, 30), sticky="nsew")

        # creacion el segundo frame
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Creacion del tercer frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # seleccion de un frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # definir el color del boton seleccionado
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # mostrar el boton elegido
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def login(self):
        ...

    def cargar_organigrama(self):
        ...


if __name__ == "__main__":
    app = App()
    app.mainloop()

