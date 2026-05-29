import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ATOM_PATH = ROOT / ".i18n" / "legacy" / "thiswind.github.io.old.atom.xml"
POSTS_DIR = ROOT / "_posts"
IMAGE_DIR = ROOT / "assets" / "images" / "legacy-old"
FEED_URL = "https://raw.githubusercontent.com/thiswind/thiswind.github.io.old/master/atom.xml"
NS = {"a": "http://www.w3.org/2005/Atom"}

QUEUE_ORDER = [
    "治愈",
    "乾园餐厅",
    "自由软件",
    "yaml格式在markdown当中的写法",
    "MathTest",
    "bash临时取消alias的办法",
    "大数据分析是人机共同体",
    "IPython Notebook",
    "很想念我的朋友",
    "赫洛与勒安得耳",
    "docker-compose.yml中指定UDP端口",
    "InfluxDB的查询语句必须用单引号",
    "各种BIN路径的区别",
    "DNSMasq and DNSCrypt in one Docker",
    "Circle CI 中docker-compose 版本问题",
    "circle.yml基本概念",
    "Mac OS X 删除 Docker Toolbox 的办法",
    "Tree 命令中文乱码问题的解决",
    "糟糕的犬儒主义",
    "Ubuntu下用DNSCrypt做代理用DNSMasq做缓存配置安全DNS服务器",
]


def slugify(value):
    value = re.sub(r"\s+", "-", value.strip())
    value = re.sub(r"[\\/:*?\"<>|#%{}^~\[\]`;]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "legacy-post"


def yaml_quote(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"') + '"'


def ensure_atom():
    if ATOM_PATH.exists():
        return ATOM_PATH.read_text(encoding="utf-8")
    ATOM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(FEED_URL, timeout=30) as response:
        content = response.read().decode("utf-8")
    ATOM_PATH.write_text(content, encoding="utf-8")
    return content


def load_entries():
    root = ET.fromstring(ensure_atom())
    entries = []
    for entry in root.findall("a:entry", NS):
        title = entry.findtext("a:title", namespaces=NS)
        published = entry.findtext("a:published", namespaces=NS)
        updated = entry.findtext("a:updated", namespaces=NS)
        content = entry.findtext("a:content", namespaces=NS) or ""
        link = entry.find("a:link", NS).attrib.get("href", "")
        categories = [node.attrib.get("term") for node in entry.findall("a:category", NS) if node.attrib.get("term")]
        entries.append({
            "title": title,
            "date": published[:10],
            "published": published,
            "updated": updated,
            "content": content,
            "link": link,
            "categories": categories,
        })
    by_title = {entry["title"]: entry for entry in entries}
    ordered = [by_title[title] for title in QUEUE_ORDER if title in by_title]
    ordered.extend(entry for entry in entries if entry["title"] not in QUEUE_ORDER)
    return ordered


def text_content(html):
    class TextParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.parts = []
        def handle_data(self, data):
            self.parts.append(data)
    parser = TextParser()
    parser.feed(html)
    return unescape("".join(parser.parts))


def convert_highlight_figures(html):
    pattern = re.compile(r'<figure class="highlight(?:\s+([^"]+))?">.*?<td class="code"><pre>(.*?)</pre></td>.*?</figure>', re.S)
    def repl(match):
        lang = match.group(1) or ""
        code_html = re.sub(r'<span class="line">(.*?)</span>(?:<br>)?', lambda m: text_content(m.group(1)) + "\n", match.group(2), flags=re.S)
        code = unescape(re.sub(r"<.*?>", "", code_html)).rstrip()
        return f"\n\n```{lang}\n{code}\n```\n\n"
    return pattern.sub(repl, html)


def ext_for_url(url, content_type):
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix and len(suffix) <= 6:
        return suffix
    if "png" in content_type:
        return ".png"
    if "jpeg" in content_type or "jpg" in content_type:
        return ".jpg"
    if "gif" in content_type:
        return ".gif"
    if "webp" in content_type:
        return ".webp"
    return ".img"


def download_image(url, post_slug, index):
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type", "")
        if not data or (content_type and not content_type.startswith("image/")):
            return None
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        ext = ext_for_url(url, content_type)
        path = IMAGE_DIR / f"{post_slug}-{index}{ext}"
        path.write_bytes(data)
        return "/" + path.relative_to(ROOT).as_posix()
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


class MarkdownConverter(HTMLParser):
    def __init__(self, post_slug):
        super().__init__(convert_charrefs=False)
        self.post_slug = post_slug
        self.parts = []
        self.links = []
        self.skip_stack = []
        self.list_stack = []
        self.image_index = 0
        self.in_pre = False
        self.in_code = False
        self.pre_parts = []
        self.inline_code_parts = []
        self.heading = None
        self.heading_parts = []
        self.blockquote_depth = 0

    def append(self, text):
        if self.skip_stack:
            return
        if self.in_pre:
            self.pre_parts.append(text)
        elif self.in_code:
            self.inline_code_parts.append(text)
        elif self.heading:
            self.heading_parts.append(text)
        else:
            self.parts.append(text)

    def newline(self, count=2):
        if self.skip_stack or self.in_pre or self.in_code or self.heading:
            return
        current = "".join(self.parts)
        stripped = current.rstrip("\n")
        self.parts[:] = [stripped + "\n" * count]

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style"}:
            self.skip_stack.append(tag)
            return
        if tag in {"p", "div"}:
            self.newline(2)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.newline(2)
            self.heading = int(tag[1])
            self.heading_parts = []
        elif tag == "br":
            self.append("\n")
        elif tag in {"strong", "b"}:
            self.append("**")
        elif tag in {"em", "i"}:
            self.append("*")
        elif tag == "a":
            self.links.append({"href": attrs.get("href", ""), "text": []})
        elif tag == "img":
            src = attrs.get("src")
            if not src:
                return
            self.image_index += 1
            local_src = download_image(src, self.post_slug, self.image_index)
            if not local_src:
                return
            alt = attrs.get("alt") or "image"
            self.append(f"![{alt}]({local_src})")
        elif tag in {"ul", "ol"}:
            self.newline(2)
            self.list_stack.append({"tag": tag, "index": 1})
        elif tag == "li":
            self.newline(1)
            if self.list_stack and self.list_stack[-1]["tag"] == "ol":
                marker = f"{self.list_stack[-1]['index']}. "
                self.list_stack[-1]["index"] += 1
            else:
                marker = "- "
            self.append("  " * max(0, len(self.list_stack) - 1) + marker)
        elif tag == "blockquote":
            self.newline(2)
            self.blockquote_depth += 1
            self.append("> ")
        elif tag == "pre":
            self.newline(2)
            self.in_pre = True
            self.pre_parts = []
        elif tag == "code":
            if self.in_pre:
                return
            self.in_code = True
            self.inline_code_parts = []
        elif tag == "hr":
            self.newline(2)
            self.append("---")
            self.newline(2)

    def handle_endtag(self, tag):
        if self.skip_stack and self.skip_stack[-1] == tag:
            self.skip_stack.pop()
            return
        if tag in {"p", "div"}:
            self.newline(2)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self.heading:
            text = normalize_inline("".join(self.heading_parts))
            self.parts.append(f"{'#' * min(self.heading, 6)} {text}\n\n")
            self.heading = None
            self.heading_parts = []
        elif tag in {"strong", "b"}:
            self.append("**")
        elif tag in {"em", "i"}:
            self.append("*")
        elif tag == "a" and self.links:
            link = self.links.pop()
            text = normalize_inline("".join(link["text"]))
            href = link["href"]
            rendered = f"[{text}]({href})" if href and not href.startswith("#fn") else text
            if self.links:
                self.links[-1]["text"].append(rendered)
            else:
                self.append(rendered)
        elif tag in {"ul", "ol"} and self.list_stack:
            self.list_stack.pop()
            self.newline(2)
        elif tag == "blockquote" and self.blockquote_depth:
            self.blockquote_depth -= 1
            self.newline(2)
        elif tag == "pre" and self.in_pre:
            code = unescape("".join(self.pre_parts)).strip("\n")
            self.in_pre = False
            self.parts.append(f"\n\n```\n{code}\n```\n\n")
            self.pre_parts = []
        elif tag == "code" and self.in_code:
            code = normalize_inline("".join(self.inline_code_parts))
            self.in_code = False
            self.append(f"`{code}`")
            self.inline_code_parts = []

    def handle_data(self, data):
        data = unescape(data)
        if self.links:
            self.links[-1]["text"].append(data)
        else:
            self.append(data)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")

    def markdown(self):
        return normalize_markdown("".join(self.parts))


def normalize_inline(text):
    return re.sub(r"\s+", " ", unescape(text)).strip()


def preserve_math_delimiters(text):
    return re.sub(r"(?<!\\)\\([\\[\\]()])", r"\\\\\1", text)


def normalize_markdown(text):
    text = text.replace("\xa0", " ")
    text = preserve_math_delimiters(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines).strip() + "\n"


def html_to_markdown(html, post_slug):
    html = convert_highlight_figures(html)
    parser = MarkdownConverter(post_slug)
    parser.feed(html)
    return parser.markdown()


def write_post(entry):
    slug = slugify(entry["title"])
    path = POSTS_DIR / f"{entry['date']}-{slug}.md"
    source_id = f"{entry['date']}-{slugify(entry['title']).lower()}"
    body = html_to_markdown(entry["content"], slugify(entry["title"]))
    categories = entry["categories"] or ["notes"]
    frontmatter = [
        "---",
        "layout: post",
        f"title: {yaml_quote(entry['title'])}",
        f"date: {entry['published']}",
        "lang: zh",
        "dir: ltr",
        f"source_id: {yaml_quote(source_id)}",
        "categories:",
    ]
    frontmatter.extend(f"  - {yaml_quote(category)}" for category in categories)
    frontmatter.extend([
        "legacy_source:",
        "  repository: thiswind/thiswind.github.io.old",
        f"  url: {yaml_quote(entry['link'])}",
        "---",
        "",
    ])
    path.write_text("\n".join(frontmatter) + body, encoding="utf-8")
    return path


def print_queue(entries):
    for index, entry in enumerate(entries, start=1):
        print(f"{index:02d} {entry['date']} {entry['title']} ({len(entry['content'])} html chars)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--index", type=int)
    parser.add_argument("--title")
    args = parser.parse_args()

    entries = load_entries()
    if args.list:
        print_queue(entries)
        return
    if args.title:
        matches = [entry for entry in entries if entry["title"] == args.title]
        if not matches:
            raise SystemExit(f"title not found: {args.title}")
        entry = matches[0]
    elif args.index:
        if args.index < 1 or args.index > len(entries):
            raise SystemExit(f"index out of range: {args.index}")
        entry = entries[args.index - 1]
    else:
        parser.error("use --list, --index, or --title")

    path = write_post(entry)
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
