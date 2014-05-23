#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, argparse, errno, re

class Remover:
   "Removes files and directories from source to destination"

   def __init__( self, g_args, gluster ):
      self.run_delete( g_args, gluster )

   def run_delete( self, g_args, gluster ):
      try:
         self.remove_file( g_args['path'], gluster )
      except OSError as error:
         if error.errno == errno.EISDIR:
            self.remove_dir( g_args, gluster )
         else: print error

   def remove_file( self, g_tgt, gluster ):
      gluster.unlink( g_tgt )

   def remove_dir( self, g_args, gluster ):
      root_src_dir = os.path.join( '.', g_args['path'])

      for (src_dir, dirs, files) in gluster.walk( root_src_dir ,topdown=False):
         for file_ in files:
            src_file = os.path.join( src_dir, file_ )
            self.remove_file( src_file, gluster )
         gluster.rmdir( src_dir )

class Parse_Arguments:
   """
   parse arguments for source file/directory and
   target file/directory
   """

   def __init__( self ):
      self.parse_args()

   def parse_args( self ):
      parser = argparse.ArgumentParser(
         description = 'remove files/directories from source to destination'
      )
      parser.add_argument( 'gluster_url' , help='source file/directory to move from')
      return parser.parse_args().__dict__

def main():
   a_parser = Parse_Arguments()
   g_parser = gluster_parse.Parser()
   p_args   = a_parser.parse_args()
   g_args   = g_parser.parse(p_args['gluster_url'])

   gluster = gfapi.Volume(g_args['host'], g_args['volume'])
   gluster.mount()

   Remover(g_args, gluster)

if __name__ == '__main__':
   main()
