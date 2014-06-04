#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount, gluster_evaluate
import os, sys, argparse, errno, re

class Copier:
   "copies files and directories across gluster volumes"

   def __init__( self, p_args, g_args, g_vol ):
      # declare instance variables
      self.src_vol  = g_vol['source']
      self.src_path = g_args['source']['path']
      self.tgt_vol  = g_vol['target']
      self.tgt_path = g_args['target']['path']

      #run program
      self.run_copy()

   def run_copy( self ):
      if self.src_vol.isfile( self.src_path ):
         self.copy_file( self.src_path, self.tgt_path)

      elif self.src_vol.isdir( self.src_path ):
         self.copy_dir()

   def pass_link( self, target ):
      print "symbol link '%s' skipped" % target

   def copy_file( self, source, target ):
      if self.src_vol.islink( source ):
         self.pass_link( source )

      elif self.tgt_vol.exists( target ):
         self.tgt_vol.open( target, os.O_TRUNC )

      else:
         self.tgt_vol.open( target, os.O_CREAT )

      try:
         file_src = self.src_vol.open(
            source, os.O_RDONLY
         )
         file_tgt = self.tgt_vol.open(
            target, os.O_WRONLY
         )
         size = self.src_vol.getsize(source)
         file_read  = file_src.read(size)
         file_write = file_tgt.write(file_read)
         file_src.close()
         file_tgt.close()

      except:
         pass

   def copy_dir( self ):
      root_src_dir = self.src_path
      root_tgt_dir = self.tgt_path
      perm_dir=0755

      if not self.tgt_vol.exists(root_tgt_dir):
         self.tgt_vol.mkdir(root_tgt_dir,perm_dir)

      for (src_dir, dirs, files) in self.src_vol.walk( root_src_dir ):
         tgt_dir =  src_dir.replace( root_src_dir, root_tgt_dir )
         if not self.tgt_vol.exists( tgt_dir ):
            self.tgt_vol.mkdir( tgt_dir, perm_dir )
         for file_ in files:
            src_file = os.path.join( src_dir, file_ )
            tgt_file = os.path.join( tgt_dir, file_ )

            self.copy_file( src_file, tgt_file )

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
        description = 'copy files/directories from source to destination'
    )
    parser.add_argument( 'gluster_source', help='source file/directory to copy from')
    parser.add_argument( 'gluster_target', help='target file/directory to copy to')
    return parser.parse_args().__dict__

def main():
   a_parser = Parse_Arguments()
   p_args   = a_parser.parse_args()
   g_parser = gluster_parse.Parser()

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

   Copier( p_args, g_args, g_vol )

if __name__ == '__main__':
  main()
