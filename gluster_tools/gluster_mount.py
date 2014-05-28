#!/bin/python

import gfapi
import socket
import errno

class Mounter:
   """ mount gluster volume"""

   def __init__( self ):
      pass

   def mount( self, g_args ):
      test = self.test_connect( g_args )
      mount = self.mount_volume( g_args )
      return mount

   def test_connect( self, g_args ):
      try:
         sock = socket.socket()
         sock.settimeout(10)
         sock.connect(( g_args['host'], int(g_args['port']) ))
         sock.close()
      except IOError as error:
         if error.errno == -errno.EIO:
            print 'error: no address associated with', g_args['host']
         elif error.errno == errno.ETIMEOUT:
            print 'error: netowkr connection timed out'
         elif error.errno == errno.ECONNREFUSED:
            print 'error: network connection was refused to port', g_args['port']
         elif error.errno == errno.ENETRESET:
            print 'error: network connection was reset'
         elif error.errno == errno.ENETDOWN:
            print 'error: network connection is down'
         elif error.errno == errno.ENETUNREACH:
            print 'error: network connection is unreachable'
         else:
            print error
         raise SystemExit

   def mount_volume( self, g_args ):
      mnt = gfapi.Volume(g_args['host'], g_args['volume'])
      mnt.mount()
      return mnt

def main():
   pass

if __name__ == '__main__':
   main()
