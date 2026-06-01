#!/usr/bin/env python3
"""Additively apply frontmatter (tags / moc / related / title) to first-class notes.
NEVER modifies note body text. Idempotent: skips files already carrying a type/ tag.
Touches only the YAML frontmatter block (insert-before-fence) or prepends a new block."""
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = json.load(open(os.path.join(ROOT, '_kb_build', 'manifest.json'), encoding='utf-8'))

def render_list(key, items, link=False):
    out = [f'{key}:']
    for it in items:
        out.append(f'  - "[[{it}]]"' if link else f'  - {it}')
    return out

def detect_h1(body):
    for line in body.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return None

changed, skipped, errors = [], [], []

for relpath, spec in manifest.items():
    full = os.path.join(ROOT, relpath)
    if not os.path.exists(full):
        errors.append(f'MISSING: {relpath}'); continue
    with open(full, 'r', encoding='utf-8') as f:
        text = f.read()

    new_tags = spec.get('tags', [])
    moc = spec.get('moc', [])
    related = spec.get('related', [])

    has_fm = text.startswith('---\n')
    fm_block = None
    after = None
    if has_fm:
        idx = text.find('\n---', 4)
        if idx == -1:
            errors.append(f'BAD-FM (no closing fence): {relpath}'); continue
        fm_block = text[4:idx]
        after = text[idx+4:]  # everything after the closing '---'

    # Idempotency: already tagged?
    region = fm_block if has_fm else text
    if 'type/' in region:
        skipped.append(relpath); continue

    body_before = after if has_fm else text  # for verification

    if not has_fm:
        # Case A: prepend a fresh frontmatter block
        title = spec.get('title') or detect_h1(text) or os.path.splitext(os.path.basename(relpath))[0]
        block = ['---', f'title: "{title}"']
        block += render_list('tags', new_tags)
        if moc: block += render_list('moc', moc, link=True)
        if related: block += render_list('related', related, link=True)
        block.append('---')
        new_text = '\n'.join(block) + '\n\n' + text
        assert new_text.endswith(text), 'body altered (A)'
    else:
        lines = fm_block.split('\n')
        # locate existing tags: key (list form)
        tags_i = next((i for i, l in enumerate(lines) if re.match(r'^tags:\s*$', l)), None)
        tags_inline_i = next((i for i, l in enumerate(lines) if re.match(r'^tags:\s*\[', l)), None)
        if tags_i is not None:
            # find end of the list (consecutive indented '- ' items)
            j = tags_i + 1
            while j < len(lines) and re.match(r'^\s*-\s+', lines[j]):
                j += 1
            existing = set(re.sub(r'^\s*-\s+', '', l).strip().strip('"') for l in lines[tags_i+1:j])
            additions = [f'  - {t}' for t in new_tags if t not in existing]
            lines[j:j] = additions
        elif tags_inline_i is not None:
            errors.append(f'INLINE-TAGS unhandled: {relpath}'); continue
        else:
            # no tags key -> append a tags block at end of fm
            lines += render_list('tags', new_tags)
        # append moc / related blocks at end of fm (only if not already present)
        joined = '\n'.join(lines)
        if moc and 'moc:' not in joined:
            lines += render_list('moc', moc, link=True)
        if related and 'related:' not in joined:
            lines += render_list('related', related, link=True)
        new_fm = '\n'.join(lines)
        new_text = '---\n' + new_fm + '\n---' + after
        assert new_text.endswith(after), 'body altered (B/C)'

    with open(full, 'w', encoding='utf-8') as f:
        f.write(new_text)
    changed.append(relpath)

print(f'CHANGED: {len(changed)}   SKIPPED(already tagged): {len(skipped)}   ERRORS: {len(errors)}')
for e in errors: print('  !!', e)
print('--- changed files ---')
for c in changed: print('  +', c)
