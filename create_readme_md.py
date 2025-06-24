import os

MARKER_START = "<!-- AUTO-GENERATED: BEGIN -->"
MARKER_END = "<!-- AUTO-GENERATED: END -->"

# Static preamble inserted before auto-generated content
PREAMBLE = """
# In Process
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

This project is licensed under the [GNU AGPLv3 License](LICENSE).

© 2025 thewindghost. All rights reserved.
---

## 🐞 Vulnerability Catalogue

This repository intentionally includes many security bugs discovered during my bug bounty hunting.
**Do NOT deploy to production, but you can practice in here for pentest skills.**

---
## How can Build ?

### Build for developer
```bash
python => 3.10 version
pip install -r requirements.txt
python3 ./run.py or python.exe ./run.py
```
---

### Build with docker-compose for security researcher
```bash
docker-compose up -d && docker-compose build
```
---

### Note 1: if you have updated the code from local and want docker container to have that code. Run the docker-compose build command again
#### Warning: There is a tool to clean all unused docker containers and docker images, use with caution.
```bash
sh clean_docker_not_using.sh && docker-compose build && docker-compose up -d
```

### Note 2: Because updating code into README.md is quite time consuming, I made a tool to update all the code into it, and just click run. It will automatically create README.md synthesizing all the code in the folder.
```bash
python.exe ./create_readme_md.py or python3 ./create_readme_md.py
```
---
"""

# Files or directories to ignore
IGNORE = {'.env', 'database.db', '.git', 'README.md', 'favicon.ico', 'LICENSE', 'create_readme_md.py'}
IGNORE_DIRS = {'__pycache__'}

# File extensions to include and their fence language
LANG_MAP = {
    '.py': 'python',
    '.html': 'html',
    '.css': 'css',
    '.json': 'json',
    '.txt': '',
    '.yml': 'yaml',
    '.yaml': 'yaml',
    '.md': 'markdown',
    '.sh': 'bash',
    '.conf': 'config'
}


def get_project_tree(path=".", prefix="", is_root=True):
    """
    Recursively build a tree listing for `path`. At the root level, files are
    listed before directories for clearer project overview.
    """
    lines = []
    entries = os.listdir(path)
    # filter ignored
    entries = [e for e in sorted(entries) if e not in IGNORE and e not in IGNORE_DIRS]
    # at root, sort files first, then dirs
    if is_root:
        entries.sort(key=lambda e: (os.path.isdir(os.path.join(path, e)), e))
    for i, item in enumerate(entries):
        full_path = os.path.join(path, item)
        connector = '└──' if i == len(entries) - 1 else '├──'
        if os.path.isdir(full_path):
            lines.append(f"{prefix}{connector} {item}/")
            extension_prefix = '    ' if i == len(entries) - 1 else '│   '
            lines.extend(get_project_tree(full_path, prefix + extension_prefix, False))
        else:
            lines.append(f"{prefix}{connector} {item}")
    return lines


def extract_code_snippets(root_dir):
    snippets = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in sorted(files):
            if file in IGNORE:
                continue
            ext = os.path.splitext(file)[1]
            if ext in LANG_MAP:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        rel = os.path.relpath(file_path, '.')
                        snippets.append((rel, lines, ext))
                except Exception as e:
                    print(f"[WARN] Could not read {file_path}: {e}")
    return snippets


def build_markdown(tree_lines, snippets):
    output = []
    # prepend the static preamble
    output.append(PREAMBLE)
    # then auto-generated section
    output.append("## 📁 Project Structure\n")
    output.append("```text")
    output.extend(tree_lines)
    output.append("```\n")

    for rel_path, lines, ext in snippets:
        lang = LANG_MAP.get(ext, '')
        fence = lang if lang else ''
        output.append(f"### `{rel_path}`")
        output.append(f"```{fence}")
        output.extend([line.rstrip() for line in lines])
        output.append("```\n")
    return "\n".join(output)


def get_output_path(base_path):
    if not os.path.exists(base_path) or os.path.getsize(base_path) == 0:
        return base_path
    name, ext = os.path.splitext(base_path)
    idx = 1
    while True:
        candidate = f"{name}{idx}{ext}"
        if not os.path.exists(candidate) or os.path.getsize(candidate) == 0:
            return candidate
        idx += 1


def update_readme(content, readme_path="README.md"):
    # Choose output path: if existing non-empty, append index
    output_path = get_output_path(readme_path)

    try:
        with open(output_path, "r", encoding="utf-8") as f:
            old = f.read()
    except FileNotFoundError:
        old = f"{MARKER_START}\n{MARKER_END}"

    if MARKER_START in old and MARKER_END in old:
        pre, rest = old.split(MARKER_START, 1)
        _, post = rest.split(MARKER_END, 1)
        new_content = f"{pre}{MARKER_START}\n{content}\n{MARKER_END}{post}"
    else:
        new_content = f"{old}\n\n{MARKER_START}\n{content}\n{MARKER_END}"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[+] Updated {output_path} with project structure and full code snippets.")


if __name__ == "__main__":
    tree = get_project_tree('.')
    snippets = extract_code_snippets('.')
    markdown = build_markdown(tree, snippets)
    update_readme(markdown)
