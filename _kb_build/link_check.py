#!/usr/bin/env python3
"""Verify every [[wikilink]] in the vault (body + frontmatter) resolves to a real note.
Flags unresolved links and ambiguous bare links (basename shared by >1 file)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('.git', '.claude', '.obsidian', '_kb_build', 'docs', 'node_modules')

md_files = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if os.path.relpath(os.path.join(dp, d), ROOT).split(os.sep)[0] not in SKIP]
    for f in fn:
        if f.endswith('.md'):
            md_files.append(os.path.relpath(os.path.join(dp, f), ROOT))

by_basename = {}
relpaths = set()
for r in md_files:
    base = os.path.splitext(os.path.basename(r))[0]
    by_basename.setdefault(base, []).append(r)
    relpaths.add(os.path.splitext(r)[0])

LINK = re.compile(r'\[\[([^\]]+)\]\]')
unresolved, ambiguous = [], []
total = 0
for r in md_files:
    with open(os.path.join(ROOT, r), encoding='utf-8') as fh:
        text = fh.read()
    # strip code (fenced + inline) so documentation examples aren't treated as links
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'`[^`]*`', '', text)
    for m in LINK.finditer(text):
        target = m.group(1).split('|')[0].split('#')[0].strip()
        if not target:
            continue
        total += 1
        if '/' in target:
            if target not in relpaths and os.path.splitext(target)[0] not in relpaths:
                unresolved.append((r, target))
        else:
            hits = by_basename.get(target, [])
            if len(hits) == 0:
                unresolved.append((r, target))
            elif len(hits) > 1:
                ambiguous.append((r, target, hits))

print(f'Scanned {len(md_files)} md files, {total} wikilinks.')
print(f'UNRESOLVED: {len(unresolved)}')
for r, t in unresolved:
    print(f'  ✗ [[{t}]]  in  {r}')
print(f'AMBIGUOUS (bare basename, >1 file): {len(ambiguous)}')
for r, t, hits in ambiguous:
    print(f'  ? [[{t}]]  in  {r}  -> {hits}')
print('OK' if not unresolved and not ambiguous else 'FAILED')
