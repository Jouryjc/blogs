#!/usr/bin/env python3
"""Scan the repo and classify every .md as a first-class note (with type) or attachment,
per the selection rules in the approved spec. Outputs JSON + a human summary."""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories never scanned
SKIP_DIR_PREFIXES = ('.git', '.claude', '.obsidian', 'docs', '_kb_build', 'node_modules')

# Path segments that mark a .md as an attachment (production artifact)
ATTACH_SEGMENTS = {'illustrations', 'cover-image', 'imgs', 'prompts'}
# Filename patterns that mark a .md as an attachment
ATTACH_NAME_RE = re.compile(r'(^outline\.md$|^system-prompt\.md$|^prompt-.*\.md$|^cover.*\.md$)')

def rel(p):
    return os.path.relpath(p, ROOT)

def read_head(path, n=4000):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read(n)
    except Exception as e:
        return ''

def parse_frontmatter(text):
    """Return (has_fm, dict_of_simple_keys, raw_block_or_None). Text-only, no reserialize."""
    if not text.startswith('---\n'):
        return False, {}, None
    end = text.find('\n---', 4)
    if end == -1:
        return False, {}, None
    block = text[4:end]
    keys = {}
    for line in block.splitlines():
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):(.*)$', line)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return True, keys, block

def first_h1(text):
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return None

def is_attachment(relpath, name):
    segs = relpath.split(os.sep)
    if any(s in ATTACH_SEGMENTS for s in segs[:-1]):
        return True
    if ATTACH_NAME_RE.match(name):
        return True
    return False

def classify_type(relpath):
    segs = relpath.split(os.sep)
    if segs[0] == 'wiki':
        return 'moc'
    if segs[0] == 'reports':
        return 'report'
    if relpath.startswith('raw/news/'):
        return 'news'
    if 'x-to-markdown' in segs:
        return 'thread'
    if segs[0] == 'raw':
        return 'source'
    if segs[0] in ('outputs', 'post-to-wechat', 'output'):
        # post-to-wechat: only <slug>/<slug>.md is the article
        if segs[0] == 'post-to-wechat':
            stem = os.path.splitext(segs[-1])[0]
            parent = segs[-2] if len(segs) >= 2 else ''
            if stem != parent:
                # supporting file: source notes become sources, others are attachments
                return 'source' if 'source' in segs else None
        return 'article'
    return None

records = []
attachments = []
unclassified = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not any(
        rel(os.path.join(dirpath, d)).split(os.sep)[0] == p for p in SKIP_DIR_PREFIXES)]
    for fn in filenames:
        if not fn.endswith('.md'):
            continue
        full = os.path.join(dirpath, fn)
        r = rel(full)
        if r.split(os.sep)[0] in SKIP_DIR_PREFIXES:
            continue
        if r in ('AGENTS.md', 'AGETNS.md', 'README.md'):
            continue  # schema/readme docs, not notes
        if r == 'wiki/xiaoyu-2.0-rewrite-prompt.md':
            attachments.append(r); continue
        if is_attachment(r, fn):
            attachments.append(r); continue
        t = classify_type(r)
        if t is None:
            unclassified.append(r); continue
        text = read_head(full)
        has_fm, keys, _ = parse_frontmatter(text)
        records.append({
            'path': r,
            'basename': os.path.splitext(fn)[0],
            'type': t,
            'has_fm': has_fm,
            'has_tags': 'tags' in keys,
            'title': keys.get('title', '').strip('"') or (first_h1(text) or ''),
            'fm_keys': sorted(keys.keys()),
        })

records.sort(key=lambda x: (x['type'], x['path']))
out = {'first_class': records, 'attachments': sorted(attachments), 'unclassified': sorted(unclassified)}
with open(os.path.join(ROOT, '_kb_build', 'inventory.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# Human summary
from collections import Counter
c = Counter(r['type'] for r in records)
print('=== FIRST-CLASS NOTES BY TYPE ===')
for t in ['article','source','report','news','thread']:
    print(f'  {t}: {c.get(t,0)}')
print(f'  TOTAL first-class: {len(records)}')
print(f'  attachments: {len(attachments)}')
print(f'  unclassified: {len(unclassified)}')
print()
# basename collisions among first-class
bn = Counter(r['basename'] for r in records)
dupes = {k:v for k,v in bn.items() if v>1}
print('=== BASENAME COLLISIONS (first-class) ===')
print('  ', dupes if dupes else 'none')
print()
print('=== FIRST-CLASS LIST ===')
for r in records:
    flag = '' if r['has_fm'] else '  [NO-FM]'
    tg = '' if r['has_tags'] else ' [no-tags]'
    print(f"  [{r['type']:<7}] {r['path']}{flag}{tg}")
print()
print('=== UNCLASSIFIED (review!) ===')
for u in unclassified:
    print('  ', u)
