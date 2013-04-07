#!/bin/bash
#
# INEGI cron
# Descarga TSVs desde INEGI, descomprime, y envia a Parser
#
# @rafaelcr (Rafael Cardenas)

echo "Descargando informacion de INEGI..."
DATOSDIR=$(dirname $0)/datos
BASEPATH="http://www3.inegi.org.mx/sistemas/descarga/descargaArchivo.aspx?file=Por+entidad+federativa"

mkdir -p $DATOSDIR
cd $DATOSDIR
curl -O -J -# $BASEPATH%2f00+Nacional%2f00_NacionalyEntidadesFederativas_tsv.zip

echo "Descomprimiendo archivos..."
for z in *.zip; do
  dir=${z:0:(${#z}-4)}
  mkdir $dir
  unzip $z -d $dir
  rm $z
done