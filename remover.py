#!/usr/bin/python

import os
import argparse
import errno

class Remover:
  "Removes files and directories from source to destination"

  def __init__( self, p_args ):
    try:
      self.remove_file( p_args.source )
    except OSError as error:
      if error.errno == errno.EISDIR:
        self.remove_dir( p_args )
      else: print error

  def remove_file( self, p_src ):
    os.remove( p_src )

  def remove_dir( self, p_args ):
    root_src_dir = os.path.join( '.', p_args.source )

    for (src_dir, dirs, files) in os.walk( root_src_dir ,topdown=False):
      for file_ in files:
        src_file = os.path.join( src_dir, file_ )
        self.remove_file( src_file )
      os.rmdir( src_dir )

class Parse_Arguments:
  "parses command-line arguments"

  def __init__( self ):
    self.parse_args()

  def parse_args( self ):
    parser = argparse.ArgumentParser(
        description = 'remove files/directories from source to destination'
    )
    parser.add_argument( 'source'
    , help='source file/directory to move from'
    )
    return parser.parse_args()

Remover(Parse_Arguments().parse_args())
