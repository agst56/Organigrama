from OrganigramaNodo import OrganigramaNodo
from functions import ConstruirOrganigrama
from functions.OrganigramaGrafico import OrganigramaGrafico

organigrama = ConstruirOrganigrama.construir("ABC")

ConstruirOrganigrama.imprimirOrganigrama(organigrama)
app = OrganigramaGrafico(organigrama)
app.mainloop()

  
