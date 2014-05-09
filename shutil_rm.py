#!/usr/bin/python

import os, shutil, errno, argparse

class Shutil_Remove:
  "removes files and directories from source to destination"

  def __init__( self, p_args ):
    try:
      shutil.rmtree(p_args.source)
    except OSError as error:
      if error.errno == errno.ENOTDIR:
        os.remove(p_args.source)
      else: print error


class Parse_Arguments:
  "parses command-line arguments"

  def __init__( self ):
    self.parse_args()

  def parse_args( self ):
    parser = argparse.ArgumentParser(
        description = 'remove files/directories from source to destination'
    )
    parser.add_argument( 'source'
    , help='source file/directory to copy from'
    )
    return parser.parse_args()


Shutil_Remove(Parse_Arguments().parse_args())
