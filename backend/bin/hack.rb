$:.unshift File.expand_path("../../lib", __FILE__)

require "json"
require "auth"
require "user"

puts User.register("nem", "pisswasser").to_json
