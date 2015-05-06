FROM node:0.12

MAINTAINER Vika Zhou, <vika.zhou@gmail.com>

RUN npm install -g cnpm --registry=https://r.cnpmjs.org \
  && cnpm install -g hexo-cli \
  && mkdir -p /data/blog \
  && cd /data/blog \
  && hexo init

WORKDIR /data/blog


VOLUME ["/data/blog"]

EXPOSE 4000

CMD hexo server

