# modules

## Key Files

| Path | Purpose |
| --- | --- |
| `file_re_chain2.py` | Binary Chain2 reader/writer and version specific layout handling. |
| `blender_re_chain.py` | Converts parsed Chain2 data into Blender collections and objects. |

## Common Patterns

- Keep file version constants and `supportedVersionSet` in `file_re_chain2.py` aligned with the game list extensions.
- Chain2 version 17 omits the collision-attribute and extra-data header offsets, inserts eight reserved bytes after the remaining offsets, and ends at the 112-byte null tail before settings; preserve this conditional layout in both `read` and `write`.
- Keep Blender object conversion independent from binary layout changes; parsed offsets should be resolved by `Chain2File.read` before `blender_re_chain.py` consumes the data.

- OWOTS export uses the v17 header and relocates free-link records (40-byte entry plus 16-byte endpoints). Preserve opaque parameters/endpoints in collection metadata across save/reopen; do not convert these links to older versions or silently merge them.
- Chain2 Blender conversion retains unexposed header fields, link counts/CLSP flags and unresolved terminal hashes. The import dialog exposes Import Unknown Hashes; use it when the mesh lacks chain bones to preserve records, without claiming their viewport attachment is correct.
