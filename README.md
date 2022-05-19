# Ecoservices
"""<br>
Monitoring provision of ecosystem services. <br>
Created on Fri Dec 2 2021 <br>
Metodologic Basis: Me.Aline da Nóbrega Oliveira - http://lattes.cnpq.br/8126823114126601 <br>
Programing: Me.Bruno Rodrigues de Oliveira - http://lattes.cnpq.br/3064858361190088 <br>
Description: Calculation of the water ecosystem services of a subbasin with ##-- based on the methodology of Lima et.al (2017) - https://dx.doi.org/10.1016/j.ecolind.2017.07.028 <br>
"""

"""Calculation of the water ecosystem services of a subbasin.
			:param: folder whre the geodatabase will be created
      :param: landuse
      :param: slope
      :param: soil
      :param: distance
      :return: Rasters for ecosistemic services "CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"
		"""

Note: landuse and soil vectors/ layers must hav fields named with "CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"

Tested on ArcMap Desktop 10.8 and 10.7.1 - Should work on all Arcgis Desktop versions<br>

# Dependences

Python 2.7 (arcpy) <br>
Spatial Analist Extension <br>

# Dependences

Check if all layers have the necessary fields.
