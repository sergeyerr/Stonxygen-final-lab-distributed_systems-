$:.unshift File.expand_path("../../lib", __FILE__)

require "stock"
require "json"

puts Stock.all_available.to_json
puts Stock.with_codes(["A", "B"]).to_json
