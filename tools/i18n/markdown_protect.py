import re

PATTERNS = [
    ("CODE_BLOCK", re.compile(r"```[\s\S]*?```")),
    ("LIQUID", re.compile(r"({%[\s\S]*?%}|{{[\s\S]*?}})")),
    ("IMAGE", re.compile(r"!\[[^\]]*\]\([^\)]*\)")),
    ("LINK", re.compile(r"\[[^\]]+\]\((?:https?://|/)[^\)]*\)")),
    ("INLINE_CODE", re.compile(r"`[^`]+`")),
    ("URL", re.compile(r"https?://[^\s)]+")),
]


def protect_markdown(text: str):
    protected = {}
    result = text
    counter = 0
    for name, pattern in PATTERNS:
        def replace(match):
            nonlocal counter
            token = f"__I18N_{name}_{counter:04d}__"
            protected[token] = match.group(0)
            counter += 1
            return token
        result = pattern.sub(replace, result)
    return result, protected


def restore_markdown(text: str, protected: dict):
    result = text
    for token, value in protected.items():
        result = result.replace(token, value)
    return result
