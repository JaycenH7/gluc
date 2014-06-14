#!/usr/bin/python

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

import argparse, re

class Parser:
   """parse for the host, port, volume and path of a gluster url"""

   def parse( self, gluster_url ):
      g_args = {}

      try:
         g_args_match = re.match('^(?:gluster://)([^/]*)/([^/]*)(/.*)?$', gluster_url).groups()
      except:
         print "'%s' is not a valid gluster URL" % gluster_url
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
