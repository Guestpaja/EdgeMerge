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
    
    #Lenghts of each edge in a right angle triangle for the given edge (suppossing it's under an angle)
    lenghts = [abs(vert1.co[i] - vert2.co[i]) for i in range(3)]
    ratios = []
    
    #Calculate tangents and cotangents
    for i in range(-1, 2):
        try:
            ratios.append(lenghts[i] / lenghts[i + 1])
        except ZeroDivisionError:
            ratios.append(0)
    
    ratio_types = [type(i) for i in ratios]

    return ratios, ratio_types


def get_unnecessary_verts(last_vert_id, unnecessary_verts, verts, last_ratios, last_r_types, vert_counter = 0):
    
    try:
        last_vert = verts[last_vert_id]
        current_vert = verts[last_vert_id + 1]
        current_ratios, current_r_types = get_ratios(last_vert, current_vert)
        ratios_equal = True
        
        #Check if ratios are equal (within given tolerance)
        for i in range(3):
            if abs(last_ratios[i] - current_ratios[i]) <= 0.0007:
                pass
            else:
                ratios_equal = False
                break
        
        #If types and ratios are equal, then the edge is under the same angle(s) and the last vertex can be removed
        if ratios_equal and current_r_types == last_r_types:
            
            vert_counter += 1
            
            if vert_counter >= 2:
                unnecessary_verts.append(last_vert)
                get_unnecessary_verts(last_vert_id + 1, unnecessary_verts, verts, current_ratios, current_r_types, vert_counter)
            
            else:
                get_unnecessary_verts(last_vert_id + 1, unnecessary_verts, verts, current_ratios, current_r_types, vert_counter)
            
        else:
            vert_counter = 1
            get_unnecessary_verts(last_vert_id + 1, unnecessary_verts, verts, current_ratios, current_r_types, vert_counter)
                    
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
        
        #Check for open/closed loop
        temp_adj_verts = [edge.other_vert(corrected_order[0]) for edge in corrected_order[0].link_edges]
        
        if corrected_order[-1] in temp_adj_verts:
            start_vert = -2
        else:
            start_vert = 0

        unnecessary_verts = []
        temp_ratios, temp_r_types = get_ratios(corrected_order[start_vert], corrected_order[start_vert + 1])

        get_unnecessary_verts(start_vert, unnecessary_verts, corrected_order, temp_ratios, temp_r_types)
        
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