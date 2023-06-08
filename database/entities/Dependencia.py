from database.entities.Persona import Persona
class Dependencia:
    def __init__(self, COD_DEP, NOM, RES:Persona, x, y, COD_ORG):
        self.COD_DEP = COD_DEP  
        self.NOM = NOM
        self.RES = RES ##RES es un objeto persona
        self.posX = x
        self.posY = y 
        self.COD_ORG = COD_ORG
