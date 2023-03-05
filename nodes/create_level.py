# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import unreal

from iogunreal_threading import unreal_game_thread


class CreateLevel(iograft.Node):
    """
    Create a new blank level and save it. Load the newly created level. If
    `template_asset_path` is provided, use the level at the given path
    as the template for the new level.
    """
    level_name = iograft.InputDefinition("name", iobasictypes.String())
    destination_path = iograft.InputDefinition("destination_path",
                                               iobasictypes.String())
    template_asset_path = iograft.InputDefinition("template_asset_path",
                                                  iobasictypes.String(),
                                                  default_value="")

    level_path = iograft.OutputDefinition("path", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("create_level", "unreal")
        node.SetMenuPath("Unreal")
        node.AddInput(cls.level_name)
        node.AddInput(cls.destination_path)
        node.AddInput(cls.template_asset_path)
        node.AddOutput(cls.level_path)
        return node

    @staticmethod
    def Create():
        return CreateLevel()

    @unreal_game_thread
    def Process(self, data):
        level_name = iograft.GetInput(self.level_name, data)
        destination_path = iograft.GetInput(self.destination_path, data)
        destination_path = destination_path.rstrip("/")
        template_asset_path = iograft.GetInput(self.template_asset_path, data)

        # Create the new level.
        level_path = "/".join([destination_path, level_name])
        level_editor = unreal.LevelEditorSubsystem()
        if template_asset_path:
            success = level_editor.new_level_from_template(level_path,
                                                           template_asset_path)
        else:
            success = level_editor.new_level(level_path)

        if not success:
            # TODO: Currently, there is no way to access the UE_LOG output.
            # In this case that means we don't have access to a better error
            # message as to why creating the level failed.
            raise RuntimeError("Failed to create level at path: {}".format(
                                                                level_path))

        iograft.SetOutput(self.level_path, data, level_path)


def LoadPlugin(plugin):
    node = CreateLevel.GetDefinition()
    plugin.RegisterNode(node, CreateLevel.Create)
