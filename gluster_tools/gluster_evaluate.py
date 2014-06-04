#!/usr/bin/python

import os

class Evaluator:
   """evaluates the source and directory file type"""

   def __init__( self, g_args, g_vol ):
      # declare instance variables
      self.src_vol  = g_vol['source']
      self.src_path = g_args['source']['path']
      self.tgt_vol  = g_vol['target']
      self.tgt_path = g_args['target']['path']
      self.src_type = None
      self.tgt_type = None

      #run program
      self.run_eval()

   def run_eval( self ):
      self.eval_src_type()
      self.eval_tgt_type()
      # self.eval_relation()

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
         # ask user whether to overwrite file/dir
         self.eval_overwrite()

      elif self.src_type == 'file' and self.tgt_type == 'dir':
         # ensure source file is copied/moved INTO target directory
         self.mod_path()

      elif self.src_type == 'dir' and self.tgt_type == 'dir':
         # ensure source directory is copied/moved INTO target directory
         self.mod_path()

      elif self.src_type == 'dir' and self.tgt_type == 'file':
         # cannot copy a source directory into a target file
         print "error: cannot overwrite non-directory '%s' with directory '%s'" % ( self.tgt_path, self.src_path )
         raise SystemExit

      return self.tgt_path

   def mod_path( self ):
      # print 'old path:', self.tgt_path
      path_name = os.path.basename( self.src_path )
      self.tgt_path =  os.path.join( self.tgt_path, path_name )
      if self.tgt_vol.isfile( self.tgt_path ) \
      or self.tgt_vol.isdir( self.tgt_path ):
         self.eval_overwrite()
      # print 'new path:', self.tgt_path

   def eval_overwrite( self ):
      print 'overwrite?',
      response = raw_input()
      try:
         re.match( '^y',response.lower() ).group()
      except:
         raise SystemExit

def main():
   pass

if __name__ == '__main__':
   main()
