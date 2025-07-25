import pyglet
import yaml
import os

SCENE_FILE = os.path.join(os.path.dirname(__file__), 'scene.yaml')

class Entity:
    def __init__(self, entity_id, x, y, width=50, height=50, color=(255, 0, 0)):
        self.id = entity_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=color)

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': list(self.color),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['x'],
            data['y'],
            width=data.get('width', 50),
            height=data.get('height', 50),
            color=tuple(data.get('color', [255, 0, 0])),
        )

    def update_shape(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height
        self.rect.color = self.color

class SceneEditor(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600, 'Scene Editor')
        self.entities = []
        self.selected = None
        self.drag_offset = (0, 0)
        self.load_scene()

    def on_draw(self):
        self.clear()
        for e in self.entities:
            e.rect.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.N:
            self.add_entity()
        elif symbol == pyglet.window.key.S:
            self.save_scene()
        elif symbol == pyglet.window.key.L:
            self.load_scene()

    def add_entity(self):
        entity_id = len(self.entities) + 1
        e = Entity(entity_id, 100, 100)
        self.entities.append(e)

    def on_mouse_press(self, x, y, button, modifiers):
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

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and self.selected:
            offset_x, offset_y = self.drag_offset
            self.selected.x = x - offset_x
            self.selected.y = y - offset_y
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
