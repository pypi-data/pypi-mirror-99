import subprocess, re, sys
from subprocess import DEVNULL
from typing import Optional, Any
import xml.etree.ElementTree as ET

def query_yn(question: str) -> bool:
    while True:
        print(question + ' [y/n]', end=' ')
        choice = input().lower()
        if choice == 'y' or choice == 'yes':
            return True
        elif choice == 'n' or choice == 'no':
            return False

def apply_vars(text: str, vars: dict[str,Any]) -> str:
    for k, v in vars.items():
        text = text.replace('{%s}' % k, str(v))
    return text

def cmd_exists(args: list[str]) -> bool:
    try:
        subprocess.call(args, stdout=DEVNULL, stderr=DEVNULL)
        return True
    except FileNotFoundError:
        return False

def flatpak_app_installed(app_id: str) -> bool:
    if not cmd_exists(['flatpak', '--help']):
        return False
    res = subprocess.check_call(['flatpak', 'info', app_id], stdout=DEVNULL, stderr=DEVNULL)
    return res == 0

def inkscape_run(args: list[str]) -> int:
    if cmd_exists(['inkscape', '--help']):
        return subprocess.check_call(['inkscape', *args])
    elif flatpak_app_installed('org.inkscape.Inkscape'):
        return subprocess.check_call(['flatpak', 'run', 'org.inkscape.Inkscape', *args])
    else:
        raise FileNotFoundError('You need to install inkscape (either native or flatpak)')

def pattern_get(pattern: str, string: str, group: int) -> str:
    match = re.search(pattern, string)
    if not match: raise ValueError(f'No match found by "{pattern}"')
    g = match.group(group)
    if g is None: raise ValueError(f'Match group {group} is None')
    return g

def number_of_pages(filename: str) -> int:
    res = subprocess.check_output(['pdfinfo', filename]).decode(sys.stdout.encoding)
    match = re.search(r'^\s*Pages:\s*(\d+)', res, flags=re.MULTILINE)
    return int(match.group(1))

def parse_range(text: str, num_pages: int) -> set[int]:
    tokens: list[str] = text.split()
    if not tokens: return set()
    if len(tokens) == 1 and tokens[0] == 'all': return {p for p in range(1, num_pages+1)}
    pages: set[int] = set()
    for token in tokens:
        match = re.search(r'^(\d+)-(\d+)$', token)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            pages.update([p for p in range(start, end+1)])
            continue
        match = re.search(r'^(\d+)$', token)
        if match:
            p = int(match.group(1))
            pages.add(p)
            continue
        raise ValueError(f'Invalid page range: {text}')
    return pages

def find_elements_by_class(tree: ET.ElementTree, cls: str) -> ET.Element:
    result = []
    for el in tree.iter():
        if cls in el.get('class', ''):
            result.append(el)
    return result

def px(length: str) -> float:
    match = re.search(r'([0-9.]+)\s*([a-zA-Z%]*)', length)
    num = match.group(1)
    unit = match.group(2)
    if   unit == 'cm':
        return float(num) * 37.795
    elif unit == 'mm':
        return float(num) * 3.7795
    elif unit == 'in':
        return float(num) * 96.0
    elif unit == 'pc':
        return float(num) * 16.0
    elif unit == 'pt':
        return float(num) * 1.333333333
    elif unit == 'px' or unit == '':
        return float(num)
    else:
        raise ValueError(f'Invalid length: {length}')
