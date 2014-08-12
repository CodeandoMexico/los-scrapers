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

#Prueba para subprueba
#Estados = {1:"Aguascalientes",2:"Baja California",3:"Baja California Sur",4:"Campeche",7:"Chiapas",8:"Chihuahua",5:"Coahuila",6:"Colima",9:"Distrito Federal",10:"Durango",15:"Estado de México",11:"Guanajuato",12:"Guerrero",13:"Hidalgo",14:"Jalisco",16:"Michoacán",17:"Morelos",18:"Nayarit",19:"Nuevo León",20:"Oaxaca",21:"Puebla",22:"Querétaro",23:"Quintana Roo",24:"San Luis Potosí",25:"Sinaloa",26:"Sonora",27:"Tabasco",28:"Tamaulipas",29:"Tlaxcala",30:"Veracruz",31:"Yucatán",32:"Zacatecas"}
#Estados = {3:"Baja California Sur"}
#Convocatorias = {1:"Pública y Abierta",2:"Egresados de Normales"}
#Convocatorias = {1:"Pública y Abierta"}
#Examenes= {101:"EDUCACIÓN PREESCOLAR",105:"EDUCACIÓN PREESCOLAR INDÍGENA",2011:"EDUCACIÓN PRIMARIA",205:"EDUCACIÓN PRIMARIA INDÍGENA",2103:"INGLÉS EN EDUCACIÓN PREESCOLAR",2101:"INGLÉS EN EDUCACIÓN PRIMARIA",9002:"EDUCACIÓN SECUNDARIA DE ASIGNATURA ESTATAL",303:"EDUCACIÓN SECUNDARIA DE BIOLOGÍA",301:"EDUCACIÓN SECUNDARIA DE ESPAÑOL",304:"EDUCACIÓN SECUNDARIA DE FÍSICA",309:"EDUCACIÓN SECUNDARIA DE FORMACIÓN CÍVICA Y ÉTICA",311:"EDUCACIÓN SECUNDARIA DE FRANCÉS",307:"EDUCACIÓN SECUNDARIA DE GEOGRAFÍA",308:"EDUCACIÓN SECUNDARIA DE HISTORIA",310:"EDUCACIÓN SECUNDARIA DE INGLÉS",302:"EDUCACIÓN SECUNDARIA DE MATEMÁTICAS",305:"EDUCACIÓN SECUNDARIA DE QUÍMICA",7011:"EDUCACIÓN SECUNDARIA DE ARTES VISUALES",7012:"EDUCACIÓN SECUNDARIA DE DANZA",7013:"EDUCACIÓN SECUNDARIA DE MÚSICA",7014:"EDUCACIÓN SECUNDARIA DE TEATRO",3502:"TELESECUNDARIA",4031:"EDUCACIÓN SECUNDARIA DE ACUICULTURA",4032:"EDUCACIÓN SECUNDARIA ADMINISTRACIÓN CONTABLE",4033:"EDUCACIÓN SECUNDARIA DE AGRICULTURA",4034:"EDUCACIÓN SECUNDARIA DE APICULTURA",4035:"EDUCACIÓN SECUNDARIA DE CARPINTERÍA E INDUSTRIA DE LA MADERA",4036:"EDUCACIÓN SECUNDARIA CLIMATIZACIÓN Y REFRIGERACIÓN",4037:"EDUCACIÓN SECUNDARIA DE CONFECCIÓN DEL VESTIDO E INDUSTRIA TEXTIL",4038:"EDUCACIÓN SECUNDARIA DE CREACIÓN ARTESANAL",4039:"EDUCACIÓN  SECUNDARIA DE DISEÑO ARQUITÉCTONICO",40310:"EDUCACIÓN SECUNDARIA DE DISEÑO DE CIRCUITOS ELÉCTRICOS",40311:"EDUCACIÓN SECUNDARIA DE DISEÑO DE ESTRUCTURAS METÁLICAS",40312:"EDUCACIÓN SECUNDARIA DE DISEÑO DE INTERIORES",40313:"EDUCACIÓN SECUNDARIA DE DISEÑO GRÁFICO",40314:"EDUCACIÓN SECUNDARIA DE DISEÑO INDUSTRIAL",40315:"EDUCACIÓN SECUNDARIA DE DISEÑO Y CREACIÓN PLÁSTICA",40316:"EDUCACIÓN SECUNDARIA DE DISEÑO Y MECÁNICA AUTOMOTRIZ",40317:"EDUCACIÓN SECUNDARIA DE DISEÑO Y TRANSPORTE MARÍTIMO",40318:"EDUCACIÓN SECUNDARIA DUCTOS Y CONTROLES",40319:"EDUCACIÓN SECUNDARIA ELECTRÓNICA, COMUNICACIÓN Y SISTEMAS DE CONTROL",40320:"EDUCACIÓN SECUNDARIA DE ESTÉTICA Y SALUDO CORPORAL",40321:"EDUCACIÓN SECUNDARIA DE INFORMÁTICA",40322:"EDUCACIÓN SECUNDARIA DE MÁQUINAS, HERRAMIENTAS Y SISTEMAS DE CONTROL",40323:"EDUCACIÓN SECUNDARIA DE OFIMÁTICA",40324:"EDUCACIÓN SECUNDARIA DE PECUARIA",40325:"EDUCACIÓN SECUNDARIA DE PESCA",40326:"EDUCACIÓN SECUNDARIA DE PREPARACIÓN Y CONSERVACIÓN DE ALIMENTOS",40327:"EDUCACIÓN SECUNDARIA DE PREPARACIÓN, CONSERVACIÓN E INDUSTRIALIZACIÓN DE ALIMENTOS AGRÍCOLAS",40328:"EDUCACIÓN SECUNDARIA DE PROCESAMIENTO DE PRODUCTOS PESQUEROS",40329:"EDUCACIÓN SECUNDARIA DE SILVICULTURA",40330:"EDUCACIÓN SECUNDARIA DE TURISMO",4021:"EDUCACIÓN FÍSICA",5011:"EDUCACIÓN ESPECIAL Auditiva y Lenguaje",2012:"EDUCACIÓN BÁSICA PARA ADULTOS PRIMARIA",3501:"EDUCACIÓN BÁSICA PARA ADULTOS SECUNDARIA",2013:"MISIONES CULTURALES",40331:"EDUCACIÓN SECUNDARIA Preparación, Conservación e Industrialización de Alimentos Pecuarios (Cárnicos)",5012:"EDUCACIÓN ESPECIAL Intelectual",5013:"EDUCACIÓN ESPECIAL Motriz",5014:"EDUCACIÓN ESPECIAL Psicologia Educativa",5015:"EDUCACIÓN ESPECIAL Visual",5016:"EDUCACIÓN ESPECIAL Especial",8013:"EDUCACIÓN ESPECIAL Acompañante de Música",8010:"EDUCACIÓN PREESCOLAR Acompañante de Música",40332:"EDUCACIÓN SECUNDARIA Preparación, Conservación e Industrialización de Alimentos Pecuarios (Lácteos)",40333:"EDUCACIÓN SECUNDARIA Preparación, Conservación e Industrialización de Alimentos (A,C y L)",8034:"EDUCACIÓN PREESCOLAR Maestro de Taller de Lectura y Escritura",8011:"EDUCACIÓN PRIMARIA Maestro de Enseñanza Artística",8040:"EDUCACIÓN PRIMARIA Maestro de Taller",8035:"EDUCACIÓN PRIMARIA Maestro de Taller de Lectura y Escritura",8020:"EDUCACIÓN SECUNDARIA Maestro de Aula de Medios",8036:"EDUCACIÓN SECUNDARIA Maestro de Taller de Lectura y Escritura",8012:"EDUCACIÓN PRIMARIA INDÍGENA Maestro de Música",8043:"EDUCACIÓN INDÍGENA Maestro de Taller",8042:"EDUCACIÓN ESPECIAL Maestro de Taller"}
#Examenes= {105:"EDUCACIÓN PREESCOLAR INDÍGENA",205:"EDUCACIÓN PRIMARIA INDÍGENA",9002:"EDUCACIÓN SECUNDARIA DE ASIGNATURA ESTATAL"}
#Examenes= {9002:"EDUCACIÓN SECUNDARIA DE ASIGNATURA ESTATAL"}

D105 ={1:[],2:[["021050011","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco Alto"],["021050021","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco Bajo"],["021050041","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco (Guerrero)"]], 3:[], 4:["041050072","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Maya"], 5:[], 6:[], 7:[["071050081","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Ch ol"],["071050082","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Ch ol"],["071050091","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mam"],["071050111","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tseltal"],["071050112","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tseltal"],["071050121","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tsotsil"],["071050122","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tsotsil"],["071050131","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Zoque"],["071050132","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Zoque"]], 8:[], 9:[], 10:["101050141","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tepehuano del sur"], 11:[["111050161","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Otomí"],["111050162","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Otomí"]], 12:[["121050171","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Amuzgo"],["121050172","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Amuzgo"],["121050181","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco"],["121050182","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco"],["121050191","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["121050192","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["121050201","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tlapaneco"],["121050202","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tlapaneco"]], 13:[["131050211","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["131050212","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["131050221","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Otomí Valle del Mezquital"],["131050222","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Otomí Valle del Mezquital"]], 14:[["141050231","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Huichol"],["141050241","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"]], 15:[["151050251","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mazahua"],["151050261","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["151050271","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Otomí"]], 16:["161050301","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Tarasco"], 17:[["171050311","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"]], 18:[["181050321","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Cora"],["181050331","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Huichol"]], 19:["191050311","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl de Morelos"], 20:[], 21:[["211050661","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mazateco Mazatzongo"],["211050671","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco Tepexi de Rodriguez"],["211050672","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mixteco Tepexi de Rodriguez"],["211050681","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Ahuacatlan"],["211050691","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Ajalpan, Cinco Señores"],["211050711","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Ayotoxco"],["211050721","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Chichiquila"],["211050731","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Chilchotla"],["211050741","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Cuacuila"],["211050742","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Cuacuila"],["211050751","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Del Valle"],["211050761","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Hueyapan"],["211050771","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Naupan"],["211050772","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Naupan"],["211050781","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl San Miguel Canoa"],["211050782","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl San Miguel Canoa"],["211050791","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl San Miguel Eloxochitlán"],["211050801","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl San Miguel Tzinacapan"],["211050811","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Teopantlan, Izucar de Matamoros"],["211050821","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Tepezintla"],["211050841","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Tetela de Ocampo"],["211050851","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Teziutlán"],["211050861","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Tlatlauquitepec"],["211050871","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Tepetzintan"],["211050881","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Zacapoaxtla"],["211050891","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl Zoquiapan"],["211050931","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Popoloca San Marcos Tlacoyalco"],["211050941","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco Amixtlan"],["211050951","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco Hermenegildo Galeana"],["211050961","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco Huehuetla"],["211050962","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco Huehuetla"],["211050971","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco San Pedro Petlacotla"],["211050981","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco Tepango"]], 22:["221050991","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Otomí"], 23:[["231051001","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Maya"],["231051002","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Maya"]], 24:[["241051011","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Huasteco"],["241051012","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Huasteco"],["241051021","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["241051022","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"],["241051031","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Pame"]], 25:["251051041","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mayo"],26:[["261051051","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mayo"],["261051052","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Mayo"]], 27:[["271051071","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Ch ol"],["271051081","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Chontal"]],28:[],29:["291051091","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl"], 30: [["301051111","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Náhuatl del centro"],["301051141","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Totonaco"]], 31:[["311051151","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Maya"],["311051152","EDUCACIÓN PREESCOLAR INDÍGENA Lengua Maya"]], 32:[]}
D9002 = {1:[["019000011","ASIGNATURA ESTATAL Educación ambiental para la sustentabilidad en Aguascalientes"],["019000021","ASIGNATURA ESTATAL Formación ciudadana para una cultura de la legalidad en Aguascalientes"]],2:["029000031","ASIGNATURA ESTATAL Formación ciudadana democrática para una Cultura de la legalidad. Baja California"],3:[["039000041","ASIGNATURA ESTATAL Jóvenes sudcalifornianos por una cultura de la sustentabilidad ambiental"],["039000051","ASIGNATURA ESTATAL Formación ciudadana. Construyendo una cultura de la democracia y la legalidad en Baja California Sur"]],4:["049000062","ASIGNATURA ESTATAL Educación ambiental en el estado de Campeche"],5:[["059000071","ASIGNATURA ESTATAL Historia de Coahuila"],["059000072","ASIGNATURA ESTATAL Historia de Coahuila"]],6:["069000082","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Colima"],7:[],8:[["089000091","ASIGNATURA ESTATAL Historia de Chihuahua"],["089000092","ASIGNATURA ESTATAL Historia de Chihuahua"]],9:[["099000101","ASIGNATURA ESTATAL Sexualidad y Equidad de Género en el Distrito Federal"],["099000102","ASIGNATURA ESTATAL Sexualidad y Equidad de Género en el Distrito Federal"]],10:[["109000111","ASIGNATURA ESTATAL Cultura del agua para la sustentabilidad en Durango"],["109000121","ASIGNATURA ESTATAL Cultura de prevención y autocuidado de los adolescentes en Durango"],["109000122","ASIGNATURA ESTATAL Cultura de prevención y autocuidado de los adolescentes en Durango"],["109000131","ASIGNATURA ESTATAL Educación sexual y proyecto de vida de los adolescentes de Durango"],["109000141","ASIGNATURA ESTATAL La formación ciudadana para una convivencia democratica en el marco de una cultura de la legalidad en el estado de Durango."]],11:[["119000151","ASIGNATURA ESTATAL Formación ciudadana para adolescentes de Guanajuato."],["119000152","ASIGNATURA ESTATAL Formación ciudadana para adolescentes de Guanajuato."]],12:[],13:[],14:[["149000161","ASIGNATURA ESTATAL Educación ambiental, adolescentes y sustentabilidad en Jalisco."],["149000162","ASIGNATURA ESTATAL Educación ambiental, adolescentes y sustentabilidad en Jalisco."],["149000171","ASIGNATURA ESTATAL Historia de Jalisco"],["149000181","ASIGNATURA ESTATAL Formación Ciudadana democrática para una cultura de la Legalidad Jalisco"],["149000182","ASIGNATURA ESTATAL Formación Ciudadana democrática para una cultura de la Legalidad Jalisco"]],15:[["159000191","ASIGNATURA ESTATAL Patrimonio cultural y natural del Estado de México"],["159000201","ASIGNATURA ESTATAL Ne zakjü ñe k o pãrãji ne jñaa ñe ko kjijñiji ne jñatjo. Vida y conocimiento de la lengua y cultura Mazahua"],["159000211","ASIGNATURA ESTATAL Formación ciudadana para adolescentes mexiquenses"]],16:[["169000221","ASIGNATURA ESTATAL Educación ambiental para la sustentabilidad en Michoacán"],["169000231","ASIGNATURA ESTATAL Sexualidad y equidad de genero en Michoacán: Una mirada a nuestros campos desde la igualidad."],["169000232","ASIGNATURA ESTATAL Sexualidad y equidad de genero en Michoacán: Una mirada a nuestros campos desde la igualidad."]],17:[["179000241","ASIGNATURA ESTATAL Formación ciudadana de los adolescentes en el estado de Morelos"],["179000242","ASIGNATURA ESTATAL Formación ciudadana de los adolescentes en el estado de Morelos"]],18:[["189000251","ASIGNATURA ESTATAL Formación de ambientes protectores para la adolescencia nayarita"],["189000252","ASIGNATURA ESTATAL Formación de ambientes protectores para la adolescencia nayarita"],["189000262","ASIGNATURA ESTATAL Adolescentes nayaritas construyendo una educación sexual desde un enfoque de equidad y genero."]],19:[["199000271","ASIGNATURA ESTATAL Historia de Nuevo León"],["199000281","ASIGNATURA ESTATAL La formación ciudadana para una convivencia democratica en el marco de una cultura de la legalidad. Nuevo León"]],20:[["209000291","ASIGNATURA ESTATAL Patrimonio cultural y natural del estado de Oaxaca"],["209000302","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Oaxaca"]],21:[["219000312","ASIGNATURA ESTATAL Patrimonio cultural y natural de Puebla"],["219000321","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Puebla"],["219000322","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Puebla"]],22:["229000331","ASIGNATURA ESTATAL Patrimonio cultural y natural en Querétaro"],23:[["239000341","ASIGNATURA ESTATAL Educación y cultura ambiental para la sustentabilidad en Quintana Roo"],["239000351","ASIGNATURA ESTATAL Ambientes de protección para los adolescentes de Quintana Roo"],["239000352","ASIGNATURA ESTATAL Ambientes de protección para los adolescentes de Quintana Roo"],["239000361","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Quintana Roo"],["239000362","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Quintana Roo"]],24:[],25:[["259000371","ASIGNATURA ESTATAL Historia de Sinaloa"],["259000381","ASIGNATURA ESTATAL Formación ciudadana y cultura de la legalidad en Sinaloa"]],26:[["269000391","ASIGNATURA ESTATAL El autocuidado en los adolescentes sonorenses"],["269000392","ASIGNATURA ESTATAL El autocuidado en los adolescentes sonorenses"],["269000401","ASIGNATURA ESTATAL (Lengua y cultura del Pueblo Yaqui. Sonora )"],["269000411","ASIGNATURA ESTATAL Formación ciudadana para una convivencia democrática Sonora"]],27:[["279000421","ASIGNATURA ESTATAL Educación ambiental para la sustentabilidad en Tabasco"],["279000431","ASIGNATURA ESTATAL Patrimonio cultural y natural de los tabasqueños"],["279000441","ASIGNATURA ESTATAL Geografía de Tabasco"],["279000451","ASIGNATURA ESTATAL Historia de Tabasco"],["279000461","ASIGNATURA ESTATAL Cultura de la legalidad en Tabasco"],["279000462","ASIGNATURA ESTATAL Cultura de la legalidad en Tabasco"]],28:[["289000481","ASIGNATURA ESTATAL El adolescente y su sexualidad responsable en Tamaulipas"],["289000492","ASIGNATURA ESTATAL Formación ciudadana democrática para una cultura de la legalidad en Tamaulipas"],["289000471","ASIGNATURA ESTATAL Educación ambiental para la sustentabilidad en Tamaulipas"]],29:[["299000501","ASIGNATURA ESTATAL Educación ambiental para el Desarrollo sustentable en Tlaxcala"],["299000511","ASIGNATURA ESTATAL Historia de Tlaxcala"]],30:[["309000521","ASIGNATURA ESTATAL Tlajlamikilitli uan Nauatlajtoli tlen altepetl Zongolica. Lengua y Cultura Indígena de los Nahuas de la Región de Zongolica"],["309000531","ASIGNATURA ESTATAL Educación sexual integral hacia la formación de adolescentes responsables en Veracruz"],["309000541","ASIGNATURA ESTATAL Formación ciudadana en el marco de una cultura de la legalidad. Veracruz"]],31:["319000552","ASIGNATURA ESTATAL Patrimonio cultural y natural de Yucatán"],32:["329000562","ASIGNATURA ESTATAL Jóvenes zacatecanos por una cultura de la legalidad"]}
D205 = { 1:[],2:[["022050011","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco Alto"],["022050021","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco Bajo"],["022050031","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco de la Costa"],["022050041","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco (Guerrero)"],["022050051","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tarasco"],["022050061","EDUCACIÓN PRIMARIA INDÍGENA Lengua Zapoteco"]],3:[],4:[["042050071","EDUCACIÓN PRIMARIA INDÍGENA Lengua Maya"],["042050072","EDUCACIÓN PRIMARIA INDÍGENA Lengua Maya"]],5:[],6:[],7:[["072050081","EDUCACIÓN PRIMARIA INDÍGENA Lengua Ch ol"],["072050082","EDUCACIÓN PRIMARIA INDÍGENA Lengua Ch ol"],["072050091","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mam"],["072050101","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tojolabal"],["072050102","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tojolabal"],["072050111","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tseltal"],["072050112","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tseltal"],["072050121","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tsotsil"],["072050122","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tsotsil"],["072050131","EDUCACIÓN PRIMARIA INDÍGENA Lengua Zoque"]],8:[],9:[],10:["102050141","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tepehuano del sur"],11:[["112050151","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["112050161","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí"]],12:[["122050171","EDUCACIÓN PRIMARIA INDÍGENA Lengua Amuzgo"],["122050181","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco"],["122050182","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco"],["122050191","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["122050192","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["122050201","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tlapaneco"],["122050202","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tlapaneco"]],13:[["132050211","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["132050212","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["132050221","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí Valle del Mezquital"],["132050222","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí Valle del Mezquital"]],14:[["142050231","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huichol"],["142050232","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huichol"],["142050241","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"]],15:[["152050251","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mazahua"],["152050261","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["152050262","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["152050271","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí"]],16:[["162050281","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["162050291","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí"],["162050301","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tarasco"]],17:["172050311","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],18:[["182050321","EDUCACIÓN PRIMARIA INDÍGENA Lengua Cora"],["182050331","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huichol"],["182050332","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huichol"],["182050341","EDUCACIÓN PRIMARIA INDÍGENA Lengua Tepehuano del sur"]],19:["192050351","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl del Norte"],20:[["202050362","EDUCACIÓN PRIMARIA INDÍGENA Lengua Amuzgo"],["202050372","EDUCACIÓN PRIMARIA INDÍGENA Lengua CHATINO Central"],["202050382","EDUCACIÓN PRIMARIA INDÍGENA Lengua CHATINO Oriental Bajo"],["202050392","EDUCACIÓN PRIMARIA INDÍGENA Lengua CHATINO"],["202050402","EDUCACIÓN PRIMARIA INDÍGENA Lengua Chinanteco Sureste Medio"],["202050412","EDUCACIÓN PRIMARIA INDÍGENA Lengua Chinanteco"],["202050422","EDUCACIÓN PRIMARIA INDÍGENA Lengua Cuicateco"],["202050432","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huave"],["202050442","EDUCACIÓN PRIMARIA INDÍGENA Lengua MAZATECO  Central"],["202050452","EDUCACIÓN PRIMARIA INDÍGENA Lengua MAZATECO  De Puebla"],["202050461","EDUCACIÓN PRIMARIA INDÍGENA Lengua MAZATECO"],["202050462","EDUCACIÓN PRIMARIA INDÍGENA Lengua MAZATECO"],["202050472","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXE Alto del Centro"],["202050482","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXE Medio del Este"],["202050491","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXE"],["202050492","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXE"],["202050502","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO  ALTO"],["202050512","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO COSTA"],["202050522","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO  Ixtayutla"],["202050531","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO San Mateo Peñasco"],["202050542","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO Noroeste"],["202050552","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO Oeste Central"],["202050562","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO Santa María Peñoles"],["202050572","EDUCACIÓN PRIMARIA INDÍGENA Lengua MIXTECO Sierra sur"],["202050582","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl del Sur"],["202050592","EDUCACIÓN PRIMARIA INDÍGENA Lengua TRIQUI BAJO"],["202050602","EDUCACIÓN PRIMARIA INDÍGENA Lengua ZAPOTECO COSTA ESTE"],["202050612","EDUCACIÓN PRIMARIA INDÍGENA Lengua ZAPOTECO Planicie costera"],["202050622","EDUCACIÓN PRIMARIA INDÍGENA Lengua ZAPOTECO SERRANO"],["202050632","EDUCACIÓN PRIMARIA INDÍGENA Lengua ZAPOTECO Sierra Sur"],["202050642","EDUCACIÓN PRIMARIA INDÍGENA Lengua ZAPOTECO"],["202050651","EDUCACIÓN PRIMARIA INDÍGENA Lengua Zoque"],["202050652","EDUCACIÓN PRIMARIA INDÍGENA Lengua Zoque"]],21:[["212050661","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mazateco Mazatzongo"],["212050671","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mixteco Tepexi de Rodriguez"],["212050681","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Ahuacatlan"],["212050682","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Ahuacatlan"],["212050691","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Ajalpan, Cinco Señores"],["212050701","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Alcomunga"],["212050702","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Alcomunga"],["212050711","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Ayotoxco"],["212050721","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Chichiquila"],["212050731","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Chilchotla"],["212050741","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Cuacuila"],["212050751","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Del Valle"],["212050752","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Del Valle"],["212050761","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Hueyapan"],["212050771","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Naupan"],["212050781","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl San Miguel Canoa"],["212050791","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl San Miguel Eloxochitlán"],["212050801","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl San Miguel Tzinacapan"],["212050821","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Tepezintla"],["212050831","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Tepexi de Rodriguez"],["212050841","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Tetela de Ocampo"],["212050851","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Teziutlán"],["212050861","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Tlatlauquitepec"],["212050871","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Tepetzintan"],["212050881","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Zacapoaxtla"],["212050891","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl Zoquiapan"],["212050901","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí Pahuatlan"],["212050911","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí Pantepec"],["212050921","EDUCACIÓN PRIMARIA INDÍGENA Lengua Popoloca San Felipe Otlaltepec"],["212050931","EDUCACIÓN PRIMARIA INDÍGENA Lengua Popoloca San Marcos Tlacoyalco"],["212050941","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco Amixtlan"],["212050942","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco Amixtlan"],["212050951","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco Hermenegildo Galeana"],["212050961","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco Huehuetla"],["212050971","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco San Pedro Petlacotla"],["212050981","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco Tepango"]],22:["222050991","EDUCACIÓN PRIMARIA INDÍGENA Lengua Otomí"],23:[["232051001","EDUCACIÓN PRIMARIA INDÍGENA Lengua Maya"],["232051002","EDUCACIÓN PRIMARIA INDÍGENA Lengua Maya"]],24:[["242051011","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huasteco"],["242051012","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huasteco"],["242051021","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["242051022","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl"],["242051031","EDUCACIÓN PRIMARIA INDÍGENA Lengua Pame"],["242051032","EDUCACIÓN PRIMARIA INDÍGENA Lengua Pame"]],25:[["252051041","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mayo"],["252051042","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mayo"]],26:[["262051051","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mayo"],["262051052","EDUCACIÓN PRIMARIA INDÍGENA Lengua Mayo"],["262051061","EDUCACIÓN PRIMARIA INDÍGENA Lengua Yaqui"],["262051062","EDUCACIÓN PRIMARIA INDÍGENA Lengua Yaqui"]],27:[["272051071","EDUCACIÓN PRIMARIA INDÍGENA Lengua Ch ol"],["272051081","EDUCACIÓN PRIMARIA INDÍGENA Lengua Chontal"],["272051082","EDUCACIÓN PRIMARIA INDÍGENA Lengua Chontal"]],28:[],29:[],30:[["302051101","EDUCACIÓN PRIMARIA INDÍGENA Lengua Huasteco"],["302051111","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl del centro"],["302051112","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl del centro"],["302051121","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl del Norte"],["302051131","EDUCACIÓN PRIMARIA INDÍGENA Lengua Náhuatl del sur"],["302051141","EDUCACIÓN PRIMARIA INDÍGENA Lengua Totonaco"]],31:[["312051151","EDUCACIÓN PRIMARIA INDÍGENA Lengua Maya"],["312051152","EDUCACIÓN PRIMARIA INDÍGENA Lengua Maya"]],32:[]}


def getbody(Entidad,Convocatoria,Examen,sess, Subprueba = None):
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
	ddlExamen.form().submit()

	if Subprueba is not None:
		#Examen Adicional
		ddlExamenAd = sess.at_xpath('//*[@name="ddl_ExamenAdicional"]')
		ddlExamenAd.set(Subprueba)
	

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
			ddlExamen.form().submit()
			if Subprueba is not None:
				#Examen Adicional
				ddlExamenAd = sess.at_xpath('//*[@name="ddl_ExamenAdicional"]')
				ddlExamenAd.set(Subprueba)
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
		if findtable is None:
			findtable = soup.find('table', id="gvResultadosEvaluacion4")
			tipo = 3
		if findtable is None: tipo = 1

		tables.append(findtable)


	return tables, tipo

def printcsv(tables,Entidad,Convocatoria,Examen,tipo, Subprueba=None):
	#Toma las tablas de la combinacion actual y las escribe en el archivo.
	if Subprueba == None:
		vectordataplace = [Entidad,Convocatoria,Examen]
	else: 
		vectordataplace = [Entidad,Convocatoria,Subprueba]

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
				Subpruebas = None
				if int(keyExamen) == 105:
					Subpruebas = D105[keyEstado]
				elif int(keyExamen) == 205: 
					Subpruebas = D205[keyEstado]
				elif int(keyExamen) ==9002:
					Subpruebas = D9002[keyEstado]

				if Subpruebas == None or Subpruebas == []:
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
				else:
					for parsubprueba in Subpruebas:
						#Obtener las paginas de las tablas
						pages = getbody(keyEstado,keyConvocatoria,keyExamen,sess, parsubprueba[0])

						#Extraer dichas tablas
						tables, tipo = scrappetable(pages)

						#Para la combinacion actual, ¿Hay informacion?
						if tipo==1: 
							print "Sin informacion."
						else:
							print "Imprimiendo."
							printcsv(tables,keyEstado,keyConvocatoria,keyExamen, tipo, parsubprueba[0]) 


#Modificar Archivo para quitar espacios extra.
open("output_clean.csv", "w").write(open("output.csv").read().replace(" ",""))

