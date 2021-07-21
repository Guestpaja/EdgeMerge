# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "EdgeMerge",
    "author" : "Pavel Hradil (Guestpaja)",
    "description" : "A simple add-on to help with cleaning up after boolean or knife operations",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from os import close
import bpy
import bmesh
from bpy.types import GPENCIL_MT_move_to_layer
import numpy as np

def CleanUp():

    def correct_verts(start_vert, verts, corrected_verts):
        
        nonlocal closed_loop
        
        #Correct the indices such that the vert_ids correspond to how the verts are arranged on the model
        adjacent_verts = [edge.other_vert(start_vert) for edge in start_vert.link_edges]
        counter = 0

        #Check for potential loose ends
        for adjacent_vert in adjacent_verts:
            if adjacent_vert in verts:
                    counter += 1
            else:
                pass

        if counter == 2:
            pass
        elif counter == 1:
            closed_loop = False
        else:
            print("Operation failed, please check for any loose vertices")
            raise Exception
        
        #Check if/which vert of the adjacent ones was also selected and if it hasn't been corrected, correct it
        for adjacent_vert in adjacent_verts:
            
            if adjacent_vert in verts and adjacent_vert not in corrected_verts:
                    
                    if closed_loop:
                        corrected_verts.append(adjacent_vert)
                        correct_verts(adjacent_vert, verts, corrected_verts)
                    else:
                        corrected_verts.insert(0, adjacent_vert)
                        correct_verts(adjacent_vert, verts, corrected_verts)
                
            else:
                pass
        
    #Set up vars
    verts = []
    obj = bpy.context.object

    #Check for edit mode, if the mode isn't edit mode pass
    if obj.mode == 'EDIT':
        
        #Get selected verts
        bm = bmesh.from_edit_mesh(obj.data)

        for vert in bm.verts:
            if vert.select:
                verts.append(vert)
            else:
                pass
        
        #Set up vars
        corrected_verts = [verts[0]]
        closed_loop = True

        correct_verts(verts[0], verts, corrected_verts)
        
        
    else:
        print("Object is not in edit mode.")
    
    #Change modes to "apply" changes
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')

#Create operator
class CleanUpOperator(bpy.types.Operator):
    
    bl_idname = "edgemerge.edge_clean_up"
    bl_label = "Edge Clean Up"
    
    def execute(self, context):
        try:
            CleanUp()
            return {'FINISHED'}
        
        except:
            print("Well shit")
            return {'CANCELLED'}

#UI and register handling
def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("edgemerge.edge_clean_up", text = "Edge Clean Up")

def register():
    bpy.utils.register_class(CleanUpOperator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(draw_menu)

def unregister():
    bpy.utils.unregister_class(CleanUpOperator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_menu)
    
if __name__ == '__main__':
    register()