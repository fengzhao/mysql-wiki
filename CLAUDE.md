# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **MkDocs Material** documentation site (mysql-wiki) covering MySQL, PostgreSQL, Oracle, NoSQL, and related database/big data topics. Content is written in Chinese (Simplified). The site is deployed to https://mysql.fengzhao.pro via GitHub Pages.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Local dev server (http://127.0.0.1:8000)
mkdocs serve

# Build static site (outputs to site/)
mkdocs build
```

## Architecture

- **mkdocs.yml** — Central config: site metadata, theme settings (Material), plugins, markdown extensions, and the full `nav` tree. All navigation structure is defined here.
- **docs/** — All content as Markdown files, organized into numbered section directories (`01-mysql-basics/`, `02-mysql-fundamental/`, etc.). Each section has an `index.md`.
- **docs/stylesheets/extra.css** — Custom CSS for wide-screen layout and typography.
- **requirements.txt** — Python dependencies: `mkdocs`, `mkdocs-material`, `mkdocs-minify-plugin`, `mkdocs-git-revision-date-localized-plugin`, `mkdocs-git-authors-plugin`.
- **.github/workflows/publish_docs.yml** — CI pipeline: builds and deploys to GitHub Pages on push to `master`.
- **.gitlab-ci.yml** — Legacy GitLab CI config (no longer primary).

## Content Conventions

- File naming: lowercase English with hyphens, numbered prefix matching nav order (e.g., `01-introduce-database.md`, `02-install-mysql.md`).
- Content is written in Chinese; file names and code are in English.
- Markdown extensions in use: admonition, code highlighting with line numbers (`pymdownx.highlight`), tabbed content, task lists, footnotes, emoji, math (`pymdownx.arithmatex`), and more — see `mkdocs.yml` `markdown_extensions` for the full list.
- When adding a new page, it must also be added to the `nav` section in `mkdocs.yml`.

## Key Details

- Default branch: `master`
- MySQL examples target version **8.0** (some content applies to 5.7).
- Theme: Material for MkDocs with light/dark toggle, sticky tabs, search, and Google Analytics.
