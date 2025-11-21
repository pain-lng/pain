# Utilities

## convert_icons.py

Генерирует Windows ICO и macOS ICNS для `pain-compiler` и `pain-lsp` из исходных PNG.

### Требования

```bash
pip install Pillow
```

### Запуск

```bash
python utils/convert_icons.py
```

Скрипт надо вызывать из корня репозитория. Он:
- Берёт PNG из `pain-compiler/resources/icons/linux/` и `pain-lsp/resources/icons/linux/`
- Пересобирает `pain.ico` и обе копии `lsp.ico`
- Готовит ICNS и вспомогательные `.iconset` структуры (на macOS можно добить `iconutil`)

CI (GitHub Actions) гоняет тот же скрипт перед релизной сборкой, поэтому локально и на сервере используются одинаковые артефакты.

