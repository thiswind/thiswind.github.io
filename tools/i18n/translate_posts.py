import argparse
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
from prompts import BATCH_TRANSLATION_SYSTEM, batch_translation_prompt

TRANSLATABLE_STATUSES = {"pending", "missing", "stale", "failed"}
TRANSLATABLE_FRONTMATTER_FIELDS = ("title", "description", "excerpt")
BATCH_DIR = ANALYSIS_DIR / "batches"


def read_text(path: Path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def write_yaml(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path.read_text(encoding="utf-8")


def parse_batch_response(content: str):
    payload = yaml.safe_load(content)
    if not isinstance(payload, dict):
        raise ValueError("batch translation response must be a YAML mapping")
    if not isinstance(payload.get("analysis"), dict):
        raise ValueError("batch translation response must contain an analysis mapping")
    if not isinstance(payload.get("translations"), dict):
        raise ValueError("batch translation response must contain a translations mapping")
    return payload


def target_languages(source_record, only_lang=None):
    targets = {}
    for lang, translation in source_record.get("translations", {}).items():
        if only_lang and lang != only_lang:
            continue
        if translation.get("locked") or translation.get("status") not in TRANSLATABLE_STATUSES:
            continue
        targets[lang] = translation
    return targets


def previous_analyses_for(targets):
    analyses = {}
    for lang, translation in targets.items():
        analysis = read_text(ROOT / translation["analysis_path"])
        if analysis:
            analyses[lang] = analysis
    return analyses or None


def write_translation(source_record, source_post, source_hash, lang, translation, translated_payload, analysis_payload):
    if not isinstance(translated_payload, dict) or not translated_payload.get("body"):
        raise ValueError(f"translation for {lang} must be a mapping with a body field")

    translated_body = restore_markdown(str(translated_payload["body"]), write_translation.protected)
    metadata = build_translated_metadata(source_post, lang, LANGUAGES[lang], Path(source_record["source_path"]), source_hash)
    for field in TRANSLATABLE_FRONTMATTER_FIELDS:
        if field in source_post.metadata:
            metadata[field] = translated_payload.get(field) or source_post.metadata[field]
    metadata["translation_updated_at"] = datetime.now(timezone.utc).isoformat()

    translated_post = frontmatter.Post(translated_body, **metadata)
    dump_post(ROOT / translation["path"], translated_post)
    write_yaml(ROOT / translation["analysis_path"], analysis_payload)
    translation.update({
        "status": "active",
        "source_hash": source_hash,
        "translation_hash": sha256_text(frontmatter.dumps(translated_post)),
        "model": LLM_MODEL,
        "updated_at": metadata["translation_updated_at"],
    })
    translation.pop("error", None)


def translate_source(manifest, source_id, only_lang=None):
    source_record = manifest["sources"][source_id]
    targets = target_languages(source_record, only_lang)
    if not targets:
        return []

    source_path = ROOT / source_record["source_path"]
    source_hash = sha256_file(source_path)
    source_post = load_post(source_path)
    protected_body, protected = protect_markdown(source_post.content)
    write_translation.protected = protected

    frontmatter_fields = {field: source_post.metadata.get(field) for field in TRANSLATABLE_FRONTMATTER_FIELDS if field in source_post.metadata}
    target_configs = {lang: LANGUAGES[lang] for lang in targets}
    batch_path = BATCH_DIR / f"{source_id}.yml"

    print(f"batch translating {source_id} -> {', '.join(targets)}", flush=True)
    messages = [
        {"role": "system", "content": BATCH_TRANSLATION_SYSTEM},
        {"role": "user", "content": batch_translation_prompt(
            protected_body,
            frontmatter_fields,
            target_configs,
            read_text(batch_path),
            previous_analyses_for(targets),
        )},
    ]
    response = complete(messages, temperature=0.2)
    try:
        batch_payload = parse_batch_response(response)
    except yaml.YAMLError as exc:
        response = complete(messages + [
            {"role": "assistant", "content": response},
            {"role": "user", "content": f"The YAML above is invalid: {exc}. Return the same content as strictly valid YAML only. Use block scalars with | for every Markdown body, description, excerpt, and analysis field."},
        ], temperature=0.1)
        batch_payload = parse_batch_response(response)
    translations = batch_payload["translations"]
    analysis_payload = batch_payload["analysis"]
    write_yaml(batch_path, batch_payload)

    failures = []
    for lang, translation in targets.items():
        try:
            write_translation(source_record, source_post, source_hash, lang, translation, translations.get(lang), analysis_payload)
            print(f"translated {source_id} -> {lang}", flush=True)
        except Exception as exc:
            translation["status"] = "failed"
            translation["error"] = str(exc)
            failures.append(f"{source_id}:{lang}: {exc}")
    return failures


def translate_all(only_lang=None):
    manifest = load_manifest()
    failures = []
    for source_id, source_record in manifest.get("sources", {}).items():
        if source_record.get("source_status") != "active":
            continue
        try:
            failures.extend(translate_source(manifest, source_id, only_lang))
        except Exception as exc:
            for lang, translation in target_languages(source_record, only_lang).items():
                translation["status"] = "failed"
                translation["error"] = str(exc)
                failures.append(f"{source_id}:{lang}: {exc}")
        save_manifest(manifest)
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=sorted(LANGUAGES.keys()))
    args = parser.parse_args()
    translate_all(args.lang)
