from database.connection.Connect import Connect
from database.entities.Organigrama import Organigrama
from database.entities.Dependencia import Dependencia
from database.entities.Persona import Persona
db = Connect()

def updateDepPos(pos, cod_dep:str):
    update = '''UPDATE dependencias SET pos_x=%s, pos_y=%s WHERE cod_dep=%s'''
    params = (pos[0], pos[1], cod_dep)
    result = db.update_data(update, params)
    if(result):
        print("posicion actualizada de la dependencia con id = "+cod_dep)
    else:
         print("error al actualizar la posicion la dependencia con id = "+cod_dep)   

def updateDepNom(newNom:str, cod_dep:str):
    update = '''UPDATE dependencias SET nom=%s WHERE cod_dep=%s'''
    params = (newNom, cod_dep)
    result = db.update_data(update, params)
    if(result):
        print("nombre actualizado de la dependencia con id = "+cod_dep)
    else:
         print("error al actualizar el nombrela dependencia con id = "+cod_dep) 
         print("nombre nuevo = "+newNom)  

def updateDeps(cambios):
    for cod_dep in cambios:
        for cambio in cambios[cod_dep]:
            print(cambio)
            if cambio=="pos":
                updateDepPos(cambios[cod_dep]["pos"], cod_dep)
            elif cambio=="nom":
                updateDepNom(cambios[cod_dep]["nom"], cod_dep)

def insertOrganigrama(org:Organigrama):
    insert = '''INSERT INTO organigramas(cod_org, org, fec) VALUES(%s,%s,%s)'''
    params = (org.COD_ORG, org.ORG, org.FEC)
    db.update_data(insert, params)

def insertDependencia(dep:Dependencia):
    insert = '''INSERT INTO dependencias(cod_dep, nom, codres, cod_org, pos_x, pos_y) 
    VALUES (%s, %s,%s,%s,%s,%s)'''

def crearOrganigrama(org:Organigrama, depMayor:Dependencia):
    pass
