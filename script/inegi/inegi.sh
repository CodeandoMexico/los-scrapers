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
curl -O -J -# $BASEPATH%2f01+Aguascalientes%2f01_Aguascalientes_tsv.zip
curl -O -J -# $BASEPATH%2f02+Baja+California%2f02_BajaCalifornia_tsv.zip
curl -O -J -# $BASEPATH%2f03+Baja+California+Sur%2f03_BajaCaliforniaSur_tsv.zip
curl -O -J -# $BASEPATH%2f04+Campeche%2f04_Campeche_tsv.zip
curl -O -J -# $BASEPATH%2f05+Coahuila+de+Zaragoza%2f05_CoahuiladeZaragoza_tsv.zip
curl -O -J -# $BASEPATH%2f06+Colima%2f06_Colima_tsv.zip
curl -O -J -# $BASEPATH%2f07+Chiapas%2f07_Chiapas_tsv.zip
curl -O -J -# $BASEPATH%2f08+Chihuahua%2f08_Chihuahua_tsv.zip
curl -O -J -# $BASEPATH%2f09+Distrito+Federal%2f09_DistritoFederal_tsv.zip
curl -O -J -# $BASEPATH%2f10+Durango%2f10_Durango_tsv.zip
curl -O -J -# $BASEPATH%2f11+Guanajuato%2f11_Guanajuato_tsv.zip
curl -O -J -# $BASEPATH%2f12+Guerrero%2f12_Guerrero_tsv.zip
curl -O -J -# $BASEPATH%2f13+Hidalgo%2f13_Hidalgo_tsv.zip
curl -O -J -# $BASEPATH%2f14+Jalisco%2f14_Jalisco_tsv.zip
curl -O -J -# $BASEPATH%2f15+M%e9xico%2f15_Mexico_tsv.zip
curl -O -J -# $BASEPATH%2f16+Michoac%e1n+de+Ocampo%2f16_MichoacandeOcampo_tsv.zip
curl -O -J -# $BASEPATH%2f17+Morelos%2f17_Morelos_tsv.zip
curl -O -J -# $BASEPATH%2f18+Nayarit%2f18_Nayarit_tsv.zip
curl -O -J -# $BASEPATH%2f19+Nuevo+Le%f3n%2f19_NuevoLeon_tsv.zip
curl -O -J -# $BASEPATH%2f20+Oaxaca%2f20_Oaxaca_tsv.zip
curl -O -J -# $BASEPATH%2f21+Puebla%2f21_Puebla_tsv.zip
curl -O -J -# $BASEPATH%2f22+Quer%e9taro%2f22_Queretaro_tsv.zip
curl -O -J -# $BASEPATH%2f23+Quintana+Roo%2f23_QuintanaRoo_tsv.zip
curl -O -J -# $BASEPATH%2f24+San+Luis+Potos%ed%2f24_SanLuisPotosi_tsv.zip
curl -O -J -# $BASEPATH%2f25+Sinaloa%2f25_Sinaloa_tsv.zip
curl -O -J -# $BASEPATH%2f26+Sonora%2f26_Sonora_tsv.zip
curl -O -J -# $BASEPATH%2f27+Tabasco%2f27_Tabasco_tsv.zip
curl -O -J -# $BASEPATH%2f28+Tamaulipas%2f28_Tamaulipas_tsv.zip
curl -O -J -# $BASEPATH%2f29+Tlaxcala%2f29_Tlaxcala_tsv.zip
curl -O -J -# $BASEPATH%2f30+Veracruz+de+Ignacio+de+la+Llave%2f30_VeracruzdeIgnaciodelaLlave_tsv.zip
curl -O -J -# $BASEPATH%2f31+Yucat%e1n%2f31_Yucatan_tsv.zip
curl -O -J -# $BASEPATH%2f32+Zacatecas%2f32_Zacatecas_tsv.zip

echo "Descomprimiendo archivos..."
for z in *.zip; do
  dir=${z:0:(${#z}-4)}
  mkdir $dir
  unzip $z -d $dir
  rm $z
done

echo "Comenzando parser..."
cd ..
python parse.py --dbwrite datos/*