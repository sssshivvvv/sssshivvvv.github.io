# sssshivvvv.github.io

Personal website of **Shivam Singh** — Research Fellow at AMD India.

## Pages

| Page | File |
|------|------|
| Home (Introduction + News) | `index.html` |
| Research | `research.html` |
| Interests | `interests.html` |
| Photography | `photography.html` |
| Monkey Business | `monkey-business.html` |
| Motorcycling | `motorcycling.html` |

## Local preview

```bash
cd sssshivvvv.github.io
python3 -m http.server 8080
# open http://localhost:8080
```

## Structure

```
assets/
  css/style.css       # shared design system
  js/main.js          # nav toggle + lightbox
  img/                # optimized photos + paper teasers
  cv/                 # resume PDF
scripts/              # image optimization + arXiv teaser fetch
```

Built with plain HTML/CSS/JS — no build step required. Deployed via GitHub Pages.
