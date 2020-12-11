FROM ruby
WORKDIR code
COPY . . 
RUN gem install bundler
RUN bundler install
ENTRYPOINT ["ruby", "bin/hack.rb"]