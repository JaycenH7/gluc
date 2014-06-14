#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, sys, argparse, re

class Symlink:
   """
   create a symbolic link to TARGET or create multiple symbolic
   links to TARGETs in a directory
   """

# create 1st form: 
#     create one link in current directory
#     create the link with 'link_name'

# create 2nd form:
#     create multiple links to a directory

# only check if link already exists

# arguments
#     -t, --target-directory=DIRECTORY
#     -T, --no-target-directory

# gfapi
#     use api method to create links
#     symlink( source, link_name )

   def __init__( self, p_args, g_args, g_vol ):
      # declare instance variables
      self.p_args    = p_args
      self.vol       = g_vol
      self.path      = g_args['path']

      # run program
      self.eval_overwrite()
      self.run_link()

   def eval_overwrite( self ):
      if self.vol.exists( self.path ):
         print 'overwrite?'
         response = raw_input()
         try:
            re.match( '^y', response.lower() ).group()
         except:
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
      parser.add_argument('TARGET', nargs='+', help='gluster volume to list files and directories')
      parser.add_argument('LINK_NAME', nargs='?', help='gluster volume to list files and directories')
      parser.add_argument('-t', '--target-directory', action="store_true", help='specifcy the DIRECTORY to create the links')
      parser.add_argument('-T', '--no-target-directory', action="store_true", help='treat LINK_NAME as a normal file')
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
