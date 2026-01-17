# Contributing to Ryde Waste Collection Integration

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Logs (if applicable, with sensitive info removed)

### Suggesting Features

Feature requests are welcome! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- Possible implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation if needed
4. **Test your changes**
   ```bash
   ./setup.sh
   ./get-ryde-bins.sh
   ```
5. **Commit your changes**
   ```bash
   git commit -m "feat: Add your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## Testing

Before submitting a PR, please test:
- Standalone scraper functionality
- Home Assistant integration (if applicable)
- Error handling with invalid inputs
- Documentation updates

## Documentation

If you change functionality:
- Update relevant documentation files
- Update README if needed
- Add examples where helpful

## Commit Messages

Use clear, descriptive commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for test additions/changes

Examples:
- `feat: Add support for multiple addresses`
- `fix: Handle timeout errors gracefully`
- `docs: Update Home Assistant setup guide`

## Questions?

Feel free to open an issue for questions or discussions!

## Code of Conduct

Be respectful and constructive in all interactions.

---

Thank you for contributing! 🙏
