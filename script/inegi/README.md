INEGI Parser
============

Script de Python que toma los archivos TSV de INEGI para todas las Entidades
Federativas de México, los parsea y los transmite hacia una base de datos
MongoDB (noSQL) o PostgreSQL (SQL).  
Los archivos son tomados de la sección de 
[Descarga Masiva](http://www3.inegi.org.mx/sistemas/descarga/default.aspx?c=28088) 
de la INEGI por un shell script que los descarga y descomprime 
automáticamente.  

Dependencias
------------
* Python 2.7.2
* [MongoDB 2.4.1](http://www.mongodb.org/downloads)
* [pymongo 2.5](http://api.mongodb.org/python/current/)
* [PostgreSQL](http://www.postgresql.org/) 9.1.5
* [psycopg2](http://initd.org/psycopg/) 2.4.6

Para instalar las dependencias usando pip, puedes correr:

    pip install -r requirements.txt

Ejemplo de uso
------------

Para correr el proceso completo, primero hay que ejecutar nacional.sh o estatal.sh,
estos scripts bajan y descomprimen los archivos de todos los estados o el agregado
nacional del INEGI. 

    ./estatal.sh
    ./nacional.sh

Después se corre el parser (para SQL o noSQL) individualmente:

    ./inegi_nosql.py --dbwrite datos/*
    ./inegi_sql.py -dinegi -urafaelcr -hlocalhost datos/*

Con estas opciones, el script procesa todas las subcarpetas con la notación de
nombre XX\_EEEEEE\_tsv, en donde XX es la clave del estado de 2 dígitos y EEEEEE
es el nombre del estado bajo los 
[estandares de nombramiento del INEGI](http://www3.inegi.org.mx/sistemas/descarga/descargaArchivo.aspx?file=Por+entidad+federativa%2fDescripcion_archivos_txt.txt). 
El repositorio incluye los datos de Nuevo León para pruebas.

Base de Datos (noSQL)
------------

Cada uno de los documentos JSON escritos hacia la BD consiste
en datos de un *indicador* en cierto municipio del país a lo largo del tiempo.
Los [indicadores de la INEGI](http://www3.inegi.org.mx/sistemas/descarga/descargaArchivo.aspx?file=Por+entidad+federativa%2fTabla_de_contenidos_pdf.pdf) 
cubren estadísticas de población, salud, infraestructura, comunicación, agricultura,
etc. Ya que los datos se encuentran en MongoDB, se pueden hacer consultas muy
poderosas con mucha facilidad.  

### Ejemplos

Encontrar el estado que haya beneficiado a la mayor cantidad de familias con el
seguro popular en el 2006 (R: Guanajuato):  

    db.entidades.find({
      "Id_Indicador": "1004000045", 
      "2006.valor":{$ne:null}, 
      "Cve_Municipio":"000"
      }).sort({"2006.valor": -1}).limit(1).pretty()

    {
      "_id" : ObjectId("5158b783b2a757fb57053a3a"),
      "Desc_Municipio" : "Total estatal",
      "Indicador" : "Familias beneficiadas por el seguro popular",
      "Cve_Entidad" : "11",
      "Id_Indicador" : "1004000045",
      "Tema_nivel_3" : "Derechohabiencia y uso de servicios de salud",
      "Tema_nivel_2" : "Salud",
      "Tema_nivel_1" : "Sociedad y Gobierno",
      "2006" : {
        "fuente" : "Instituto de Salud del Gobierno del Estado.",
        "valor" : 504209
      },
      "2007" : {
        "fuente" : "Instituto de Salud del Gobierno del Estado.",
        "valor" : 568573
      },
      "2005" : {
        "fuente" : "Instituto de Salud del Gobierno del Estado.",
        "valor" : 397341
      },
      "Desc_Entidad" : "Guanajuato",
      "2008" : {
        "fuente" : "Instituto de Salud del Gobierno del Estado.",
        "valor" : 620299
      },
      "2009" : {
        "fuente" : "Instituto de Salud del Gobierno del Estado.",
        "valor" : 676987
      },
      "Cve_Municipio" : "000"
    }

Base de Datos (SQL)
------------

El esquema de las tablas (con ejemplos) es el siguiente:

### indicador

         id     |              descripcion                  |  notas   
    ------------+-------------------------------------------+----------
     1009000001 | Superficie sembrada total                 |
     1009000002 | Superficie sembrada de alfalfa verde      |
     1009000003 | Superficie sembrada de avena forrajera    |
     1009000004 | Superficie sembrada de chile verde        |
     1009000005 | Superficie sembrada de frijol             |
     1009000006 | Superficie sembrada de maíz grano         |
     1009000007 | Superficie sembrada de pastos             |
     1009000008 | Superficie sembrada de sorgo grano        |
     1009000009 | Superficie sembrada de tomate rojo        |

### entidad

     id |     nombre     
    ----+----------------
     06 | Colima
     01 | Aguascalientes

### municipio

     entidad | id  |      nombre      
    ---------+-----+------------------
     06      | 000 | Total estatal
     06      | 008 | Minatitlán
     06      | 009 | Tecomán
     06      | 001 | Armería
     06      | 010 | Villa de Álvarez
     06      | 002 | Colima
     06      | 003 | Comala
     06      | 996 | No especificado
     06      | 997 | Otros estados
     06      | 004 | Coquimatlán

### categoria

     id |                    nombre                   | parent 
    ----+---------------------------------------------+--------
      1 | Economía                                    |      0
      2 | Actividades primarias                       |      1
      3 | Agricultura                                 |      2
      4 | Explotación forestal                        |      2
      5 | Ganadería                                   |      2
      6 | Pesca                                       |      2
      7 | Actividades secundarias                     |      1
      8 | Construcción                                |      7
      9 | Electricidad y Agua                         |      7
     10 | Minería                                     |      7
     11 | Actividades terciarias                      |      1
     12 | Actividades gubernamentales                 |     11
     13 | Comercio                                    |     11

### valor

     indicador  | municipio | entidad | anio |     valor      | unidades  | fuente               
    ------------+-----------+---------+------+----------------+-----------+----------------------
     1005000078 | 006       | 06      | 2001 |       91.10000 |           | Instituto de Educa...
     1009000001 | 000       | 06      | 1998 |   167886.00000 | Hectáreas | Secretaría de Agri...
     1009000001 | 000       | 06      | 2001 |   159068.00000 | Hectáreas | Secretaría de Agri...
     1009000001 | 000       | 06      | 2006 |   161638.00000 | Hectáreas | Secretaría de Agri...

Funcionalidad pendiente
------------
* Incluir datos de los TSVs de "Notas por valor del indicador"
* Corregir errores en TSVs que vienen con linebreaks extra que rompen el formato
* Por el momento la escritura a la BD en noSQL hace solo "append", debe 
sobreescribir valores anteriores que empaten.
* En PostgreSQL, falta agregar parametro de password en la connection string. 
Funciona ahorita con usuarios sin password.
