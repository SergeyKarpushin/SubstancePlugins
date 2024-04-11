import os
from PySide2 import QtWidgets
import substance_painter

plugin_widgets = []
"""Keep track of added ui elements for cleanup"""

my_settings = substance_painter.project.Settings(
                default_texture_resolution=2048,
                normal_map_format=substance_painter.project.NormalMapFormat.OpenGL,
                #project_workflow=substance_painter.project.ProjectWorkflow.UVTile
            )

open_file_path = '.'

def start_plugin():
    # Create a simple widget
    button = QtWidgets.QPushButton("Create new project")
    button.clicked.connect(select_mesh)
    button.setWindowTitle("Character Creator Bridge")

    # Add this widget as a dock to the interfdace
    substance_painter.ui.add_dock_widget(button)
    
    # Store added widget for proper cleanup when stopping the plugin
    plugin_widgets.append(button)

    # connections = {
    #     substance_painter.event.ProjectCreated: on_project_created,
    # }
    # for event, callback in connections.items():
    #     substance_painter.event.DISPATCHER.connect(event, callback)

    print("Plugin started successfully.")

def select_mesh():
    if substance_painter.project.is_open():
        substance_painter.project.close()
    
    global open_file_path
    files = QtWidgets.QFileDialog.getOpenFileName(None, 'Open a Mesh to Import', open_file_path, '*.obj *.fbx')
    open_file_path = os.path.dirname(files[0])
    create_new_project(files[0])

def create_new_project(mesh_file_path):
    textures_folder = next(os.walk(os.path.dirname(mesh_file_path)))[1][0]
    mesh_textures_folder = os.path.join(os.path.dirname(mesh_file_path), textures_folder)
    maps_list = [os.path.join(mesh_textures_folder, f) for f in os.listdir(mesh_textures_folder) if os.path.isfile(os.path.join(mesh_textures_folder, f))]

    # create new project using selected mesh file
    substance_painter.project.create(mesh_file_path, mesh_map_file_paths=maps_list, settings=my_settings)
    print("Project created successfully.")

    substance_painter.project.execute_when_not_busy(process_texturesets)

    
def on_project_created(event):
    substance_painter.project.execute_when_not_busy(process_texturesets)

def process_texturesets():
    for resourse in substance_painter.resource.list_layer_stack_resources():
        print(resourse)

    texture_set = substance_painter.textureset.TextureSet.from_name("Std_Skin_Body")

    for stack in texture_set.all_stacks():
        print(stack)
        for k,v in stack.all_channels().items():
            print("{0}: {1}".format(k, str(v.format())))


def close_plugin():
    # We need to remove all added widgets from the UI.
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()
    print("Plugin closed successfully.")

if __name__ == "__main__":
    start_plugin()
