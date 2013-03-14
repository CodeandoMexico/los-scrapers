require 'nokogiri'
require 'open-uri'

# Contratos de pemex refinación
contratos = []
url = 'http://portaltransparencia.gob.mx/buscador/search/search.do?query=&idDependenciaZoom=18576&method=search&siglasDependencia=PEMEX+REFINACI%D3N&idFraccionZoom=XIII&searchBy=0'

# Let the scraping begin
(1..9).each do |i|
  doc = Nokogiri::HTML(open("#{url}&nuevaPagina=#{i}"))

  doc.css('div#info').each do |div|
    matches = div.content.match(/monto de \$\s*(\d+([.,]\d+)*)/)
    monto = matches[1] unless matches.nil?
    razon = div.css('a').first.content.capitalize
    contratos << { razon: razon, monto: monto }
  end
end

contratos.each do |c|
  puts "#{c[:monto]} - #{c[:razon]}"
end
