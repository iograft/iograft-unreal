# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import unreal

from iogunreal_threading import unreal_game_thread


class ImportFBXStaticMesh(iograft.Node):
    """
    Import an FBX mesh into Unreal as a static mesh. Optionally can import
    materials and textures as well. This import does not save the newly
    imported assets, and should be followed by a `save_dirty_packages` node
    or similar.

    TODO: Expose all available FBX import options.
    """
    filename = iograft.InputDefinition("filename", iobasictypes.Path())

    destination_path = iograft.InputDefinition("destination_path",
                                               iobasictypes.String())
    destination_name = iograft.InputDefinition("destination_name",
                                               iobasictypes.String(),
                                               default_value="")
    import_materials = iograft.InputDefinition("import_materials",
                                               iobasictypes.Bool(),
                                               default_value=False)
    import_textures = iograft.InputDefinition("import_textures",
                                              iobasictypes.Bool(),
                                              default_value=False)

    imported_paths = iograft.OutputDefinition("imported_paths",
                                              iobasictypes.StringList())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("import_fbx_static_mesh")
        node.SetNamespace("unreal")
        node.SetMenuPath("Unreal")
        node.AddInput(cls.filename)
        node.AddInput(cls.destination_path)
        node.AddInput(cls.destination_name)
        node.AddInput(cls.import_materials)
        node.AddInput(cls.import_textures)
        node.AddOutput(cls.imported_paths)
        return node

    @staticmethod
    def Create():
        return ImportFBXStaticMesh()

    @unreal_game_thread
    def Process(self, data):
        filename = iograft.GetInput(self.filename, data)
        destination_path = iograft.GetInput(self.destination_path, data)
        destination_name = iograft.GetInput(self.destination_name, data)
        import_materials = iograft.GetInput(self.import_materials, data)
        import_textures = iograft.GetInput(self.import_textures, data)

        # Build the AssetImportTask
        asset_import_task = unreal.AssetImportTask()
        asset_import_task.set_editor_property("automated", True)
        asset_import_task.set_editor_property("async_", False)
        asset_import_task.set_editor_property("save", False)
        asset_import_task.set_editor_property("replace_existing", True)
        asset_import_task.set_editor_property("filename", filename)
        asset_import_task.set_editor_property("destination_path",
                                              destination_path)
        if destination_name:
            asset_import_task.set_editor_property("destination_name",
                                                  destination_name)

        # Setup the import options.
        fbx_options = _build_fbx_import_options(
                                            import_materials=import_materials,
                                            import_textures=import_textures)
        asset_import_task.set_editor_property("options", fbx_options)

        # Execute the asset import tasks.
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks([asset_import_task])

        # Gather the imported objects to provide as output from the node.
        imported_paths = [str(path) for path in
                                    asset_import_task.imported_object_paths]
        iograft.SetOutput(self.imported_paths, data, imported_paths)


def _build_fbx_static_mesh_import_data():
    """
    Fill in the FbxStaticMeshImportData object providing settings for the
    static mesh import.
    """
    static_mesh_options = unreal.FbxStaticMeshImportData()

    # Note: The 'lo_ds' with an underscore is not a typo.
    static_mesh_options.set_editor_property("import_mesh_lo_ds", True)
    return static_mesh_options


def _build_fbx_texture_import_data():
    """
    Fill in the FbxTextureImportData object providing settings for the
    texture import.
    """
    texture_options = unreal.FbxTextureImportData()
    return texture_options


def _build_fbx_import_options(import_materials=False, import_textures=False):
    """
    Build an FbxImportUI object with the options for the import task.
    """
    fbx_options = unreal.FbxImportUI()
    fbx_options.set_editor_property("mesh_type_to_import",
                                    unreal.FBXImportType.FBXIT_STATIC_MESH)
    fbx_options.reset_to_default()

    static_mesh_import_data = _build_fbx_static_mesh_import_data()
    fbx_options.set_editor_property("static_mesh_import_data",
                                    static_mesh_import_data)
    fbx_options.set_editor_property("import_mesh", True)
    fbx_options.set_editor_property("import_animations", False)
    fbx_options.set_editor_property("import_as_skeletal", False)

    fbx_options.set_editor_property("import_materials", import_materials)
    fbx_options.set_editor_property("import_textures", import_textures)
    if import_materials or import_textures:
        texture_import_data = _build_fbx_texture_import_data()
        fbx_options.set_editor_property("texture_import_data",
                                        texture_import_data)

    return fbx_options


def LoadPlugin(plugin):
    node = ImportFBXStaticMesh.GetDefinition()
    plugin.RegisterNode(node, ImportFBXStaticMesh.Create)
