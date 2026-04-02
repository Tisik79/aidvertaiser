# Spec: Google Ads Holiday & Automation Tools for adsmcp

**Date:** 2026-04-02
**Context:** We need to automatically pause all campaigns on Czech state holidays (and re-enable them on the next business day). Google Ads Scripts and Automated Rules are **UI-only** — no API access. However, the Google Ads API fully supports campaign status mutations, bulk operations, and label management.

## Current State

- `google_update_campaign` can already pause/enable individual campaigns
- `google_set_ad_schedule` handles day-of-week scheduling (Mon-Fri already configured)
- No bulk pause/enable, no label management, no date-based scheduling

## What Needs to Be Built

### Tool 1: `google_bulk_set_campaign_status`

**File:** `src/unified_ads_mcp/google/campaigns.py`
**Purpose:** Pause or enable multiple campaigns in a single API call.

```python
@mcp.tool()
async def google_bulk_set_campaign_status(
    campaign_ids: list[str],          # List of campaign IDs
    status: str,                       # ENABLED or PAUSED
    customer_id: str | None = None,
    login_customer_id: str | None = None,
) -> dict:
    """Bulk pause or enable multiple campaigns in one API call.
    
    Uses GoogleAdsService.Mutate for batch efficiency (up to 10,000 ops/request).
    
    Args:
        campaign_ids: List of campaign IDs to update.
        status: Target status - ENABLED or PAUSED.
    
    Returns:
        dict with updated_count, failed_count, and details.
    """
```

**Implementation notes:**
- Use `GoogleAdsService.Mutate` with multiple `campaign_operation` entries
- Each operation sets `campaign.status` and uses field mask `["status"]`
- Return individual success/failure per campaign

### Tool 2: `google_manage_labels`

**File:** `src/unified_ads_mcp/google/campaigns.py` (or new `labels.py`)
**Purpose:** Create labels and assign them to campaigns for grouping (e.g., "holiday-pausable").

```python
@mcp.tool()
async def google_create_label(
    name: str,                         # Label name, e.g. "Holiday Pausable"
    description: str | None = None,
    customer_id: str | None = None,
    login_customer_id: str | None = None,
) -> dict:
    """Create a label for organizing campaigns."""

@mcp.tool()
async def google_list_labels(
    customer_id: str | None = None,
    login_customer_id: str | None = None,
) -> list[dict]:
    """List all labels in the account."""

@mcp.tool()
async def google_assign_label_to_campaigns(
    label_id: str,
    campaign_ids: list[str],
    customer_id: str | None = None,
    login_customer_id: str | None = None,
) -> dict:
    """Assign a label to multiple campaigns."""

@mcp.tool()
async def google_remove_label_from_campaigns(
    label_id: str,
    campaign_ids: list[str],
    customer_id: str | None = None,
    login_customer_id: str | None = None,
) -> dict:
    """Remove a label from multiple campaigns."""
```

**Implementation notes:**
- `LabelService.MutateLabels` for create/delete
- `CampaignLabelService.MutateCampaignLabels` for assignment
- GAQL to query: `SELECT campaign.id FROM campaign_label WHERE label.id = {id}`

### Tool 3: `google_set_holiday_schedule`

**File:** `src/unified_ads_mcp/google/campaigns.py`
**Purpose:** High-level tool that stores holiday dates and campaign targets in a config file. A companion cron/scheduler reads this config daily and pauses/enables campaigns accordingly.

```python
@mcp.tool()
async def google_set_holiday_schedule(
    customer_id: str | None = None,
    campaign_ids: list[str] | None = None,  # Specific campaigns, or all ENABLED if None
    label_id: str | None = None,            # Or all campaigns with this label
    holidays: list[str] | None = None,      # List of dates in YYYY-MM-DD format
    country: str | None = None,             # "CZ", "SK", etc. — uses built-in holiday calendar
    year: int | None = None,                # Year for built-in calendar (default: current)
    login_customer_id: str | None = None,
) -> dict:
    """Configure holiday pausing for campaigns.

    Stores schedule in ~/.unified-ads-mcp/holiday-schedules/{customer_id}.json.
    Use with the companion cron tool to auto-pause/enable.

    Args:
        campaign_ids: Specific campaign IDs to pause on holidays.
        label_id: Alternative — pause all campaigns with this label.
        holidays: Explicit list of holiday dates (YYYY-MM-DD).
        country: Use built-in holiday calendar for this country (CZ, SK, DE, etc.)
        year: Year for the built-in calendar.

    Returns:
        dict with schedule details and next upcoming holiday.
    """
```

### Tool 4: `google_run_holiday_check`

**File:** `src/unified_ads_mcp/google/campaigns.py`
**Purpose:** Check if today is a holiday and pause/enable campaigns accordingly. Designed to be called daily by a cron job.

```python
@mcp.tool()
async def google_run_holiday_check(
    customer_id: str | None = None,
    dry_run: bool = False,
    login_customer_id: str | None = None,
) -> dict:
    """Check today's date against holiday schedule and pause/enable campaigns.

    Reads schedule from ~/.unified-ads-mcp/holiday-schedules/{customer_id}.json.
    - If today IS a holiday and campaigns are ENABLED → pause them
    - If today is NOT a holiday and campaigns are PAUSED (by this tool) → enable them

    Args:
        dry_run: If True, report what would happen without making changes.

    Returns:
        dict with action_taken, campaigns_affected, next_holiday.
    """
```

**Implementation notes:**
- Track which campaigns were paused BY THIS TOOL (not manually by user) in a state file
- Only re-enable campaigns that were auto-paused, not manually paused ones
- State file: `~/.unified-ads-mcp/holiday-state/{customer_id}.json`
- Include `paused_by: "holiday-scheduler"` metadata

## Built-in Czech Holiday Calendar

Embed the Czech holiday calendar directly (no external dependency needed):

```python
CZECH_HOLIDAYS = {
    2026: [
        "2026-01-01",  # New Year's Day
        "2026-04-03",  # Good Friday
        "2026-04-06",  # Easter Monday
        "2026-05-01",  # Labor Day
        "2026-05-08",  # Liberation Day
        "2026-07-05",  # Saints Cyril and Methodius Day
        "2026-07-06",  # Jan Hus Day
        "2026-09-28",  # Czech Statehood Day
        "2026-10-28",  # Independent Czechoslovak State Day
        "2026-11-17",  # Struggle for Freedom and Democracy Day
        "2026-12-24",  # Christmas Eve
        "2026-12-25",  # Christmas Day
        "2026-12-26",  # St. Stephen's Day
    ],
    2027: [
        "2027-01-01",  # New Year's Day
        "2027-03-26",  # Good Friday
        "2027-03-29",  # Easter Monday
        "2027-05-01",  # Labor Day
        "2027-05-08",  # Liberation Day
        "2027-07-05",  # Saints Cyril and Methodius Day
        "2027-07-06",  # Jan Hus Day
        "2027-09-28",  # Czech Statehood Day
        "2027-10-28",  # Independent Czechoslovak State Day
        "2027-11-17",  # Struggle for Freedom and Democracy Day
        "2027-12-24",  # Christmas Eve
        "2027-12-25",  # Christmas Day
        "2027-12-26",  # St. Stephen's Day
    ],
}
```

**Note:** Easter dates change yearly. Use `dateutil.easter` or hardcode. Good Friday = Easter Sunday - 2, Easter Monday = Easter Sunday + 1.

## Scheduling / Cron

The `google_run_holiday_check` tool needs to run **daily at ~00:05 CET**. Options:

1. **MCP-internal cron** — if the MCP server supports background scheduling, add an internal daily check
2. **External cron** — a system cron or Cloud Scheduler that calls the MCP tool via CLI:
   ```bash
   # crontab entry
   5 0 * * * /path/to/mcp-cli call google_run_holiday_check
   ```
3. **Claude Code scheduled trigger** — use the `/schedule` skill to set up a daily agent that calls the tool

**Recommended:** Option 2 (external cron) is simplest and most reliable.

## API References

- [GoogleAdsService.Mutate](https://developers.google.com/google-ads/api/reference/rpc/v22/GoogleAdsService#mutate) — bulk operations
- [LabelService](https://developers.google.com/google-ads/api/reference/rpc/v22/LabelService) — label CRUD
- [CampaignLabelService](https://developers.google.com/google-ads/api/reference/rpc/v22/CampaignLabelService) — assign labels
- [Campaign.status field](https://developers.google.com/google-ads/api/reference/rpc/v22/Campaign) — ENABLED/PAUSED mutation

## Priority

1. **P0:** `google_bulk_set_campaign_status` — needed immediately for manual holiday pausing
2. **P1:** `google_set_holiday_schedule` + `google_run_holiday_check` — automated holiday handling
3. **P2:** Label management tools — nice for organization but not blocking

## Interim Workaround (No Code Required)

Until these tools are built, the AI agent can manually pause campaigns on holidays using existing tools:
```
google_update_campaign(campaign_id="...", status="PAUSED")  # On holiday morning
google_update_campaign(campaign_id="...", status="ENABLED")  # On next business day
```
This can be triggered via Claude Code's `/schedule` feature for a daily check.
