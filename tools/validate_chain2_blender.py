"""Validate a Chain2 import against an extracted mesh armature in Blender."""

from __future__ import annotations

import argparse
from contextlib import redirect_stderr, redirect_stdout
import importlib
import io
import json
from pathlib import Path
import sys

import bpy


def parse_args() -> argparse.Namespace:
    try:
        separator = sys.argv.index("--")
        argv = sys.argv[separator + 1 :]
    except ValueError:
        argv = []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh", required=True, help="Extracted .mesh.<version> path")
    parser.add_argument("--chain", required=True, help="Extracted .chain2.<version> path")
    parser.add_argument("--mesh-addon", required=True, help="RE Mesh Editor add-on directory")
    parser.add_argument("--chain-addon", required=True, help="RE Chain Editor add-on directory")
    parser.add_argument("--import-unknowns", action="store_true")
    parser.add_argument("--expected-groups", type=int)
    parser.add_argument("--expected-nodes", type=int)
    parser.add_argument("--expected-links", type=int)
    parser.add_argument("--fail-on-missing-bones", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def enable_addon(path_value: str):
    addon_path = Path(path_value).expanduser().resolve()
    if str(addon_path.parent) not in sys.path:
        sys.path.insert(0, str(addon_path.parent))
    result = bpy.ops.preferences.addon_enable(module=addon_path.name)
    if "FINISHED" not in result:
        raise RuntimeError("Failed to enable %s: %s" % (addon_path.name, result))
    return importlib.import_module(addon_path.name)


def main() -> int:
    args = parse_args()
    mesh_path = Path(args.mesh).expanduser().resolve()
    chain_path = Path(args.chain).expanduser().resolve()
    mesh_addon = enable_addon(args.mesh_addon)
    enable_addon(args.chain_addon)
    chain_impl = importlib.import_module(
        Path(args.chain_addon).resolve().name + ".modules.blender_re_chain"
    )
    mesh_options = {
        "clearScene": True,
        "createCollections": True,
        "loadMaterials": False,
        "loadMDFData": False,
        "loadShellFur": False,
        "loadUnusedTextures": False,
        "loadUnusedProps": False,
        "useBackfaceCulling": False,
        "reloadCachedTextures": False,
        "mdfPath": "",
        "importAllLODs": True,
        "importBlendShapes": True,
        "rotate90": True,
        "mergeArmature": "",
        "importArmatureOnly": False,
        "mergeGroups": False,
        "importShadowMeshes": False,
        "importOcclusionMeshes": False,
        "importBoundingBoxes": False,
    }
    log_buffer = io.StringIO()
    with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
        mesh_impl = getattr(mesh_addon, "importREMeshFile")
        mesh_warnings, mesh_errors = mesh_impl(str(mesh_path), mesh_options)
        armature = next(
            (obj for obj in bpy.data.objects if obj.type == "ARMATURE"), None
        )
        chain_result = False
        if armature is not None:
            chain_result = chain_impl.importChainFile(
                str(chain_path),
                {
                    "targetArmature": armature.data.name,
                    "mergeChain": "",
                    "importUnknowns": args.import_unknowns,
                },
                isChain2=True,
            )

    log = log_buffer.getvalue()
    clean_lines = [line.strip() for line in log.splitlines() if line.strip()]
    type_errors = [line for line in clean_lines if "bpy_struct[key]" in line]
    missing_bones = [line for line in clean_lines if "Could not find hashed bone" in line]
    group_count = sum(
        1 for obj in bpy.data.objects if obj.get("TYPE") == "RE_CHAIN_CHAINGROUP"
    )
    node_count = sum(
        1 for obj in bpy.data.objects if obj.get("TYPE") == "RE_CHAIN_NODE"
    )
    link_count = sum(
        1 for obj in bpy.data.objects if obj.get("TYPE") == "RE_CHAIN_LINK"
    )
    summary = {
        "mesh": str(mesh_path),
        "chain": str(chain_path),
        "importUnknowns": args.import_unknowns,
        "meshWarnings": list(mesh_warnings or []),
        "meshErrors": list(mesh_errors or []),
        "chainResult": bool(chain_result),
        "armatureObjects": sum(1 for obj in bpy.data.objects if obj.type == "ARMATURE"),
        "armatureBones": sum(
            len(obj.data.bones) for obj in bpy.data.objects if obj.type == "ARMATURE"
        ),
        "chainGroups": group_count,
        "chainNodes": node_count,
        "chainLinks": link_count,
        "missingHashedBones": missing_bones,
        "typeErrors": type_errors,
        "tracebackLines": [line for line in clean_lines if "Traceback" in line],
    }
    strict_failures = []
    if args.strict:
        if not summary["chainResult"]:
            strict_failures.append("Chain2 import returned failure")
        if summary["typeErrors"]:
            strict_failures.append("Blender 5 geometry modifier TypeErrors were logged")
        if summary["tracebackLines"]:
            strict_failures.append("Traceback was logged during import")
        if args.fail_on_missing_bones and summary["missingHashedBones"]:
            strict_failures.append("hashed bones are missing from the armature")
        for key, expected in (
            ("chainGroups", args.expected_groups),
            ("chainNodes", args.expected_nodes),
            ("chainLinks", args.expected_links),
        ):
            if expected is not None and summary[key] != expected:
                strict_failures.append(
                    "%s=%s, expected %s" % (key, summary[key], expected)
                )
    summary["strictFailures"] = strict_failures
    summary["ok"] = not strict_failures
    if args.output:
        args.output.expanduser().resolve().write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
