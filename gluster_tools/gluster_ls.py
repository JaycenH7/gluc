#!/bin/python

import gfapi
import gluster_parse, gluster_mount
import os, argparse, stat, sys, time
from pwd import getpwuid

class Listing:
  """list files and directories in a gluster volume"""

  def __init__( self, p_args, g_args, gluster ):
    for li in gluster.listdir(g_args['path']):
      if p_args['long']:
        self.print_stat(li, g_args, gluster)
      else:
        print li

  def print_stat(self, item, g_args, gluster):
    """print permissions, owner and other info of a given file/directory"""
    file_ = os.path.join(g_args['path'], item)
    stat_info = gluster.lstat(file_)
    self.stat_type(stat_info)
    self.stat_perm(stat_info)
    self.stat_misc(stat_info, item)

  def stat_type(self, stat_info):
    """print file type"""
    type_dict = {
        stat.S_ISDIR:'d',
        stat.S_ISLNK:'l',
        stat.S_ISCHR:'c',
        stat.S_ISSOCK:'s',
        stat.S_ISREG:'-'
    }

    for key, val in sorted(type_dict.iteritems()):
      if key(stat_info.st_mode):
        sys.stdout.write(val)

  def stat_perm(self, stat_info):
    """print file permissions"""
    perm_dict = {
        stat.S_IRUSR:'r', stat.S_IWUSR:'w', stat.S_IXUSR:'x',
        stat.S_IRGRP:'r', stat.S_IWGRP:'w', stat.S_IXGRP:'x',
        stat.S_IROTH:'r', stat.S_IWOTH:'w', stat.S_IXOTH:'x'
    }

    for key, val in sorted(perm_dict.iteritems(), reverse=True):
      if bool(stat_info.st_mode & key):
        sys.stdout.write(val)
      else:
        sys.stdout.write('-')

  def stat_misc(self, stat_info, stat_name):
    """print file size, hard links and last time file was modified"""
    if stat_info.st_size > 102400:
      st_size = str(format(stat_info.st_size/1024000.0,'.1f'))+"M"
    elif stat_info.st_size > 10240:
      st_size = str(format(stat_info.st_size/1024.0,'.0f'))+"K"
    elif stat_info.st_size > 1024:
      st_size = str(format(stat_info.st_size/1024.0,'.1f'))+"K"
    else:
      st_size = stat_info.st_size
    fmt = '{:<0} {:<1} {:<4} {:<4} {:<4} {:<4}'
    print(fmt.format(
      '',
      stat_info.st_nlink,
      getpwuid(stat_info.st_uid).pw_name,
      st_size,
      time.strftime(
        "%b %d %H:%M"
      , time.localtime(stat_info.st_mtime)
      ),
      stat_name
    ))

class Parse_Arguments:
  """
  parse arguments for source file/directory and
  target file/directory
  """

  def __init__( self ):
    self.parse_args()

  def parse_args(self):
    parser = argparse.ArgumentParser(description='Lists directory contents, like the unix ls command')
    parser.add_argument('gluster_url', help='gluster volume to list files and directories')
    parser.add_argument('-l', '--long', action="store_true", help='long listing format'
    )
    return parser.parse_args().__dict__

def main():
  a_parser = Parse_Arguments()
  g_parser = gluster_parse.Parser()
  p_args   = a_parser.parse_args()
  g_args   = g_parser.parse(p_args['gluster_url'])

  gluster = gfapi.Volume(g_args['host'], g_args['volume'])
  gluster.mount()

  Listing(p_args, g_args, gluster)

if __name__ == '__main__':
  main()
