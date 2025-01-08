import glfw
from OpenGL.GL import *
import numpy as np
from shader_loader import load_shader

def init_openGL():
    # Initialize the glfw library
    if not glfw.init():
        raise Exception("GLFW initialization failed")

    # Create a windowed mode window and OpenGL context
    window = glfw.create_window(800, 600, "Upscale Shader", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window creation failed")

    glfw.make_context_current(window)
    return window

def create_shader_program(vertex_shader_path, fragment_shader_path):
    # Load vertex and fragment shaders
    vertex_shader = load_shader(vertex_shader_path, gl.GL_VERTEX_SHADER)
    fragment_shader = load_shader(fragment_shader_path, gl.GL_FRAGMENT_SHADER)

    # Create and compile shader program
    shader_program = gl.glCreateProgram()
    gl.glAttachShader(shader_program, vertex_shader)
    gl.glAttachShader(shader_program, fragment_shader)
    gl.glLinkProgram(shader_program)

    # Check for shader linking errors
    if not gl.glGetProgramiv(shader_program, gl.GL_LINK_STATUS):
        info_log = gl.glGetProgramInfoLog(shader_program)
        print(f"Error linking shader program: {info_log}")
    
    return shader_program

def setup_vertices():
    vertices = np.array([
        # Positions       # Texture Coordinates
        -1.0, -1.0, 0.0,  0.0, 0.0,
         1.0, -1.0, 0.0,  1.0, 0.0,
         1.0,  1.0, 0.0,  1.0, 1.0,
         1.0,  1.0, 0.0,  1.0, 1.0,
        -1.0,  1.0, 0.0,  0.0, 1.0,
        -1.0, -1.0, 0.0,  0.0, 0.0
    ], dtype=np.float32)
    
    # Create buffer and vertex array objects
    VBO = gl.glGenBuffers(1)
    VAO = gl.glGenVertexArrays(1)
    
    gl.glBindVertexArray(VAO)
    
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
    
    # Position attribute
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    
    # Texture coordinates attribute
    gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    gl.glEnableVertexAttribArray(1)
    
    return VAO

def main():
    # Initialize OpenGL
    window = init_openGL()

    # Load shaders
    shader_program = create_shader_program("shaders/conv2d_tf.glsl", "shaders/conv2d_tf1.glsl")

    # Setup vertex data
    VAO = setup_vertices()

    # Main rendering loop
    while not glfw.window_should_close(window):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        gl.glUseProgram(shader_program)
        
        # Render the object
        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
        
        # Swap buffers
        glfw.swap_buffers(window)
        
        # Poll events
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
