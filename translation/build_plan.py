"""Build the translation plan: source->target manifest and word-balanced batches.

Outputs (all under translation/):
  documents.json  - [{"source", "target", "words", "title"}, ...]
  titles_en.json  - {"<source rel path>": "<document title>"}
  batches.json    - [{"id": "b001", "files": [<source>], "words": N}, ...]

Source paths are relative to the repository root and use forward slashes.
Target paths live under zh/:
  en/foo/bar.adoc            -> zh/foo/bar.adoc
  README.adoc                -> zh/README.adoc
  attachments/x/README.adoc  -> zh/attachments/x/README.adoc
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "en"
ATTACHMENTS = ROOT / "attachments"
ROOT_DOCS = ["README.adoc", "CONTRIBUTING.adoc", "CODE_OF_CONDUCT.adoc", "CONTRIBUTORS.adoc"]

MAX_WORDS = 6000
MAX_FILES = 10

TITLE_RE = re.compile(r"^(={1,3})\s+(.+?)\s*$")


def document_title(text: str) -> str:
    for line in text.splitlines():
        m = TITLE_RE.match(line)
        if m:
            return m.group(2)
    return ""


def target_for(source: str) -> str:
    if source.startswith("en/"):
        return "zh/" + source[len("en/"):]
    return "zh/" + source


def main() -> None:
    sources: list[str] = []
    for name in ROOT_DOCS:
        if (ROOT / name).exists():
            sources.append(name)
    for path in sorted(EN.rglob("*.adoc")):
        sources.append(path.relative_to(ROOT).as_posix())
    for path in sorted(ATTACHMENTS.rglob("*.adoc")):
        sources.append(path.relative_to(ROOT).as_posix())
    sources.sort(key=lambda p: (p.startswith("en/"), p))

    documents = []
    titles: dict[str, str] = {}
    for rel in sources:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        title = document_title(text)
        titles[rel] = title
        documents.append(
            {
                "source": rel,
                "target": target_for(rel),
                "words": len(text.split()),
                "title": title,
            }
        )

    words = {d["source"]: d["words"] for d in documents}

    out = ROOT / "translation"
    out.mkdir(exist_ok=True)
    (out / "titles_en.json").write_text(
        json.dumps(titles, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "documents.json").write_text(
        json.dumps(documents, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    batches: list[dict] = []
    current: list[str] = []
    current_words = 0

    def flush() -> None:
        nonlocal current, current_words
        if current:
            batches.append(
                {"id": f"b{len(batches) + 1:03d}", "files": current, "words": current_words}
            )
            current = []
            current_words = 0

    for rel in sources:
        w = words[rel]
        if current and (current_words + w > MAX_WORDS or len(current) >= MAX_FILES):
            flush()
        current.append(rel)
        current_words += w
        if w >= MAX_WORDS:
            flush()
    flush()

    (out / "batches.json").write_text(
        json.dumps(batches, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    batch_dir = out / "batches"
    if batch_dir.exists():
        for stale in batch_dir.glob("*.json"):
            stale.unlink()
    batch_dir.mkdir(exist_ok=True)
    doc_by_source = {d["source"]: d for d in documents}
    for batch in batches:
        payload = {
            "id": batch["id"],
            "words": batch["words"],
            "files": [
                {
                    "source": src,
                    "target": doc_by_source[src]["target"],
                    "words": doc_by_source[src]["words"],
                    "title": doc_by_source[src]["title"],
                }
                for src in batch["files"]
            ],
        }
        (batch_dir / f"{batch['id']}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"documents: {len(documents)}")
    print(f"total words: {sum(words.values())}")
    print(f"batches: {len(batches)}")


if __name__ == "__main__":
    main()
