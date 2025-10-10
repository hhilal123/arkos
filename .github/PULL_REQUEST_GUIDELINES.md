# Pull Request Guidelines

Thank you for contributing to **ARKOS**!
We welcome all contributions — from bug fixes to major features.
To keep our codebase clean, consistent, and easy to review, please follow these pull request guidelines.

---

## 1. Before You Start

- Open an issue first if your change is substantial (new feature, major refactor, or breaking change).
  This helps maintainers and contributors discuss the approach before code is written.
- Keep PRs focused — one feature, fix, or improvement per pull request. Smaller PRs are reviewed faster.
- Sync with the latest main branch before opening your PR:

    git fetch origin
    git rebase origin/main

---

## 2. Branch and Commit Naming

- Branch names: use lowercase with hyphens, for example:
    fix-import-chaos
    feature-agent-memory
    docs-installation-update
- Commit messages: use clear, present-tense descriptions:
    fix: correct import path in engine module
    feat: add persistent agent memory interface
    docs: update README with local deployment steps
- Follow Conventional Commits (https://www.conventionalcommits.org/) where possible.

---

## 3. Code Standards

- Follow project style conventions (PEP8 for Python, ESLint/Prettier for JavaScript, etc.).
- Include type hints and docstrings for new functions and classes.
- Add or update tests when relevant.
- Avoid large, unrelated formatting changes.

---

## 4. Testing

- Ensure all tests pass locally before submitting:

    pytest

- Add tests for any new behavior or features.
- Do not skip or comment out failing tests.

---

## 5. Documentation

- Update the README, docs, or inline comments to reflect any new features or changes.
- If your PR affects the public API or configuration, document those changes clearly.

---

## 6. Opening the Pull Request

- Use a clear and descriptive title (avoid “misc updates” or “fix stuff”).
- In your PR description:
    - Explain why this change is needed.
    - Summarize what was changed.
    - Link to related issues using Closes #<issue-number>.
    - Include screenshots or logs if they help explain your changes.

Example Template:

    ## Summary
    Fixes import issues in engine initialization due to circular dependencies.

    ## Changes
    - Reorganized module imports
    - Updated __init__.py files
    - Added regression test

    Closes #68

---

## 7. Review and Merge Process

- Be open to feedback. Maintainers may request changes for clarity or consistency.
- Squash commits if requested to keep the history clean.
- At least one maintainer review is required before merging.
- Maintainers handle version bumps and changelog updates.

---

## 8. After Merge

- Delete your feature branch after merging.
- Confirm that your change appears in the next release.
- Thank you for helping make **ARKOS** better!
