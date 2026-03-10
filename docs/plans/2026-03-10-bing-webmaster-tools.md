# Bing Webmaster Tools Integration Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add Bing Webmaster Tools as a new platform integration to the unified ads MCP server, prefixed with `bing_`.

**Architecture:** Follow the Matomo pattern (httpx + API key auth). Bing API uses simple REST with API key as query parameter. Base URL: `https://ssl.bing.com/webmaster/api.svc/json/`. Responses wrapped in `{"d": ...}` envelope.

**Tech Stack:** httpx, pyyaml (already in project), no new dependencies needed.

---

### Task 1: Auth & Client

**Files:**
- Create: `src/unified_ads_mcp/auth/bing_auth.py`
- Create: `src/unified_ads_mcp/bing/__init__.py`
- Create: `src/unified_ads_mcp/bing/client.py`

Config: `~/bing-webmaster.yaml` with `api_key` and optional `default_site_url`. Env override: `BING_WEBMASTER_CREDENTIALS`.

Client: httpx-based, handles `{"d": ...}` envelope unwrapping and ASP.NET date format parsing.

### Task 2: Sites Module

**Files:** Create: `src/unified_ads_mcp/bing/sites.py`

Tools: `bing_list_sites`, `bing_add_site`, `bing_verify_site`, `bing_remove_site`

### Task 3: URL Submissions Module

**Files:** Create: `src/unified_ads_mcp/bing/submissions.py`

Tools: `bing_submit_url`, `bing_submit_url_batch`, `bing_get_url_submission_quota`

### Task 4: Sitemaps Module

**Files:** Create: `src/unified_ads_mcp/bing/sitemaps.py`

Tools: `bing_list_sitemaps`, `bing_submit_sitemap`, `bing_remove_sitemap`

### Task 5: Analytics Module

**Files:** Create: `src/unified_ads_mcp/bing/analytics.py`

Tools: `bing_get_query_stats`, `bing_get_page_stats`, `bing_get_rank_and_traffic_stats`

### Task 6: Crawl Module

**Files:** Create: `src/unified_ads_mcp/bing/crawl.py`

Tools: `bing_get_crawl_stats`, `bing_get_crawl_issues`, `bing_get_crawl_settings`, `bing_save_crawl_settings`

### Task 7: Keywords Module

**Files:** Create: `src/unified_ads_mcp/bing/keywords.py`

Tools: `bing_get_keyword`, `bing_get_related_keywords`

### Task 8: Links Module

**Files:** Create: `src/unified_ads_mcp/bing/links.py`

Tools: `bing_get_link_counts`, `bing_get_url_links`

### Task 9: Server Integration

**Files:** Modify: `src/unified_ads_mcp/server.py`

Add imports for all bing modules and update MCP instructions with Bing section.
