require 'rubygems'
require 'open-uri'
require 'hpricot'
require 'optparse'
require 'json'

url = "http://curul501.org/partido_politico/"
members = []

(1..6).each do |i|
  open("#{url}#{i}", "User-Agent" => "Ruby/#{RUBY_VERSION}") { |f| 
    response = f.read
    member = {} 
    doc = Hpricot(response)
    (doc/"div.congresista").each do |div| 
      member[:avatar] = (div/"ul/li").first.at("img").attributes['src']
      member[:name] = (div/"ul/li.nombre/a").inner_html
      members << member
    end
  }
end

options = {}
OptionParser.new do |opts| 
  opts.banner = "Usage: example.rb [options]"
  opts.on("--format json") do |f| 
    options[:format] = f 
  end
end.parse!

# Deliver results
if options[:format] == "json"
  members.to_json
else 
  puts "Se descargaron datos de #{members.length} miembros del congreso en Curul501.org"
end
