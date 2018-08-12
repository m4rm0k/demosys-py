import moderngl
from demosys import context


class TextureHelper:
    _quad = None

    _texture2d_shader = None
    _texture2d_sampler = None

    _depth_shader = None
    _depth_sampler = None

    def __init__(self):
        pass

    @property
    def initialized(self):
        return self._quad is not None

    @property
    def ctx(self):
        return context.ctx()

    def draw(self, texture, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw texture using a fullscreen quad.
        By default this will conver the entire screen.

        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        if not self.initialized:
            self.init()

        self._texture2d_shader.uniform("offset", (pos[0] - 1.0, pos[1] - 1.0))
        self._texture2d_shader.uniform("scale", (scale[0], scale[1]))
        texture.use(location=0)
        self._texture2d_sampler.use(location=0)
        self._texture2d_shader.uniform("texture0", 0)
        self._quad.draw(self._texture2d_shader)
        self._texture2d_sampler.clear(location=0)

    def draw_depth(self, texture, near, far, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw depth buffer linearized.
        By default this will draw the texture as a full screen quad.
        A sampler will be used to ensure the right conditions to draw the depth buffer.

        :param near: Near plane in projection
        :param far: Far plane in projection
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        if not self.initialized:
            self.init()

        self._depth_shader.uniform("offset", (pos[0] - 1.0, pos[1] - 1.0))
        self._depth_shader.uniform("scale", (scale[0], scale[1]))
        self._depth_shader.uniform("near", near)
        self._depth_shader.uniform("far", far)
        self._depth_sampler.use(location=0)
        texture.use(location=0)
        self._depth_shader.uniform("texture0", 0)
        self._quad.draw(self._depth_shader)
        self._depth_sampler.clear(location=0)

    def _init_texture2d_draw(self):
        """Initialize geometry and shader for drawing FBO layers"""
        from demosys import context, geometry  # noqa

        if not TextureHelper._quad:
            TextureHelper._quad = geometry.quad_fs()
        # Shader for drawing color layers
        TextureHelper._texture2d_shader = context.ctx().program(
            vertex_shader="""
                #version 330

                in vec3 in_position;
                in vec2 in_uv;
                out vec2 uv;
                uniform vec2 offset;
                uniform vec2 scale;

                void main() {
                    uv = in_uv;
                    gl_Position = vec4((in_position.xy + vec2(1.0, 1.0)) * scale + offset, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330

                out vec4 out_color;
                in vec2 uv;
                uniform sampler2D texture0;

                void main() {
                    out_color = texture(texture0, uv);
                }
            """
        )

        TextureHelper._texture2d_sampler = self.ctx.sampler(
            filter=(moderngl.LINEAR, moderngl.LINEAR),
        )

    def _init_depth_texture_draw(self):
        """Initialize geometry and shader for drawing FBO layers"""
        from demosys import context, geometry  # noqa

        if not TextureHelper._quad:
            TextureHelper._quad = geometry.quad_fs()
        # Shader for drawing depth layers
        TextureHelper._depth_shader = context.ctx().program(
            vertex_shader="""
                #version 330

                in vec3 in_position;
                in vec2 in_uv;
                out vec2 uv;
                uniform vec2 offset;
                uniform vec2 scale;

                void main() {
                    uv = in_uv;
                    gl_Position = vec4((in_position.xy + vec2(1.0, 1.0)) * scale + offset, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330

                out vec4 out_color;
                in vec2 uv;
                uniform sampler2D texture0;
                uniform float near;
                uniform float far;

                void main() {
                    float z = texture(texture0, uv).r;
                    float d = (2.0 * near) / (far + near - z * (far - near));
                    out_color = vec4(d);
                }
            """
        )

        TextureHelper._depth_sampler = self.ctx.sampler(
            filter=(moderngl.LINEAR, moderngl.LINEAR),
            compare_func='',
        )


texture = TextureHelper()
