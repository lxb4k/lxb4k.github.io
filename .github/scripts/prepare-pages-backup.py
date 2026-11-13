"""Make the published backup usable on case-insensitive filesystems."""

from collections import defaultdict
from pathlib import Path
from unicodedata import normalize


def is_redirect(path: Path) -> bool:
    return path.suffix == ".html" and '<meta http-equiv="refresh"' in path.read_text(
        encoding="utf-8", errors="ignore"
    )


root = Path("docs")
groups: dict[str, list[Path]] = defaultdict(list)
for path in root.rglob("*"):
    if path.is_file():
        relative = path.relative_to(root).as_posix()
        groups[normalize("NFD", relative).casefold()].append(path)

for paths in groups.values():
    if len(paths) < 2:
        continue
    real_pages = [path for path in paths if not is_redirect(path)]
    if len(real_pages) != 1:
        raise RuntimeError(f"Cannot choose canonical page from {paths}")
    for path in paths:
        if path != real_pages[0]:
            path.unlink()

fallback = root / "404.html"
redirect_script = """
<script>
  const decodedPath = decodeURI(location.pathname)
  const lowerPath = decodedPath.toLocaleLowerCase()
  if (lowerPath !== decodedPath) {
    location.replace(encodeURI(lowerPath) + location.search + location.hash)
  }
</script>
"""
page = fallback.read_text(encoding="utf-8")
if "</html>" not in page:
    raise RuntimeError("Backup 404 page has no closing HTML tag")
fallback.write_text(page.replace("</html>", redirect_script + "</html>"), encoding="utf-8")
