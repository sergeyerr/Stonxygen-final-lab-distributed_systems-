require "json"
require "bunny"
require "env"
require "error"
require "socket"
require "timeout"
require "logs"

CONN = Bunny.new("amqp://guest:rabbit@#{Env::RABBITMQ}:5672")
CONN.start

class StatRequest
  def initialize(username, code)
    @channel = CONN.create_channel
    @exchange = @channel.default_exchange
    @username = username
    @code = code
  end

  def perform
    socket = TCPServer.new("localhost", 0)
    port = socket.addr[1]
    q = @channel.queue("statistic-queue", auto_delete: true)

    message = {
      user: @username,
      code: @code,
      host: Env::HOSTNAME,
      port: port
    }.to_json

    @exchange.publish(message, routing_key: q.name, expiration: "3000")
    LOGGER.debug(
      "Awaiting response to the sent message with socket on port #{port}..."
    )
    begin
      wait_for_response(socket)
    rescue Timeout::Error
      LOGGER.warn("Statistic service is unresponsive...")
      raise CommunicationError.new("The request to statistic service has timed out")
    end
  end

  private

  def wait_for_response(socket)
    Timeout.timeout(5) do
      s = socket.accept
      b = s.recv(1)
      if b == "1"
        LOGGER.debug("Received statistic from service...")
        st = Stock.statistic(@username, @code)
        if st.nil?
          raise CommunicationError.new(
            "The requested statistic was not found in the store"
          )
        else
          st
        end
      elsif b == "0"
        raise CommunicationError.new("The statistic service failed")
      end
    end
  end
end
