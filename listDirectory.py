#!/usr/bin/python

import os
import argparse

class Listing:
  "list files and directories"

  def __init__(self):
    self.run_list()

  def run_list(self):
    args = self.parse_args()
    dir_list = self.get_dir(args)
    dir_name = args.target_directory
    if args.directories:
      self.print_list_dir(args, dir_list, dir_name)
    elif args.files:
      self.print_list_file(args, dir_list, dir_name)
    else:
      self.print_list(dir_list)

  def parse_args(self):
    parser = argparse.ArgumentParser(description='This is a demo script for Podomatic')
    parser.add_argument('target_directory', help='directory to list files and directories')
    parser.add_argument('-f','--files', help='list only files', action="store_true")
    parser.add_argument('-d','--directories', help='list only directories', action="store_true")
    return parser.parse_args()

  def get_dir(self, p_args):
    dir_name = p_args.target_directory
    dir_list = os.listdir(dir_name)
    return dir_list

  def print_list_dir(self, p_args, p_dir_list, p_dir_name):
    for li in p_dir_list:
      if os.path.isdir(os.path.join(p_dir_name, li)):
        print li

  def print_list_file(self, p_args, p_dir_list, p_dir_name):
    dir_name = p_args.target_directory
    for li in p_dir_list:
      if os.path.isfile(os.path.join(p_dir_name, li)):
        print li

  def print_list(self, p_dir_list):
    for li in p_dir_list:
        print li

Listing()
