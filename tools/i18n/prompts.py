BATCH_TRANSLATION_SYSTEM = """You analyze Chinese source blog posts and rewrite them into multiple target languages.
This is not literal translation. It is faithful cross-cultural retelling based on the source meaning.
Analyze both the explicit surface meaning and the unspoken internal intent before rewriting.
Respect cross-cultural, religious, social, and publishing conventions of each target language.
Preserve Markdown structure, heading levels, placeholders, code placeholders, URLs, Liquid placeholders, and technical identifiers.
Return only valid YAML. Do not wrap it in Markdown fences. Use YAML block scalars with | for every multi-sentence or Markdown field.
"""


def batch_translation_prompt(protected_body, metadata, target_languages, previous_batch=None, previous_analyses=None):
    language_lines = []
    translation_schema = []
    for lang, lang_config in target_languages.items():
        dialect = lang_config.get("dialect", "none")
        forbidden = ""
        if lang == "ar":
            forbidden = " Must use only Damascus Levantine Arabic; never Modern Standard Arabic and never Saudi dialect."
        language_lines.append(
            f"- {lang}: {lang_config['name']}; dir={lang_config['dir']}; style={lang_config['style']}; dialect={dialect}.{forbidden}"
        )
        translation_schema.append(
            f"  {lang}:\n    title: translated title or null\n    description: |\n      translated description or null\n    excerpt: |\n      translated excerpt or null\n    body: |\n      translated Markdown body"
        )

    return f"""Target languages:
{chr(10).join(language_lines)}

Source front matter fields to rewrite when present:
{metadata}

Previous batch translation cache, if any:
{previous_batch or 'none'}

Previous per-language analysis cache, if any:
{previous_analyses or 'none'}

Protected Chinese Markdown body:
{protected_body}

First produce one shared analysis for the Chinese source post. The analysis must cover source_summary, literal_layer, implicit_layer, cross_cultural_layer, retelling_strategy, terminology_policy, and forbidden_styles.
Then rewrite the post independently for every target language listed above while keeping the shared meaning consistent across languages.
Keep every placeholder exactly unchanged in every translated body.

Return YAML with exactly this structure:
analysis:
  source_summary: |
    ...
  literal_layer: |
    ...
  implicit_layer: |
    ...
  cross_cultural_layer: |
    ...
  retelling_strategy: |
    ...
  terminology_policy: |
    ...
  forbidden_styles: |
    ...
translations:
{chr(10).join(translation_schema)}
"""
