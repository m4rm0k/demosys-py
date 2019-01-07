from ctypes import c_int

from demosys import context
from demosys.context.base import BaseWindow
from demosys.context.sdl2.keys import Keys

import moderngl
import sdl2
import sdl2.ext
import sdl2.video


class Window(BaseWindow):
    """
    Window implementation using PySDL2
    """
    keys = Keys

    def __init__(self):
        """
        Initializes sdl2, sets up key and mouse events and
        creates a ``moderngl.Context`` using the context sdl2 createad.

        Using the sdl2 window requires sdl binaries and PySDL2.
        """
        super().__init__()
        self.window_closing = False
        self.tmp_size_x = c_int()
        self.tmp_size_y = c_int()

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise ValueError("Failed to initialize sdl2")

        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, self.gl_version.major)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, self.gl_version.minor)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)

        # TODO: Fullscreen
        # SDL_WINDOW_FULLSCREEN
        self.window = sdl2.SDL_CreateWindow(
            self.title.encode(),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.width,
            self.height,
            sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE,
        )

        if not self.window:
            raise ValueError("Failed to create window:", sdl2.SDL_GetError())

        self.context = sdl2.SDL_GL_CreateContext(self.window)
        self.ctx = moderngl.create_context(require=self.gl_version.code)
        context.WINDOW = self
        self.fbo = self.ctx.screen
        self.set_default_viewport()

    def use(self):
        """
        Bind the window framebuffer making it the current render target
        """
        self.fbo.use()

    def swap_buffers(self):
        self.frames += 1
        sdl2.SDL_GL_SwapWindow(self.window)
        self.process_events()

    def resize(self, width, height):
        """
        Sets the new size and buffer size internally
        """
        self.width = width
        self.height = height

        # Fetch the actual buffer size of the screen. This can double the size on 4k displays
        sdl2.SDL_GL_GetDrawableSize(self.window, self.tmp_size_x, self.tmp_size_y)
        self.buffer_width, self.buffer_height = self.tmp_size_x.value, self.tmp_size_y.value

        self.set_default_viewport()

    def process_events(self):
        for event in sdl2.ext.get_events():
            if event.type in [sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP]:
                self.keyboard_event(event.key.keysym.sym, event.type, None)

            elif event.type == sdl2.SDL_QUIT:
                self.window_closing = True
                break

            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    self.resize(event.window.data1, event.window.data2)

    def should_close(self):
        return self.window_closing

    def close(self):
        self.window_closing = True

    def terminate(self):
        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
