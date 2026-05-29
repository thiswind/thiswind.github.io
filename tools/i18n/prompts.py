ANALYSIS_SYSTEM = """You analyze Chinese source blog posts before cross-cultural rewriting.
Return only valid YAML. Do not wrap it in Markdown fences.
Analyze both the explicit surface meaning and the unspoken internal intent.
Respect cross-cultural, religious, social, and publishing conventions of the target language.
"""

TRANSLATION_SYSTEM = """You rewrite Chinese blog posts into the target language after reading an analysis report.
This is not literal translation. It is faithful cross-cultural retelling based on the source meaning.
Preserve Markdown structure, heading levels, placeholders, code placeholders, URLs, Liquid placeholders, and technical identifiers.
Return only the translated Markdown body, without YAML front matter.
"""


def analysis_prompt(source_body, metadata, lang, lang_config, previous_analysis=None):
    dialect = lang_config.get("dialect", "")
    forbidden = ""
    if lang == "ar":
        forbidden = "Arabic must be Damascus Levantine dialect. Do not use Modern Standard Arabic. Do not use Saudi dialect."
    return f"""Target language: {lang_config['name']} ({lang}).
Target writing direction: {lang_config['dir']}.
Target style: {lang_config['style']}.
Target dialect: {dialect or 'none'}.
{forbidden}

Source front matter:
{metadata}

Previous analysis, if any:
{previous_analysis or 'none'}

Chinese source body:
{source_body}

Return YAML with these top-level keys:
source_summary, literal_layer, implicit_layer, cross_cultural_layer, retelling_strategy, terminology_policy, forbidden_styles.
"""


def translation_prompt(protected_body, analysis_yaml, lang, lang_config):
    forbidden = ""
    if lang == "ar":
        forbidden = "Use only Damascus Levantine Arabic. Avoid Modern Standard Arabic and Saudi dialect completely."
    return f"""Target language: {lang_config['name']} ({lang}).
Target style: {lang_config['style']}.
{forbidden}

Analysis report:
{analysis_yaml}

Protected Chinese Markdown body:
{protected_body}

Rewrite the body naturally in the target language while staying faithful to the source meaning.
Keep every placeholder exactly unchanged.
Return only Markdown body.
"""
