# How to Use Debug CLI

This guide provides comprehensive instructions for using the Debug CLI tool effectively.

## Table of Contents

- [Quick Start](#quick-start)
- [Basic Usage](#basic-usage)
- [Command Options](#command-options)
- [Configuration](#configuration)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Installation

#### Option A: Python Package
```bash
# Install from source
pip install -e .

# Or install from PyPI (when published)
pip install debug-cli
```

#### Option B: Docker (Cross-Platform)
```bash
# Run with Docker (no Python installation required)
docker run --rm -e OPENAI_API_KEY="your-api-key" debug-cli:latest main --command "your-command" --error "error-output"

# Or use docker-compose for easier management
export OPENAI_API_KEY="your-api-key"
docker-compose run debug-cli main --command "your-command" --error "error-output"
```

### 2. Set Up API Key

**Important**: For global usage (using debug from anywhere on your system), you have two options:

#### Option A: Set Environment Variable (Recommended)
```bash
# Set OpenAI API key for current session
export OPENAI_API_KEY="your-api-key-here"

# For permanent setup, add to your shell profile
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc  # For bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc   # For zsh
```

#### Option B: Create .env File
```bash
# Create .env in your home directory (for global access)
echo "OPENAI_API_KEY=your-api-key-here" > ~/.env

# Or create .env in project directory (only works when in that directory)
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**Note**: The `.env` file must be in the directory where you run the `debug` command, or in your home directory for global access.

### 3. Basic Usage
```bash
# Analyze a failed command
debug main --command "python nonexistent.py" --error "FileNotFoundError: [Errno 2] No such file or directory" --exit-code 2
```

## Basic Usage

### Command Structure
```bash
debug main [OPTIONS]
```

### Required Parameters
When using `--command`, you must also provide:
- `--error`: The error output from the failed command
- `--exit-code`: The exit code of the failed command

### Example
```bash
debug main --command "npm install missing-package" --error "npm ERR! code E404" --exit-code 1
```

## Command Options

### Core Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--last-n` | `-n` | Explain the last N failed commands | `--last-n 3` |
| `--raw` | `-r` | Print raw AI output without formatting | `--raw` |
| `--copy` | `-c` | Copy explanation to clipboard | `--copy` |
| `--verbose` | `-v` | Enable verbose output | `--verbose` |

### Input Options

| Option | Description | Example |
|--------|-------------|---------|
| `--command` | Specific command to analyze | `--command "python script.py"` |
| `--error` | Specific error output to analyze | `--error "ModuleNotFoundError"` |
| `--exit-code` | Exit code for the command | `--exit-code 1` |

### Combined Usage
```bash
# Analyze multiple commands with clipboard copy
debug main --last-n 2 --copy

# Raw output with verbose mode
debug main --command "git push" --error "rejected" --raw --verbose

# Specific command with all options
debug main --command "docker run ubuntu" --error "pull access denied" --exit-code 1 --copy --verbose
```

## Configuration

### Environment Variables

Create a `.env` file in your project root or home directory:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-3.5-turbo
API_TIMEOUT=30
DEFAULT_EXPLANATION_STYLE=detailed
ENABLE_COLORS=true
```

### Configuration Commands
```bash
# Show current configuration
debug config

# Show version information
debug version

# Show help
debug --help
```

## Examples

### Python Errors

#### File Not Found
```bash
debug main --command "python script.py" --error "python: can't open file 'script.py': [Errno 2] No such file or directory" --exit-code 2
```

#### Import Error
```bash
debug main --command "python -c 'import nonexistent'" --error "ModuleNotFoundError: No module named 'nonexistent'" --exit-code 1
```

#### Syntax Error
```bash
debug main --command "python -c 'print('hello'" --error "SyntaxError: unexpected EOF while parsing" --exit-code 1
```

### Node.js/NPM Errors

#### Package Not Found
```bash
debug main --command "npm install missing-package" --error "npm ERR! code E404" --exit-code 1
```

#### Permission Error
```bash
debug main --command "npm install -g package" --error "npm ERR! EACCES: permission denied" --exit-code 1
```

### Git Errors

#### Push Rejected
```bash
debug main --command "git push origin main" --error "error: failed to push some refs" --exit-code 1
```

#### Merge Conflict
```bash
debug main --command "git merge feature-branch" --error "CONFLICT (content): Merge conflict in file.txt" --exit-code 1
```

### Docker Errors

#### Image Pull Failed
```bash
debug main --command "docker run ubuntu" --error "pull access denied for ubuntu" --exit-code 1
```

#### Container Not Found
```bash
debug main --command "docker start mycontainer" --error "Error response from daemon: No such container: mycontainer" --exit-code 1
```

### System Errors

#### Permission Denied
```bash
debug main --command "sudo rm /root/file" --error "rm: cannot remove '/root/file': Permission denied" --exit-code 1
```

#### Command Not Found
```bash
debug main --command "nonexistent-command" --error "bash: nonexistent-command: command not found" --exit-code 127
```

## Docker Usage

### Basic Docker Commands

#### Run Single Command
```bash
# Basic usage
docker run --rm -e OPENAI_API_KEY="your-key" debug-cli:latest main --command "python script.py" --error "error message"

# With verbose output
docker run --rm -e OPENAI_API_KEY="your-key" debug-cli:latest main --command "python script.py" --error "error message" --verbose

# Copy explanation to clipboard
docker run --rm -e OPENAI_API_KEY="your-key" debug-cli:latest main --command "python script.py" --error "error message" --copy
```

#### Interactive Mode
```bash
# Run interactive shell inside container
docker run --rm -it -e OPENAI_API_KEY="your-key" debug-cli:latest bash

# Then use debug commands normally
debug main --command "python script.py" --error "error message"
```

### Docker Compose Usage

#### Setup
```bash
# Create .env file with your API key
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Run with docker-compose
docker-compose run debug-cli main --command "python script.py" --error "error message"
```

#### Development Mode
```bash
# Start development environment
docker-compose --profile dev up debug-cli-dev

# This gives you an interactive shell with the code mounted
```

### Docker Troubleshooting

#### Common Issues

**1. Permission Denied**
```bash
# Fix: Run with proper user permissions
docker run --rm -u $(id -u):$(id -g) -e OPENAI_API_KEY="your-key" debug-cli:latest
```

**2. Shell History Not Available**
```bash
# Fix: Mount shell history files
docker run --rm -e OPENAI_API_KEY="your-key" \
  -v ~/.bash_history:/home/debug-user/.bash_history:ro \
  -v ~/.zsh_history:/home/debug-user/.zsh_history:ro \
  debug-cli:latest
```

**3. Environment Variables Not Working**
```bash
# Fix: Use --env-file
echo "OPENAI_API_KEY=your-key" > .env
docker run --rm --env-file .env debug-cli:latest
```

## Advanced Usage

### Batch Analysis
```bash
# Analyze multiple failed commands
debug main --last-n 3

# Get raw output for scripting
debug main --last-n 2 --raw
```

### Clipboard Integration
```bash
# Copy explanation to clipboard
debug main --command "python test.py" --error "FileNotFoundError" --copy

# Copy multiple explanations
debug main --last-n 2 --copy
```

### Verbose Mode
```bash
# Get detailed debugging information
debug main --command "npm install" --error "package not found" --verbose
```

### Custom Configuration
```bash
# Use different AI model
export OPENAI_MODEL="gpt-4"
debug main --command "python script.py" --error "error" --exit-code 1

# Disable colors
export ENABLE_COLORS=false
debug main --command "python script.py" --error "error" --exit-code 1
```

### Scripting Integration
```bash
# Use in shell scripts
ERROR_OUTPUT=$(python script.py 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    debug main --command "python script.py" --error "$ERROR_OUTPUT" --exit-code $EXIT_CODE --raw
fi
```

### Pipeline Usage
```bash
# Pipe output to other commands
debug main --command "python script.py" --error "error" --raw | grep "Fix Suggestions"

# Save to file
debug main --command "python script.py" --error "error" --raw > explanation.txt
```

## Troubleshooting

### Common Issues

#### API Key Not Set
```
Error: OpenAI API key is required
```
**Solution**: Set the `OPENAI_API_KEY` environment variable or create a `.env` file.

#### .env File Not Found (Global Usage Issue)
```
Error: OpenAI API key is required
```
**Problem**: You're running `debug` from a directory that doesn't contain a `.env` file.

**Solutions**:
1. **Set environment variable** (recommended for global usage):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Create .env in home directory**:
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > ~/.env
   ```

3. **Go to project directory**:
   ```bash
   cd /path/to/debug-cli
   debug config
   ```

#### Command Not Found
```
bash: debug: command not found
```
**Solution**: Make sure the package is installed with `pip install -e .`

#### Permission Denied
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Check file permissions or use `sudo` if necessary.

#### Network Issues
```
ConnectionError: Failed to connect to OpenAI API
```
**Solution**: Check your internet connection and API key validity.

### Debug Mode
```bash
# Enable verbose output for debugging
debug main --command "your-command" --error "error" --verbose
```

### Configuration Issues
```bash
# Check current configuration
debug config

# Validate configuration
debug config --validate
```


## Best Practices

### 1. Global Usage Setup
For using debug CLI from anywhere on your system:

**Recommended Approach**:
```bash
# Add to your shell profile for permanent setup
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc  # For zsh
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc # For bash

# Reload your shell
source ~/.zshrc  # or source ~/.bashrc
```

**Alternative Approach**:
```bash
# Create .env in home directory
echo "OPENAI_API_KEY=your-api-key-here" > ~/.env
```

### 2. Use Specific Error Messages
```bash
# Good: Specific error message
debug main --command "python script.py" --error "FileNotFoundError: [Errno 2] No such file or directory: 'script.py'" --exit-code 2

# Avoid: Generic error message
debug main --command "python script.py" --error "error" --exit-code 1
```

### 2. Include Full Context
```bash
# Good: Include working directory context
debug main --command "python /path/to/script.py" --error "FileNotFoundError" --exit-code 2

# Good: Include command arguments
debug main --command "npm install --save package-name" --error "npm ERR! code E404" --exit-code 1
```

### 3. Use Appropriate Exit Codes
```bash
# Use actual exit codes from failed commands
python script.py
echo $?  # Get the actual exit code
debug main --command "python script.py" --error "error" --exit-code $?
```

### 4. Combine Options Effectively
```bash
# For interactive use: Beautiful formatting
debug main --command "python script.py" --error "error" --exit-code 1

# For scripting: Raw output
debug main --command "python script.py" --error "error" --exit-code 1 --raw

# For sharing: Copy to clipboard
debug main --command "python script.py" --error "error" --exit-code 1 --copy
```

## Integration Examples

### Shell Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias explain='debug main --command "$(history 1 | cut -d" " -f4-)" --error "$(cat /tmp/last_error)" --exit-code $?'

# Usage
python script.py 2> /tmp/last_error
explain
```

### Git Hook
```bash
# In .git/hooks/pre-commit
#!/bin/bash
if ! python -m pytest; then
    debug main --command "python -m pytest" --error "$(python -m pytest 2>&1)" --exit-code $? --copy
    exit 1
fi
```

### CI/CD Integration
```bash
# In GitHub Actions or similar
- name: Debug failed tests
  if: failure()
  run: |
    debug main --command "python -m pytest" --error "$(python -m pytest 2>&1)" --exit-code $? --raw >> debug.log
```

This guide should help you make the most of the Debug CLI tool. For more information, see the main README.md file.
