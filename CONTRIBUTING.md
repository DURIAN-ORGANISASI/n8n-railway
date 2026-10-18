# Contributing

Thanks for improving this Railway starter. Keep pull requests focused, explain the reason for the change, and preserve safe defaults.

## Before opening a pull request

1. Keep API keys, PostgreSQL passwords, `N8N_ENCRYPTION_KEY`, real `.env` files, and private deployment logs out of commits and issues.
2. Update both `README.md` and `README.en.md` when deployment instructions, variables, or behavior changes.
3. Update `docs/SOURCES.md` when introducing upstream dependencies, copied material, screenshots, fonts, or other third-party assets.
4. Do not silently update the pinned `N8N_VERSION`. Include the release notes reviewed, backup plan, and tested upgrade/rollback steps.
5. Test configuration changes against a disposable Railway project when possible. Do not make production changes as part of documentation validation.

## Local checks

Python 3.10+ is enough; no third-party package installation is needed for the static checks.

```bash
python scripts/validate-repo.py
python scripts/check_docs.py
python -m json.tool railway.json
```

The checks validate required files, essential Railway/n8n settings, local Markdown references, and SVG/XML integrity. They do not connect to Railway, test a live PostgreSQL database, or prove that an n8n migration or external webhook succeeds.

## Pull request checklist

- [ ] The change has a clear summary and purpose.
- [ ] No real secrets or private deployment data are included.
- [ ] Indonesian and English documentation stay aligned.
- [ ] Local static checks pass.
- [ ] The n8n version remains pinned unless an upgrade is intentional and documented.
- [ ] Backup, encryption key retention, and rollback implications are documented for relevant changes.
- [ ] The root `LICENSE` and `FILE-MANIFEST.json` are kept accurate.

## Platform and license notes

The repository's MIT license covers only project material included in that license. It does not change n8n's upstream license, Railway terms, or third-party license obligations. The starter is independent and is not endorsed by n8n or Railway.
