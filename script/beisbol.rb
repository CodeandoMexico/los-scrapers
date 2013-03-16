require 'nokogiri'
require 'open-uri'

contratos = []
url = 'http://portaltransparencia.gob.mx/buscador/search/search.do?query=&idDependenciaZoom=&method=search&siglasDependencia=&idFraccionZoom=XIII&searchBy=1'
# Let the scraping begin
content_available = true
page = 400
while content_available do
  page += 1
  current_page = "#{url}&nuevaPagina=#{page}"
  doc = Nokogiri::HTML(open(current_page))
  puts "Current page #{current_page} has #{doc.css('div#info').size}"
  content_available = doc.css('div#info').size > 0

  doc.css('div#info').each do |div|
    matches = div.content.match(/monto de \$\s*(\d+([.,]\d+)*)/)
    monto = matches[1] unless matches.nil?
    razon = div.css('a').first.content.capitalize
    datos = { razon: razon, monto: monto }
    #puts datos
    contratos << datos
  end
  puts "Done"
end

contratos.each do |c|
  puts "#{c[:monto]} - #{c[:razon]}"
end
