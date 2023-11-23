import os
import fnmatch

folder_path = 'images'  # Replace with your folder path

for filename in os.listdir(folder_path):
    if fnmatch.fnmatch(filename, "*Copy*"):
        os.remove(os.path.join(folder_path, filename))
