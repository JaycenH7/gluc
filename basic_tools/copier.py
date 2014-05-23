#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, argparse, errno

class Copier:
  "copies files and directories from source to destination"

  def __init__( self, p_args ):
    try:
      self.copy_file( p_args.source, p_args.target )
    except IOError as error:
      if error.errno == errno.EISDIR:
        self.copy_dir( p_args )
      else: print error

  def copy_file( self, p_src, p_tgt ):
    """copy a file"""
    file_read = file( p_src, 'r' ).read()
    file_write = file( p_tgt, 'w' ).write( file_read )

  def copy_dir( self, p_args ):
    """copy a directory"""
    root_src_dir = os.path.join( '.', p_args.source )
    root_tgt_dir = os.path.join( '.', p_args.target )

    if not os.path.exists( p_args.target ):
      os.mkdir( p_args.target )

    for (src_dir, dirs, files) in os.walk( root_src_dir ):
      tgt_dir =  src_dir.replace( root_src_dir, root_tgt_dir )
      if not os.path.exists( tgt_dir ):
        os.mkdir( tgt_dir )
      for file_ in files:
        src_file = os.path.join( src_dir, file_ )
        tgt_file = os.path.join( tgt_dir, file_ )

        if os.path.exists( tgt_file ):
          os.remove( tgt_file )

        self.copy_file( src_file, tgt_file )

class Parse_Arguments:
  "parses command-line arguments"

  def __init__( self ):
    self.parse_args()

  def parse_args( self ):
    """
    parse arguments for source file/directory and 
    target file/directory
    """
    parser = argparse.ArgumentParser(
        description = 'copy files/directories from source to destination'
    )
    parser.add_argument( 'source'
    , help='source file/directory to copy from'
    )
    parser.add_argument( 'target', default='.'
    , help='target file/directory to copy to'
    )
    return parser.parse_args()

if __name__ == '__main__':
  Copier(Parse_Arguments().parse_args())
