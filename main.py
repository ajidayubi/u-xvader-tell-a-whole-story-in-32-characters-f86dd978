"""Wi-Fi name entry: a single network name, at most 32 characters.

The program writes the name to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output), then reads the file back as bytes and as text and verifies
both, so a bad write can never pass silently. Deterministic: no
network, no randomness, no clock, no input besides the environment
variable naming the output directory.
"""

import os
import sys

NAME = "The Cat Sat On The Router Again"
MAX_CHARS = 32


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(NAME)
    with open(path, "rb") as f:
        raw = f.read()
    if raw != NAME.encode("utf-8"):
        print("entry bytes do not match the name", file=sys.stderr)
        return 1
    back = raw.decode("utf-8")
    if back != NAME or not (1 <= len(back) <= MAX_CHARS) or not back.strip():
        print("entry failed verification", file=sys.stderr)
        return 1
    print(f"{back} ({len(back)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
