import os, shutil, errno

source = os.getcwd()
target = 'web'

if os.path.exists(target):
  shutil.rmtree(target)

try:
  shutil.copytree(source, target)
except OSError as exc:
  if exc.errno == errno.ENOTDIR:
    shutil.copy(source, target)
  else: raise
