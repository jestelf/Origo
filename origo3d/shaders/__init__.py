"""Простейшие шейдеры для тестового рендера."""

VERTEX_SHADER_SOURCE = """
#version 330
uniform mat4 u_mvp;
in vec3 in_position;
in vec3 in_color;
out vec3 v_color;
void main() {
    gl_Position = u_mvp * vec4(in_position, 1.0);
    v_color = in_color;
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330
in vec3 v_color;
out vec4 fragColor;
void main() {
    fragColor = vec4(v_color, 1.0);
}
"""
