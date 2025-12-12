import socket
import time
from datetime import datetime
import sys
import random

import vac_client as vc
import get_args as ga

# from Kyle:
# Its IP address is 131.225.97.191

# this shows that the dhcp name doesn't quite match the IP address
# > 131.225.97.191
# 191.97.225.131.in-addr.arpa     name = raspberrypi.dhcp.fnal.gov.
# $ ping raspberrypi.dhcp.fnal.gov
# PING raspberrypi.dhcp.fnal.gov (131.225.96.229) 56(84) bytes of data.

# csresearch08.fnal.gov (131.225.161.198)

if __name__ == "__main__":
    p=ga.get_args()
    sender = vc.PressureSender(p)

    rc = sender.ping()
    if rc<0:
        print("server not running - ping failed")
        sys.exit(-1)

    print("Server is running fine")

