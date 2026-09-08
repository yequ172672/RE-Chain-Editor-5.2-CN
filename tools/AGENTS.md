# tools

## Key Files

| Path | Purpose |
| --- | --- |
| `validate_chain2_sample.py` | Parses a real Chain2 file and emits header, object counts, and SHA256 as JSON. |
| `validate_chain2_blender.py` | Imports a Chain2 file after importing its mesh armature and checks Blender object counts and 5.2 callback errors. |

## Common Patterns

- Run with the add-on root as the working directory and the full Python path when the PATH Python lacks pytest.
- The validator uses the same pure Python parser as the add-on and does not require Blender or modify the input file.
- Use `--output` to preserve a JSON report beside validation samples.
- Run the Blender validator with `--import-unknowns --expected-groups 22 --expected-nodes 82 --expected-links 10 --strict` for the OWOTS ch001 sample; missing hashed bones remain explicit in the report unless `--fail-on-missing-bones` is requested.
