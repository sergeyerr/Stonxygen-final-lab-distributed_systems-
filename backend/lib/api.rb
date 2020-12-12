require "sinatra"
require "json"
require "stock"
require "user"
require "error"
require "statistic"

configure do
  set :protection, except: [:json_csrf]
end

before do
  content_type :json
end

get "/api/ping" do
  {success: true, reason: ""}.to_json
end

get "/api/stock/list" do
  stocks = Stock.all_available
  {
    success: true,
    reason: "",
    stocks: stocks
  }.to_json
end

def check_credentials(request)
  begin
    request.body.rewind
    body = JSON.parse(request.body.read)
    name = body["name"]
    password = body["password"]

    if name.nil? || password.nil?
      halt(
        400,
        {
          success: false,
          reason: "name or password was not provided"
        }
      )
    end

    if name == "" || password == "" ||
        name.length > 255 || password.length > 255
      halt(
        400,
        {
          success: false,
          reason: "empty or too long credentials"
        }.to_json
      )
    end
  rescue JSON::ParserError
    halt(
      400,
      {
        success: false,
        reason: "the request was not a JSON object"
      }.to_json
    )
  end
end

post "/api/user/login" do
  check_credentials request
  request.body.rewind
  body = JSON.parse(request.body.read)
  LOGGER.debug("Logging in #{body["name"]} with password #{body["password"]}")
  u, t = User.login(body["name"], body["password"])
  {
    success: true,
    reason: "",
    user: u,
    token: t
  }.to_json
end

post "/api/user/signup" do
  check_credentials request
  request.body.rewind
  body = JSON.parse(request.body.read)
  LOGGER.debug("Signing up #{body["name"]} with password #{body["password"]}")
  u, t = User.signup body["name"], body["password"]
  [
    201,
    {
      success: true,
      reason: "",
      user: u,
      token: t
    }.to_json
  ]
end

get "/api/user/info" do
  u = User.authenticate request.cookies["token"]
  if !u.nil?
    {
      success: true,
      reason: "",
      user: u
    }.to_json
  else
    raise BadTokenError
  end
end

def check_for_code(request)
  unless params.has_key?("code")
    halt [
      400,
      {
        success: false,
        reason:
          "malformed request, please make " \
          'sure URL-parameter "code" is present'
      }.to_json
    ]
  end
end

post "/api/stock/buy" do
  check_for_code request
  LOGGER.debug("Buying #{params["code"]}")
  u = User.authenticate request.cookies["token"]
  if !u.nil?
    u.buy(params["code"])
    {success: true, reason: ""}.to_json
  else
    403
  end
end

post "/api/stock/sell" do
  check_for_code request
  u = User.authenticate request.cookies["token"]
  if !u.nil?
    u.sell(params["code"])
    {success: true, reason: ""}.to_json
  else
    403
  end
end

get "/api/stock/statistic" do
  check_for_code request
  u = User.authenticate request.cookies["token"]
  if !u.nil?
    s = Stock.statistic(u.name, params["code"])
    if s.nil?
      sr = StatRequest.new(u.name, params["code"])
      s = sr.perform
    end
    {success: true, reason: "", statistic: s}.to_json
  else
    403
  end
end

error InvalidCredentialsError do
  [
    200,
    {
      success: false,
      reason: "username of password incorrect"
    }
  ]
end

error UserExistsError do
  [
    200,
    {
      success: false,
      reason: "user exists"
    }
  ]
end

error BadTokenError do
  [
    200,
    {
      success: false,
      reason: "bad user token"
    }.to_json
  ]
end

error 403 do
  {
    success: false,
    reason: "forbidden"
  }.to_json
end

error 500 do
  {
    success: false,
    reason:
      "a dark wizard has magically " \
      "transformed the remote server into a toad"
  }.to_json
end

not_found do
  {
    success: false,
    reason: "dead end"
  }.to_json
end
