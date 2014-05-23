#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, argparse, errno, re

class Mover:
   "moves files and directories from source to destination"

   def __init__( self, g_args, gluster ):
      self.eval_exist( g_args, gluster )
      self.run_move( g_args, gluster )

   def eval_exist( self, g_args, gluster ):
      if not gluster['source'].exists(g_args['source']['path']):
         print 'error:', g_args['source']['path'], 'does not exist'
         raise SystemExit
      if gluster['target'].exists(g_args['target']['path']):
         self.eval_file( g_args, gluster )
      elif gluster['source'].isfile(g_args['source']['path']) or \
      gluster['source'].isdir(g_args['source']['path']):
         gluster['target'].rename(
            g_args['source']['path']
         ,  g_args['target']['path']
         )
         raise SystemExit

   def eval_file( self, g_args, gluster ):
      if gluster['target'].isfile(g_args['target']['path']):
         print 'overwrite?',
         response = raw_input()
         try:
            re.match( '^y', response.lower() )
         except:
            raise SystemExit

   def create_file( self, g_tgt, gluster ):
      gluster['target'].open(g_tgt, os.O_CREAT)

   def run_move( self, g_args, gluster ):
      g_src = g_args['source']['path']
      g_tgt = g_args['target']['path']

      try:
         self.move_file( g_src, g_tgt,  gluster )
      except OSError as error:
         if error.errno == errno.EISDIR:
            self.move_dir( g_args, gluster )
         else: print error

   def move_file( self, g_src, g_tgt, gluster ):
      gluster['source'].unlink(g_tgt)
      gluster['target'].rename(g_src, g_tgt)

   def move_dir( self, g_args, gluster ):
      root_src_dir = g_args['source']['path']
      root_tgt_dir = g_args['target']['path']
      perm_dir=0755

      if not gluster['target'].exists( root_tgt_dir ):
         gluster['target'].mkdir( g_args['target']['path'] )

      for (src_dir, dirs, files) in gluster['source'].walk( root_src_dir ,topdown=False):
         tgt_dir = src_dir.replace( root_src_dir, root_tgt_dir )
         if not gluster['target'].exists( tgt_dir ):
            gluster['target'].mkdir( tgt_dir, perm_dir )
         for file_ in files:
            src_file = os.path.join( src_dir, file_ )
            tgt_file = os.path.join( tgt_dir, file_ )

            if gluster['target'].exists( tgt_file ):
               gluster['target'].unlink( tgt_file )

            self.create_file( tgt_file, gluster )
            self.move_file( src_file, tgt_file, gluster )

         gluster['source'].rmdir( src_dir )

class Parse_Arguments:
   """
   parse arguments for source file/directory and
   target file/directory
   """

   def __init__( self ):
      self.parse_args()

   def parse_args( self ):
      """
      parse arguments for source file/directory and
      target file/directory
      """
      parser = argparse.ArgumentParser(
         description = 'move files/directories from source to destination'
      )
      parser.add_argument( 'gluster_source', help='source file/directory to move from')
      parser.add_argument( 'gluster_target', help='target file/directory to move to')
      return parser.parse_args().__dict__

def main():
   a_parser = Parse_Arguments()
   g_parser = gluster_parse.Parser()
   p_args   = a_parser.parse_args()
   g_args   = {}
   g_args['source']   = g_parser.parse(p_args['gluster_source'])
   g_args['target']   = g_parser.parse(p_args['gluster_target'])

   gluster = {}
   gluster['source'] = gfapi.Volume(g_args['source']['host'], g_args['source']['volume'])
   gluster['target'] = gfapi.Volume(g_args['target']['host'], g_args['target']['volume'])
   gluster['source'].mount()
   gluster['target'].mount()

   Mover(g_args, gluster)

if __name__ == '__main__':
   main()
