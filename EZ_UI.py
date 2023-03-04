#03/04/2023
#V_1.0
#program made by adelo, 
#unlockCtrl and offsetCtrl are forked.

import maya.cmds as cmd

class AS_Window(object):
    
    def __init__(self):
        
        self.window = "AS_Window"
        self.title = "EZ UI"
        self.size = (400, 400)
        
        #close all previous panels
        if cmd.window(self.window, exists = True):
            cmd.deleteUI(self.window, window = True)
        
        #create new window
        self.window = cmd.window(self.window, title=self.title, widthHeight=self.size)
        cmd.columnLayout(adjustableColumn = True)
        cmd.text("script panel")
        cmd.separator(height = 30)
        self.locAtCentBTN= cmd.button(label='Locator at center of selection', command=self.locAtCent)
        self.unlockctrlBTN= cmd.button(label='Unlock controls',  command=self.unlockCtrl)
        self.offsetScriptBTN= cmd.button(label='Offset controller | object clean', command=self.offsetScript)
        self.offsetObjBTN= cmd.button(label='Offset object', command=self.offsetObj)
        
               
        #display new window
        cmd.showWindow()
        
    
    def locAtCent(self, *args):
        
        tempArray = cmds.ls(sl=True) 
        
        cluster1 = cmd.cluster( rel=True )
        locator1 = cmd.spaceLocator( p=(0, 0, 0),)
        pconst = cmd.parentConstraint( cluster1, locator1, mo = False )
        cmds.delete(cluster1, pconst )
    
    
    def unlockCtrl(self, *args):
        
        selList = cmds.ls(sl=1, ap=1, tr=1 ) #sl = check selection/ ap = return full name/ tr = returns transform
                
        for sel in selList :
            
            cmd.setAttr((sel + ".tx"), k=1, l=0)
            cmd.setAttr((sel + ".ty"), k=1, l=0)
            cmd.setAttr((sel + ".tz"), k=1, l=0)
            
            cmd.setAttr((sel + ".rx"), k=1, l=0)
            cmd.setAttr((sel + ".ry"), k=1, l=0)
            cmd.setAttr((sel + ".rz"), k=1, l=0)
            
            cmd.setAttr((sel + ".sx"), k=1, l=0)
            cmd.setAttr((sel + ".sy"), k=1, l=0)
            cmd.setAttr((sel + ".sz"), k=1, l=0)
            
            cmd.setAttr((sel + ".v"), k=1, l=0)
            
    def offsetScript(self, *args):
        
        my_sel = cmd.ls(sl=True)
        if len(my_sel) < 2 or len(my_sel) > 3:
            cmd.error("Please select atleast 1 ctrlCurve and 1 joints")
        ctl_og = cmd.group(empty = True)
        cmd.parent(my_sel[0], my_sel[1])
        cmd.parent(ctl_og, my_sel[1])
        
        axis = ["x", "y", "z"]
        for i in axis:
            cmd.setAttr(my_sel[0] + ".t" + i, 0)
            cmd.setAttr(my_sel[0] + ".r" + i, 0)
            cmd.setAttr(ctl_og + ".t" + i, 0)
            cmd.setAttr(ctl_og + ".r" + i, 0)
        
        cmd.parent(ctl_og, w=True)
        cmd.parent(my_sel[0], ctl_og)
        
        newname = cmd.rename(my_sel[0], my_sel[1] + "_CTL")
        grpname = newname.split("_CTL")[0]
        og_name = cmd.rename(ctl_og, grpname + "_OG")
        cmd.parentConstraint(newname, my_sel[1], mo=False)
        if len(my_sel) == 3:
            cmd.parentConstraint(my_sel[2], og_name, mo=True)
            
    def offsetObj(self, *args):
        sel = cmd.ls(sl=True)
        pconst = cmd.parentConstraint ( sel[0], sel[1], mo = False )
        cmd.delete( pconst )
    
        
            
myWindow = AS_Window() 


