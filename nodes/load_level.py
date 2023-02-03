# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import unreal


class LoadLevel(iograft.Node):
    """
    Load the level at the given path.
    """
    level_path = iograft.InputDefinition("path", iobasictypes.String())
    level_path_out = iograft.OutputDefinition("path", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("load_level", "unreal")
        node.SetMenuPath("Unreal")
        node.AddInput(cls.level_path)
        node.AddOutput(cls.level_path_out)
        return node

    @staticmethod
    def Create():
        return LoadLevel()

    def Process(self, data):
        level_path = iograft.GetInput(self.level_path, data)

        # Attempt to load the level. First check if the level exists (so
        # that a better error message can be provided).
        if not unreal.EditorAssetSubsystem().does_asset_exist(level_path):
            raise RuntimeError("No asset exists at path: {}".format(level_path))

        level_editor = unreal.LevelEditorSubsystem()
        success = level_editor.load_level(level_path)
        if not success:
            # TODO: Currently, there is no way to access the UE_LOG output.
            # In this case that means we don't have access to a better error
            # message as to why the load level failed.
            raise RuntimeError("Failed to load level at path: {}".format(
                                                                    level_path))

        # Output the path of the loaded level as a "passthrough".
        iograft.SetOutput(self.level_path_out, data, level_path)


def LoadPlugin(plugin):
    node = LoadLevel.GetDefinition()
    plugin.RegisterNode(node, LoadLevel.Create)
