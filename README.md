# Debug CLI
**AI-Powered Terminal Error Explanation & Analysis Tool**


Transform your debugging workflow with intelligent error analysis, AI-powered explanations, and actionable fix suggestions. Built with modern Python technologies and OpenAI integration for instant, human-readable error explanations.

## Features

### **Intelligent Error Analysis**
- **AI-Powered Explanations**: Get detailed, human-readable explanations for any failed command
- **Root Cause Analysis**: Understand why commands fail with intelligent diagnosis
- **Fix Suggestions**: Receive specific, actionable commands to resolve issues
- **Confidence Scoring**: Know how confident the AI is in its analysis

### **Beautiful Terminal Interface**
- **Rich Formatting**: Beautiful colored output with panels, tables, and structured layouts
- **Multiple Output Modes**: Formatted display for humans, raw text for scripting
- **Cross-Platform**: Works seamlessly on macOS, Linux, and Windows
- **ANSI Colors**: Optional colored output for better readability

### **Flexible Command Analysis**
- **Manual Input**: Analyze specific commands and errors directly
- **History Integration**: Capture and analyze failed commands from shell history
- **Multiple Commands**: Analyze the last N failed commands in sequence
- **Exit Code Handling**: Proper processing of command exit codes

### **Advanced Features**
- **Clipboard Integration**: Copy explanations directly to clipboard
- **Caching System**: Redis caching for common errors to reduce API calls
- **Verbose Mode**: Detailed debugging information for troubleshooting
- **Configuration Management**: Environment-based configuration with validation

## Technology Stack

### **Core Framework**
- **Python 3.9+** - Modern Python with type hints and async support
- **Typer** - Modern CLI framework with automatic help generation
- **Rich** - Beautiful terminal formatting and colored output
- **Pydantic** - Data validation and settings management

### **AI Integration**
- **OpenAI API** - GPT-3.5-turbo for intelligent error analysis
- **Custom Prompts** - Optimized prompts for technical error explanation
- **Response Parsing** - Intelligent parsing of AI responses into structured data
- **Fallback Handling** - Graceful degradation when AI service is unavailable

### **Infrastructure**
- **Docker** - Containerization for easy deployment and reproducibility
- **GitHub Actions** - Automated testing and CI/CD pipeline

### **Development Tools**
- **pytest** - Comprehensive testing framework with coverage reporting
- **Black & isort** - Code formatting and import sorting
- **flake8 & mypy** - Linting and type checking
- **pre-commit** - Git hooks for code quality

## Project Setup

### **Installation**

#### Option 1: Python Package (Recommended)
```bash
# Install from PyPI (when published)
pip install debug-cli

# Or install in development mode
git clone https://github.com/yourusername/debug-cli.git
cd debug-cli
pip install -e ".[dev]"
```

#### Option 2: Docker (Cross-Platform)
```bash
# Run with Docker (no Python installation required)
docker run --rm -e OPENAI_API_KEY="your-api-key" debug-cli:latest main --command "your-command" --error "error-output"

# Or use docker-compose for easier management
export OPENAI_API_KEY="your-api-key"
docker-compose run debug-cli main --command "your-command" --error "error-output"
```

### **Environment Configuration**
Create `.env` file in project root:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Optional: API Configuration
API_TIMEOUT=30

# CLI Configuration
DEFAULT_EXPLANATION_STYLE=detailed
ENABLE_COLORS=true
```

### **Quick Start**
```bash
# Set up API key (for global usage)
export OPENAI_API_KEY="your-api-key-here"

# Analyze a failed command
debug main --command "python nonexistent.py" --error "FileNotFoundError: [Errno 2] No such file or directory" --exit-code 2
```

**Note**: For global usage (using debug from anywhere), set the environment variable or create `.env` in your home directory.

**For detailed usage instructions, see [HOW_TO_USE.md](HOW_TO_USE.md)**

## Project Structure

```
debug-cli/
├── debug_cli/                    # Main CLI package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # CLI entry point and command definitions
│   ├── core/                    # Core functionality
│   │   ├── command_capture.py   # Command history and capture logic
│   │   └── shell_integration.py # Shell integration utilities
│   ├── ai/                      # AI integration
│   │   ├── openai_client.py     # OpenAI API client
│   │   └── explanation_service.py # Explanation generation service
│   ├── utils/                   # Utility functions
│   │   ├── output_formatter.py  # Rich terminal formatting
│   │   ├── clipboard.py         # Cross-platform clipboard integration
│   │   └── config.py            # Configuration management
│   └── models/                  # Data models
│       ├── command.py           # Command and result models
│       └── explanation.py       # Explanation and fix suggestion models
├── tests/                       # Test suite
│   ├── test_models.py           # Model tests
│   └── test_command_capture.py  # Core functionality tests
├── docker/                      # Docker configuration
├── .github/workflows/           # CI/CD pipeline
├── pyproject.toml               # Python packaging configuration
├── Dockerfile                   # Main containerization
├── docker-compose.yml           # Multi-service orchestration
└── README.md                    # This file
```

## CLI Commands

### **Main Commands**
```bash
# Explain failed terminal commands
debug main [OPTIONS]

# Show current configuration
debug config

# Show version information
debug version

# Setup shell integration
debug setup
```

**For complete command documentation and examples, see [HOW_TO_USE.md](HOW_TO_USE.md)**


## Key Features in Detail

### **AI-Powered Error Analysis**
- **Intelligent Parsing**: Advanced prompt engineering for technical error analysis
- **Context Awareness**: Considers command context, working directory, and shell type
- **Structured Output**: Consistent JSON response parsing with fallback handling
- **Confidence Scoring**: Reliability indicators for each explanation and fix

### **Terminal Integration**
- **Shell Detection**: Automatic detection of bash, zsh, fish, and other shells
- **History Parsing**: Intelligent parsing of shell history files
- **Command Capture**: Real-time capture of failed commands and error output
- **Cross-Platform**: Consistent behavior across different operating systems

### **Output Formatting**
- **Rich Display**: Beautiful panels, tables, and colored output using Rich library
- **Raw Mode**: Clean text output for scripting and automation
- **Clipboard Support**: Cross-platform clipboard integration for easy sharing
- **Configurable**: Customizable colors and output styles

### **Performance & Optimization**
- **API Optimization**: Efficient OpenAI API usage with retry logic
- **Response Time**: Sub-3 second response times for most explanations
- **Batch Processing**: Efficient handling of multiple command analysis

## Development

### **Running Tests**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=debug_cli --cov-report=term-missing

# Run specific test file
pytest tests/test_models.py -v
```

### **Code Quality**
```bash
# Linting
flake8 debug_cli/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Type checking
mypy debug_cli/ --ignore-missing-imports

# Code formatting
black debug_cli/ tests/
isort debug_cli/ tests/
```

### **Docker Development**
```bash
# Build Docker image
docker build -t debug-cli:latest .

# Run container
docker run --rm debug-cli:latest debug --help

```

## Examples

**For comprehensive examples and use cases, see [HOW_TO_USE.md](HOW_TO_USE.md)**

### **Quick Examples**
```bash
# Python error
debug main --command "python nonexistent.py" --error "FileNotFoundError: [Errno 2] No such file or directory" --exit-code 2

# NPM error
debug main --command "npm install missing-package" --error "npm ERR! code E404" --exit-code 1

# Git error
debug main --command "git push origin main" --error "error: failed to push some refs" --exit-code 1
```

**Debug CLI** - Transform cryptic errors into actionable insights with AI-powered terminal debugging.