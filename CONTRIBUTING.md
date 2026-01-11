# Contributing to GTM Repository Starter

Thank you for your interest in contributing! This project aims to help teams build compounding knowledge in their go-to-market processes.

## How to Contribute

### 1. Reporting Issues

Found a bug or have a feature request? Please:
- Check [existing issues](https://github.com/mherzog4/cannonballgtm-repo-starter/issues) first
- Use our issue templates for clarity
- Provide as much context as possible

### 2. Suggesting Improvements

We welcome improvements to:
- **Documentation** - Clarifications, examples, typo fixes
- **Pipeline Scripts** - Better implementations, new features
- **Prompt Templates** - More effective AI prompts
- **Example Campaigns** - Real-world use cases
- **Data Schemas** - Support for more CRM systems

### 3. Submitting Changes

#### Small Changes (Documentation, Typos)
- Fork the repo
- Make your changes
- Submit a pull request

#### Larger Changes (New Features, Refactors)
- Open an issue first to discuss
- Get feedback before spending time coding
- Follow the pull request process below

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/cannonballgtm-repo-starter.git
cd cannonballgtm-repo-starter

# Install Python dependencies
pip install pandas pyyaml pyarrow

# Run tests (if you're adding code)
python -m pytest tests/  # (we should add this)
```

## Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow existing code style
   - Add comments where helpful
   - Update documentation if needed

3. **Test Your Changes**
   - Verify Python scripts run without errors
   - Check that documentation renders correctly
   - Test with sample data if applicable

4. **Commit with Clear Messages**
   ```bash
   git commit -m "Add: Brief description of what you added

   - More detailed explanation if needed
   - Use bullet points for multiple changes"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a pull request on GitHub.

6. **Respond to Feedback**
   - Be open to suggestions
   - Make requested changes
   - Keep the conversation productive

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints where helpful
- Add docstrings to functions
- Keep scripts under 300 lines (modularize if longer)

### Markdown
- Use ATX-style headers (`# Header`)
- Include helpful code examples
- Add HTML comments for usage instructions
- Keep lines under 120 characters where possible

### YAML
- Use 2-space indentation
- Add comments explaining complex structures
- Validate YAML before committing

## Documentation Standards

When adding or updating documentation:

1. **Include Usage Context**
   ```markdown
   <!--
   PURPOSE: What this file is for
   HOW TO USE: Step-by-step instructions
   WHEN TO UPDATE: Triggers for updates
   -->
   ```

2. **Provide Examples**
   - Show before/after states
   - Include sample commands
   - Link to related files

3. **Keep It Practical**
   - Focus on "how-to" not just "what"
   - Anticipate common questions
   - Address edge cases

## File Organization

When adding new files:

- **Source templates** → `source/*/`
- **Analysis templates** → `analysis/*/`
- **Prompt templates** → `prompts/`
- **Pipeline scripts** → `pipelines/`
- **Documentation** → `docs/`
- **Examples** → `campaigns/YYYY-MM-DD_example_name/`

## Testing Guidelines

If you're adding Python code:

1. **Test with Sample Data**
   - Create a `tests/fixtures/` directory
   - Use synthetic data (no real PII)
   - Test happy path and edge cases

2. **Document Test Setup**
   ```python
   # tests/test_segment.py
   def test_classify_account():
       """Test that accounts are classified correctly"""
       # Setup
       # Execute
       # Assert
   ```

3. **Run Before Submitting**
   ```bash
   # Add these commands as we build tests
   python -m pytest tests/
   python -m mypy pipelines/
   ```

## What We're Looking For

### High Priority
- Support for more CRM systems (HubSpot, Pipedrive, etc.)
- Additional enrichment provider integrations
- More prompt templates for different use cases
- Real-world example campaigns (anonymized)
- Pipeline improvements (performance, features)

### Medium Priority
- Testing framework setup
- CI/CD automation
- Data validation scripts
- Visualization tools (plotly, matplotlib)

### Always Welcome
- Documentation improvements
- Typo fixes
- Example refinements
- Issue triage and support

## Community Guidelines

- **Be Respectful** - Everyone is learning
- **Be Patient** - Maintainers are volunteers
- **Be Constructive** - Suggest solutions, not just problems
- **Be Collaborative** - Help others in issues and discussions

## Questions?

- 💬 **Discussions** - For general questions, use [GitHub Discussions](https://github.com/mherzog4/cannonballgtm-repo-starter/discussions)
- 🐛 **Bug Reports** - Use the bug report issue template
- 💡 **Feature Requests** - Use the feature request template
- 📧 **Private Inquiries** - For sensitive topics, open a private security advisory

## Recognition

Contributors will be:
- Acknowledged in release notes
- Listed in the README (if desired)
- Appreciated in commit messages

Thank you for making this project better!

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
