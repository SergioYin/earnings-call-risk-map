# Security And Privacy

`earnings-call-risk-map` is designed for local, deterministic review work from checked-out files. It does not fetch live data, call APIs, open sockets, use workflow runners, require a database, or require credentials to run package commands.

## Local-Only Operation

All public CLI commands read local JSON fixtures, templates, package files, and generated artifacts. Outputs are written to user-selected local paths or printed to stdout.

The project intentionally avoids runtime package dependencies and network-client imports. Static HTML dashboards are self-contained and do not load hosted JavaScript, CSS, fonts, images, analytics, or market-data feeds.

## No Credentials

Package commands do not require API keys, tokens, secrets, passwords, proxies, cloud credentials, or credential environment variables.

The audit check scans package and script sources for credential environment variable reads. The test suite also runs CLI commands with a minimal credential-free environment to confirm commands do not depend on secrets being present.

Users remain responsible for the fixture content they provide. Do not place private account numbers, unreleased company information, confidential notes, personal data, or secrets into fixtures intended for public demos, documentation, release artifacts, or issue reports.

## No Workflow Files

The repository does not include `.github/workflows` files, and no package command requires GitHub Actions or another workflow runner. Release, audit, demo, manifest, and maturity-evidence commands are local commands that can be run from a checkout.

If a downstream user adds their own workflow files, that automation is outside this package boundary and should be reviewed separately for credentials, permissions, logs, artifacts, and data retention.

## Privacy Scan Assumptions

`python scripts/privacy_scan.py` is a lightweight public-safety scan for repository text files. It looks for a small set of patterns that should not appear in public artifacts, including local absolute home paths, runtime asset references, likely OpenAI and AWS key formats, and disallowed private-context wording.

The privacy scan is not a full data-loss-prevention system. It does not prove that fixtures are free of personal data, confidential business information, proprietary research notes, or every possible secret format. Treat a passing scan as one release-readiness signal, not as permission to publish unreviewed inputs.

Before sharing public artifacts:

1. Review fixture text and source attribution manually.
2. Confirm static or stale data is labeled with `as_of`, `data_cutoff`, and `accessed_at` dates where relevant.
3. Run `python scripts/privacy_scan.py`.
4. Run `PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown` and confirm the Local-Only No-Network Guarantee remains passed.

## Boundary For Integrations

Downstream thesis, portfolio, database, hosted dashboard, market-data, or workflow systems own their own security model. This project only produces local Markdown, JSON, JSON Lines, and static HTML artifacts; it does not manage authentication, authorization, retention, approval workflows, or investment decisions.
