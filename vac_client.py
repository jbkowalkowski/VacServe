import socket
import time
from datetime import datetime
import sys
import random

# from Kyle:
# Its IP address is 131.225.97.191

# this shows that the dhcp name doesn't quite match the IP address
# > 131.225.97.191
# 191.97.225.131.in-addr.arpa     name = raspberrypi.dhcp.fnal.gov.
# $ ping raspberrypi.dhcp.fnal.gov
# PING raspberrypi.dhcp.fnal.gov (131.225.96.229) 56(84) bytes of data.

# csresearch08.fnal.gov (131.225.161.198)

import get_args as ga

class PressureSender:
    def __init__(self, args):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.settimeout(1.0)
        self.seq = 1
        self.udp_server = args.udp_server
        self.udp_port = args.udp_port
        self.addr = (args.udp_server, args.udp_port)

    def ping(self):
        return self.send_data("P", 'ping')        

    def send_list(self, payload:list):
        s = ",".join([str(x) for x in payload])
        return self.send(s)

    def send(self, payload:str):
        rc = self.send_data("D", payload)
        self.seq += 1
        return rc

    def send_data(self, type, payload):
        self.soc.sendto(f'{type}, {self.seq}, {payload}'.encode(), self.addr)

        try:
            data, address = self.soc.recvfrom(4096)
            rc=int(data.decode().split(',')[1]) 
            #print(f'got back {data.decode()} {rc}')
            if rc != self.seq: rc=None
        except socket.timeout as err:
            rc=-1

        return rc



if __name__ == "__main__":
    p=ga.get_args()
    sender = PressureSender(p)

    rc = sender.ping()
    if rc<0:
        print("server not running - ping failed")
        sys.exit(-1)

    while True:

        #now = time.strftime('%Y%m%d-%H-%M-%S',time.localtime())
        now = datetime.now()
        now1 = now.strftime('%Y-%m-%d')
        now2 = now.strftime('%H:%M:%S.%f')[:-3]
        pressure = random.random()

        #payload = f'{now1}, {now2}, {pressure}'
        #rc = sender.send(payload)

        rc = sender.send_list([now1, now2, pressure])

        # this is what is written in the VacToolbox code
        # w.writerow([now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S.%f')[:-3], pressure])

        if rc == None:
            print("Server ACK did not contain matching data sequence number")
        elif rc <0:
            print("Server ACK timed out")
            
        time.sleep(10)



