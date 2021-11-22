# Copyright 2021 Fabrica Software, LLC

import iograft
import iobasictypes


class ImportAsset(iograft.Node):
    """ Import an asset into Unreal from the given file path. """
    asset_path = iograft.InputDefinition("asset_filepath", iobasictypes.String())
    project_path = iograft.InputDefinition("project_path",
                                           iobasictypes.String())

    imported_objects = iograft.OutputDefinition("imported_objects",
                                                iobasictypes.StringList())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("import_asset")
        node.AddInput(cls.asset_path)
        node.AddInput(cls.project_path)
        node.AddOutput(cls.imported_objects)
        return node

    @staticmethod
    def Create():
        return ImportAsset()

    def Process(self, data):
        import unreal

        asset_path = iograft.GetInput(self.asset_path, data)
        project_path = iograft.GetInput(self.project_path, data)

        # Run the Asset import.
        AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
        AssetImportTask = unreal.AssetImportTask()
        AssetImportTask.set_editor_property("filename", asset_path)
        AssetImportTask.set_editor_property("destination_path", project_path)
        AssetImportTask.set_editor_property("save", True)
        AssetImportTask.set_editor_property("automated", True)
        AssetTools.import_asset_tasks([AssetImportTask])

        # Output the import object strings.
        imported_paths = [str(path) for path in AssetImportTask.imported_object_paths]
        iograft.SetOutput(self.imported_objects, data, imported_paths)


def LoadPlugin(plugin):
    node = ImportAsset.GetDefinition()
    plugin.RegisterNode(node, ImportAsset.Create)
