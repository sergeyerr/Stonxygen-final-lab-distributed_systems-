$:.unshift File.expand_path("../../lib", __FILE__)

require "grpc"
require "rpc/auth_services_pb"

class AuthenticationService < AuthService::Auth::Service
  def get_token(request, _call)
    AuthService::TokenAnswer.new(token: "mackerel")
  end

  def check_token(request, _call)
    AuthService::OkAnswer.new(ok_code: 1)
  end

  def register_user(request, _call)
    AuthService::OkAnswer.new(ok_code: 1)
  end
end

PORT = "0.0.0.0:50000"
s = GRPC::RpcServer.new
s.add_http2_port(PORT, :this_port_is_insecure)
puts "Running insecurely on #{PORT}"
s.handle(AuthenticationService.new)
s.run_till_terminated_or_interrupted([1, "int", "SIGQUIT"])
