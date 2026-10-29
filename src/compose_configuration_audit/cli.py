from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import audit_compose

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Docker Compose normalized JSON risk audit.")
    parser.add_argument("config", help="Output from docker compose config --format json (keep private)")
    parser.add_argument("--strict", action="store_true", help="Fail on medium as well as high-severity findings")
    args = parser.parse_args(argv)
    result = audit_compose(json.loads(Path(args.config).read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2))
    return 1 if result["high"] or (args.strict and result["medium"]) else 0

if __name__ == "__main__":
    raise SystemExit(main())
