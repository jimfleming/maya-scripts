import maya.cmds as cmds

scenename = cmds.file(query=True, sceneName=True, shortName=True)
scenename = scenename[:-3]
print "Cleaning %s..." % scenename


# Clean history
transforms = cmds.ls(sl=True, transforms=True, visible=True)
for transform in transforms:
    cmds.delete(transform, constructionHistory=True)
print "Cleaned history."


# Unparent everything
def unparent():
    transforms = cmds.ls(sl=True, transforms=True)
    for transform in transforms:
        parent = cmds.listRelatives(transform, path=True, parent=True)
        if parent is not None:
            try:
                cmds.parent(transform, world=True)
            except:
                pass
    print "Unparented."


def emptyGroups():
    # Find empty groups
    deleted = []
    transforms = cmds.ls(sl=True, transforms=True, visible=True)
    for transform in transforms:
        children = cmds.listRelatives(transform, children=True)
        if children is None:
            deleted.append(transform)
    
    # Delete empty groups
    if len(deleted) > 0:
        cmds.delete(deleted)
        print "Deleted empty groups: %s" % deleted

        emptyGroups()

unparent()
emptyGroups()


# Rename pieces
pieces = cmds.ls(sl=True, transforms=True, visible=True)
for i, piece in enumerate(pieces):
    piece = cmds.rename(piece, "%s_Piece%s_LOD0" % (scenename, i))
    
    # Create LOD Group
    pieces[i] = cmds.group(piece, name="%s_Piece%s" % (scenename, i))
    print "Created LOD group"
    
    # Center pivot
    cmds.xform(piece, centerPivots=True)
print "Renamed, centered pieces: %s" % pieces


# Group set
groupName = cmds.group(*pieces, name=scenename)
print "Created parent"

if groupName:
    # Center pivot
    cmds.xform(groupName, centerPivots=True)
    cmds.move(0, 0, 0, groupName, rotatePivotRelative=True)
    print "Cented parent"

print "Done. %s" % scenename
