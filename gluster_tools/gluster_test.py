#!/bin/python

import argparse
import re
import errno

"""
syntax
  gluster_ = identity ":/" volume/path [:port]
    identity       = ip_addr | host_name
    port(optional) = num
    volume
    path

example:
  gluster://storage.int.example.net/bigfiles/iso-images
  gluster://storage.int.example.net:80/bigfiles/iso-images
    host   = storage.int.example.net
    port   = 80
    volume = bigfiles
    path   = iso-images
"""

class Gluster_Listing:
  """parse a given Gluster Volume"""

  # def __init__( self, gluster_volume ):
  def __init__( self ):
    # gluster_volume = 'luster://storage.int.example.net/bigfiles/iso-images'
    # gluster_volume = 'gluster://storage.int.example.net/bigfiles/iso-images'
    gluster_volume = 'gluster://storage.int.example.net:80/bigfiles/iso-images'
    # gluster_volume = 'gluster://209.49.13.42:80/bigfiles/iso-images'
    self.parse_gluster_volume(gluster_volume)

  def parse_gluster_volume( self, gluster_volume ):
    """get the individual parts of a gluster volume"""
    try:
      gluster_match = re.match('^(?:gluster://)(.*)/(.*)/(.*)$',gluster_volume).groups()
    except:
      print 'Error: enter a valid gluster URL'
      raise SystemExit
    id_group = gluster_match[0]
    volume   = gluster_match[1]
    path     = gluster_match[2]

    identity = re.match('^([^:]*)(?::(\d*))?$',id_group).groups()[0]
    port = re.match('^([^:]*)(?::(\d*))?$',id_group).groups()[1]

    self.print_gluster_volume(gluster_volume)
    self.print_identity(identity)
    self.print_port(port)
    self.print_volume(volume)
    self.print_path(path)

  def print_gluster_volume( self, gluster_volume ):
    print 'gluster volume:', gluster_volume

  def print_identity( self, identity ):
    """print ip address or host name"""
    if re.match('\d+.\d+.\d+.\d+',identity):
      print 'IP address:', identity
    else:
      print 'Host name:', identity

  def print_port( self, port):
    if port:
      print 'port:', port

  def print_volume( self, volume):
    print 'volume:' , volume

  def print_path( self, path):
    print 'path:' , path


class Parse_Arguments:
  "parses command-line arguments"

  def __init__( self ):
    self.parse_args()

  def parse_args( self ):
    """return argument for gluster volume"""
    parser.add_argument('gluster volume', help='')
    return parser.parse_args().lower()

if __name__ == '__main__':
  # Gluster_Listing(Parse_Arguments.parse_args())
  Gluster_Listing()
