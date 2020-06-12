
# -------------------------------------------------------------------
# -------------------------------------------------------------------

__version__ = "$Id: $"

#
# source(6/2020): https://github.com/bmo/py-wsjtx/blob/master/pywsjtx/extra/simple_server.py
# Copyright 2018 Brian Moran  

#
# In WSJTX parlance, the 'network server' is a program external to the wsjtx.exe program that handles packets emitted by wsjtx
#
# TODO: handle multicast groups.
#
# see dump_wsjtx_packets.py example for some simple usage
#
# See end of file for comment block including change history and references.

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# ---------------------------------------------------------
# -----------------------------------------------
# -------------------------------------

# ---------------------------------------------------------
import platform
assert (platform.python_version() == "3.7.6"), "Written for Python 3.7.6" 

# import json
# import os
# import time
import sys
# import lib.fsm as fsm
# import lib.logzero as logzero
# from lib.logzero import logger
# from socket import socket, AF_INET, SOCK_DGRAM

# ---------------------------------------------------------
# Setup logfile

# logzero.logfile("../wsjt-x-sandbox/temp/simple-server.log")

# -----------------------------------------------
# ---------------------------
# print(sys.version)
# ---------------------------
# source(8/2018):
# https://stackoverflow.com/questions/32000934/python-print-a-variables-name-and-value
# Usage: debug('expression')

def debug(expression):
  '''
  document/test me
  '''
  frame = sys._getframe(1)
  print(
      expression, '=',
      repr(eval(expression, frame.f_globals, frame.f_locals)
  ))

# ---------------------------------------------------------
import socket
import struct

# ke2kq, 6/7/2020, -1+1
import pywsjtx
# import wsjtx_packets

import logging
import ipaddress

# ---------------------------------------------------------
class SimpleServer(object):
    logger = logging.getLogger()
    MAX_BUFFER_SIZE = pywsjtx.GenericWSJTXPacket.MAXIMUM_NETWORK_MESSAGE_SIZE
    DEFAULT_UDP_PORT = 2237
    #
    #
    def __init__(self, ip_address='127.0.0.1', udp_port=DEFAULT_UDP_PORT, **kwargs):
        self.timeout = None
        self.verbose = kwargs.get("verbose",False)

        if kwargs.get("timeout") is not None:
            self.timeout = kwargs.get("timeout")

        the_address = ipaddress.ip_address(ip_address)
        if not the_address.is_multicast:
            self.sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.sock.bind((ip_address, int(udp_port)))
        else:
            self.multicast_setup(ip_address, udp_port)

        if self.timeout is not None:
            self.sock.settimeout(self.timeout)

    def multicast_setup(self, group, port=''):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def rx_packet(self):
        try:
            pkt, addr_port = self.sock.recvfrom(self.MAX_BUFFER_SIZE)  # buffer size is 1024 bytes
            return(pkt, addr_port)
        except socket.timeout:
            if self.verbose:
                logging.debug("rx_packet: socket.timeout")
            return (None, None)

    def send_packet(self, addr_port, pkt):
        bytes_sent = self.sock.sendto(pkt,addr_port)
        self.logger.debug("send_packet: Bytes sent {} ".format(bytes_sent))

    def demo_run(self):
        while True:
            (pkt, addr_port) = self.rx_packet()
            if (pkt != None):
                the_packet = pywsjtx.WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
                print(the_packet)

# -----------------------------------------------
def main():
  ss = SimpleServer()
  print('control-c to exit')
  ss.demo_run()

# ---------------------------------------------------------
if __name__ == '__main__':

  try:
    debug("__name__")
    main()
  except Exception as e:
    print('Exception', e)

# -------------------------------------------------------------------

REFERENCES = '''
 ----------------------------------------------------------
references(6/2020):
https://logzero.readthedocs.io/en/latest/

 ----------------------------------------------------------

'''
