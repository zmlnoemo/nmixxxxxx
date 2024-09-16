import maya.api.OpenMaya as om
import maya.OpenMayaMPx as MPx
import maya.cmds as cmds
import maya.mel as mel
from math import *
from functools import partial
import random as rand
import json	 
import os
import webbrowser 
          

shader_suite_path = ""

def openModelLibrarySettings(*args):
    # Opens a file dialog to select a directory and sets the shader_suite_path global variable to the selected path.
    global shader_suite_path
    file_path = cmds.fileDialog2(fileMode=3, dialogStyle=2)  # Open file dialog to select directory
    if file_path:
        shader_suite_path = file_path[0]  # Set the global shader_suite_path to the selected path

def setShaderSuitePath(path):
    # Sets the shader_suite_path global variable to the given path.
    global shader_suite_path
    shader_suite_path = path  # Set the global shader_suite_path to the given path

##---------------------------------------------------------------------------------------------------------------
# coding=utf-8 
# 材质调用脚本文件
# ZRCG(知然新立)
# 邮箱 w1778216708163@163.com
# 网站 www.321suc.com
def LayoutFrameTabLayout_ArnoldLib(*args):
    # Creates a UI layout for Arnold shader library, displaying different material categories and their contents.
    global shader_suite_path
    sos1 = ['01-WOOD', '02-LEAVES']
    formLayout_A = 'formLayout_A1'
    lib_path_text = cmds.internalVar(usd=1) + 'ArnoldLib/ArnoldLib.xm'  # Path to ArnoldLib configuration file
    
    if cmds.frameLayout(formLayout_A, q=1, ex=1):
        cmds.deleteUI(formLayout_A)  # Delete existing frame layout if it exists
    
    cmds.frameLayout(formLayout_A, cll=0, cl=0, l='Leaf or trunk material selection', bgc=[0, 0, 0])  # Create new frame layout
    
    if os.path.isfile(lib_path_text):  # Check if the library path configuration file exists
        fileContent_A1 = ''
        with open(lib_path_text, 'r') as f:
            fileContent_A1 = f.read()  # Read the content of the configuration file
        
        getFile = os.listdir(fileContent_A1)  # List directories in the configuration path
        tabLayout1 = cmds.tabLayout(innerMarginWidth=10, innerMarginHeight=10, w=430)  # Create tab layout
        
        for i in getFile:
            if i not in sos1:
                cmds.error('Abnormal material folder, please do not create or change the original folder name in the material library')  # Error if directory name is not in predefined list
            
            rowColumnLayout1 = cmds.rowColumnLayout(numberOfColumns=2, columnSpacing=[(1, 10), (2, 10)], rowSpacing=[(1, 10)], w=430)  # Create row-column layout
            mot_name_path = fileContent_A1 + '/' + i + '/'  # Construct path to the material directory
            getFile_mot = os.listdir(mot_name_path)  # List files in the material directory
            
            for n in getFile_mot:
                split1 = n.split('.')
                if split1[-1] == 'ma':  # Check if the file is a Maya file
                    cmds.columnLayout(w=200)
                    cmm1 = 'ArnoldLibWindow_data("' + i + '","' + n + '")'  # Command for symbol button
                    cmm2 = 'ArnoldLibWindow_data1("' + i + '","' + n + '")'  # Command for menu item
                    cmds.symbolButton(w=150, h=150, image=mot_name_path + split1[0] + '.png', c=cmm1)  # Create symbol button with image
                    cmds.popupMenu()
                    cmds.menuItem(l='New scene Open material', c=cmm2)  # Create menu item to open material in a new scene
                    cmds.text('   %s  ' % split1[0])  # Display material name
                    cmds.setParent('..')
            
            cmds.setParent('..')
            cmds.tabLayout(tabLayout1, edit=1, tl=(rowColumnLayout1, i))  # Add row-column layout to tab layout
        
        cmds.setParent('..')
        
def mot_lib_win_set(*args):
    # Creates a UI window for setting the Arnold shader library path.
    lib_path_text = cmds.internalVar(usd=1) + 'ArnoldLib/ArnoldLib.xm'  # Path to ArnoldLib configuration file
    window2 = 'ArnoldLibWindow2'
    if cmds.window(window2, q=True, ex=True):
        cmds.deleteUI(window2)  # Delete existing window if it exists

    cmds.window(window2, t=u"325 Arnold Material call tool", mb=1)  # Create new window
    cmds.columnLayout(adj=1)
    if os.path.isfile(lib_path_text):  # Check if the library path configuration file exists
        cmds.separator(h=30)
        cmds.text(u'The model library location has been specified')  # Display text indicating that the library path is set
        cmds.separator(h=20)
        cmds.button(l=u'Specify the new model library location', c=mot_lib_data_set)  # Button to set a new library path
    else:
        cmds.separator(h=30)
        cmds.text(u'The model library location is not specified')  # Display text indicating that the library path is not set
        cmds.separator(h=20)
        cmds.button(l=u'Specify the model library location', c=mot_lib_data_set)  # Button to set the library path

    cmds.window(window2, e=True, w=300, h=100)  # Set window size
    cmds.showWindow(window2)  # Show the window

def mot_lib_data_set(*args):
    # Sets the path to the Arnold shader library and writes it to a configuration file.
    lib_path_text = cmds.internalVar(usd=1) + 'ArnoldLib/ArnoldLib.xm'  # Path to ArnoldLib configuration file
    filename1 = cmds.fileDialog2(fileMode=2, ds=1, okc=u'confirm', caption=u'select')  # Open file dialog to select directory
    motionfile = filename1[0]
    if not os.path.isdir(cmds.internalVar(usd=1) + 'ArnoldLib'):
        os.makedirs(cmds.internalVar(usd=1) + 'ArnoldLib')  # Create ArnoldLib directory if it does not exist

    if os.path.isfile(lib_path_text):
        os.remove(lib_path_text)  # Remove existing configuration file if it exists

    with open(lib_path_text, 'a') as file1:
        file1.write(motionfile)  # Write the selected path to the configuration file

def ArnoldLibWindow_data(lib_name, mot_name):
    # Imports the specified Arnold material into the current scene and sets up shading groups.
    global shader_suite_path
    lib_path_text = cmds.internalVar(usd=1) + 'ArnoldLib/ArnoldLib.xm'
    if not os.path.isfile(lib_path_text):
        cmds.error('The material library record file is empty')  # Error if the material library record file does not exist
    fileContent_A1 = ''
    with open(lib_path_text, 'r') as f:
        fileContent_A1 = f.read()  # Read the content of the material library record file

    if len(fileContent_A1) < 1:
        cmds.error('The material library record file is empty')  # Error if the material library record file is empty

    sel = cmds.ls(sl=1)  # Get selected objects
    j_data = 0
    if sel is not None:
        if len(sel) > 0:
            j_data = 1  # Check if there are selected objects

    sp1 = mot_name.split('.')[0].split('_')
    im_mot_name = sp1[0] + '_' + sp1[1]  # Construct initial material name

    if j_data == 0:
        if cmds.objExists(im_mot_name):
            cmds.rename(im_mot_name, im_mot_name + '#')  # Rename existing material

        if cmds.objExists(im_mot_name + '_DISP'):
            cmds.rename(im_mot_name + '_DISP', im_mot_name + '#' + '_DISP')  # Rename existing displacement map

        mel.eval('file -import -type "mayaAscii" "%s"' % (fileContent_A1 + '/' + lib_name + '/' + mot_name))  # Import material file
        rename_a = cmds.rename(im_mot_name, im_mot_name + '#')  # Rename imported material

        rename_b = im_mot_name + '_DISP'
        if cmds.objExists(im_mot_name + '_DISP'):
            rename_b = cmds.rename(im_mot_name + '_DISP', im_mot_name + '#' + '_DISP')  # Rename imported displacement map

        cmds.select(rename_a)
        sg_new_name = Material_completion_SG(rename_b)  # Complete shading group setup
        if sg_new_name == '1234567895215':
            cmds.delete(rename_a)
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
            cmds.error('Abnormal sequence')  # Error if the shading group setup is incorrect

        cmds.select(cl=1)  # Clear selection

    else:
        if cmds.objExists(im_mot_name):
            cmds.rename(im_mot_name, im_mot_name + '#')  # Rename existing material

        if cmds.objExists(im_mot_name + '_DISP'):
            cmds.rename(im_mot_name + '_DISP', im_mot_name + '#' + '_DISP')  # Rename existing displacement map

        sets = mel.eval('sets -n "Settemps#"')  # Create a temporary set
        internalVaa = mel.eval('file -import -type "mayaAscii" "%s"' % (fileContent_A1 + '/' + lib_name + '/' + mot_name))  # Import material file
        rename_a = cmds.rename(im_mot_name, im_mot_name + '#')  # Rename imported material

        rename_b = im_mot_name + '_DISP'
        if cmds.objExists(im_mot_name + '_DISP'):
            rename_b = cmds.rename(im_mot_name + '_DISP', im_mot_name + '#' + '_DISP')  # Rename imported displacement map

        cmds.select(rename_a)
        sg_new_name = Material_completion_SG(rename_b)  # Complete shading group setup
        if sg_new_name == '1234567895215':
            cmds.delete(rename_a)
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
            cmds.error('Abnormal sequence')  # Error if the shading group setup is incorrect

        cmds.select(sets)
        cmds.ls(selection=1)
        cmds.delete(sets)  # Delete the temporary set
        for i in sel:
            mel.eval('hyperShade -a %s' % rename_a)  # Assign material to selected objects
            cmds.select(rename_a)
        cmds.select(cl=1)  # Clear selection

def ArnoldLibWindow_data1(lib_name, mot_name):
    # Opens a new scene and imports the specified Arnold material into it.
    global shader_suite_path
    lib_path_text = cmds.internalVar(usd=1) + 'ArnoldLib/ArnoldLib.xm'
    if not os.path.isfile(lib_path_text):
        cmds.error('The material library record file is empty')  # Error if the material library record file does not exist
    fileContent_A1 = ''
    with open(lib_path_text, 'r') as f:
        fileContent_A1 = f.read()  # Read the content of the material library record file

    if len(fileContent_A1) < 1:
        cmds.error('The material library record file is empty')  # Error if the material library record file is empty

    cmds.NewScene()
    mel.eval('file -import -type "mayaAscii" "%s"' % (fileContent_A1 + '/' + lib_name + '/' + mot_name))  # Import material file

    cmds.select(cl=1)  # Clear selection

def Material_completion_SG(rename_b):
    # Sets up the shading group for the imported material and connects displacement if present.
    global shader_suite_path
    sel = cmds.ls(sl=1)  # Get selected objects
    rename2 = '1234567895215'
    for i in sel:
        aiSt1 = mel.eval('createRenderNodeCB -asShader "surfaceShader" "aiStandardSurface" ""')  # Create aiStandardSurface shader
        mel.eval('connectAttr -f %s.outColor %sSG.surfaceShader' % (i, aiSt1))  # Connect shader to shading group
        cmds.delete(aiSt1)
        rename2 = cmds.rename(aiSt1 + 'SG', i + 'SG')  # Rename shading group
        if cmds.objExists(rename_b):
            mel.eval('connectAttr -f %s.displacement %s.displacementShader' % (rename_b, rename2))  # Connect displacement map if present

    return rename2  # Return new shading group name
##-------------------------------------------------------------------------------------------------------------------


def autoHierarchy():
    # Automatically generate the tree hierarchy, identifying and organizing branches and leaves.
    # It checks the selected objects and separates the branches and leaves into different global lists based on the object names and hierarchy.
    global AllMeshBranchesF  # Global variable to store all the branches
    global selOrig  # Global variable to store the originally selected object
    global AllLeaves  # Global variable to store all the leaves
    global AllMeshBranches  # Global variable to store all the branches (not flattened)
    global AllTrunks  # Global variable to store all the trunks

    selOrig = cmds.ls(sl=1)  # Get the currently selected object
    if len(selOrig) == 0:
        cmds.warning('Please select a branch')  # Warn if no object is selected
    if len(selOrig) > 1:
        cmds.warning('Only one branch can be selected')  # Warn if multiple objects are selected
    if len(selOrig) == 1:
        try:
            AllMeshBranches = []
            AllTrunks = []
            # Parse the selected object's name and check if it is a valid branch
            treeName = selOrig[0].split('_')
            treeName = treeName[0] + treeName[2]
            if treeName != 'Treebranch':
                cmds.warning('Please select a valid branch')  # Warn if it is not a valid branch
            if treeName == 'Treebranch':
                sel = cmds.ls(sl=1)  # Get the selected object
                brnches = []  # List to store branches
                cnt = 0
                AllLeaves = []  # List to store leaves
                try:
                    for e in range(50):  # Maximum loop count to avoid infinite loop
                        for i in sel:
                            brnche = cmds.listRelatives(i, c=1)  # Get the children of the current object
                            os = []  # List to store mesh-type children
                            LvsG = []  # List to store leaf groups
                            for l in brnche:
                                L = l.split('leaves')  # Check if the child name contains 'leaves'
                                if len(L) == 2:
                                    LvsG.append(l)  # If it is a leaf group, add to LvsG list
                                    lvsGchild = cmds.listRelatives(l, c=1)  # Get the children of the leaf group
                                    for lc in lvsGchild:
                                        AllLeaves.append(lc)  # Add the leaves to the AllLeaves list

                                o = cmds.objectType(l)  # Get the type of the child
                                if o == 'mesh':
                                    os.append(l)  # If it is a mesh type, add to os list

                        for oo in os:
                            brnche.remove(oo)  # Remove mesh-type children from the branch list

                        for ll in LvsG:
                            brnche.remove(ll)  # Remove leaf groups from the branch list

                        brnches.append(brnche)  # Add the current level of branches to the brnches list
                        sel = brnches
                        cnt = cnt + 1

                except:
                    pass
                
                # Build the final lists of branches and leaves
                AllMeshBranches = brnches[0:len(brnches) - 1]
                AllMeshBranchesF = [ val for sublist in AllMeshBranches for val in sublist ]
                AllLeaves = list(set(AllLeaves))  # Deduplicated list of all leaves

                # Build the list of trunks
                for branch in AllMeshBranchesF:
                    trunk = cmds.listRelatives(branch, p=True)  # Get the parent of the branch
                    if trunk and trunk[0] not in AllTrunks:
                        if trunk and trunk[0] not in AllLeaves:
                            AllTrunks.append(trunk[0])  # Add the parent to the trunk list if it is not in the leaf list

        except:
            cmds.warning('Please select a valid branch')  # Warn if an error occurs


def autoHierarchyDef(*args):
    # Automatically generate the tree hierarchy, identifying and organizing branches and leaves.
    # It checks the selected objects and separates the branches and leaves into different global lists based on the object names and hierarchy.
    global AllMeshBranchesF  # Global variable to store all the branches
    global selOrig  # Global variable to store the originally selected object
    global AllLeaves  # Global variable to store all the leaves
    global AllMeshBranches  # Global variable to store all the branches (not flattened)
    global AllTrunks  # Global variable to store all the trunks

    selOrig = cmds.ls(sl=1)  # Get the currently selected object
    if len(selOrig) == 0:
        cmds.warning('Please select a trunk')  # Warn if no object is selected
        return
    if len(selOrig) > 1:
        cmds.warning('Only one trunk can be selected')  # Warn if multiple objects are selected
        return
    if len(selOrig) == 1:
        try:
            AllMeshBranches = []
            AllTrunks = []
            # Parse the selected object's name and check if it is a valid trunk
            treeNameParts = selOrig[0].split('_')
            treeName = treeNameParts[0] + treeNameParts[2] + treeNameParts[3]
            if treeName != 'TreebranchtrunkMesh':
                cmds.warning('Please select a valid trunk')  # Warn if it is not a valid trunk
                return
            if treeName == 'TreebranchtrunkMesh':
                sel = cmds.ls(sl=1)  # Get the selected object
                brnches = []  # List to store branches
                cnt = 0
                AllLeaves = []  # List to store leaves
                try:
                    for e in range(50):  # Maximum loop count to avoid infinite loop
                        for i in sel:
                            brnche = cmds.listRelatives(i, c=1, type='transform')  # Only get transform nodes
                            os = []  # List to store mesh-type children
                            LvsG = []  # List to store leaf groups
                            for l in brnche:
                                if 'leaves' in l:
                                    LvsG.append(l)
                                    lvsGchild = cmds.listRelatives(l, c=1, type='mesh')  # Get the leaf children
                                    if lvsGchild:
                                        AllLeaves.extend(lvsGchild)  # Add the leaves to the AllLeaves list
                                elif cmds.objectType(l) == 'mesh':
                                    os.append(l)  # If it is a mesh type, add to os list
                                else:
                                    AllTrunks.append(l)  # If it is neither, add to AllTrunks list

                            for oo in os:
                                brnche.remove(oo)  # Remove mesh-type children from the branch list

                            for ll in LvsG:
                                brnche.remove(ll)  # Remove leaf groups from the branch list

                            brnches.append(brnche)  # Add the current level of branches to the brnches list
                            sel = brnches
                            cnt += 1

                except Exception as e:
                    cmds.warning('Error processing branches and leaves: {}'.format(str(e)))  # Warn if an error occurs
                
                # Build the final lists of branches and leaves
                AllMeshBranches = brnches[0:len(brnches) - 1]
                AllMeshBranchesF = [val for sublist in AllMeshBranches for val in sublist]
                AllLeaves = list(set(AllLeaves))  # Deduplicated list of all leaves
                AllTrunks = list(set(AllTrunks))  # Deduplicated list of all trunks

                cmds.warning('Tree Hierarchy Loaded')  # Notify that the hierarchy is loaded
        except Exception as e:
            cmds.warning('Please select a valid tree: {}'.format(str(e)))  # Warn if an error occurs


def loadTreeData(*args):
    # This function loads the hierarchical data of a tree structure in Autodesk Maya.
    # It retrieves and reconstructs the hierarchy of branches and leaves from custom attributes stored on a selected trunk mesh.
    global AllMeshBranchesF  # Global variable to store all the branches (flattened)
    global trunkMesh  # Global variable to store the trunk mesh
    global AllLeaves  # Global variable to store all the leaves
    global AllMeshBranches  # Global variable to store all the branches (not flattened)
    
    trunkMesh = cmds.ls(sl=1)  # Get the currently selected object
    try:
        # Try to get the branch hierarchy attribute from the selected trunk
        attrr = cmds.getAttr(trunkMesh[0] + '.branchHierarchy')
        AllMeshBranches = json.loads(attrr)  # Parse the JSON-encoded branch hierarchy
        AllMeshBranches.reverse()  # Reverse the order of branches
        AllMeshBranchesF = [ val for sublist in AllMeshBranches for val in sublist ]  # Flatten the list of branches
        cmds.select(trunkMesh)  # Reselect the trunk mesh
        trunkMesh = cmds.ls(sl=1)  # Update the trunk mesh variable
        cmds.warning('Tree loaded')  # Notify that the tree is loaded
    except:
        cmds.warning('This is an invalid tree')  # Warn if the selected object is not a valid tree

    try:
        # Try to get the all leaves attribute from the selected trunk
        attrr = cmds.getAttr(trunkMesh[0] + '.allLeaves')
        AllLeaves = json.loads(attrr)  # Parse the JSON-encoded list of leaves
        cmds.warning('Tree and leaves loaded')  # Notify that the tree and leaves are loaded
    except:
        pass  # Do nothing if the leaves attribute is not found


def Del_LeafDyna(*args):
    # This function removes dynamics from the leaves of a selected branch in Autodesk Maya.
    # It uses the autoHierarchy function to organize the tree structure and then deletes dynamics and resets the rotation for each leaf.
    autoHierarchy()  # Organize tree structure and identify branches and leaves
    try:
        cmds.delete(AllLeaves, e=1)  # Delete dynamics from all leaves
        for e in AllLeaves:
            cmds.xform(e, ro=(0, 0, 0))  # Reset rotation for each leaf

    except:
        cmds.warning('Please select a branch to remove dynamics')  # Display a warning if no valid branch is selected


def leaves_Dynamics(freq2Field, intens2Field, turb2Field, turbVariField, *args):
    # This function adds dynamic motion to the leaves of a selected branch in Autodesk Maya.
    # It uses the autoHierarchy function to organize the tree structure, retrieves user-specified dynamic parameters, and applies noise-based rotation to each leaf using expressions.
    freq = cmds.floatSliderGrp(freq2Field, q=1, v=1)  # Retrieve user-specified dynamic parameters from UI sliders
    intens = cmds.floatSliderGrp(intens2Field, q=1, v=1)
    turb = cmds.floatSliderGrp(turb2Field, q=1, v=1)
    turbVari = cmds.floatSliderGrp(turbVariField, q=1, v=1)
    turbVari = turbVari * turb
    autoHierarchy()  # Organize tree structure and identify branches and leaves
    try:
        cmds.delete(AllLeaves, e=1)  # Delete existing expressions from all leaves
        Vals = ''
        for e in AllLeaves:  # Apply dynamic rotation to each leaf
            offsetx = rand.randint(0, 200)
            offsety = rand.randint(0, 200)
            offsetz = rand.randint(0, 200)
            turbRand = rand.uniform(-turbVari, turbVari)
            turbRand = round(turbRand, 4)
            vx = '\n' + str(e) + '.rotateX = ' + str(intens) + '*noise(((time +' + str(offsetx) + ') /' + str(freq) + ') *' + str(turb + turbRand) + ');'
            vy = '\n' + str(e) + '.rotateY = ' + str(intens) + '*noise(((time +' + str(offsety) + ') /' + str(freq) + ') *' + str(turb + turbRand) + ');'
            vz = '\n' + str(e) + '.rotateZ = ' + str(intens) + '*noise(((time +' + str(offsetz) + ') /' + str(freq) + ') *' + str(turb + turbRand) + ');'
            V = vx + vy + vz
            V = str(V)
            cmds.expression(s=V, n=e + '_Leaf_Dyna_Expression')  # Apply the expression to the leaf

    except:
        cmds.warning('Please select a branch to apply dynamics')  # Display a warning if no valid branch is selected


def loadLeaf(*args):
    # This function loads a selected leaf in Autodesk Maya, ensuring it is a valid mesh leaf named 'masterLeaf'.
    # It applies transformations and deletes history on the selected leaf.
    global lf  # Declare global variable lf to store the loaded leaf
    obj = cmds.ls(sl=1)  # Get the currently selected object
    if len(obj) == 0:  # Check if no object is selected
        cmds.warning('Choose a main leaf')
    if len(obj) > 1:  # Check if more than one object is selected
        cmds.warning('Only one main leaf can be selected')
    if len(obj) == 1:  # Check if exactly one object is selected
        leafName = obj[0].split('_')  # Extract the name of the selected object
        leafName = leafName[0]
        if leafName != 'masterLeaf':  # Check if the selected object is named 'masterLeaf'
            cmds.warning('Please select a valid main leaf')
        if leafName == 'masterLeaf':
            shape = cmds.listRelatives(obj)[0]  # Get the shape node of the selected object
            shapeType = cmds.objectType(shape)
            if shapeType != 'mesh':
                cmds.warning('Please select a polygon of leaves')
            if shapeType == 'mesh':
                lf = cmds.ls(sl=1)  # Store the selected leaf in the global variable lf
                cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                cmds.DeleteHistory()
                cmds.select(cl=1)
                cmds.warning('Main leaf loaded')


def masterLeaf(*args):
    # This function creates a master leaf polygon in Autodesk Maya.
    cmds.softSelect(e=1, sse=0)  # Disable soft selection if it's enabled
    lf = cmds.polyPlane(w=2, h=1, sx=4, sy=2, n='masterLeaf_01')[0]  # Create a polygon plane representing the master leaf
    cmds.xform(lf, t=(-1, 0, 0), ws=1)  # Translate the leaf to a specific position in world space
    cmds.xform(lf, sp=(0, 0, 0), rp=(0, 0, 0), ws=1)  # Set the pivot point and reset point to the origin
    cmds.select(lf + '.vtx[0]', lf + '.vtx[5]', lf + '.vtx[10]')  # Select and move specific vertices to shape the leaf
    cmds.move(0, -0.24, 0, r=1)
    cmds.select(lf + '.vtx[2:3]', lf + '.vtx[7:8]', lf + '.vtx[12:13]')
    cmds.move(0, 0.12, 0, r=1)
    cmds.select(lf + '.vtx[10:14]', lf + '.vtx[0:4]')
    cmds.move(0, 0.1, 0, r=1)
    cmds.select(lf)  # Select the entire leaf and scale it uniformly
    cmds.scale(0.5, 0.5, 0.5)
    cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)  # Reset transformations to apply the scaling properly


def leavesGen(CuLevelsField, leafNumField, GravityField, GravIncField, rotateField, rotateIncField, tiltField, spacingField, scaleField, scaleIncField, *args):
    # Generates leaves on selected branches based on user-defined parameters in Autodesk Maya.
    global AllLeavesG  # stores groups of leaves as they are generated
    global AllLeaves  # stores individual leaf objects
    cmds.softSelect(e=1, sse=0)  # Disable soft selection in Maya
    sel = cmds.ls(sl=1)  # Get selected objects (assumed to be branches)
    if len(sel) == 0:  # Check if exactly one branch is selected
        cmds.warning('No trunk or branch is selected. Please select one')
    if len(sel) > 1:
        cmds.warning('Only one trunk or branch can be selected')
    if len(sel) == 1:
        autoHierarchy()  # Automatically organize branches and leaves
        try:
            if len(lf) == 0:
                cmds.warning('No main leaf is loaded. Please load one')
            if len(lf) == 1:
                try:
                    cmds.select(lf)
                    lf2 = cmds.ls(sl=1)
                except:
                    lf2 = cmds.ls(sl=1)

            if len(lf2) == 0:
                cmds.warning('No main leaf is loaded. Please load one')
            if len(lf2) == 1:
                CuLevels = cmds.intSliderGrp(CuLevelsField, q=1, v=1)  # Retrieve user-defined parameters
                # Remove overlapping leaves and branches
                try:
                    bn = AllMeshBranches[0][0][0:8]
                    ln = AllLeaves[0][0:8]
                    if bn == ln:
                        cmds.select(AllLeaves)
                        cmds.pickWalk(d='up')
                        cmds.delete()
                except:
                    pass

                Curvs = []
                meshBs = []
                AllMeshBranches.reverse()  # Remove overlapping leaves and branches
                for h, g in zip(AllMeshBranches, range(CuLevels)):
                    try:
                        meshBs.append(h)
                        for Br in h:
                            A = (
                             Br + '.vtx[0]', Br + '.vtx[8]', Br + '.vtx[9]', Br + '.vtx[10]', Br + '.vtx[11]', Br + '.vtx[12]')
                            B = (Br + '.vtx[3]', Br + '.vtx[33]', Br + '.vtx[34]', Br + '.vtx[35]', Br + '.vtx[36]', Br + '.vtx[37]')
                            PosCUs = []
                            for e, f in zip(A, B):
                                Apos = cmds.xform(e, t=1, ws=1, q=1)
                                Bpos = cmds.xform(f, t=1, ws=1, q=1)
                                AvPos = ((Apos[0] + Bpos[0]) / 2, (Apos[1] + Bpos[1]) / 2, (Apos[2] + Bpos[2]) / 2)
                                PosCUs.append(AvPos)
                            # Create curve and rebuild it
                            CuBr = cmds.curve(p=PosCUs)
                            cmds.rebuildCurve(ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=5, d=3, tol=0.01)
                            Curvs.append(CuBr)

                    except:
                        pass

                meshBs = [ val for sublist in meshBs for val in sublist ]
                truckName = AllMeshBranches[0][0][0:8]
                leafNum = cmds.intSliderGrp(leafNumField, q=1, v=1)
                maxVal = len(Curvs) * leafNum
                progres = cmds.window(t=' Growing Leaves :) ')  # Display progress window
                cmds.columnLayout()
                progressControl = cmds.progressBar(maxValue=maxVal, width=380)
                cmds.showWindow(progres)
                p = 0
                AllLeaves = []
                AllLeavesG = []
                # Generate leaves along curves and apply transformations
                for c, d in zip(Curvs, meshBs):
                    Gr = cmds.floatSliderGrp(GravityField, q=1, v=1)
                    GrInc = cmds.floatSliderGrp(GravIncField, q=1, v=1)
                    rott = cmds.floatSliderGrp(rotateField, q=1, v=1)
                    rottInc = cmds.floatSliderGrp(rotateIncField, q=1, v=1)
                    tilt = cmds.floatSliderGrp(tiltField, q=1, v=1)
                    spac = cmds.floatSliderGrp(spacingField, q=1, v=1)
                    scl = cmds.floatSliderGrp(scaleField, q=1, v=1)
                    sclInc = cmds.floatSliderGrp(scaleIncField, q=1, v=1)
                    cnt = 0
                    i = 0.95
                    rott2 = rott
                    leavs = []
                    for e in range(leafNum):
                        CP = cmds.pointOnCurve(c, pr=i, p=1)
                        i = i - spac
                        if CP[0] != 0 and CP[1] != 0 and CP[2] != 0:
                            leaf = cmds.duplicate(lf2, n=d + '_leaf_01')
                            leafBase = cmds.group(em=1, n='leafBase')
                            cmds.parent(leaf, leafBase)
                            cmds.xform(leafBase, t=CP, ws=1)
                            if cnt == 0:
                                cmds.xform(leaf, ro=(0, 180, -Gr), s=(scl, scl, scl), ws=1)
                            if cnt > 0 and cnt % 2 == 0:
                                cmds.xform(leaf, ro=(0, 180 + rott, -Gr), s=(scl, scl, scl), ws=1)
                                cmds.xform(leaf, ro=(tilt, 0, 0), r=1, os=1)
                                rott = rott + rottInc
                            if cnt % 2 != 0:
                                cmds.xform(leaf, ro=(0, 180 - rott2, -Gr), s=(scl, scl, scl), ws=1)
                                cmds.xform(leaf, ro=(-tilt, 0, 0), r=1, os=1)
                                rott2 = rott2 + rottInc
                            cnt = cnt + 1
                            Gr = Gr + GrInc
                            scl = scl + sclInc
                            TC = cmds.tangentConstraint(c, leafBase, weight=1, aimVector=(1,
                                                                                          0,
                                                                                          0), upVector=(0,
                                                                                                        1,
                                                                                                        0), worldUpType='vector', worldUpVector=(0,
                                                                                                                                                 1,
                                                                                                                                                 0))
                            cmds.delete(TC)
                            cmds.parent(leaf, w=1)
                            leavs.append(leaf[0])
                            cmds.delete(leafBase)
                        progressInc = cmds.progressBar(progressControl, edit=True, pr=p + 1)
                        p = p + 1

                    AllLeaves.append(leavs)  
                    LeavesG = cmds.group(leavs, n=d + '_leaves_G')
                    AllLeavesG.append(LeavesG)
                    cmds.parent(LeavesG, d)

                AllLeaves = [ val for sublist in AllLeaves for val in sublist ]  # Flatten list of leaves
                AllMeshBranches.reverse()
                cmds.makeIdentity(AllLeaves, apply=1, t=1, r=1, s=1, n=0, pn=1)  # Reset transformations
                cmds.sets(AllLeaves, name=truckName + '_Leaves_set')  # Create a set for the leaves
                # Clear selection and delete progress window
                cmds.select(cl=1)
                cmds.deleteUI(progres)
                cmds.delete(Curvs)

                # Hide original meshName if specified
                if meshName:
                    cmds.hide(meshName[0])
                    cmds.warning('The input shape has been hidden')

                try:
                    # Store generated leaves in JSON format
                    ALv = json.dumps(AllLeaves)
                    cmds.setAttr(trunkMesh[0] + '.allLeaves', l=0)
                    cmds.setAttr(trunkMesh[0] + '.allLeaves', ALv, type='string', l=1)
                except:
                    cmds.warning('Leaves have Grown :)')

        except:
            cmds.warning('No main leaf is loaded. Please load one')

        cmds.select(selOrig)  # Restore original selection and flush undo queue
        cmds.flushUndo()


def selectLeaves(*args):
    # Selects all leaves in the scene after automatically organizing the hierarchy.
    autoHierarchy()  # Ensure branches and leaves are organized
    try:
        cmds.select(AllLeaves)  # Attempt to select all leaves
    except:
        pass  # Ignore if selection fails


def Del_Branch_Dyna(ChkBox, *args):
    # Deletes dynamic behavior from selected branches or all branches based on user choice.
    selectedBranch = cmds.checkBox(ChkBox, q=1, v=1)
    if selectedBranch == 1:
        # Delete dynamics from selected branches
        selbrnch = cmds.ls(sl=1)
        cmds.delete(selbrnch, e=1)
    if selectedBranch == 0:
        # Delete dynamics from all branches
        autoHierarchy()
        cmds.delete(AllMeshBranchesF, e=1)
        for e in AllMeshBranchesF:
            cmds.xform(e, ro=(0, 0, 0))  # Reset rotations of all branches


def BranchDynamics(freqField, freq_incrField, intensField, intens_incrField, turbField, ChkBox, *args):
    # It manages dynamic animations (likely rotational) for selected tree branches or all branches based on user settings
    # Retrieve slider values
    freq = cmds.floatSliderGrp(freqField, q=1, v=1)
    freq_incr = cmds.floatSliderGrp(freq_incrField, q=1, v=1)
    intens = cmds.floatSliderGrp(intensField, q=1, v=1)
    intens_incr = cmds.floatSliderGrp(intens_incrField, q=1, v=1)
    turb = cmds.floatSliderGrp(turbField, q=1, v=1)
    selectedBranch = cmds.checkBox(ChkBox, q=1, v=1)
    if selectedBranch == 1:  # If a branch is selected
        # Get selected branch objects
        selbrnch = cmds.ls(sl=1)
        treeName = selbrnch[0].split('_')
        treeName = treeName[0] + treeName[2]
        if treeName != 'Treebranch':  # Check if selected object matches expected name pattern
            cmds.warning('Please select a valid branch')  # Warn if not a valid branch
        if treeName == 'Treebranch':
            cmds.delete(selbrnch, e=1)  # Delete selected branches
            for b in selbrnch:
                # Create dynamic expressions for rotation based on noise
                offsetx = rand.randint(0, 200)
                offsety = rand.randint(0, 200)
                offsetz = rand.randint(0, 200)
                vx = '\n' + str(b) + '.rotateX = ' + str(intens) + '*noise(((time +' + str(offsetx) + ') /' + str(freq) + ') *' + str(turb) + ');'
                vy = '\n' + str(b) + '.rotateY = ' + str(intens) + '*noise(((time +' + str(offsety) + ') /' + str(freq) + ') *' + str(turb) + ');'
                vz = '\n' + str(b) + '.rotateZ = ' + str(intens) + '*noise(((time +' + str(offsetz) + ') /' + str(freq) + ') *' + str(turb) + ');'
                V = vx + vy + vz
                V = str(V)
                cmds.expression(s=V, n=b + '_Dyna_Expression')

    if selectedBranch == 0:  # If no branch selected (auto mode)
        autoHierarchy()  # Assuming autoHierarchy() sets up AllMeshBranches
        cmds.delete(AllMeshBranchesF, e=1)  # Delete existing dynamic expressions
        Vals = ''
        for b in AllMeshBranches:
            for e in b:
                # Create dynamic expressions for rotation with increasing intensity and decreasing frequency
                offsetx = rand.randint(0, 200)
                offsety = rand.randint(0, 200)
                offsetz = rand.randint(0, 200)
                vx = '\n' + str(e) + '.rotateX = ' + str(intens) + '*noise(((time +' + str(offsetx) + ') /' + str(freq) + ') *' + str(turb) + ');'
                vy = '\n' + str(e) + '.rotateY = ' + str(intens) + '*noise(((time +' + str(offsety) + ') /' + str(freq) + ') *' + str(turb) + ');'
                vz = '\n' + str(e) + '.rotateZ = ' + str(intens) + '*noise(((time +' + str(offsetz) + ') /' + str(freq) + ') *' + str(turb) + ');'
                V = vx + vy + vz
                V = str(V)
                cmds.expression(s=V, n=e + '_Dyna_Expression')

            intens = intens + intens_incr  # Increase intensity
            freq = freq - freq_incr  # Decrease frequency
            if freq < 1:
                freq = 0.5  # Ensure frequency doesn't go below 0.5


def LoadMesh_Curves(*args):
    # It manages the loading and processing of selected input shapes, specifically handling cases where two shapes (one center curve and one mesh) need to be selected
    global Pps  # List to store vertex positions
    global meshName  # List to store mesh names
    global centerCurve  # List to store center curve names
    global SelVtxs  # List to store selected vertices
    global Pps2  # Backup list for vertex positions
    sel = cmds.ls(sl=1)  # Get current selection
    centerCurve = []  # Initialize centerCurve list
    meshName = []  # Initialize meshName list
    sel = cmds.ls(sl=1)
    # Handle selection errors and warnings
    if len(sel) > 2:
        cmds.warning('Only select 2 input shapes')
    if len(sel) == 0:
        cmds.warning('Please select input shapes')
    if len(sel) == 1:
        cmds.warning('Please select 2 input shapes')
    if len(sel) > 3:
        cmds.warning('Please select 2 input shapes')
    if len(sel) == 2:  # If exactly 2 shapes are selected
        Gp = cmds.group(n='gp')  # Create a temporary group
        cmds.SelectHierarchy()  # Select all children
        cmds.pickWalk(d='down')  # Move down in hierarchy
        cmds.pickWalk(d='down')  # Move down in hierarchy
        cmds.pickWalk(d='up')  # Move back up
        cmds.parent(w=1)  # Unparent
        cmds.delete(Gp)  # Delete the temporary group
        sel = cmds.ls(sl=1)  # Get selection again
        for e in sel:
            cmds.rename(e, 'inputsShape_01')  # Rename selected shapes

        sel = cmds.ls(sl=1)
        for e in sel:
            shape = cmds.listRelatives(e)[0]  # Get shape node
            shapeType = cmds.objectType(shape)  # Get shape type
            # Classify shapes into center curves or meshes
            if shapeType == 'nurbsCurve':
                centerCurve = [
                 e]  # Store center curve
            if shapeType == 'mesh':
                meshName = [
                 e]  # Store mesh
                
        # Handle case where selections aren't valid
        if len(centerCurve) == 0 or len(meshName) == 0:
            cmds.warning('Please select 2 valid input shapes')
        # If exactly 1 center curve and 1 mesh are selected
        if len(centerCurve) == 1 and len(meshName) == 1:
            # Rebuild the center curve
            cmds.rebuildCurve(centerCurve[0], ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=5, d=3, tol=0.01)
            cmds.select(meshName)
            cmds.duplicate()  # Duplicate the mesh
            dupmesh = cmds.ls(sl=1)
            cmds.ConvertSelectionToVertices()  # Convert selection to vertices
            SelVtxs = cmds.ls(sl=1, fl=1)  # Get selected vertices
            Pps = []  # Initialize vertex positions list
            Pps2 = []  # Initialize backup vertex positions list
            # Store vertex positions
            for e in SelVtxs:
                p = cmds.xform(e, t=1, q=1, ws=1)  # Get vertex position
                Pps.append(p)  # Store position in Pps
                Pps2.append(p)  # Store position in Pps2

            cmds.delete(dupmesh)  # Delete duplicated mesh
            cmds.warning('Input shapes loaded successfully')  # Display success message


def loadGround(*args):
    global ground  # Global variable to store ground object(s)
    ground = cmds.ls(sl=1)  # Store selected objects in 'ground' variable
    cmds.warning('The ground has been loaded')  # Display a warning message indicating ground has been loaded


def RandomGen(vField, inclGroundField, *args):
    # Generates random transformations for selected vertices of loaded meshes, optionally including ground interaction.
    global Pps  # Global list to store modified vertex positions
    global SelVtxs  # Global list to store selected vertices
    global Pps2  # Global backup list for vertex positions
    # Retrieve slider values
    v = cmds.floatSliderGrp(vField, q=1, v=1)
    inclGround = cmds.intSliderGrp(inclGroundField, q=1, v=1)
    try:
        if len(meshName) == 0:  # Check if meshes are loaded
            cmds.warning('Please load input shapes first')
        if len(meshName) == 1:  # If exactly one mesh is loaded
            try:
                try:
                    if inclGround == 1:  # If ground inclusion is enabled
                        # Duplicate ground and perform operations
                        ground2 = cmds.duplicate(ground)
                        cmds.xform(ground2, t=(0, 0.0, 0), r=1)
                        meshShape = cmds.listRelatives(ground2, shapes=True)
                        CPOM = cmds.createNode('closestPointOnMesh', n='CPOMG')
                        cmds.connectAttr(meshShape[0] + '.worldMatrix', CPOM + '.inputMatrix')
                        cmds.connectAttr(meshShape[0] + '.worldMesh', CPOM + '.inMesh')
                except:
                    pass

                # Duplicate selected mesh and operate on its vertices
                cmds.select(meshName)
                cmds.duplicate()
                dupmesh = cmds.ls(sl=1)
                cmds.ConvertSelectionToVertices()
                SelVtxs = cmds.ls(sl=1, fl=1)
                Ps = []
                Ps2 = []
                for e in SelVtxs:  # Store original vertex positions
                    p = cmds.xform(e, t=1, q=1, ws=1)
                    Ps.append(p)
                    Ps2.append(p)

                cmds.delete(dupmesh)  # Delete duplicated mesh
                VtxsN = len(SelVtxs)  # Delete duplicated mesh
                RandVals = []
                # Generate random transformations for each vertex
                for e in range(VtxsN):
                    Rx = rand.uniform(-v, v)
                    Ry = rand.uniform(-v, v)
                    Rz = rand.uniform(-v, v)
                    Rands = [Rx, Ry, Rz]
                    RandVals.append(Rands)

                Ppss = []
                Pps22 = []
                # Apply random transformations to vertices
                for g, f in zip(Ps, RandVals):
                    p = [
                     g[0] + f[0], g[1] + f[1], g[2] + f[2]]
                    try:
                        if inclGround == 1:  # If ground inclusion is enabled
                            cmds.setAttr(CPOM + '.ip', p[0], p[1], p[2], type='double3')
                            p = cmds.getAttr(CPOM + '.p')[0]
                    except:
                        pass

                    Ppss.append(p)
                    Pps22.append(p)

                Pps = Ppss  # Store modified vertex positions
                Pps2 = Pps22  # Store backup of vertex positions
                try:
                    if inclGround == 1:  # If ground inclusion is enabled
                        cmds.delete(CPOM, ground2)  # Delete temporary nodes
                except:
                    pass

                cmds.warning('Tree canopy mesh updated')  # Display success message
            except:
                cmds.warning('Input shapes not found')  # Warn if input shapes not found

    except:
        cmds.warning('No input shapes loaded')  # Warn if no input shapes loaded


def CreateBranches(RB1, LinAttrValField, CanopyBiasField, trunkStartField, RFactorField, mergField,*args):
    # generates a procedural tree structure based on various parameters and user inputs
    cmds.softSelect(e=1, sse=0)  # Enable soft selection with specific settings

    def Branchezz():
        # Define global variables used within the function
        global AllCUBranches
        global trunkMesh
        global Number
        global AllCUBranchesF
        global centerCurveRoot
        global AllMeshBranches
        global AllMeshBranchesF
        global fullTree

        # Retrieve user input values from UI elements
        radialAttract = cmds.radioButton(RB1, q=1, sl=1)
        randa = 0.06
        noiseFactor = 0.8
        LinearAttract = 1
        LinAttrVal = cmds.intSliderGrp(LinAttrValField, q=1, v=1)
        TrunkBias = 1.4
        CanopyBias = cmds.floatSliderGrp(CanopyBiasField, q=1, v=1)
        trunkStart = cmds.floatSliderGrp(trunkStartField, q=1, v=1)
        rads = 0.02
        RFactor = cmds.floatSliderGrp(RFactorField, q=1, v=1)
        merg = cmds.floatSliderGrp(mergField, q=1, v=1)
        createRoots = 0
        revrsTrunk = 0
        attract = 1
        crmesh = 1
        try:
            # Check if there is an existing tree object and delete it if found
            if fullTree[1] == meshName:
                try:
                    if len(centerCurve) == 0:
                        cmds.warning('Please provide a canopy mesh and a trunk curve')
                    if len(centerCurve) == 1:
                        cmds.select(centerCurve)
                        cmds.delete(fullTree[0])
                except:
                    pass
        except:
            pass
        try:
            # Ensure a canopy mesh and trunk curve are provided
            if len(centerCurve) == 0:
                cmds.warning('Please provide a canopy mesh and a trunk curve')
            if len(centerCurve) == 1:
                cmds.select(centerCurve)
                cmds.warning('createRoots')
                cmds.warning(createRoots)
                if createRoots == 1:
                    # Duplicate the ground mesh and adjust its position
                    ground2 = cmds.duplicate(ground)
                    cmds.xform(ground2, t=(0, 0.05, 0), r=1)
                    meshShape = cmds.listRelatives(ground2, shapes=True)
                    # Create and connect a closestPointOnMesh node
                    CPOM = cmds.createNode('closestPointOnMesh', n='CPOMG')
                    cmds.connectAttr(meshShape[0] + '.worldMatrix', CPOM + '.inputMatrix')
                    cmds.connectAttr(meshShape[0] + '.worldMesh', CPOM + '.inMesh')
                Ps = Pps
                Ps2 = Pps2
                x = len(SelVtxs)
                xs = []
                for i in range(100):
                    x = int(x / 2)
                    xs.append(x)
                    if x == 0:
                        break
                K = (len(xs) - 1) * 2 - 1
                Cinc = 0
                CincProg = 1.0 / (K / 0.8) / trunkStart
                Fact = 1 + 1.0 / (K / RFactor)
                K = int(K / TrunkBias)
                maxVal = len(SelVtxs) * 4
                # Create a progress window to display the growth process
                progres = cmds.window(t=' Growing Tree & its Branches :) ')
                cmds.columnLayout()
                progressControl = cmds.progressBar(maxValue=maxVal, width=380)
                cmds.showWindow(progres)
                p = 0
                # Create a curve to be used as a path for extrusion
                CU = mel.eval('curve -d 3 -p 0 0 0 -p 0 1 0 -p 0 2 0 -p 0 3 0 -k 0 -k 0 -k 0 -k 1 -k 1 -k 1')
                div = 0
                UVBranches = []
                for i in range(2):
                    if div == 0:
                        divi = 5
                    if div == 1:
                        divi = 8
                    # Create a plane to represent branch UVs and smooth it
                    cmds.polyPlane(w=0.2, h=0.2, sx=1, sy=1, n='BranchUV')
                    UVBranch = cmds.ls(sl=1)
                    UVBranches.append(UVBranch[0])
                    cmds.polySmooth(UVBranch[0], mth=1)
                    cmds.select(UVBranch[0])
                    cmds.DeleteHistory()
                    # Align the branch UV plane to the curve
                    TC = cmds.tangentConstraint(CU, UVBranch[0], weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType='vector', worldUpVector=(0, 1, 0))
                    cmds.delete(TC[0])
                    cmds.select(UVBranch[0])
                    cmds.rotate(0, 0, -90, os=1, r=1)
                    cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                    # Extrude the plane along the curve
                    cmds.polyExtrudeFacet(UVBranch[0], ch=1, keepFacesTogether=1, pvx=-0.1636236144, pvy=0.3921607532, pvz=5.33632759, divisions=divi, twist=0, taper=1, off=0, thickness=0, smoothingAngle=100, inputCurve=CU)
                    delface = UVBranch[0] + '.f[0:7]'
                    cmds.delete(delface)
                    cmds.select(UVBranch[0])
                    cmds.DeleteHistory()
                    cmds.polyProjection(UVBranch[0] + '.f[0:100]', ch=1, type='Cylindrical', ibd=1, sf=1)
                    mel.eval('polyMultiLayoutUV -lm 1 -sc 2 -rbf 0 -fr 1 -ps 0.2 -l 2 -psc 0 -su 1 -sv 1 -ou 0 -ov 0')
                    div = div + 1
                cmds.delete(CU)
                Number = 1
                Number = str(Number)
                Tr = cmds.ls(tr=1)
                nos = []
                for n in Tr:
                    if n[0:6] == 'Tree_0':
                        Number = int(n[5:8]) + 1
                        nos.append(Number)
                        Number = str(Number)
                if len(Number) == 1:
                    Number = '00' + Number
                if len(Number) == 2:
                    Number = '0' + Number
                CUs = []
                PsNs = [
                 Ps]
                inc = 1000
                CUrootsN = []
                CUroots = []
                cn = 0
                AllMeshBranches = []
                if createRoots == 1:
                    centerCurveRoot = cmds.duplicate(centerCurve)
                AllCUBranches = []
                for g in range(inc):
                    if createRoots == 1:
                        CeP = cmds.pointOnCurve(centerCurveRoot, pr=Cinc, p=1
                        )
                    CeP = cmds.pointOnCurve(centerCurve, pr=Cinc, p=1)
                    Cinc = Cinc + CincProg
                    if Cinc > 1:
                        Cinc = 1
                    CUrootsN = CUroots
                    MeshBranches = []
                    CUBranches = []
                    CUroots = []
                    PsN = []
                    Ps2N = []
                    Lcount = 0
                    if len(Ps) == 1:
                        # Duplicate the center curve to create the trunk
                        Trunk = cmds.duplicate(centerCurve)
                        cmds.select(Trunk[0])
                        cmds.rename('Tree_' + Number + '_branch_CU_' + str(cn))
                        Trunk = cmds.ls(sl=1)
                        cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                        if revrsTrunk == 0:
                            cmds.reverseCurve(Trunk[0], ch=1, rpo=1)
                        # Get the curve shape and create a nearestPointOnCurve node
                        CUShape = cmds.listRelatives(Trunk[0], s=1)
                        CPOC = cmds.createNode('nearestPointOnCurve')
                        cmds.connectAttr(CUShape[0] + '.worldSpace', CPOC + '.inputCurve')
                        cmds.setAttr(CPOC + '.inPosition', 1, 2, 3, type='double3')
                        cmds.setAttr(CPOC + '.inPositionX', avgpos[0])
                        cmds.setAttr(CPOC + '.inPositionY', avgpos[1])
                        cmds.setAttr(CPOC + '.inPositionZ', avgpos[2])
                        cutVal = cmds.getAttr(CPOC + '.parameter')
                        cmds.delete(CPOC)
                        # Detach the curve at the specified parameter
                        cmds.detachCurve(Trunk[0] + '.u[%f]' % cutVal, ch=1, cos=1, rpo=1)
                        cmds.delete()
                        # Rebuild the curve with new settings
                        cmds.rebuildCurve(Trunk[0], ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=5, d=3, tol=0.01)
                        FCvPos = cmds.xform(Trunk[0] + '.cv[0]', q=1, ws=1, t=1)
                        LCvPos = cmds.xform(Trunk[0] + '.cv[7]', q=1, ws=1, t=1)
                        cmds.select(cl=1)
                        Jt1 = cmds.joint(p=FCvPos)
                        cmds.select(cl=1)
                        Jt2 = cmds.joint(p=LCvPos)
                        cmds.select(Jt1, Jt2, Trunk[0])
                        cmds.skinCluster()  # Select the joints and the trunk curve and skin them together
                        cmds.xform(Jt2, t=avgpos, ws=1)  # Move the second joint to the average position of the first and last CVs
                        cmds.select(Trunk[0])
                        cmds.DeleteHistory()  # Select the trunk curve and delete its history
                        cmds.delete(Jt1, Jt2)  # Delete the joints created for skinning
                        cmds.polyPlane(w=rads, h=rads, sx=1, sy=1, n='Tree_' + Number + '_branch_trunkMesh_' + str(cn))  # Create a polygon plane to represent the trunk mesh
                        trunkMesh = cmds.ls(sl=1)
                        cmds.polySmooth(trunkMesh[0], mth=1)  # Smooth the trunk mesh
                        cmds.select(trunkMesh[0])
                        cmds.DeleteHistory()
                        Posi = cmds.xform(Trunk[0] + '.cv[0]', q=1, ws=1, t=1)  # Get the world space position of the first CV of the trunk curve
                        cmds.xform(trunkMesh[0], t=Posi, ws=1)  # Move the trunk mesh to the position of the first CV
                        # Apply a tangent constraint to align the trunk mesh with the trunk curve
                        TC = cmds.tangentConstraint(Trunk[0], trunkMesh[0], weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType='vector', worldUpVector=(0, 1, 0))
                        cmds.delete(TC[0])
                        # Rotate the trunk mesh and apply transformations
                        cmds.select(trunkMesh[0])
                        cmds.rotate(0, 0, -90, os=1, r=1)
                        cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                        cmds.polyExtrudeFacet(trunkMesh[0], ch=1, keepFacesTogether=1, pvx=-0.1636236144, pvy=0.3921607532, pvz=5.33632759, divisions=8, twist=0, taper=0.7, off=0, thickness=merg, smoothingAngle=100, inputCurve=Trunk[0])  # Extrude the trunk mesh along the trunk curve
                        delface = trunkMesh[0] + '.f[0:7]'
                        cmds.delete(delface)  # Delete the initial faces of the trunk mesh
                        # Select the trunk mesh and transfer UV attributes from the branches
                        cmds.select(trunkMesh[0])
                        cmds.transferAttributes(UVBranches[1], trunkMesh[0], pos=0, nml=0, uvs=2, col=0, sampleSpace=4, sourceUvSpace='map1', targetUvSpace='map1', searchMethod=3, flipUVs=0, colorBorders=1)
                        cmds.DeleteHistory()
                        cmds.delete(Trunk[0])
                        MeshBranches.append(trunkMesh[0])  # Append the trunk mesh to the list of mesh branches
                        break
                    if len(Ps) > 1:
                        for e in Ps:
                            Dists = []
                            for i in Ps2:
                                if e == i:
                                    pass
                                if e != i:
                                    Dist = (
                                     sqrt(pow(e[0] - i[0], 2) + pow(e[1] - i[1], 2) + pow(e[2] - i[2], 2)), e, i)
                                    Dists.append(Dist)  # Calculate the distance between points and store it in a list
                            sortdist = sorted(Dists)  # Sort the distances and get the closest pair of points
                            mindist = sortdist[0]
                            pos1, pos2 = mindist[1], mindist[2]
                            # Calculate the average position between the closest pair of points
                            if radialAttract == True:
                                # Calculate the average position with canopy bias
                                avgposx, avgposy, avgposz = (pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2 - mindist[0] / CanopyBias, (pos1[2] + pos2[2]) / 2
                                avgposx1, avgposy1, avgposz1 = (avgposx + CeP[0]) / 2, (avgposy + CeP[1]) / 2, (avgposz + CeP[2]) / 2
                                # Adjust the average position based on LinearAttract flag
                                if LinearAttract == 0:
                                    for f in range(K):
                                        avgposx1, avgposy1, avgposz1 = (avgposx + avgposx1) / 2, (avgposy + avgposy1) / 2, (avgposz + avgposz1) / 2
                                    avgpos = (
                                     avgposx1, avgposy1, avgposz1)
                                if LinearAttract == 1:
                                    for f in range(LinAttrVal):
                                        avgposx1, avgposy1, avgposz1 = (avgposx + avgposx1) / 2, (avgposy + avgposy1) / 2, (avgposz + avgposz1) / 2
                                # Further adjustments based on root creation flag and number of points
                                if createRoots == 0:
                                    if len(Ps) < 5:
                                        LinAttrVal = 0
                                avgpos = (
                                 avgposx1, avgposy1, avgposz1)
                                if createRoots == 1:
                                    if len(Ps) <= 3 and len(Ps) > 2:
                                        cmds.setAttr(CPOM + '.ip', avgposx1, avgposy1, avgposz1, type='double3')
                                        avgpos = cmds.getAttr(CPOM + '.p')[0]
                                        for f in range(1):
                                            avgposx1, avgposy1, avgposz1 = (avgpos[0] + avgposx1) / 2, (avgpos[1] + avgposy1) / 2, (avgpos[2] + avgposz1) / 2
                                        avgpos = (
                                         avgposx1, avgposy1, avgposz1)
                                    if len(Ps) > 3 and len(Ps) <= 8:
                                        cmds.setAttr(CPOM + '.ip', avgposx1, avgposy1, avgposz1, type='double3')
                                        avgpos = cmds.getAttr(CPOM + '.p')[0]
                                        for f in range(3):
                                            avgposx1, avgposy1, avgposz1 = (avgpos[0] + avgposx1) / 2, (avgpos[1] + avgposy1) / 2, (avgpos[2] + avgposz1) / 2
                                        avgpos = (
                                         avgposx1, avgposy1, avgposz1)
                                    if len(Ps) > 8:
                                        cmds.setAttr(CPOM + '.ip', avgposx1, avgposy1, avgposz1, type='double3')
                                        avgpos = cmds.getAttr(CPOM + '.p')[0]
                                        for f in range(8):
                                            avgposx1, avgposy1, avgposz1 = (avgpos[0] + avgposx1) / 2, (avgpos[1] + avgposy1) / 2, (avgpos[2] + avgposz1) / 2
                                        avgpos = (
                                         avgposx1, avgposy1, avgposz1)
                                # Apply random variations
                                raX = rand.uniform(-randa, randa)
                                raY = 0
                                raZ = rand.uniform(-randa, randa)
                                raX2 = rand.uniform(-randa, randa)
                                raY2 = 0
                                raZ2 = rand.uniform(-randa, randa)
                                mid1 = (e[0] + raX, ((avgposy1 + e[1]) / 2 + e[1]) / 2 + raY, e[2] + raZ)
                                mid2 = (avgposx1 + raX2, ((avgposy1 + e[1]) / 2 + avgposy1) / 2 + raY2, avgposz1 + raZ2)
                            if attract == 0:
                                # For non-radial attraction, calculate the average position
                                avgposx, avgposy, avgposz = (pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2 - mindist[0] / CanopyBias, (pos1[2] + pos2[2]) / 2
                                avgpos = (avgposx, avgposy, avgposz)
                                # Apply random variations
                                raX = rand.uniform(-randa, randa)
                                raY = 0
                                raZ = rand.uniform(-randa, randa)
                                raX2 = rand.uniform(-randa, randa)
                                raY2 = 0
                                raZ2 = rand.uniform(-randa, randa)
                                mid1 = (e[0] + raX, ((avgposy + e[1]) / 2 + e[1]) / 2 + raY, e[2] + raZ)
                                mid2 = (avgposx + raX2, ((avgposy + e[1]) / 2 + avgposy) / 2 + raY2, avgposz + raZ2)
                            # Append the new average position to the lists
                            PsN.append(avgpos)
                            Ps2N.append(avgpos)
                            midd = (
                             (avgpos[0] + e[0]) / 2, (avgpos[1] + e[1]) / 2, (avgpos[2] + e[2]) / 2)  # Calculate the midpoint for the curve
                            CU = cmds.curve(p=(avgpos, midd, e), d=1, n='Tree_' + Number + '_branch_CU_' + str(cn))  # Create a curve between the average position, midpoint, and endpoint
                            cmds.rebuildCurve(ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=4, d=1, tol=0.01)  # Rebuild the curve for smoothness
                            # Adjust control vertices (CVs) of the curve with random variations
                            CUbcv = (CU + '.cv[1]', CU + '.cv[2]', CU + '.cv[3]')
                            cuLen = cmds.arclen(CU)
                            for eb in CUbcv:
                                rrX = rand.uniform(-randa, randa) * cuLen
                                rrY = rand.uniform(-randa, randa) * cuLen
                                rrZ = rand.uniform(-randa, randa) * cuLen
                                cmds.xform(eb, t=(rrX, rrY, rrZ), r=1)
                            CUBranches.append(CU)  # Append the curve to the list of branches
                            CuRootP = cmds.xform(CU + '.cv[0]', q=1, ws=1, t=1)  # Get the root position of the curve
                            cmds.xform(CU, sp=CuRootP, rp=CuRootP, ws=1)
                            CUs.append(CU)  # Add the curve to the list of all curves
                            if crmesh == 0:  # Check if mesh creation is required
                                CUroot = (
                                 avgpos, e, CU)
                            if crmesh == 1:
                                # Create a polygon plane for the branch mesh
                                cmds.polyPlane(w=rads, h=rads, sx=1, sy=1, n='Tree_' + Number + '_branch_Mesh_' + str(cn))
                                mesh = cmds.ls(sl=1)
                                cmds.cluster()
                                meshC = cmds.ls(sl=1)
                                cmds.polySmooth(mesh[0], mth=1)
                                # Position the mesh cluster on the curve
                                cmds.select(mesh[0])
                                CP = cmds.pointOnCurve(CU, pr=0.02, p=1)
                                cmds.xform(meshC[0], t=CP, ws=1)
                                TC = cmds.tangentConstraint(CU, meshC[0], weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType='vector', worldUpVector=(0, 1, 0))
                                cmds.delete(TC[0])
                                # Rotate and transform the mesh cluster
                                cmds.select(meshC[0])
                                cmds.rotate(0, 0, -90, os=1, r=1)
                                cmds.xform(meshC[0], t=avgpos, ws=1)
                                cmds.makeIdentity(apply=1, t=1, r=1, s=1, n=0, pn=1)
                                cmds.polyExtrudeFacet(mesh[0], ch=1, keepFacesTogether=1, pvx=-0.1636236144, pvy=0.3921607532, pvz=5.33632759, divisions=5, twist=0, taper=0.6, off=0, thickness=-0.05 * cuLen, smoothingAngle=100, inputCurve=CU)  # Extrude the polygon facet along the curve
                                delface = mesh[0] + '.f[0:7]'
                                cmds.delete(delface)  # Delete unnecessary faces from the mesh
                                cmds.select(mesh[0])
                                cmds.transferAttributes(UVBranches[0], mesh[0], pos=0, nml=0, uvs=2, col=0, sampleSpace=4, sourceUvSpace='map1', targetUvSpace='map1', searchMethod=3, flipUVs=0, colorBorders=1)  # Transfer UV attributes from the original branch to the mesh
                                CUroot = (
                                 avgpos, e, CU, mesh[0], meshC[0])
                                cn = cn + 1
                            CUroots.append(CUroot)  # Append the root information to the list of roots
                            MeshBranches.append(mesh[0])  # Append the mesh branch to the list of mesh branches
                            progressInc = cmds.progressBar(progressControl, edit=True, pr=p + 1)  # Update progress bar
                            p = p + 1
                        # Remove duplicate points from the lists
                        PsN = list(set(PsN))
                        Ps2N = list(set(Ps2N))
                        PsNs.append(Ps2N)  # Append the modified list of points to the main list
                        Ps = PsN
                        Ps2 = Ps2N
                        inc = inc - 1  # Decrease the iteration count
                    AllMeshBranches.append(MeshBranches)  # Append all mesh branches to the list of all mesh branches
                    AllCUBranches.append(CUBranches)
                    # Adjust growth factors
                    rads = rads * Fact
                    randa = randa * noiseFactor
                    merg = merg * 1.2
                    K = K - 1
                    # Check for connected roots and parent branches
                    if len(CUrootsN) > 0:
                        All = []
                        for ee in CUrootsN:
                            for ii in CUroots:
                                if ee[0] == ii[1]:
                                    if crmesh == 0:
                                        cmds.parent(ee[2], ii[2])
                                    if crmesh == 1:
                                        cmds.parent(ee[3], ii[3])
                                        np = cmds.pointOnCurve(ii[2], pr=0.83, p=1)
                                        cmds.reverseCurve(ee[2], rpo=1)
                                        cmds.curve(ee[2], a=1, p=np)
                                        cmds.reverseCurve(ee[2], rpo=1)
                                        cmds.xform(ee[4], t=np, ws=1)
                                        cmds.xform(ee[3], sp=np, rp=np, ws=1)
                                        if len(CUroots) < 3:
                                            np2 = cmds.pointOnCurve(ii[2], pr=0, p=1)
                                            cmds.xform(ii[3], sp=np, rp=np2, ws=1)
                                All.append(ii[2])
                                All.append(ii[3])
                AllCUBranchesF = [ val for sublist in AllCUBranches for val in sublist ]  # Flatten the list of all branches
                # Parent mesh branches for visual hierarchy
                cmds.parent(All[1], MeshBranches[0])
                cmds.parent(All[3], MeshBranches[0])
                fullTree = (
                 cmds.group(CUroots, MeshBranches, n='Tree_' + Number + '_GRP'), meshName)  # Group all elements of the tree under a main group node
                cmds.select(cl=1)
                AllMeshBranches.reverse()  # Reverse the list of all mesh branches
                AllMeshBranchesF = [ val for sublist in AllMeshBranches for val in sublist ]  # Flatten the list of all mesh branches
                cmds.select(AllMeshBranchesF, trunkMesh[0])  # Select all mesh branches and the trunk mesh
                cmds.pickWalk(d='down')  # Pick walk to descend through hierarchy
                cmds.sets(name='Tree_' + Number + '_Branches_Set')  # Create a set for all branches
                cmds.delete(UVBranches)  # Delete UV branches
                if createRoots == 1:
                    cmds.delete(CPOM, ground2, centerCurveRoot)  # Clean up if root creation was enabled
                # Final adjustments and operations on the main trunk mesh
                MB = MeshBranches[0]
                ChildBranch = cmds.listRelatives(MB, c=1)
                vtxLoop = (MB + '.vtx[15]', MB + '.vtx[23]', MB + '.vtx[31]', MB + '.vtx[39]', MB + '.vtx[47]', MB + '.vtx[55]', MB + '.vtx[63]', MB + '.vtx[71]')
                cmds.transferAttributes(ChildBranch[1], vtxLoop, transferPositions=1)
                cmds.select(MB)
                cmds.DeleteHistory()
                vtxLoop = ChildBranch[1] + '.vtx[0:7]'
                cmds.transferAttributes(MB, vtxLoop, transferPositions=1)
                cmds.select(ChildBranch[1])
                cmds.DeleteHistory()
                vtxLoop = ChildBranch[2] + '.vtx[0:7]'
                cmds.transferAttributes(MB, vtxLoop, transferPositions=1)
                cmds.select(ChildBranch[2])
                cmds.DeleteHistory()
                # Iterate through all mesh branches for further adjustments
                for b in AllMeshBranches:
                    try:
                        for a in b:
                            ChildBranch = cmds.listRelatives(a, c=1)
                            ParentBranch = cmds.listRelatives(a, p=1)
                            vtxLoop = (a + '.vtx[12]', a + '.vtx[17]', a + '.vtx[22]', a + '.vtx[27]', a + '.vtx[32]', a + '.vtx[37]', a + '.vtx[42]', a + '.vtx[47]')
                            vtxLoop2 = a + '.vtx[0:7]'
                            cmds.transferAttributes(ParentBranch[0], vtxLoop2, transferPositions=1)
                            cmds.transferAttributes(ChildBranch[1], vtxLoop, transferPositions=1)
                            cmds.select(a)
                            cmds.DeleteHistory()
                            progressInc = cmds.progressBar(progressControl, edit=True, pr=p + 1)
                            p = p + 1
                    except:
                        pass
                # Clear selection and finalize
                cmds.select(cl=1)
                cmds.flushUndo()
                cmds.deleteUI(progres)
                cmds.warning('Your Tree has Grown :)')
        except:
            cmds.warning(' Please 1st Load Input Shapes')
    Branchezz()


def combine_selected_meshes(*args):
    # Composite crown network
    selected_objects = cmds.ls(selection=True)  # Gets the currently selected object
    if not selected_objects:  # Check for selected objects
        cmds.warning("No objects selected.")
        return
    combined_object = cmds.polyUnite(selected_objects, name='combined_mesh')[0]  # Combine the selected object
    cmds.delete(combined_object, constructionHistory=True)  # Delete history to ensure a clean combined network
    cmds.select(combined_object)
    cmds.confirmDialog(title='Success', message='Meshes combined successfully!', button=['OK'])  # Ensure that the newly created object is selected


def generate_vine(*args):
    thickness_value = cmds.floatSliderGrp(thickness, query=True, value=True)
    leaf_size_value = cmds.floatSliderGrp(leaf_size, query=True, value=True)
    leaf_density_value = cmds.floatSliderGrp(leaf_density, query=True, value=True)

    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.error("Please select a curve.")
        return

    curve = selected_objects[0]

    # Check if the selected object is a valid NURBS curve
    shapes = cmds.listRelatives(curve, shapes=True)
    if not shapes or cmds.nodeType(shapes[0]) != 'nurbsCurve':
        cmds.error("Please select a NURBS curve.")
        return

    create_vine(curve, thickness_value, leaf_size_value, leaf_density_value)

def create_vine(curve, thickness, leaf_size, leaf_density):
    # Create the vine by extruding a circle along the curve
    circle = cmds.circle(radius=thickness, sections=8, normal=(0, 1, 0))[0]
    extruded = cmds.extrude(circle, curve, ch=True, rn=False, po=0, et=2, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1)[0]
    
    # Randomly place leaves along the vine
    place_leaves(extruded, curve, leaf_size, leaf_density, thickness)
    cmds.delete(circle)

def place_leaves(extruded, curve, leaf_size, leaf_density, thickness):
    # Get the length of the curve
    curve_length = cmds.arclen(curve)
    leaves = []
    
    for i in range(int(leaf_density)):
        # Randomly position along the curve's parameter range
        param = rand.uniform(0, 1)
        point_on_curve = cmds.pointOnCurve(curve, pr=param, p=True, top=True)
        if not point_on_curve:
            cmds.warning(f"Failed to get point on curve at parameter {param}")
            continue
        
        # Create a leaf plane
        leaf = cmds.polyPlane(width=leaf_size, height=leaf_size, sx=1, sy=1)[0]
        
        # Position the leaf at the point on the curve
        cmds.move(point_on_curve[0], point_on_curve[1], point_on_curve[2], leaf)
        
        # Align the leaf with the curve tangent
        tangent = cmds.pointOnCurve(curve, pr=param, nt=True)
        if not tangent:
            cmds.warning(f"Failed to get tangent at parameter {param}")
            continue
        cmds.rotate(tangent[0], tangent[1], tangent[2], leaf, ws=True, pcp=True)
        
        # Move the leaf along the normal to avoid placing it inside the vine
        normal = cmds.pointOnCurve(curve, pr=param, nn=True)
        if not normal:
            cmds.warning(f"Failed to get normal at parameter {param}")
            continue
        cmds.move(normal[0] * (thickness + leaf_size/2), normal[1] * (thickness + leaf_size/2), normal[2] * (thickness + leaf_size/2), leaf, relative=True)
        
        # Randomly rotate the leaf
        cmds.rotate(rand.uniform(0, 360), rand.uniform(0, 360), rand.uniform(0, 360), leaf)
        
        # Attach leaf to the vine (optional: this is just a parenting step)
        cmds.parent(leaf, extruded)
        leaves.append(leaf)


def leafland_gui_set():
    # Plug-in ui display page
    windowID = 'Branchez'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    global thickness, leaf_size, leaf_density
    global shader_suite_path
    maya_version = cmds.about(version=True)  # Determine Maya version
    # Create main window
    cmds.window(windowID, title='LeafyLand V 1.0', sizeable=1, menuBar=1, resizeToFitChildren=1, h=700, w=430)
    cmds.scrollLayout('scrollLayout')
    cmds.columnLayout(adjustableColumn=1)
    # Menu for Model Library Settings
    cmds.menu(label="Model base setting", to=True)
    cmds.menuItem(label="Model base setting", c=mot_lib_win_set)
    # Add cover image
    current_script_path = cmds.file(query=True, location=True)
    script_dir = os.path.dirname(current_script_path)
    image_path = os.path.join(script_dir, "media", "111.jpg")  # Relative path to the picture path
    cmds.symbolButton(image=image_path, width=400, height=130)

    cmds.text(label='')
    cmds.setParent(top=1)
    cmds.columnLayout(adjustableColumn=1)
    cmds.setParent(top=1)
    # Vine Formation Frame
    cmds.frameLayout(label='Vine Formation', fn='boldLabelFont', bgc=(0.3, 0.4, 0.5), collapsable=1, collapse=0)
    cmds.setParent()
    cmds.text(label='')
    cmds.text(label="  Select the curve and set parameters", al='left', bgc=(0.3,
                                                                                    0.3,
                                                                                    0.35))
    thickness = cmds.floatSliderGrp(label='vine thickness', field=True, minValue=0.00, maxValue=0.20, value=0.05, step=0.01)  # Vine thickness slider
    leaf_size = cmds.floatSliderGrp(label='leaf size', field=True, minValue=0.1, maxValue=2.0, value=0.5)  # Leaf size slider
    leaf_density = cmds.floatSliderGrp(label='leaf density', field=True, minValue=1, maxValue=200, value=75)  # Leaf density slider
    cmds.button(label="Generate Vine", command=partial(generate_vine), bgc=(0.4, 
                                                                                                0.6,
                                                                                                0.6))  # Button to generate vine
    cmds.setParent(top=1)
    cmds.separator(h=10)
    cmds.setParent(top=1)
    cmds.frameLayout(label='Trunk Formation', fn='boldLabelFont', bgc=(0.3, 0.4, 0.5), collapsable=1, collapse=0)  # Trunk Formation Frame
    cmds.setParent()
    cmds.frameLayout(label='create branches', fn='obliqueLabelFont', bgc=(0.2, 0.4,
                                                                                        0.4), collapsable=1, collapse=0)  # Branching Frame
    cmds.text(label='')
    cmds.text(label='  Select all meshes if your crown consists of multiple meshes', al='left', bgc=(0.3,
                                                                                                              0.3,
                                                                                                              0.35))
    # Add a button that, when clicked, calls the combine_selected_meshes function
    cmds.button(label="Combine Selected Meshes", command=partial(combine_selected_meshes), bgc=(0.4, 
                                                                                                0.6,
                                                                                                0.6))
    cmds.text(label='  Select 1 trunk curve as the trunk and 1 mesh', al='left', bgc=(0.3,
                                                                                                              0.3,
                                                                                                              0.35))
    vVal = cmds.floatSliderGrp(label='random seed ', field=1, minValue=0, maxValue=1, precision=2, value=0.3, step=0.1)  # Random seed slider
    inclGroundVal = cmds.intSliderGrp(label='Include Creep/Ground mesh', field=1, minValue=0, maxValue=1, value=0, step=1, en=0, vis=0, h=1)  # Include Creep/Ground mesh slider
    cmds.rowColumnLayout(numberOfRows=1, cs=[10, 5])
    # Button to load curves and surfaces
    cmds.button(label=' Load Curves and Surfaces', command=partial(LoadMesh_Curves), bgc=(0.4,
                                                                                  0.6,
                                                                                  0.6), w=194)
    # Button to apply randomization
    cmds.button(label=' Apply Randomization', command=partial(RandomGen, vVal, inclGroundVal), bgc=(0.4,
                                                                                                          0.6,
                                                                                                          0.6), w=194)
    cmds.setParent(u=1)
    cmds.separator(h=1)
    # Branch shape parameter section
    cmds.text(label='   Branch shape parameter:', al='left', fn='boldLabelFont', bgc=(0.35,
                                                                                       0.4,
                                                                                       0.4), h=25)
    RFactorVal = cmds.floatSliderGrp(label='trunk width', field=1, minValue=1, maxValue=10, precision=2, value=4.5, step=0.1)  # Trunk width slider
    mergVal = cmds.floatSliderGrp(label='branch merging ', field=1, minValue=0.01, maxValue=0.04, precision=2, value=0.02, step=0.1, vis=0, en=0, h=1)  # Branch merging slider
    cmds.separator(h=1)
    # Tree shape parameter section
    cmds.text(label='   Tree shape parameter:', al='left', fn='boldLabelFont', bgc=(0.35,
                                                                                     0.4,
                                                                                     0.4), h=25)
    cmds.radioCollection()
    RB1 = cmds.radioButton('Crown Profile ', sl=1, bgc=(0.3, 0.3, 0.35))
    LinAttrValVal = cmds.intSliderGrp(label='canopy radiating shape', field=1, minValue=1, maxValue=5, value=2, step=1, en=1, vis=1)  # Canopy radiating shape slider
    cmds.text(label='gentle <---                 ---> winding   ', al='right')
    CanopyBiasVal = cmds.floatSliderGrp(label='intermediate shape lift ', field=1, minValue=1.5, maxValue=10, precision=2, value=4, step=0.1)  # Intermediate shape lift slider
    trunkStartVal = cmds.floatSliderGrp(label='trunk starting position ', field=1, minValue=0.9, maxValue=5, precision=2, value=1, step=0.1)  # Trunk starting position slider
    # Button to create branches
    cmds.button(label='Create Branches', command=partial(CreateBranches, RB1, LinAttrValVal, CanopyBiasVal, trunkStartVal, RFactorVal, mergVal), bgc=(0.4,
                                                                                                                                                                                                                            0.6,
                                                                                                                                                                                                                            0.6))
    # Branches or Leaves Material Selection Frame
    cmds.setParent(top=1)
    cmds.separator(h=10)
    cmds.setParent(top=1)
    cmds.frameLayout(label='Branches or Leaves Material Selection', fn='boldLabelFont', bgc=(0.3, 0.4, 0.5), collapsable=1, collapse=0)
    cmds.setParent()
    cmds.text(label='')
    cmds.separator(h=1)
    cmds.columnLayout(adj=True)
    LayoutFrameTabLayout_ArnoldLib()  # Call to function to create layout for Arnold library
    cmds.setParent(u=1)
    cmds.text(label='')
    cmds.setParent(u=1)
    # Branching Movement Frame
    cmds.setParent(top=1)
    cmds.separator(h=10)
    cmds.setParent(top=1)
    cmds.frameLayout(label='Branch Movement', collapsable=1, fn='boldLabelFont', bgc=(0.3, 0.4, 0.5), collapse=0)
    cmds.text(label='')
    cmds.separator(h=1)
    cmds.text(label='   Branch-motion parameter:', al='left', fn='boldLabelFont', bgc=(0.35,
                                                                                                           0.4,
                                                                                                           0.4), h=25)
    freqVal = cmds.floatSliderGrp(label=' swing frequency ', field=1, minValue=1, maxValue=20, precision=2, value=10, step=0.1, vis=1, en=1)  # Swing frequency slider
    intensVal = cmds.floatSliderGrp(label=' swing strength ', field=1, minValue=0.1, maxValue=20, precision=2, value=1, step=0.1, vis=1, en=1)  # Swing strength slider
    turbVal = cmds.floatSliderGrp(label=' swing disturbance ', field=1, minValue=1, maxValue=50, precision=2, value=3, step=0.1, vis=1, en=1)  # Swing disturbance slider
    # Swing increment settings for branch animation
    cmds.text(label='   Swing increment (from trunk to branch tip) : ', al='left', fn='boldLabelFont', bgc=(0.35,
                                                                                                                  0.4,
                                                                                                                  0.4), h=25)
    freq_incrVal = cmds.floatSliderGrp(label=' frequency increase ', field=1, minValue=0, maxValue=5, precision=2, value=1, step=0.1, vis=1, en=1)  # Frequency increase amplitude slider
    intens_incrVal = cmds.floatSliderGrp(label=' strength increase ', field=1, minValue=0, maxValue=5, precision=2, value=0.5, step=0.1, vis=1, en=1)
    ChkBox = cmds.checkBox(label=' Only the selected branches ', v=0)
    # Row layout for branch animation buttons
    cmds.rowColumnLayout(numberOfRows=1, cs=[10, 5])
    cmds.button(label='Add Branch Animation', command=partial(BranchDynamics, freqVal, freq_incrVal, intensVal, intens_incrVal, turbVal, ChkBox), bgc=(0.4,
                                                                                                                                                                    0.6,
                                                                                                                                                                    0.6), w=194)
    cmds.button(label='Delete Animation', command=partial(Del_Branch_Dyna, ChkBox), bgc=(0.7,
                                                                                               0.6,
                                                                                               0.5), w=194)
    cmds.setParent(top=1)
    cmds.separator(h=10)
    cmds.setParent(top=1)
    # Frame layout for leaf settings
    cmds.frameLayout(label='Leaf', fn='boldLabelFont', bgc=(0.3, 0.4, 0.5), collapsable=1, collapse=0)
    cmds.setParent()
    cmds.frameLayout(label='Create Leaves', collapsable=1, fn='obliqueLabelFont', bgc=(0.2,
                                                                                       0.4,
                                                                                       0.4), collapse=0)
    cmds.separator(h=10)
    # Row layout for leaf creation buttons
    cmds.rowColumnLayout(numberOfRows=1, cs=[10, 5])
    cmds.button(label='Initial Blade', command=partial(masterLeaf), bgc=(0.4,
                                                                                     0.7,
                                                                                     0.6), w=194)
    cmds.button(label='Loading Main Leaf', command=partial(loadLeaf), bgc=(0.4, 0.7,
                                                                          0.6), w=194)
    cmds.separator(h=1)
    cmds.setParent(u=1)
    # Leaf parameter settings
    cmds.text(label='   Leaf parameter:', al='left', fn='boldLabelFont', bgc=(0.35,
                                                                                 0.4,
                                                                                 0.4), h=25)
    cmds.text(label='    Leaf distribution:', al='left', h=25, fn='boldLabelFont')
    CuLevelsVal = cmds.intSliderGrp(label='branch leaf', field=1, minValue=1, maxValue=20, value=2, step=1)
    leafNumVal = cmds.intSliderGrp(label='number of leaves', field=1, minValue=1, maxValue=50, value=3, step=1)
    spacingVal = cmds.floatSliderGrp(label='leaf spacing', field=1, minValue=0.01, maxValue=1, precision=2, value=0.15, step=0.1, vis=1, en=1)
    # Leaf scaling and direction settings
    cmds.text(label='    Leaf scaling & direction:', al='left', h=25, fn='boldLabelFont')
    scaleVal = cmds.floatSliderGrp(label='global scaling ', field=1, minValue=0.01, maxValue=3, precision=2, value=1, step=0.1, vis=1, en=1)
    scaleIncVal = cmds.floatSliderGrp(label='scaling increment ', field=1, minValue=0.01, maxValue=20, precision=2, value=0.05, step=0.1, vis=1, en=1)
    cmds.text(label='')
    GravityVal = cmds.floatSliderGrp(label='leaf sag ', field=1, minValue=-50, maxValue=100, precision=2, value=30, step=0.1, vis=1, en=1)
    GravIncVal = cmds.floatSliderGrp(label='sag increment ', field=1, minValue=1, maxValue=20, precision=2, value=0, step=0.1, vis=1, en=1)
    rotateVal = cmds.floatSliderGrp(label='leaf diffusion', field=1, minValue=1, maxValue=80, precision=2, value=30, step=0.1, vis=1, en=1)
    rotateIncVal = cmds.floatSliderGrp(label='diffusion increment ', field=1, minValue=1, maxValue=20, precision=2, value=8, step=0.1, vis=1, en=1)
    tiltVal = cmds.floatSliderGrp(label='leaf tilt', field=1, minValue=1, maxValue=80, precision=2, value=35, step=0.1, vis=1, en=1)
    # Row layout for create leaves button
    cmds.rowColumnLayout(numberOfRows=1, cs=[10, 10])
    cmds.button(label='Create Leaves', command=partial(leavesGen, CuLevelsVal, leafNumVal, GravityVal, GravIncVal, rotateVal, rotateIncVal, tiltVal, spacingVal, scaleVal, scaleIncVal), bgc=(0.4,
                                                                                                                                                                                              0.7,
                                                                                                                                                                                              0.6), w=395)
    cmds.setParent(u=1)
    cmds.setParent(u=1)
    # Frame layout for leaf selection
    cmds.frameLayout(label='Leaves selection', fn='obliqueLabelFont', bgc=(0.2, 0.4, 0.4), collapsable=1, collapse=1)
    cmds.button(label='Load Tree', command=partial(autoHierarchyDef), bgc=(0.4, 0.7,
                                                                           0.6))
    cmds.button(label='Select Leaves', command=partial(selectLeaves), bgc=(0.4, 0.7,
                                                                           0.6))
    
    cmds.setParent(u=1)
    cmds.setParent(u=1)
    # Frame layout for leaf movement
    cmds.setParent(top=1)
    cmds.separator(h=10)
    cmds.setParent(top=1)
    cmds.frameLayout(label='Leaf movement', collapsable=1, fn='boldLabelFont', bgc=(0.3,
                                                                                                0.4,
                                                                                                0.5), collapse=0)
    cmds.text(label='')
    cmds.text(label='   Leaf movement parameter', al='left', fn='boldLabelFont', bgc=(0.35,
                                                                                                     0.4,
                                                                                                     0.4), h=25)
    # Leaf movement parameter sliders
    freq2Val = cmds.floatSliderGrp(label='swing frequency ', field=1, minValue=1, maxValue=20, precision=2, value=1, step=0.1, vis=1, en=1)
    intens2Val = cmds.floatSliderGrp(label=' rocking strength ', field=1, minValue=1, maxValue=50, precision=2, value=5, step=0.1, vis=1, en=1)
    turb2Val = cmds.floatSliderGrp(label=' disturb ', field=1, minValue=1, maxValue=50, precision=2, value=3, step=0.1, vis=1, en=1)
    turbVariVal = cmds.floatSliderGrp(label=' disturb change ', field=1, minValue=0, maxValue=1, precision=2, value=0.5, step=0.1, vis=1, en=1)
    # Row layout for leaf animation buttons
    cmds.rowColumnLayout(numberOfRows=1, cs=[10, 3])
    cmds.button(label='Add Leaf Animation', command=partial(leaves_Dynamics, freq2Val, intens2Val, turb2Val, turbVariVal), bgc=(0.4,
                                                                                                                                             0.7,
                                                                                                                                             0.6), w=193)
    cmds.separator(h=5)
    cmds.button(label='Remove Animation', command=partial(Del_LeafDyna), bgc=(0.8,
                                                                                    0.7,
                                                                                    0.6), w=193)
    cmds.setParent(top=1)
    cmds.setParent(top=1)
    cmds.showWindow(windowID)  # Show the main window


if __name__ == "__main__":
    leafland_gui_set()
