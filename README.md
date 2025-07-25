
Origo3D — Модульная 3D-игровая платформа  
📌 Назначение проекта  
Origo3D — это модульная, расширяемая игровая среда и движок, ориентированный на создание, тестирование, моддинг и анализ интерактивных 3D-сцен. Проект поддерживает скрипты, визуальное редактирование, облачную инфраструктуру, продвинутые пайплайны и инструменты наблюдаемости.

🧭 Навигация по структуре проекта  
Основной уровень  
| Путь                         | Назначение                                     |
| ---------------------------- | ----------------------------------------------- |
| `main.py`                    | Главная точка запуска редактора или движка      |
| `requirements.txt`           | Зависимости для сборки и разработки             |
| `extend_origo_structure.py`  | Скрипт для генерации/расширения структуры каталогов проекта |
| `config.yaml`                | Глобальная конфигурация проекта                 |

📁 Описание ключевых директорий  
- **`.docs/`** — Внутренняя документация по процессам  
  Содержит шаблоны, гайды, требования к PR, changelog, code style. Используется командой для контроля качества и соглашений по коду.  
  **Связи:**  
  - Связан с `docs/conventions/`  
  - Участвует в CI для проверки PR (см. `.github/workflows/`)

- **`docs/`** — Функциональная, техническая и архитектурная документация  
  Содержит:  
  - Архитектурные гайды (`docs/architecture/`)  
  - Конвенции (`docs/conventions/`)  
  - Терминологию, use-case'ы  
  - Описание форматов (`scene_format.md`, `resources.md`)  
  - Глоссарий, лицензия, описание API  
  **Связи:**  
  - Используется в `generate_docs.py` из `tools/`  
  - Сопровождает `origo3d/`, `assets/`, `configs/` и `scene/`

- **`assets/`** — Все игровые и редакторские ресурсы  
  - `animations/`, `audio/`, `models/`, `textures/`, `video/`, `ui/`  
  - `locales/`: поддержка i18n через `.json/.yaml`  
  **Связи:**  
  - Загружается через `origo3d.resources`
  - Управляется через `build/`, `asset_pipeline/` и `tools/compile_shaders.py`
  - Оптимизация мобильных ассетов: `scripts/maintenance/optimize_assets.py`

- **`build/`** — Сборка проекта  
  - Скрипты сборки: `build_game.py`, `package_game.py`,
    `android_build.sh`, `ios_build.sh`, `wasm_build.sh`
  - Метаданные сборки: `build/meta/`  
  - Поддержка ОС: `linux/`, `web/`, `windows/`  
  - Подпись и проверка: `build/signing/`  
  **Связи:**  
  - Использует `assets/`, `configs/`, `scripts/maintenance/`  
  - Интеграция с CI: `cloud_build/`, `ci_config/`

- **`configs/`** — Конфигурационные YAML-файлы движка  
  - `engine.yaml`, `graphics.yaml`, `input.yaml`, `feature_flags.yaml` и др.  
- `env/`: переменные окружения (dev, staging, prod)
  **Связи:**
  - Загружается в `runtime/env_settings.py`
  - Используется в `main.py`, `tools/validate_config.py`
  - При запуске движка конфигурации автоматически считываются,
    например `configs/graphics.yaml` задаёт размер окна, режим vsync и
    выбираемое API рендера.

- **`origo3d/`** — Основной код движка  
  Подсистемы:  
  | Подмодуль                                   | Назначение                                   |
  | ------------------------------------------- | --------------------------------------------- |
  | `ecs/`, `components/`, `systems/`           | Entity-компонентная модель                   |
  | `rendering/`, `shaders/`, `resources/`      | Рендеринг                                    |
  | `physics/`, `math/`                         | Физика, математика                           |
  | `audio/`, `animation/`, `dialogue/`         | Медиа подсистемы                             |
  | `ai/`, `fsm/`, `procedural/`                | ИИ, деревья поведения, генерация             |
  | `editor/`, `tools/`, `debug/`               | Devtools и GUI                               |
  | `scene/`, `serialization/`                  | Сцены, сохранения                            |
  | `security/`, `networking/`, `input/`, `localization/` | Инфраструктурные модули           |  
  **Связи:**  
  - Подключается в `main.py`, `scripts/`, `editors/`, `devtools/`, `tests/`

- **`scripts/`** — Автоматизация и утилиты  
  - CLI-интерфейс: `cli.py`  
  - Запуск сцен: `scene_runner.py`  
  - Bootstrap-процессы: `bootstrap_env.py`  
  - `maintenance/`: скрипты для очистки, миграций, архивации  
  **Связи:**  
  - Используется в CI/CD, `build/`, `cloud/`, `infra/monitoring`

- **`infra/`** — Инфраструктура и мониторинг  
  - `docker/`: `docker-compose.yml`, `nginx.conf`  
  - `monitoring/`: Prometheus + Grafana  
  - `alerts/`, `blackbox_probes/`, `log_ingestion/`  
  **Связи:**  
  - Настраивает прод окружение (`deployment/`)  
  - Интеграция с `telemetry/`, `logs/`, `cloud_build/`

- **`feedback/`** — Сбор обратной связи  
  - Ручные исследования (`usability_studies/`)  
  - Жалобы и предложения игроков (`player_reports/`)  
  - Анализ опросов (`user_survey_results.md`)  
  - Корреляция телеметрии (`telemetry_correlation.md`)  

- **`telemetry/`** — A/B-тесты, аналитика и схемы событий  
  - `ab_tests/`, `ab_test_dashboard.py`  
  - `events_schema.yaml` — стандарт формата событий  
  - `crash_frequency.py`  
  **Связи:**  
  - Генерирует данные для `dashboard/` и `analytics/`  
  - Анализирует поведение через `ai/` и `user_metrics.py`

- **`dashboard/`** — Панели и мониторинг пользователей  
  - Отображение метрик (`metrics_panel.py`)  
  - Поведение пользователей, фидбек, краши  
  - Визуальный монитор: `error_heatmap.py`, `build_monitor.py`

- **`qa/`** — Тестирование и контроль качества  
  - Матрица совместимости (`compatibility_matrix.md`)  
  - Ручные тест-кейсы (`manual_test_cases/`)  
  **Связь с:** `tests/`, `feedback/`, `dashboard/`

- **`sdk/examples/`** — Примеры использования SDK  
  - Расширения движка: `custom_component.py`, `gameplay_extension.py`

- **`mock_data/`** — Тестовые данные и шаблоны  
  - Подделки пользователей (`fake_users.json`)  
  - Примеры сцен (`test_scenes/`)

- **`cloud/` и `cloud_build/`** — Облачные хранилища и сборки  
  - AWS и GCP функции, CI-хуки  
  - Интеграция с GitHub Actions, Kubernetes (`deployment/`)

- **`devtools/`** — Визуальные отладочные инструменты  
  - Просмотр ресурсов, сцен, производительности  
  - `editor_layouts/`, `editors/`, `ui_tests/`  
  - Интеграции с Unity, Godot, Unreal  
  - UI автоматические тесты

- **`contrib/`** — Патчи и фичи сообщества  
  - `README.md` + `community_patch_01/`

- **`security/`** — Угрозы, политика, шаблоны ключей  
  - `threat_model.md`, `secrets_template.env`  
  - `policies/`, `audit/`

- **`scripting/`, `prefabs/`, `projects/`, `user_content/`**  
  Расширения и игровые проекты, сцены и моддинг

🔁 Взаимодействие подсистем  
- `ecs ↔ components ↔ systems` — основа сцены  
- `resources ↔ asset_pipeline ↔ build` — управление ресурсами  
- `ai ↔ analytics ↔ telemetry` — поведение + метрики  
- `devtools ↔ gui, scene` — визуальный дебаг  
- `networking + security + cloud` — онлайн-режимы и защита  
- `docs + .docs + ci_config` — контроль качества и документации

🚀 Этапы разработки  
- Создание сцен: `editor/`, `scene/`, `prefabs/`  
- Расширение логики: `components/`, `systems/`, `scripts/`  
- Импорт и сборка: `importers/`, `asset_pipeline/`, `build/`  
- Тестирование: `tests/`, `benchmarks/`, `ui_tests/`  
- Деплой: `deployment/`, `cloud_build/`, `infra/`  
- Поддержка: `feedback/`, `telemetry/`, `dashboard/`  
- Анализ и улучшения: `ai/`, `analytics/`, `devtools/`

✅ Как начать  
```bash
pip install -r requirements.txt
python main.py
````

Файлы конфигурации находятся в каталоге `configs/`. Перед запуском вы
можете изменить, например, `configs/graphics.yaml`, чтобы задать размер
окна, частоту обновления и предпочитаемый API рендерера.

При запуске в консоль выводятся основные сообщения инициализации,
что помогает убедиться в успешном создании окна и загрузке настроек.

Альтернативы:

* `python scripts/cli.py` — CLI-режим
* `python scripts/scene_runner.py` — запуск сцены напрямую
* `python build/build_game.py` — сборка билда

🎮 Редактор сцен
* `python editor/scene_editor.py` — запустит упрощённый редактор.
  Используйте `N` для создания объекта, перетаскивайте его мышью,
  `S` для сохранения сцены и `L` для загрузки из `editor/scene.yaml`.

🧩 Расширяемость

* Поддержка модов через `user_content/`
* Управление модами: `python scripts/mod_manager.py`
* CLI-плагины: `origo_cli/plugins/`
* Внешние расширения: `extensions/`
* Расширения сцены и логики через `sdk/examples/`, `tools/codegen/`
* Горячая перезагрузка модулей и ресурсов через подсистему `hotreload/`

📜 Лицензия
См. `legal/LICENSE.txt`
