"""Geometry Nodes modifier input compatibility tests without Blender."""

from __future__ import annotations

import importlib
from types import SimpleNamespace
import sys


def load_utils(monkeypatch, version):
    fake_bpy = SimpleNamespace(app=SimpleNamespace(version=version))
    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)
    sys.modules.pop("modules.blender_utils", None)
    return importlib.import_module("modules.blender_utils")


def test_legacy_modifier_keys_are_preserved(monkeypatch):
    utils = load_utils(monkeypatch, (3, 6, 0))
    modifier = {}
    assert utils.setGeometryNodeModifierInput(modifier, 0, 1.25)
    assert modifier == {"Input_0": 1.25}

    utils = load_utils(monkeypatch, (4, 3, 0))
    modifier = {}
    assert utils.setGeometryNodeModifierInput(modifier, 1, "node")
    assert modifier == {"Socket_1": "node"}


def test_blender5_modifier_properties_inputs_are_used(monkeypatch):
    utils = load_utils(monkeypatch, (5, 2, 0))

    class Socket:
        def __init__(self):
            self.value = None

    modifier = SimpleNamespace(
        properties=SimpleNamespace(
            inputs=SimpleNamespace(Socket_0=Socket(), Socket_1=Socket())
        )
    )
    assert utils.setGeometryNodeModifierInput(modifier, 0, 0.5)
    assert utils.setGeometryNodeModifierInput(modifier, 1, "obj")
    assert modifier.properties.inputs.Socket_0.value == 0.5
    assert modifier.properties.inputs.Socket_1.value == "obj"


def test_link_collision_radius_callback_uses_blender5_inputs(monkeypatch):
    import ast
    from pathlib import Path
    utils = load_utils(monkeypatch, (5, 2, 0))
    source = Path(__file__).resolve().parents[1] / "modules/re_chain_propertyGroups.py"
    tree = ast.parse(source.read_text())
    callback = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "update_ChainLinkCollisionRadius")
    socket = SimpleNamespace(value=0)
    modifier = SimpleNamespace(properties=SimpleNamespace(inputs=SimpleNamespace(Socket_2=socket)), node_group=SimpleNamespace(interface_update=lambda context: None))
    obj = type("Object", (dict,), {})(TYPE="RE_CHAIN_LINK_COLLISION")
    obj.modifiers = {"REChainGeometryNodes": modifier}
    obj.re_chain_chainlink_collision = SimpleNamespace(collisionRadius=0.125)
    ns = {"setGeometryNodeModifierInput": utils.setGeometryNodeModifierInput}
    exec(compile(ast.Module(body=[callback], type_ignores=[]), str(source), "exec"), ns)
    ns[callback.name](SimpleNamespace(id_data=obj), None)
    assert socket.value == 0.125
