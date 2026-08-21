# Contributing to pykvision

Thanks for helping improve the project.

This guide explains how to set up the environment, make changes safely, and open a clean pull request.

## Getting started

1. Fork the repository.
2. Clone your fork locally.
3. Create a feature branch for your change.
4. Install the project dependencies.
5. Make a focused change.
6. Run the relevant tests.
7. Open a pull request with a clear description.

## Development setup

```bash
git clone https://github.com/HandreyGama/pykvision.git
cd pykvision
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r dev-requirements.txt
```

## Recommended workflow

### 1) Create a branch

```bash
git checkout -b feature/my-change
```

### 2) Keep changes focused

Prefer small, well-scoped edits over broad refactors. This makes review easier and reduces the chance of regressions.

### 3) Run tests

```bash
python -m pytest -q
```

If you add new functionality, include tests whenever possible.

### 4) Update documentation

If your change affects:

- setup steps;
- usage examples;
- supported endpoints;
- authentication assumptions;
- troubleshooting guidance;

then update the relevant documentation as well.

## Coding expectations

- keep naming consistent with the existing codebase;
- prefer clear and explicit names;
- keep functions small and focused;
- add comments only when they clarify intent;
- avoid unnecessary style churn.

## Reporting bugs

When opening an issue, include:

- Python version;
- OS version;
- project version or commit;
- Hikvision device model and firmware version where relevant;
- endpoint used;
- request/response sample if possible;
- traceback or error message.

## Pull request guidelines

A good PR should include:

- a concise description of the problem;
- a short explanation of the fix;
- any impact or considerations;
- tests or validation steps;
- links to related issues if applicable.

Example title:

```text
feat: add support for intelligent FDLib capabilities
```

Example body:

```text
## What changed
- add mapping for new FDLib capability fields;
- populate the dataclass values correctly;
- add regression coverage.

## Validation
- python -m pytest -q
```

## Best practices

- avoid committing hardcoded device credentials;
- do not leave debugging prints in the codebase;
- keep commit messages clear and concise;
- validate changes with the local test suite before opening a PR.

## Need help?

If you are unsure where to begin, a good starting point is:

- reviewing open issues;
- improving documentation;
- adding tests for unsupported endpoints;
- helping with compatibility fixes;
- expanding device support and model mappings.

Thank you for contributing.
