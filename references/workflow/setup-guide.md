# Business Expert Skill — Setup Guide

Practical setup for getting the business-expert skill fully operational. Organized by priority: start at the top, work down.

---

## Contents

- [1. Agent Teams Setup](#1-agent-teams-setup) - Enable peer-to-peer agent communication
- [2. Permission Configuration](#2-permission-configuration) - Allow web access and bash commands
- [3. Required MCP Servers](#3-required-mcp-servers) - Essential MCPs for the skill
- [4. Recommended Data MCPs](#4-recommended-data-mcps) - Domain-specific data sources
- [5. Python Dependencies (API Fallback Scripts)](#5-python-dependencies-api-fallback-scripts) - Backup data access
- [6. Troubleshooting](#6-troubleshooting) - Common issues and solutions

---

## 1. Agent Teams Setup

The skill works best with Claude Code's experimental Agent Teams feature, which enables peer-to-peer agent communication and shared task lists (e.g., a research agent and an analysis agent coordinating on a single deliverable).

Enable it by setting the environment variable:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

To persist across sessions, add it to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) or configure it in `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

If not enabled, the skill falls back to standard single-agent mode. Everything still works — you just lose the multi-agent coordination benefits.

---

## 2. Permission Configuration

To avoid constant approval prompts, add these to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "WebFetch",
      "WebSearch",
      "Bash(python:*)",
      "Bash(npm:*)",
      "Bash(npx:*)"
    ]
  }
}
```

Why each permission is needed:

| Permission | Purpose |
|---|---|
| `Read` | Read data files, configs, and intermediate outputs |
| `Write` | Create reports, YAML process files, and analysis outputs |
| `Edit` | Update existing files (e.g., appending to a running analysis) |
| `Glob` | Find files by pattern (locating data sources, templates, prior reports) |
| `Grep` | Search file contents (finding relevant data points across files) |
| `WebFetch` | Fetch web pages for research (company filings, news, reference data) |
| `WebSearch` | Run web searches to gather market/industry information |
| `Bash(python:*)` | Execute Python scripts for API queries and data processing |
| `Bash(npm:*)` | Install npm packages needed by MCP servers |
| `Bash(npx:*)` | Run MCP servers and Node-based tools |

Note: `--dangerously-skip-permissions` exists as a CLI flag and bypasses all permission checks. Whether to use it is your call.

---

## 3. Required MCP Servers

### Notion MCP

Required only if you want output delivered to Notion.

Add to your MCP config (`~/.claude/claude_desktop_config.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "<your-notion-integration-token>"
      }
    }
  }
}
```

Get your integration token at notion.so/my-integrations. Make sure to share the target database/page with the integration.

---

## 4. Recommended Data MCPs

These provide structured data access. Each one unlocks specific analysis capabilities. Install whichever match your use case.

### Octagon MCP — Company & Financial Data

Provides company financials, funding rounds, investor data, and competitive intelligence.

```json
{
  "mcpServers": {
    "octagon": {
      "command": "npx",
      "args": ["-y", "octagon-mcp@latest"],
      "env": {
        "OCTAGON_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

- API key required. Free tier available at app.octagonai.co.
- Enables: company deep-dives, funding analysis, competitive landscape mapping, investor profiling.

### Yahoo Finance MCP — Stock & Market Data

Provides real-time and historical stock prices, mar and basic company financials.

```json
{
  "mcpServers": {
    "yahoo-finance": {
      "command": "uvx",
      "args": ["mcp-yahoo-finance"]
    }
  }
}
```

- No API key needed. Free.
- Enables: stock performance analysis, market trend tracking, valuation comparisons, portfolio screening.

### FRED MCP — US Macroeconomic Data

Provides Federal Reserve Economic Data: GDP, inflation, employment, interest rates, and hundreds of other US macro indicators.

```json
{
  "mcpServers": {
    "fred": {
      "command": "uvx",
      "args": ["fred-mcp"],
      "env": {
        "FRED_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

- API key required. Free at fred.stlouisfed.org/docs/api/api_key.html.
- Enables: macro environment analysis, economic cycle assessment, policy impact modeling, cross-indicator correlation.

### AkShare MCP — China Macro & Financial Data

Provides China-specific macro data, A-share market data, fund data, and economic indicators.

```json
{
  "mcpServers": {
    "akshare": {
      "command": "uv",
      "args": ["run", "akshare-mcp"]
    }
  }
}
```

- No API key needed. Free.
- Enables: China market analysis, cross-border comparison, RMB/CNY tracking, China macro environment assessment.

### Brave Search MCP — Web Research

General-purpose web search for filling gaps when structured data sources don't cover a topic.

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-brave-search"],
      "env": {
        "BRAVE_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

- API key required. Free tier at brave.com/search/api/.
- Enables: news gathering, industry report discovery, regulatory update tracking, general research fallback.

---

## 5. Python Dependencies (API Fallback Scripts)

When MCP servers aren't available, the skill falls back to Python scripts that query free public APIs directly. Install the dependencies:

```bash
pip install eurostat sdmx1 wbgapi imfp fredapi requests pyyaml
```

What each package covers:

| Package | Data Source |
|---|---|
| `eurostat` | EU statistical data (Eurostat API) |
| `sdmx1` | OECD, ECB, and other SDMX-compatible data providers |
| `wbgapi` | World Bank indicators (GDP, poverty, development) |
| `imfp` | IMF data (balance of payments, exchange rates, global outlook) |
| `fredapi` | US Federal Reseic data (same as FRED MCP, script-based) |
| `requests` | HTTP client for custom API calls |
| `pyyaml` | Read/write YAML process files used by the skill |

---

## 6. Troubleshooting

### "MCP server not found"

- Verify the config is in the right file (`~/.claude/claude_desktop_config.json` for Claude Desktop, `.mcp.json` for project-level).
- Check that the `command` binary exists (`npx`, `uvx`, `uv`) — run `which npx` etc. to confirm.
- Restart Claude after changing MCP config. Servers are loaded at startup.

### "Permission denied"

- Add the relevant permission to your allowlist in `~/.claude/settings.json` (see section 2).
- Alternatively, approve when prompted — the skill will continue after approval.

### "Agent Teams not working"

- Confirm the env variable is set: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` should print `1`.
- If you set it in `settings.json`, restart the session for it to take effect.
- The skill will still work without it — just in single-agent mode.

### "YAML write failed"

- Check that the `process/` directory exists and is writable.
- Run `ls -la` on the skill's working directory to verify permissions.
- If running in a restrvironment, ensure the user has write access to the project folder.

### "API rate limited"

- This happens with free-tier API keys under heavy use.
- The skill will log the gap in its analysis and fall back to web search or cached data.
- Wait a few minutes and retry, or upgrade to a paid API tier for higher limits.
