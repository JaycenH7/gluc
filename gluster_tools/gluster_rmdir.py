#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, sys, argparse

class RemoverDir:
   """
   Remove empty directories
   """

# create 1st form:
#    removes one directory
#    removes multiple directories (-p)

# arguments
#     -p, --parents

# gfapi
#     use api method to remove directories
#     rmdir( path )
#        - remove one directory
#     rmtree( path, ignore_errors=False, onerorr=None )
#        - remove directory tree


   def __init__( self, p_args, g_args, g_vol ):
      # declare instance variables
      self.p_args    = p_args
      self.vol       = g_vol
      self.path      = g_args['path']

      # run program
      self.check_exist()
      self.run_link()

   def check_exist( self ):
      if not self.vol.exists( self.path ):
         print "error:'%s' does not exist" % self.path
         raise SystemExit

   def run_link( self ):
      pass

class Parse_Arguments:
   """
   parse arguments for source file/directory and
   target file/directory
   """

   def __init__( self ):
      pass

   def parse_args( self ):
      parser = argparse.ArgumentParser(description='Lists directory contents, like the unix ls command')
      parser.add_argument('DIRECTORY', nargs='+', help='directories to be removed')
      parser.add_argument('-p', '--parents', action="store_true", help='remove DIRECTORY and its ancestors')
      return parser.parse_args().__dict__

def main():
   a_parser  = Parse_Arguments()
   p_args    = a_parser.parse_args()
   g_parser  = gluster_parse.Parser()
   for g_url in p_args['gluster_url']:
       g_args = g_parser.parse( g_url )
       g_vol  = gluster_mount.Mounter( g_args )
       g_vol  = g_vol.mount()

       Link( p_args, g_args, g_vol )

if __name__ == '__main__':
   main()
