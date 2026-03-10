# Unified Ads MCP Server

A unified MCP (Model Context Protocol) server for managing advertising, analytics, and webmaster tools across multiple platforms.

## Supported Platforms

| Platform | Prefix | Auth Method |
|----------|--------|-------------|
| Google Ads | `google_` | OAuth (browser) |
| Meta Ads | `meta_` | OAuth (browser) |
| Google Analytics (GA4) | `ga4_` | OAuth (browser) |
| Google Search Console | `gsc_` | OAuth (browser) |
| Matomo Analytics | `matomo_` | API token |
| Bing Webmaster Tools | `bing_` | API key |

## Installation

```bash
uv sync
```

## Configuration

### Google Ads

Create `~/google-ads.yaml`:

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
login_customer_id: YOUR_MCC_ID  # Optional, for MCC access
default_customer_id: YOUR_DEFAULT_CUSTOMER  # Optional, skip account listing
```

Or set `GOOGLE_ADS_CREDENTIALS` env var to a custom path.

### Meta Ads

Set environment variables:

```bash
export META_APP_ID=your_app_id
export META_APP_SECRET=your_app_secret
export META_ACCESS_TOKEN=your_token  # Optional, bypasses OAuth
```

### Google Analytics (GA4)

Create `~/google-analytics.yaml` or falls back to `~/google-ads.yaml` for client credentials:

```yaml
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
default_property_id: YOUR_PROPERTY_ID  # Optional
```

Or set `GOOGLE_ANALYTICS_CREDENTIALS` env var.

### Google Search Console

Falls back to `~/google-ads.yaml` for client credentials (same Google Cloud project). Token cached at `~/.unified-ads-mcp/google_searchconsole_token.json`.

### Matomo Analytics

Create `~/matomo.yaml`:

```yaml
url: https://your-matomo-instance.com
token_auth: YOUR_API_TOKEN
default_site_id: 1  # Optional
```

Or set `MATOMO_CREDENTIALS` env var.

### Bing Webmaster Tools

Create `~/bing-webmaster.yaml`:

```yaml
api_key: YOUR_API_KEY
default_site_url: https://yoursite.com  # Optional
```

Get the API key from: Bing Webmaster Tools > Settings > API Access > Generate API Key.

Or set `BING_WEBMASTER_CREDENTIALS` env var.

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
      "GOOGLE_ADS_CREDENTIALS": "/path/to/google-ads.yaml"
    }
  }
}
```

## Available Tools

### Google Ads (`google_`)

- `google_list_campaigns` - List campaigns with metrics
- `google_create_campaign` / `google_update_campaign` / `google_delete_campaign`
- `google_list_ad_groups` / `google_create_ad_group` / `google_update_ad_group`
- `google_list_ads` / `google_create_responsive_search_ad` / `google_update_ad`
- `google_list_keywords` / `google_add_keywords` / `google_update_keyword`
- `google_list_conversion_actions` / `google_create_conversion_action`
- `google_run_query` - Execute GAQL queries
- `google_get_campaign_performance` / `google_get_ad_performance`
- Performance Max: `google_create_pmax_campaign`, `google_list_asset_groups`

### Meta Ads (`meta_`)

- `meta_list_campaigns` / `meta_create_campaign` / `meta_update_campaign`
- `meta_list_adsets` / `meta_create_adset` / `meta_update_adset`
- `meta_list_ads` / `meta_create_ad` / `meta_update_ad`
- `meta_get_insights` - Performance reports
- `meta_list_pixels` / `meta_create_pixel` - Tracking pixels
- `meta_search_interests` / `meta_search_behaviors` - Audience targeting
- `meta_send_conversion_event` / `meta_send_conversion_events_batch`

### Google Analytics (`ga4_`)

- `ga4_list_accounts` / `ga4_list_properties`
- `ga4_run_report` - Standard analytics reports
- `ga4_run_realtime_report` - Live data
- `ga4_get_metadata` - Discover available dimensions and metrics
- `ga4_list_data_streams` / `ga4_create_web_data_stream`
- `ga4_get_tracking_code` - Get tracking snippet
- `ga4_list_key_events` / `ga4_create_key_event`

### Google Search Console (`gsc_`)

- `gsc_list_sites` / `gsc_add_site` / `gsc_delete_site`
- `gsc_search_analytics` - Full search traffic data (clicks, impressions, CTR, position)
- `gsc_search_analytics_by_query` / `gsc_search_analytics_by_page` - Quick lookups
- `gsc_inspect_url` - Check indexing status of a URL
- `gsc_list_sitemaps` / `gsc_submit_sitemap` / `gsc_delete_sitemap`

### Matomo Analytics (`matomo_`)

- `matomo_list_sites` / `matomo_add_site` / `matomo_update_site`
- `matomo_get_visits_summary` - Basic visit metrics
- `matomo_get_live_counters` - Real-time active visitors
- `matomo_get_page_urls` / `matomo_get_entry_pages` / `matomo_get_exit_pages`
- `matomo_get_referrers` / `matomo_get_countries` / `matomo_get_devices`
- `matomo_list_goals` / `matomo_add_goal` - Conversion tracking
- `matomo_get_tracking_code` - Get tracking snippet

### Bing Webmaster Tools (`bing_`)

- `bing_list_sites` / `bing_add_site` / `bing_verify_site` / `bing_remove_site`
- `bing_submit_url` / `bing_submit_url_batch` - Submit URLs for indexing
- `bing_get_url_submission_quota` - Check daily submission quota
- `bing_list_sitemaps` / `bing_submit_sitemap` / `bing_remove_sitemap`
- `bing_get_rank_and_traffic_stats` - Overall search performance
- `bing_get_query_stats` / `bing_get_page_stats` - Query/page breakdowns
- `bing_get_crawl_stats` / `bing_get_crawl_issues` - Crawl health
- `bing_get_crawl_settings` / `bing_save_crawl_settings` - Crawl rate control
- `bing_get_keyword` / `bing_get_related_keywords` - Keyword research (Bing-wide)
- `bing_get_link_counts` / `bing_get_url_links` - Backlink analysis

## Authentication Flow

**OAuth platforms** (Google Ads, Meta, GA4, Search Console):

1. Server starts a local OAuth callback server on `localhost:8888+`
2. Browser opens automatically with the authentication URL
3. User completes authentication in browser
4. Token is captured and cached to `~/.unified-ads-mcp/`
5. Tokens auto-refresh; Meta short-lived tokens are exchanged for long-lived (60 days)

**API key/token platforms** (Matomo, Bing): No browser flow needed — credentials are read directly from YAML config.

## License

MIT
