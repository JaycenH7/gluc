import gfapi
import stat
import sys
import os

gluster = gfapi.Volume('Pod-VM','gv0')
gluster.mount()

"""make test directories and files"""
# gluster.mkdir('dir1', 0755)
# gluster.open('file1',0755)
# gluster.open('dir2/subfile4',0755)
# gluster.open('dir2/subfile5',0755)
# gluster.open('dir2/subfile6',0755)

# print gluster.isfile('file1')

# for li in dir(gluster):
#   print li

# gfapi.File.read(gluster.open('file1', 0777))
# gluster.open('file1', 0777)

# myfile1 = gluster.open('file1', os.O_RDONLY)
# myfile2 = gluster.open('fileabc', os.O_WRONLY)
# myfile.write('hahahaha')
# mywrite = myfile.write('hahaha')
# print mywrite

# myread = myfile1.read(128000)
# mywrite = myfile2.write(myread)
# print mywrite
# myfile1.close()
# myfile2.close()

print gluster.exists('dir1')
