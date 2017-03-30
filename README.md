# demosys-py

A python 3.6 implementation of a C++ project used to create and prototype
demos (see [demoscene](https://en.wikipedia.org/wiki/Demoscene)) in OpenGL. The design of 
this version is heavily inspired by the [Django](https://www.djangoproject.com/) project.

We only support OpenGL 4.1+ core profiles (no backwards compatibility).

**Also note that Python 3.6 will and is the minimum requirement for reasons
we won't dig deeper into right now**

This was originally made for for non-interactive real time graphics combined
with music ("real time music videos"). It's made for people who enjoy
playing around with modern OpenGL without having to spend lots of time
creating all the tooling to get things up and running and at the same time
avoid all the old cruft in OpenGL.

The package is not yet on PyPI, but will be on the near future.

## Contributing

Any contribution to the project is welcome. Never hesitate to ask questions or submit
pull requests (completed or work in progress). The worst thing that an happen is that
we or you might learn something. This is supposed to be a fun project

## Running the damn thing

Currently you just clone the repo and run `manage.py`. This runs the `testproject` package
in the repository. You can of course also make your own.

## Quick Introduction

Anything we draw to the screen must be implemented as an Effect.
If that effect is one or multiple things is entirely up to you.
An effect is an individual package/directory containing an `effect.py`
module. This package can also contain a `shaders` and `textures` directory
that demosys will automatically find and load resources from.
See the `testproject` directory for reference.

Explore the small `testproject` folder, and you'll get the point.

What we currently support:
- All geometry must be defined using VAOs. There's a very convenient VAO class
  for this already making it quick and easy to create them. Look at the
  `demosys.opengl.geometry` module for examples.
- We support vertex, fragment and geometry shaders for now. A program must currently
  be written in one single `.glsl` file separating the shaders with preprocessors.
  See existing shaders in `testproject`.
- The Shader class will inspect the linked shader and cache all attributes and uniforms
  in local dictionaries. This means all `uniform*`-setters use the name of the uniform
  instead of the location. Location is resolved internally in the object/class.
- The VAOs `bind(..)` requires you to pass in a shader. This is because the VAO
  will automatically adapt to the attributes in your shader. During the VAO creation
  you need to make the name mapping to the attribute name. If you have a VAO with positions,
  normals, uvs and tangents and pass in a shader that only use position; the VAO
  class will on-the-fly generate a version internally with only positions.
- We only support 2D textures at the moment loaded with PIL/Pillow, but this is trivial
  to extend.
- Resource loading is supported in the `Effect` class itself. In `__init__()' you can
  fetch resources using for example `self.get_shader` or self.get_texture'. This will
  return a lazy object that will be populated after the loading stage is done.
- We don't have any scene/mesh loaders. You can hack something in yourself for now
  or just stick to or extend the `geometry` module.
- We try to do as much validation as possible and give useful feedback when
  something goes wrong.
- The `time` value passed to the effects `draw` method is the current duration
  in the playing music. If no music is loaded, a dummy timer is used.

See also the TODO.md file.

## Settings

The `settings.py` file must be present in your project and contains (you guessed right!)
settings for the framework. This is pretty much identical to Django.

### OPENGL

Using these values you are sure it will run on all platforms. OS X only support
forward compatible core contexts. This will bump you to the latest version
you drivers support.

```python
OPENGL = {
    "version": (4, 1),
    "profile": "core",
    "forward_compat": True,
}
```

### WINDOW

Window properties. If you are using Retina display, be aware that these values
refer to the virual size. The actual buffer size will be 2 x.

```python
WINDOW = {
    "size": (1280, 768),
    "resizable": False,
    "fullscreen": False,
    "title": "demosys-py",
}
```

### MUSIC

If `MUSIC` is defined, demosys will attempt to play. (We have only tried mp3 files!)

```python
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')
```

### EFFECTS

Effect packages demosys will initialize and use (Same as apps in Django).
Currently all effects registered will run simultaneously as we currently
don't have a time line concept for scheduling when they should run. (SOON!)

```python
EFFECTS = (
    'testproject.cube',
)
```

### SHADER_*

`DIRS` contains absolute paths the `FileSystemFinder` will look for shader while
`EffectDirectoriesFinder` will look for shaders in all registered effects in 
the order they were added.

```python
SHADER_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/shaders'),
)

SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder',
)
```

### TEXTURE_*

Same principle as shaders.

```python
# Hardcoded paths to shader dirs
TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resource/textures'),
)

# Finder classes
TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)
```

## Known Issues

The sound player an be a bit wonky at times on startup refusing to play on
some platforms. We have tried a few libraries and ended up using pygame's
mixer module. 

Audio Requirements:
- As the current position in the music is what all draw timers are connected to,
we need a library that can deliver this.
- Efficient and accurate seeking + pause support
- Some way to extract simple data from the music for visualisation

## Libraries

- [http://pyopengl.sourceforge.net](http://pyopengl.sourceforge.net/)
- [pyGLFW](https://github.com/FlorianRhiem/pyGLFW) for window and context creation + input
- [PIL/Pillow](https://github.com/python-pillow/Pillow) for texture loading
- [https://www.pygame.org](https://www.pygame.org) using the mixer module for music
- [https://github.com/adamlwgriffiths/Pyrr](https://github.com/adamlwgriffiths/Pyrr) for math (uses numpy)

## What inspired us to make this project?

- We are old farts from the demoscene
- We love Python
- We work a lot with Django and love it

Why not combine ideas from our own demosys written in C++ and Django making
a Python 3 version?

Also thanks to [Attila Toth](https://www.youtube.com/channel/UC4L3JyeL7TXQM1f3yD6iVQQ)
for an excellent video tutorial on Python and OpenGL. We do know OpenGL,
but had no clue where to start in the Python world.