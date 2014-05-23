#!/bin/python

import gfapi

class Mounter:
  """ mount gluster volume"""

  def __init__( self ):
    pass

  def mount( self, g_args ):
    mnt = gfapi.Volume(g_args['host'], g_args['volume'])
    return mnt.mount()

def main():
  pass

if __name__ == '__main__':
  main()
