import os
from shutil import copyfile

filenames = os.listdir('./')
print filenames
for filename in filenames:
    if filename[1] == 'a':
        print filename
        copyfile('./scene_pose.yaml', filename + '/scene_pose.yaml')