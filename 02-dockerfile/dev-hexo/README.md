# Hexo docker for dev


## Referecne

* [docker-node](https://github.com/joyent/docker-node)
* [hexo docs](http://hexo.io/docs/)
* [James Pan's Blog](http://blog.jamespan.me/2015/04/17/hexo-in-the-docker/)

## Build

    $ sudo docker build --rm -t dev:hexo .

## Start Container

本人是将整个hexo 博客目录作为VOLUME映射到了container下 `/data/blog`路径。个人认为有可能会更新`package.json`的内容来添加新的包，就不需要重新build， 会有更大的灵活性。

    $ sudo docker run -d -P -v ./hexo_blog:/data/blog dev:hexo

