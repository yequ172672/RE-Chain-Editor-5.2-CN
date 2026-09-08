"""Parse one Chain2 file and print a compact structural validation report."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.file_re_chain2 import readREChain2  # noqa: E402


def build_report(path: Path) -> dict:
    chain_file = readREChain2(str(path))
    header = chain_file.Header
    return {
        "input": str(path),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "header": {
            "version": header.version,
            "magic": "0x%08X" % header.magic,
            "masterSize": header.masterSize,
            "groupCount": header.chainGroupCount,
            "settingsCount": header.chainSettingsCount,
            "modelCollisionCount": header.chainModelCollisionCount,
            "windSettingCount": header.chainWindSettingsCount,
            "linkCount": header.chainLinkCount,
            "offsets": {
                "modelCollision": header.chainModelCollisionOffset,
                "groups": header.chainGroupOffset,
                "links": header.chainLinkOffset,
                "freeLinks": header.chainFreeLinkOffset,
                "settings": header.chainSettingsOffset,
                "windSettings": header.chainWindSettingsOffset,
            },
        },
        "counts": {
            "groups": len(chain_file.ChainGroupList),
            "settings": len(chain_file.ChainSettingsList),
            "collisions": len(chain_file.ChainCollisionList),
            "windSettings": len(chain_file.WindSettingsList),
            "links": len(chain_file.ChainLinkList),
            "nodes": sum(len(group.nodeList) for group in chain_file.ChainGroupList),
            "subGroups": sum(len(group.subGroupList) for group in chain_file.ChainGroupList),
            "linkNodes": sum(len(link.nodeColLinkList) for link in chain_file.ChainLinkList),
            "settingSubData": sum(
                len(setting.subDataList) for setting in chain_file.ChainSettingsList
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chain", type=Path, help="Path to a .chain2.<version> file")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    path = args.chain.expanduser().resolve()
    if not path.is_file():
        parser.error("Chain2 file does not exist: %s" % path)
    report = build_report(path)
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.expanduser().resolve().write_text(output, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
