# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    'name' : 'Export Youtube chapters',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (3, 3, 0),
    'location' : 'Properties > Output > Youtube Chapters',
    'description' : 'Exports Blender markers as Youtube chapters in a .txt file.',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Import-Export'
    }


import bpy
from datetime import timedelta
import os
import subprocess

def exportChapters():

    def framenum(mrk):
        return mrk.frame 

    markers = bpy.context.scene.timeline_markers
    sortedMarkers = sorted(markers, key=framenum)

    FPS = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base

    chapterfile = os.path.join(os.path.dirname(bpy.data.filepath), '.'.join((os.path.basename(bpy.data.filepath).split('.')[:-1])) + '_chapters.txt')

    
    with open(chapterfile, 'w') as f:
        for i in sortedMarkers:
            tc = timedelta(seconds=(int(i.frame / FPS)))
            tc = str(tc)
            print(FPS)
            f.write(tc + ' - ' + i.name)
            f.write('\n')
            
    #open the folder on LINUX
    subprocess.Popen(['xdg-open', bpy.path.abspath('//')])
    #open the folder on OSX
    #subprocess.Popen(["open", bpy.path.abspath('//')])
    
    
def check():
    r = False
    if bpy.data.is_saved:
        if len(bpy.context.scene.timeline_markers) > 0:
            return True
    else:
        return False
    

# operator class
class SCRIPT_OT_yt_chapters(bpy.types.Operator):
    # operator attributes
    """Export markers as Youtube chapters in a .txt file."""
    bl_label = 'Markers to Youtube chapters'
    bl_idname = 'script.yt_chapters'

    # poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return check()

    # execute
    def execute(self, context):
        exportChapters()
        return {'FINISHED'}


# panel class
class VIEW_3D_PT_yt_chapters(bpy.types.Panel):
    # panel attributes
    """Export markers as Youtube chapters in a .txt file."""
    bl_label = 'Youtube Chapters'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_category = 'Youtube Chapters'

    # draw loop
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator('script.yt_chapters', text='Export Youtube chapters')


# registration
classes = (
    VIEW_3D_PT_yt_chapters,
    SCRIPT_OT_yt_chapters
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


# enable to test the addon by running this script
if __name__ == '__main__':
    register()
