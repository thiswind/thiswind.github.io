from datetime import datetime, timezone
from pathlib import Path

import frontmatter
import yaml

from config import ANALYSIS_DIR, LLM_MODEL, ROOT
from frontmatter_io import build_translated_metadata, dump_post, load_post
from languages import LANGUAGES
from llm_client import complete
from manifest import load_manifest, save_manifest, sha256_file, sha256_text
from markdown_protect import protect_markdown, restore_markdown
from prompts import ANALYSIS_SYSTEM, TRANSLATION_SYSTEM, analysis_prompt, translation_prompt

TRANSLATABLE_STATUSES = {"pending", "missing", "stale", "failed"}


def read_previous_analysis(path: Path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def write_analysis(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    parsed = yaml.safe_load(content)
    if not isinstance(parsed, dict):
        raise ValueError("analysis response must be a YAML mapping")
    path.write_text(yaml.safe_dump(parsed, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path.read_text(encoding="utf-8")


def translate_frontmatter_field(value, lang, lang_config, analysis_yaml):
    if not value:
        return value
    result = complete([
        {"role": "system", "content": TRANSLATION_SYSTEM},
        {"role": "user", "content": f"Target language: {lang_config['name']} ({lang}).\nTarget style: {lang_config['style']}\nAnalysis:\n{analysis_yaml}\n\nRewrite this front matter field naturally and return only the rewritten text:\n{value}"},
    ])
    return result.strip().strip('"')


def translate_one(manifest, source_id, lang, translation):
    source_record = manifest["sources"][source_id]
    source_path = ROOT / source_record["source_path"]
    target_path = ROOT / translation["path"]
    lang_config = LANGUAGES[lang]
    source_hash = sha256_file(source_path)
    source_post = load_post(source_path)
    previous_analysis = read_previous_analysis(ROOT / translation["analysis_path"])

    analysis = complete([
        {"role": "system", "content": ANALYSIS_SYSTEM},
        {"role": "user", "content": analysis_prompt(source_post.content, dict(source_post.metadata), lang, lang_config, previous_analysis)},
    ])
    analysis_yaml = write_analysis(ROOT / translation["analysis_path"], analysis)

    protected_body, protected = protect_markdown(source_post.content)
    translated_body = complete([
        {"role": "system", "content": TRANSLATION_SYSTEM},
        {"role": "user", "content": translation_prompt(protected_body, analysis_yaml, lang, lang_config)},
    ], temperature=0.2)
    translated_body = restore_markdown(translated_body, protected)

    metadata = build_translated_metadata(source_post, lang, lang_config, Path(source_record["source_path"]), source_hash)
    for field in ("title", "description", "excerpt"):
        if field in source_post.metadata:
            metadata[field] = translate_frontmatter_field(source_post.metadata[field], lang, lang_config, analysis_yaml)
    metadata["translation_updated_at"] = datetime.now(timezone.utc).isoformat()

    translated_post = frontmatter.Post(translated_body, **metadata)
    dump_post(target_path, translated_post)
    translation.update({
        "status": "active",
        "source_hash": source_hash,
        "translation_hash": sha256_text(frontmatter.dumps(translated_post)),
        "model": LLM_MODEL,
        "updated_at": metadata["translation_updated_at"],
    })


def translate_all():
    manifest = load_manifest()
    failures = []
    for source_id, source_record in manifest.get("sources", {}).items():
        if source_record.get("source_status") != "active":
            continue
        for lang, translation in source_record.get("translations", {}).items():
            if translation.get("locked") or translation.get("status") not in TRANSLATABLE_STATUSES:
                continue
            try:
                translate_one(manifest, source_id, lang, translation)
                save_manifest(manifest)
                print(f"translated {source_id} -> {lang}")
            except Exception as exc:
                translation["status"] = "failed"
                translation["error"] = str(exc)
                failures.append(f"{source_id}:{lang}: {exc}")
                save_manifest(manifest)
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    translate_all()
