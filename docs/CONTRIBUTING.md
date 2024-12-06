# Contributing to PyALX

Thank you for your interest in contributing to **PyALX**!  
This project is a Python-based custom shell designed for extensibility, with plans to incorporate AI features in the future. Contributions are vital to improving PyALX, whether it's fixing bugs, adding new features, enhancing documentation, or optimizing performance.

Please read the following guidelines to ensure smooth collaboration.

---

## Getting Started

### 1. Fork the Repository
To begin, fork the repository to your GitHub account. This ensures you can make changes without affecting the main project.

### 2. Clone the Repository
Clone your fork to your local machine using:
```bash
git clone https://github.com/<your-username>/pyAlx.git
cd pyAlx
```

### 3. Set Up the Environment
Install the required dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Create a New Branch
For every contribution, create a new branch with a descriptive name:
```bash
git checkout -b feature/your-feature-name
```

---

## Contribution Guidelines

### Code Style
- Follow Python’s PEP 8 style guide for consistency.
- Use tools like `flake8` and `black` for linting and formatting:
  ```bash
  pip install flake8 black
  black . --check
  flake8 .
  ```

### Commit Messages
Write clear and descriptive commit messages. Follow this format:
```
[type]: Short description

[type] can be one of: feat (feature), fix (bug fix), docs (documentation), style (formatting), refactor (code changes), test (tests), chore (maintenance).
Example: feat: Add AI-based command auto-suggestions
```

### Testing
- Write unit tests for new features or bug fixes in the `tests/` folder.
- Run all tests before submitting your changes:
  ```bash
  pytest tests/ -v
  ```

### Documentation
- Update the `README.md` or `CONTRIBUTING.md` files if your changes affect project usage or guidelines.
- Write concise and helpful comments in your code where needed.

### Pull Requests
- Push your branch to your forked repository:
  ```bash
  git push origin feature/your-feature-name
  ```
- Open a pull request (PR) to the `main` branch of the original repository.
- Include the following in your PR description:
  - A brief summary of your changes.
  - Any issues it addresses (if applicable).
  - Steps to test the changes (if needed).

---

## Reporting Issues

Found a bug or have a feature request? Open an issue on the [GitHub Issues page](https://github.com/Ali-Beg/pyAlx/issues) with the following details:
1. A clear and concise title.
2. Steps to reproduce the issue (if applicable).
3. Expected and actual behavior.
4. Any relevant screenshots or logs.

---

## Code of Conduct

We strive to create a welcoming and inclusive environment for everyone. Please:
- Be respectful to other contributors.
- Provide constructive feedback.
- Avoid using offensive or inappropriate language.

---

## Need Help?

If you have any questions, feel free to:
- Open a [discussion thread](https://github.com/Ali-Beg/pyAlx/discussions).
- Reach out by creating an issue with the `help wanted` label.

---

## Future Enhancements

Exciting features planned for PyALX:
- AI-driven command suggestions.
- Multi-tab GUI support.
- Customizable themes.
- Shell scripting and plugin system.

We’d love for you to help make these features a reality! 🚀

Thank you for contributing to **PyALX**! Together, we can make this shell awesome.
```

---

### How to Add It to Your Repository

1. **Create the File**:
   - In your project directory, create a new file named `CONTRIBUTING.md`.
   - Copy and paste the above content into the file.

2. **Add and Commit the File**:
   ```bash
   git add CONTRIBUTING.md
   git commit -m "docs: Add CONTRIBUTING.md"
   ```

3. **Push the Changes**:
   ```bash
   git push origin main
   ```