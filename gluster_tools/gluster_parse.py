#!/bin/python

"""
syntax:
  gluster_ = identity ":/" volume/path [:port]
    identity       = ip_addr | host_name
    port(optional) = num
    volume
    path

example:
  gluster://storage.int.example.net:80/bigfiles/iso-images
    host   = storage.int.example.net
    port   = 80
    volume = bigfiles
    path   = iso-images
  test
    host = Pod-VM
    port = 24007(default)
    volume = gv0
    path = /
  1) mount 'host', 'volume'
    $ mnt = gfapi.Volume('host','volume')
    mnt.mount()
  2) list 'path'
    mnt.listdir('path')

"""

import re

class Parser:
  """parse for the host, port, volume and path of a gluster url"""

  def __init__(self):
    pass

  def parse( self, volume ):
    # Temporary ##############################################################################
    # p_args['target_volume'], p_args = 'luster://storage.int.example.net/bigfiles/iso-images'
    # p_args['target_volume'] = 'gluster://storage.int.example.net/bigfiles/iso-images'
    # volume = 'gluster://storage.int.example.net:80/bigfiles/iso-images'
    # volume = 'gluster://209.49.13.42:80/bigfiles/iso-images'
    # Temporary ##############################################################################

    g_args = {}

    try:
      g_args_match = re.match('^(?:gluster://)(.*)/(.*[^/])(/.*)?$', volume).groups()
    except:
      print 'Error: enter a valid volume URL'
      raise SystemExit
    id_group = g_args_match[0]
    g_args['volume']   = g_args_match[1]
    g_args['path']     = g_args_match[2]

    g_args['host'] = re.match('^([^:]*)(?::(\d*))?$', id_group).groups()[0]
    g_args['port'] = re.match('^([^:]*)(?::(\d*))?$', id_group).groups()[1]

    if g_args['path'] == None: g_args['path'] = '/'
    if g_args['port'] == None: g_args['port'] = 24007

    return g_args

def main():
  pass

if __name__ == '__main__':
  main()
