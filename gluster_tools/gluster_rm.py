#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, argparse, errno

class Remover:
   "Removes files and directories from source to destination"

   def __init__( self, g_args, g_vol ):
      # declare instance variables
      self.vol  = g_vol
      self.path = g_args['path']

      # run program
      self.run_delete()

   def run_delete( self ):
      try:
         self.remove_file( self.path )
      except OSError as error:
         if error.errno == errno.EISDIR:
            self.remove_dir()
         else: print error

   def remove_file( self, g_tgt ):
      self.vol.unlink( g_tgt )

   def remove_dir( self ):
      root_src_dir = os.path.join( '.', self.path )

      for (src_dir, dirs, files) in self.vol.walk( root_src_dir , topdown=False ):
         for file_ in files:
            src_file = os.path.join( src_dir, file_ )
            self.remove_file( src_file )
         self.vol.rmdir( src_dir )

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
      parser.add_argument( 'gluster_url', nargs='+', help='source file/directory to move from')
      return parser.parse_args().__dict__

def main():
   a_parser  = Parse_Arguments()
   p_args    = a_parser.parse_args()
   g_parser  = gluster_parse.Parser()

   for g_url in p_args['gluster_url']:
       g_args = g_parser.parse( g_url )
       g_vol  = gluster_mount.Mounter( g_args )
       g_vol  = g_mntr.mount()

       Remover( g_args, g_vol )

if __name__ == '__main__':
   main()
