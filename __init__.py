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
from bpy.types import RENDER_PT_color_management

###############
# MINOR FUNCS #
###############


def correct_order(current_vert, selected_verts, corrected_order, closed_loop = True):

    adj_vert_counter = 0
    adj_verts = [edge.other_vert(current_vert) for edge in current_vert.link_edges]

    #Check if the selection is a valid loop and if its open/closed
    for adj_vert in adj_verts:
        if adj_vert in selected_verts:
                adj_vert_counter += 1
        else:
            pass

    if adj_vert_counter == 2:
        pass
    elif adj_vert_counter == 1:
        pass
    else:
        print("Operation failed, please check for any loose vertices")
        raise Exception

    #Check if/which vert of the adjacent ones was also selected and if its position hasn't been corrected, correct it
    for adj_vert in adj_verts:

        if adj_vert in selected_verts and adj_vert not in corrected_order:

                if closed_loop:
                    corrected_order.append(adj_vert)
                    closed_loop = correct_order(adj_vert, selected_verts, corrected_order, closed_loop)
                else:
                    corrected_order.insert(0, adj_vert)
                    correct_order(adj_vert, selected_verts, corrected_order, closed_loop)
        else:
            pass
    
    return False


def get_ratios(vert1, vert2):
    
    lenghts = [abs(vert1.co[i] - vert2.co[i]) for i in range(3)]
    ratios = []
    
    for i in range(-1, 2):
        try:
            ratios.append(lenghts[i] / lenghts[i + 1])
        except ZeroDivisionError:
            ratios.append(0)
    
    return ratios


def correct_coords(last_vert, unnecessary_verts, verts, last_ratios, vert_counter = 0):
    
    try:
        current_vert = verts[verts.index(last_vert) + 1]
        current_ratios = get_ratios(last_vert, current_vert)
        
        print(last_ratios, "last")
        print(current_ratios, "current")
        
        for i in range(3):
            if abs(last_ratios[i] - current_ratios[i]) <= 0.0001:
                ratios_equal = True
            else:
                ratios_equal = False
                break
        
        if ratios_equal:
            
            vert_counter += 1
            
            if vert_counter >= 2:
                unnecessary_verts.append(last_vert)
                correct_coords(current_vert, unnecessary_verts, verts, current_ratios, vert_counter)
            
            else:
                correct_coords(current_vert, unnecessary_verts, verts, current_ratios, vert_counter)
            
        else:
            vert_counter = 1
            correct_coords(current_vert, unnecessary_verts, verts, current_ratios, vert_counter)
                    
    except Exception as ex:
        print(ex)


#############
# MAIN FUNC #
#############

def clean_up():

    current_obj = bpy.context.object

    if current_obj.mode == 'EDIT':
        
        selected_verts = []
        bm = bmesh.from_edit_mesh(current_obj.data)

        #Iterate through all selected_verts and list selected ones
        for vert in bm.verts:
            if vert.select:
                selected_verts.append(vert)
            else:
                pass

        corrected_order = [selected_verts[0]]

        correct_order(selected_verts[0], selected_verts, corrected_order)
        
        unnecessary_verts = []
        
        correct_coords(corrected_order[0], unnecessary_verts, corrected_order, get_ratios(corrected_order[0], corrected_order[1]))
        
        print(unnecessary_verts)
        
        
    else:
        print("Object is not in edit mode.")
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')


#######################
# ADD-ON INSTALLATION #
#######################

class CleanUpOperator(bpy.types.Operator):
    
    bl_idname = "edgemerge.edge_clean_up"
    bl_label = "Edge Clean Up"
    
    def execute(self, context):
        try:
            clean_up()
            return {'FINISHED'}
        
        except Exception as ex:
            print("Well shit")
            print(ex)
            return {'CANCELLED'}

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