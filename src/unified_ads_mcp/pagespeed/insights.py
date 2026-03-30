"""Google PageSpeed Insights Tools.

Provides MCP tools for running Google PageSpeed Insights audits.
Uses the free REST API at:
    https://www.googleapis.com/pagespeedonline/v5/runPagespeed

No authentication required for basic usage. Optionally configure an API key
via PAGESPEED_API_KEY env var or ~/pagespeed.yaml to increase rate limits.

Configuration (pagespeed.yaml):
    api_key: your_google_api_key  # optional, increases rate limits
"""

import os
from pathlib import Path
from typing import Optional

import httpx
import yaml
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp

API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

_client: Optional[httpx.Client] = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=120.0)
    return _client


def _get_api_key() -> Optional[str]:
    """Load API key from env var or ~/pagespeed.yaml."""
    key = os.environ.get("PAGESPEED_API_KEY")
    if key:
        return key

    config_path = Path.home() / "pagespeed.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
            if config and isinstance(config, dict):
                return config.get("api_key")
    return None


def _run_pagespeed(url: str, strategy: str, categories: list[str]) -> dict:
    """Run PageSpeed Insights API and return parsed results."""
    params: dict = {
        "url": url,
        "strategy": strategy,
    }
    if categories:
        params["category"] = categories  # httpx sends repeated params for lists

    api_key = _get_api_key()
    if api_key:
        params["key"] = api_key

    client = _get_client()
    resp = client.get(API_URL, params=params)

    if resp.status_code == 429:
        raise ToolError(
            "PageSpeed API rate limit exceeded. "
            "Set PAGESPEED_API_KEY env var or configure ~/pagespeed.yaml "
            "with a Google Cloud API key to increase limits."
        )
    if resp.status_code != 200:
        raise ToolError(f"PageSpeed API error {resp.status_code}: {resp.text[:500]}")

    return resp.json()


def _extract_scores(data: dict) -> dict:
    """Extract Lighthouse scores from raw API response."""
    lighthouse = data.get("lighthouseResult", {})
    categories = lighthouse.get("categories", {})

    scores = {}
    for key, cat in categories.items():
        scores[key] = {
            "title": cat.get("title", key),
            "score": int((cat.get("score") or 0) * 100),
        }
    return scores


def _extract_core_web_vitals(data: dict) -> dict:
    """Extract Core Web Vitals from the loading experience."""
    field_data = data.get("loadingExperience", {})
    metrics = field_data.get("metrics", {})

    vitals = {}
    metric_map = {
        "LARGEST_CONTENTFUL_PAINT_MS": "LCP",
        "INTERACTION_TO_NEXT_PAINT": "INP",
        "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS",
        "FIRST_CONTENTFUL_PAINT_MS": "FCP",
        "FIRST_INPUT_DELAY_MS": "FID",
        "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "TTFB",
    }

    for api_key, label in metric_map.items():
        if api_key in metrics:
            m = metrics[api_key]
            vitals[label] = {
                "percentile": m.get("percentile"),
                "category": m.get("category"),
                "distributions": m.get("distributions"),
            }

    vitals["overall_category"] = field_data.get("overall_category", "N/A")
    return vitals


def _extract_opportunities(data: dict, max_items: int = 10) -> list[dict]:
    """Extract top performance opportunities from audits."""
    lighthouse = data.get("lighthouseResult", {})
    audits = lighthouse.get("audits", {})

    # Get performance audit refs to find opportunities
    perf_cat = lighthouse.get("categories", {}).get("performance", {})
    audit_refs = perf_cat.get("auditRefs", [])

    opportunities = []
    for ref in audit_refs:
        if ref.get("group") not in ("load-opportunities", "diagnostics"):
            continue
        audit_id = ref.get("id", "")
        audit = audits.get(audit_id, {})

        score = audit.get("score")
        if score is not None and score < 1:
            item = {
                "id": audit_id,
                "title": audit.get("title", ""),
                "description": audit.get("description", ""),
                "score": int(score * 100) if score is not None else None,
                "displayValue": audit.get("displayValue", ""),
            }
            savings = audit.get("details", {}).get("overallSavingsMs")
            if savings:
                item["savingsMs"] = savings
            opportunities.append(item)

    opportunities.sort(key=lambda x: x.get("savingsMs", 0), reverse=True)
    return opportunities[:max_items]


@mcp.tool()
def pagespeed_analyze(
    url: str,
    strategy: str = "mobile",
) -> dict:
    """Runs a Google PageSpeed Insights audit on a URL.

    Returns Lighthouse scores (Performance, Accessibility, Best Practices,
    SEO), Core Web Vitals from field data, and top performance opportunities.

    This is the main tool for checking website performance. Results include
    both lab data (Lighthouse) and real-world field data (Chrome UX Report)
    when available.

    Args:
        url: The URL to analyze (e.g. "https://example.com").
        strategy: Device strategy - "mobile" (default) or "desktop".

    Returns:
        Dictionary with:
            - scores: Lighthouse category scores (0-100)
            - core_web_vitals: Field data metrics (LCP, INP, CLS, FCP, TTFB)
            - opportunities: Top items to improve, sorted by potential savings
            - final_url: The URL that was actually tested (after redirects)
    """
    if strategy not in ("mobile", "desktop"):
        raise ToolError("strategy must be 'mobile' or 'desktop'")

    try:
        data = _run_pagespeed(
            url, strategy,
            ["performance", "accessibility", "best-practices", "seo"],
        )

        lighthouse = data.get("lighthouseResult", {})

        return {
            "final_url": lighthouse.get("finalUrl", url),
            "strategy": strategy,
            "fetch_time": lighthouse.get("fetchTime", ""),
            "scores": _extract_scores(data),
            "core_web_vitals": _extract_core_web_vitals(data),
            "opportunities": _extract_opportunities(data),
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def pagespeed_compare(
    url: str,
) -> dict:
    """Runs PageSpeed Insights on both mobile and desktop and compares results.

    Useful for identifying mobile-specific performance issues. Returns
    side-by-side scores for both strategies.

    Args:
        url: The URL to analyze (e.g. "https://example.com").

    Returns:
        Dictionary with mobile and desktop scores side by side.
    """
    try:
        categories = ["performance", "accessibility", "best-practices", "seo"]

        mobile_data = _run_pagespeed(url, "mobile", categories)
        desktop_data = _run_pagespeed(url, "desktop", categories)

        mobile_scores = _extract_scores(mobile_data)
        desktop_scores = _extract_scores(desktop_data)

        comparison = {}
        all_keys = set(list(mobile_scores.keys()) + list(desktop_scores.keys()))
        for key in sorted(all_keys):
            m = mobile_scores.get(key, {})
            d = desktop_scores.get(key, {})
            comparison[key] = {
                "title": m.get("title") or d.get("title", key),
                "mobile": m.get("score", "N/A"),
                "desktop": d.get("score", "N/A"),
                "delta": (d.get("score", 0) - m.get("score", 0))
                if isinstance(m.get("score"), int) and isinstance(d.get("score"), int)
                else None,
            }

        return {
            "url": url,
            "comparison": comparison,
            "mobile_vitals": _extract_core_web_vitals(mobile_data),
            "desktop_vitals": _extract_core_web_vitals(desktop_data),
            "mobile_opportunities": _extract_opportunities(mobile_data, 5),
            "desktop_opportunities": _extract_opportunities(desktop_data, 5),
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def pagespeed_core_web_vitals(
    url: str,
    strategy: str = "mobile",
) -> dict:
    """Gets Core Web Vitals field data from Chrome UX Report for a URL.

    Returns real-world performance metrics collected from Chrome users.
    This is the data Google uses for search ranking signals.

    Metrics returned (when available):
        - LCP (Largest Contentful Paint): Should be < 2.5s
        - INP (Interaction to Next Paint): Should be < 200ms
        - CLS (Cumulative Layout Shift): Should be < 0.1
        - FCP (First Contentful Paint): Should be < 1.8s
        - TTFB (Time to First Byte): Should be < 800ms

    Args:
        url: The URL to check (e.g. "https://example.com").
        strategy: Device strategy - "mobile" (default) or "desktop".

    Returns:
        Dictionary with Core Web Vitals metrics, their categories
        (FAST/AVERAGE/SLOW), and distribution percentages.
    """
    if strategy not in ("mobile", "desktop"):
        raise ToolError("strategy must be 'mobile' or 'desktop'")

    try:
        data = _run_pagespeed(url, strategy, ["performance"])

        vitals = _extract_core_web_vitals(data)
        origin_vitals = {}

        origin_data = data.get("originLoadingExperience", {})
        if origin_data:
            origin_metrics = origin_data.get("metrics", {})
            metric_map = {
                "LARGEST_CONTENTFUL_PAINT_MS": "LCP",
                "INTERACTION_TO_NEXT_PAINT": "INP",
                "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS",
                "FIRST_CONTENTFUL_PAINT_MS": "FCP",
                "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "TTFB",
            }
            for api_key, label in metric_map.items():
                if api_key in origin_metrics:
                    m = origin_metrics[api_key]
                    origin_vitals[label] = {
                        "percentile": m.get("percentile"),
                        "category": m.get("category"),
                    }
            origin_vitals["overall_category"] = origin_data.get(
                "overall_category", "N/A"
            )

        return {
            "url": url,
            "strategy": strategy,
            "page_vitals": vitals,
            "origin_vitals": origin_vitals,
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
