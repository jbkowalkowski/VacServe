import sys
import os
import argparse

# Defaults look like this:
# -s 192.168.10.3 -b 192.168.10.3

class Fake:
    udp_client='131.225.97.191'
    udp_server='131.225.161.198'
    udp_port=6700
    path='.'
    fixed_command=False

def get_args(add_command_args=False):
    if 'site-packages' in sys.argv[0]: # os.path.basename(sys.argv[0]):
        # provide a fake for interactive application use
        return Fake()

    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--udpport", default=Fake.udp_port, type=int, dest="udp_port",help="UDP server port")
    parser.add_argument("-c","--udpclient", default=Fake.udp_client, dest="udp_client",help="UDP client address")
    parser.add_argument("-s","--udpserver", default=Fake.udp_server, dest="udp_server",help="UDP server address")
    parser.add_argument("-p","--path", default=Fake.path, dest="path",help="directory where data will be stored")

    parser.add_argument('rest', nargs=argparse.REMAINDER, help="remove --help and the list will be printed")
    # examples of bools
    #parser.add_argument("-t","--test", default=False, action='store_true', dest="test",help="run a simple test")
    #parser.add_argument("-q","--quit", default=True, action='store_false', dest="complete",help="do not stop autosend if this is set")
    # examples of swithes
    #parser.add_argument("-d","--show-dates", default=Fake.show_dates, action='store_true', dest="show_dates",help="Show dates on graph")
    #parser.add_argument("-r","--no-render", default=Fake.render, action='store_false', dest="render",help="Do not view the graph")
    pp = parser.parse_args()

    # example of adjustments from switch settings
    #if pp.test:
    #    pp.name="test"

    if add_command_args:
        pp.fixed_command=True if pp.send_reset or pp.send_start or pp.send_stop else False
    

    return pp

if __name__ == "__main__":
    p = get_args()
    print(f'p.rest = {p.rest}')
