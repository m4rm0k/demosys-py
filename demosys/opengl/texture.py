import os
from OpenGL import GL
from PIL import Image


class Texture:
    """Represents a texture"""
    def __init__(self):
        """Initialize texture without allocating data using default values"""
        self.texture = GL.glGenTextures(1)
        # dimensions
        self.width = 0
        self.height = 0
        self.depth = 0
        # format / type
        self.target = GL.GL_TEXTURE_2D
        self.lod = 0
        self.internal_format = GL.GL_RGBA8
        self.format = GL.GL_RGBA
        self.type = GL.GL_UNSIGNED_BYTE
        # filters
        self.min_filter = GL.GL_LINEAR
        self.mag_filter = GL.GL_LINEAR
        # For pre-loading files
        self.name = None
        self.path = None

    @property
    def size(self):
        """
        Get the dimensions of the texture

        :return: (w, h) tuple
        """
        return self.width, self.height

    @classmethod
    def from_image(cls, path, image=None):
        """
        Creates and image from a image file using Pillow/PIL

        :param path: The path to the file
        :param image: The PIL/Pillow image object
        :return: Texture object
        """
        t = Texture()
        t.path = path
        t.name = os.path.basename(path)
        if image:
            t.set_image(image)
        return t

    @classmethod
    def create_2d(cls, width, height, internal_format=GL.GL_RGBA8, format=GL.GL_RGBA, type=GL.GL_UNSIGNED_BYTE):
        """
        Creates a 2d texture

        :param width: Width of the texture
        :param height: height of the texture
        :param internal_format: Internal format
        :param format: Format
        :param type: Type
        :return: Texture object
        """
        t = Texture()
        t._build(width, height, 0, target=GL.GL_TEXTURE_2D,
                 internal_format=internal_format, format=format, type=type, data=None)
        return t

    def bind(self):
        """
        Binds the texture to the currently active texture unit
        """
        GL.glBindTexture(self.target, self.texture)

    def _build(self, width, height, depth, target=GL.GL_TEXTURE_2D, lod=0,
               internal_format=GL.GL_RGBA8, format=GL.GL_RGBA, type=GL.GL_UNSIGNED_BYTE, data=None):
        """Internal method for building the texture"""
        # keep track of all states
        self.width = width
        self.height = height
        self.depth = depth
        self.target = target
        self. lod = lod
        self.internal_format = internal_format
        self.format = format
        self.type = type
        # set states
        self.bind()
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)

        if self.target == GL.GL_TEXTURE_2D:
            GL.glTexImage2D(self.target, self.lod, self.internal_format,
                            self.width, self.height, 0,
                            self.format, self.type, data)
        elif self.target == GL.GL_TEXTURE_1D:
            if self.width > self.height:
                GL.glTexImage1D(self.target, self.lod, self.internal_format,
                                self.width, 0, self.format, self.type, data)
            else:
                GL.glTexImage1D(self.target, self.lod, self.internal_format,
                                self.height, 0, self.format, self.type, data)

    def set_image(self, image):
        """
        Set pixel data using a image file with PIL/Pillow.

        :param image: The PIL/Pillow image object
        """
        """Set image data using a PIL/Pillow image"""
        image_flipped = image.transpose(Image.FLIP_TOP_BOTTOM)
        data = image_flipped.convert("RGBA").tobytes()
        self.width, self.height = image.size
        if self.width == 1 or self.height == 1:
            self.target = GL.GL_TEXTURE_1D
        else:
            self.target = GL.GL_TEXTURE_2D
        self._build(self.width, self.height, 0, data=data, target=self.target)

    def set_texture_repeat(self, mode):
        """
        Sets the texture repeat mode

        :param mode: Repeat mode (gl enum)
        """
        self.bind()
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_S, mode)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_T, mode)

    def set_interpolation(self, mode):
        """
        Sets the texture interpolation mode

        :param mode: Interpolation mode (gl enum)
        """
        self.bind()
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MIN_FILTER, mode)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MAG_FILTER, mode)
