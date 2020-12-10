$:.unshift File.expand_path("../../lib", __FILE__)

require "server"

ss = SleepingServer.new "localhost", 23456

begin
  ss.start
rescue Interrupt
  puts "Stopping..."
end
