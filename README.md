# FastAPI Learning Notes

This repo contains small FastAPI examples and a learning log explaining what I learned while working with FastAPI on Windows (PowerShell). The goal is to document setup, running, and common issues so you can quickly reproduce and learn.

## What is FastAPI

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints. It uses Pydantic for data validation and Starlette for the web parts. FastAPI makes it easy to build robust, production-ready APIs with automatic OpenAPI (Swagger) docs.

## What I learned (summary)
- FastAPI uses Python type hints and Pydantic models to parse and validate request bodies.
- Handlers can be async or sync; async handlers allow non-blocking IO.
- Uvicorn is an ASGI server commonly used to run FastAPI apps.
- Common error: `Attribute "app" not found in module "main"` usually means `main.py` was empty or an import error occurred during module import.

## Prerequisites
- Python 3.10+ installed
- (Recommended) Use a virtual environment

## Quick setup (Windows PowerShell)

Open PowerShell in the project folder (this repo root). Example commands:

```powershell
# create/activate venv
python -m venv venv
.\venv\Scripts\Activate

# install dependencies
pip install --upgrade pip
pip install fastapi uvicorn pydantic
```

## Running the app (development)

Assuming you have a `main.py` with a FastAPI `app` instance (for example, `app = FastAPI()`), run:

```powershell
uvicorn main:app --reload
```

This starts a development server on `http://127.0.0.1:8000` and the `--reload` option watches for file changes.

## Example `main.py`

Here is a minimal `main.py` you can use (save to `main.py`):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post('/items/')
async def create_item(item: Item):
    return item

@app.get('/')
async def read_root():
    return {'Hello': 'World'}
```

## Common issues & debugging

- `Attribute "app" not found in module "main"` — Causes:
  - `main.py` file is empty (0 bytes) or `app` was not defined.
  - An exception occurred during module import (e.g., syntax error, missing dependency), so `app` never got created.
  - A different module named `main` in PYTHONPATH shadowing your file.

  How to debug:

  ```powershell
  # check file exists and size
  Get-ChildItem .\main.py | Format-List Name,Length,FullName

  # try importing module to show traceback
  python -c "import importlib,traceback;\
try:\
    importlib.import_module('main'); print('Imported OK')\
except Exception:\
    traceback.print_exc()"
  ```

  If the import shows an exception, fix the error printed (syntax error, bad import, etc.). If `main.py` is empty, re-save the file with the FastAPI code.

## Testing endpoints

Use a browser for `GET /` or the interactive docs at `http://127.0.0.1:8000/docs` (Swagger UI) and `http://127.0.0.1:8000/redoc` (ReDoc).

Command-line tests (PowerShell / Windows):

```powershell
# simple curl-like test (Windows 10+ has curl)
curl http://127.0.0.1:8000/

# POST example with JSON
curl -X POST http://127.0.0.1:8000/items/ -H "Content-Type: application/json" -d '{"name":"apple","price":1.23}'
```

## Next steps / Learning path
- Learn about path/query/body parameters and response models.
- Practice dependency injection (the `Depends` system).
- Explore background tasks, middleware, CORS, authentication, and websockets.
- Add tests with `pytest` and Starlette's `TestClient`.
- Look into deployment options: Uvicorn + Gunicorn (Linux), containers (Docker), or cloud platforms.

## Resources
- Official docs: https://fastapi.tiangolo.com
- Uvicorn: https://www.uvicorn.org
- Pydantic: https://pydantic-docs.helpmanual.io

## Learning log (template)

- Date: 2025-11-23
- Topic: FastAPI basics — created `main.py`, ran uvicorn, fixed `Attribute "app" not found` by saving file content.
- Notes: Use virtualenv, always save file before running `uvicorn`.
- Next: Study Pydantic models and dependency injection.

---

File added: `README.md` — edit this file with your personal notes and learning entries.
