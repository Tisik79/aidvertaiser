# Investigation: adsmcp MCP Server Bugs & Missing Features
Agent: code-investigator | Date: 2026-03-31

## TL;DR

Investigated 10 issues encountered during a marketing/PPC session. Found 3 bugs (GTM trigger update losing timer fields, GTM trigger serialization dropping type-specific data, Meta auth having no browser OAuth flow), 2 gaps in existing tools (keyword performance missing QS sub-components, campaign update missing bid strategy support), and 5 entirely missing features (GA4 Measurement Protocol, GA4 API Secret management, Sklik integration, bulk operations, bid strategy tools).

---

## ISSUE 1: GTM Timer Trigger `limit` parameter not persisting

### Root Cause
**File**: `src/unified_ads_mcp/tagmanager/triggers.py`, lines 126-167

The `gtm_update_trigger()` function fetches the current trigger state (line 149-151), then only overwrites 4 fields if provided: `name`, `customEventFilter`, `filter`, `parameter`. The full trigger body is then sent back to the API.

The ACTUAL bug is more subtle than it first appears. The function does a **read-modify-write** pattern correctly -- it fetches the current trigger, modifies fields the user specified, and sends the full body back. So timer-specific fields like `eventName`, `interval`, `limit` that are already on the trigger SHOULD be preserved because they remain in the `current` dict.

However, the problem is:

1. **The `parameter` field handling**: Timer triggers store `eventName`, `interval`, and `limit` inside the `parameter` array as GTM `Parameter` objects (e.g., `{"type": "template", "key": "eventName", "value": "timer_30s"}`). When the user passes a new `parameter` list to add `limit`, it **replaces the entire parameter array** (line 159: `current["parameter"] = parameter`), potentially dropping existing parameters like `eventName` and `interval`.

2. **No merge logic**: There is no parameter merge -- it's a full replacement. If the caller passes `parameter=[{"type": "template", "key": "limit", "value": "1"}]`, this replaces ALL parameters including the existing eventName and interval entries.

3. **`_trigger_to_dict()` also drops data**: Lines 11-22 only extract 8 fields. The returned data after update is filtered, so fields like `eventName` at the top level (some triggers have it there, not just in parameter array) are invisible.

### What Needs to Change
- **Option A (recommended)**: Add a `merge_parameters` flag to `gtm_update_trigger`. When True, merge new parameters into existing ones by `key` instead of replacing.
- **Option B**: Add dedicated parameters for common trigger-type-specific fields: `event_name`, `interval_millis`, `limit`, `wait_for_tags`, etc. as first-class arguments.
- Fix `_trigger_to_dict()` to include ALL trigger fields (see Issue 3).

### Effort: SMALL (Option A: ~30 lines of merge logic)

---

## ISSUE 2: Meta Ads authentication completely broken

### Root Cause
**Files**: 
- `src/unified_ads_mcp/auth/meta_auth.py` (full file)
- `src/unified_ads_mcp/meta/client.py` (full file)
- `src/unified_ads_mcp/meta/insights.py:121-187` (meta_get_login_link)

Unlike Google Ads auth (`auth/google_auth.py`) which has a complete browser-based OAuth flow:
1. Starts local HTTP server (`oauth_server.py`)
2. Opens browser to Google consent page
3. Receives callback with auth code
4. Exchanges code for access + refresh tokens
5. Persists tokens to `~/.unified-ads-mcp/`

Meta auth (`auth/meta_auth.py`) has **NO browser OAuth flow**. It only supports:
1. `META_ACCESS_TOKEN` environment variable (line 159)
2. `system_user_token` from `~/meta-ads.yaml` (line 170)
3. `access_token` from `~/meta-ads.yaml` (line 183)

The `meta_get_login_link` tool (insights.py:121-187) is a half-measure -- it generates an OAuth URL but:
- Points to `https://localhost:8080/callback` as redirect_uri (not a running server)
- Does NOT start a local callback server
- Does NOT exchange the auth code for a token
- Just tells the user to manually set `META_ACCESS_TOKEN`

Token refresh logic EXISTS (meta_auth.py:99-132 `_refresh_token`) but only works if you already have a valid token + app_secret to exchange for a long-lived token.

### What Needs to Change
Implement full browser-based Meta OAuth flow:
1. Reuse `auth/oauth_server.py` (already supports generic callback endpoints)
2. Create `MetaAdsAuth._browser_auth_flow()` mirroring `GoogleAdsAuth._browser_auth_flow()`
3. Register redirect URI `http://localhost:{port}/callback/meta` in Facebook app settings
4. Exchange auth code at `https://graph.facebook.com/v22.0/oauth/access_token`
5. Get long-lived token exchange if app_secret available
6. Save to `~/.unified-ads-mcp/meta_token.json`

### Effort: MEDIUM (~150 lines, following Google's pattern)

---

## ISSUE 3: GTM trigger `update_trigger` doesn't handle all trigger types

### Root Cause
**File**: `src/unified_ads_mcp/tagmanager/triggers.py`, lines 11-22

`_trigger_to_dict()` only extracts these 8 fields:
```
triggerId, name, type, filter, customEventFilter, fingerprint, path, parameter
```

The GTM API v2 Trigger object has MANY more fields depending on trigger type:

**Timer triggers**: `eventName` (top-level), `interval` (top-level), `limit` (top-level)
**Scroll Depth**: `verticalScrollPercentageList`, `horizontalScrollPercentageList`
**Element Visibility**: `visibilitySelector`, `visiblePercentage`, `totalTimeMinMilliseconds`, `continuousTimeMinMilliseconds`
**Custom Event**: `customEventFilter` (already handled)
**Form Submission**: `waitForTags`, `checkValidation`, `waitForTagsTimeout`
**Click triggers**: `uniqueTriggerId`
**All triggers**: `autoEventFilter`, `notes`, `parentFolderId`

When `gtm_update_trigger` reads the current trigger (line 149), it gets the full object. When it sends it back (line 162-163), the full object IS sent including timer fields. BUT the returned value from `_trigger_to_dict()` (line 165) strips all type-specific fields, making it look like they were lost even if they were persisted.

### What Needs to Change
Replace `_trigger_to_dict()` with either:
- **Option A**: Return the full trigger dict as-is (remove only internal/system fields)
- **Option B**: Add all known trigger fields to the extraction

### Effort: SMALL (5-15 lines)

---

## ISSUE 4: Missing GA4 Measurement Protocol tools

### Root Cause
**No implementation exists.** Searched entire codebase for "measurement_protocol" -- zero results.

The GA4 Measurement Protocol is a simple HTTP POST:
```
POST https://www.google-analytics.com/mp/collect?measurement_id=G-XXX&api_secret=YYY
Content-Type: application/json

{
  "client_id": "abc123",
  "events": [{"name": "form_submit", "params": {"page_title": "Contact"}}]
}
```

### What Needs to Change
New tool: `ga4_send_measurement_protocol_event` in `analytics/measurement_protocol.py`

Parameters:
- `measurement_id`: str (e.g., "G-4EP20G5JZ2")
- `api_secret`: str 
- `client_id`: str (unique per user/device)
- `events`: list of event dicts, each with `name` and optional `params`
- `user_id`: Optional str (for cross-device matching)
- `timestamp_micros`: Optional int
- `non_personalized_ads`: bool = False
- `validate_only`: bool = False (uses `/mp/collect` vs `/debug/mp/collect`)

No authentication needed beyond the API secret -- this is the whole point (server-side, no cookies).

### Effort: MEDIUM (~100 lines including validation endpoint support)

---

## ISSUE 5: No GA4 API Secret management

### Root Cause
**No implementation exists.** The GA4 Admin API supports Measurement Protocol secrets management:
- `properties/{property}/dataStreams/{stream}/measurementProtocolSecrets`

The `analytics/data_streams.py` file manages data streams but has no secret management.

### What Needs to Change
New functions in `analytics/data_streams.py` (or new file `analytics/measurement_protocol.py`):

1. `ga4_list_measurement_protocol_secrets(property_id, stream_id)` 
   - Uses Admin API: `client.list_measurement_protocol_secrets(parent=stream_name)`
   
2. `ga4_create_measurement_protocol_secret(property_id, stream_id, display_name)`
   - Uses Admin API: `client.create_measurement_protocol_secret(parent=stream_name, ...)`
   
3. `ga4_delete_measurement_protocol_secret(property_id, stream_id, secret_id)`

### Effort: SMALL (~80 lines -- straightforward CRUD over Admin API)

---

## ISSUE 6: Google Ads campaign-level negative keywords

### Root Cause: NOT A BUG -- Feature already exists!

**File**: `src/unified_ads_mcp/google/keywords.py`

The following campaign-level negative keyword tools already exist:
- `google_add_campaign_negative_keywords()` (line 741-819) -- adds keywords via `CampaignCriterionService`
- `google_list_campaign_negative_keywords()` (line 822-898) -- lists via GAQL on `campaign_criterion`
- `google_remove_campaign_negative_keyword()` (line 901-948)

These are fully implemented and properly use `CampaignCriterionService` with `criterion.negative = True`.

### Effort: NONE (already implemented)

---

## ISSUE 7: Missing Google Ads Quality Score in keyword performance

### Root Cause
**File**: `src/unified_ads_mcp/google/reporting.py`, lines 247-360

`google_get_keyword_performance()` queries `keyword_view` and includes:
- `ad_group_criterion.quality_info.quality_score` -- YES, included (line 294)

BUT it does NOT include the 3 sub-components:
- `ad_group_criterion.quality_info.creative_quality_score` -- MISSING
- `ad_group_criterion.quality_info.post_click_quality_score` -- MISSING  
- `ad_group_criterion.quality_info.search_predicted_ctr` -- MISSING

Meanwhile, the detail-level `google_get_keyword()` in `keywords.py:157-286` DOES include all 4 QS fields (lines 203-206 in the GAQL query, lines 254-274 in the output).

### What Needs to Change
Add 3 GAQL SELECT fields and 3 output dict entries to `google_get_keyword_performance()`:
```python
# In GAQL SELECT:
ad_group_criterion.quality_info.creative_quality_score,
ad_group_criterion.quality_info.post_click_quality_score,
ad_group_criterion.quality_info.search_predicted_ctr,

# In output dict:
"creative_quality_score": get_enum_name(...),
"post_click_quality_score": get_enum_name(...),
"search_predicted_ctr": get_enum_name(...),
```

### Effort: SMALL (~15 lines)

---

## ISSUE 8: No Sklik (Seznam.cz) integration

### Root Cause
No Sklik module exists anywhere in the codebase. Zero references to "sklik" or "Seznam".

### What Needs to Change
New module: `sklik/` with:
- `client.py` -- API client for `https://api.sklik.cz/json/v5/`
- `campaigns.py` -- list/create/update/delete campaigns
- `ad_groups.py` -- manage ad groups
- `keywords.py` -- keyword management
- `reporting.py` -- stats/reports
- Auth: API key-based (stored in `~/sklik.yaml`)

Sklik API uses JSON-RPC over HTTPS. Each call sends a JSON body with `method` and `params`.

### Effort: LARGE (new integration, 500+ lines, needs Sklik API docs study)

---

## ISSUE 9: Missing Google Ads bid strategy tools

### Root Cause
**File**: `src/unified_ads_mcp/google/campaigns.py`

`google_create_campaign()` (line 264-377) only supports:
- `target_spend: bool = True` -> `campaign.target_spend.target_spend_micros = 0` (maximize clicks)
- Hardcoded P-Max: `campaign.maximize_conversions.target_cpa_micros = 0`

`google_update_campaign()` (line 582-692) does NOT support ANY bidding strategy changes. Its field mask options are: name, status, start_date, end_date, network_settings, geo_target_type.

Missing bidding strategies:
- `target_cpa` (target cost per action)
- `target_roas` (target return on ad spend)
- `maximize_conversions` (with optional target_cpa)
- `maximize_conversion_value` (with optional target_roas)
- `manual_cpc` (with optional enhanced CPC)
- `manual_cpm`

### What Needs to Change
1. **`google_create_campaign`**: Replace `target_spend: bool` with `bidding_strategy: str` and `bidding_target: Optional[float]`
2. **`google_update_campaign`**: Add `bidding_strategy` and `bidding_target` parameters with proper field mask entries

Example:
```python
if bidding_strategy == "TARGET_CPA":
    campaign.target_cpa.target_cpa_micros = currency_to_micros(bidding_target)
    field_mask.append("target_cpa.target_cpa_micros")
elif bidding_strategy == "TARGET_ROAS":
    campaign.target_roas.target_roas = bidding_target  # e.g., 3.0 for 300%
    field_mask.append("target_roas.target_roas")
elif bidding_strategy == "MAXIMIZE_CONVERSIONS":
    campaign.maximize_conversions.target_cpa_micros = 0
    field_mask.append("maximize_conversions")
```

### Effort: MEDIUM (~50 lines in create, ~50 lines in update)

---

## ISSUE 10: No bulk operations

### Root Cause
All mutation tools operate on single entities:
- `google_update_keyword()` (keywords.py:374-455) -- one keyword per call
- `google_update_campaign()` -- one campaign per call
- `google_update_ad_group()` -- one ad group per call

The Google Ads API natively supports batched operations -- `mutate_ad_group_criteria` already accepts a LIST of operations (see how `google_add_keywords` does it at line 355-358). But the update/remove tools only ever create a list of 1 operation.

### What Needs to Change
New batch tools:

1. **`google_batch_update_keywords`**:
   - Input: `updates: list[dict]` where each dict has `{ad_group_id, keyword_id, status?, cpc_bid?}`
   - Build all operations, send in one `mutate_ad_group_criteria` call
   - The API supports up to 5000 operations per request

2. **`google_batch_update_campaigns`**:
   - Input: `updates: list[dict]` where each dict has `{campaign_id, status?, name?}`
   
3. **`google_batch_update_ad_groups`**:
   - Input: `updates: list[dict]` where each dict has `{ad_group_id, status?, cpc_bid?}`

### Effort: MEDIUM (~100 lines per batch tool, pattern is the same)

---

## Key Files

| File | Purpose |
|------|---------|
| `tagmanager/triggers.py` | GTM trigger CRUD -- Issues 1, 3 |
| `auth/meta_auth.py` | Meta token-based auth (no browser flow) -- Issue 2 |
| `meta/client.py` | Meta API client factory -- Issue 2 |
| `meta/insights.py:121-187` | Incomplete `meta_get_login_link` -- Issue 2 |
| `auth/google_auth.py:227-321` | Google browser OAuth (reference pattern) -- Issue 2 |
| `auth/oauth_server.py` | Shared OAuth callback server -- Issue 2 |
| `google/keywords.py` | Keyword management (all CRUD + negatives) -- Issues 6, 10 |
| `google/reporting.py:247-360` | Keyword performance report -- Issue 7 |
| `google/campaigns.py:264-692` | Campaign create/update -- Issue 9 |
| `analytics/data_streams.py` | GA4 data stream CRUD -- Issue 5 |
| `analytics/reporting.py` | GA4 reporting (no Measurement Protocol) -- Issue 4 |
| `server.py` | Tool registration / module imports -- Issues 4, 5, 8 |

## Priority Order (recommended implementation sequence)

1. **Issue 3** -- Fix `_trigger_to_dict()` to preserve all fields (SMALL, prevents data loss)
2. **Issue 1** -- Fix parameter merge in `gtm_update_trigger` (SMALL, bug fix)
3. **Issue 7** -- Add QS sub-components to keyword performance (SMALL, quick win)
4. **Issue 5** -- GA4 API Secret management (SMALL, needed for Issue 4)
5. **Issue 4** -- GA4 Measurement Protocol tool (MEDIUM, needed for consent bypass)
6. **Issue 10** -- Bulk operations (MEDIUM, huge time savings)
7. **Issue 9** -- Bid strategy tools (MEDIUM, critical for PPC optimization)
8. **Issue 2** -- Meta browser OAuth (MEDIUM, needed when Meta ads are used)
9. **Issue 8** -- Sklik integration (LARGE, new platform)

## Watch Out For

- GTM API v2 trigger schema is poorly documented -- different trigger types use different subsets of fields. Test with real timer, scroll, visibility, and form triggers.
- Meta OAuth redirect URI must be registered in Facebook app settings BEFORE the browser flow will work. The current hardcoded `https://localhost:8080/callback` won't work for local HTTP server.
- Google Ads batch operations have a 5000 operations per request limit, but also per-account QPS limits. Add chunking.
- GA4 Measurement Protocol secrets are per-data-stream, not per-property. The Admin API endpoint is `properties/{prop}/dataStreams/{stream}/measurementProtocolSecrets`.
- Sklik API uses JSON-RPC, not REST. Very different pattern from all other integrations.
