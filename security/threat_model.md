
## Примеры использования

### Шифрование скриптов

```python
from pathlib import Path
from origo3d.security.obfuscation.encrypt_scripts import encrypt

encrypted = encrypt(Path("game_logic.py"), b"my-secret-key")
Path("game_logic.py.enc").write_bytes(encrypted)
```

### Упаковка ассетов

```python
from pathlib import Path
from origo3d.security.obfuscation.obfuscate_assets import pack_assets

pack_assets(Path("assets"), Path("build/assets.zip"))
```
