#!/usr/bin/python

import argparse

class Copier:
  "copies files and directories from source to destination"

  def __init__(self,p_args):
    file_read = file(p_args.source,'r').read()
    file(p_args.destination,'w').write(file_read)

class Parse_Arguments:
  "parses command-line arguments"

  def __init__(self):
    self.parse_args()

  def parse_args(self):
    parser = argparse.ArgumentParser(description='copy files/directories from source to destination')
    parser.add_argument( 'source'
    , help='source file/directory to copy from'
    )
    parser.add_argument( 'destination', default='.'
    , help='destination file/directory to copy to'
    )
    return parser.parse_args()

Copier(Parse_Arguments().parse_args())
