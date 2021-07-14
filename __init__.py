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

import bpy
import bmesh
import numpy as np

def CleanUp():
    
    def correct_indices(start_bmvert, corrected_indices, bmverts):
        
        #Correct the indices such that the vert_ids correspond to how the verts are arranged on the model
        adjacent_verts = [edge.other_vert(start_bmvert) for edge in start_bmvert.link_edges]
        counter = 0
        
        #Check for potential loose ends
        for adjacent_vert in adjacent_verts:
            if adjacent_vert in bmverts:
                    counter += 1
            else:
                pass
        
        if counter <= 2:
            pass
        else:
            raise Exception("Operation failed, please check for any loose vertices")
            
        #Check if/which vert of the adjacent ones was also selected and get its index
        for adjacent_vert in adjacent_verts:
            if adjacent_vert in bmverts and adjacent_vert not in corrected_indices:
                corrected_indices.append(bmverts.index(adjacent_vert))
                correct_indices(adjacent_vert, corrected_indices, bmverts)
            else:
                pass
    
    #Set up vars
    verts = {}
    i = 0
    obj = bpy.context.object
    
    #Check for edit mode, if the mode isn't edit mode pass
    if obj.mode == 'EDIT':
        
        #Get selected verts and asign them into a dictionary such that - vert_id (int) : [bmesh vert data (BMVert), xyz coords (np array of single floats)]
        bm = bmesh.from_edit_mesh(obj.data)
        
        for vert in bm.verts:
            if vert.select:
                verts[i] = [vert, np.array([vert.co.x, vert.co.y, vert.co.z], dtype = np.single)]
                i += 1
            else:
                pass
        
        bmverts = [verts[x][0] for x in verts]
        corrected_indices = [0]
        
        correct_indices(bmverts[0], corrected_indices, bmverts)
        print(corrected_indices)
        
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