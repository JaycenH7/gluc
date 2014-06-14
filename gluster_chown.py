#!/usr/bin/python

import gfapi
import os, sys, argparse, pwd
import gluster_parse, gluster_mount

class Chown:
   """
   Change file owner and group
   """

# process
# 1. check if uid and/or guid is parsed
# 2. check given uid/gid exists
# 2. check assumed parameters
#   a. if uid given, find file's original gid
#   b. if gid given, find file's original uid
# 3. run program

# allow users and group names to be input by
# using reading '/etc/passwd'
#   then translate a user/group to uid/gid

# use lstat to get current user/group to set
# as default value if not provided

# require group id to be prepositioned with colon
# or ':'

# create 1st form:
#    change owner for one file
#    change group for one file

# create 2nd form:
#    change owner and group for multiple files

# create 3rd form:
#    change owner and group using a reference file

# arguments
#     --reference=RFILE
#     -r, --recursive

# gfapi
#     use api method to remove directories
#     fchown( uid, gid )

   def __init__( self, p_args, g_args, g_vol ):
      # declare instance variables
      self.p_args    = p_args
      self.vol       = g_vol
      self.path      = g_args['path']
      self.owner     = p_args['owner']
      self.group     = p_args[':group']

      # run program
      self.check_path()
      self.check_pwd()
      self.check_stat()
      self.run_chown()

   def check_path( self ):
      if not self.vol.exists( self.path ):
         print "error:'%s' does not exist" % self.path
         raise SystemExit

   def check_pwd( self ):
       print 'owner:', self.owner
       print 'group', self.group

   def check_uid( self ):
       """
       find uid/gid in passwd database
       """
       pass
        # if 'owner' is integer then check user id exists
        # else if 'owner' is string, convert user name to
        # uid
#        passwd = pwd.getpwall()
#        try:
#           int( self.owner )
#           self.owner_is_num = True
#        except:
#           self.owner_is_num = False
#        print 'owner is num:', self.owner_is_num
#
#        for user in passwd:
#            if self.owner_is_num == True:
#                if user.pw_uid == int(self.owner):
#                    print user.pw_name, 'exists'
#                    return user.pw_name
#            else:
#                if user.pw_name == self.owner:
#                    print user.pw_name, 'exists'
#                    return user.pw_name
#
#        print "error: '%s' does not exist" % self.owner

   def check_guid( self ):
       """
       return user/group if string provided
       """
       pass

   def check_stat( self ):
       """
       get the default uid/gid from the target file
       """
       pass

   def run_chown( self ):
       pass
   #     try:
   #        self.vol.chown(
   #          self.path
   #        , int(self.p_args['OWNER'])
   #        , int(self.p_args[':GROUP'])
   #        )
   #     except IOError as error:
   #        print error

class Parse_Arguments:
   """
   parse arguments for source file/directory and
   target file/directory
   """

   def __init__( self ):
      pass

  def group( self ):
      pass


   def parse_args( self ):
      parser = argparse.ArgumentParser(description='Lists directory contents, like the unix ls command')
      parser.add_argument('owner', nargs='?', help='owner to change file to')
      parser.add_argument(':group', nargs='?', help='group to change file to')
      parser.add_argument('owner', help='owner to change file to')
      parser.add_argument(':group', help='group to change file to')
      parser.add_argument('gluster_url', nargs='+', help='file to change owner and/or group')
      return parser.parse_args().__dict__

def main():
   a_parser  = Parse_Arguments()
   p_args    = a_parser.parse_args()
   g_parser  = gluster_parse.Parser()
   for g_url in p_args['gluster_url']:
       g_args = g_parser.parse( g_url )
       g_vol  = gluster_mount.Mounter( g_args )
       g_vol  = g_vol.mount()

       Chown( p_args, g_args, g_vol )

if __name__ == '__main__':
   main()
