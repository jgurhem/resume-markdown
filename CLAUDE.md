# resume-markdown

Markdown-to-PDF/HTML resume pipeline. Single source of truth: `resume-en.md` → `convert.py` (commonmark + weasyprint) → styled via `style.css` → deployed to GitHub Pages on every push to `master`.

## Key files

| File                                      | Purpose                                             |
|-------------------------------------------|-----------------------------------------------------|
| `resume-en.md`                            | Resume source — the only file you normally edit     |
| `convert.py`                              | Conversion script: Markdown → HTML → PDF            |
| `style.css`                               | CSS for rendering; also controls section visibility |
| `requirements.txt`                        | Python deps: `weasyprint`, `commonmark`             |
| `environment.yaml`                        | Conda env definition (env name: `cvmd`)             |
| `.github/workflows/build-and-release.yml` | CI: build + GitHub Pages deploy on push to master   |

## Build commands

```bash
# Quickest (uses local venv)
./convert.sh                           # builds HTML + PDF

# Manually
python convert.py --html resume-en.md  # HTML + PDF
python convert.py resume-en.md         # PDF only
```

### Environment setup

**venv (recommended locally)**
```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

**conda**
```bash
conda env create -f environment.yaml
conda activate cvmd
```

## Source file philosophy

`resume-en.md` is a **complete archive** of everything — all jobs, internships, skills, courses, and certifications. Visibility in the output is controlled via CSS, not by editing the source. **Never remove content from `resume-en.md`**.

`convert.py` automatically wraps every `## Heading` section in `<div id="slugified-heading">`, so every section is targetable from CSS. The slug is the heading text lowercased with non-alphanumeric runs replaced by `-` (e.g. "Old Technical Skills" → `old-technical-skills`).

Currently hidden sections in `style.css`:
| CSS selector            | What it hides              |
|-------------------------|----------------------------|
| `#certifications`       | Certifications section     |
| `#old-technical-skills` | Legacy skills              |
| `#courses`              | Courses section            |

To hide a section: add its ID selector to the hidden-sections rule in `style.css`. No changes to `resume-en.md` or `convert.py` needed.

## CSS notes

- `h2` → blue section headers (white text on blue background)
- `h3` → subsection headers (blue text, left border accent)
- Inline code `` `text` `` → renders as a badge/tag (light blue background) — used for skills/tech labels
- **Some sections are hidden via `display: none`** in `style.css`: certifications, old courses, outdated skills. Check `style.css` before adding content that should be visible.

## CI/CD

Pushing to `master` triggers `.github/workflows/build-and-release.yml`, which:
1. Builds HTML + PDF
2. Injects a "Download PDF" button (top-right corner) into the HTML
3. Deploys to GitHub Pages (`index.html` + `resume-en.pdf`)

## Gotchas

- Generated `*.html` and `*.pdf` are gitignored — do not commit them
- Never edit `resume-en.html` directly; it is overwritten on every build
- The `--double-column` flag is mentioned in the README but `style_doublecolumn.css` does not exist — do not rely on it
