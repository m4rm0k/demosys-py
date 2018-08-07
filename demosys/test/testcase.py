import os
from unittest import TestCase

os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'  # noqa

import demosys
from demosys import context, resources
from demosys.opengl import ShaderProgram

demosys.setup()
demosys.create_window().use()


class DemosysTestCase(TestCase):

    window = context.window()
    ctx = context.ctx()

    def create_program(self, source=None, path=None):
        """
        Create a shader from source or file
        """
        if source:
            program = ShaderProgram(name="test", path=path)
            program.set_source(source)
            program.prepare()

        if path:
            program = resources.programs.load(path)

        return program

    def get_texture(self, path):
        return resources.textures.load(path, create=True)

    def get_texture_array(self, path, layers=0):
        return resources.textures.load(path, create=True, loader='array', layers=layers)

    def get_track(self, name):
        return resources.tracks.get(name)
