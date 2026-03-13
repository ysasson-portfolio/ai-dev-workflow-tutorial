<!--
  SYNC IMPACT REPORT
  ==================
  Version change: [TEMPLATE] → 1.0.0 (initial ratification)

  Principles added:
  - I. Data-Source Flexibility (new)
  - II. Streamlit-Native Visualization (new)
  - III. Test-First Development (new)
  - IV. Deploy to Streamlit Community Cloud (new)
  - V. Simplicity First / YAGNI (new)

  Sections added:
  - Tech Stack
  - Development Workflow
  - Governance

  Templates reviewed:
  - .specify/templates/plan-template.md        ✅ Constitution Check section aligns
  - .specify/templates/spec-template.md        ✅ User story + acceptance criteria align with TDD principle
  - .specify/templates/tasks-template.md       ✅ Test-first task ordering aligns with Principle III

  Deferred TODOs: none
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Data-Source Flexibility

The dashboard MUST support two data sources: the bundled `data/sales-data.csv`
(default, always available) and an external relational database (e.g., Postgres,
BigQuery, SQLite). All data-loading logic MUST be written against a common
interface so that switching sources requires no changes to visualization code.

- The CSV path MUST be the default when no database connection string is configured.
- External database credentials MUST be supplied via environment variables; they
  MUST NOT be hard-coded or committed to the repository.
- Connection errors from the external database MUST surface a clear user-facing
  message in the Streamlit UI rather than a raw Python traceback.

### II. Streamlit-Native Visualization

Chart implementations MUST prefer Streamlit's built-in primitives (`st.line_chart`,
`st.bar_chart`, `st.metric`) over third-party libraries. Plotly (via
`st.plotly_chart`) is the approved fallback when a native primitive cannot meet
the visual requirement; no other charting libraries are permitted.

- Every chart MUST have a clear title and axis/metric labels visible to the user.
- The decision to use Plotly MUST be justified in a code comment at the call site
  (e.g., `# Plotly used: st.bar_chart does not support grouped bars`).

### III. Test-First Development (NON-NEGOTIABLE)

All data-loading and transformation logic MUST follow Red-Green-Refactor TDD:

1. Write the test; confirm it **fails**.
2. Write the minimum implementation to make it **pass**.
3. **Refactor** without breaking the test.

- Tests MUST be committed before their corresponding implementation in the same
  feature branch, or in a preceding commit.
- `pytest` is the required test runner.
- Streamlit UI rendering does not require automated tests; manual verification
  during local development is sufficient for UI-only changes.
- No feature task is considered "done" until its tests pass in CI.

### IV. Deploy to Streamlit Community Cloud

The single production deployment target is Streamlit Community Cloud. Local
development (`uv run streamlit run app.py`) is the development environment.

- The repository MUST remain public to enable free-tier Streamlit Cloud deployment.
- All runtime dependencies MUST be declared in `pyproject.toml` (managed via `uv`).
- Deployment MUST succeed from the `main` branch without manual intervention beyond
  the Streamlit Cloud dashboard connection step.
- Secrets (database credentials, API keys) MUST be stored in Streamlit Cloud's
  Secrets management UI, not in the repository.

### V. Simplicity First (YAGNI)

The dashboard is a tutorial project. Complexity MUST be justified by a current,
concrete requirement — not a hypothetical future one.

- A single `app.py` is the preferred structure; do not split into multiple modules
  unless a function is reused in tests or exceeds ~100 lines of pure logic.
- Do not introduce configuration files, abstract base classes, or dependency
  injection frameworks unless a specific requirement demands them.
- Every added abstraction MUST be documented with a one-line rationale comment.
- When in doubt, choose the shorter, more direct implementation.

## Tech Stack

| Concern | Choice |
|---------|--------|
| Language | Python 3.11+ |
| Package manager | `uv` |
| Web framework | Streamlit |
| Charting | Streamlit-native → Plotly fallback |
| Data manipulation | Pandas |
| Testing | pytest |
| Deployment | Streamlit Community Cloud |
| Data source (default) | `data/sales-data.csv` |
| Data source (optional) | External relational database via env var |

## Development Workflow

1. **Spec** — run `/speckit.specify` to generate a feature spec from the PRD.
2. **Plan** — run `/speckit.plan` to produce research, data model, and contracts.
3. **Tasks** — run `/speckit.tasks` to generate a dependency-ordered task list.
4. **Jira** — create issues from tasks (one Jira issue per task group or story).
5. **Code** — implement following TDD (Principle III); commit with Jira key prefix
   (e.g., `ECOM-1: Set up project environment and data loading`).
6. **Push** — push to `main`; Streamlit Cloud auto-deploys.

All commits touching data-loading or transformation logic MUST include passing
`pytest` output in the PR description or commit notes.

## Governance

- This constitution supersedes all other practices when conflicts arise.
- Amendments require: (a) a documented rationale, (b) a version bump following
  semantic versioning (MAJOR: principle removal/redefinition; MINOR: new principle
  or section; PATCH: wording/clarification), and (c) an updated Sync Impact Report
  prepended as an HTML comment.
- All feature plans MUST include a "Constitution Check" section that verifies
  compliance with Principles I–V before Phase 0 research begins.
- Complexity exceptions (violations of Principle V) MUST be recorded in the plan's
  Complexity Tracking table with a justification.
- The runtime development reference is `CLAUDE.md` at the repository root.

**Version**: 1.0.0 | **Ratified**: 2026-03-12 | **Last Amended**: 2026-03-12
