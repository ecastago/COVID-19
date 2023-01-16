import pandas as pd
from sodapy import Socrata

class Client:
    def __init__(self, numero_casos,departamento) -> None:
        self.client = Socrata("www.datos.gov.co", None)
        self.consultas = self.client.get("gt2j-8ykr", limit=numero_casos, departamento_nom=departamento)
        self.df = pd.DataFrame.from_records(self.consultas)
        try:
            self.df = self.df[["ciudad_municipio_nom","departamento_nom","edad","tipo_recuperacion","estado","pais_viajo_1_nom"]]
        except Exception:
            print(Exception)    