#!/bin/python

import os
import argparse

class Listing:
  "list files and directories"

  def __init__(self,p_args):
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
    for key_arg, val_arg in p_args.__dict__.iteritems():

      # evaluate options, match to arguments
      for key_opt, val_opt in options.iteritems():

        if key_arg == key_opt and val_arg == True:
          val_opt(p_args, dir_list, dir_name)
          itr += 1

    if key_opt == 'none' and itr == 0:
      val_opt(dir_list)

    # if p_args.directories:
    #   self.print_list_dir(p_args, dir_list, dir_name)
    # elif p_args.files:
    #   self.print_list_file(p_args, dir_list, dir_name)
    # else:
    #   self.print_list(dir_list)

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



class Parse_Arguments:
  "parses command-line arguments"

  def __init__(self):
    self.parse_args()

  def parse_args(self):
    parser = argparse.ArgumentParser(description='Lists directory contents, like the unix ls command')
    parser.add_argument(
      'target_directory', nargs='?', default='.'
    , help='directory to list files and directories, uses current directory by default'
    )
    parser.add_argument('-f','--files', action="store_true", help='list only files')
    parser.add_argument('-d','--directories', action="store_true", help='list only directories')
    return parser.parse_args()



Listing(Parse_Arguments().parse_args())
