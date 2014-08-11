# -*- coding: utf-8 -*-
#
# Scrapper de la pagina http://201.175.44.226/SNRSPD/Basica/SNRSPDresultadosbasica/ConsultaPublica.aspx
# Por: Ricardo Alanis
# Agosto del 2014
#
#

import dryscrape
from bs4 import BeautifulSoup
import csv
import re
import os

Estados = {1:"Aguascalientes",2:"Baja California",3:"Baja California Sur",4:"Campeche",7:"Chiapas",8:"Chihuahua",5:"Coahuila",6:"Colima",9:"Distrito Federal",10:"Durango",15:"Estado de México",11:"Guanajuato",12:"Guerrero",13:"Hidalgo",14:"Jalisco",16:"Michoacán",17:"Morelos",18:"Nayarit",19:"Nuevo León",20:"Oaxaca",21:"Puebla",22:"Querétaro",23:"Quintana Roo",24:"San Luis Potosí",25:"Sinaloa",26:"Sonora",27:"Tabasco",28:"Tamaulipas",29:"Tlaxcala",30:"Veracruz",31:"Yucatán",32:"Zacatecas"}
#Estados = {1:"Aguascalientes"}
Convocatorias = {1:"Pública y Abierta",2:"Egresados de Normales"}
#Convocatorias = {2:"Egresados de Normales"}
Examenes= {101:"EDUCACIÓN PREESCOLAR",105:"EDUCACIÓN PREESCOLAR INDÍGENA",2011:"EDUCACIÓN PRIMARIA",205:"EDUCACIÓN PRIMARIA INDÍGENA",2103:"INGLÉS EN EDUCACIÓN PREESCOLAR",2101:"INGLÉS EN EDUCACIÓN PRIMARIA",9002:"EDUCACIÓN SECUNDARIA DE ASIGNATURA ESTATAL",303:"EDUCACIÓN SECUNDARIA DE BIOLOGÍA",301:"EDUCACIÓN SECUNDARIA DE ESPAÑOL",304:"EDUCACIÓN SECUNDARIA DE FÍSICA",309:"EDUCACIÓN SECUNDARIA DE FORMACIÓN CÍVICA Y ÉTICA",311:"EDUCACIÓN SECUNDARIA DE FRANCÉS",307:"EDUCACIÓN SECUNDARIA DE GEOGRAFÍA",308:"EDUCACIÓN SECUNDARIA DE HISTORIA",310:"EDUCACIÓN SECUNDARIA DE INGLÉS",302:"EDUCACIÓN SECUNDARIA DE MATEMÁTICAS",305:"EDUCACIÓN SECUNDARIA DE QUÍMICA",7011:"EDUCACIÓN SECUNDARIA DE ARTES VISUALES",7012:"EDUCACIÓN SECUNDARIA DE DANZA",7013:"EDUCACIÓN SECUNDARIA DE MÚSICA",7014:"EDUCACIÓN SECUNDARIA DE TEATRO",3502:"TELESECUNDARIA",4031:"EDUCACIÓN SECUNDARIA DE ACUICULTURA",4032:"EDUCACIÓN SECUNDARIA ADMINISTRACIÓN CONTABLE",4033:"EDUCACIÓN SECUNDARIA DE AGRICULTURA",4034:"EDUCACIÓN SECUNDARIA DE APICULTURA",4035:"EDUCACIÓN SECUNDARIA DE CARPINTERÍA E INDUSTRIA DE LA MADERA",4036:"EDUCACIÓN SECUNDARIA CLIMATIZACIÓN Y REFRIGERACIÓN",4037:"EDUCACIÓN SECUNDARIA DE CONFECCIÓN DEL VESTIDO E INDUSTRIA TEXTIL",4038:"EDUCACIÓN SECUNDARIA DE CREACIÓN ARTESANAL",4039:"EDUCACIÓN  SECUNDARIA DE DISEÑO ARQUITÉCTONICO",40310:"EDUCACIÓN SECUNDARIA DE DISEÑO DE CIRCUITOS ELÉCTRICOS",40311:"EDUCACIÓN SECUNDARIA DE DISEÑO DE ESTRUCTURAS METÁLICAS",40312:"EDUCACIÓN SECUNDARIA DE DISEÑO DE INTERIORES",40313:"EDUCACIÓN SECUNDARIA DE DISEÑO GRÁFICO",40314:"EDUCACIÓN SECUNDARIA DE DISEÑO INDUSTRIAL",40315:"EDUCACIÓN SECUNDARIA DE DISEÑO Y CREACIÓN PLÁSTICA",40316:"EDUCACIÓN SECUNDARIA DE DISEÑO Y MECÁNICA AUTOMOTRIZ",40317:"EDUCACIÓN SECUNDARIA DE DISEÑO Y TRANSPORTE MARÍTIMO",40318:"EDUCACIÓN SECUNDARIA DUCTOS Y CONTROLES",40319:"EDUCACIÓN SECUNDARIA ELECTRÓNICA, COMUNICACIÓN Y SISTEMAS DE CONTROL",40320:"EDUCACIÓN SECUNDARIA DE ESTÉTICA Y SALUDO CORPORAL",40321:"EDUCACIÓN SECUNDARIA DE INFORMÁTICA",40322:"EDUCACIÓN SECUNDARIA DE MÁQUINAS, HERRAMIENTAS Y SISTEMAS DE CONTROL",40323:"EDUCACIÓN SECUNDARIA DE OFIMÁTICA",40324:"EDUCACIÓN SECUNDARIA DE PECUARIA",40325:"EDUCACIÓN SECUNDARIA DE PESCA",40326:"EDUCACIÓN SECUNDARIA DE PREPARACIÓN Y CONSERVACIÓN DE ALIMENTOS",40327:"EDUCACIÓN SECUNDARIA DE PREPARACIÓN, CONSERVACIÓN E INDUSTRIALIZACIÓN DE ALIMENTOS AGRÍCOLAS",40328:"EDUCACIÓN SECUNDARIA DE PROCESAMIENTO DE PRODUCTOS PESQUEROS",40329:"EDUCACIÓN SECUNDARIA DE SILVICULTURA",40330:"EDUCACIÓN SECUNDARIA DE TURISMO",4021:"EDUCACIÓN FÍSICA",5011:"EDUCACIÓN ESPECIAL Auditiva y Lenguaje",2012:"EDUCACIÓN BÁSICA PARA ADULTOS PRIMARIA",3501:"EDUCACIÓN BÁSICA PARA ADULTOS SECUNDARIA",2013:"MISIONES CULTURALES",40331:"EDUCACIÓN SECUNDARIA Preparación, Conservación e Industrialización de Alimentos Pecuarios (Cárnicos)",5012:"EDUCACIÓN ESPECIAL Intelectual",5013:"EDUCACIÓN ESPECIAL Motriz",5014:"EDUCACIÓN ESPECIAL Psicologia Educativa",5015:"EDUCACIÓN ESPECIAL Visual",5016:"EDUCACIÓN ESPECIAL Especial",8013:"EDUCACIÓN ESPECIAL Acompañante de Música",8010:"EDUCACIÓN PREESCOLAR Acompañante de Música",40332:"EDUCACIÓN SECUNDARIA Preparación, Conservación e Industrialización de Alimentos Pecuarios (Lácteos)",40333:"EDUCACIÓN SECUNDARIA Preparación, Conservación e Industrialización de Alimentos (A,C y L)",8034:"EDUCACIÓN PREESCOLAR Maestro de Taller de Lectura y Escritura",8011:"EDUCACIÓN PRIMARIA Maestro de Enseñanza Artística",8040:"EDUCACIÓN PRIMARIA Maestro de Taller",8035:"EDUCACIÓN PRIMARIA Maestro de Taller de Lectura y Escritura",8020:"EDUCACIÓN SECUNDARIA Maestro de Aula de Medios",8036:"EDUCACIÓN SECUNDARIA Maestro de Taller de Lectura y Escritura",8012:"EDUCACIÓN PRIMARIA INDÍGENA Maestro de Música",8043:"EDUCACIÓN INDÍGENA Maestro de Taller",8042:"EDUCACIÓN ESPECIAL Maestro de Taller"}
#Examenes= {2011:"EDUCACIÓN PRIMARIA"}



def getbody(Entidad,Convocatoria,Examen,sess):
	#Visita la pagina de la tabla, virtualmente, y extrae el html de la pagina.
	workingbody = []

	# Visitar sitio 
	sess.visit('/SNRSPD/Basica/SNRSPDresultadosbasica/ConsultaPublica.aspx')


	# Seleccionar Entidad
	ddlEntidad = sess.at_xpath('//*[@name="ddlEntidad"]')
	ddlEntidad.set(Entidad)

	#Convocatoria
	ddlConvocatoria = sess.at_xpath('//*[@name="ddlConvocatoria"]')
	ddlConvocatoria.set(Convocatoria)


	#Examen
	ddlExamen = sess.at_xpath('//*[@name="ddlExamen"]')
	ddlExamen.set(Examen)

	#Enviar
	btnconsultar = sess.at_xpath('//*[@name="btnconsultar"]')
	btnconsultar.click()

	# Guardar el cuerpo de la pagina en un vector.
	workingbody.append(sess.body())

	links_en_pagina = sess.xpath('//a[@href]')

	#Si hay mas de un link en la pagina, significa que hay mas paginas
	if len(links_en_pagina) > 1:
		lenlinks = len(links_en_pagina)-1
		i = 0
		while i < lenlinks:
			
			#eliminar el link de cajon (El de arriba de la pagina (que no tiene que ver con los datos))
			del links_en_pagina[0]
			link = links_en_pagina[i]
			link.click()
			workingbody.append(sess.body())

			numpagina = i + 2

			# Revisitar sitio base para tomar otro cuerpo de pagina, si es necesario
			sess.visit('/SNRSPD/Basica/SNRSPDresultadosbasica/ConsultaPublica.aspx')
			ddlEntidad = sess.at_xpath('//*[@name="ddlEntidad"]')
			ddlEntidad.set(Entidad)
			ddlConvocatoria = sess.at_xpath('//*[@name="ddlConvocatoria"]')
			ddlConvocatoria.set(Convocatoria)
			ddlExamen = sess.at_xpath('//*[@name="ddlExamen"]')
			ddlExamen.set(Examen)
			btnconsultar = sess.at_xpath('//*[@name="btnconsultar"]')
			btnconsultar.click()

			links_en_pagina = sess.xpath('//a[@href]')

			i = i + 1


	return workingbody

def scrappetable(pages):
	#Toma el vector de paginas alimentado por la funcion anterior, y las convierte en tablas. Nota: Se consideraron los id de lastablas  
	#localizaron en el sitio, manualmente, sin embargo, se hicieron pruebas aleatoreas y no se encontro otro id.
	tables = []
	tipo = []

	for page in pages:
		tipo = 0
		soup = BeautifulSoup(page)
		findtable = soup.find('table', id="gvResultadosEvaluacion")
		if findtable is None: findtable = soup.find('table', id="gvResultadosEvaluacion2")
		if findtable is None: 
			findtable = soup.find('table', id="gvResultadosEvaluacion3")
			tipo = 3
		if findtable is None: tipo = 1

		tables.append(findtable)


	return tables, tipo

def printcsv(tables,Entidad,Convocatoria,Examen,tipo):
	#Toma las tablas de la combinacion actual y las escribe en el archivo.
	vectordataplace = [Entidad,Convocatoria,Examen]

	for numtable, table in enumerate(tables):
		i = 1
		for row in table.findAll('tr'):
			if tipo == 3:
				cells = vectordataplace + [c.text.encode('utf-8') for c in row.findAll('td')]
			else: 
				cells = vectordataplace + [c.text.encode('utf-8') for c in row.findAll('td')] + ["NA","NA"]
			
			if i>3 and i<54: 
				if numtable==len(tables)-1 and len(tables) > 1:
					if i< len(table.findAll('tr'))-1:
						csvwriter.writerow(cells)	
				else:	
					csvwriter.writerow(cells)
			i = i + 1

	return 



#Empieza main

# Empezar la sesion para bajar archivo
sess = dryscrape.Session(base_url = 'http://201.175.44.226')
header  = ["Entidad", "Convocatoria", "Examen", "Posición_en_lista_de_prelación","Folio_del_sustentante","Grupo_de_desempeño","R_CyH_Nivel_de_desempeño","R_CyH_Puntuación_total_del_instrumento_de_evaluación","R_CyH_Puntuación_en_el_área_Intervención_didáctica","R_CyH_Puntuación_en_el_área_Aspectos_curriculares","R_HyR_Nivel_de_desempeño","R_HyR_Puntuación_total_del_instrumento_de_evaluación","R_HyR_Puntuación_en_el_área_Compromiso_ético","R_HyR_Puntuación_en_el_área_Mejora_profesional","R_HyR_Puntuación_en_el_área_Gestión_escolar_y_vinculación_con_la_comunidad", "R_ECoA_Nivel_de_Desempeño","R_ECoA_Puntuación_Total"] 

#Empieza el archivo a escribir
with open('output.csv', 'w') as f:
	csvwriter = csv.writer(f,delimiter=",")
	csvwriter.writerow(header)

	#Por cada estado en la lista, por cada convocatoria, por cada examen.
	for keyEstado, Estado in Estados.iteritems():
		for keyConvocatoria, Convocatoria in Convocatorias.iteritems():
			for keyExamen, Examen in Examenes.iteritems():

				print "Trabajando con: "  + Estado + "/" + Convocatoria + "/" + Examen
				#Obtener las paginas de las tablas
				pages = getbody(keyEstado,keyConvocatoria,keyExamen,sess)

				#Extraer dichas tablas
				tables, tipo = scrappetable(pages)

				#Para la combinacion actual, ¿Hay informacion?
				if tipo==1: 
					print "Sin informacion."
				else:
					print "Imprimiendo."
					printcsv(tables,keyEstado,keyConvocatoria,keyExamen, tipo) 

#Modificar Archivo
open("output_clean.csv", "w").write(open("output.csv").read().replace(" ",""))



