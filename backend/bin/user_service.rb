$:.unshift File.expand_path("../../lib", __FILE__)

require "grpc"
require "rpc/user_service_services_pb"

class UserServiceImpl < UserService::UserService::Service
  def add_stock_to_user(request, _call)
    UserService::OkAnswer.new(ok_code: 1)
  end

  def remove_stock_from_user(request, _call)
    UserService::OkAnswer.new(ok_code: 1)
  end

  def get_stocks(request, _call)
    UserService::StockAnswer.new(codes: ["A", "B", "C"])
  end
end

PORT = "0.0.0.0:50001"
s = GRPC::RpcServer.new
s.add_http2_port(PORT, :this_port_is_insecure)
puts "Running insecurely on #{PORT}"
s.handle(UserServiceImpl.new)
s.run_till_terminated_or_interrupted([1, "int", "SIGQUIT"])
