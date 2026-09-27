#!/usr/bin/env python3
"""Convert a Markdown document into a clean, printable PDF for Carissa.

Usage: python3 scripts/md_to_pdf.py input.md [output.pdf] [--landscape]
Default output: pdf/<input name>.pdf
"""
import datetime
import glob
import html
import os
import subprocess
import sys
import tempfile

import markdown

CSS = """
@page { size: Letter %(orient)s; margin: 0.6in 0.6in 0.7in; }
:root { --ink:#2b2320; --barn:#9b2d20; --wheat:#f4ecdf; --line:#e3d7c3; --muted:#6f625a; }
body { font-family: 'Open Sans', 'DejaVu Sans', sans-serif; color: var(--ink);
       font-size: 10.5pt; line-height: 1.5; }
.brand { display:flex; justify-content:space-between; align-items:baseline;
         border-bottom: 3px solid var(--barn); padding-bottom: 6px; margin-bottom: 18px; }
.brand b { font-family: 'Montserrat', sans-serif; font-weight: 800; letter-spacing: .08em;
           color: var(--barn); font-size: 9pt; text-transform: uppercase; }
.brand span { color: var(--muted); font-size: 8.5pt; }
h1 { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 21pt; line-height:1.2;
     margin: 0 0 10px; }
h2 { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 14pt; color: var(--barn);
     margin: 22px 0 8px; padding-top: 6px; border-top: 1px solid var(--line); break-after: avoid; }
h3 { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 11.5pt; margin: 16px 0 6px;
     break-after: avoid; }
a { color: var(--barn); text-decoration: none; word-break: break-word; }
table { width: 100%%; border-collapse: collapse; margin: 10px 0 14px; font-size: 8.8pt; }
th { background: var(--wheat); text-align: left; font-weight: 700; }
th, td { border: 1px solid var(--line); padding: 5px 7px; vertical-align: top; }
tr { break-inside: avoid; }
blockquote { margin: 10px 0; padding: 8px 14px; background: var(--wheat);
             border-left: 4px solid var(--barn); }
code { font-size: 9pt; background: #f3efe9; padding: 1px 4px; border-radius: 3px; }
pre { background: #f3efe9; padding: 10px; font-size: 8.5pt; white-space: pre-wrap; }
hr { border: 0; border-top: 1px solid var(--line); margin: 18px 0; }
ul, ol { padding-left: 20px; }
li { margin: 2px 0; }
"""


def chrome_binary():
    for pattern in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                    "/usr/bin/chromium", "/usr/bin/google-chrome"):
        found = sorted(glob.glob(pattern))
        if found:
            return found[-1]
    sys.exit("No Chromium found")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    landscape = "--landscape" in sys.argv
    src = args[0]
    name = os.path.splitext(os.path.basename(src))[0]
    out = args[1] if len(args) > 1 else os.path.join("pdf", f"{name}.pdf")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    with open(src) as f:
        body = markdown.markdown(f.read(), extensions=["tables", "fenced_code", "sane_lists"])
    today = datetime.date.today().strftime("%B %-d, %Y")
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<title>{html.escape(name)}</title><style>{CSS % {'orient': 'landscape' if landscape else 'portrait'}}</style></head>
<body><div class="brand"><b>Mini Barn Market · Instagram Studio</b><span>{today}</span></div>
{body}</body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(page)
        html_path = f.name
    subprocess.run([chrome_binary(), "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", f"--print-to-pdf={os.path.abspath(out)}",
                    f"file://{html_path}"], check=True, capture_output=True)
    os.unlink(html_path)
    print(out)


if __name__ == "__main__":
    main()
