#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount, gluster_evaluate
import os, argparse, errno, re

class Mover:
   "moves files and directories from source to destination"

   def __init__( self, g_args, g_vol ):
      # declare instance variables
      self.src_vol  = g_vol['source']
      self.src_path = g_args['source']['path']
      self.tgt_vol  = g_vol['target']
      self.tgt_path = g_args['target']['path']

      # run program
      self.run_move()

   def run_move( self ):
      try:
         self.tgt_vol.rename( self.src_path, self.tgt_path )
      except OSError as error:
         print error

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
   g_args['source'] = g_parser.parse( p_args['gluster_source'] )
   g_args['target'] = g_parser.parse( p_args['gluster_target'] )

   g_vol = {}
   g_vol['source'] = gluster_mount.Mounter( g_args['source'] )
   g_vol['source'] = g_vol['source'].mount()
   g_vol['target'] = gluster_mount.Mounter( g_args['target'] )
   g_vol['target'] = g_vol['target'].mount()

   g_eval = gluster_evaluate.Evaluator( g_args, g_vol )
   g_args['target']['path'] = g_eval.eval_relation()

   Mover( g_args, g_vol )

if __name__ == '__main__':
   main()
