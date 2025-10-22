# PR GitHub Agent 🤖

An intelligent PR Agent that analyzes code changes, suggests appropriate PR templates, monitors GitHub Actions workflows, and sends Slack notifications. Built with the Model Context Protocol (MCP) for seamless integration with Claude Code.

## 📋 Overview

This MCP server combines three powerful modules:

1. **PR Template Analysis** - Analyzes git diffs and suggests appropriate PR templates
2. **GitHub Actions Monitoring** - Receives webhook events and tracks CI/CD workflow status
3. **Slack Integration** - Sends formatted notifications to your team about CI/CD results

## 🎯 Features

- 📝 Intelligent PR template suggestions based on code changes
- 🔍 Real-time GitHub Actions workflow monitoring via webhooks
- 💬 Slack notifications for CI/CD failures and successes
- 🛠️ Multiple MCP Tools and Prompts for automated workflows
- ⚡ Handles large diffs with smart output truncation

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **uv package manager** - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **Cloudflare Tunnel (cloudflared)** - [Install cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (for webhook server)
- **Claude Code** - [Install Claude Code](https://claude.ai/download)
- **A Slack Workspace** with webhook permissions

### Environment Variables

You'll need to set up:

- `SLACK_WEBHOOK_URL` - Your Slack incoming webhook URL ([Create a Slack webhook](https://api.slack.com/messaging/webhooks))

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/medhakimbedhief/pr-github-agent
cd pr-github-agent
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
uv venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

Install all required dependencies including dev dependencies:

```bash
uv sync --all-extras
```

This will install:
- `mcp[cli]>=1.0.0` - Model Context Protocol server framework
- `aiohttp>=3.10.0` - Async HTTP for webhook server
- `requests>=2.32.0` - HTTP library for Slack notifications
- `pytest>=8.3.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support

### 4. Configure Environment Variables

Create a `.env` file or set the environment variable:

**Windows (PowerShell):**
```powershell
$env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**macOS/Linux (Bash):**
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

## ✅ Testing Your Implementation

### 1. Validate Your Code

Run the validation script to check your implementation:

```bash
uv run python src/validate_starter.py
```

This script verifies:
- All required tools are implemented
- All required prompts are defined
- Function signatures are correct
- The server can be imported without errors

### 2. Run Unit Tests

Test your implementation with the provided test suite:

```bash
uv run pytest src/test_server.py -v
```

The tests cover:
- Tool functionality
- Error handling
- Output formatting
- Large diff truncation
- Webhook event processing

### 3. Configure Claude Code

Add the MCP server to Claude Code using the CLI:

```bash
# Navigate to the src directory
cd src

# Add the MCP server
claude mcp add pr-agent-slack -- uv --directory . run server.py

# Verify the server is configured
claude mcp list
```

**Alternative: Manual Configuration**

You can also manually add the server to Claude Code's configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pr-agent-slack": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\pr-github-agent\\src", "run", "server.py"]
    }
  }
}
```

## 🎮 Usage

### Basic MCP Server (Module 1)

Start the MCP server to use PR analysis tools:

```bash
cd src
uv run server.py
```

**Available Tools:**
- `analyze_file_changes()` - Get git diff and changed files
- `get_pr_templates()` - List available PR templates
- `suggest_template()` - Get AI-suggested template based on changes

**Available Prompts:**
- `generate_pr_status_report` - Comprehensive PR status with CI/CD info
- `troubleshoot_workflow_failure` - Debug failing workflows

### With GitHub Webhook Integration (Module 2)

To receive real-time GitHub Actions events:

#### 1. Start the Webhook Server

In one terminal:

```bash
cd src
python webhook_server.py
```

This starts a local server on `http://localhost:8080`

#### 2. Start Cloudflare Tunnel

In another terminal:

```bash
cloudflared tunnel --url http://localhost:8080
```

This will output a public URL like: `https://random-words.trycloudflare.com`

#### 3. Configure GitHub Webhook

1. Go to your GitHub repository settings
2. Navigate to **Settings > Webhooks > Add webhook**
3. Set the payload URL: `https://your-tunnel-url.trycloudflare.com/webhook/github`
4. Content type: `application/json`
5. Select events: **Workflow runs** and **Check runs**
6. Click **Add webhook**

**Available Tools (added):**
- `get_recent_actions_events()` - View recent webhook events
- `get_workflow_status()` - Check current workflow states

**Available Prompts (added):**
- `analyze_ci_results` - Analyze recent CI/CD results
- `create_deployment_summary` - Generate deployment summaries
- `generate_pr_status_report` - PR status with CI/CD integration
- `troubleshoot_workflow_failure` - Debug workflow failures

### With Slack Notifications (Module 3)

Ensure `SLACK_WEBHOOK_URL` is set, then use:

**Available Tools (added):**
- `send_slack_notification()` - Send messages to Slack

**Available Prompts (added):**
- `format_ci_failure_alert` - Format CI failure alerts for Slack
- `format_ci_success_summary` - Format success messages for Slack

### Example Workflows

#### Analyze PR and Get Template Suggestion

```bash
# Start Claude Code
claude

# In Claude, ask:
"Analyze my current branch changes and suggest a PR template"
```

Claude will:
1. Call `analyze_file_changes()` to get the diff
2. Analyze the changes to determine the type
3. Call `suggest_template()` with its analysis
4. Provide you with a filled-out template

#### Monitor CI/CD and Notify Team

```bash
# Make sure webhook server and MCP server are running
# In Claude, ask:
"Check recent CI events and notify the team about any failures or successful workflows"
```

Claude will:
1. Call `get_recent_actions_events()` to fetch events
2. Call `get_workflow_status()` to check states
3. Use `format_ci_failure_alert` or `format_ci_success_summary` prompts
4. Call `send_slack_notification()` to send the message

#### Generate Complete PR Status Report

```bash
# In Claude, ask:
"Generate a comprehensive PR status report"
```

Claude will use the `generate_pr_status_report` prompt to:
1. Analyze file changes
2. Check CI/CD status
3. Suggest appropriate PR template
4. Provide recommendations and risk assessment

## 📁 Project Structure

```
pr-github-agent/
├── src/
│   ├── server.py              # Main MCP server (all 3 modules)
│   ├── webhook_server.py      # GitHub webhook receiver
│   ├── test_server.py         # Unit tests
│   ├── validate_starter.py    # Validation script
│   ├── github_events.json     # Stored webhook events (auto-generated)
│   └── .claude/               # Claude Code configuration
├── templates/                 # PR templates
│   ├── bug.md
│   ├── feature.md
│   ├── docs.md
│   ├── refactor.md
│   ├── test.md
│   ├── performance.md
│   └── security.md
├── team-guidelines/           # Team coding standards
│   ├── coding-standards.md
│   └── pr-guidelines.md
├── pyproject.toml            # Project dependencies
├── uv.lock                   # Dependency lock file
└── README.md                 # This file
```

## 🔍 Key Concepts

### MCP Tools

Tools provide Claude with capabilities to interact with external systems:

- **analyze_file_changes** - Retrieves git data
- **get_recent_actions_events** - Reads webhook events from file
- **send_slack_notification** - Sends HTTP requests to Slack

### MCP Prompts

Prompts guide Claude on how to use tools for specific workflows:

- **analyze_ci_results** - Step-by-step CI analysis workflow
- **format_ci_failure_alert** - Slack formatting guidelines
- **generate_pr_status_report** - Comprehensive PR analysis

### Working Directory Considerations

MCP servers run in their installation directory by default. The server uses MCP roots to access Claude Code's current working directory:

```python
context = mcp.get_context()
roots_result = await context.session.list_roots()
working_dir = roots_result.roots[0].uri.path
```

### Output Limiting

Large git diffs can exceed token limits. The server implements smart truncation:

```python
@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True,
    max_diff_lines: int = 500
):
    # Truncates output with informative messages
```

## 🐛 Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure dependencies are installed
uv sync --all-extras
```

**Git errors:**
```bash
# Make sure you're in a git repository
git status
```

**No webhook events received:**
- Check that `webhook_server.py` is running
- Verify Cloudflare tunnel is active
- Confirm GitHub webhook is configured correctly
- Check webhook delivery history in GitHub settings

**Slack notifications not working:**
```bash
# Verify environment variable is set
echo $SLACK_WEBHOOK_URL  # Linux/macOS
echo $env:SLACK_WEBHOOK_URL  # Windows PowerShell
```

**"Response too large" errors:**
- Use `max_diff_lines` parameter to limit output
- Set `include_diff=false` to exclude full diff
- The server defaults to 500 lines, adjust as needed

**Git commands run in wrong directory:**
- The server uses MCP roots to access Claude's working directory
- Ensure Claude Code is opened in the correct project folder

**MCP server not showing in Claude Code:**
```bash
# Verify configuration
claude mcp list

# Check the configuration file exists and is valid JSON
```

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Guide](https://github.com/jlowin/fastmcp)
- [Hugging Face MCP Course - Unit 3](https://huggingface.co/learn/mcp-course/en/unit3/build-mcp-server)
- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## 🎓 Course Modules

This project is part of the Hugging Face MCP Course Unit 3:

1. **Module 1: Build MCP Server** - Core PR analysis tools
2. **Module 2: GitHub Actions Integration** - Webhook monitoring and prompts
3. **Module 3: Slack Notification** - Team communication integration

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💡 Tips for Success

1. **Start simple** - Test each module independently before combining
2. **Use validation scripts** - They catch common issues early
3. **Monitor logs** - Both MCP server and webhook server provide detailed logging
4. **Test incrementally** - Verify each tool works before moving to prompts
5. **Read the course materials** - The Hugging Face course has detailed explanations

## 🎯 Next Steps

After setting up the basic agent, you can:

- Customize PR templates in the `templates/` directory
- Add more workflow analysis tools
- Integrate with other communication platforms
- Extend with custom prompts for your team's workflows
- Add more sophisticated CI/CD analytics

---

Built with ❤️ using [Model Context Protocol](https://modelcontextprotocol.io/)