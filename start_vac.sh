#!/usr/bin/env bash

# uid=8624(jbk) gid=1751(g163) groups=1751(g163),8674(fwk),53301(magis-group)
# csresearch02 private IP is 172.19.8.193
# csresearch08 private IP is 172.19.8.199
# uboonegpvm07 IP is 131.225.240.146
# vacuum pressure IP is 131.225.97.191 (although this is DHCP)
# csresearch08 IP is 131.225.161.198

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

# the default_in section needed to be used!
# accept all on port 6700
# nft add rule inet filter INPUT udp dport 6700 accept
# nft add rule inet filter default_in udp dport 6700 accept
# accept only from vac and uboone subnets
# nft add rule inet filter INPUT ip saddr 131.225.97.0/24 udp dport 6700 accept
# nft add rule inet filter INPUT ip saddr 131.225.240.0/24 udp dport 6700 accept
# nft add rule inet filter default_in ip saddr 131.225.97.0/24 udp dport 6700 accept
# nft add rule inet filter default_in ip saddr 131.225.240.0/24 udp dport 6700 accept

export H=/work1/fwk/magis-group
export MAG=$H/VacServe
export PYENV=/work1/fwk/magispy
export SERV='131.225.161.198'
export CLIENT='131.225.240.146'
#export CLIENT='131.225.97.191'

cd $MAG
source $PYENV/bin/activate
echo "starting the thing" > /tmp/vac_output2.txt
nohup $PYENV/bin/python3 ./vac_server.py -s $SERV -c $CLIENT >/tmp/vac_output1.txt 2>&1 &
disown -ar
echo "started the thing" >> /tmp/vac_output2.txt
# systemd-notify --ready

