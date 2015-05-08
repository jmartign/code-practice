#!/usr/bin/env python

from docker import Client

# cli = Client(base_url='tcp://127.0.0.1:2375')
cli = Client(base_url='unix://var/run/docker.sock')

print cli.version()
print cli.info()

container = cli.create_container(
                  image='registry:latest',
                  command='/bin/uname -a')
response = cli.start(container=container.get('Id'))
print response

print cli.containers()

