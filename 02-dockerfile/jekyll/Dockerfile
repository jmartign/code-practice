FROM ruby:latest
MAINTAINER Vika Zhou <vika.zhou@gmail.com>

RUN gem install jekyll \
        && gem install rdiscount

RUN mkdir /data
VOLUME /data
WORKDIR /data

EXPOSE 4000

CMD jekyll serve
