#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, sys, argparse, errno, re

class Copier:
   "copies files and directories across gluster volumes"

   def __init__( self, p_args, g_args, g_mount ):
      # declare instance variables
      self.src_mount = g_mount['source']
      self.src_path  = g_args['source']['path']
      self.tgt_mount = g_mount['target']
      self.tgt_path  = g_args['target']['path']

      #run program
      self.eval_exist()
      self.run_copy()

   def eval_exist( self ):
      if not self.src_mount.exists(self.src_path):
         print 'error:', self.src_path, 'does not exist'
         raise SystemExit

      if self.tgt_mount.exists(self.tgt_path):
         self.eval_file()

      elif self.src_mount.isfile( self.src_path ):
         self.create_file( self.tgt_path)

   def eval_file( self ):
      if self.tgt_mount.isfile( self.tgt_path ):
         print 'overwrite?',
         response = raw_input()
         try:
            re.match( '^y',response.lower() ).group()
         except:
            raise SystemExit

   def create_file( self, path ):
      self.tgt_mount.open( path, os.O_CREAT )

   def run_copy( self ):
      try:
         self.copy_file( self.src_path, self.tgt_path)

      except OSError as error:
         if error.errno == errno.EISDIR:
           self.copy_dir() 
         else: print error

   def copy_file( self, source, target ):
      file_src = self.src_mount.open(
         source, os.O_RDONLY
      )
      file_tgt = self.tgt_mount.open(
         target, os.O_WRONLY
      )

      try:
         file_read  = file_src.read(128000)
         file_write = file_tgt.write(file_read)

      except:
         pass

      file_src.close()
      file_tgt.close()

   def copy_dir( self ):
      root_src_dir = self.src_path
      root_tgt_dir = self.tgt_path
      perm_dir=0755

      if not self.tgt_mount.exists(root_tgt_dir):
         self.tgt_mount.mkdir(root_tgt_dir,perm_dir)

      for (src_dir, dirs, files) in self.src_mount.walk( root_src_dir ):
         tgt_dir =  src_dir.replace( root_src_dir, root_tgt_dir )
         if not self.tgt_mount.exists( tgt_dir ):
            self.tgt_mount.mkdir( tgt_dir, perm_dir )
         for file_ in files:
            src_file = os.path.join( src_dir, file_ )
            tgt_file = os.path.join( tgt_dir, file_ )

            if self.tgt_mount.exists( tgt_file ):
               self.tgt_mount.unlink( tgt_file )

            self.create_file( tgt_file )
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
  g_args['source']   = g_parser.parse(p_args['gluster_source'])
  g_args['target']   = g_parser.parse(p_args['gluster_target'])

  gluster = {}
  gluster['source'] = gfapi.Volume(g_args['source']['host'], g_args['source']['volume'])
  gluster['source'].mount()
  gluster['target'] = gfapi.Volume(g_args['target']['host'], g_args['target']['volume'])
  gluster['target'].mount()

  Copier(p_args, g_args, gluster)

if __name__ == '__main__':
  main()
