# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import unreal


class SaveDirtyPackages(iograft.Node):
    """
    Save all dirty packages in the Unreal project. Show the save dialog
    if `show_dialog` is True.
    """
    save_maps = iograft.InputDefinition("save_map_packages",
                                        iobasictypes.Bool(),
                                        default_value=False)
    save_content = iograft.InputDefinition("save_content_packages",
                                           iobasictypes.Bool(),
                                           default_value=True)
    show_dialog = iograft.InputDefinition("show_dialog",
                                          iobasictypes.Bool(),
                                          default_value=False)

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("save_dirty_packages")
        node.SetNamespace("unreal")
        node.SetMenuPath("Unreal")
        node.AddInput(cls.save_maps)
        node.AddInput(cls.save_content)
        node.AddInput(cls.show_dialog)
        return node

    @staticmethod
    def Create():
        return SaveDirtyPackages()

    def Process(self, data):
        save_maps = iograft.GetInput(self.save_maps, data)
        save_content = iograft.GetInput(self.save_content, data)
        show_dialog = iograft.GetInput(self.show_dialog, data)

        if show_dialog:
            success = \
                unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(
                                                            save_maps, save_content)
        else:
            success = unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
                                                        save_maps, save_content)

        if not success:
            raise RuntimeError("Failed to save packages.")


def LoadPlugin(plugin):
    node = SaveDirtyPackages.GetDefinition()
    plugin.RegisterNode(node, SaveDirtyPackages.Create)
