require "socket"
require "json"
require "bunny"

conn = Bunny.new
conn.start

ch = conn.create_channel
q = ch.queue("statistic-queue", auto_delete: true)

q.subscribe do |delivery_info, metadata, payload|
  puts "Received #{payload}"
  message = JSON.parse(payload)
  host = message["host"]
  port = message["port"]

  s = TCPSocket.new host, port
  s.send "1", 0
  s.close
end

sleep 15
