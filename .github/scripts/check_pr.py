#!/usr/bin/env python3
"""Проверка PR старосты: менять можно только content/<его группа>/, только .md/.pdf/.png/.jpg/.jpeg,
файл до 10 МБ, в .md без опасного HTML. Ничего из PR не скачивается и не запускается."""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
ALLOWED_EXT = {".md", ".pdf", ".png", ".jpg", ".jpeg"}
MAX_BYTES = 10 * 1024 * 1024
MAX_MD_BYTES = 1024 * 1024
MAX_FILES = 200
TRUSTED = {"OWNER", "MEMBER", "COLLABORATOR"}
MARKER = "<!-- group-check -->"
BAD_HTML = re.compile(
    r"<\s*(script|iframe|object|embed|style|link|meta|base|form)\b"
    r"|<[^>]*\son\w+\s*="
    r"|(href|src)\s*=\s*[\"']?\s*(javascript|data):"
    r"|\]\(\s*(javascript|data):",
    re.I,
)


def api(path, method="GET", data=None, raw=False):
    req = urllib.request.Request(
        path if path.startswith("http") else API + path,
        method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github.raw+json" if raw else "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read()
    return body.decode("utf-8", "replace") if raw else json.loads(body or b"null")


def pr_files(repo, number):
    files, page = [], 1
    while True:
        chunk = api(f"/repos/{repo}/pulls/{number}/files?per_page=100&page={page}")
        files += chunk
        if len(chunk) < 100 or len(files) > MAX_FILES:
            return files
        page += 1


def group_of(author, authors_path=".github/authors.json"):
    with open(authors_path, encoding="utf-8") as f:
        authors = {k.lower(): v for k, v in json.load(f).items()}
    return authors.get(author.lower())


def check(files, group, head_repo, head_sha):
    """Возвращает список текстов ошибок (пустой список = всё хорошо)."""
    errors = []
    if len(files) > MAX_FILES:
        return [f"Слишком много файлов в одном PR (больше {MAX_FILES})."]
    prefix = f"content/{group}/"

    def inside(path):
        parts = path.split("/")
        return (
            path.startswith(prefix)
            and ".." not in parts
            and not any(p.startswith(".") for p in parts)
        )

    for f in files:
        name, status = f["filename"], f["status"]
        paths = [name] + ([f["previous_filename"]] if f.get("previous_filename") else [])
        bad = [p for p in paths if not inside(p)]
        if bad:
            errors.append(f"`{bad[0]}`: можно менять только файлы в `{prefix}`.")
            continue
        if status == "removed":
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in ALLOWED_EXT:
            errors.append(f"`{name}`: тип файла `{ext or 'без расширения'}` не разрешён (можно: .md, .pdf, .png, .jpg).")
            continue
        url = f"/repos/{head_repo}/contents/{urllib.parse.quote(name)}?ref={head_sha}"
        try:
            meta = api(url)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            errors.append(f"`{name}`: не удалось прочитать файл из PR ({e}).")
            continue
        if isinstance(meta, list) or meta.get("type") != "file":
            errors.append(f"`{name}`: это не обычный файл (ссылки и подмодули запрещены).")
            continue
        if meta.get("size", 0) > MAX_BYTES:
            errors.append(f"`{name}`: больше 10 МБ. Тяжёлые файлы лучше выложить отдельно и дать ссылку.")
            continue
        if ext == ".md":
            if meta.get("size", 0) > MAX_MD_BYTES:
                errors.append(f"`{name}`: конспект больше 1 МБ.")
                continue
            text = api(url, raw=True)
            m = BAD_HTML.search(text)
            if m:
                errors.append(f"`{name}`: в тексте есть недопустимый HTML (`{m.group(0).strip()[:30]}`). Скрипты и встраивание запрещены.")
    return errors


def comment(repo, number, body):
    comments = api(f"/repos/{repo}/issues/{number}/comments?per_page=100")
    mine = next((c for c in comments if MARKER in c["body"]), None)
    if mine:
        api(f"/repos/{repo}/issues/comments/{mine['id']}", "PATCH", {"body": body})
    else:
        api(f"/repos/{repo}/issues/{number}/comments", "POST", {"body": body})


def main():
    env = os.environ
    repo, number, author = env["REPO"], env["PR_NUMBER"], env["PR_AUTHOR"]
    if env.get("AUTHOR_ASSOC") in TRUSTED:
        print("Автор — владелец или участник репозитория, проверка пропущена.")
        return 0
    group = group_of(author)
    if not group:
        errors = [f"Пользователя @{author} нет в `.github/authors.json`. Напиши владельцу сайта, чтобы тебя добавили."]
    else:
        errors = check(pr_files(repo, number), group, env["HEAD_REPO"], env["HEAD_SHA"])
    if errors:
        body = MARKER + "\n**Проверка не пройдена**\n\n" + "\n".join(f"- {e}" for e in errors)
        for e in errors:
            print("::error::" + e.replace("\n", " "))
        try:
            comment(repo, number, body)
        except Exception as e:  # комментарий не критичен
            print("Не удалось оставить комментарий:", e)
        return 1
    print(f"Проверка пройдена: изменения только в content/{group}/.")
    try:
        comment(repo, number, MARKER + f"\n**Проверка пройдена** ✅ Изменения только в `content/{group}/`.")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
