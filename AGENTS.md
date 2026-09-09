# RE Chain Editor

## Key Files

| Path | Purpose |
| --- | --- |
| `__init__.py` | Blender add-on registration and supported Chain/Chain2 version lists. |
| `translations.py` | Blender 5.2 `zh_CN`/`zh_HANS` translation tables and dynamic text helpers. |
| `LOCALIZATION.md` | Short guide to translation contexts, dynamic helpers, and isolated Blender validation. |
| `modules/file_re_chain2.py` | Chain2 binary reader/writer, including version-specific header layouts. |
| `tests/test_chain2_versions.py` | Regression coverage for v15 and Onimusha v17 binary layouts. |
| `tools/validate_chain2_sample.py` | Reproducible pure Python report for a real Chain2 sample. |
| `tools/validate_chain2_blender.py` | Headless Blender mesh-armature plus Chain2 import validation. |

## Subdirectories

| Directory | Purpose |
| --- | --- |
| `modules/` | Blender integration and binary format implementation. |
| `tests/` | Pure Python parser regression tests. |
| `tools/` | Standalone parser validation utilities. |

## Common Patterns

- Keep OWOTS changes on `feat/onimusha-wots`; `origin` is the user's `yequ172672/RE-Chain-Editor-5.2-CN` fork and `upstream` is `NSACloud/RE-Chain-Editor`.
- Keep a Chain2 file version in `modules/file_re_chain2.py::supportedVersionSet` and the Blender file-handler set in `__init__.py` together.
- Version 17 omits two header offsets, inserts an eight-byte reserved block, and uses a 112-byte header with no older cfil offset tail; both read and write paths must preserve that layout.
- Run parser tests without Blender; use Blender 5.2 headless only for add-on registration and scene import checks.
- Keep Chinese localization in `translations.py`; register both `zh_CN` and `zh_HANS` through `bpy.app.translations` and preserve `*`/`Operator` contexts, English fallback, format identifiers, and game IDs.

- Preserve upstream authorship and label yequ172672 as fork maintainer. Preferences and README link to `https://github.com/yequ172672/RE-Chain-Editor-5.2-CN`; updater releases/tags use this fork and the explicit `feat/onimusha-wots` branch option. Do not fall back to upstream or the updater default master branch.

- The N-sidebar RE Chain tab includes a default-collapsed Fork Maintenance panel declared in `__init__.py`; keep it visible without an active object and respect the existing tab hide flag.
