require "sinatra"
require "json"
require "stock"
require "user"
require "error"

before do
  content_type :json
end

get "/api/ping" do
  "pong"
end

get "/api/stock/list" do
  stocks = Stock.all_available
  {
    success: true,
    reason: "",
    stocks: stocks
  }.to_json
end

post(/\/api\/user\/(?:login|signup)/) do
  error = false

  if request.env.has_key?("HTTP_NAME") && request.env.has_key?("HTTP_PASSWORD")
    name = request.env["HTTP_NAME"]
    password = request.env["HTTP_PASSWORD"]
    if name == "" || password == "" ||
        name.length > 255 || password.length > 255
      error = true
    else
      pass
    end
  else
    error = true
  end

  if error
    [
      400,
      {
        success: false,
        reason:
          "malformed request, make sure " \
          'it contains valid "name" and "password" headers',
        user: "",
        token: ""
      }.to_json
    ]
  end
end

post "/api/user/login" do
  name = request.env["HTTP_NAME"]
  password = request.env["HTTP_PASSWORD"]
  u, t = User.login(name, password)
  {
    success: true,
    reason: "",
    user: u,
    token: t
  }.to_json
end

post "/api/user/signup" do
  name = request.env["HTTP_NAME"]
  password = request.env["HTTP_PASSWORD"]
  u, t = User.signup name, password
  {
    success: true,
    reason: "",
    user: u,
    token: t
  }.to_json
end

get "/api/*" do
  if User.authenticate(request.cookies["token"])
    pass
  else
    403
  end
end

get "/api/user/info" do
  u = User.authenticate(request.cookies["token"])
  if !u.nil?
    {
      success: true,
      reason: "",
      user: u
    }.to_json
  else
    403
  end
end

get(/\/api\/stock\/(?:buy|sell)/) do
  if params.has_key?("code")
    pass
  else
    [
      400,
      {
        success: false,
        reason:
          "malformed request, please make " \
          "sure \"code\" URL-parameter is present"
      }.to_json
    ]
  end
end

get "/api/stock/buy" do
  u = User.authenticate
  if !u.nil?
    u.buy(params["code"])
    {success: true, reason: ""}.to_json
  else
    403
  end
end

get "/api/stock/sell" do
  u = User.authenticate
  if !u.nil?
    u.sell(params["code"])
    {success: true, reason: ""}.to_json
  else
    403
  end
end

get "/api/stock/statistic" do
  u = User.authenticate
  if !u.nil?
    s = Stock.statistic(params["code"], u.name)
    {success: true, reason: "", statistic: s}.to_json
  else
    403
  end
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
    reason: env["sinatra.error"].to_s
  }.to_json
end
