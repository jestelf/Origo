from origo3d.rendering.shader_preview import ShaderPreview


def test_preview_render_bytes():
    preview = ShaderPreview(64, 64)
    data = preview.render()
    assert isinstance(data, (bytes, bytearray))
    # ожидаем количество байт равно width*height*3
    assert len(data) == 64 * 64 * 3
