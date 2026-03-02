# Notion Output Reference

## Setup

Requires the Notion MCP server. Add to your MCP config:

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

Get your integration token at notion.so/profile/integrations. Share target pages/databases with the integration.

---

## Available Operations

### Pages
- `notion_create_a_page` — Create a new page (in a database or as child of another page)
- `notion_retrieve_a_page` — Get page properties
- `notion_update_page_properties` — Update page properties
- `notion_archive_a_page` — Archive (soft-delete) a page

### Blocks (Content)
- `notion_retrieve_block_children` — Get all child blocks of a page
- `notion_append_block_children` — Add content blocks (paragraphs, headings, lists, code, etc.)
- `notion_update_a_block` — Modify block content
- `notion_delete_a_block` — Delete a block

### Databases
- `notion_create_a_database` — Create a new database
- `notion_query_a_database` — Query with filters and sorts
- `notion_retrieve_a_database` — Get database schema

### Search
- `notion_search` — Full-text search across pages and databases

---

## Building a Strategy Deliverable in Notion

### Recommended Structure

Create a parent page, then build sections as child pages or as blocks within the parent:

1. **Parent page** — Title of the engagement
2. **Executive Summary** — Toggle heading with key findings
3. **Storyline sections** — Each storyline as a heading with supporting content
4. **Data tables** — Use Notion databases for financial data, benchmarks, comparisons
5. **Recommendations** — Callout blocks for actionable items
6. **Appendix** — Collapsible toggle blocks for detailed data

### Block Types for Consulting Content

| Content | Notion Block Type |
|---------|------------------|
| Section headers | `heading_2`, `heading_3` |
| Key findings | `callout` with icon |
| Data tables | `table` or linked database |
| Evidence points | `bulleted_list_item` |
| Recommendations | `numbered_list_item` in callout |
| Charts | Embed image blocks (generate chart images first) |
| Citations | `toggle` block at end of each section |
| Appendix | `toggle` heading blocks (collapsible) |

### Tips

- Use `callout` blocks with colored backgrounds to highlight key recommendations
- Create linked databases for financial comparisons — users can sort/filter
- Use `toggle` blocks for citations so they don't clutter the narrative
- Add a table of contents block at the top for navigation
- Leave collaborative sections (empty blocks with prompts) for team input
