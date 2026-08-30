from pathlib import Path
import html
import re

root = Path(__file__).resolve().parent
output_path = root / "sitemap.html"


def extract_title(file_path: Path) -> str:
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return file_path.stem.replace("_", " ").replace("-", " ").title()

    match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = html.unescape(title).strip()
        if title:
            return title

    return file_path.stem.replace("_", " ").replace("-", " ").title()


html_files = sorted(
    [p for p in root.glob("*.html") if p.name.lower() != "sitemap.html"],
    key=lambda p: p.name.lower(),
)

items_html = "\n".join(
    f'''        <li>\n          <a href="{p.name}">\n            <span>{extract_title(p)}</span>\n            <span class="meta">{p.name}</span>\n          </a>\n        </li>'''
    for p in html_files
)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Site Map</title>
  <style>
    :root {{
      --navy: #1d3b6d;
      --navy-dark: #10294f;
      --gold: #d9b15d;
      --bg: #f5f7fb;
      --card: #ffffff;
      --text: #1f2a37;
      --muted: #5b6472;
      --border: #dfe5f1;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}

    .wrap {{
      max-width: 960px;
      margin: 48px auto;
      padding: 0 20px;
    }}

    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 8px 25px rgba(16, 41, 79, 0.08);
      padding: 30px;
    }}

    h1 {{
      margin: 0 0 12px;
      color: var(--navy-dark);
      font-size: 2rem;
    }}

    .subtitle {{
      margin: 0 0 24px;
      color: var(--muted);
      font-size: 1rem;
    }}

    ul {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 12px;
    }}

    li {{
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #fafcff;
    }}

    a {{
      display: block;
      padding: 16px 18px;
      color: var(--navy);
      text-decoration: none;
      font-weight: 600;
    }}

    a:hover {{
      background: #eef4ff;
    }}

    .meta {{
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 0.9rem;
      font-weight: 400;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Project Site Map</h1>
      <p class="subtitle">Existing HTML pages in this workspace.</p>

      <ul>
{items_html}
      </ul>
    </div>
  </div>
</body>
</html>
'''

output_path.write_text(page, encoding="utf-8")
print(f"Generated sitemap for {len(html_files)} page(s): {output_path.name}")
