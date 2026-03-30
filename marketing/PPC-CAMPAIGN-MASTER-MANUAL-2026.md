# PPC CAMPAIGN MASTER MANUAL 2026
## Complete End-to-End Checklist: From Landing Page to Analysis

**Date:** March 2026 | **Platforms:** Google Ads, Microsoft Ads
**Purpose:** AI-executable manual with every setting, every checkbox, every decision point

---

# TABLE OF CONTENTS

1. [PHASE 1: PRE-LAUNCH FOUNDATION](#phase-1-pre-launch-foundation)
2. [PHASE 2: LANDING PAGE SETUP](#phase-2-landing-page-setup)
3. [PHASE 3: TRACKING & CONVERSION SETUP](#phase-3-tracking--conversion-setup)
4. [PHASE 4: ACCOUNT STRUCTURE](#phase-4-account-structure)
5. [PHASE 5: CAMPAIGN CREATION - EVERY SETTING](#phase-5-campaign-creation---every-setting)
6. [PHASE 6: AD GROUP CONFIGURATION](#phase-6-ad-group-configuration)
7. [PHASE 7: KEYWORD STRATEGY](#phase-7-keyword-strategy)
8. [PHASE 8: AD CREATION](#phase-8-ad-creation)
9. [PHASE 9: AUDIENCE TARGETING](#phase-9-audience-targeting)
10. [PHASE 10: BIDDING STRATEGY](#phase-10-bidding-strategy)
11. [PHASE 11: BUDGET MANAGEMENT](#phase-11-budget-management)
12. [PHASE 12: FRAUD PREVENTION & SCAM PROTECTION](#phase-12-fraud-prevention--scam-protection)
13. [PHASE 13: DISPLAY/PMAX/VIDEO/DEMAND GEN SPECIFICS](#phase-13-displaypmaxvideodemand-gen-specifics)
14. [PHASE 14: LAUNCH CHECKLIST](#phase-14-launch-checklist)
15. [PHASE 15: ONGOING OPTIMIZATION CADENCE](#phase-15-ongoing-optimization-cadence)
16. [PHASE 16: REPORTING & ANALYTICS](#phase-16-reporting--analytics)
17. [PHASE 17: COMPETITIVE ANALYSIS](#phase-17-competitive-analysis)
18. [PHASE 18: PRIVACY & COMPLIANCE](#phase-18-privacy--compliance)
19. [APPENDIX A: INDUSTRY BENCHMARKS](#appendix-a-industry-benchmarks)
20. [APPENDIX B: TOOLS & SOFTWARE STACK](#appendix-b-tools--software-stack)

---

# PHASE 1: PRE-LAUNCH FOUNDATION

## 1.1 Business Goals Definition Checklist

- [ ] Define primary campaign objective (leads, sales, awareness, app installs, phone calls)
- [ ] Set target CPA (cost per acquisition) based on business economics
- [ ] Set target ROAS if e-commerce (Revenue / Spend x 100; benchmark: 400% is good)
- [ ] Define customer lifetime value (CLV) to determine max acceptable CPA
- [ ] Identify primary conversion actions (form submit, purchase, phone call, chat)
- [ ] Identify secondary/micro conversions (PDF download, video view, page scroll)
- [ ] Set monthly budget range
- [ ] Define geographic markets
- [ ] Identify target audience personas
- [ ] List competitor URLs for research
- [ ] Determine campaign timeline (ongoing vs. time-bound promotion)

## 1.2 Competitive Research Checklist

- [ ] Run SpyFu/SEMrush on top 5 competitors -- extract their keywords, ad copy, estimated spend
- [ ] Check Google Ads Transparency Center for competitor ad creatives
- [ ] Use SimilarWeb for competitor traffic analysis
- [ ] Document competitor landing pages (screenshot, note offers, CTAs, trust signals)
- [ ] Identify gaps competitors aren't covering
- [ ] Use Ahrefs PPC features for competitive keyword gaps
- [ ] Check iSpionage/Adbeat for Display ad intelligence

## 1.3 Keyword Research Checklist

- [ ] Use Google Keyword Planner -- extract search volume, CPC estimates, competition level
- [ ] Cross-reference with SEMrush/Ahrefs keyword data
- [ ] Group keywords by intent: informational, navigational, commercial, transactional
- [ ] Identify negative keyword seeds from initial research
- [ ] Estimate required budget based on keyword CPCs and desired click volume
- [ ] Check keyword trends for seasonality (Google Trends)
- [ ] Create keyword map: keyword group -> ad group -> landing page

---

# PHASE 2: LANDING PAGE SETUP

## 2.1 Landing Page Selection Rules

| Scenario | Page Type |
|----------|-----------|
| Brand campaign (users searching your name) | Homepage acceptable |
| Product/service specific keywords | Dedicated landing page per ad group |
| High-volume, high-value keyword groups | Unique page per keyword group |
| Low-volume long-tail keywords | Dynamic content on template page |
| Promotions/offers | Dedicated promo landing page |

**Critical rule:** One ad group = one offer = one landing page. NEVER send PPC traffic to a generic homepage for non-brand campaigns.

**Key stat:** Businesses with 40+ landing pages generate 12x more leads than those with 5 or fewer.

## 2.2 Landing Page Design Checklist

### Above-the-Fold (must include ALL):
- [ ] Headline -- matches ad copy exactly (message match = 25% higher conversions)
- [ ] Subheadline -- supports with specifics
- [ ] Hero image or video (video increases conversions up to 80-86%)
- [ ] Primary CTA button -- visible without scrolling
- [ ] Value proposition in 1-2 sentences

### Trust Signals:
- [ ] Customer testimonials (video > text by 80-86%)
- [ ] Client/partner logos
- [ ] Industry certifications/awards
- [ ] Security badges (SSL, Norton, BBB)
- [ ] Money-back guarantee
- [ ] Social proof ("Join 10,000+ users", "4.8/5 from 2,000+ reviews")
- [ ] Privacy policy link visible near forms

### Form Design:
- [ ] 5 or fewer fields (120% better conversion than more fields)
- [ ] Multi-step forms for complex requests (86% higher conversion)
- [ ] Start with easy fields (name, email) before sensitive data
- [ ] Single-column layout
- [ ] Inline validation
- [ ] Clear field labels

### CTA Button:
- [ ] High contrast color (stands out from page, appears nowhere else)
- [ ] Action-oriented text ("Get My Free Trial" not "Submit")
- [ ] Minimum 44x44px tap target for mobile
- [ ] Repeated at logical scroll points
- [ ] Sticky CTA on mobile (27% more clicks)

### Mobile:
- [ ] Fully responsive (83% of traffic is mobile)
- [ ] 16px minimum font size
- [ ] Thumb-friendly buttons
- [ ] Click-to-call phone numbers
- [ ] No horizontal scrolling
- [ ] Single-column layout

### Page Structure (top to bottom):
1. Value proposition (above fold)
2. Benefits (how you solve problems)
3. Features (specifics)
4. Social proof (evidence)
5. Final CTA

## 2.3 Technical Requirements Checklist

- [ ] HTTPS/SSL certificate (mandatory -- non-HTTPS penalized)
- [ ] Core Web Vitals passing:
  - [ ] LCP (Largest Contentful Paint) < 2.5 seconds
  - [ ] INP (Interaction to Next Paint) < 200ms
  - [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] Server response time (TTFB) < 200ms
- [ ] Images optimized (WebP format, lazy loading, srcset for responsive)
- [ ] Image dimensions specified (width/height to prevent CLS)
- [ ] CDN configured for global campaigns (Cloudflare free tier works)
- [ ] No redirect chains (max 1 redirect between ad click and page)
- [ ] `<meta name="robots" content="noindex, nofollow">` for PPC-only pages
- [ ] Do NOT block page via robots.txt (crawler must see noindex tag)
- [ ] Schema markup added (Product, Offer, FAQPage, Review, Organization)
- [ ] Page speed tested on Google PageSpeed Insights, GTmetrix, WebPageTest

**Key stat:** 0.1-second improvement in page speed = 8-10% conversion lift. 53% of mobile users abandon after 3+ seconds.

## 2.4 Post-Click Experience

- [ ] Thank you page optimized (20%+ secondary conversion rate possible)
  - [ ] Confirms action taken
  - [ ] Sets expectations for next steps
  - [ ] Secondary CTA (referral, social share, related content)
  - [ ] Video introducing team or next steps
- [ ] Confirmation email sends immediately
  - [ ] Delivers promised asset
  - [ ] Outlines next steps
  - [ ] Includes social proof reinforcement
  - [ ] Uses real person sender name (not noreply@)
- [ ] Lead nurturing sequence configured:
  - Immediate: Confirmation + asset delivery
  - Day 1-2: Additional value content
  - Day 3-5: Social proof + authority
  - Day 7: Soft pitch
  - Day 10-14: Stronger CTA with urgency
  - Day 21+: Long-term nurture
- [ ] CRM integration (real-time lead flow, no manual entry)
  - [ ] Auto-scoring based on source, keyword, engagement
  - [ ] Auto-assignment to sales reps
  - [ ] Revenue data flows back to Google Ads for ROAS

---

# PHASE 3: TRACKING & CONVERSION SETUP

## 3.1 Google Tag Manager Setup

- [ ] Create GTM container
- [ ] Install GTM snippet in `<head>` and `<body>` of ALL pages
- [ ] Add Google Tag (AW- ID) -- fire on all pages
- [ ] Add Conversion Linker tag -- fire on all pages (critical for attribution)
- [ ] Create conversion tags for each action
- [ ] Set up triggers (form submit, button click, thank-you page view)
- [ ] Test with GTM Preview Mode before publishing
- [ ] Verify with Google Tag Assistant Chrome Extension
- [ ] Allow 24 hours for first conversions to appear

## 3.2 Google Ads Conversion Tracking

- [ ] Create conversion actions in Google Ads (Tools > Measurement > Conversions)
- [ ] For each conversion action, configure:
  - [ ] Conversion name (descriptive)
  - [ ] Category (Purchase, Lead, Sign-up, etc.)
  - [ ] Value: Static value OR dynamic value from page
  - [ ] Count: "One" for leads, "Every" for purchases
  - [ ] Click-through conversion window: 30 days default (range: 1-90 days)
  - [ ] View-through conversion window: 1 day default (range: 1-30 days)
  - [ ] Engaged-view conversion window: Set for video campaigns
  - [ ] Attribution model: Data-Driven (default in 2026) or Last Click
  - [ ] Primary vs Secondary designation:
    - **Primary:** Actions you want to optimize toward (included in bidding)
    - **Secondary:** Tracking-only actions (NOT used in bidding)

## 3.3 Enhanced Conversions Setup

- [ ] Enhanced Conversions for Web:
  - [ ] Enable in Google Ads conversion settings
  - [ ] Implement via GTM, Google tag, or API
  - [ ] Sends hashed first-party data (email, phone, name, address) with conversion
  - [ ] Improves measurement when cookies blocked
- [ ] Enhanced Conversions for Leads:
  - [ ] Upload offline conversion data using GCLID
  - [ ] Or use Enhanced Conversions for Leads tag to pass hashed user data
  - [ ] Critical for B2B/lead-gen to optimize toward actual closed deals

## 3.4 Google Analytics 4 Integration

- [ ] Link GA4 property with Google Ads account
- [ ] Import GA4 conversions into Google Ads (if using GA4 for conversion tracking)
- [ ] Configure UTM parameters on all ads:
  - `utm_source=google` (or `microsoft`)
  - `utm_medium=cpc`
  - `utm_campaign={campaign_name}` or `{_campaign}`
  - `utm_content={creative}` or ad variation identifier
  - `utm_term={keyword}`
- [ ] Set up custom dimensions (client type, lead score, etc.)
- [ ] Create GA4 audiences for remarketing export to Google Ads
- [ ] Enable cross-device tracking (Google signals)
- [ ] Set up Explorations: Funnel analysis, Path analysis, Segment overlap

## 3.5 Event Tracking on Landing Pages

Track ALL of these:
- [ ] Scroll depth: 25%, 50%, 75%, 90%, 100%
- [ ] Button clicks: Primary CTA, secondary CTAs
- [ ] Form interactions: Field focus, field completion, abandonment, submission
- [ ] Video views: Play, 25%, 50%, 75%, completion
- [ ] Time on page: 15s, 30s, 60s thresholds
- [ ] Phone clicks: Click-to-call
- [ ] Chat widget: Opens, messages sent
- [ ] File downloads
- [ ] Exit intent popup: Shown, interacted, converted

## 3.6 Heatmap & Session Recording Setup

- [ ] Install Microsoft Clarity (free, unlimited, recommended as default)
- [ ] Or Hotjar ($39/mo for deeper insights + surveys)
- [ ] Deploy via GTM
- [ ] Configure GDPR/CCPA consent requirement before data collection
- [ ] Review recordings weekly for UX issues

## 3.7 Microsoft Ads: UET Tag

- [ ] Create UET (Universal Event Tracking) tag in Microsoft Ads
- [ ] Install on all pages via GTM
- [ ] Create conversion goals in Microsoft Ads
- [ ] Verify tag fires with UET Tag Helper extension

---

# PHASE 4: ACCOUNT STRUCTURE

## 4.1 Campaign Naming Convention

Use a consistent naming structure:
```
[Campaign Type]_[Product/Service]_[Targeting]_[Match Type]_[Geography]
```
Examples:
- `Search_CRM-Software_Brand_Exact_US`
- `Search_CRM-Software_Competitor_Phrase_US`
- `PMax_CRM-Software_AllAssets_US`
- `Display_CRM-Software_Remarketing_US`
- `Video_CRM-Software_Awareness_YouTube_US`

## 4.2 Campaign Structure Best Practices

- [ ] Separate brand vs non-brand campaigns (always)
- [ ] Separate by match type if using manual bidding
- [ ] Separate by geography if performance varies by region
- [ ] Separate remarketing from prospecting
- [ ] Separate Search from Display (never combine)
- [ ] Keep ad groups tightly themed (5-10 keywords max per ad group)
- [ ] Create separate PMax campaigns alongside Search (PMax takes priority over Display/Shopping but defers to Search for exact match keywords)

## 4.3 Account-Level Settings (Do First)

- [ ] Set account-level conversion goals
- [ ] Set account-level IP exclusions (500 limit at account level)
- [ ] Set account-level placement exclusions for Display (65,000 limit)
- [ ] Set account-level negative keyword lists
- [ ] Link Google Merchant Center (if e-commerce)
- [ ] Link GA4 property
- [ ] Link YouTube channel
- [ ] Set up auto-tagging (should be ON by default)

---

# PHASE 5: CAMPAIGN CREATION - EVERY SETTING

## 5.1 Campaign Type Selection

| Goal | Campaign Type |
|------|--------------|
| High-intent search traffic | Search |
| Brand protection | Search (brand keywords) |
| Product listing ads (e-commerce) | Shopping or Performance Max |
| Retargeting website visitors | Display or Demand Gen |
| YouTube video promotion | Video |
| All Google surfaces (automated) | Performance Max |
| Gmail/YouTube/Discover feed prospecting | Demand Gen |
| App installs/engagement | App |

### Google Ads Campaign Types Available (2026):
1. **Search** (Standard, DSA, AI Max for Search)
2. **Display** (Standard)
3. **Shopping** (Standard)
4. **Video** (Video Reach, Video View, Video Action/Conversions, Sequencing)
5. **Performance Max**
6. **Demand Gen** (formerly Discovery)
7. **App** (Installs, Engagement, Pre-registration)

### Microsoft Ads Campaign Types:
1. Search
2. Shopping
3. Audience
4. Performance Max
5. Shopping for Brands
6. Microsoft Store Ads
7. Audience CTV Video
8. Audience Video

## 5.2 Campaign Settings - Complete Checklist

### Basic Settings:
- [ ] Campaign name (follow naming convention)
- [ ] Campaign status (Paused until ready to launch)
- [ ] Start date
- [ ] End date (if time-bound)

### Network Settings (Search campaigns):
- [ ] **Search Network:** ON (always)
- [ ] **Search Partners:** OFF initially (test later; 2-3x higher fraud rate)
  - Includes YouTube search, Google Maps, Google Shopping, Google Images, non-Google sites
  - Parked domains removed from Search Partners as of Feb 2026
  - Cannot set separate bids; cannot exclude specific partners
- [ ] **Display Network:** OFF for Search campaigns (ALWAYS -- this is a common mistake)
  - Google often auto-includes Display in Search campaigns
  - Creates low-quality Display clicks mixed with Search data
  - Run Display as a separate campaign type

### Location Targeting:
- [ ] Target specific locations (countries, states/provinces, cities, postal codes, radius)
- [ ] **CRITICAL SETTING -- Presence vs Interest:**
  - [ ] Select **"Presence: People in or regularly in your targeted locations"**
  - [ ] DO NOT use "Presence or interest" (default) -- this shows ads to people merely interested in your location who may be anywhere in the world
  - This single setting is the #1 cause of wasted spend from irrelevant geographies
- [ ] Radius targeting: Minimum 1km radius
- [ ] Location groups available (e.g., near airports, universities)
- [ ] Bulk location upload: Up to 1,000 locations
- [ ] Location bid adjustments: -90% to +300%
- [ ] Location exclusions: Exclude regions you don't serve

### Language Targeting:
- [ ] Set language(s) matching your target audience
- [ ] Google matches based on user's Google interface language, not query language
- [ ] "All languages" casts widest net but may include irrelevant clicks

### Bidding Strategy:
(See Phase 10 for detailed guidance)
- [ ] Select appropriate strategy based on data maturity and goals
- [ ] Set bid limits where applicable

### Budget:
(See Phase 11 for detailed guidance)
- [ ] Set daily budget
- [ ] Remember: Google can spend up to 2x daily budget on any day
- [ ] Monthly max = Daily budget x 30.4

### Ad Rotation:
- [ ] **"Optimize"** (recommended) -- Google shows best-performing ads more often
- [ ] "Rotate indefinitely" -- Only use during structured A/B testing

### Ad Schedule (Dayparting):
- [ ] Set days and hours when ads should show
- [ ] Up to 6 schedules per day
- [ ] 15-minute increments available
- [ ] Bid adjustments per schedule: -90% to +900%
- [ ] Base on business hours initially; optimize later with data
- [ ] Consider time zones of target audience

### Campaign URL Options:
- [ ] Tracking template: `{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={_campaign}`
- [ ] Final URL suffix: For additional tracking parameters
- [ ] Custom parameters: Up to 8 custom parameters ({_param1} through {_param8})

### IP Exclusions:
- [ ] Add known fraudulent IPs (up to 500 per campaign)
- [ ] Add competitor office IPs
- [ ] Add your own office IPs (prevent employee clicks)
- [ ] Supports individual IPs and CIDR notation
- [ ] Also set at account level (additional 500)
- [ ] NOTE: Not available for PMax, Video, Hotel, or App campaigns

### Content Exclusions (Display/Video):
- [ ] **Inventory type:**
  - [ ] Expanded inventory (all content)
  - [ ] Standard inventory (recommended -- excludes extreme content)
  - [ ] Limited inventory (strictest -- excludes all sensitive content)
- [ ] **Digital content labels:**
  - [ ] DL-G (General audiences)
  - [ ] DL-PG (Parental guidance)
  - [ ] DL-T (Teen)
  - [ ] DL-MA (Mature)
  - [ ] DL-NR (Not yet rated) -- consider excluding
- [ ] **Sensitive content categories to exclude:**
  - [ ] Tragedy and conflict
  - [ ] Sensitive social issues
  - [ ] Sexually suggestive content
  - [ ] Sensational and shocking
  - [ ] Profanity and rough language
  - [ ] Content suitable for families
- [ ] **Content types to consider excluding:**
  - [ ] Below-the-fold ad slots
  - [ ] Embedded YouTube videos
  - [ ] Live streaming YouTube videos
  - [ ] Parked domains (now removed from SPN as of Feb 2026)

### Brand Settings:
- [ ] Brand restrictions for broad match (limit which brands can trigger ads)
- [ ] Brand exclusions for Search/PMax (prevent ads showing for excluded brand queries)

### Conversion Settings:
- [ ] Choose campaign-level conversion goals (or use account-level defaults)
- [ ] Only set PRIMARY conversions as optimization targets
- [ ] Set secondary conversions for tracking only

### Automatically Created Assets / AI Max:
- [ ] Toggle ON/OFF for automatically generated text
- [ ] Review generated assets regularly
- [ ] AI Max for Search (May 2025): Optional campaign overlay that adds broad match expansion + auto-generated headlines/descriptions + dynamic landing page selection
  - Average 14% conversion lift reported
  - Can be toggled ON/OFF at campaign level

### Device Bid Adjustments:
- [ ] Desktop: Set adjustment (-100% to +900%)
- [ ] Mobile: Set adjustment (-100% to +900%)
- [ ] Tablet: Set adjustment (-100% to +900%)
- [ ] -100% = completely exclude that device type
- [ ] With Smart Bidding: Only -100% honored; all other adjustments handled by algorithm

---

# PHASE 6: AD GROUP CONFIGURATION

## 6.1 Ad Group Settings Checklist

- [ ] Ad group name (descriptive, matches keyword theme)
- [ ] Default bid (for Manual CPC campaigns)
- [ ] Ad group-level URL (if different from campaign)
- [ ] **Optimized Targeting toggle:**
  - [ ] ON for Display prospecting (Google finds users beyond your targeting)
  - [ ] OFF when you need strict audience control (regulated industries, tight budgets)
  - [ ] Enabled by default on new Display campaigns -- check this!
- [ ] Demographic targeting within ad group:
  - [ ] Age: 18-24, 25-34, 35-44, 45-54, 55-64, 65+, Unknown
  - [ ] Gender: Female, Male, Unknown
  - [ ] Parental Status: Parent, Not a Parent, Unknown
  - [ ] Household Income: Top 10%, 11-20%, 21-30%, 31-40%, 41-50%, Lower 50%, Unknown
  - Exclude irrelevant demographics (bid -100%) OR adjust bids based on performance

## 6.2 Ad Group Structure

- [ ] 5-10 keywords per ad group (tightly themed)
- [ ] 2-3 Responsive Search Ads per ad group
- [ ] All keywords in group should logically share the same landing page
- [ ] Create SKAG (Single Keyword Ad Groups) for highest-value keywords only

---

# PHASE 7: KEYWORD STRATEGY

## 7.1 Match Types (2026 Behavior)

| Match Type | Syntax | Behavior (2026) |
|-----------|--------|-----------------|
| **Broad match** | `keyword` | Matches related meanings, synonyms, related searches. With Smart Bidding, uses signals to find relevant queries. |
| **Phrase match** | `"keyword"` | Matches queries including the meaning of your keyword, in the same order. Includes implied words. |
| **Exact match** | `[keyword]` | Matches same meaning/intent. Includes close variants, rewordings, same-intent queries. |

### Match Type Decision:
- [ ] Start with **exact match** for proven, high-converting keywords
- [ ] Add **phrase match** for discovery and expansion
- [ ] Use **broad match** ONLY with Smart Bidding (required for it to work well)
- [ ] With Smart Bidding + broad match, Google uses auction-time signals to match intent

## 7.2 Negative Keywords Checklist

- [ ] Build initial negative keyword list from keyword research (irrelevant terms)
- [ ] Add industry-standard negatives (free, cheap, jobs, salary, DIY, tutorial, etc. -- as appropriate)
- [ ] Create negative keyword lists at account level (shared across campaigns)
- [ ] Levels available:
  - Ad group level negatives
  - Campaign level negatives
  - Account level negatives (new)
  - Negative keyword lists (shared library)
  - PMax: Up to 10,000 campaign-level negative keywords (expanded 2025)
- [ ] Schedule weekly negative keyword mining from Search Terms report
- [ ] Match types for negatives:
  - Broad negative: blocks if ALL negative words appear (any order)
  - Phrase negative: blocks if words appear in that order
  - Exact negative: blocks only that exact query

## 7.3 Quality Score Monitoring

Quality Score = 1-10 scale, based on three components:

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| Expected CTR | ~39% | Predicted click-through rate vs competitors |
| Ad Relevance | ~22% | How well ad matches keyword intent |
| Landing Page Experience | ~39% | Page quality, relevance, speed, navigation |

- [ ] Monitor Quality Score weekly for top keywords
- [ ] Target "Above Average" for all three components
- [ ] Above-average landing page experience = 750% better CVR, 36% lower CPC
- [ ] Fix "Below Average" components before increasing bids

---

# PHASE 8: AD CREATION

## 8.1 Responsive Search Ads (RSA) -- Search Campaigns

### Specifications:
- **Headlines:** Up to 15 (minimum 3). Max 30 characters each
- **Descriptions:** Up to 4 (minimum 2). Max 90 characters each
- **Display URL path:** 2 path fields, 15 characters each
- **Final URL:** Landing page URL

### RSA Best Practices Checklist:
- [ ] Write 15 unique headlines (don't repeat themes)
- [ ] Include keyword in at least 3 headlines
- [ ] Include CTA in at least 2 headlines ("Get Started", "Book Now")
- [ ] Include numbers/stats in at least 2 headlines
- [ ] Include brand name in at least 1 headline
- [ ] Include unique value propositions
- [ ] Write 4 descriptions -- each should stand alone
- [ ] Pin ONLY when absolutely necessary (pinning limits optimization)
  - Pin brand name to Position 1 if required
  - Pin CTA to Position 2 or 3 if needed
- [ ] Aim for "Excellent" ad strength
- [ ] Test 2-3 RSAs per ad group

## 8.2 Ad Assets (Extensions) -- All Types

### Google Ads Assets (add ALL applicable):
- [ ] **Sitelinks:** 4-8 recommended. 25-char headline, 35-char description x2. Link to different pages
- [ ] **Callout extensions:** 25 characters each. Highlight key benefits ("Free Shipping", "24/7 Support")
- [ ] **Structured snippets:** Header + values. Headers: Amenities, Brands, Courses, Destinations, etc.
- [ ] **Call extension:** Business phone number. Set call tracking ON. Set call reporting hours
- [ ] **Location extension:** Link Google Business Profile
- [ ] **Price extension:** Type + items with prices. Minimum 3 items
- [ ] **Promotion extension:** Occasion, promo code, date range
- [ ] **Lead form extension:** Capture leads directly in ad (name, email, phone)
- [ ] **Image extension:** 1200x628 (landscape), 1200x1200 (square). Related to ad content
- [ ] **Business name:** Appears at top of ad
- [ ] **Business logo:** 1200x1200 recommended

### Microsoft Ads Extensions:
- [ ] All of the above equivalents PLUS:
- [ ] **Action extensions:** CTA buttons (Apply Now, Book, Contact Us, etc.)
- [ ] **Multimedia ads:** Large visual ads for Microsoft Audience Network
- [ ] **Video extensions:** Add video to search ads
- [ ] **Filter link extensions:** Filterable options in ads

---

# PHASE 9: AUDIENCE TARGETING

## 9.1 Audience Types Available

### Google Ads:
| Type | Best For | Available In |
|------|----------|-------------|
| **Affinity segments** (~150) | Top-of-funnel awareness | All campaigns |
| **In-market segments** (1000+) | Mid/bottom-funnel intent | All campaigns |
| **Custom segments** | Niche targeting by keywords/URLs/apps | Display, Video, Demand Gen, PMax |
| **Detailed demographics** | Parental status, marital, education, homeowner, employment | All campaigns |
| **Life events** (9 types) | Major milestones (marriage, moving, graduation, etc.) | Display, Video, Demand Gen, PMax |
| **Your data (remarketing)** | Website visitors, app users, YouTube, Customer Match | All campaigns |
| **Combined segments** | AND/OR/NOT logic combinations | Search, Display only |
| **Optimized targeting** | AI-expanded beyond your targeting | Display, Demand Gen |

### Microsoft Ads (unique features):
- [ ] **LinkedIn Profile Targeting** (exclusive to Microsoft):
  - Company (80,000+ companies, up to 1,000 per campaign)
  - Industry (148 industries)
  - Job Function (26 functions)
  - Job Seniority (rolling out)
  - Company Size (rolling out)
  - Performance: +16% CTR, +64% conversion rate vs non-LinkedIn
- [ ] Similar Audiences (still available, unlike Google)
- [ ] Predictive Targeting (AI-driven for Audience ads)

## 9.2 Targeting vs Observation Mode

| Mode | What It Does | When to Use |
|------|-------------|-------------|
| **Targeting** | Only show ads to selected audience | Remarketing, Customer Match, Display prospecting with specific segments |
| **Observation** | Show to everyone but monitor/bid-adjust audiences | All Search campaigns (default), data gathering phase |

**Rules:**
- [ ] Default to Observation mode on Search campaigns
- [ ] Use Targeting mode for remarketing campaigns
- [ ] With Smart Bidding, audiences in Observation mode become automatic bidding signals
- [ ] Never use Targeting on Search unless running a specific RLSA strategy

## 9.3 Customer Match Setup

- [ ] Verify account eligibility (good standing, policy compliance, spend history)
- [ ] Prepare CSV file with columns: `Email, Phone, First Name, Last Name, Country, Zip`
- [ ] Normalize data:
  - Email: lowercase, trim whitespace
  - Phone: E.164 format (+14155552671)
  - Names: lowercase, trim whitespace
- [ ] SHA256 hash: Email, Phone, First Name, Last Name (Country and Zip NOT hashed)
- [ ] Upload via Audience Manager or Data Manager API
- [ ] Expected match rates: 30-70%
- [ ] Include multiple identifiers (email + phone + address) for +10-30% match rate
- [ ] Processing time: 24-72 hours
- [ ] Membership expires at 540 days (April 2025 change) -- refresh regularly
- [ ] **API migration required by April 2026:** Must use Data Manager API (OfflineUserDataJobService deprecated)

## 9.4 Remarketing Lists Setup

- [ ] Create lists in Audience Manager:
  - All website visitors (30, 60, 90 days)
  - Specific page visitors (product pages, pricing page, blog)
  - Cart/form abandoners
  - Past converters (for upsell or exclusion)
  - YouTube viewers, subscribers, channel visitors
- [ ] Minimum list sizes (Dec 2025 update):
  - Display: 100 active users
  - Search (RLSA): 100 (some accounts still 1,000)
  - Shopping: 100
  - YouTube: 100 (some accounts still 1,000)
  - Demand Gen: 1,000
  - PMax: No strict minimum
- [ ] Maximum membership: 540 days
- [ ] Recommended durations:
  - Cart abandoners: 7-30 days
  - Product page visitors: 30-90 days
  - General visitors: 30-180 days

## 9.5 Audience Exclusions Checklist

EXCLUDE these audiences:
- [ ] Recent converters (7-30 day window based on buying cycle)
- [ ] Existing customers (from acquisition campaigns)
- [ ] Careers/jobs page visitors (job seekers, not buyers)
- [ ] Competitor employees (upload list if available)
- [ ] Your own employees (upload email list)
- [ ] Support/help page visitors (already customers)
- [ ] Disengaged visitors (GA4 low-engagement audience)
- [ ] Overlapping audiences between campaigns (prevent double-serving)
- [ ] Non-converting segments identified from data

## 9.6 Audience Bid Adjustments (Manual CPC Only)

| Audience | Starting Bid Adjustment |
|----------|------------------------|
| Cart abandoners | +50% to +150% |
| Pricing page visitors | +30% to +100% |
| Past converters (upsell) | +20% to +80% |
| General website visitors | +10% to +30% |
| In-market segments | +10% to +25% |
| Affinity segments | +0% to +10% |
| Non-converting audiences | -30% to -90% |

**With Smart Bidding:** Manual adjustments are overridden. Focus on providing quality audience signals instead.

## 9.7 RLSA (Remarketing Lists for Search Ads) Strategies

- [ ] Strategy 1: Bid-Only -- Add audiences in Observation mode, increase bids for past visitors
- [ ] Strategy 2: Target-Only -- Separate campaigns targeting ONLY past visitors with broader keywords
- [ ] Strategy 3: Keyword Broadening -- Use broad match for past visitors (too expensive for cold traffic)
- [ ] Strategy 4: Custom Ad Copy -- Tailored messaging for returning visitors ("Welcome back")
- [ ] Implementation flow: Observation (2-4 weeks data) -> Analyze -> Targeting for top performers

## 9.8 Sequential Messaging / Funnel Stages

| Stage | Audience | Message Type | Exclude |
|-------|----------|-------------|---------|
| Top (Cold) | Affinity, broad in-market, custom | Problem awareness, education | Stage 2+3 audiences |
| Middle (Warm) | Site visitors 30-90d, YouTube engagers | Trust, social proof, case studies | Stage 3 audiences + converters |
| Bottom (Hot) | Cart abandoners 7-14d, pricing visitors | Direct CTA, offers, urgency | Recent converters |

---

# PHASE 10: BIDDING STRATEGY

## 10.1 Strategy Selection Guide

| Your Situation | Recommended Strategy |
|---------------|---------------------|
| New account, no conversion data | Manual CPC |
| Small budget <$2K/mo | Manual CPC |
| Building traffic, no conversion tracking | Maximize Clicks (set max CPC limit!) |
| Brand protection | Target Impression Share (set max CPC limit!) |
| Lead gen, equal-value leads, 15-30 conv/mo | Maximize Conversions |
| Lead gen, equal-value leads, 30+ conv/mo | Target CPA |
| E-commerce, varying product values, 30+ conv/mo | Maximize Conversion Value -> Target ROAS |
| Video awareness (YouTube) | CPV or tCPM |
| Display brand awareness | vCPM or tCPM |
| Multiple similar campaigns | Portfolio strategy + shared budget |

### Progression Path:
1. Manual CPC (build baseline data)
2. Maximize Conversions (15-30 conversions/month)
3. Target CPA or Target ROAS (30-50+ conversions/month)

## 10.2 Bidding Strategy Details

### Target CPA Requirements:
- Minimum: 15 conversions in 30 days (Google min)
- Recommended: 30+ conversions in 30 days
- Daily budget: At least 2-3x your target CPA
- Set initial target at or slightly above actual average CPA
- Lower by no more than 20% per week

### Target ROAS Requirements:
- Minimum: 30 conversions in 30 days
- Recommended: 50+ conversions in 30 days
- Requires accurate conversion value tracking
- Formula: ROAS = (Revenue / Spend) x 100
- Industry average: 200% (2:1); Common target: 400% (4:1)

### Enhanced CPC: DEPRECATED (March 31, 2025)
- Campaigns auto-migrated to Manual CPC
- If you see eCPC on old campaigns, it was force-changed

## 10.3 Learning Period Management

### What Triggers Learning:
1. New campaign/strategy
2. Bid strategy change
3. Target CPA/ROAS change
4. Budget change >20%
5. Conversion action change
6. Targeting changes
7. Adding/removing significant keywords (>20%)

### Duration: 7-30 days (typically ~14 days, ~50 conversion events)

### Rules During Learning:
- [ ] DO NOT make additional changes
- [ ] DO NOT panic at volatile performance
- [ ] DO NOT switch strategies mid-learning
- [ ] Make ONE change at a time, wait one week
- [ ] Follow the **20% rule**: Max 20% change to budget/bids per week
- [ ] Use graduated budget approach: 60% week 1, 80% week 2, 100% after learning

### "Limited by Learning" Fix:
- [ ] Check conversion volume (need 30-50/month)
- [ ] Ensure budget >= 2-3x target CPA
- [ ] Consolidate campaigns to pool data
- [ ] Consider less data-hungry strategy (Maximize Conversions instead of Target CPA)

## 10.4 Bid Adjustments Reference

| Type | Range | Level | Smart Bidding Compatible? |
|------|-------|-------|--------------------------|
| Device | -100% to +900% | Campaign/Ad Group | Only -100% |
| Location | -90% to +900% | Campaign | No |
| Ad Schedule | -90% to +900% | Campaign | No |
| Audience | -90% to +900% | Campaign/Ad Group | No |
| Demographics (Age) | -90% to +900% | Campaign/Ad Group | No |
| Demographics (Gender) | -90% to +900% | Campaign/Ad Group | No |
| Demographics (HHI) | -90% to +900% | Campaign/Ad Group | No |
| Interactions (Calls) | -90% to +900% | Campaign | No |

**Compounding formula:** Final Bid = Base x (1 + Adj1) x (1 + Adj2) x ...
Example: $1 bid + 10% schedule + 20% location = $1 x 1.10 x 1.20 = $1.32

## 10.5 Smart Bidding Signals

Google uses 70M+ signal combinations at auction time:
- Device, OS, browser
- Physical location (city level)
- Location intent
- Time of day, day of week
- Actual search query
- Demographics (age, gender, HHI)
- Remarketing list membership
- Customer Match membership
- Ad creative being shown
- Search history patterns
- Cross-device behavior
- Price competitiveness (Shopping)

### Seasonality Adjustments:
- [ ] Set for expected conversion rate changes (sales, holidays)
- [ ] Best for 1-7 day events
- [ ] Modifier range: 0.1 to 10.0 (1.0 = no change, 2.0 = double conversion rate expected)
- [ ] Tools > Budgets and bidding > Adjustments > Seasonal

### Data Exclusions:
- [ ] Exclude date ranges with bad tracking data
- [ ] Prevents Smart Bidding from learning incorrect patterns
- [ ] Tools > Shared library > Bid strategies > Advanced controls

### Conversion Value Rules:
- [ ] Adjust conversion values by location, device, or audience
- [ ] Multiply: 0.5x to 10x
- [ ] Add: Static dollar amount
- [ ] Set: Override to fixed value
- [ ] Only for information Google doesn't already know (e.g., LTV)

---

# PHASE 11: BUDGET MANAGEMENT

## 11.1 Budget Rules

- **Daily budget x 30.4 = Monthly maximum** (you never pay more)
- Google can spend up to **2x daily budget** on any single day
- Only **Standard delivery** available (spreads spend throughout day)

## 11.2 Budget Allocation Model

**The 70/20/10 Rule:**
- 70% to proven, consistently performing campaigns
- 20% to optimization and scaling experiments
- 10% to high-risk/high-reward tests

## 11.3 Budget Checklist

- [ ] Set daily budgets per campaign
- [ ] For Target CPA: Daily budget >= 2-3x target CPA
- [ ] For Maximize Conversions: Budget IS the control lever -- set carefully
- [ ] Consider shared budgets for campaigns with same goal (pooled with portfolio strategy = +13% conversions)
- [ ] Plan seasonal budget increases in advance (gradual, not sudden)
- [ ] Use Performance Planner for forecasting
- [ ] Check pacing every Friday: (Monthly Budget - MTD Spend) / Days Remaining = Real Daily Limit
- [ ] New: Campaign Total Budgets (2026) for fixed 3-90 day periods

## 11.4 Budget Cautions

- [ ] Google's budget recommendations are self-serving -- validate against your ROI data
- [ ] Don't change budget >20% at once (resets Smart Bidding learning)
- [ ] Mid-month budget changes trigger recalculation
- [ ] Lowering budget after overspending can cause continued overspend

---

# PHASE 12: FRAUD PREVENTION & SCAM PROTECTION

## 12.1 Threat Landscape

- Click fraud is a $100+ billion annual global problem
- ~1 in 6 PPC clicks is fraudulent (21.3% invalid traffic)
- Google catches only 5-15% of sophisticated fraud (auto-refund rate 1-3%)
- 30% of small business PPC budgets consumed by fraud
- Click farm hubs: India (Mumbai, Delhi, Kolkata), Bangladesh, Philippines, Vietnam, China

## 12.2 Day 1 Defense Stack (Free)

### Geographic Protection:
- [ ] **CRITICAL: Set location targeting to "Presence" only** (not "Presence or interest")
  - This is the #1 mistake and the #1 source of fraudulent/irrelevant clicks
- [ ] Exclude fraud-heavy regions you don't serve:
  - Review performance by country/region
  - Fraud rates by region: South Africa ~45%, India ~45% desktop, China top 5 globally
- [ ] Exclude any countries where you don't do business

### IP Exclusions:
- [ ] Exclude your own office IPs (prevent employee clicks)
- [ ] Exclude known competitor IPs
- [ ] Limit: 500 per campaign + 500 account-level
- [ ] Supports CIDR notation (e.g., 192.168.1.0/24)
- [ ] NOT available for PMax, Video, Hotel, or App campaigns

### Device Targeting:
- [ ] Mobile accounts for 50% of click fraud
- [ ] Consider -20% to -50% bid adjustment on mobile if fraud is high
- [ ] Monitor Android vs iOS performance (Android has higher fraud rates)

### Ad Scheduling:
- [ ] Bot-heavy hours: 12 AM - 6 AM local time
- [ ] Reduce bids by 50-100% during off-hours
- [ ] If targeting audience in specific time zone, exclude IST 10:00-18:00 hours (click farm operating hours in India = UTC 4:30-12:30)
- [ ] 15-25% waste reduction from scheduling alone

### Search Partners:
- [ ] Turn OFF Search Partners initially
- [ ] Search Partners have 2-3x higher fraud rate than Google Search
- [ ] Test separately after establishing baseline

### Placement Exclusions (Display/PMax):
- [ ] Exclude ALL mobile apps if not relevant to your business:
  - Account-level: Settings > Content Suitability > Excluded content > App categories
  - Use code: `mobileappcategory::69500` for all apps
  - Also exclude specific app categories in Google Ads Editor
- [ ] Exclude MFA (Made for Advertising) sites
- [ ] Exclude parked domains (auto-excluded from SPN as of Feb 2026)
- [ ] Import pre-built exclusion lists (Lunio provides 100K+ exclusions)
- [ ] Limits: 20,000 per campaign, 65,000 per account
- [ ] Account-level placement exclusions launched Jan 2026

## 12.3 Week 1 Defense Stack (Free Monitoring)

### GA4 Fraud Detection Setup:
- [ ] Create custom dimensions: IP-based location, session quality, device fingerprint
- [ ] Monitor for anomalies:
  - CTR spikes >300% of baseline
  - Bounce rate >95% from specific sources
  - Session duration <5 seconds
  - Geographic anomalies (clicks from countries you don't target)
  - Time-of-day patterns (2-6 AM spikes)
  - Device/browser anomalies (unusual user agents)
- [ ] Create GA4 audience for suspicious traffic (bounce <5s + specific geos)
- [ ] Establish 30-day baseline for normal metrics before making conclusions

### Search Terms Report Audit:
- [ ] Review search terms weekly
- [ ] Flag irrelevant queries and add as negative keywords
- [ ] Look for patterns indicating bot/farm traffic (nonsensical queries)

### "Where Did My Ads Show" Report (Display/PMax):
- [ ] Review placement reports weekly
- [ ] Exclude low-quality placements
- [ ] Look for suspicious sites (unknown domains, parked sites, MFA sites)

## 12.4 Month 1 Defense Stack (Paid Tools)

### Click Fraud Protection Tools:

| Tool | Price | Best For |
|------|-------|----------|
| **ClickCease** | $84-$124/mo | Small-medium spend, Google+Meta |
| **Lunio** | $0-$299/mo | All platforms, 100K+ placement exclusion list |
| **TrafficGuard** | Free tier to 2% of spend | Mobile-heavy campaigns |
| **ClickGUARD** | $74-$500+/mo | Advanced customization |
| **CHEQ** | Custom enterprise pricing | Enterprise, advanced fingerprinting |
| **Fraud Blocker** | $49-$69+/mo | Budget-friendly |
| **Fraud0** | Custom | Mobile app fraud |

### Recommendation by Monthly Ad Spend:
- <$5K/mo: Google's built-in protection + manual monitoring
- $5K-$20K/mo: ClickCease or Lunio ($84-$124/mo)
- $20K-$100K/mo: Lunio or TrafficGuard
- $100K+/mo: CHEQ or enterprise solution

## 12.5 Honeypot Setup (Advanced)

- [ ] Add hidden form fields (CSS display:none) that only bots fill in
- [ ] Server-side: reject any submission where honeypot field has a value
- [ ] Add time-based detection (form completed in <3 seconds = bot)
- [ ] Create honeypot landing pages (linked from visible-only-to-bots links)

## 12.6 Google Refund Process for Click Fraud

- [ ] File at: https://support.google.com/google-ads/contact/click_quality
- [ ] Required evidence: GCLIDs, IP addresses, server logs, date range
- [ ] Filing window: Within 60 days of fraudulent clicks
- [ ] Google's stated timeline: 5-10 business days (real-world: weeks to months)
- [ ] Tips:
  - Include specific data, not vague complaints
  - Show patterns (same IPs, same times, same behavior)
  - Document conversion absence from suspicious clicks
  - File monthly if fraud is ongoing

## 12.7 Red Flags Your Campaign Is Under Attack

- [ ] Sudden CTR spike (>300% above baseline) without conversion increase
- [ ] Bounce rate >98% from specific sources
- [ ] Click clusters from same IP ranges
- [ ] Clicks concentrated between midnight and 6 AM
- [ ] Budget exhausted unusually early in the day
- [ ] Conversions tank while clicks increase
- [ ] Unusual geographic distribution (clicks from countries you don't target)
- [ ] Identical session patterns (same pages, same duration, same device)

### Immediate Response:
1. Pause affected campaigns
2. Export click data and analyze patterns
3. Add IP exclusions for suspicious ranges
4. Tighten geographic targeting
5. Reduce bids during suspicious time periods
6. File Google click fraud report
7. Consider third-party fraud tool deployment

---

# PHASE 13: DISPLAY/PMAX/VIDEO/DEMAND GEN SPECIFICS

## 13.1 Display Network Campaign Checklist

### Targeting Setup:
- [ ] Choose targeting method(s):
  - Audience (WHO): Affinity, In-market, Custom, Remarketing
  - Content (WHERE): Topics, Placements, Keywords
  - Demographics: Age, gender, HHI, parental status
- [ ] Layer targeting for precision (audience + content = narrower)
- [ ] Start with managed placements for control OR audience targeting for reach

### Content Exclusions (mandatory):
- [ ] Exclude all mobile app categories (if not relevant)
- [ ] Exclude sensitive content categories
- [ ] Set inventory type to "Standard" minimum
- [ ] Import placement exclusion lists

### Responsive Display Ad Specs:
- Images: 1200x628 (landscape), 1200x1200 (square), 1200x314 (landscape for native)
- Logos: 1200x1200, 512x128
- Headlines: Up to 5, max 30 characters each
- Long headline: 1, max 90 characters
- Descriptions: Up to 5, max 90 characters each
- Business name: 25 characters
- CTA: Select from predefined options

### Dynamic Remarketing:
- [ ] Connect product/service feed
- [ ] Create remarketing lists by product interaction
- [ ] Ads automatically show products users viewed

## 13.2 Performance Max Campaign Checklist

### Asset Groups:
- [ ] Create 3-6 asset groups per campaign (one per audience concept)
- [ ] Assets per group:
  - Images: Up to 20 (1200x628, 960x1200, 1200x1200 required)
  - Logos: Up to 5 (1200x1200, 512x128)
  - Videos: Up to 5 (minimum 10 seconds; Google creates auto-video if none provided)
  - Headlines: Up to 15 (max 30 chars)
  - Long headlines: Up to 5 (max 90 chars)
  - Descriptions: Up to 5 (max 90 chars; one must be 60 chars or fewer)
  - Business name: 25 chars
  - CTA: Auto or select specific

### Audience Signals:
- [ ] Tier 1 (highest impact): First-party data (Customer Match, converters)
- [ ] Tier 2: Custom segments (high-intent search queries, competitor URLs)
- [ ] Tier 3: In-market and detailed demographics
- [ ] Add search themes (up to 50 per asset group)
- [ ] Remember: Signals are SUGGESTIONS, not restrictions

### URL Expansion:
- [ ] Toggle URL expansion ON/OFF
- [ ] Set URL exclusion rules (exclude /careers, /blog if not relevant)
- [ ] Without URL expansion: Only your specified final URLs used

### Brand Settings:
- [ ] Add brand exclusions (prevent showing for competitor brands if unwanted)
- [ ] Add brand inclusions (for brand-specific asset groups)

### Negative Keywords:
- [ ] Add campaign-level negative keywords (up to 10,000, expanded 2025)

### Shopping Integration (e-commerce):
- [ ] Link Merchant Center
- [ ] Configure listing groups (equivalent to product groups)
- [ ] Set up product feed with proper attributes

### PMax Cannibalization Prevention:
- [ ] PMax takes priority over Display and Shopping campaigns
- [ ] PMax defers to Search for exact match keywords
- [ ] Use Google's "Power Pack": PMax + exact/phrase Search + broad match Search
- [ ] Monitor Search campaign impression share for drops after PMax launch
- [ ] Optmyzr study: 91.45% of accounts have PMax/Search overlap

### PMax Channel Reporting:
- [ ] Review Insights tab for channel-level performance (Search, Display, YouTube, Discover, Gmail, Maps, Shopping)
- [ ] Available since 2025 transparency update

## 13.3 Demand Gen Campaign Checklist (formerly Discovery)

### Placements:
- YouTube Home feed, Watch Next, Shorts, In-stream
- Gmail Promotions and Social tabs
- Google Discover feed
- Google Maps (new 2025)
- Connected TV (new 2025)
- Channel controls launched Dec 2025 -- can target/exclude specific surfaces

### Ad Formats:
- [ ] Single image ads: 1200x628, 960x1200, 1200x1200
- [ ] Carousel ads: 2-10 cards, each 1200x1200
- [ ] Video ads: Landscape 16:9, Square 1:1, Vertical 9:16

### Audience:
- [ ] Lookalike segments (exclusive to Demand Gen):
  - Narrow: 2.5% expansion
  - Balanced: 5% expansion
  - Broad: 10% expansion
  - **March 2026:** Transitioning to signal mode (no longer hard targeting ceiling)
- [ ] Minimum audience size: 1,000 users

### Bidding:
- Maximize Conversions
- Maximize Conversion Value
- Target CPA
- Target ROAS
- Maximize Clicks

## 13.4 Video Campaign Checklist (YouTube)

### Campaign Subtypes:
- **Video Reach Campaigns (VRC):** Maximize awareness/reach
  - Efficient Reach (mix of bumper + skippable in-stream)
  - Target Frequency (show ad multiple times)
  - Non-skippable in-stream (15 seconds)
- **Video View Campaigns (VVC):** Get most views at lowest CPV
- **Video Action/Conversions:** Drive conversions from video
- **Video Sequencing:** Show ads in specific order

### Ad Format Specifications:
| Format | Length | Skippable | Charged When |
|--------|--------|-----------|-------------|
| Skippable in-stream | No max (recommended <3 min) | After 5 seconds | 30s view or interaction |
| Non-skippable | 15 seconds exactly | No | Per impression (CPM) |
| Bumper | 6 seconds max | No | Per impression (CPM) |
| In-feed (Discovery) | Any | N/A (click to play) | Click to watch |
| Shorts ads | <60 seconds, 9:16 | Swipe | View or interaction |
| Outstream | Any | Auto-mute | 50% viewable 2+ seconds |

### YouTube Targeting:
- [ ] Topics (26 top-level categories)
- [ ] Placements (specific channels, videos)
- [ ] Keywords (contextual)
- [ ] Audiences (affinity, in-market, remarketing, custom)
- [ ] Demographics

### Video Settings:
- [ ] Frequency capping (impressions per user per day/week/month)
- [ ] Companion banners (300x60px, shows alongside video ad)
- [ ] Content exclusions (same as Display)

### Video Sequencing:
- [ ] Up to 4 templates: Introduce > Reinforce > Inspire, Mini-Series, Follow-up, Repurpose
- [ ] Progression triggers: Impression or View
- [ ] Frequency caps apply across sequence

## 13.5 Topic Targeting Taxonomy (26 Top-Level)

1. Arts & Entertainment
2. Autos & Vehicles
3. Beauty & Fitness
4. Books & Literature
5. Business & Industrial
6. Computers & Electronics
7. Finance
8. Food & Drink
9. Games
10. Health
11. Hobbies & Leisure
12. Home & Garden
13. Internet & Telecom
14. Jobs & Education
15. Law & Government
16. News
17. Online Communities
18. People & Society
19. Pets & Animals
20. Real Estate
21. Reference
22. Science
23. Shopping
24. Sports
25. Travel
26. World Localities

Each has dozens of subcategories. Use topic exclusions to block irrelevant content categories.

---

# PHASE 14: LAUNCH CHECKLIST

## Pre-Launch Verification (do ALL before unpausing)

### Account Level:
- [ ] Billing information correct and card valid
- [ ] Auto-tagging ON
- [ ] Account-level negative keyword lists applied
- [ ] Account-level placement exclusions set
- [ ] Account-level IP exclusions set
- [ ] GA4 linked
- [ ] YouTube channel linked (if applicable)
- [ ] Merchant Center linked (if e-commerce)

### Campaign Level:
- [ ] Campaign name follows convention
- [ ] Networks: Display Network UNCHECKED on Search campaigns
- [ ] Location: "Presence only" selected (NOT "Presence or interest")
- [ ] Languages correct
- [ ] Bidding strategy matches data maturity
- [ ] Budget set appropriately (2-3x target CPA for Smart Bidding)
- [ ] Ad schedule configured
- [ ] IP exclusions added
- [ ] Content exclusions set (Display/Video)
- [ ] Mobile app categories excluded (Display)
- [ ] Conversion goals correct (primary vs secondary)
- [ ] Start date set

### Ad Group Level:
- [ ] Optimized Targeting reviewed (ON or OFF as needed)
- [ ] Keywords tightly themed (5-10 per group)
- [ ] Negative keywords at ad group level added
- [ ] Demographics bid adjustments set
- [ ] Audiences added (Observation mode for Search)

### Ad Level:
- [ ] 2-3 RSAs per ad group with unique headlines
- [ ] Ad strength "Good" or "Excellent"
- [ ] Landing page URLs correct and loading
- [ ] All applicable ad assets/extensions added
- [ ] UTM parameters in tracking template

### Tracking Level:
- [ ] GTM tags firing correctly (verified in Preview Mode)
- [ ] Conversion Linker tag active on all pages
- [ ] Conversion tags firing on correct events
- [ ] Enhanced Conversions enabled
- [ ] GA4 events tracking properly
- [ ] Test conversion: Submit a test form/purchase and verify it registers
- [ ] Heatmap/session recording tool active
- [ ] Phone call tracking active (if applicable)

### Landing Page Level:
- [ ] All landing page URLs return 200 status (no 404s, no redirects)
- [ ] Pages pass Core Web Vitals (LCP <2.5s, INP <200ms, CLS <0.1)
- [ ] HTTPS active on all pages
- [ ] Message match verified (ad headline = page headline)
- [ ] Forms working correctly
- [ ] Thank you page/confirmation set up
- [ ] Mobile rendering checked on actual devices

### Fraud Prevention:
- [ ] Location targeting set to "Presence" only
- [ ] Search Partners OFF (or knowingly ON)
- [ ] IP exclusions active
- [ ] Click fraud tool connected (if budget warrants)
- [ ] Mobile app exclusions in place (Display)

---

# PHASE 15: ONGOING OPTIMIZATION CADENCE

## 15.1 Daily Tasks (10-15 minutes)

- [ ] Check budget pacing (running out too fast? Underspending?)
- [ ] Monitor for anomalies (CTR spikes, CPC jumps, conversion drops)
- [ ] Check account alerts and notifications
- [ ] Verify ads are serving (no disapprovals, billing issues)
- [ ] Monitor impression share for key campaigns
- [ ] Check for click fraud indicators (unusual patterns)
- [ ] Review any automated rule triggers
- [ ] Quick scan of top-performing and bottom-performing keywords

## 15.2 Weekly Tasks (1-2 hours)

- [ ] **Search Terms Report:** Mine for negative keywords; add converting search terms as keywords
- [ ] **Bid adjustments:** Review device, location, time, audience performance; adjust bids (manual strategies)
- [ ] **Ad performance:** Check RSA combinations; pause underperformers
- [ ] **Quality Score check:** Flag any keywords below 5; investigate below-average components
- [ ] **Placement review (Display/PMax):** Exclude low-quality/fraudulent placements
- [ ] **Budget reallocation:** Shift budget from underperforming to overperforming campaigns
- [ ] **Session recordings review:** Watch 5-10 recordings for UX issues on landing pages

## 15.3 Bi-Weekly Tasks (30-60 minutes)

- [ ] **Ad copy testing:** Launch new ad variations if current tests have reached significance
- [ ] **Landing page A/B tests:** Review results; launch new tests
- [ ] **Audience segment review:** Check audience performance in Observation mode
- [ ] **Negative keyword list update:** Consolidate weekly findings into shared lists

## 15.4 Monthly Tasks (2-4 hours)

- [ ] **Quality Score deep dive:** Analyze all components; prioritize improvements
- [ ] **Competitor analysis:** Review Auction Insights; check competitor ads/landing pages
- [ ] **Account structure review:** Any ad groups need splitting? Campaigns need restructuring?
- [ ] **Conversion tracking audit:** Verify all conversions still firing correctly
- [ ] **Budget planning:** Next month's budget based on this month's performance
- [ ] **Audience list refresh:** Update Customer Match lists with new CRM data
- [ ] **Ad asset review:** Update sitelinks, callouts, promotions if stale
- [ ] **Heatmap analysis:** Review heatmaps for landing page optimization opportunities
- [ ] **IP exclusion list cleanup:** Remove old entries; add new suspicious IPs
- [ ] **Click fraud report:** Review click fraud tool reports; file Google refund if warranted

## 15.5 Quarterly Tasks (4-8 hours)

- [ ] **Strategy review:** Overall account performance vs business goals
- [ ] **Account restructure assessment:** Major changes to campaign structure needed?
- [ ] **Bidding strategy review:** Ready to advance to smarter strategy? Run experiments
- [ ] **Landing page overhaul:** Major updates based on 3 months of A/B testing data
- [ ] **Creative refresh:** New ad copy, new images, new video
- [ ] **Seasonal planning:** Upcoming quarters -- budget adjustments, seasonal messaging
- [ ] **Competitive landscape review:** New competitors? Market changes?
- [ ] **ROI/ROAS deep analysis:** True profitability after considering all costs

## 15.6 Ad Copy Testing Methodology

- [ ] Test ONE element at a time (headline, description, CTA)
- [ ] Minimum data for significance: 1,000 clicks OR 100 conversions per variant
- [ ] Required confidence level: 95%
- [ ] Run test for minimum 2 weeks
- [ ] Use Google's ad variations experiment feature
- [ ] Document all test results for future reference

## 15.7 Negative Keyword Mining Process

1. Go to Keywords > Search Terms
2. Sort by impressions (high to low)
3. Identify irrelevant queries
4. Check "Did this term convert?" before adding as negative
5. Add as phrase match negative (unless very specific = exact match)
6. Add to shared negative keyword list
7. Review impact after 1 week

---

# PHASE 16: REPORTING & ANALYTICS

## 16.1 Key Metrics Dashboard

### Performance Metrics:
| Metric | Formula | 2025 All-Industry Benchmark |
|--------|---------|---------------------------|
| CTR | Clicks / Impressions x 100 | 6.66% |
| CPC | Cost / Clicks | $5.26 |
| Conversion Rate | Conversions / Clicks x 100 | 7.52% |
| CPA | Cost / Conversions | $70.11 |
| ROAS | Revenue / Spend | 4:1 is good |

### Visibility Metrics:
| Metric | What It Tells You |
|--------|-------------------|
| Search Impression Share | % of eligible impressions you received |
| Lost IS (Budget) | % lost due to insufficient budget |
| Lost IS (Rank) | % lost due to low Ad Rank |
| Top Impression Rate | % of impressions in top position |
| Absolute Top Impression Rate | % in position #1 |

### Quality Metrics:
| Metric | Components |
|--------|-----------|
| Quality Score (1-10) | Expected CTR (39%), Landing Page (39%), Ad Relevance (22%) |

## 16.2 Google Ads Reports to Run

- [ ] **Search Terms Report** -- weekly (negative keyword mining)
- [ ] **Auction Insights** -- monthly (competitive position)
- [ ] **Quality Score Report** -- monthly (improvement tracking)
- [ ] **Ad Performance Report** -- weekly (ad testing)
- [ ] **Device Report** -- weekly (bid adjustment data)
- [ ] **Location Report** -- monthly (geo performance)
- [ ] **Time of Day Report** -- monthly (schedule optimization)
- [ ] **Placement Report** (Display/PMax) -- weekly (exclusion candidates)
- [ ] **Asset Performance Report** -- monthly (which assets work)

### Useful Segments:
- Time: Hour of day, Day of week, Month
- Device: Computer, Mobile, Tablet
- Network: Google Search, Search Partners, Display
- Click type: Headline, Sitelink, etc.
- Conversion action: Individual conversion types

## 16.3 GA4 Integration Reporting

- [ ] **Acquisition > Google Ads:** Campaign, ad group, keyword performance with on-site engagement
- [ ] **Funnel Exploration:** Visualize conversion funnel drop-offs
- [ ] **Path Exploration:** Understand user journeys from ad click to conversion
- [ ] **Segment Overlap:** Compare audience segments
- [ ] **Attribution:** Compare models (DDA vs Last Click)

### Consent Mode Impact on Data:
- Modeling activates when: 700+ clicks over 7 days AND 20%+ consent rate
- Advanced Consent Mode preserves up to 80% of tracking data even when consent denied

## 16.4 Automated Reporting

- [ ] Set up scheduled reports in Google Ads (email delivery)
- [ ] Create Looker Studio dashboard connecting Google Ads + GA4
- [ ] Consider Google Ads scripts for automated alerts:
  - Budget monitoring script (alert when pacing off)
  - Broken URL checker (alert when landing pages return errors)
  - Quality Score tracker (alert on score drops)
  - Anomaly detection (alert on metric spikes/drops)

## 16.5 Third-Party Reporting Tools

| Tool | Price | Best For |
|------|-------|----------|
| Optmyzr | $249/mo | All-in-one optimization + reporting |
| Adalysis | $149/mo | Ad testing and Quality Score tracking |
| Opteo | $97/mo | Automated recommendations |

---

# PHASE 17: COMPETITIVE ANALYSIS

## 17.1 Auction Insights (in Google Ads)

Available metrics:
- **Impression Share:** Your share vs competitors
- **Overlap Rate:** How often competitor shows alongside you
- **Position Above Rate:** How often competitor ranks above you
- **Outranking Share:** How often you rank above competitor
- **Top of Page Rate:** Competitor's top impression rate
- **Absolute Top of Page Rate:** Competitor's #1 position rate

### How to Interpret:
- High overlap + low outranking = competitor dominating your space
- High impression share + low conversion = ad/landing page issue, not visibility
- Rising competitor overlap = new competitor entering market

## 17.2 External Competitive Tools

- [ ] **SpyFu:** Competitor keywords, estimated ad spend, ad history
- [ ] **SEMrush:** PPC competitor analysis, keyword gaps, ad copy
- [ ] **Ahrefs:** PPC keyword research, competitive gaps
- [ ] **iSpionage / Adbeat:** Display ad intelligence
- [ ] **SimilarWeb:** Overall traffic analysis
- [ ] **Google Ads Transparency Center:** Free -- see any advertiser's current ads

## 17.3 Competitive Analysis Workflow

1. Export Auction Insights monthly
2. Track competitor impression share trends
3. Screenshot competitor ads quarterly
4. Audit competitor landing pages quarterly
5. Identify gaps in competitor keyword coverage
6. Test competitor brand keyword campaigns (where legal/appropriate)

---

# PHASE 18: PRIVACY & COMPLIANCE

## 18.1 Consent Mode V2 (Mandatory for EEA/UK)

### Four Consent Signals:
| Parameter | Controls | Default |
|-----------|----------|---------|
| `ad_storage` | Ad cookies | `denied` |
| `analytics_storage` | Analytics cookies | `denied` |
| `ad_user_data` | User data to ads platforms | `denied` |
| `ad_personalization` | Personalized ads/remarketing | `denied` |

### Implementation:
- [ ] Integrate CMP (CookieYes, OneTrust, Cookiebot, etc.)
- [ ] Deploy via GTM with defaults set to `denied`
- [ ] Update parameters dynamically on user consent
- [ ] Use Advanced Consent Mode (sends cookieless pings for conversion modeling)
- [ ] Verify with Tag Diagnostics

### Timeline:
- March 2024: Mandatory for EEA/UK
- July 2025: Google restricts data from non-compliant sites
- Feb 2026: Stricter conversion data requirements via Ads API

### Impact of Non-Compliance:
- Loss of remarketing capabilities
- Loss of lookalike/similar audiences
- Loss of conversion modeling
- Potential account suspension

## 18.2 GDPR Compliance Checklist

- [ ] Explicit opt-in consent for EEA/UK users
- [ ] Data processing agreements with Google in place
- [ ] Right to erasure supported
- [ ] Consent records maintained
- [ ] Cookie consent banner implemented
- [ ] Privacy policy updated to include ad tracking disclosure

## 18.3 CCPA Compliance Checklist

- [ ] "Do Not Sell" opt-out mechanism for California users
- [ ] Honor Global Privacy Control (GPC) signals
- [ ] Data deletion requests supported
- [ ] Privacy policy includes CCPA disclosures

---

# APPENDIX A: INDUSTRY BENCHMARKS (2025)

## Search Ads Benchmarks

| Industry | CTR | CPC | CVR | CPA |
|----------|-----|-----|-----|-----|
| Arts & Entertainment | 13.04% | $3.13 | 13.41% | $23.31 |
| Attorneys & Legal | 4.76% | $9.21 | 7.00% | $131.69 |
| Auto (Repair/Service) | 5.65% | $3.06 | 12.96% | $23.59 |
| B2B | 5.17% | $5.47 | 5.53% | $98.89 |
| Dentists & Dental | 5.34% | $6.49 | 10.40% | $62.44 |
| Education & Instruction | 6.41% | $4.10 | 7.07% | $57.97 |
| Finance & Insurance | 5.70% | $4.01 | 4.11% | $97.52 |
| Health & Fitness | 6.44% | $4.18 | 7.71% | $54.22 |
| Home Improvement | 4.80% | $6.55 | 10.22% | $64.13 |
| Industrial & Commercial | 5.34% | $4.35 | 6.82% | $63.77 |
| Real Estate | 9.09% | $1.55 | 2.88% | $53.52 |
| Restaurants & Food | 8.65% | $1.95 | 5.06% | $38.46 |
| Shopping/E-commerce | 6.39% | $1.16 | 2.81% | $41.16 |
| Technology | 5.08% | $5.57 | 4.49% | $124.08 |
| Travel & Hospitality | 10.03% | $1.63 | 3.87% | $42.18 |
| **All Industries** | **6.66%** | **$5.26** | **7.52%** | **$70.11** |

## Landing Page Benchmarks

| Industry | Median Conversion Rate |
|----------|----------------------|
| Events & Entertainment | 12.3% |
| Financial Services | 8.4% |
| Legal Services | 7.4% |
| Travel & Hospitality | 5.0% |
| Overall Median | 6.6% |
| SaaS | 3.8% |
| E-commerce | 2.35% |
| Healthcare | 1.9% |

Top 10% of landing pages achieve 10%+ conversion rates. Top performers reach 15-20%.

---

# APPENDIX B: TOOLS & SOFTWARE STACK

## Essential Tools

| Category | Tool | Price | Purpose |
|----------|------|-------|---------|
| **Tag Management** | Google Tag Manager | Free | Centralized tag deployment |
| **Analytics** | Google Analytics 4 | Free | Website analytics |
| **Heatmaps** | Microsoft Clarity | Free | Heatmaps + session recordings |
| **Heatmaps (Pro)** | Hotjar | $39/mo+ | Heatmaps + surveys + feedback |
| **Keyword Research** | Google Keyword Planner | Free | Search volume + CPC estimates |
| **Competitive Intel** | SpyFu | $39/mo+ | Competitor PPC intelligence |
| **Competitive Intel** | SEMrush | $129/mo+ | Full competitive analysis |
| **Click Fraud** | ClickCease | $84/mo+ | Click fraud protection |
| **Click Fraud** | Lunio | $0-$299/mo | Multi-platform fraud protection |
| **A/B Testing** | VWO | Custom | Landing page testing |
| **A/B Testing** | PageTest.ai | Free | Simple A/B testing |
| **Landing Pages** | Unbounce | $74/mo+ | Landing page builder + Smart Traffic AI |
| **Landing Pages** | Leadpages | $37/mo+ | Budget landing page builder |
| **Automation** | Optmyzr | $249/mo+ | PPC management + optimization |
| **Automation** | Opteo | $97/mo+ | Automated recommendations |
| **Reporting** | Looker Studio | Free | Dashboard + visualization |
| **CRM** | HubSpot | Free-$1200/mo | Lead management + nurturing |
| **Brand Safety** | IAS / DoubleVerify | Custom | Third-party verification |

## Google Ads Scripts (Most Useful)

1. **Broken URL Checker** -- Alerts when landing pages return errors
2. **Budget Monitor** -- Alerts when spend is off pace
3. **Quality Score Tracker** -- Historical QS tracking
4. **Search Query Miner** -- Automated negative keyword suggestions
5. **N-gram Analysis** -- Find converting/wasting search term patterns
6. **Ad Performance** -- Pause low-performing ads automatically
7. **Bid Management** -- Automated bid adjustments based on rules

---

# QUICK REFERENCE: CRITICAL NUMBERS

| Setting | Value |
|---------|-------|
| Max headlines per RSA | 15 |
| Max descriptions per RSA | 4 |
| Headline character limit | 30 |
| Description character limit | 90 |
| IP exclusions per campaign | 500 |
| IP exclusions per account | 500 |
| Placement exclusions per account | 65,000 |
| PMax negative keywords limit | 10,000 |
| Customer Match expiry | 540 days |
| Daily budget overspend limit | 2x |
| Monthly spend formula | Daily x 30.4 |
| Min conversions for Target CPA | 30/month recommended |
| Min conversions for Target ROAS | 50/month recommended |
| Learning period | 7-30 days |
| Budget change trigger | >20% |
| Bid adjustment max increase | +900% |
| Bid adjustment max decrease | -90% (-100% device only) |
| Core Web Vitals LCP | < 2.5 seconds |
| Core Web Vitals INP | < 200ms |
| Core Web Vitals CLS | < 0.1 |
| A/B test significance | 95% confidence |
| Min audience size (Display) | 100 users |
| Min audience size (Search RLSA) | 100-1,000 users |
| Remarketing max membership | 540 days |
| Click fraud rate (industry avg) | ~21% of clicks |
| Google auto-refund rate | 1-3% |

---

*This manual was compiled from 7 parallel research streams covering 200+ sources, March 2026. All settings and features verified against current Google Ads and Microsoft Ads documentation.*
