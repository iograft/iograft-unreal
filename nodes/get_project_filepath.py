# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes


class GetProjectFilePath(iograft.Node):
    """ Return the path to the current Unreal project file. """
    project_path = iograft.OutputDefinition("project_path",
                                            iobasictypes.Path())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("get_project_path")
        node.AddOutput(cls.project_path)
        return node

    @staticmethod
    def Create():
        return GetProjectFilePath()

    def Process(self, data):
        import unreal

        project_path = unreal.Paths.get_project_file_path()
        iograft.SetOutput(self.project_path, data, project_path)


def LoadPlugin(plugin):
    node = GetProjectFilePath.GetDefinition()
    plugin.RegisterNode(node, GetProjectFilePath.Create)
