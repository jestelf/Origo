import moderngl
from origo3d.resources.shader_manager import ShaderManager


def test_shader_caching(tmp_path):
    try:
        ctx = moderngl.create_standalone_context(backend="egl")
    except Exception:
        ctx = moderngl.create_standalone_context()
    vert = tmp_path / "test.vert"
    frag = tmp_path / "test.frag"
    vert.write_text("#version 330\nvoid main(){}")
    frag.write_text("#version 330\nvoid main(){}")
    manager = ShaderManager()
    prog1 = manager.load_program(ctx, vert, frag)
    prog2 = manager.load_program(ctx, vert, frag)
    assert prog1 is prog2
