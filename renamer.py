from maya import cmds

# make a dictionary of suffixes
SUFFIXES = {
    "mesh": "Geo",
    "nurbsCurve": "Crv",
    "aiAreaLight": "area_Lit",
    "aiSkyDomeLight": "dome_Lit",
    "RedshiftPhysicalLight": "phy_Lit",
    "RedshiftDomeLight": "dome_Lit",
    "transform": "Grp",
    "joint": "Jnt",
    "camera": None,
}

defaultSuffix = None
newNames = []

def rename(selection = False):
    # if you don't enter selection = True, it will return all the objects
    selected_objs = cmds.ls(selection=selection, dag=True, long=True)

    # nothing selected
    if selection and not selected_objs:
        raise RuntimeError("You're not selecting anything!")

    # sort by length of elements and reverse sorting
    selected_objs.sort(key=len, reverse=True)

    for path in selected_objs:
        # divide the path and get last object of each path
        shortName = path.split('|')[-1]

        # get lists of children of every object, return an empty list if no children
        children = cmds.listRelatives(path, shapes=True) or []

        # get child type if the object has only one child
        if len(children) != 0:
            child = f"{path}|{children[0]}"
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(path)

        # get suffix from dictionary
        suffix = SUFFIXES.get(objType, defaultSuffix)

        # skip objects with no suffix
        if not suffix:
            continue

        # make sure we don't name an already renamed object
        if path.endswith("_" + suffix):
            continue

        #rename with new name
        newName = f"{shortName}_{suffix}"
        cmds.rename(path, newName)

        # get a list of renamed objects' names
        newNames.append(newName)

    print("These objects are renamed:")
    print(newNames)
