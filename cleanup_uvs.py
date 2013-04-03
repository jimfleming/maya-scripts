import maya.cmds

def cleanup_uvs():
  uvs = maya.cmds.polyUVSet(q=True, allUVSets=True)

  if not uvs:
    print 'No uvs to delete'
    return
    
  uvs_to_delete = [uv for uv in uvs if uv != 'map1']

  if len(uvs_to_delete) == 0:
    print 'No uvs to delete'
    return
    
  for uv in uvs_to_delete:
    maya.cmds.polyUVSet(delete=True, uvSet=uv)

  print 'Deleted uv sets: %s' % uvs_to_delete
  
cleanup_uvs()