import pyglet

from editor.scene_editor import SceneEditor


class HierarchyWindow(pyglet.window.Window):
    """Simple hierarchy listing entities."""

    LINE_HEIGHT = 20

    def __init__(self, editor: SceneEditor) -> None:
        super().__init__(250, 400, "Hierarchy")
        self.editor = editor

    def on_draw(self) -> None:  # pragma: no cover - GUI
        self.clear()
        y = self.height - self.LINE_HEIGHT
        for ent in self.editor.entities:
            label = pyglet.text.Label(
                f"Entity {ent.id}",
                x=5,
                y=y,
                anchor_x="left",
                anchor_y="top",
                color=(255, 255, 255, 255),
            )
            if ent is self.editor.selected:
                pyglet.graphics.draw(
                    4,
                    pyglet.gl.GL_LINE_LOOP,
                    ("v2f", (0, y - self.LINE_HEIGHT + 4, self.width, y - self.LINE_HEIGHT + 4,
                            self.width, y + 4, 0, y + 4)),
                    ("c3B", (255, 255, 0) * 4),
                )
            label.draw()
            y -= self.LINE_HEIGHT

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:  # pragma: no cover - GUI
        index = int((self.height - y) / self.LINE_HEIGHT)
        if 0 <= index < len(self.editor.entities):
            self.editor.selected = self.editor.entities[index]


class InspectorWindow(pyglet.window.Window):
    """Display properties of the selected entity."""

    def __init__(self, editor: SceneEditor) -> None:
        super().__init__(250, 400, "Inspector")
        self.editor = editor

    def on_draw(self) -> None:  # pragma: no cover - GUI
        self.clear()
        if not self.editor.selected:
            text = "No entity selected"
            label = pyglet.text.Label(text, x=10, y=self.height - 20, anchor_x="left", anchor_y="top")
            label.draw()
            return
        e = self.editor.selected
        lines = [
            f"ID: {e.id}",
            f"Pos: ({e.x:.0f}, {e.y:.0f})",
            f"Size: {e.width}x{e.height}",
            f"Rotation: {e.rotation:.1f}",
            f"Scale: {e.scale:.2f}",
            f"Color: {e.color}",
        ]
        y = self.height - 20
        for line in lines:
            label = pyglet.text.Label(line, x=10, y=y, anchor_x="left", anchor_y="top")
            label.draw()
            y -= 20


class FullEditor:
    """Launcher for multiple windows resembling a simple Unity layout."""

    def __init__(self) -> None:
        self.scene = SceneEditor()
        self.hierarchy = HierarchyWindow(self.scene)
        self.inspector = InspectorWindow(self.scene)

        @self.scene.event
        def on_close():
            pyglet.app.exit()

        @self.hierarchy.event
        def on_close():
            pyglet.app.exit()

        @self.inspector.event
        def on_close():
            pyglet.app.exit()


if __name__ == "__main__":
    FullEditor()
    pyglet.app.run()
