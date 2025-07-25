"""Базовые PBR-шейдеры, используемые в предпросмотре материалов."""

PBR_VERTEX_SHADER = """
#version 330
in vec3 in_position;
in vec3 in_normal;
uniform mat4 u_mvp;
out vec3 v_normal;
void main() {
    v_normal = in_normal;
    gl_Position = u_mvp * vec4(in_position, 1.0);
}
"""

PBR_FRAGMENT_SHADER = """
#version 330
in vec3 v_normal;
out vec4 f_color;

uniform vec3 u_albedo;
uniform float u_metallic;
uniform float u_roughness;

void main() {
    vec3 N = normalize(v_normal);
    float ndotl = clamp(dot(N, vec3(0.0, 0.0, 1.0)), 0.0, 1.0);
    vec3 diffuse = u_albedo * ndotl;
    vec3 spec = mix(vec3(0.04), u_albedo, u_metallic);
    float rough = max(u_roughness, 0.05);
    vec3 color = diffuse + spec * pow(ndotl, 1.0 / rough);
    f_color = vec4(color, 1.0);
}
"""
