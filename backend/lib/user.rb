require "rpc/user_service_services_pb"
require "rpc/auth_services_pb"
require "env"
require "stock"

USER = UserService::UserService::Stub.new(
  "#{Env::USER}:50001",
  :this_channel_is_insecure
)

AUTH = AuthService::Auth::Stub.new(
  "#{Env::AUTH}:50000",
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
    response = AUTH.get_token(request)
    token = response.token
    stocks = self.stocks(name)

    User.new(name, stocks, token)
  end

  def self.authenticate(token)
    request = AuthService::CheckTokenRequest.new(token)
    response = AUTH.CheckToken(request)
    response.ok_code
  end

  def self.register(name, password)
    request = AuthService::UserPasswordRequest.new(
      user: name,
      password: password
    )
    response = USER.register_user(request)
    User.new(name, stocks, response.token)
  end

  def to_json(*options)
    {name: @name, stocks: @stocks, token: @token}.to_json(*options)
  end

  private

  def stocks(name)
    request = UserService::GetUserStocksRequest(user: name)
    response = USER.get_stocks(request)
    response.codes.map { |code| Stock.new(code, "", 0) }
  end
end
