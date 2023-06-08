from database.access import DataAccess
from database.access import UpdateData
from OrganigramaNodo import OrganigramaNodo
from database.entities.Dependencia import Dependencia
from database.entities.Organigrama import Organigrama
from random import choice
import datetime
forId = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
           'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def depRecursiva(nodo: OrganigramaNodo):
    depSucesoras = DataAccess.retrieveDepSuc(nodo.dep.COD_DEP)
    listDep=[]
    for dep in depSucesoras:
        nodoSuc = OrganigramaNodo(dep)
        listDep.append(nodoSuc)
        depRecursiva(nodoSuc)
    nodo.setListDep(listDep)
def construir(COD_ORG:str) -> OrganigramaNodo:
    depMayor = DataAccess.retrieveOrgInit(COD_ORG)
    nodoMayor = OrganigramaNodo(depMayor)
    depRecursiva(nodoMayor)
    return nodoMayor

def imprimirOrganigrama(nodo: OrganigramaNodo):
    print(nodo.dep.NOM)
    for nodoSuc in nodo.listDep:
        imprimirOrganigrama(nodoSuc)


def crearOrganigrama(nom_org):
    cod_org = choice(forId)+choice(forId)+choice(forId)
    cod_dep = choice(forId)+choice(forId)+choice(forId)+choice(forId)
    fec = datetime.datetime.now().date().strftime('%Y-%m-%d')
    org = Organigrama(cod_org, nom_org, fec)
    dep = Dependencia(cod_dep, "", None, 600, 100, cod_org)
    UpdateData.insertOrganigrama(org)
    UpdateData.insertDependencia(dep)
    UpdateData.insertOrgDep(cod_org=cod_org, cod_dep_mayor=cod_dep)
    print("Organigrama creado con nombre: "+nom_org+ " y cod_org: "+cod_org)
    return cod_org
    
    