"""Structural verifier for the Chinese translation.

Checks that each zh/ file is a faithful structural mirror of its en/ source:
  1. literal/code blocks are byte-identical (after trailing-space normalization)
  2. xref / link / image / include targets appear in the same order
  3. [[anchor]] ids match as a set
  4. heading count and level sequence match
  5. attribute lines (":name: value") match
  6. no untranslated full-line English prose remains
  7. the target file exists

Usage:
  python translation/verify.py                 # verify every translated document
  python translation/verify.py --file en/00_Introduction.adoc
  python translation/verify.py --missing       # list documents not yet translated
  python translation/verify.py --batch b003    # verify one batch
  python translation/verify.py --json          # machine-readable summary
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSLATION = ROOT / "translation"

LITERAL_DELIMS = {"----", "....", "++++", "////"}
PROSE_DELIMS = {"====", "****", "____", "--", "|==="}
COMMENT_PREFIX = "//"

DIRECTIVE_RULES = [
    ("xref", re.compile(r"xref:([^\[\s]+)\[")),
    ("link", re.compile(r"(?<![\w/])link:([^\[\s]+)\[")),
    ("image", re.compile(r"image::?([^\[\s]+)\[")),
    ("include", re.compile(r"include::([^\[\s]+)\[")),
]
ANCHOR_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^(={1,6})\s+\S")
ATTR_RE = re.compile(r"^:([A-Za-z0-9_][A-Za-z0-9_-]*):\s*(.*)$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
URL_RE = re.compile(r"https?://\S+?\[[^\]]*\]|https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def read_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]


def split_blocks(lines: list[str]):
    """Split into (kind, payload) segments.

    kind is 'literal', 'prose_block' or 'line'.
    For literal blocks payload is the list of inner lines; for prose blocks only
    the delimiter type is recorded; for normal lines payload is the line itself.
    """
    segments = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        token = line.strip()
        if token in LITERAL_DELIMS or token in PROSE_DELIMS:
            delim = token
            kind = "literal" if delim in LITERAL_DELIMS else "prose_block"
            inner = []
            j = i + 1
            closed = False
            while j < n:
                if lines[j].strip() == delim or (
                    delim in {"--", "|==="} and lines[j].strip().startswith(delim)
                ):
                    closed = True
                    break
                inner.append(lines[j])
                j += 1
            segments.append((kind, delim, inner))
            i = j + 1 if closed else n
        else:
            segments.append(("line", "", [line]))
            i += 1
    return segments


def collect_directives(lines: list[str]):
    found = []
    for line in lines:
        for name, regex in DIRECTIVE_RULES:
            for m in regex.finditer(line):
                found.append((name, m.group(1).strip()))
    return found


def collect_anchors(lines: list[str]) -> set[str]:
    out = set()
    for line in lines:
        for m in ANCHOR_RE.finditer(line):
            out.add(m.group(1).strip())
    return out


def collect_headings(lines: list[str]):
    out = []
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            out.append(len(m.group(1)))
    return out


def collect_attributes(lines: list[str]):
    out = []
    for line in lines:
        m = ATTR_RE.match(line)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def literal_blocks(lines: list[str]):
    return [
        (delim, inner)
        for kind, delim, inner in split_blocks(lines)
        if kind == "literal" and delim in {"----", "....", "++++"}
    ]


def untranslated_prose(lines: list[str]) -> list[int]:
    """Line numbers of prose lines that still look like full English sentences."""
    hits = []
    for idx, (kind, delim, payload) in enumerate(split_blocks(lines)):
        if kind != "line":
            continue
        line = payload[0]
        stripped = line.strip()
        if not stripped or stripped.startswith(COMMENT_PREFIX):
            continue
        if DIRECTIVE_RULES and any(r.search(line) for _, r in DIRECTIVE_RULES):
            continue
        if ATTR_RE.match(line):
            continue
        if CJK_RE.search(line):
            continue
        # headers are checked structurally and often contain product names only
        if stripped.startswith("="):
            continue
        # ignore pure asciidoc structure such as list bullets or table separators,
        # inline code spans, and link titles that are legitimately kept in English
        core = INLINE_CODE_RE.sub(" ", stripped)
        core = URL_RE.sub(" ", core).lstrip("*.-0123456789. \t")
        words = WORD_RE.findall(core)
        # require a few lowercase-starting words so product-name lists are not flagged
        lowercase = [w for w in words if w[:1].islower()]
        if len(words) >= 4 and len(lowercase) >= 3:
            hits.append(idx)
    return hits


def check_pair(source_rel: str, target_rel: str) -> dict:
    src_path = ROOT / source_rel
    tgt_path = ROOT / target_rel
    problems: list[str] = []

    if not tgt_path.exists():
        return {"source": source_rel, "target": target_rel, "status": "MISSING", "problems": ["target missing"]}

    src_lines = read_lines(src_path)
    tgt_lines = read_lines(tgt_path)

    src_blocks = literal_blocks(src_lines)
    tgt_blocks = literal_blocks(tgt_lines)
    if len(src_blocks) != len(tgt_blocks):
        problems.append(f"literal block count {len(tgt_blocks)} != {len(src_blocks)}")
    for k, ((sdelim, sinner), (tdelim, tinner)) in enumerate(zip(src_blocks, tgt_blocks)):
        if sdelim != tdelim:
            problems.append(f"block #{k + 1} delimiter {tdelim!r} != {sdelim!r}")
        if sinner != tinner:
            first = next(
                (i for i, (a, b) in enumerate(zip(sinner, tinner)) if a != b),
                min(len(sinner), len(tinner)),
            )
            problems.append(f"block #{k + 1} content differs at line {first + 1}")

    src_dirs = collect_directives(src_lines)
    tgt_dirs = collect_directives(tgt_lines)
    if src_dirs != tgt_dirs:
        missing = [d for d in src_dirs if d not in tgt_dirs]
        extra = [d for d in tgt_dirs if d not in src_dirs]
        if missing:
            problems.append(f"lost directives: {missing[:5]}")
        elif extra:
            problems.append(f"extra directives: {extra[:5]}")
        else:
            problems.append("directive order changed")

    if collect_anchors(src_lines) != collect_anchors(tgt_lines):
        problems.append("anchor ids differ")

    src_heads = collect_headings(src_lines)
    tgt_heads = collect_headings(tgt_lines)
    if src_heads != tgt_heads:
        problems.append(f"heading structure differs (en={src_heads} zh={tgt_heads})")

    if collect_attributes(src_lines) != collect_attributes(tgt_lines):
        problems.append("attribute lines differ")

    leftovers = untranslated_prose(tgt_lines)
    if leftovers:
        first = split_blocks(tgt_lines)[leftovers[0]][2][0].strip()
        problems.append(
            f"{len(leftovers)} untranslated prose line(s), first: {first[:70]!r}"
        )

    return {
        "source": source_rel,
        "target": target_rel,
        "status": "PASS" if not problems else "FAIL",
        "problems": problems,
    }


def load_documents() -> list[dict]:
    path = TRANSLATION / "documents.json"
    if not path.exists():
        print("documents.json missing; run: python translation/build_plan.py", file=sys.stderr)
        sys.exit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="source path, e.g. en/00_Introduction.adoc")
    parser.add_argument("--batch", help="batch id, e.g. b003")
    parser.add_argument("--missing", action="store_true", help="list untranslated documents")
    parser.add_argument("--summary", action="store_true", help="progress grouped by course")
    parser.add_argument("--json", action="store_true", help="json output")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args()

    documents = load_documents()
    by_source = {d["source"]: d for d in documents}

    if args.missing:
        missing = [d["source"] for d in documents if not (ROOT / d["target"]).exists()]
        if args.json:
            print(json.dumps(missing, ensure_ascii=False, indent=2))
        else:
            print(f"{len(missing)} / {len(documents)} documents not translated yet")
            for rel in missing:
                print(f"  {rel}")
        return 0

    if args.summary:
        groups: dict[str, dict[str, int]] = {}
        for d in documents:
            rel = d["source"]
            parts = rel.split("/")
            if parts[0] == "en":
                key = parts[1] if len(parts) > 2 else "核心教程（en 根目录）"
            elif parts[0] == "attachments":
                key = "附件 README"
            else:
                key = "仓库根级文档"
            g = groups.setdefault(key, {"total": 0, "translated": 0, "pass": 0})
            g["total"] += 1
            if (ROOT / d["target"]).exists():
                g["translated"] += 1
                if check_pair(d["source"], d["target"])["status"] == "PASS":
                    g["pass"] += 1
        for key in sorted(groups):
            g = groups[key]
            print(f"{key:38s} {g['pass']:4d} PASS / {g['translated']:4d} 已译 / {g['total']:4d} 总数")
        totals = {
            k: sum(g[k] for g in groups.values()) for k in ("total", "translated", "pass")
        }
        print("-" * 72)
        print(f"{'合计':36s} {totals['pass']:4d} PASS / {totals['translated']:4d} 已译 / {totals['total']:4d} 总数")
        return 0 if totals["pass"] == totals["total"] else 1

    if args.file:
        if args.file not in by_source:
            print(f"unknown document: {args.file}", file=sys.stderr)
            return 2
        targets = [by_source[args.file]]
    elif args.batch:
        batches = json.loads((TRANSLATION / "batches.json").read_text(encoding="utf-8"))
        batch = next((b for b in batches if b["id"] == args.batch), None)
        if not batch:
            print(f"unknown batch: {args.batch}", file=sys.stderr)
            return 2
        targets = [by_source[f] for f in batch["files"]]
    else:
        targets = [d for d in documents if (ROOT / d["target"]).exists()]

    results = [check_pair(d["source"], d["target"]) for d in targets]
    failed = [r for r in results if r["status"] != "PASS"]

    if args.json:
        print(json.dumps({"checked": len(results), "failed": len(failed), "results": results}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if r["status"] == "PASS" and args.quiet:
                continue
            print(f"[{r['status']}] {r['target']}")
            for p in r["problems"]:
                print(f"    - {p}")
        print(f"\nchecked={len(results)} pass={len(results) - len(failed)} fail={len(failed)}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
