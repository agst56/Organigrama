import tkinter as tk
import customtkinter as ctk
from OrganigramaNodo import OrganigramaNodo
from database.access.UpdateData import updateDeps
from database.access.UpdateData import updateDepDep
from database.access.UpdateData import insertDepDep
from database.access.UpdateData import insertDependencia
from database.access.UpdateData import eliminarDep
from database.entities.Dependencia import Dependencia
from functions.ConstruirOrganigrama import forId
from random import choice

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
    depdep={}
    dep_nuevos = []
    depdep_nuevos={}
    dep_deleted = []
    nodosLinea = {"nodo_ant": None, "nodo_suc":None}
    

    def __init__(self, organigrama:OrganigramaNodo) -> None:
        super().__init__()
        self.organigrama = organigrama
        self.iniciar()

    def iniciar(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.nodosLinea = {"nodo_ant": None, "nodo_suc":None}
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.validation = self.register(validate_text)
        self.construir(self.organigrama)
        boton_guardar = ctk.CTkButton(self, 100, 50, text="Guardar", command=self.guardar)
        boton_guardar.place(x=1000, y=500)

    def guardar(self):
        print("en guardar")
        if bool(self.cambios):
            updateDeps(self.cambios)
            self.cambios={}
        for dep in self.dep_nuevos:
            insertDependencia(dep)
        for dep_suc in self.depdep_nuevos:
            insertDepDep(self.depdep_nuevos[dep_suc], dep_suc)
        for dep_suc in self.depdep:
            updateDepDep(self.depdep[dep_suc], dep_suc)
        for cod_dep in self.dep_deleted:
            eliminarDep(cod_dep=cod_dep)
        self.depdep_nuevos = {}
        self.dep_deleted=[]
        self.depdep={}
        self.dep_nuevos = []
        self.iniciar()

    def mover_nodo(self, event, nodo:ctk.CTkLabel, lineaIn, lineasOut, orgNodo:OrganigramaNodo):
        
        for lineaOut in lineasOut:
            x1,y1, xHijo, yHijo = self.canvas.coords(lineaOut)
            self.canvas.coords(lineaOut, event.x_root, event.y_root, xHijo, yHijo)    

        if lineaIn!=None:
            xMayor, yMayor, x2, y2 = self.canvas.coords(lineaIn)
            self.canvas.coords(lineaIn, xMayor, yMayor, event.x_root, event.y_root)
        
        nodo.place(x=event.x_root, y=event.y_root)
        orgNodo.dep.posX = event.x_root
        orgNodo.dep.posY = event.y_root
        if(orgNodo.dep.COD_DEP in self.cambios):
            self.cambios[orgNodo.dep.COD_DEP]['pos'] = [event.x_root, event.y_root]
        else:
            self.cambios[orgNodo.dep.COD_DEP] = {'pos':[event.x_root, event.y_root]}    

    def editar_texto(self, event, label:ctk.CTkLabel, orgNodo:OrganigramaNodo):
        label.configure(cursor="ibeam")
        entry = ctk.CTkEntry(self, width=label.winfo_width(), height=label.winfo_height(), fg_color=label.cget("bg_color"),
                         justify="center", validate="key", validatecommand=(self.validation, '%P'))
        entry.place(x=label.winfo_x(), y=label.winfo_y())

        entry.insert(tk.END, label.cget("text"))
        entry.focus_set()    
        entry.bind("<FocusOut>", lambda eventEntry: self.finalizar_edicion(eventEntry, entry, label, orgNodo))
        entry.bind("<Return>", lambda eventEntry: self.finalizar_edicion(eventEntry, entry, label, orgNodo))

    def finalizar_edicion(self, event, entry, label, orgNodo:OrganigramaNodo):
        label.configure(cursor="arrow")
        label.configure(text=entry.get())
        orgNodo.dep.NOM = entry.get()
        if(orgNodo.dep.COD_DEP in self.cambios):
            self.cambios[orgNodo.dep.COD_DEP]['nom'] = entry.get()
        else:
            self.cambios[orgNodo.dep.COD_DEP] = {'nom':entry.get()}           
        entry.destroy()

    def enter_nodo(self, orgNodo:OrganigramaNodo):
        nodoAnt = self.nodosLinea["nodo_ant"]
        nodoSuc = self.nodosLinea["nodo_suc"]
        if nodoAnt !=None:
            if len(orgNodo.listDep) <5:
                orgNodo.listDep.append(nodoSuc)
                self.depdep[nodoSuc.dep.COD_DEP] = orgNodo.dep.COD_DEP
                pos=0
                for nodo in nodoAnt.listDep:
                    if nodo.dep.COD_DEP==nodoSuc.dep.COD_DEP:
                        break
                    pos+=1
                del nodoAnt.listDep[pos]
            self.iniciar()
        

    def leave_nodo(self):
        pass

    def construir(self, orgNodo: OrganigramaNodo, lineaIn=None, nodoAnt=None):
        nodoLabel = ctk.CTkLabel(self, text=orgNodo.dep.NOM, width=self.width_nodo, height=self.height_nodo, bg_color=self.bg_color)
        nodoLabel.place(x=orgNodo.dep.posX, y=orgNodo.dep.posY)
        nodoLabel.bind("<Enter>", lambda event: self.enter_nodo(orgNodo))
        nodoLabel.bind("<Leave>", lambda event: self.leave_nodo())
        nodoLabel.bind("<Button-3>", lambda event: self.mostrar_opciones(event, orgNodo, nodoAnt))
        if (lineaIn!=None):
            xMayor, yMayor, x2, y2 = self.canvas.coords(lineaIn)
            self.canvas.coords(lineaIn, xMayor, yMayor, orgNodo.dep.posX, orgNodo.dep.posY)
            self.canvas.tag_bind(lineaIn, "<B3-Motion>", lambda event: self.mover_linea(event, lineaIn))
            self.canvas.tag_bind(lineaIn, "<ButtonRelease-3>", lambda event: self.linea_release(orgNodo, nodoAnt))
            
        lineasOut = []

        for nodoSuc in orgNodo.listDep:
            lineaOut = self.canvas.create_line(orgNodo.dep.posX, orgNodo.dep.posY, orgNodo.dep.posX, orgNodo.dep.posY, fill="black", width=5)
            lineasOut.append(lineaOut)
            self.construir(nodoSuc, lineaOut, orgNodo)

        nodoLabel.bind("<B1-Motion>",lambda event: self.mover_nodo(event, nodoLabel, lineaIn, lineasOut, orgNodo))
        nodoLabel.bind("<Double-Button-1>", lambda event: self.editar_texto(event, nodoLabel, orgNodo))
        

    def mostrar_opciones(self, event, orgNodo:OrganigramaNodo, nodoAnt:OrganigramaNodo):
        opciones = Opciones(master=self, orgNodo=orgNodo, width=100, height=50, bg_color="red", fg_color="blue", nodoAnt=nodoAnt)
        opciones.bind("<Button-3>", lambda event: opciones.destroy())
        opciones.place(x=orgNodo.dep.posX, y=orgNodo.dep.posY+50)

    def mover_linea(self, event, linea):
        x1, y1, xNodo, yNodo = self.canvas.coords(linea)
        self.canvas.coords(linea, event.x_root, event.y_root, xNodo, yNodo)

    def linea_release(self, nodoSuc:OrganigramaNodo, nodoAnt:OrganigramaNodo):
        self.nodosLinea["nodo_ant"] = nodoAnt
        self.nodosLinea["nodo_suc"] = nodoSuc


class Opciones(ctk.CTkFrame):
    def __init__(self, master:OrganigramaGrafico, orgNodo:OrganigramaNodo, nodoAnt:OrganigramaNodo, **kwargs):
        super().__init__(master, **kwargs)
        buttonAgregar = ctk.CTkButton(self, text="Agregar Dep", width=50, height=25, command=lambda:self.crearNodo(master, orgNodo))
        buttonAgregar.grid(row=0, sticky="s")
        buttonAgregar.bind("<Button-3>", lambda event: self.destroy())
        
        buttonPersonas = ctk.CTkButton(self, text="Ver Personas", width=50, height=25)
        buttonPersonas.grid(row=1, sticky="s")
        buttonPersonas.bind("<Button-3>", lambda event: self.destroy())

        buttonEliminar = ctk.CTkButton(self, text="Eliminar", width=50, height=25, command=lambda:self.eliminarNodo(master, orgNodo, nodoAnt))
        buttonEliminar.grid(row=2, sticky="s")
        buttonEliminar.bind("<Button-3>", lambda event: self.destroy())



    def crearNodo(self, master:OrganigramaGrafico, nodoAnt:OrganigramaNodo):
        if len(nodoAnt.listDep)>=5:
            return
        cod_dep = choice(forId)+choice(forId)+choice(forId)+choice(forId)
        dep = Dependencia(cod_dep, "", None, nodoAnt.dep.posX, nodoAnt.dep.posY+150, nodoAnt.dep.COD_ORG)
        orgNodo = OrganigramaNodo(dep)
        master.dep_nuevos.append(dep)
        master.depdep_nuevos[cod_dep] = nodoAnt.dep.COD_DEP
        nodoAnt.listDep.append(orgNodo)
        master.iniciar()

    def eliminarNodo(self, master:OrganigramaGrafico, orgNodo:OrganigramaNodo, nodoAnt:OrganigramaNodo):
        pos=0
        for nodo in nodoAnt.listDep:
            if orgNodo.dep.COD_DEP == nodo.dep.COD_DEP:
                break
            pos+=1
        del nodoAnt.listDep[pos]
        master.dep_deleted.append(orgNodo.dep.COD_DEP)
        master.iniciar()