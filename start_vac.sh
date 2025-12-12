#!/usr/bin/env bash

# uid=8624(jbk) gid=1751(g163) groups=1751(g163),8674(fwk),53301(magis-group)

# this is meant to be run by systemd.
# copy magsys.service to /usr/lib/systemd/system
# make sure the paths are correct in magsys.servive
# make sure the paths are correct in this script
# reload systemd and start the service
#  $ systemctl daemon-reload
#  $ systemctl enable magsys.service
#  $ systemctl enable magsys.service
#  $ service magsys start
#  $ service magsys status

export H=/work1/fwk/magis-group
export MAG=$H/VacServe
export PYENV=/work1/fwk/magispy
export SERV='131.225.161.198'
export CLIENT='131.225.97.191'

cd $MAG
source $PYENV/bin/activate
echo "starting the thing" > /tmp/vac_output2.txt
nohup $PYENV/bin/python3 ./vac_server.py -s $SERV -c $CLIENT >/tmp/vac_output1.txt 2>&1 &
disown -ar
echo "started the thing" >> /tmp/vac_output2.txt
# systemd-notify --ready


