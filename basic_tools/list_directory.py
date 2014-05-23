#!/bin/python

import os, argparse, stat, sys, time
from pwd import getpwuid

class Listing:
  """list files and directories"""

  def __init__(self,p_args):
    opt = self.run_options(p_args)
    if p_args.long:
      self.run_long(p_args,opt)
    else:
      self.run_default(p_args,opt)

  def run_options (self,p_args):
    """instantiate options hash from given arguments"""
    opt = {}
    opt['dir_name'] = p_args.target_directory
    opt['dir_list'] = os.listdir(p_args.target_directory)
    return opt

  def run_default(self, p_args, opt):
    """default(short) listing format of files/directories"""
    print_dict = {
      'directories' : self.path_dir,
      'files'       : self.path_file
    }

    if p_args.long:
      p_args.__dict___['long'] = False
      long_arg = True

    itr = 0
    for key, val in p_args.__dict__.iteritems():
      if val == True:
        itr += 1
        for li in opt['dir_list']:
          if print_dict[key](li,opt):
            print li

    if itr == 0:
      for li in opt['dir_list']:
        print li

  def path_dir(self, dir_, opt):
    """return if directory content is a directory"""
    if os.path.isdir(os.path.join(opt['dir_name'],dir_)):
      return True

  def path_file(self, file_, opt):
    """return if directory content is a file"""
    if os.path.isfile(os.path.join(opt['dir_name'],file_)):
      return True

  def run_long(self, p_args, opt):
    """long listing format of files/directories"""
    print_dict = {
      'directories' : self.path_dir,
      'files'       : self.path_file
    }

    p_args.__dict__['long']=False

    itr = 0
    for key, val in p_args.__dict__.iteritems():
      if val == True:
        itr += 1
        for li in opt['dir_list']:
          if print_dict[key](li,opt):
            self.print_stat(li,opt)

    if itr == 0:
      for li in opt['dir_list']:
        self.print_stat(li,opt)

  def print_stat(self,item,opt):
    """print permissions, owner and other info of a given file/directory"""
    file = os.path.join(opt['dir_name'],item)
    stat_info = os.lstat(file)
    self.check_stat(stat_info)
    self.print_long_more(stat_info, item)

  def check_stat(self, stat_info):
    """check permissions and file type"""
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
      if key(stat_info.st_mode):
        sys.stdout.write(val)

    for key, val in sorted(perm_dict.iteritems(), reverse=True):
      if bool(stat_info.st_mode & key):
        sys.stdout.write(val)
      else:
        sys.stdout.write('-')

  def print_long_more(self, stat_info, stat_name):
    """print file size, hard links and last time file was modified"""
    if stat_info.st_size > 10240:
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


if __name__ == '__main__':
  Listing(Parse_Arguments().parse_args())
