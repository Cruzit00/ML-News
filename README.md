# ML Morning Digest — website

A searchable archive of every daily ML Morning Digest, with a permanent link
for each edition and an RSS feed. It is a plain [Jekyll](https://jekyllrb.com/)
site that GitHub Pages builds by itself: there is no server and nothing to
deploy by hand.

- **Archive and search:** the home page lists every digest by month, and the
  search box searches the full text of all of them.
- **Permanent links:** each digest lives at `/YYYY/MM/DD/`.
- **RSS:** `/feed.xml`, with the 30 most recent digests.

## Publishing a digest

Each digest is one Markdown file in `_posts/`. The daily routine creates it
from the same text it posts to Discord:

```sh
python3 scripts/publish_digest.py digest.md        # writes _posts/<today>-ml-morning-digest.md
git add _posts && git commit -m "Digest for $(TZ=America/Chicago date +%F)" && git push origin main
```

`digest.md` starts with the `# ☭ ML Morning Digest — …` heading. The script
uses that heading as the title, uses the intro line as the summary in the
archive, and drops the `(story N, cont.)` labels that only make sense on
Discord. Pages republishes the site a minute or two after the push.

## Turning on GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch**,
branch **main**, folder **/ (root)**. The site appears at
<https://cruzit00.github.io/ML-News/>.

If you later use a custom domain, set `url` to it and `baseurl` to `""` in
`_config.yml`.

## Previewing locally (optional)

```sh
bundle install
bundle exec jekyll serve
```
