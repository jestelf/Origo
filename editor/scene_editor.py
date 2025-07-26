import pyglet
import yaml
import os

SCENE_FILE = os.path.join(os.path.dirname(__file__), 'scene.yaml')

class Entity:
    """Примитивный объект сцены."""

    def __init__(self, entity_id: int, x: float, y: float,
                 width: float = 50, height: float = 50,
                 color: tuple[int, int, int] = (255, 0, 0)) -> None:
        self.id = entity_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rotation = 0.0
        self.scale = 1.0
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=color)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': list(self.color),
            'rotation': self.rotation,
            'scale': self.scale,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Entity':
        ent = cls(
            data['id'],
            data['x'],
            data['y'],
            width=data.get('width', 50),
            height=data.get('height', 50),
            color=tuple(data.get('color', [255, 0, 0])),
        )
        ent.rotation = data.get('rotation', 0.0)
        ent.scale = data.get('scale', 1.0)
        ent.update_shape()
        return ent

    def update_shape(self) -> None:
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width * self.scale
        self.rect.height = self.height * self.scale
        self.rect.color = self.color
        self.rect.rotation = self.rotation

class SceneEditor(pyglet.window.Window):
    """Простейший редактор сцен."""

    GRID_SPACING = 50

    def __init__(self) -> None:
        super().__init__(800, 600, "Scene Editor")
        self.entities: list[Entity] = []
        self.selected: Entity | None = None
        self.drag_offset = (0, 0)
        self.rotating = False
        self.prev_mouse = (0, 0)
        self.show_grid = True
        self.info_label = pyglet.text.Label(
            "N - новый объект | Delete - удалить | Ctrl+S - сохранить | Ctrl+L - загрузка",
            x=5,
            y=self.height - 5,
            anchor_x="left",
            anchor_y="top",
        )
        self.load_scene()

    def on_draw(self):
        self.clear()
        if self.show_grid:
            self.draw_grid()
        for e in self.entities:
            e.rect.draw()
        self.info_label.draw()

    def draw_grid(self) -> None:
        step = self.GRID_SPACING
        modern_api = int(pyglet.version.split(".")[0]) >= 2

        # Pyglet 2.x uses 3D positions and RGBA colors in its default shader.
        # Provide dummy Z coordinate and full alpha so grid lines render correctly.
        for x in range(0, self.width, step):
            if modern_api:
                pyglet.graphics.draw(
                    2,
                    pyglet.gl.GL_LINES,
                    position=("f", (x, 0, 0, x, self.height, 0)),
                    colors=("Bn", (200, 200, 200, 255) * 2),
                    tex_coords=("f", (0.0, 0.0, 0.0) * 2),
                )
            else:
                pyglet.graphics.draw(
                    2,
                    pyglet.gl.GL_LINES,
                    ("v2f", (x, 0, x, self.height)),
                    ("c3B", (200, 200, 200) * 2),
                )
        for y in range(0, self.height, step):
            if modern_api:
                pyglet.graphics.draw(
                    2,
                    pyglet.gl.GL_LINES,
                    position=("f", (0, y, 0, self.width, y, 0)),
                    colors=("Bn", (200, 200, 200, 255) * 2),
                    tex_coords=("f", (0.0, 0.0, 0.0) * 2),
                )
            else:
                pyglet.graphics.draw(
                    2,
                    pyglet.gl.GL_LINES,
                    ("v2f", (0, y, self.width, y)),
                    ("c3B", (200, 200, 200) * 2),
                )

    def on_key_press(self, symbol, modifiers):
        ctrl = modifiers & pyglet.window.key.MOD_CTRL
        if symbol == pyglet.window.key.N and ctrl:
            self.add_entity()
        elif symbol == pyglet.window.key.S and ctrl:
            self.save_scene()
        elif symbol == pyglet.window.key.L and ctrl:
            self.load_scene()
        elif symbol == pyglet.window.key.D and ctrl and self.selected:
            self.duplicate_selected()
        elif symbol == pyglet.window.key.DELETE and self.selected:
            self.entities.remove(self.selected)
            self.selected = None
        elif symbol == pyglet.window.key.R and self.selected:
            self.selected.rotation = (self.selected.rotation + 15) % 360
            self.selected.update_shape()
        elif symbol in (pyglet.window.key.PLUS, pyglet.window.key.NUM_ADD) and self.selected:
            self.selected.scale += 0.1
            self.selected.update_shape()
        elif symbol in (pyglet.window.key.MINUS, pyglet.window.key.NUM_SUBTRACT) and self.selected:
            self.selected.scale = max(0.1, self.selected.scale - 0.1)
            self.selected.update_shape()
        elif symbol == pyglet.window.key.G:
            self.show_grid = not self.show_grid

    def on_text_motion(self, motion: int):
        if not self.selected:
            return
        if motion == pyglet.window.key.MOTION_LEFT:
            self.selected.x -= 5
        elif motion == pyglet.window.key.MOTION_RIGHT:
            self.selected.x += 5
        elif motion == pyglet.window.key.MOTION_UP:
            self.selected.y += 5
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.selected.y -= 5
        self.selected.update_shape()

    def add_entity(self):
        entity_id = len(self.entities) + 1
        e = Entity(entity_id, 100, 100)
        self.entities.append(e)

    def duplicate_selected(self) -> None:
        if not self.selected:
            return
        entity_id = len(self.entities) + 1
        copy = Entity(
            entity_id,
            self.selected.x + 10,
            self.selected.y + 10,
            width=self.selected.width,
            height=self.selected.height,
            color=self.selected.color,
        )
        copy.rotation = self.selected.rotation
        copy.scale = self.selected.scale
        copy.update_shape()
        self.entities.append(copy)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.RIGHT and self.selected:
            self.rotating = True
            self.prev_mouse = (x, y)
            return
        if button != pyglet.window.mouse.LEFT:
            return
        for e in self.entities:
            if (e.x <= x <= e.x + e.width) and (e.y <= y <= e.y + e.height):
                self.selected = e
                self.drag_offset = (x - e.x, y - e.y)
                break

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.selected = None
        elif button == pyglet.window.mouse.RIGHT:
            self.rotating = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and self.selected:
            offset_x, offset_y = self.drag_offset
            self.selected.x = x - offset_x
            self.selected.y = y - offset_y
            self.selected.update_shape()
        if self.rotating and self.selected and (buttons & pyglet.window.mouse.RIGHT):
            self.selected.rotation += dx
            self.selected.update_shape()

    def save_scene(self):
        data = [e.to_dict() for e in self.entities]
        with open(SCENE_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        print(f'Scene saved to {SCENE_FILE}')

    def load_scene(self):
        if not os.path.exists(SCENE_FILE):
            return
        with open(SCENE_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or []
        self.entities.clear()
        for item in data:
            e = Entity.from_dict(item)
            self.entities.append(e)
        print(f'Scene loaded from {SCENE_FILE}')

if __name__ == '__main__':
    editor = SceneEditor()
    pyglet.app.run()
