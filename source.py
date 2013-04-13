import sys
import os
 
def source(module):
  f = os.path.basename(module)
  path = os.path.dirname(module)

  tokens = f.split('.')
  module_name = tokens[0]

  # Check if directory is really a directory
  if os.path.exists(path):
    # Check if the file directory already exists in the sys.path array
    paths = sys.path
    pathfound = False
    for p in paths:
      if path == p:
        pathfound = True

  # If the dirrectory is not part of sys.path add it
  if not pathfound:
    sys.path.append(path)

  # exec works like MEL's eval but you need to add in globals() 
  # at the end to make sure the file is imported into the global 
  # namespace else it will only be in the scope of this function
  exec('import ' + module_name) in globals()

  # reload the file to make sure its up to date
  exec('reload(' + module_name + ')') in globals()

  # This returns the namespace of the file imported
  return module_name
 
# When you import a file you must give it the full path
source('/Users/Documents/3D/maya/path_to_directory/name_of_python_file.py')
