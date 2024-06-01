import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Load shader as string from file
def load_shader(shader_file):
    with open(shader_file, 'r') as file:
        return file.read()

v_shader = load_shader('vertex.glsl')
f_shader = load_shader('fragment.glsl')

# Define the vertices of the triangle
vertices = np.array([
    [-0.5, -0.5, 0.0],  # Vertex 1
    [0.5, -0.5, 0.0],   # Vertex 2
    [0.0, 0.5, 0.0]     # Vertex 3
], dtype=np.float32)

# Create shader program
def create_shader_program(vertex_shader, fragment_shader):
    # Create the vertex shader
    vertex_shader_id = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader_id, vertex_shader)
    glCompileShader(vertex_shader_id)

    # Create the fragment shader
    fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader_id, fragment_shader)
    glCompileShader(fragment_shader_id)

    # Create the shader program
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader_id)
    glAttachShader(shader_program, fragment_shader_id)
    glLinkProgram(shader_program)

    # Delete the shaders as they're linked into our program now and no longer necessery
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)

    return shader_program

shader = create_shader_program(v_shader, f_shader)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Create a vertex buffer object (VBO)
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Create a vertex array object (VAO)
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # Unbind VAO
    glBindVertexArray(0)

    # Unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glUseProgram(shader)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        pygame.display.flip()

if __name__ == '__main__':
    main()
