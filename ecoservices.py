# -*- coding: utf-8 -*-
"""
Monitoring provision of ecosystem services.
Created on Fri Dec 2 2021
Metodologic Basis: Me.Aline da Nóbrega Oliveira
Programing: Me.Bruno Rodrigues de Oliveira
Description: Calculation of the water ecosystem services of a subbasin with ##-- based on the methodology of Lima et.al (2017)
"""

## Importing Modules
import arcpy
from arcpy.sa import *
import os


########################################################################################################################################################################
## Define a classe coms os dados do usuário
########################################################################################################################################################################

class servicos_ecossistemicos():
	def __init__(self, folder, soil, landuse, slope, drainage_distance):
		self.folder = folder
		self.soil =  soil
		self.landuse = landuse
		self.slope = slope
		self.drainage_distance = drainage_distance
		self.geodatabase_path = self.createGeodatabase()
		arcpy.env.workspace = folder
		arcpy.env.scratchWorkspace = folder
		arcpy.env.overwriteOutput = True
	
	@property
	def layers(self):
		return self.layers
	
	def checkFields(self):
		"""Check if all layers have the necessary fields.
			:return: None
		"""
		layers_array = [self.soil, self.landuse]
		analisys_fields = ["CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"]
		for layer in layers_array:
			field_array = []
			desc = arcpy.Describe(layer)
			fields = desc.fields
			for field in fields:
				#arcpy.AddMessage(field.name)
				field_array.append(field.name)
			for fieldName in analisys_fields:
				if fieldName not in field_array:
					arcpy.AddError('Field %s not available in layer %s' % (fieldName, layer))
				else:
					arcpy.AddMessage('Field %s available in layer %s' % (fieldName, layer))
	
	def createGeodatabase (self):
		"""Create geodatabase of analisys.
			:return: Geodatabase path
		"""
		try:
			arcpy.CreateFileGDB_management(self.folder, 'ECOSERVICES')
			path = os.path.join(self.folder, 'ECOSERVICES.gdb')
			return path
		except Exception as e:
			arcpy.AddError('Failed to create geodatabase. Reason: %s'% (e))


	def convertRasters (self):
		"""Convert landuse and soil vectors to rastes using attribute table values. More information at Lima et.al (2017).
			:return: Soil and Landuser rasters reclassified
		"""
		fields = ["CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"]
		arcpy.AddMessage('Converting vectors to rasters...')
		for field in fields:
			raster_landuse = field + "_landuse"
			out_raster_landuse = os.path.join(self.geodatabase_path, raster_landuse)
			arcpy.conversion.PolygonToRaster(self.landuse, field, out_raster_landuse)

			raster_soil = field + "_soil"
			out_raster_soil = os.path.join(self.geodatabase_path, raster_soil)
			arcpy.conversion.PolygonToRaster(self.soil, field, out_raster_soil)
	
	def convertSlope(self):
		"""Reclassify slove using adequade values. More information at Lima et.al (2017).
			:return: Slope rasters reclassified
		"""
		arcpy.AddMessage('Converting slope to adequate values ...')
		fields = ["CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"]
		for field in fields:
			raster_name = field + "_slopeReclass"
			out_rasterdataset = os.path.join(self.geodatabase_path, raster_name)
			if field == "CONTROLE_RUNOFF":
				outReclass = arcpy.sa.Reclassify(self.slope, "Value", RemapRange([[0,5,90],[5,10,80],[10,15,60],[15,20,60],[20,25,50],[25,30,50],[30,9999,50]]))
				outReclass.save(out_rasterdataset)
			elif field == "ABAST_AGUA":
				outReclass = arcpy.sa.Reclassify(self.slope, "Value", RemapRange([[0,5,90],[5,10,80],[10,15,60],[15,20,60],[20,25,50],[25,30,50],[30,9999,50]]))
				outReclass.save(out_rasterdataset)
			elif field == "MAN_QUAL_AGUA":
				outReclass = arcpy.sa.Reclassify(self.slope, "Value", RemapRange([[0,5,95],[5,10,90],[10,15,80],[15,20,80],[20,25,60],[25,30,60],[30,9999,60]]))
				outReclass.save(out_rasterdataset)
			elif field == "MAN_QUAL_SOLO":
				outReclass = arcpy.sa.Reclassify(self.slope, "Value", RemapRange([[0,5,100],[5,10,95],[10,15,90],[15,20,90],[20,25,85],[25,30,85],[30,9999,85]]))
				outReclass.save(out_rasterdataset)
			elif field == "CONTROLE_EROSAO":
				outReclass = arcpy.sa.Reclassify(self.slope, "Value", RemapRange([[0,5,95],[5,10,90],[10,15,80],[15,20,80],[20,25,80],[25,30,60],[30,9999,60]]))
				outReclass.save(out_rasterdataset)

	def finalRasters (self):
		"""Remove temporary files.
			:return: Analazing data.... Please wait....
		"""
		arcpy.AddMessage('Analizing data.... Please wait....')
		fields = ["CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"]
		for field in fields:
			raster_name_uso_cobertura = field + "_landuse"
			out_rasterdataset_vetor_uso_cobertura = os.path.join(self.geodatabase_path, raster_name_uso_cobertura)
			raster_name_pedologia = field + "_soil"
			out_rasterdataset_vetor_pedologia = os.path.join(self.geodatabase_path, raster_name_pedologia)
			raster_name_declividade = field + "_slopeReclass"
			out_rasterdataset = os.path.join(self.geodatabase_path, raster_name_declividade)
			if field == "MAN_QUAL_AGUA":
				output_raster_path = os.path.join(self.geodatabase_path, field)
				imput_raster_path_uso = Raster(os.path.join(self.geodatabase_path, raster_name_uso_cobertura))
				imput_raster_path_pedologia = Raster(os.path.join(self.geodatabase_path, raster_name_pedologia))
				imput_raster_path_declividade = Raster(os.path.join(self.geodatabase_path, raster_name_declividade))
				imput_raster_path_distancia = Raster(self.drainage_distance)
				raster_calculator_enter = Float(imput_raster_path_uso) * Float(imput_raster_path_pedologia) * (Float(imput_raster_path_declividade)/100.0) * Float(imput_raster_path_distancia)
				raster_calculator_enter.save(output_raster_path)
			else:
				output_raster_path = os.path.join(self.geodatabase_path, field)
				imput_raster_path_uso = Raster(os.path.join(self.geodatabase_path, raster_name_uso_cobertura))
				imput_raster_path_pedologia = Raster(os.path.join(self.geodatabase_path, raster_name_pedologia))
				imput_raster_path_declividade = Raster(os.path.join(self.geodatabase_path, raster_name_declividade))		
				raster_calculator_enter = Float(imput_raster_path_uso) * Float(imput_raster_path_pedologia) * (Float(imput_raster_path_declividade)/100.0)
				raster_calculator_enter.save(output_raster_path)

	def removeTemporary(self):
		"""Remove temporary files.
			:return: Slope rasters reclassified
		"""
		arcpy.AddMessage('Erase temporary rasters...')
		fields = ["CONTROLE_RUNOFF","ABAST_AGUA", "MAN_QUAL_AGUA", "MAN_QUAL_SOLO", "CONTROLE_EROSAO"]
		for field in fields:
			raster_landuse = field + "_landuse"
			out_raster_landuse = os.path.join(self.geodatabase_path, raster_landuse)
			arcpy.Delete_management(out_raster_landuse, "")
			raster_soil = field + "_soil"
			out_raster_soil = os.path.join(self.geodatabase_path, raster_soil)
			arcpy.Delete_management(out_raster_soil, "")
			raster_name_declividade = field + "_slopeReclass"
			out_rasterdataset = os.path.join(self.geodatabase_path, raster_name_declividade)
			arcpy.Delete_management(out_rasterdataset, "")

########################################################################################################################################################################
## Main
########################################################################################################################################################################

if __name__ == '__main__':
	arcpy.CheckOutExtension("Spatial")
	folder = arcpy.GetParameterAsText(0)
	soil = arcpy.GetParameterAsText(1)
	landuse = arcpy.GetParameterAsText(2)
	slope = arcpy.GetParameterAsText(3)
	drainage_distance = arcpy.GetParameterAsText(4)
	arcpy.AddMessage('Configuring environment....')
	se = servicos_ecossistemicos(folder, soil, landuse, slope, drainage_distance)
	se.checkFields()
	se.convertRasters()
	se.convertSlope()
	se.finalRasters()
	se.removeTemporary()