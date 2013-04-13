from undoable import undoable
import maya.cmds

def prep(transform):
  # Select the transform
  cmds.select(transform, replace=True)
  # Fix normals
  cmds.polySetToFaceNormal()
  # Delete history
  cmds.delete(constructionHistory=True)
  # Scale 10x
  cmds.scale(centerPivot=True, scaleXYZ=10)
  # Freeze transformations
  cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=1)

def cleanup(transform):
  # Select the transform
  cmds.select(transform, replace=True)
  # Scale 1/10x
  cmds.scale(centerPivot=True, scaleXYZ=1/10)
  # Freeze transformations
  cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=1)

def cut_one_with_one(cutter, target):
  print 'Cutting 1:1 %s with %s' % (target, cutter)

  # Duplicate targets
  targetA = cmds.duplicate(target, returnRootsOnly=True)[0]
  targetB = cmds.duplicate(target, returnRootsOnly=True)[0]

  prep(targetA)
  prep(targetB)

  cmds.delete(target)

  # Set up cutters
  cutterA = cmds.duplicate(cutter, returnRootsOnly=True)[0]
  cutterB = cmds.duplicate(cutter, returnRootsOnly=True)[0]

  prep(cutterA)
  prep(cutterB)

  # Flip second cutter's normals
  cmds.polyNormal(cutterB, normalMode=0, userNormalMode=0, constructionHistory=0)

  # Perform intersections
  newTargetA = cmds.polyBoolOp(cutterA, targetA, op=3, constructionHistory=False)[0]
  newTargetB = cmds.polyBoolOp(cutterB, targetB, op=3, constructionHistory=False)[0]

  return [newTargetA, newTargetB]

def cut_many_with_one(cutter, targets):
  newTargets = []
  for target in targets:
    newTargets += cut_one_with_one(cutter, target)
  return newTargets

def cut_one_with_many(cutters, target):
  targets = [target]
  for i, cutter in enumerate(cutters):
    targets = cut_many_with_one(cutter, targets)
  return targets

@undoable
def cut_with_selection():
  sel = cmds.ls(selection=True)
  if len(sel) != 2:
    print 'Need to select at least two objects: cutters then target'

  target = sel[-1]
  cutters = sel[:-1]

  results = cut_one_with_many(cutters, target)
  for result in results:
    cleanup(result)
  cmds.group(results, world=True, name="patient")

cut_with_selection()
