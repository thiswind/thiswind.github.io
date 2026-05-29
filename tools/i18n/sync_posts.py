from datetime import datetime, timezone
from pathlib import Path

from config import ANALYSIS_DIR, ROOT, SOURCE_POSTS_DIR, TARGET_LANGS
from frontmatter_io import load_post
from languages import LANGUAGES
from manifest import load_manifest, save_manifest, sha256_file


def source_id_for(path: Path, post) -> str:
    return post.metadata.get("source_id") or path.stem


def target_path_for(source_path: Path, lang: str) -> Path:
    return ROOT / LANGUAGES[lang]["collection_dir"] / source_path.name


def is_locked(path: Path, translation_record: dict) -> bool:
    if translation_record.get("locked"):
        return True
    if not path.exists():
        return False
    post = load_post(path)
    return bool(post.metadata.get("translation_locked"))


def sync():
    manifest = load_manifest()
    sources = manifest.setdefault("sources", {})
    current_source_ids = set()

    for source_path in sorted(SOURCE_POSTS_DIR.glob("*.md")):
        post = load_post(source_path)
        source_id = source_id_for(source_path, post)
        current_source_ids.add(source_id)
        source_hash = sha256_file(source_path)
        rel_source_path = source_path.relative_to(ROOT).as_posix()
        record = sources.setdefault(source_id, {
            "source_path": rel_source_path,
            "source_hash": source_hash,
            "source_status": "active",
            "translations": {},
        })
        old_hash = record.get("source_hash")
        changed = old_hash != source_hash
        record.update({
            "source_path": rel_source_path,
            "source_hash": source_hash,
            "source_status": "active",
            "date": str(post.metadata.get("date", "")),
            "title": str(post.metadata.get("title", "")),
        })

        for lang in TARGET_LANGS:
            target_path = target_path_for(source_path, lang)
            rel_target_path = target_path.relative_to(ROOT).as_posix()
            analysis_path = ANALYSIS_DIR / source_id / f"{lang}.yml"
            translation = record.setdefault("translations", {}).setdefault(lang, {})
            locked = is_locked(target_path, translation)
            target_exists = target_path.exists()
            status = translation.get("status", "pending")
            if not target_exists:
                status = "missing"
            elif changed and not locked:
                status = "stale"
            elif status in {"pending", "missing", "stale", "failed"} and target_exists and not changed:
                status = "active"
            translation.update({
                "path": rel_target_path,
                "source_hash": source_hash,
                "status": status,
                "analysis_path": analysis_path.relative_to(ROOT).as_posix(),
                "locked": locked,
            })
            if "dialect" in LANGUAGES[lang]:
                translation["dialect"] = LANGUAGES[lang]["dialect"]

    for source_id, record in sources.items():
        if source_id in current_source_ids or record.get("source_status") == "deleted":
            continue
        record["source_status"] = "deleted"
        record["deleted_at"] = datetime.now(timezone.utc).isoformat()
        for lang, translation in record.get("translations", {}).items():
            translation["status"] = "deleted"

    save_manifest(manifest)


if __name__ == "__main__":
    sync()
