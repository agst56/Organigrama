from database.connection.Connect import Connect
from database.entities.Organigrama import Organigrama
from database.entities.Dependencia import Dependencia
from database.entities.Persona import Persona
db = Connect()
SELECT = 'SELECT '

def retrieveOrganigramas():
    query = "SELECT * FROM organigramas"
    resultList = db.query(query)
    organigramas = []
    for result in resultList:
        organigrama = Organigrama(result['cod_org'], result['org'], result['fec'])
        organigramas.append(organigrama)
    return organigramas
def retrieveOrgInit(COD_ORG):
    columns= '''org.COD_ORG as COD_ORG, org.ORG, org.FEC, dep.COD_DEP as COD_DEP, dep.NOM as NOM_DEP,
    dep.pos_x, dep.pos_y, 
    p.COD_PER, p.NOM as NOM_PER, p.APE, p.TEL, p.DIR, p.SAL'''
    query = SELECT+columns+''' FROM Organigramas org INNER JOIN OrgDep od ON od.COD_ORG=org.COD_ORG
    INNER JOIN Dependencias dep ON dep.COD_DEP=od.DEP_MAYOR
    LEFT JOIN Personas p ON dep.CODRES=p.COD_PER WHERE org.COD_ORG=%s'''
    params = [COD_ORG]
    resultList = db.query(query, params)
    result = resultList[0]
    responsable = Persona(result['cod_per'], result['ape'], result['nom_per'], result['tel'], result['dir'], result['sal'], result['cod_dep'])
    dependencia = Dependencia(result['cod_dep'], result['nom_dep'], responsable, result["pos_x"], result["pos_y"], result["cod_org"])
    return dependencia


def retrieveDepSuc(COD_DEP):
    columns = '''dep_suc.COD_DEP as COD_DEP, dep_suc.NOM as NOM_DEP, dep_suc.COD_ORG,   
    dep_suc.pos_x, dep_suc.pos_y, p.COD_PER, p.NOM as NOM_PER, p.APE, p.TEL, p.DIR, p.SAL'''
    query = SELECT+columns+''' FROM DepDep ddp  
    INNER JOIN Dependencias dep_suc ON dep_suc.COD_DEP=ddp.DEP_SUC
    LEFT JOIN Personas p ON p.COD_PER = dep_suc.CODRES  
    WHERE ddp.DEP_ANT=%s
    '''
    params = [COD_DEP]
    resultList = db.query(query, params)
    depSucesoras = []
    for result in resultList:
        responsable = Persona(result['cod_per'], result['ape'], result['nom_per'], result['tel'], result['dir'], result['sal'], result['cod_dep'])
        dependencia = Dependencia(result['cod_dep'], result['nom_dep'], responsable, result["pos_x"], result["pos_y"], result["cod_org"])
        depSucesoras.append(dependencia)
        

    return depSucesoras

def retrievePersonas(cod_dep:str):
    query = '''SELECT * FROM personas WHERE dep=%s'''
    params = (cod_dep)
    resultList = db.query(query, params)
    personas=[]
    for result in resultList:
        persona = Persona(Persona(result['cod_per'], result['ape'], result['nom'], result['tel'], result['dir'], result['sal'], result['dep']))
        personas.append(persona)

    return personas


