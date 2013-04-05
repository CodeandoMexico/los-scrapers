#!/usr/bin/python

"""Parser INEGI

Recibe un TSV de informacion del INEGI y lo transmite hacia
una base de datos PostgreSQL.
http://www3.inegi.org.mx/sistemas/descarga/default.aspx?c=28088

Los nombres de archivos y directorios estan basados en la convencion de nombres
especificada por INEGI
"""

__author__ = "@rafaelcr (Rafael Cardenas)"

import csv
import psycopg2
import subprocess
import sys

class INEGIParser(object):

  def __init__(self, database, user, host, directory):
    self.path = directory.strip('/')
    self.entidad = self.path.split('/')[-1:][0][:-3]
    self.dbconfigure(database, user, host)
    self.parse()
    self.dbclose()

  def dbconfigure(self, database, user, host):
    self.sqlconn = psycopg2.connect("dbname=%s user=%s host=%s" 
      % (database, user, host))
    self.sqlconn.autocommit = True
    self.sql = self.sqlconn.cursor()
    self.sql.execute("CREATE TABLE IF NOT EXISTS entidad (\
      id varchar(2) PRIMARY KEY,\
      nombre varchar);")
    self.sql.execute("CREATE TABLE IF NOT EXISTS municipio (\
      entidad varchar(2) references entidad(id),\
      id varchar(3),\
      nombre varchar,\
      PRIMARY KEY (entidad, id));")
    self.sql.execute("CREATE TABLE IF NOT EXISTS indicador (\
      id bigint PRIMARY KEY,\
      descripcion varchar,\
      notas varchar);")
    self.sql.execute("CREATE TABLE IF NOT EXISTS valor (\
      indicador bigint references indicador(id),\
      municipio varchar(3),\
      entidad varchar(2),\
      anio integer,\
      valor numeric(20,5),\
      unidades varchar,\
      fuente varchar,\
      PRIMARY KEY (indicador, municipio, entidad, anio));")
    self.sql.execute("CREATE TABLE IF NOT EXISTS categoria (\
      id serial,\
      nombre varchar PRIMARY KEY,\
      parent integer);")

  def dbclose(self):
    self.sql.close()
    self.sqlconn.close()

  def parse(self):
    # el csv de nacional no trae las columnas de los anios como las estatales,
    # y no son provistos en ningun archivo
    anio = [1895,1900,1910,1921,1930,1940,1950,1960,1970,1980,1981,1982,1983,
      1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,
      1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010]

    # determinar encoding de csv. algunos malamente no vienen en utf-8
    fenc = subprocess.Popen(["file","--mime-encoding",
      "%s/%sValor.tsv" % (self.path, self.entidad)], stdout=subprocess.PIPE)
    self.encoding = fenc.stdout.read().split(':')[1].strip()

    print 'Parseando archivos para entidad %s...' % (self.entidad)
    print "Procesando CSV 1/4..."
    with open("%s/%sValor.tsv" % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l == 0 and (not line[0].isdigit()): # corregir si viene con columnas
          continue
        self.wentidad(line[0],line[1])
        self.wmunicipio(line[0],line[2],line[3])
        self.windicador(line[7],line[8])
        self.wcategoria(line[4],"")
        self.wcategoria(line[5],line[4])
        self.wcategoria(line[6],line[5])
        for i, a in enumerate(line[9:]):
          if a:
            self.wvalor(line[7],line[2],line[0],anio[i],a)

    print "Procesando CSV 2/4..."
    with open("%s/%sNotas.tsv" % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l == 0: # ignorar nombres de columnas
          continue
        # TODO: hay lineas que empiezan sin ID, son linebreaks de la anterior.
        # ademas hay algunos IDs repetidos que su desc debe ser concatenada
        if line[0].isdigit():
          self.wnota(line[0],line[2])

    print "Procesando CSV 3/4..."
    with open("%s/%sUnidadMedida.tsv" % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l == 0 and (not line[0].isdigit()):
          continue
        for i, a in enumerate(line[9:]):
          if a:
            self.wunidades(line[7],line[2],line[0],anio[i],a)

    print "Procesando CSV 4/4..."
    with open("%s/%sFuente.tsv" % (self.path, self.entidad)) as inegi_tsv:
      for l, line in enumerate(csv.reader(inegi_tsv, dialect="excel-tab")):
        if l == 0 and (not line[0].isdigit()):
          continue
        for i, a in enumerate(line[9:]):
          if a:
            self.wfuente(line[7],line[2],line[0],anio[i],a)

  def strdecode(self, s):
    if not self.encoding == "utf-8":
      return s.decode("latin1")
    else:
      return s

  def wvalor(self, indicador, municipio, entidad, anio, valor):
    self.sql.execute("INSERT INTO valor \
      (indicador,municipio,entidad,anio,valor) VALUES (%s,%s,%s,%s,%s);", 
      (int(indicador),municipio,entidad,anio,float(valor)))

  def wunidades(self, indicador, municipio, entidad, anio, unidades):
    self.sql.execute("UPDATE valor SET unidades=%s WHERE indicador=%s \
      AND municipio=%s AND entidad=%s AND anio=%s;", 
      (self.strdecode(unidades),int(indicador),municipio,entidad,anio))

  def wfuente(self, indicador, municipio, entidad, anio, fuente):
    self.sql.execute("UPDATE valor SET fuente=%s WHERE indicador=%s \
      AND municipio=%s AND entidad=%s AND anio=%s;", 
      (self.strdecode(fuente).strip(),int(indicador),municipio,entidad,anio))

  def wentidad(self, eid, nombre):
    try:
      self.sql.execute("INSERT INTO entidad (id,nombre) VALUES (%s,%s);",
          (eid,self.strdecode(nombre)))
    except Exception, e:
      pass
        
  def wmunicipio(self, entidad, mid, nombre):
    try:
      self.sql.execute("INSERT INTO municipio (entidad,id,nombre) \
        VALUES (%s,%s,%s);", (entidad,mid,self.strdecode(nombre)))
    except Exception, e:
      pass

  def windicador(self, iid, descripcion):
    try:
      self.sql.execute("INSERT INTO indicador (id,descripcion) VALUES \
        (%s,%s);", (int(iid),self.strdecode(descripcion)))
    except Exception, e:
      pass

  def wnota(self, iid, notas):
    self.sql.execute("UPDATE indicador SET notas=%s WHERE id=%s;", 
      (self.strdecode(notas),int(iid)))

  def wcategoria(self, nombre, parent):
    if nombre:
      self.sql.execute("SELECT * FROM categoria WHERE nombre=%s", 
        (self.strdecode(nombre),))
      if not self.sql.fetchone():
        if parent:
          self.sql.execute("SELECT * FROM categoria WHERE nombre=%s", 
            (self.strdecode(parent),))
          parent = int(self.sql.fetchone()[0])
        else:
          parent = 0 
        self.sql.execute("INSERT INTO categoria (nombre,parent) VALUES \
          (%s,%s);", (self.strdecode(nombre),parent))

def main():
  args = sys.argv[1:]
  usage = "usage: inegi_sql.py -d[database] -u[user] -h[host] [directories...]"
  if len(args) < 4:
    print usage
    sys.exit(1)

  database = args[0][2:]
  del args[0]
  user = args[0][2:]
  del args[0]
  host = args[0][2:]
  del args[0]

  print '* Parser INEGI *'
  for directory in args:
    p = INEGIParser(database, user, host, directory)

if __name__ == '__main__':
  main()