# compose-configuration-audit

[![CI](https://github.com/LazyPanda902/compose-configuration-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/LazyPanda902/compose-configuration-audit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Read-only security posture scanning of normalized Docker Compose JSON configuration.

## Why this project exists

compose-configuration-audit is a small portfolio-grade operations tool designed around a concrete troubleshooting workflow rather than a demo-only code sample. It favors deterministic behavior, readable output, explicit failure states, and tests that exercise the core logic. The implementation intentionally stays narrow enough to understand quickly while still doing real work an IT support, systems, or homelab operator could use.

## What it demonstrates

- Python CLI design with no runtime third-party dependencies.
- Defensive input parsing and explicit exit behavior.
- Testable core logic separated from command-line presentation.
- GitHub Actions CI across supported Python versions.
- Privacy-conscious, read-only behavior appropriate for support tooling.
- Source-inspiration documentation that separates problem-space research from implementation.

## Quick start

```bash
git clone https://github.com/LazyPanda902/compose-configuration-audit.git
cd compose-configuration-audit
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
compose-configuration-audit --help
```

## Safety and data handling

This project is intentionally defensive and read-only. It does not exploit hosts, change remote configuration, collect credentials, or transmit collected data to a hosted service. Inputs and output stay local unless the operator explicitly redirects or shares them.

## Originality and source inspiration

Problem-space inspiration: [louislam/dockge](https://github.com/louislam/dockge). The reference repository was used only to understand an operational problem area and useful product ergonomics. **No source code from the reference repository is copied, vendored, or translated into this project.** The implementation, tests, CLI behavior, documentation, and project structure here are original Career Lab work.

See [`docs/source-inspiration.json`](docs/source-inspiration.json) for the machine-readable provenance note and [`docs/architecture.md`](docs/architecture.md) for the local design.

## Development

```bash
python -m pip install -e '.[dev]'
python -m compileall -q src
pytest -q
```

Pull requests should keep the project deterministic, local-first, and easy to audit. Do not add credential collection, remote exploitation, destructive actions, or mandatory cloud dependencies.

## License

MIT. See `LICENSE`.

### Strict mode for CI

Use the optional --strict flag before the input file to fail when a medium-severity finding occurs, in addition to high-severity findings. Default behavior and JSON output are unchanged. The option never modifies the target.
