# Contributing Guide

Thank you for your interest in contributing to **Recon Automation Framework**.

Contributions of all kinds are welcome, including bug fixes, documentation improvements, feature enhancements, performance optimizations, and new reconnaissance modules.

Please take a moment to review the following guidelines before contributing.

---

# Ways to Contribute

You can contribute by:

- Reporting bugs
- Suggesting new features
- Improving documentation
- Fixing existing issues
- Optimizing performance
- Adding new reconnaissance modules
- Improving the dashboard or reporting system
- Writing tests
- Reviewing pull requests

---

# Development Setup

## 1. Fork the Repository

Fork the project from GitHub.

## 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/Recon-Automation-Framework.git

cd Recon-Automation-Framework
```

## 3. Create a Virtual Environment

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# Create a Branch

Create a dedicated branch for your changes.

```bash
git checkout -b feature/my-feature
```

Examples:

```text
feature/new-module
feature/dashboard

fix/http-timeout
fix/report-export

docs/readme
```

---

# Coding Guidelines

Please follow these guidelines:

- Follow PEP 8 style conventions.
- Write clear, readable, and maintainable code.
- Keep functions focused on a single responsibility.
- Prefer descriptive variable and function names.
- Avoid unnecessary dependencies.
- Reuse existing utilities whenever possible.

---

# Project Structure

New modules should follow the existing project layout.

```text
module/

├── analyzer.py
├── constants.py
├── exporter.py
├── helpers.py
├── manager.py
├── plugin.py
├── statistics.py
└── ...
```

Maintain consistency with the existing architecture.

---

# Commit Messages

Use descriptive commit messages.

Examples:

```text
feat: add CDN fingerprint detection

fix: resolve HTTP timeout handling

docs: improve installation guide

refactor: simplify dashboard exporter

perf: optimize DNS resolution
```

---

# Pull Requests

Before opening a Pull Request:

- Ensure the project runs successfully.
- Verify that your changes do not introduce regressions.
- Update documentation when necessary.
- Keep pull requests focused on a single topic.
- Clearly describe the purpose of your changes.

---

# Bug Reports

When reporting a bug, please include:

- Operating system
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Relevant logs or screenshots

---

# Feature Requests

Feature requests should include:

- Problem statement
- Proposed solution
- Expected benefit
- Example use case

---

# Security

If your contribution involves a security vulnerability, **do not create a public issue**.

Please follow the instructions in **SECURITY.md** for responsible disclosure.

---

# Questions

If you have questions about the project, feel free to:

- Open a GitHub Discussion (if enabled)
- Open an Issue
- Contact the maintainer

---

# License

By contributing to this project, you agree that your contributions will be licensed under the **MIT License**.

---

Thank you for helping improve **Recon Automation Framework** and supporting the open-source security community.