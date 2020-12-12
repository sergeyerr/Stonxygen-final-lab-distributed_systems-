require "redis"
require "error"
require "env"
require "logs"

def redis
  if Env::REDIS == "localhost"
    Redis.new(host: Env::REDIS, port: 6379)
  else
    sentinels = [{host: Env::REDIS_SENTINEL, port: 26379}]
    Redis.new(
      host: Env::REDIS,
      password: "redis",
      sentinels: sentinels,
      role: :slave
    )
  end
end

class Stock
  def initialize(code, organization, price)
    @code = code
    @organization = organization
    @price = price
  end

  attr_reader :code

  def self.all_available
    r = redis
    results = r.hscan("Stocks", 0)
    stocks = results[1]
    organizations = stocks.map { |s| s[1] }
    codes = stocks.map { |s| s[0] }
    prices = self.prices(codes)

    self.stocks(codes, prices, organizations)
  end

  def self.with_codes(codes)
    r = redis
    organizations = r.hmget("Stocks", *codes)
    prices = self.prices(codes)

    stocks(codes, prices, organizations)
  end

  def self.statistic(username, code)
    r = redis
    s = r.get("#{username}_#{code}")
    s&.to_f
  end

  def to_json(*options)
    {
      code: @code,
      organization: @organization,
      price: @price
    }.to_json(*options)
  end

  def self.prices(codes)
    if codes.length == 0
      return []
    end

    r = redis
    prices = r.mget(*codes)
    if prices.any? { |p| p.nil? }
      raise DataError.new("Some stocks prices are unavailable")
    end

    begin
      prices.map { |p| p.to_f }
    rescue
      raise DataError.new("Some prices are not numbers")
    end
  end

  def self.stocks(codes, prices, organizations)
    codes.zip(organizations).zip(prices).map { |s|
      Stock.new(s[0][0], s[0][1], s[1])
    }
  end

  private_class_method :prices
  private_class_method :stocks
end
