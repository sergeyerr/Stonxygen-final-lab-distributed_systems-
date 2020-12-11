$:.unshift File.expand_path("../../lib", __FILE__)

require "stock"
require "json"

stocks = Stock.all_available
puts stocks.to_json
puts Stock.with_codes(["A", "B"]).to_json

s = stocks[0]
puts s.statistic("criminal")
