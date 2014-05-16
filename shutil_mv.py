#!/usr/bin/python

import os, shutil, errno, argparse

class Shutil_Move:
  "moves files and directories from source to destination"

  def __init__( self, p_args ):
    if os.path.exists(p_args.target):
      shutil.rmtree(p_args.target)

    shutil.move(p_args.source, p_args.target)


class Parse_Arguments:
  "parses command-line arguments"

  def __init__( self ):
    self.parse_args()

  def parse_args( self ):
    parser = argparse.ArgumentParser(
        description = 'move files/directories from source to destination'
    )
    parser.add_argument( 'source'
    , help='source file/directory to copy from'
    )
    parser.add_argument( 'target', default='.'
    , help='target file/directory to copy to'
    )
    return parser.parse_args()

if __name__ == '__main__':
  Shutil_Move(Parse_Arguments().parse_args())
