
__version__ = "$Id: $"

# See end of file for comment block including change history and references.

LICENSE = '''
 ----------------------------------------------------------

 ----------------------------------------------------------
 '''
# -------------------------------------------------------------------
# ---------------------------------------------------------
# -----------------------------------------------
# -------------------------------------

# ---------------------------------------------------------
# ---------------------------------------------------------

import platform
assert (platform.python_version() == "3.7.6"), "Written for Python 3.7.6" 

import json
import os
import time
import sys
import lib.fsm as fsm
import lib.logzero as logzero
from lib.logzero import logger
from socket import socket, AF_INET, SOCK_DGRAM

# ---------------------------------------------------------
# Setup logfile
logzero.logfile("../JS8Call SandBox/temp/js8callapi.log")

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

# -----------------------------------------------
listen = ('127.0.0.1', 2242)

# -----------------------------------------------
def from_message(content):
    try:
        return json.loads(content)
    except ValueError:
        return {}

# -----------------------------------------------
def to_message(typ, value='', params=None):
    if params is None:
        params = {}
    return json.dumps({'type': typ, 'value': value, 'params': params})

# -----------------------------------------------
class Server(object):
    first = True
    def process(self, message):
        pass
        # ke2kq, 2:23 PM 5/3/2020, -1+1
        # print('message process: ', message)
        # debug only, too verbose >> logger.info("message process: %s", message)
# ke2kq, eventually the follow will be used to parse info from js8 and Q a response.
#        typ = message.get('type', '')
#        value = message.get('value', '')
#        params = message.get('params', {})
#        if not typ:
#            return
#        print('->', type)
#        if value:
#            print('-> value', value)
#        if params:
#            print('-> params: ', params)
#        elif typ == 'CLOSE':
#            self.close()

    # -------------------------------------------
    def send(self, *args, **kwargs):
        params = kwargs.get('params', {})
        if '_ID' not in params:
            params['_ID'] = int(time.time()*1000)
            kwargs['params'] = params
        message = to_message(*args, **kwargs)
        print('outgoing message:', message)
        self.sock.sendto(message.encode, self.reply_to)
   
    # -------------------------------------------
    def listen(self):
        print('listening on', ':'.join(map(str, listen)))
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(listen)
        self.listening = True
        try:
            while self.listening:

                # ke2kq, 20200503, -1+4
                # content, addr = self.sock.recvfrom(65500)
                try:
                    content, addr = self.sock.recvfrom(65500)
                except KeyboardInterrupt:
                   logger.info("control-c pressed, program ended --------------------")
                   raise SystemExit('control-c pressed, program ended')

                print('incoming message:', ':'.join(map(str, addr)))
                try:
                    message = json.loads(content)
                except ValueError:
                    message = {}
                if not message:
                    continue
                self.reply_to = addr
                self.process(message)
        finally:
            self.sock.close()

    # -------------------------------------------
    def close(self):
        self.listening = False

# -----------------------------------------------
def main():
#   logger.info('starting udp api')
  s = Server()
  while True:
    s.listen()
# ke2kq 1:32 PM 5/3/2020
#    try:
#      s.listen()
#    except KeyboardInterrupt:
#      raise SystemExit('control-c pressed, program ended')

# ---------------------------------------------------------
if __name__ == '__main__':

  try:
    debug("__name__")
    logger.info("starting js8call udp api --------------------")
    main()
  except Exception as e:
    logger.exception(e)

# uncomment below to test logzero
#  # These log messages are sent to the console
#  logger.debug("hello")
#  logger.info("info")
#  logger.warning("warning")
#  logger.error("error")
#  # This is how you'd log an exception
#  try:
#      raise Exception("this is a demo exception")
#  except Exception as e:
#      logger.exception(e)

# -------------------------------------------------------------------

REFERENCES = '''
 ----------------------------------------------------------
"""
Source(5/2020): https://github.com/metachris/logzero
Copyright 2017, Chris Hager. Revision b5d49fc2. MIT license.
"""

references(4/2020):
https://bitbucket.org/widefido/js8call/raw/cbe3e519364658baf07148b3b4d108e1a29cc46d/udp.p
https://github.com/m0iax/JS8CallUtilities_V
https://logzero.readthedocs.io/en/latest/

 ----------------------------------------------------------

'''
