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
    monto = div.content.match(/monto de \$\s*(\d+([.,]\d+)*)/)[1]
    razon = div.css('a').first.content
    fecha = div.content.match(/realizó el (.*) con el proveedor/)[1]
    id    = div.content.match(/con clave (.*) con el objeto/)[1]
    dependencia = div.css('.tit-info').last.content
    proveedor   = div.content.match(/proveedor (.*) un /)[1]
    fecha.gsub!(' ', '')
    datos = { id:id, fecha: fecha, razon: razon, monto: monto,
              dependencia: dependencia, proveedor: proveedor}
    puts datos
    contratos << datos
  end
end

contratos.each do |c|
  puts c.inspect
end
