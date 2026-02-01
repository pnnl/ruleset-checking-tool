# AGENTS.md

# Contribution Guide for AI Agents

This document describes the expected workflow for contributing to this repository. Follow it for any change that may land in a pull request.

## Repository Layout (rct229)
The core package lives in `rct229/` with this structure:
- `rct229/rule_engine` — RCT evaluation engine.
- `rct229/report_engine` — reporting engine.
- `rct229/rulesets` — ruleset plugins/play rulesets (currently supports ASHRAE 90.1 2019 and 2022).
- `rct229/reports` — ruleset evaluation reports (currently supports ASHRAE 90.1 2019 and 2022).
- `rct229/ruletest_engine` — rule test engine.
- `rct229/schema` — ruleset evaluation schema (RES).
- `rct229/utils` — helper functions.

Related assets live under `docs/` (RDS), `examples/`, and `test/`.

## General Guidance
- The package targets Python 3.10 and uses Poetry for dependency management.
- The default install includes the ASHRAE 90.1-2019 ruleset. The 2022 ruleset is optional.
- Follow the rule definition and rule test workflows described in `README.md`.
- Keep updates consistent with the Rule Definition Strategy (RDS) documents under `docs/`.

## Building and Testing
Install dependencies with Poetry:
- Default ruleset (2019): `poetry install`
- Add 2022 ruleset: `poetry install --extras ashrae9012022`
- All available rulesets: `poetry install --all-extras`

Run tests:
- Unit tests: `poetry run pytest -v`
- Coverage: `poetry run pytest --cov`
- Rule tests (2019): `poetry run rct229 test -rs ashrae9012019`
- Rule tests (2022): `poetry run rct229 test -rs ashrae9012022`

CLI smoke test example:
- `poetry run rct229 evaluate -rs ashrae9012019 -f examples/chicago_demo/baseline_model.json -f examples/chicago_demo/proposed_model.json -f examples/chicago_demo/user_model.json -r ASHRAE9012019_DETAIL`

## CI/CD Pipeline (GitHub Actions)
Workflow: `.github/workflows/python-app.yml` (runs on pull requests).
- **Black formatting check** using `psf/black@stable` (version 22.6.0).
- **Unit tests** on Ubuntu with Python 3.10 (`poetry run pytest -v`).
- **Rule tests** run conditionally based on changed files:
  - 2019 tests run when files change under `rct229/rulesets/ashrae9012019/**` or `rct229/ruletest_engine/ruletest_jsons/ashrae9012019/**`.
  - 2022 tests run when files change under `rct229/rulesets/ashrae9012022/**` or `rct229/ruletest_engine/ruletest_jsons/ashrae9012022/**`.
- Rule tests run with `RCT_DISABLE_CACHE=1` in CI.

## Commit Messages and Pull Requests
- **Branch/PR naming convention**: `CODE/INITIALS/DESCRIPTIVE_NAME`
  - `RCT` for high-level repo changes (README, schema, etc.)
  - `RDS` for RDS docs
  - `RS` for ruleset code
  - `RT` for rule test engine
- Use concise, descriptive commit messages in the imperative mood.
- Before committing, run:
  1. `poetry run isort .`
  2. `poetry run black .`
  3. `poetry run pytest --cov`
  4. `poetry run rct229 test` (add `-rs ashrae9012019` or `-rs ashrae9012022` as appropriate)

## Review Checklist
- **Formatting**: `isort` and `black` applied.
- **Tests**: `pytest` passes; relevant rule tests executed for any ruleset changes.
- **Ruleset changes**: updates to `rules_dict`, RDS docs, and rule tests are consistent.
- **Schema changes**: RES updates align with schema files under `rct229/schema`.
- **Docs/examples**: README and any referenced docs/examples remain accurate.
- **Optional dependencies**: changes to 2022 ruleset use Poetry extras as needed.
