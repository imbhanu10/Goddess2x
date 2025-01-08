from OpenGL.GL import *
import os

def load_shader(path, shader_type):
    """Load and compile shader."""
    with open(path, 'r') as file:
        shader_code = file.read()

    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_code)
    glCompileShader(shader)
    
    # Check for shader compile errors
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error_msg = glGetShaderInfoLog(shader)
        print(f"Error compiling shader {path}: {error_msg.decode('utf-8')}")
    
    return shader
