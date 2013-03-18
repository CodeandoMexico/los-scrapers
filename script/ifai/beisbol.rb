#!/bin/env ruby
# encoding: utf-8

require 'open-uri'
require 'nokogiri'
require 'logger'
require 'httparty'

log = Logger.new('log/ifai.log')
contratos = []
base_url = 'http://portaltransparencia.gob.mx/buscador/search/search.do?'
content_available = true
page = 0
cookie = ''

while content_available do
  page += 1

  # HACK: Por alguna razón la primera página debe de ser cargada diferente que
  # las demás.
  if page == 1
    url =  "#{base_url}query=&idDependenciaZoom=&method=search"
    url << '&siglasDependencia=&idFraccionZoom=XIII&searchBy=1'
  else
    url =  "#{base_url}method=paginas&fstNavegadores=&nuevaPagina=#{page}"
    url << '&idDependenciaZoom=&searchBy=1&idFraccionZoom=XIII'
  end

  log.info("Opening #{url}")
  response = HTTParty.get(url, headers: { 'Cookie' => cookie })
  new_cookie = response.headers['set-cookie']
  cookie = new_cookie if new_cookie && new_cookie.size > 0

  doc = Nokogiri::HTML(response.body)
  content_available = doc.css('div#info').size > 0

  doc.css('div#info').each do |div|
    # Extracción
    monto = div.content.match(/monto de \$( *)([0-9,.]*) ([A-Z]*) el/)
    id    = div.content.match(/con clave (.*) con el objeto/)
    proveedor   = div.content.match(/proveedor (.*) un /)
    fecha = div.content.match(/realizó el (.*) con el proveedor/)
    fecha = div.content.match(/cual iniciará (.*) y concluirá/) if fecha.nil?

    razon = div.css('a').first.content
    dependencia = div.css('.tit-info').last.content

    # Validación y asignación
    unless monto && monto.size == 4
      raise "Error fetching monto from #{div.content} "
    end
    raise "Error fetching razon from #{div.content} " unless razon
    raise "Error fetching id from #{div.content} " unless id
    raise "Error fetching dependencia from #{div.content} " unless dependencia
    raise "Error fetching proveedor from #{div.content} " unless proveedor
    raise "Error fetching fecha from #{div.content} " unless fecha

    moneda = monto[3]
    monto  = monto[2]
    id     = id[1]
    fecha  = fecha[1]
    proveedor = proveedor[1]

    # Transformacion
    fecha.gsub!(' ', '')
    monto.gsub!(' ', '')
    monto.gsub!(',', '')

    datos = { id:id, fecha: fecha, razon: razon, monto: monto, moneda: moneda,
              dependencia: dependencia, proveedor: proveedor}
    puts datos
    contratos << datos
  end
end

contratos.each do |c|
  puts c.inspect
end
