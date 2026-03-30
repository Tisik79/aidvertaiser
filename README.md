# Unified Ads MCP Server

A unified MCP (Model Context Protocol) server for managing advertising, analytics, and webmaster tools across multiple platforms.

## Supported Platforms

| Platform | Prefix | Auth Method |
|----------|--------|-------------|
| Google Ads | `google_` | OAuth (browser) |
| Meta Ads | `meta_` | OAuth (browser) |
| Google Analytics (GA4) | `ga4_` | OAuth (browser) |
| Google Search Console | `gsc_` | OAuth (browser) |
| Google Tag Manager | `gtm_` | OAuth (browser) |
| Matomo Analytics | `matomo_` | API token |
| Bing Webmaster Tools | `bing_` | API key |
| PageSpeed Insights | `pagespeed_` | API key (optional) |

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

Also provides access to the **Google Indexing API** for submitting URLs for indexing. Requires the **Web Search Indexing API** to be enabled in Google Cloud Console.

### Google Tag Manager

Create `~/google-tagmanager.yaml` or falls back to `~/google-ads.yaml` for client credentials:

```yaml
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
default_account_id: YOUR_GTM_ACCOUNT_ID  # Optional
default_container_id: YOUR_GTM_CONTAINER_ID  # Optional
```

Or set `GOOGLE_TAGMANAGER_CREDENTIALS` env var.

Requires the **Tag Manager API** to be enabled in Google Cloud Console.

Use `gtm_list_accounts` and `gtm_list_containers` to find your account and container IDs.

### PageSpeed Insights

No config needed for basic usage (rate-limited to ~5 req/min without API key).

Create `~/pagespeed.yaml` for higher rate limits:

```yaml
api_key: YOUR_GOOGLE_API_KEY  # 25,000 requests/day
```

Or set `PAGESPEED_API_KEY` env var.

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

### Google Ads (`google_`) — 44 tools

**Accounts & Reporting:**
- `google_list_accounts` - List accessible Google Ads accounts
- `google_get_account_summary` - Get account overview with metrics
- `google_run_query` - Execute GAQL queries

**Campaigns:**
- `google_list_campaigns` - List campaigns with optional status filter
- `google_get_campaign` - Get single campaign details
- `google_create_campaign` - Create a new campaign
- `google_update_campaign` - Update campaign settings
- `google_delete_campaign` - Remove a campaign
- `google_get_campaign_performance` - Campaign performance metrics
- `google_set_campaign_conversion_goal` - Set conversion goals for a campaign
- `google_create_pmax_campaign` - Create Performance Max campaign

**Ad Groups:**
- `google_list_ad_groups` - List ad groups in a campaign
- `google_get_ad_group` - Get single ad group details
- `google_create_ad_group` - Create a new ad group
- `google_update_ad_group` - Update ad group settings
- `google_delete_ad_group` - Remove an ad group

**Ads:**
- `google_list_ads` - List ads in an ad group
- `google_get_ad` - Get single ad details
- `google_create_responsive_search_ad` - Create responsive search ad
- `google_update_ad` - Update ad content
- `google_delete_ad` - Remove an ad
- `google_get_ad_performance` - Ad performance metrics

**Keywords:**
- `google_list_keywords` - List keywords in an ad group
- `google_get_keyword` - Get single keyword details
- `google_add_keywords` - Add keywords to an ad group
- `google_update_keyword` - Update keyword bid/status
- `google_remove_keyword` - Remove a keyword
- `google_get_keyword_performance` - Keyword performance metrics
- `google_get_search_terms_report` - Search terms triggering ads
- `google_add_negative_keywords` - Add negative keywords to ad group
- `google_list_negative_keywords` - List negative keywords in ad group
- `google_remove_negative_keyword` - Remove a negative keyword
- `google_add_campaign_negative_keywords` - Add campaign-level negative keywords
- `google_list_campaign_negative_keywords` - List campaign negative keywords
- `google_remove_campaign_negative_keyword` - Remove campaign negative keyword

**Conversions:**
- `google_list_conversion_actions` - List conversion actions
- `google_get_conversion_action` - Get conversion action details
- `google_create_conversion_action` - Create conversion action
- `google_update_conversion_action` - Update conversion action
- `google_delete_conversion_action` - Remove conversion action
- `google_get_conversion_action_performance` - Conversion performance
- `google_upload_offline_conversions` - Upload offline conversion data
- `google_upload_enhanced_conversions` - Upload enhanced conversions

**Assets & Performance Max:**
- `google_list_assets` - List account assets
- `google_create_text_asset` - Create a text asset
- `google_create_text_assets_batch` - Create multiple text assets
- `google_create_image_asset` - Create an image asset
- `google_link_asset_to_campaign` - Link asset to campaign
- `google_list_asset_groups` - List PMax asset groups
- `google_get_asset_group` - Get asset group details
- `google_create_asset_group` - Create PMax asset group
- `google_update_asset_group` - Update asset group
- `google_delete_asset_group` - Remove asset group
- `google_add_asset_group_asset` - Add asset to asset group
- `google_remove_asset_group_asset` - Remove asset from group
- `google_get_asset_automation_settings` - Get auto-asset settings
- `google_update_asset_automation_settings` - Update auto-asset settings
- `google_list_auto_created_assets` - List auto-created assets
- `google_remove_auto_created_asset` - Remove auto-created asset

### Meta Ads (`meta_`) — 38 tools

**Accounts:**
- `meta_list_accounts` - List accessible ad accounts
- `meta_get_account_info` - Get account details
- `meta_get_login_link` - Get OAuth login URL

**Campaigns:**
- `meta_list_campaigns` - List campaigns
- `meta_get_campaign_details` - Get campaign details
- `meta_create_campaign` - Create a new campaign
- `meta_update_campaign` - Update campaign settings

**Ad Sets:**
- `meta_list_adsets` - List ad sets
- `meta_get_adset_details` - Get ad set details
- `meta_create_adset` - Create a new ad set
- `meta_update_adset` - Update ad set settings

**Ads & Creatives:**
- `meta_list_ads` - List ads
- `meta_get_ad_details` - Get ad details
- `meta_create_ad` - Create a new ad
- `meta_update_ad` - Update ad settings
- `meta_get_ad_creatives` - Get ad creative details
- `meta_create_creative` - Create ad creative
- `meta_update_creative` - Update ad creative
- `meta_upload_image` - Upload image for ads

**Insights & Reporting:**
- `meta_get_insights` - Get performance reports

**Targeting:**
- `meta_search_interests` - Search interest targeting options
- `meta_get_interest_suggestions` - Get interest suggestions
- `meta_search_behaviors` - Search behavior targeting
- `meta_search_geo_locations` - Search geographic locations
- `meta_estimate_audience_size` - Estimate audience size

**Tracking Pixels:**
- `meta_list_pixels` - List tracking pixels
- `meta_get_pixel` - Get pixel details
- `meta_create_pixel` - Create a tracking pixel
- `meta_update_pixel` - Update pixel settings
- `meta_get_pixel_stats` - Get pixel event statistics

**Conversions:**
- `meta_send_conversion_event` - Send a conversion event
- `meta_send_conversion_events_batch` - Send batch conversion events
- `meta_list_custom_conversions` - List custom conversions
- `meta_get_custom_conversion` - Get custom conversion details
- `meta_create_custom_conversion` - Create custom conversion
- `meta_update_custom_conversion` - Update custom conversion
- `meta_delete_custom_conversion` - Delete custom conversion
- `meta_list_offline_conversion_sets` - List offline conversion sets
- `meta_create_offline_conversion_set` - Create offline conversion set
- `meta_upload_offline_conversions` - Upload offline conversions

### Google Analytics (`ga4_`) — 26 tools

**Accounts & Properties:**
- `ga4_list_accounts` - List GA4 accounts
- `ga4_list_account_summaries` - List account summaries
- `ga4_list_properties` - List properties in an account
- `ga4_get_property` - Get property details
- `ga4_create_property` - Create a new property
- `ga4_update_property` - Update property settings
- `ga4_delete_property` - Remove a property

**Data Streams:**
- `ga4_list_data_streams` - List data streams for a property
- `ga4_get_data_stream` - Get data stream details
- `ga4_create_web_data_stream` - Create web data stream
- `ga4_create_android_data_stream` - Create Android data stream
- `ga4_create_ios_data_stream` - Create iOS data stream
- `ga4_update_data_stream` - Update data stream settings
- `ga4_delete_data_stream` - Remove a data stream
- `ga4_get_tracking_code` - Get tracking code snippet

**Reporting:**
- `ga4_run_report` - Run standard analytics report
- `ga4_run_realtime_report` - Run real-time analytics report
- `ga4_get_metadata` - Discover available dimensions and metrics

**Key Events:**
- `ga4_list_key_events` - List key events (conversions)
- `ga4_create_key_event` - Create a key event
- `ga4_update_key_event` - Update key event settings
- `ga4_delete_key_event` - Remove a key event

**Custom Dimensions:**
- `ga4_list_custom_dimensions` - List all custom dimensions
- `ga4_create_custom_dimension` - Create a custom dimension (e.g. page_type, content_category)
- `ga4_update_custom_dimension` - Update display name or description
- `ga4_archive_custom_dimension` - Archive (soft-delete) a custom dimension

### Google Search Console (`gsc_`) — 18 tools

**Sites:**
- `gsc_list_sites` - List all registered sites
- `gsc_get_site` - Get site details
- `gsc_add_site` - Register a new site
- `gsc_delete_site` - Remove a site

**Search Analytics:**
- `gsc_search_analytics` - Full search traffic data (clicks, impressions, CTR, position)
- `gsc_search_analytics_by_query` - Top search queries (shortcut)
- `gsc_search_analytics_by_page` - Top pages by performance (shortcut)

**URL Inspection:**
- `gsc_inspect_url` - Check indexing status of a URL

**Indexing API:**
- `gsc_submit_url_for_indexing` - Submit a URL to Google for indexing/removal
- `gsc_submit_urls_for_indexing` - Batch submit multiple URLs (~200/day limit)
- `gsc_get_indexing_notification_status` - Check last indexing notification for a URL

**Sitemaps:**
- `gsc_list_sitemaps` - List submitted sitemaps
- `gsc_get_sitemap` - Get sitemap details
- `gsc_submit_sitemap` - Submit a sitemap
- `gsc_delete_sitemap` - Remove a sitemap

**Verification:**
- `gsc_get_verification_token` - Get site verification token
- `gsc_verify_site` - Verify site ownership
- `gsc_list_verified_sites` - List all verified sites

### Matomo Analytics (`matomo_`) — 21 tools

**Sites:**
- `matomo_list_sites` - List all tracked websites
- `matomo_get_site` - Get site details
- `matomo_add_site` - Add a new website
- `matomo_update_site` - Update site settings
- `matomo_delete_site` - Remove a site
- `matomo_get_site_urls` - Get URLs for a site
- `matomo_get_tracking_code` - Get tracking code snippet

**Reporting:**
- `matomo_get_visits_summary` - Basic visit metrics
- `matomo_get_page_urls` - Page URL performance
- `matomo_get_entry_pages` - Top entry pages
- `matomo_get_exit_pages` - Top exit pages
- `matomo_get_referrers` - Referrer sources
- `matomo_get_referrer_types` - Referrer type breakdown
- `matomo_get_search_keywords` - Internal search keywords
- `matomo_get_countries` - Visitor countries
- `matomo_get_devices` - Visitor devices

**Live:**
- `matomo_get_live_counters` - Real-time active visitors
- `matomo_get_last_visits` - Recent visit details
- `matomo_get_visitor_profile` - Individual visitor profile

**Goals:**
- `matomo_list_goals` - List configured goals
- `matomo_add_goal` - Create a new goal
- `matomo_update_goal` - Update goal settings
- `matomo_delete_goal` - Remove a goal
- `matomo_get_goal_report` - Goal conversion report

### Google Tag Manager (`gtm_`) — 14 tools

**Accounts & Containers:**
- `gtm_list_accounts` - List all GTM accounts
- `gtm_list_containers` - List containers in an account
- `gtm_list_workspaces` - List workspaces in a container

**Tags:**
- `gtm_list_tags` - List all tags in a workspace
- `gtm_create_tag` - Create a tag (GA4 event, Google Ads conversion, custom HTML, etc.)
- `gtm_update_tag` - Update tag settings
- `gtm_delete_tag` - Remove a tag

**Triggers:**
- `gtm_list_triggers` - List all triggers in a workspace
- `gtm_create_trigger` - Create a trigger (page view, click, custom event, etc.)
- `gtm_update_trigger` - Update trigger settings
- `gtm_delete_trigger` - Remove a trigger

**Versions & Publishing:**
- `gtm_list_versions` - List container version history
- `gtm_create_version` - Create a version from current workspace state
- `gtm_publish_version` - Publish a version (makes changes live on the website)

### PageSpeed Insights (`pagespeed_`) — 3 tools

- `pagespeed_analyze` - Full Lighthouse audit (scores, Core Web Vitals, opportunities)
- `pagespeed_compare` - Mobile vs desktop side-by-side comparison
- `pagespeed_core_web_vitals` - Chrome UX Report field data (LCP, INP, CLS, FCP, TTFB)

### Bing Webmaster Tools (`bing_`) — 21 tools

**Sites:**
- `bing_list_sites` - List all registered sites
- `bing_add_site` - Register a new site
- `bing_verify_site` - Verify site ownership
- `bing_remove_site` - Remove a site

**URL Submission:**
- `bing_submit_url` - Submit a URL for crawling/indexing
- `bing_submit_url_batch` - Batch submit up to 500 URLs
- `bing_get_url_submission_quota` - Check daily submission quota

**Sitemaps:**
- `bing_list_sitemaps` - List submitted sitemaps
- `bing_submit_sitemap` - Submit a sitemap
- `bing_remove_sitemap` - Remove a sitemap

**Search Analytics:**
- `bing_get_rank_and_traffic_stats` - Overall search performance
- `bing_get_query_stats` - Per-query search metrics
- `bing_get_page_stats` - Per-page search metrics

**Crawl Management:**
- `bing_get_crawl_stats` - Crawl activity statistics
- `bing_get_crawl_issues` - Crawl errors found by Bingbot
- `bing_get_crawl_settings` - Current crawl rate settings
- `bing_save_crawl_settings` - Update crawl rate (1-10)

**Keyword Research:**
- `bing_get_keyword` - Search volume for a keyword (Bing-wide)
- `bing_get_related_keywords` - Related keyword suggestions (Bing-wide)

**Link Analysis:**
- `bing_get_link_counts` - Total inbound link counts
- `bing_get_url_links` - Detailed inbound link list

## Required Google Cloud APIs

Enable these APIs in your [Google Cloud Console](https://console.cloud.google.com/apis/library) for the project matching your `client_id`:

| API | Required for | Enable command |
|-----|-------------|----------------|
| Google Ads API | `google_*` tools | `gcloud services enable googleads.googleapis.com` |
| Google Analytics Admin API | `ga4_*` tools | `gcloud services enable analyticsadmin.googleapis.com` |
| Google Analytics Data API | `ga4_run_report`, `ga4_run_realtime_report` | `gcloud services enable analyticsdata.googleapis.com` |
| Google Search Console API | `gsc_*` tools | `gcloud services enable searchconsole.googleapis.com` |
| Web Search Indexing API | `gsc_submit_url_for_indexing` | `gcloud services enable indexing.googleapis.com` |
| Tag Manager API | `gtm_*` tools | `gcloud services enable tagmanager.googleapis.com` |
| Site Verification API | `gsc_verify_site`, `gsc_get_verification_token` | `gcloud services enable siteverification.googleapis.com` |
| PageSpeed Insights API | `pagespeed_*` (optional, for higher rate limits) | `gcloud services enable pagespeedonline.googleapis.com` |

## Authentication Flow

**OAuth platforms** (Google Ads, Meta, GA4, Search Console, Tag Manager):

1. Server starts a local OAuth callback server on `localhost:8888+`
2. Browser opens automatically with the authentication URL
3. User completes authentication in browser
4. Token is captured and cached to `~/.unified-ads-mcp/`
5. Tokens auto-refresh; Meta short-lived tokens are exchanged for long-lived (60 days)

Each Google OAuth service uses separate tokens cached at:
- `~/.unified-ads-mcp/google_ads_token.json`
- `~/.unified-ads-mcp/google_analytics_token.json`
- `~/.unified-ads-mcp/google_searchconsole_token.json`
- `~/.unified-ads-mcp/google_tagmanager_token.json`
- `~/.unified-ads-mcp/meta_token.json`

To force re-authentication (e.g. after adding new OAuth scopes), delete the relevant token file.

**API key/token platforms** (Matomo, Bing, PageSpeed): No browser flow needed — credentials are read directly from YAML config.

## License

MIT
