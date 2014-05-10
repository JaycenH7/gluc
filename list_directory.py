#!/bin/python

import os, argparse, stat, sys, time
from pwd import getpwuid

class Listing:
  "list files and directories"

  def __init__(self,p_args):
    if p_args.long:
      self.run_long(p_args)
    else:
      self.run_list(p_args)

  def run_list(self,p_args):
    dir_list = self.get_dir(p_args)
    dir_name = p_args.target_directory
    options = {
      'directories' : self.print_list_dir,
      'files'       : self.print_list_file,
      'none'        : self.print_list
    }

    # evaluate arguments
    itr = 0
    for key, val in p_args.__dict__.iteritems():
      if val == True:
        options[key](p_args, dir_list, dir_name)
        itr += 1

    if itr == 0:
        options['none'](dir_list)

  def get_dir(self, p_args):
    dir_name = p_args.target_directory
    dir_list = os.listdir(dir_name)
    return dir_list

  def print_list_dir(self, p_args, p_dir_list, p_dir_name):
    for li in p_dir_list:
      if os.path.isdir(os.path.join(p_dir_name, li)):
        print li

  def print_list_file(self, p_args, p_dir_list, p_dir_name):
    for li in p_dir_list:
      if os.path.isfile(os.path.join(p_dir_name, li)):
        print li

  def print_list(self, p_dir_list):
    for li in p_dir_list:
      print li

  def run_long(self, p_args):
    stat_info = os.lstat(p_args.target_directory)
    self.check_stat(stat_info)
    self.print_long_more(stat_info, p_args)

  def check_stat(self, p_stat_info):
    type_dict = {
        stat.S_ISDIR:'d',
        stat.S_ISLNK:'l',
        stat.S_ISCHR:'c',
        stat.S_ISSOCK:'s',
        stat.S_ISREG:'-'
    }

    perm_dict = {
        stat.S_IRUSR:'r', stat.S_IWUSR:'w', stat.S_IXUSR:'x',
        stat.S_IRGRP:'r', stat.S_IWGRP:'w', stat.S_IXGRP:'x',
        stat.S_IROTH:'r', stat.S_IWOTH:'w', stat.S_IXOTH:'x'
    }

    for key, val in sorted(type_dict.iteritems()):
      if key(p_stat_info.st_mode):
        sys.stdout.write(val)

    for key, val in sorted(perm_dict.iteritems(), reverse=True):
      if bool(p_stat_info.st_mode & key):
        sys.stdout.write(val)
      else:
        sys.stdout.write('-')


  def print_long_more(self, p_stat_info, p_args):
    print '',
    print p_stat_info.st_nlink,
    print getpwuid(p_stat_info.st_uid).pw_name,
    print p_stat_info.st_size,
    print time.strftime(
      "%B %d %H:%M"
    , time.localtime(p_stat_info.st_mtime)
    ),
    print p_args.target_directory
    sys.stdout.write('\n')



class Parse_Arguments:
  "parses command-line arguments"

  def __init__(self):
    self.parse_args()

  def parse_args(self):
    parser = argparse.ArgumentParser(description='Lists directory contents, like the unix ls command')
    parser.add_argument(
      'target_directory', nargs='?', default='.'
    , help='directory to list files and directories\
    , uses current directory by default'
    )
    parser.add_argument('-f','--files', action="store_true"
    , help='list only files')
    parser.add_argument('-d','--directories', action="store_true"
    , help='list only directories')
    parser.add_argument( '-l', '--long', action="store_true", help='long listing format'
    )
    return parser.parse_args()



Listing(Parse_Arguments().parse_args())
