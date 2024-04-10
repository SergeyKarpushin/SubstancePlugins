import os
from PySide2 import QtWidgets
from substance_painter import project, resource, ui

plugin_widgets = []
"""Keep track of added ui elements for cleanup"""

my_settings = project.Settings(
                default_texture_resolution=2048,
                normal_map_format=project.NormalMapFormat.OpenGL,
                #project_workflow=project.ProjectWorkflow.UVTile
            )

open_file_path = '.'

def start_plugin():
    # Create a simple widget
    button = QtWidgets.QPushButton("Create new project")
    button.clicked.connect(select_mesh)
    button.setWindowTitle("Character Creator Bridge")

    # Add this widget as a dock to the interfdace
    ui.add_dock_widget(button)
    
    # Store added widget for proper cleanup when stopping the plugin
    plugin_widgets.append(button)

    print("Plugin started successfully.")

def select_mesh():
    if project.is_open():
        project.close()
    
    global open_file_path
    files = QtWidgets.QFileDialog.getOpenFileName(None, 'Open a Mesh to Import', open_file_path, '*.obj *.fbx')
    open_file_path = os.path.dirname(files[0])
    create_new_project(files[0])

def create_new_project(mesh_file_path):
    # create new project using selected mesh file
    project.create(mesh_file_path, settings=my_settings)

    # import textures into project shelf
    textures_folder = next(os.walk(os.path.dirname(mesh_file_path)))[1][0]
    mesh_textures_folder = os.path.join(os.path.dirname(mesh_file_path), textures_folder)
    files_list = [f for f in os.listdir(mesh_textures_folder) if os.path.isfile(os.path.join(mesh_textures_folder, f))]
    for file in files_list:
        print("Importing: " + file)
        resource.import_project_resource(os.path.join(mesh_textures_folder, file), resource.Usage.TEXTURE)

    resource.Shelves.refresh_all()




def close_plugin():
    # We need to remove all added widgets from the UI.
    for widget in plugin_widgets:
        ui.delete_ui_element(widget)
    plugin_widgets.clear()
    print("Plugin closed successfully.")

if __name__ == "__main__":
    start_plugin()
