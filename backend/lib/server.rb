require "socket"

class SleepingServer
  def initialize(host, port)
    @port = port
    @socket = TCPServer.new(host, port)
  end

  def start
    loop do
      puts "Listening on #{@port}..."
      Thread.start(@socket.accept) do |s|
        puts "Yaaawn..."
        sleep 5
        s.send "電気を消してください", 0
        s.close
      end
      puts "Handler launched in a thread..."
    end
  end

  def start_blocking
    loop do
      puts "Listening on #{@port}..."
      s = @socket.accept
      puts "Yaaawn..."
      sleep 5
      s.send "電気を消してください", 0
      s.close
    end
  end
end
