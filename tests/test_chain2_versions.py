"""Regression coverage for Chain2 v15 and Onimusha v17 binary layouts."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import struct
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules import file_re_chain2 as chain2  # noqa: E402


MAGIC = 846096483


def independent_header_bytes(version: int) -> bytes:
    """Build a header from the REE-Lib field order, without HeaderData.write."""

    prefix = struct.pack("<4I", version, MAGIC, 0x10203040, 0x55667788)
    offsets = (
        0x1111111111111111,
        0x2222222222222222,
        0x3333333333333333,
        0x4444444444444444,
        0x5555555555555555,
        0x6666666666666666,
    )
    if version < 17:
        prefix += struct.pack(
            "<8Q",
            0xAAAAAAAAAAAAAAAA,
            offsets[0],
            0xBBBBBBBBBBBBBBBB,
            *offsets[1:],
        )
    else:
        prefix += struct.pack("<6Q", *offsets) + b"\x00" * 8

    # Eight one-byte counts/enums, followed by flags, step time, and hit flags.
    prefix += struct.pack(
        "<8B2I f12B",
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        0x77777777,
        0x88888888,
        1.25,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    )
    if version >= 12:
        prefix += struct.pack(
            "<HHBBHII",
            0x1212,
            0x3434,
            0x56,
            0x78,
            0x9A9A,
            0xBCBCBCBC,
            0xDEDEDEDE,
        )
        if version >= 17:
            # OWOTS ends after the two-byte null tail; the bytes that would
            # be the older cfil offset are the first settings record.
            prefix = prefix[:-8]
    return prefix


def test_header_layout_is_independent_for_v15_and_v17():
    v15 = independent_header_bytes(15)
    assert len(v15) == 128
    assert struct.unpack_from("<8Q", v15, 16) == (
        0xAAAAAAAAAAAAAAAA,
        0x1111111111111111,
        0xBBBBBBBBBBBBBBBB,
        0x2222222222222222,
        0x3333333333333333,
        0x4444444444444444,
        0x5555555555555555,
        0x6666666666666666,
    )

    v17 = independent_header_bytes(17)
    assert len(v17) == 112
    assert struct.unpack_from("<6Q", v17, 16) == (
        0x1111111111111111,
        0x2222222222222222,
        0x3333333333333333,
        0x4444444444444444,
        0x5555555555555555,
        0x6666666666666666,
    )
    assert v17[64:72] == b"\x00" * 8

    parsed = chain2.Chain2HeaderData()
    parsed.read(BytesIO(v17))
    assert parsed.version == 17
    assert parsed.collisionAttrAssetOffset == 0
    assert parsed.extraDataOffset == 0
    assert parsed.chainModelCollisionOffset == 0x1111111111111111
    assert parsed.chainGroupOffset == 0x2222222222222222
    assert parsed.chainSettingsOffset == 0x5555555555555555


def make_nonzero_file(version: int) -> chain2.Chain2File:
    file = chain2.Chain2File()
    file.Header.version = version
    file.Header.chainSettingsCount = 1
    file.Header.chainGroupCount = 1
    file.Header.chainWindSettingsCount = 1
    file.Header.chainLinkCount = 1

    setting = chain2.Chain2SettingsData()
    setting.id = 0x1234
    setting.settingsAttrFlags = 0xA5
    setting.springCalcType = 3
    setting.windID = -2
    setting.motionForce = 1.25
    setting.groupDefaultAttr = 0x87654321
    setting.windEffectCoef = 0.75
    setting.velocityLimit = 12.5
    setting.hardness = 0.33
    setting.motionForceCalcType = 4
    file.ChainSettingsList.append(setting)

    node = chain2.Chain2NodeData()
    node.angleLimitDirectionX = 0.1
    node.angleLimitDirectionW = 0.9
    node.angleLimitRad = 0.42
    node.collisionFilterFlags = 0x12345678
    node.attrFlags = 0xABCDEF01
    node.constraintJntNameHash = 0x13572468
    node.windCoef = 0.66
    node.angleMode = 2
    node.collisionShape = 3
    node.attachType = 4
    node.rotationType = 5
    node.gravityCoef = 0.8
    node.jointHash = 0x24681357
    node.basePos = (1.0, 2.0, 3.0)

    group = chain2.Chain2GroupData()
    group.settingID = setting.id
    group.nodeCount = 1
    group.rotationOrder = 2
    group.autoBlendCheckNodeNo = 3
    group.windID = 1
    group.tag0 = 0x10203040
    group.hierarchyHash0 = 0x50607080
    group.dampingNoise0 = 0.2
    group.endRotConstMax = 8.5
    group.attrFlags = 0x11112222
    group.clspFlags0 = 0x33334444
    group.clspFlags1 = 0x55556666
    group.interpCount = 7
    group.nodeInterpolationMode = 8
    group.nodeList.append(node)
    file.ChainGroupList.append(group)

    wind = chain2.Chain2WindSettingsData()
    wind.id = 1
    wind.windDirection = 2
    wind.windCount = 3
    wind.windType = 4
    wind.randomDamping = 0.25
    wind.dir0X = 0.5
    wind.max0 = 1.5
    file.WindSettingsList.append(wind)

    link = chain2.Chain2LinkData()
    link.terminateNodeNameHashA = 0x01020304
    link.terminateNodeNameHashB = 0x05060708
    link.distanceShrinkLimitCoef = 0.4
    link.distanceExpandLimitCoef = 1.6
    link.clspFlags0 = 0x11111111
    link.clspFlags1 = 0x22222222
    link.linkMode = 2
    link.connectFlags = 3
    link.linkAttrFlags = 4
    link.nodeCount = 1
    link.skipGroupA = 5
    link.skipGroupB = 6
    link.linkOrder = 7
    link_node = chain2.Chain2LinkNode()
    link_node.collisionRadius = 0.77
    link_node.collisionFilterFlags = 0x12345678
    link.nodeColLinkList.append(link_node)
    file.ChainLinkList.append(link)
    return file


@pytest.mark.parametrize("version", [15, 17])
def test_nonzero_settings_group_node_wind_and_link_roundtrip(version: int):
    source = make_nonzero_file(version)
    stream = BytesIO()
    source.write(stream)

    stream.seek(0)
    parsed = chain2.Chain2File()
    parsed.read(stream)

    assert parsed.Header.version == version
    assert parsed.Header.chainSettingsCount == 1
    assert parsed.Header.chainGroupCount == 1
    assert parsed.Header.chainWindSettingsCount == 1
    assert parsed.Header.chainLinkCount == 1

    setting = parsed.ChainSettingsList[0]
    assert setting.id == 0x1234
    assert setting.settingsAttrFlags == 0xA5
    assert setting.windID == -2
    assert setting.motionForce == pytest.approx(1.25)
    assert setting.groupDefaultAttr == 0x87654321

    group = parsed.ChainGroupList[0]
    assert group.settingID == 0x1234
    assert group.tag0 == 0x10203040
    assert group.attrFlags == 0x11112222
    assert group.nodeInterpolationMode == 8
    node = group.nodeList[0]
    assert node.constraintJntNameHash == 0x13572468
    assert node.jointHash == 0x24681357
    assert node.basePos == pytest.approx((1.0, 2.0, 3.0))

    wind = parsed.WindSettingsList[0]
    assert wind.id == 1
    assert wind.windDirection == 2
    assert wind.windType == 4
    assert wind.randomDamping == pytest.approx(0.25)

    link = parsed.ChainLinkList[0]
    assert link.terminateNodeNameHashA == 0x01020304
    assert link.terminateNodeNameHashB == 0x05060708
    assert link.clspFlags0 == 0x11111111
    assert link.clspFlags1 == 0x22222222
    assert link.nodeColLinkList[0].collisionRadius == pytest.approx(0.77)
    assert link.nodeColLinkList[0].collisionFilterFlags == 0x12345678
