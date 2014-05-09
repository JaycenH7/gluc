#!/usr/bin/python

import os, shutil, errno, argparse

class Shutil_Copy:
  "copies files and directories from source to destination"

  def __init__( self, p_args ):
    if os.path.exists(p_args.target):
      shutil.rmtree(target)

    try:
      shutil.copytree(p_args.source, p_args.target)
    except OSError as error:
      if error.errno == errno.ENOTDIR:
        shutil.copy(p_args.source, p_args.target)
      else: print error


class Parse_Arguments:
  "parses command-line arguments"

  def __init__( self ):
    self.parse_args()

  def parse_args( self ):
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


Shutil_Copy(Parse_Arguments().parse_args())
