from database.access import DataAccess
from OrganigramaNodo import OrganigramaNodo
from database.entities.Dependencia import Dependencia

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
    
    