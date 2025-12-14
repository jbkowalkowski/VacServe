import socketserver
import struct
import selectors
import time
import sys

# from Kyle:
# Its IP address is 131.225.97.191

# this shows that the dhcp name doesn't quite match the IP address
# > 131.225.97.191
# 191.97.225.131.in-addr.arpa     name = raspberrypi.dhcp.fnal.gov.
# $ ping raspberrypi.dhcp.fnal.gov
# PING raspberrypi.dhcp.fnal.gov (131.225.96.229) 56(84) bytes of data.

# csresearch08.fnal.gov (131.225.161.198)

# from the writer:
# w.writerow([now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S.%f')[:-3], pressure])

import get_args as ga

class UserData:
    def __init__(self):
        path='.'
        fout=None
        client=None

class Handler(socketserver.BaseRequestHandler):

   def handle(self):
        data=self.request[0].decode()
        soc=self.request[1]
        the_addr=self.client_address[0]

        if the_addr != self.server.ud.client:
            print(f"bad client {the_addr}")
            sys.stdout.flush()
            return
        
        f = data.strip().split(',')
        back = f"A, {f[1]}".encode()
        #print(f'sending back: {back}')
        soc.sendto(back, self.client_address)

        if f[0] == "P":
            return
        
        fout = self.server.ud.fout
        print(data, file=fout, end='\n')
        #fout.write(data)
        fout.flush()

if __name__ == "__main__":
    p=ga.get_args()

    path = p.path
    now = time.strftime('%Y%m%d-%H-%M-%S',time.localtime())
    filename = f'{path}/VacData-{now}.csv'
    fout = open(filename,'w')
    ud = UserData()

    ud.path=path
    ud.fout=fout
    ud.client=p.udp_client

    sel = selectors.SelectSelector()

    with socketserver.UDPServer((p.udp_server,p.udp_port), Handler) as server:
        sel.register(server.fileno(),selectors.EVENT_READ, server.handle_request)

        server.ud = ud

        while True:
            evs = sel.select(1)
            for k,m in evs:
                k.data()

