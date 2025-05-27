# -*- coding: utf-8 -*-
"""."""

import pathlib
import subprocess
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parent

compiler = 'blueprint-compiler'

platform = sys.platform
if platform == 'win32':
    compiler = 'python3 C:\\msys64\\mingw64\\bin\\blueprint-compiler'


def blp_to_ui(file):
    print('[[!] Converting (blp -> ui), please wait... [!]')
    output = file.parent.joinpath(f'{file.stem}.ui')
    # try:
    #     subprocess.call(args=[compiler, 'compile', '--output', output, file])
    # except Exception as error:
    #     print(f'[X] Fail: {error}')

    result = subprocess.run(
        args=[compiler, 'compile', '--output', output, file],
        capture_output=True,
        check=True,
        text=True,
    )

    print(f'Return Code: {result.returncode}.')
    # print(f'Standard Output: {result.stdout}.')
    # print(f'Standard Error: {result.stderr}.')
    print('[!] Conversion finished [!]')


if __name__ == '__main__':
    pass
