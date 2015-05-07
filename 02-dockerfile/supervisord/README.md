## Reference

* https://docs.docker.com/articles/using_supervisord/
* https://docs.docker.com/articles/cfengine_process_management/
* [Supervisor](http://supervisord.org/)

## Build

    $ sudo docker build -t <yourname>/supervisord .

## Run

    $ sudo docker run -p 22 -p 80 -t -i <yourname>/supervisord

