require "sinatra"
require "json"
require "stock"
require "user"
<<<<<<< HEAD
require "error"
=======
>>>>>>> e0eb3809017b2d144d4165e794326a94e5baed6e

before do
  content_type :json
end

get "/api/ping" do
  "pong"
end

get "/api/stock/list" do
<<<<<<< HEAD
  stocks = Stock.all_available
=======
  stocks = (1..25).map { |v|
    Stock.new("Stock #{v}", "Organization #{v}", v / 100.0)
  }

>>>>>>> e0eb3809017b2d144d4165e794326a94e5baed6e
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
<<<<<<< HEAD
  if User.authenticate(request.cookies["token"])
    pass
  else
    403
=======
  if request.cookies["token"] == "mackerel"
    pass
  else
    [
      403,
      {
        success: false,
        reason: "forbidden"
      }.to_json
    ]
>>>>>>> e0eb3809017b2d144d4165e794326a94e5baed6e
  end
end

get "/api/user/info" do
<<<<<<< HEAD
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
=======
  stocks = (100..110).map { |v|
    Stock.new("Stock #{v}", "Organization #{v}", v / 100.0)
  }

  {
    success: true,
    reason: "",
    user: User.new("Mackerel", stocks)
  }.to_json
end

get(/\/api\/stock\/(?:buy|sell)/) do
  if params.has_key?("code") && params.has_key?("user")
>>>>>>> e0eb3809017b2d144d4165e794326a94e5baed6e
    pass
  else
    [
      400,
      {
        success: false,
        reason:
          "malformed request, please make " \
<<<<<<< HEAD
          "sure \"code\" URL-parameter is present"
=======
          "sure \"code\" and \"user\" URL-parameters are present"
>>>>>>> e0eb3809017b2d144d4165e794326a94e5baed6e
      }.to_json
    ]
  end
end

get "/api/stock/buy" do
<<<<<<< HEAD
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
=======
  "STUB"
end

get "/api/stock/sell" do
  "STUB"
>>>>>>> e0eb3809017b2d144d4165e794326a94e5baed6e
end
