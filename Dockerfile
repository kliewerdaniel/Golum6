FROM jekyll/jekyll:4.2.0
WORKDIR /srv/jekyll
COPY . .
RUN bundle install
CMD ["jekyll", "serve", "--force_polling", "-H", "0.0.0.0"]
