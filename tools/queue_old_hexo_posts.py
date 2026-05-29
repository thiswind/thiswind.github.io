import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from migrate_old_hexo_feed import html_to_markdown, load_entries, slugify, yaml_quote

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
QUEUE_DIR = ROOT / ".i18n" / "legacy_queue"
QUEUE_POSTS_DIR = QUEUE_DIR / "posts"
MANIFEST_PATH = ROOT / ".i18n" / "manifest.yml"


def existing_source_ids():
    ids = set()
    for path in POSTS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r'^source_id:\s*["\']?([^"\'\n]+)', text, re.M)
        if match:
            ids.add(match.group(1).strip())
    return ids


def render_post(entry):
    slug = slugify(entry["title"])
    source_id = f"{entry['date']}-{slugify(entry['title']).lower()}"
    body = html_to_markdown(entry["content"], slug)
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
    filename = f"{entry['date']}-{slug}.md"
    return source_id, filename, "\n".join(frontmatter) + body


def prepare_queue():
    if QUEUE_POSTS_DIR.exists():
        shutil.rmtree(QUEUE_POSTS_DIR)
    QUEUE_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    existing_ids = existing_source_ids()
    queued = []
    for entry in load_entries():
        source_id, filename, content = render_post(entry)
        if source_id in existing_ids:
            continue
        index = len(queued) + 1
        post_dir = QUEUE_POSTS_DIR / f"{index:02d}-{slugify(entry['title'])}"
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / filename).write_text(content, encoding="utf-8")
        for image_path in image_paths(content):
            queued_image = post_dir / "assets" / image_path.relative_to(ROOT)
            queued_image.parent.mkdir(parents=True, exist_ok=True)
            if image_path.exists():
                shutil.move(str(image_path), queued_image)
        queued.append((post_dir, entry["title"], filename))
    print(f"prepared {len(queued)} posts in {QUEUE_POSTS_DIR.relative_to(ROOT)}")
    for post_dir, title, filename in queued:
        print(f"{post_dir.name}: {filename} {title}")


def run(command):
    subprocess.run(command, cwd=ROOT, check=True)


def git_output(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def assert_clean_tree():
    status = git_output("status", "--short")
    if status:
        raise SystemExit(f"working tree is not clean:\n{status}")


def image_paths(markdown):
    paths = []
    for match in re.finditer(r"\]\((/assets/images/legacy-old/[^)]+)\)", markdown):
        path = ROOT / match.group(1).lstrip("/")
        if path.exists():
            paths.append(path)
    return paths


def queued_post_dirs():
    if not QUEUE_POSTS_DIR.exists():
        raise SystemExit("queue is missing; run prepare first")
    return sorted(path for path in QUEUE_POSTS_DIR.iterdir() if path.is_dir())


def commit_queue():
    assert_clean_tree()
    for post_dir in queued_post_dirs():
        markdown_files = sorted(post_dir.glob("*.md"))
        if len(markdown_files) != 1:
            raise SystemExit(f"expected one markdown file in {post_dir.relative_to(ROOT)}")
        source = markdown_files[0]
        target = POSTS_DIR / source.name
        if target.exists():
            print(f"skip existing {target.relative_to(ROOT)}")
            shutil.rmtree(post_dir)
            continue

        markdown = source.read_text(encoding="utf-8")
        target.write_text(markdown, encoding="utf-8")
        for queued_image in (post_dir / "assets").glob("**/*") if (post_dir / "assets").exists() else []:
            if queued_image.is_file():
                image_target = ROOT / queued_image.relative_to(post_dir / "assets")
                image_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(queued_image, image_target)
        run([sys.executable, "tools/i18n/sync_posts.py"])

        paths = [target, MANIFEST_PATH, *image_paths(markdown)]
        run(["git", "add", *[str(path.relative_to(ROOT)) for path in paths]])
        status = git_output("diff", "--cached", "--name-only")
        if not status:
            raise SystemExit(f"nothing staged for {target.relative_to(ROOT)}")

        title_match = re.search(r'^title:\s*["\']?([^"\'\n]+)', markdown, re.M)
        title = title_match.group(1).strip() if title_match else target.stem
        message = f"Migrate old Hexo post {title}\n\nCo-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
        run(["git", "commit", "-m", message])
        run(["git", "push", "origin", "main"])
        shutil.rmtree(post_dir)
        assert_clean_tree()
        print(f"pushed {target.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("prepare")
    subparsers.add_parser("run")
    args = parser.parse_args()

    if args.command == "prepare":
        prepare_queue()
    elif args.command == "run":
        commit_queue()


if __name__ == "__main__":
    main()
