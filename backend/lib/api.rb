require "sinatra"
require "json"
require "stock"
require "user"

before do
  content_type :json
end

get "/api/ping" do
  "pong"
end

get "/api/stock/list" do
  stocks = (1..25).map { |v|
    Stock.new("Stock #{v}", "Organization #{v}", v / 100.0)
  }

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
  {
    success: true,
    reason: "",
    user: User.new("Mackerel", []),
    token: "mackerel"
  }.to_json
end

post "/api/user/signup" do
  {
    success: true,
    reason: "",
    user: User.new("Mackerel", []),
    token: "mackerel"
  }.to_json
end

get "/api/*" do
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
  end
end

get "/api/user/info" do
  stocks = (100..110).map { |v|
    Stock.new("Stock #{v}", "Organization #{v}", v / 100.0)
  }

  {
    success: true,
    reason: "",
    user: User.new("Mackerel", stocks)
  }.to_json
end

get "/api/stock/buy" do
  if params.has_key?("code")
    {
      success: true,
      reason: ""
    }.to_json
  else
    [
      400,
      {
        success: false,
        reason:
          "malformed request, please make " \
          "sure \"code\" is provided in the URL"
      }.to_json
    ]
  end
end
