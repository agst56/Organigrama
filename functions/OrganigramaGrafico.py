import tkinter as tk
import customtkinter as ctk
from OrganigramaNodo import OrganigramaNodo
from database.access.UpdateData import updateDeps

def validate_text(new_text):

    if len(new_text) <= 10: 
        return True
    else:
        return False
    

class OrganigramaGrafico(ctk.CTk):
    width_nodo=100
    height_nodo=50
    bg_color="black"
    cambios={}
    def __init__(self, organigrama:OrganigramaNodo) -> None:
        super().__init__()
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.validation = self.register(validate_text)
        self.construir(organigrama, None)
        boton_guardar = ctk.CTkButton(self, 100, 50, command=self.guardar)
        boton_guardar.place(x=1000, y=500)

    def guardar(self):
        print("en guardar")
        if bool(self.cambios):
            print("self.cambioss")
            print(self.cambios)
            updateDeps(self.cambios)

    def mover_nodo(self, event, nodo:ctk.CTkLabel, lineaIn, lineasOut, cod_dep):
        
        for lineaOut in lineasOut:
            x1,y1, xHijo, yHijo = self.canvas.coords(lineaOut)
            self.canvas.coords(lineaOut, event.x_root, event.y_root, xHijo, yHijo)    

        if lineaIn!=None:
            xMayor, yMayor, x2, y2 = self.canvas.coords(lineaIn)
            self.canvas.coords(lineaIn, xMayor, yMayor, event.x_root, event.y_root)
        
        nodo.place(x=event.x_root, y=event.y_root)
        if(cod_dep in self.cambios):
            self.cambios[cod_dep]['pos'] = [event.x_root, event.y_root]
        else:
            self.cambios[cod_dep] = {'pos':[event.x_root, event.y_root]}    

    def editar_texto(self, event, label:ctk.CTkLabel, cod_dep):
        label.configure(cursor="ibeam")
        entry = ctk.CTkEntry(self, width=label.winfo_width(), height=label.winfo_height(), fg_color=label.cget("bg_color"),
                         justify="center", validate="key", validatecommand=(self.validation, '%P'))
        entry.place(x=label.winfo_x(), y=label.winfo_y())

        entry.insert(tk.END, label.cget("text"))
        entry.focus_set()    
        entry.bind("<FocusOut>", lambda eventEntry: self.finalizar_edicion(eventEntry, entry, label, cod_dep))
        entry.bind("<Return>", lambda eventEntry: self.finalizar_edicion(eventEntry, entry, label, cod_dep))

    def finalizar_edicion(self, event, entry, label, cod_dep):
        label.configure(cursor="arrow")
        label.configure(text=entry.get())
        if(cod_dep in self.cambios):
            self.cambios[cod_dep]['nom'] = entry.get()
        else:
            self.cambios[cod_dep] = {'nom':entry.get()}           
        entry.destroy()

    def construir(self, orgNodo: OrganigramaNodo, lineaIn):
        nodoLabel = ctk.CTkLabel(self, text=orgNodo.dep.NOM, width=self.width_nodo, height=self.height_nodo, bg_color=self.bg_color)
        nodoLabel.place(x=orgNodo.dep.posX, y=orgNodo.dep.posY)
        if (lineaIn!=None):
            xMayor, yMayor, x2, y2 = self.canvas.coords(lineaIn)
            self.canvas.coords(lineaIn, xMayor, yMayor, orgNodo.dep.posX, orgNodo.dep.posY)
            
        lineasOut = []

        for nodoSuc in orgNodo.listDep:
            lineaOut = self.canvas.create_line(orgNodo.dep.posX, orgNodo.dep.posY, orgNodo.dep.posX, orgNodo.dep.posY, fill="black", width=5)
            lineasOut.append(lineaOut)
            self.construir(nodoSuc, lineaOut)

        nodoLabel.bind("<B1-Motion>",lambda event: self.mover_nodo(event, nodoLabel, lineaIn, lineasOut, orgNodo.dep.COD_DEP))
        nodoLabel.bind("<Double-Button-1>", lambda event: self.editar_texto(event, nodoLabel, orgNodo.dep.COD_DEP))