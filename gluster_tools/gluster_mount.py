#!/bin/python

import gfapi
import socket
import errno

class Mounter:
   """ mount gluster volume"""

   def __init__( self, g_args ):
      # declare instance variables
      self.host   = g_args['host']
      self.port   = g_args['port']
      self.volume = g_args['volume']

   def mount( self ):
      test  = self.test_connect()
      mount = self.mount_volume()
      return mount

   def test_connect( self ):
      try:
         sock = socket.socket()
         sock.settimeout(10)
         sock.connect(( self.host, int(self.port) ))
         sock.close()
      except IOError as error:
         if error.errno == -errno.EIO:
            print 'error: no address associated with', self.host

         elif error.errno == errno.ETIMEOUT:
            print 'error: netowkr connection timed out'

         elif error.errno == errno.ECONNREFUSED:
            print 'error: network connection was refused to port', self.port

         elif error.errno == errno.ENETRESET:
            print 'error: network connection was reset'

         elif error.errno == errno.ENETDOWN:
            print 'error: network connection is down'

         elif error.errno == errno.ENETUNREACH:
            print 'error: network connection is unreachable'

         else:
            print error

         raise SystemExit

   def mount_volume( self ):
      mnt_vol = gfapi.Volume( self.host, self.volume )
      mnt_vol.mount()
      return mnt_vol

def main():
   pass

if __name__ == '__main__':
   main()
