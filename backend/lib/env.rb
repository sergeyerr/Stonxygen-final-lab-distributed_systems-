module Env
  HOSTNAME = ENV["MY_HOSTNAME"] || "localhost"
  REDIS = ENV["REDIS"] || "localhost"
  RABBITMQ = ENV["RABBITMQ"] || "localhost"
  AUTH = ENV["AUTH"] || "localhost"
  USER = ENV["USER"] || "localhost"
end
