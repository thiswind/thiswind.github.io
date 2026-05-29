import frontmatter

TRANSLATABLE_FIELDS = {"title", "description", "excerpt"}
PRESERVED_FIELDS = {"layout", "date", "categories", "tags", "author", "slug", "source_id", "math"}


def load_post(path):
    return frontmatter.loads(path.read_text(encoding="utf-8"))


def dump_post(path, post):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dumps(post), encoding="utf-8")


def build_translated_metadata(source_post, lang, lang_config, source_path, source_hash):
    metadata = {}
    for key in PRESERVED_FIELDS:
        if key in source_post.metadata:
            metadata[key] = source_post.metadata[key]
    metadata.update({
        "layout": source_post.metadata.get("layout", "post"),
        "lang": lang,
        "dir": lang_config["dir"],
        "source_lang": "zh",
        "source_path": str(source_path),
        "source_hash": source_hash,
        "translated_by": "llm",
        "translation_model": "gpt-5.4-nano",
    })
    if "dialect" in lang_config:
        metadata["dialect"] = lang_config["dialect"]
    return metadata
