module Env
  HOSTNAME = ENV["MY_HOSTNAME"] || "localhost"
  REDIS = ENV["REDIS"] || "localhost"
  REDIS_SENTINEL = ENV["REDIS_SENTINEL"] || "localhost"
  RABBITMQ = ENV["RABBITMQ"] || "localhost"
  AUTH_SERVICE = ENV["AUTH_SERVICE"] || "localhost"
  USER_SERVICE = ENV["USER_SERVICE"] || "localhost"
end
