# TODO

## Backlog

### BUG FIXES (from 2026-03-31 investigation)

- [ ] **ISSUE 1: GTM Timer Trigger `limit` parameter not persisting** — `gtm_update_trigger` only updates `name`, `customEventFilter`, `filter`, and generic `parameter` list. Timer triggers store `eventName`, `interval`, `limit` as top-level GTM `Parameter` objects but `_trigger_to_dict()` does not extract them and `gtm_update_trigger` does not merge them. See `tagmanager/triggers.py:126-167`. FIX: Add `eventName`, `interval`, `limit`, `waitForTags`, `checkValidation`, `waitForTagsTimeout`, `uniqueTriggerId`, `autoEventFilter`, `continuousTimeMinMilliseconds`, `totalTimeMinMilliseconds` to the update body handling. Effort: SMALL.

- [ ] **ISSUE 2: Meta Ads authentication — no browser OAuth flow** — Unlike Google auth (which has a full browser-based OAuth flow in `auth/google_auth.py:227-321`), Meta auth (`auth/meta_auth.py`) only supports pre-configured tokens from `~/meta-ads.yaml` or env vars. The `meta_get_login_link` tool (in `meta/insights.py:121-187`) only returns a URL and instructions — it does NOT complete the OAuth code exchange. Users must manually copy tokens from Graph API Explorer. FIX: Implement browser-based OAuth flow similar to Google (reuse `oauth_server.py`). Effort: MEDIUM.

- [ ] **ISSUE 3: GTM trigger types incomplete** — `_trigger_to_dict()` in `tagmanager/triggers.py:11-22` only extracts 7 fields: triggerId, name, type, filter, customEventFilter, fingerprint, path, parameter. Missing: `eventName`, `interval`, `limit`, `waitForTags`, `checkValidation`, `autoEventFilter`, `uniqueTriggerId`, `maxTimerLengthSeconds`, `verticalScrollPercentageList`, `horizontalScrollPercentageList`, `visibilitySelector`, `visiblePercentage`, `totalTimeMinMilliseconds`, `continuousTimeMinMilliseconds`. Entire families of trigger types lose data on round-trip. FIX: Either pass through the full trigger dict or explicitly handle all trigger-type-specific fields. Effort: SMALL.

### NEW FEATURES (from 2026-03-31 investigation)

- [ ] **ISSUE 4: GA4 Measurement Protocol tools** — No server-side event sending exists. Need `ga4_send_measurement_protocol_event` tool that POSTs to `https://www.google-analytics.com/mp/collect?measurement_id=G-XXX&api_secret=YYY`. Useful for consent-bypassed server-side tracking. Requires: measurement_id, api_secret, client_id, events[]. Effort: MEDIUM.

- [ ] **ISSUE 5: GA4 Measurement Protocol API Secret management** — GA4 Admin API supports `listMeasurementProtocolSecrets` and `createMeasurementProtocolSecret` on data streams. Need `ga4_list_measurement_protocol_secrets(property_id, stream_id)` and `ga4_create_measurement_protocol_secret(property_id, stream_id, display_name)`. Effort: SMALL.

- [ ] **ISSUE 7: Quality Score detail missing from keyword performance** — `google_get_keyword_performance()` in `google/reporting.py:247-360` includes `quality_score` but NOT the sub-components (`creative_quality_score`, `post_click_quality_score`, `search_predicted_ctr`). The detail-level `google_get_keyword()` in `google/keywords.py:157-286` DOES include them. FIX: Add the 3 QS sub-component fields to `get_keyword_performance`. Effort: SMALL.

- [ ] **ISSUE 8: Sklik (Seznam.cz) integration** — No Sklik module exists. Would need: new `sklik/` module with client, campaigns, ad_groups, keywords, reporting. Sklik API: `https://api.sklik.cz/json/v5/`. Auth: API key. Effort: LARGE.

- [ ] **ISSUE 9: Google Ads bid strategy tools** — `google_update_campaign` (campaigns.py:582-692) does NOT support changing bidding strategy. Only supports: name, status, start_date, end_date, network_settings, geo_target_type. `google_create_campaign` only supports `target_spend` (maximize clicks). Missing: `target_cpa`, `target_roas`, `maximize_conversions`, `maximize_conversion_value`, `manual_cpc`, `manual_cpm`. FIX: Add bidding strategy parameters to both create and update. Effort: MEDIUM.

- [ ] **ISSUE 10: No bulk operations** — `google_update_keyword` processes one keyword at a time. When we needed to un-pause 155 keywords, had to make 155 individual API calls. Need `google_batch_update_keywords(updates: list[{ad_group_id, keyword_id, status?, cpc_bid?}])` that batches into a single `mutate_ad_group_criteria` call. Also useful for: batch campaign updates, batch ad group updates. Effort: MEDIUM.

## In Progress

## Blocked

## Done
- [x] Add ONLY_DEFAULT_ACCOUNT configuration to bypass account listing and force a single account id everywhere.
- [x] **2026-03-31 code-investigator**: Full investigation of 10 issues reported. Output: `.plan/investigation-2026-03-31.md`
