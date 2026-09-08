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
