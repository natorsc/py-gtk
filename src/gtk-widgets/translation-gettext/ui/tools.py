# -*- coding: utf-8 -*-
"""."""

import pathlib
import subprocess

APP_ID = 'br.com.justcode.Gtk'
LC_MESSAGES = 'LC_MESSAGES'

BASE_DIR = pathlib.Path(__file__).resolve().parent
LOC_DIR = BASE_DIR / 'locale'
if not LOC_DIR.exists():
    LOC_DIR.mkdir(exist_ok=True, parents=True)

POT_FILE = LOC_DIR / f'{APP_ID}.pot'

LANGS = ['pt_BR']
FILES = list(BASE_DIR.rglob('*.blp')) + list(BASE_DIR.rglob('*.py'))


def main() -> None:
    create_pot_file()
    create_po_file()
    update_translations()
    compile_translations()


def create_pot_file() -> None:
    print('[!] Creating POT file [!]')
    output = LOC_DIR / f'{APP_ID}.pot'
    cmd = [
        'xgettext',
        '--from-code=UTF-8',
        '--add-comments',
        '--keyword=_',
        '--keyword=C_:1c,2',
        '-d',
        APP_ID,
        '-o',
        str(output),
    ]
    for file in FILES:
        if not file.name == 'tools.py':
            cmd.append(str(file))

    result = subprocess.run(
        cmd,
        capture_output=True,
        check=True,
        text=True,
    )
    print('Return Code:', result.returncode)
    print('Standard Output:', result.stdout)
    print('Standard Error:', result.stderr)
    print('[!] Done [!]\n')


def create_po_file() -> None:
    print('[!] Creating PO file [!]')
    for lang in LANGS:
        lang_dir = LOC_DIR / lang / LC_MESSAGES
        if not lang_dir.exists():
            lang_dir.mkdir(exist_ok=True, parents=True)
        output = lang_dir / f'{APP_ID}.po'
        if not output.exists():
            result = subprocess.run(
                args=[
                    'msginit',
                    '--no-translator',
                    '-i',
                    str(POT_FILE),
                    '-l',
                    lang,
                    '-o',
                    str(output),
                ],
                capture_output=True,
                check=True,
                text=True,
            )
            print('Return Code:', result.returncode)
            print('Standard Output:', result.stdout)
            print('Standard Error:', result.stderr)
            print('[!] Done [!]\n')


def update_translations() -> None:
    print('[!] Updating the translations, please wait... [!]')

    for po in LOC_DIR.rglob('*.po'):
        if po.is_file() and po.suffix == '.po':
            result = subprocess.run(
                args=['msgmerge', '--update', str(po), str(POT_FILE)],
                capture_output=True,
                check=True,
                text=True,
            )
            print('Return Code:', result.returncode)
            print('Standard Output:', result.stdout)
            print('Standard Error:', result.stderr)

    print('[!] Done [!]\n')


def compile_translations() -> None:
    print('[!] Compiling the translations (*.po -> *.mo), please wait... [!]')
    for po in LOC_DIR.rglob('*.po'):
        if po.is_file() and po.suffix == '.po':
            output = po.parent.joinpath(f'{po.stem}.mo')
            result = subprocess.run(
                args=['msgfmt', po, '-o', output],
                capture_output=True,
                check=True,
                text=True,
            )
            print('Return Code:', result.returncode)
            print('Standard Output:', result.stdout)
            print('Standard Error:', result.stderr)

    print('[!] Done [!]\n')


if __name__ == '__main__':
    main()
