require "rpc/user_service_services_pb"
require "rpc/auth_services_pb"
require "env"

USER = UserService::UserService::Stub.new(
  "localhost:50001",
  :this_channel_is_insecure
)

AUTH = AuthService::Auth::Stub.new(
  "localhost:50000",
  :this_channel_is_insecure
)

class User
  def initialize(name, stocks, token)
    @name = name
    @stocks = []
    @token = ""
  end

  def self.login(name, password)
    request = AuthService::UserPasswordRequest.new(user: name, password: password)
    response = STUB.get_token(request)
    response.token
  end

  def self.authenticate(token)
    request = AuthService::CheckTokenRequest.new(token)
    response = STUB.CheckToken(request)
    response.ok_code
  end

  def self.register(name, password)
    request = AuthService::UserPasswordRequest.new(
      user: name,
      password: password
    )
    response = AUTH.register_user(request)
    User.new(name, [], response.token)
  end

  def to_json(*options)
    {name: @name, stocks: @stocks, token: @token}.to_json(*options)
  end
end
