from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_POSTS_DIR = ROOT / "_posts"
I18N_DIR = ROOT / ".i18n"
MANIFEST_PATH = I18N_DIR / "manifest.yml"
ANALYSIS_DIR = I18N_DIR / "analysis"
LLM_BASE_URL = "https://apinexus.net/v1"
LLM_MODEL = "gpt-5.4-nano"
SOURCE_LANG = "zh"
TARGET_LANGS = ["en", "th", "my", "km", "lo", "ru", "fa", "ar", "tr"]
