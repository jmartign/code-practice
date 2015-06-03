docs: http://docs.saltstack.com

## standalone minion

modify /etc/salt/minion

    file_client: local
    file_roots:
      base:
        /srv/salt/tut01

run `salt-call`

    sudo salt-call state.highstate --local  -l debug

when use `--local`, no need to change `file_client:local`

## some commands

* salt '*' state.highstate
* salt '*' test.ping
* salt '*' pillar.items

