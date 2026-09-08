# tests

## Key Files

| Path | Purpose |
| --- | --- |
| `test_chain2_versions.py` | Pure Python regression tests for independent v15/v17 header layouts and non-zero Chain2 data roundtrips. |
| `test_geometry_modifier_inputs.py` | Checks Blender 3/4 legacy keys and Blender 5 modifier input properties. |

## Common Patterns

- On this workstation run `$env:PYTHONDONTWRITEBYTECODE='1'; & 'D:\\codeprogram\\Python\\python.exe' -m pytest --rootdir tests --import-mode=importlib tests/test_chain2_versions.py` from the add-on root (Python 3.14.6 / pytest 9.1.1); the explicit test root prevents pytest from importing the Blender add-on `__init__.py`.
- A PATH-independent alternative is `uv run --no-project --with pytest python -m pytest --rootdir tests --import-mode=importlib tests/test_chain2_versions.py`.
- The header fixture is assembled with `struct`, independently of `Chain2HeaderData.write`, so offset and reserved-byte regressions are caught.
- The data fixture uses non-zero settings, group/node, wind, and link values for both v15 and v17.
