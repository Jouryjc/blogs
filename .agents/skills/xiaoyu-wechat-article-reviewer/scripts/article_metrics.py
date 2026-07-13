#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def strip_frontmatter(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: article_metrics.py <markdown_file>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).expanduser()
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    raw = path.read_text(encoding="utf-8")
    text = strip_frontmatter(raw)
    no_code = strip_code_blocks(text)

    title_match = re.search(r"^#\s+(.+)$", text, flags=re.M)
    headings = re.findall(r"^(#{2,4})\s+(.+)$", text, flags=re.M)
    links = re.findall(r"\[[^\]]+\]\([^)]+\)|https?://\S+", raw)
    images = re.findall(r"!\[[^\]]*\]\([^)]+\)", raw)
    code_blocks = re.findall(r"```", raw)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", no_code)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", no_code) if p.strip()]

    cta_patterns = [
        r"关注",
        r"回复",
        r"关键词",
        r"领取",
        r"模板",
        r"清单",
        r"转发",
        r"分享",
        r"收藏",
        r"留言",
        r"下一篇",
    ]
    ai_smell_patterns = [
        r"换句话说",
        r"这意味着",
        r"这一步让",
        r"真正",
        r"核心",
        r"本质",
        r"价值就在这里",
        r"值得注意",
        r"总的来说",
        r"不仅如此",
        r"很多人会以为",
        r"这件事",
        r"可以看到",
    ]

    result = {
        "path": str(path),
        "title": title_match.group(1).strip() if title_match else None,
        "chinese_chars_excluding_code": len(chinese_chars),
        "paragraph_count": len(paragraphs),
        "heading_count_h2_to_h4": len(headings),
        "link_count": len(links),
        "image_count": len(images),
        "code_block_count": len(code_blocks) // 2,
        "cta_keyword_hits": sorted({p for p in cta_patterns if re.search(p, no_code)}),
        "ai_smell_hits": sorted({p for p in ai_smell_patterns if re.search(p, no_code)}),
        "warnings": [],
    }

    if len(chinese_chars) > 10000:
        result["warnings"].append("Article is over 10000 Chinese chars; consider splitting unless it is a report.")
    if len(result["cta_keyword_hits"]) < 2:
        result["warnings"].append("CTA/follow-conversion signals are weak.")
    if not images:
        result["warnings"].append("No images found; WeChat technical articles often need at least one visual anchor.")
    if len(headings) < 4:
        result["warnings"].append("Few subheadings; mobile scanning may be weak.")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

