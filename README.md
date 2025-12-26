# Unified Ads MCP Server

A unified MCP (Model Context Protocol) server for managing advertising campaigns across both Google Ads and Meta Ads platforms.

## Features

- **Unified Interface**: Single MCP server for both Google Ads and Meta Ads
- **Browser-based OAuth**: Automatic browser authentication when tokens expire
- **Token Caching**: Persistent token storage at `~/.unified-ads-mcp/`
- **Full CRUD Operations**: Create, read, update, and manage campaigns, ad sets, ads, and more
- **Reporting**: GAQL queries for Google Ads, insights API for Meta Ads

## Installation

```bash
uv sync
```

## Configuration

### Google Ads

Create `~/google-ads.yaml` with:

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
login_customer_id: YOUR_MCC_ID  # Optional, for MCC access
```

Or set `GOOGLE_ADS_CREDENTIALS` environment variable to a custom path.

### Meta Ads

Set environment variables:

```bash
export META_APP_ID=your_app_id  # Optional, has default
export META_APP_SECRET=your_app_secret  # Required for long-lived tokens
export META_ACCESS_TOKEN=your_token  # Optional, bypasses OAuth flow
```

## Usage

### Run the MCP Server

```bash
uv run unified-ads-mcp
```

### MCP Server Configuration

Add to `~/.claude/mcp_servers.json`:

```json
{
  "unified-ads": {
    "command": "uv",
    "args": ["run", "--directory", "/path/to/adsmcp", "unified-ads-mcp"],
    "env": {
      "GOOGLE_ADS_CREDENTIALS": "/path/to/google-ads.yaml",
      "META_APP_ID": "your_app_id",
      "META_APP_SECRET": "your_app_secret"
    }
  }
}
```

## Available Tools

### Google Ads (prefix: `google_`)

- `google_list_accounts` - List accessible accounts
- `google_list_campaigns` - List campaigns with metrics
- `google_create_campaign` - Create new campaigns
- `google_update_campaign` - Update campaign settings
- `google_run_query` - Execute GAQL queries

### Meta Ads (prefix: `meta_`)

- `meta_list_accounts` - List accessible accounts
- `meta_list_campaigns` - List campaigns
- `meta_create_campaign` - Create new campaigns
- `meta_update_campaign` - Update campaign settings
- `meta_get_insights` - Get performance reports

## Authentication Flow

When tokens are missing or expired:

1. Server starts a local OAuth callback server on `localhost:8888+`
2. Browser opens automatically with the authentication URL
3. User completes authentication in browser
4. Token is captured and cached to `~/.unified-ads-mcp/`
5. For Meta, short-lived tokens are exchanged for long-lived (60 days)

## License

MIT
