Reference: [http://tech.uc.cn/?p=2726](http://tech.uc.cn/?p=2726)

Build:

    docker build --rm -t dev:base . 

Start Container:

    docker run -i -t --name ruby dev:base irb
