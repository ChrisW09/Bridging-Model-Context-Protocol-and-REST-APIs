# Contributing to MCP Proxy Implementation

Thank you for your interest in contributing to the MCP Proxy Implementation project! This document provides guidelines and instructions for contributing to the project.

## 🎯 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📋 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and diverse perspectives
- **Be constructive**: Provide helpful feedback and suggestions
- **Be collaborative**: Work together towards common goals

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git version control
- Basic understanding of HTTP protocols and APIs
- Familiarity with the Model Context Protocol (MCP) is helpful

### Quick Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Bridging-Model-Context-Protocol-and-REST-APIs.git
   cd Bridging-Model-Context-Protocol-and-REST-APIs
   ```

3. **Set up the development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Verify the setup** by running tests:
   ```bash
   python test_mcp_proxy.py
   ```

## 🛠️ Development Setup

### Environment Configuration

Create a local configuration file (optional):
```bash
cp .env.example .env  # If available
```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:
```bash
pre-commit install
```

This will automatically run code formatting and linting before each commit.

## 📝 Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

1. **🐛 Bug Reports**: Help us identify and fix issues
2. **✨ Feature Requests**: Suggest new functionality
3. **📖 Documentation**: Improve or add documentation
4. **🔧 Code Contributions**: Implement features or fix bugs
5. **🧪 Testing**: Add or improve test coverage
6. **🎨 Examples**: Create usage examples and tutorials

### Areas for Contribution

- **MCP Tools**: Implement new MCP tools and capabilities
- **Proxy Features**: Enhance proxy functionality and performance
- **Error Handling**: Improve error messages and recovery mechanisms
- **Documentation**: Expand guides, examples, and API documentation
- **Testing**: Add unit tests, integration tests, and performance tests
- **Performance**: Optimize proxy performance and resource usage

## 🔄 Pull Request Process

### Before Submitting

1. **Search existing issues** to avoid duplicates
2. **Discuss major changes** by opening an issue first
3. **Follow code standards** and run linting tools
4. **Add tests** for new functionality
5. **Update documentation** as needed

### Submission Steps

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our code standards

3. **Test your changes**:
   ```bash
   # Run existing tests
   python test_mcp_proxy.py
   
   # Run any new tests you've added
   pytest tests/ -v
   
   # Check code formatting
   black --check .
   isort --check-only .
   flake8 .
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes
   
   - Detailed explanation of what was changed
   - Why the change was made
   - Any breaking changes or migration notes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots or examples if applicable
   - Test results and verification steps

### Pull Request Review

- All PRs require at least one review from a maintainer
- Address feedback promptly and respectfully
- Keep PRs focused and atomic (one feature per PR)
- Be prepared to make changes based on review feedback

## 🐛 Issue Reporting

### Bug Reports

When reporting bugs, please include:

```markdown
**Bug Description**
A clear description of what the bug is.

**Reproduction Steps**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. macOS, Windows, Linux]
- Python Version: [e.g. 3.9.7]
- FastMCP Version: [e.g. 1.11.0]
- Browser (if applicable): [e.g. Chrome, Firefox]

**Additional Context**
- Error logs
- Screenshots
- Configuration files (remove sensitive data)
```

### Feature Requests

For feature requests, please include:

- **Problem Statement**: What problem does this solve?
- **Proposed Solution**: How should this work?
- **Alternatives Considered**: What other approaches did you consider?
- **Use Cases**: How would this feature be used?

## 🔧 Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `feature/*`: New features and enhancements
- `bugfix/*`: Bug fixes
- `docs/*`: Documentation updates
- `hotfix/*`: Critical fixes for production

### Commit Message Format

Follow conventional commits format:
```
type(scope): short description

Longer description if needed

- Bullet points for details
- Reference issues with #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Release Process

1. Update `CHANGELOG.md` with new version details
2. Update version numbers in relevant files
3. Create a pull request for the release
4. Tag the release after merge

## 📊 Code Standards

### Python Style Guide

- Follow **PEP 8** conventions
- Use **Black** for code formatting
- Use **isort** for import sorting
- Use **type hints** for function signatures
- Maximum line length: **88 characters** (Black default)

### Code Quality Tools

Run these tools before submitting:
```bash
# Format code
black .
isort .

# Check for issues
flake8 .
mypy .
bandit -r .
```

### Naming Conventions

- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Files**: `snake_case.py`

## 🧪 Testing

### Test Structure

```
tests/
├── unit/
│   ├── test_manual_proxy.py
│   ├── test_proxy_server.py
│   └── test_backend_server.py
├── integration/
│   ├── test_end_to_end.py
│   └── test_mcp_protocol.py
└── performance/
    └── test_load.py
```

### Writing Tests

- Use **pytest** for testing framework
- Follow **AAA pattern**: Arrange, Act, Assert
- Use **descriptive test names**
- Mock external dependencies
- Test both success and failure cases

Example test:
```python
def test_currency_converter_with_valid_input():
    """Test currency conversion with valid input parameters."""
    # Arrange
    request_data = {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    }
    
    # Act
    response = client.post("/currency_converter", json=request_data)
    
    # Assert
    assert response.status_code == 200
    assert "converted_amount" in response.json()
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_manual_proxy.py

# Run with verbose output
pytest -v
```

## 📚 Documentation

### Documentation Standards

- Use **Markdown** for documentation files
- Include **code examples** for APIs and functions
- Add **docstrings** to all public functions and classes
- Keep documentation **up-to-date** with code changes

### Docstring Format

Use Google-style docstrings:
```python
def currency_converter(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert amount from one currency to another.
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
        
    Returns:
        Dictionary containing conversion result with keys:
        - converted_amount: The converted amount
        - exchange_rate: The rate used for conversion
        - currency: The target currency
        
    Raises:
        ValueError: If currency codes are invalid
        ConnectionError: If exchange rate service is unavailable
        
    Example:
        >>> result = currency_converter(100, "USD", "EUR")
        >>> result["converted_amount"]
        85.0
    """
```

## 🤝 Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the comprehensive README first

### Stay Updated

- **Watch** the repository for notifications
- **Star** the project if you find it useful
- **Follow** the project for updates

## 🙏 Recognition

We value all contributions and will:

- Add contributors to the project's acknowledgments
- Mention significant contributions in release notes
- Provide feedback and support for learning

Thank you for contributing to the MCP Proxy Implementation project! 🚀
