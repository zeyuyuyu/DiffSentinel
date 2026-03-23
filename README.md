# DiffSentinel

## AI-Powered Git Diff Quality Guardian

DiffSentinel is an intelligent code review assistant that analyzes Git diffs in real-time to detect potential issues before they reach production. Using advanced LLMs and static analysis, it provides actionable insights beyond traditional linting.

### Key Features

- 🤖 AI-powered analysis of semantic changes in diffs
- 🔍 Detection of potential runtime errors and edge cases
- 📊 Impact analysis on system architecture
- 🔐 Security vulnerability scanning in changed dependencies
- 🎯 Smart test coverage suggestions
- 🔄 Automated fix proposals

### Installation

```bash
pip install diffsentinel
```

### Usage

```bash
diffsentinel analyze --diff HEAD~1
```

### Configuration

Create a `diffsentinel.yml` in your project root:

```yaml
model: gpt-6
analyze:
  security: true
  architecture: true
  performance: true
ignore:
  - "*.test.js"
  - "docs/*"
```

### Contributing

Pull requests welcome! See CONTRIBUTING.md for guidelines.

### License

MIT