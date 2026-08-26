# PDF Alchemy

This is the template repo for the CLI tool to manipulate pdfs

**Fork** the project to your github account, this will have the assotiated tests and template to start the project and finish implementation

# Requirements
- Python
- UV
- pymupdf

# Sync and update project packages

```bash
uv sync
```

# Run the tool

1. Initialize `venv`
```bash
uv venv
```

```bash
source .venv/bin/activate
```

2. Run the tool
```bash
uv run main.py
```

# Commands

Se han añadido dos nuevas funcionalidades al CLI de PDF Alchemy:

1. ** Traducir PDF (translate):** Permite traducir automáticamente el contenido de texto de un archivo PDF al idioma seleccionado y generar un nuevo archivo PDF con el texto traducido.
Ejemplo de uso: uv run main.py -f ./tests/assets/test_alchemy.pdf -o ./translate_test/translated.pdf translate --to es
2. ** Añadir imagen (image):**  Permite insertar una imagen en una página específica del PDF, definiendo su posición y dimensiones dentro de la página.
Ejemplo de uso: uv run main.py -f ./tests/assets/test_alchemy.pdf -o ./image_test/image_added.pdf image ./tests/assets/test.png --page 1 --x 100 --y 100 --width 200 --height 200
# Run tests

```bash
uv run pytest -q
```

# Compile to a standalone executable

```bash
uv pip install pyinstaller
```

```bash
uv run pyinstaller --onefile main.py
```

> You'll see the new compilation under `dist/`
