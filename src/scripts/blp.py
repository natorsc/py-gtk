# -*- coding: utf-8 -*-
"""."""


import subprocess
import sys

compiler = [
    sys.executable,
    r"C:\msys64\ucrt64\bin\blueprint-compiler"
]


def blp_to_ui(file):
    print("[[!] Converting (blp -> ui), please wait... [!]")

    output = file.parent / f"{file.stem}.ui"

    cmd = [
        *compiler,
        "compile",
        "--output",
        str(output),
        str(file),
    ]

    print(cmd)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("blueprint-compiler failed")

    print("[!] Conversion finished [!]")


if __name__ == "__main__":
    pass
