import tkinter as tk
import customtkinter as ctk
from OrganigramaNodo import OrganigramaNodo



class OrganigramaGrafico(ctk.CTk):
    width_nodo=100
    height_nodo=50
    bg_color="black"
    def __init__(self, organigrama:OrganigramaNodo) -> None:
        super().__init__()
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.construir(organigrama, None)

    def mover_nodo(self, event, nodo:ctk.CTkLabel, lineaIn, lineasOut):
    
        for lineaOut in lineasOut:
            x1,y1, xHijo, yHijo = self.canvas.coords(lineaOut)
            self.canvas.coords(lineaOut, event.x_root, event.y_root, xHijo, yHijo)    

        if lineaIn!=None:
            xMayor, yMayor, x2, y2 = self.canvas.coords(lineaIn)
            self.canvas.coords(lineaIn, xMayor, yMayor, event.x_root, event.y_root)
        
        nodo.place(x=event.x_root, y=event.y_root)


    def construir(self, orgNodo: OrganigramaNodo, lineaIn):
        print(orgNodo.dep.NOM)
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

        nodoLabel.bind("<B1-Motion>",lambda event: self.mover_nodo(event, nodoLabel, lineaIn, lineasOut))