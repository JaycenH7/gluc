#!/usr/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, sys, argparse, errno, re

class Copier:
   "copies files and directories across gluster volumes"

   def __init__( self, p_args, g_args, g_vol ):
      # declare instance variables
      self.src_vol  = g_vol['source']
      self.src_path = g_args['source']['path']
      self.tgt_vol  = g_vol['target']
      self.tgt_path = g_args['target']['path']
      self.src_type = None
      self.tgt_type = None

      #run program
      self.eval_src_type()
      self.eval_tgt_type()
      self.eval_relation()
      self.run_copy()

   def eval_src_type( self ):
      dict_type = {
         self.src_vol.isfile : 'file'
      ,  self.src_vol.isdir  : 'dir'
      }

      if not self.src_vol.exists( self.src_path ):
         print "error: '%s' does not exist" % self.src_path
         raise SystemExit

      for key, val in sorted( dict_type.iteritems() ):
         if key( self.src_path ):
            self.src_type = val

   def eval_tgt_type( self ):
      dict_type = {
         self.tgt_vol.isfile : 'file'
      ,  self.tgt_vol.isdir  : 'dir'
      }

      for key, val in sorted( dict_type.iteritems() ):
         if key( self.tgt_path ):
            self.tgt_type = val

   def eval_relation( self ):
      if self.src_path == self.tgt_path:
         # cannot copy to self
         print "'%s' and '%s' are the same path" % ( self.tgt_path, self.src_path )
         raise SystemExit

      elif self.src_type == 'file' and self.tgt_type == 'file':
         self.eval_overwrite()

      elif self.src_type == 'file' and self.tgt_type == 'dir':
         # ensure source file is copied/moved INTO target directory
         src_filename =  os.path.basename(self.src_path)
         self.tgt_path =  os.path.join( self.tgt_path, src_filename )
         if self.tgt_vol.isfile( self.tgt_path ):
            self.eval_overwrite()

      elif self.src_type == 'dir' and self.tgt_type == 'dir':
         # ensure source directory is copied/moved INTO target directory
         src_dirname =  os.path.basename(self.src_path)
         self.tgt_path =  os.path.join( self.tgt_path, src_dirname )
         if self.tgt_vol.isdir( self.tgt_path ):
            self.eval_overwrite()

      elif self.src_type == 'dir' and self.tgt_type == 'file':
         # cannot copy a source directory into a target file
         print "error: cannot overwrite non-directory '%s' with directory '%s'" % ( self.tgt_path, self.src_path )
         raise SystemExit

   def eval_overwrite( self ):
      print 'overwrite?',
      response = raw_input()
      try:
         re.match( '^y',response.lower() ).group()
      except:
         raise SystemExit

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
         file_read  = file_src.read(128000)
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

   Copier( p_args, g_args, g_vol )

if __name__ == '__main__':
  main()
