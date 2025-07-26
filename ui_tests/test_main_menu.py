import os
import subprocess
import sys
import time

import pytest

# UI тесты требуют pyautogui для эмуляции ввода
pyautogui = pytest.importorskip("pyautogui")


@pytest.mark.skipif("DISPLAY" not in os.environ, reason="Требуется доступ к X-серверу")
def test_open_editor_main_menu():
    """Проверяем, что главное окно редактора запускается и принимает ввод."""
    env = os.environ.copy()
    env.pop("PYGLET_HEADLESS", None)  # гарантируем запуск с графикой
    proc = subprocess.Popen([sys.executable, "editor/scene_editor.py"], env=env)
    try:
        time.sleep(2)
        pyautogui.press("g")  # пример ввода: переключение сетки
        time.sleep(1)
        assert proc.poll() is None, "Редактор завершился преждевременно"
    finally:
        proc.terminate()
        proc.wait(timeout=5)

