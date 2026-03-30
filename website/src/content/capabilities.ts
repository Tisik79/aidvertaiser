/* -------------------------------------------------------------------------- */
/*  Capability Data — Aidvertaiser Marketing Website                         */
/* -------------------------------------------------------------------------- */

export interface Capability {
  slug: string;
  icon: string;
  title: Record<string, string>;
  shortDescription: Record<string, string>;
  metaDescription: Record<string, string>;
  content: Record<string, string>;
  platforms: string[];
  toolExamples: string[];
  relatedSlugs: string[];
}

/* Helper: for languages we haven't translated yet, fall back to English */
function ml(en: string, cs: string): Record<string, string> {
  return { en, cs, fr: en, es: en, zh: en, hi: en, pt: en, pl: en, ar: en, bn: en };
}

export const capabilities: Capability[] = [
  /* ==================================================================== */
  /*  1. Campaign Management                                              */
  /* ==================================================================== */
  {
    slug: 'campaign-management',
    icon: 'Megaphone',
    title: ml('Campaign Management', 'Sprava kampani'),
    shortDescription: ml(
      'Full campaign lifecycle management across Google Ads and Meta Ads. Create, configure, optimize, pause, and analyze campaigns on both platforms through natural language — no Ads Manager needed.',
      'Kompletni sprava zivotniho cyklu kampani napric Google Ads a Meta Ads. Vytvarejte, konfigurujte, optimalizujte, pozastavujte a analyzujte kampane na obou platformach prirozenim jazykem — bez nutnosti Ads Manageru.',
    ),
    metaDescription: ml(
      'Manage advertising campaigns across Google Ads and Meta Ads with AI. Create, optimize, pause, and analyze campaigns through natural language with Aidvertaiser MCP tools.',
      'Spravujte reklamni kampane napric Google Ads a Meta Ads pomoci AI. Vytvarejte, optimalizujte a analyzujte kampane prirozenim jazykem s Aidvertaiser MCP nastroji.',
    ),
    content: {
      en: `<h2 id="overview">End-to-End Campaign Control</h2>
<p>Campaign management is the core capability of Aidvertaiser. With dedicated tools for both <strong>Google Ads</strong> and <strong>Meta Ads</strong>, you can manage every aspect of your advertising campaigns through natural language commands. No more switching between platform interfaces, memorizing settings locations, or manually copying data between tools.</p>
<p>The campaign management tools cover the full advertising hierarchy on each platform. On Google Ads, that means campaigns, ad groups, ads, and keywords. On Meta Ads, it means campaigns, ad sets, ads, and creatives. Every level of the hierarchy supports full CRUD operations — create, read, update, and delete.</p>

<h2 id="google-ads-campaigns">Google Ads Campaign Management</h2>
<p>Create Google Ads campaigns with complete configuration in a single conversation. Specify the campaign type (Search, Display, Shopping, Video, Performance Max), set the bidding strategy (Manual CPC, Maximize Conversions, Target CPA, Target ROAS), configure the daily budget, define location and language targeting, and set ad schedules.</p>
<p>Once campaigns are running, update any setting on the fly. Pause campaigns for weekends, increase budgets for peak periods, switch bidding strategies as conversion data accumulates, and adjust targeting based on performance data. All changes are applied immediately through the Google Ads API.</p>
<p>Below the campaign level, manage ad groups with their own bids and targeting refinements. Create Responsive Search Ads with up to 15 headlines and 4 descriptions. Add and manage keywords across all match types. Build negative keyword lists to eliminate wasted spend. Pull search terms reports to discover new keyword opportunities.</p>

<h2 id="meta-ads-campaigns">Meta Ads Campaign Management</h2>
<p>Meta Ads campaigns follow a three-tier structure: campaigns, ad sets, and ads. Aidvertaiser provides tools for every tier. Create campaigns with objectives aligned to your business goals — awareness, traffic, engagement, leads, app promotion, or sales. Configure ad sets with detailed audience targeting, budget allocation, placement selection, and optimization goals.</p>
<p>Build ad creatives with images, videos, carousels, and collections. Upload creative assets directly to your ad account. Configure ad copy with primary text, headlines, descriptions, and call-to-action buttons. Manage the complete lifecycle from draft to active to paused to archived.</p>

<h2 id="cross-platform">Cross-Platform Coordination</h2>
<p>The real power of Aidvertaiser emerges when you manage campaigns across both platforms simultaneously. Ask your AI assistant to create a coordinated campaign launch — a Search campaign on Google Ads targeting high-intent keywords alongside a traffic campaign on Meta Ads targeting relevant interest audiences. Monitor performance across both platforms in a single conversation.</p>
<p>Compare cost-per-click, cost-per-acquisition, and return on ad spend between platforms to inform budget allocation decisions. When a campaign performs well on one platform, replicate the strategy on the other with appropriate adaptations for the platform's targeting model.</p>

<h2 id="performance-max">Performance Max Campaigns</h2>
<p>Google's Performance Max campaigns represent the most advanced automated campaign type. Aidvertaiser provides 16 dedicated tools for P-Max management, including asset group creation, listing group configuration, brand guidelines setup, and audience signal definition. P-Max campaigns run across all Google surfaces — Search, Display, YouTube, Gmail, Maps, and Discover — using Google's AI to optimize placements and bids automatically.</p>

<h2 id="tool-examples">Example Workflows</h2>
<ul>
<li>"Create a Google Ads Search campaign targeting 'CRM software' keywords in the US with a $50 daily budget and Target CPA of $25"</li>
<li>"Pause all Meta Ads campaigns with a CPA above $40 in the last 7 days"</li>
<li>"Show me the top 10 search terms by spend across all active Google Ads campaigns"</li>
<li>"Create a Meta Ads traffic campaign targeting users interested in project management, aged 25-45, in California"</li>
<li>"Compare yesterday's performance between Google Ads and Meta Ads — show CPC, conversions, and ROAS"</li>
</ul>`,
      cs: `<h2 id="overview">Kompletni rizeni kampani</h2>
<p>Sprava kampani je zakladni schopnosti Aidvertaiser. S nastroji pro <strong>Google Ads</strong> i <strong>Meta Ads</strong> muzete spravovat kazdy aspekt vasich reklamnich kampani prostrednictvim prikazu v prirozenen jazyce. Konec prepinani mezi rozhranimi platforem a manualniho kopirovani dat.</p>

<h2 id="google-ads-campaigns">Sprava kampani Google Ads</h2>
<p>Vytvarejte kampane Google Ads s kompletni konfiguraci v jedinem rozhovoru. Zadejte typ kampane, strategii nabidek, denni rozpocet, cileni na lokality a casove plany reklam. Aktualizujte jakoukoli nastaveni za behu — pozastavujte kampane, zvysujte rozpocty a upravujte cileni na zaklade dat o vykonnosti.</p>

<h2 id="meta-ads-campaigns">Sprava kampani Meta Ads</h2>
<p>Kampane Meta Ads sledují tristupnovou strukturu: kampane, sady reklam a reklamy. Aidvertaiser poskytuje nastroje pro kazdou uroven. Vytvarejte kampane s cili vyrovnanymi s vasimi obchodnimi cili, konfigurujte detailni cileni na publika a spravujte kreativni obsah.</p>

<h2 id="cross-platform">Koordinace napric platformami</h2>
<p>Skutecna sila Aidvertaiser se projevi pri soucasne sprave kampani na obou platformach. Porovnavejte cenu za kliknuti, cenu za ziskani zakaznika a navratnost reklamnich vydaju mezi platformami pro informovane rozhodovani o alokaci rozpoctu.</p>

<h2 id="performance-max">Kampane Performance Max</h2>
<p>Aidvertaiser poskytuje 16 specializovanych nastroju pro spravu P-Max vcetne skupin assetu, skupin polozek, pravidel znacky a signalu publika.</p>`,
    },
    platforms: ['google-ads', 'meta-ads'],
    toolExamples: [
      'google_create_campaign',
      'google_update_campaign',
      'google_list_campaigns',
      'meta_create_campaign',
      'meta_create_ad_set',
      'meta_create_ad',
    ],
    relatedSlugs: ['conversion-tracking', 'budget-optimization', 'audience-targeting'],
  },

  /* ==================================================================== */
  /*  2. Conversion Tracking                                              */
  /* ==================================================================== */
  {
    slug: 'conversion-tracking',
    icon: 'Target',
    title: ml('Conversion Tracking', 'Sledovani konverzi'),
    shortDescription: ml(
      'Comprehensive conversion tracking across platforms. Set up Google Ads conversion actions, Meta Pixels, Conversions API, offline conversion uploads, enhanced conversions, and custom conversion events — all through AI.',
      'Komplexni sledovani konverzi napric platformami. Nastavte konverzni akce Google Ads, Meta Pixely, Conversions API, offline konverze, vylepsene konverze a vlastni konverzni udalosti — vse prostrednictvim AI.',
    ),
    metaDescription: ml(
      'Set up conversion tracking across Google Ads and Meta Ads. Pixels, Conversions API, offline uploads, enhanced conversions, and custom events with Aidvertaiser MCP tools.',
      'Nastavte sledovani konverzi napric Google Ads a Meta Ads. Pixely, Conversions API, offline konverze a vlastni udalosti s Aidvertaiser MCP nastroji.',
    ),
    content: {
      en: `<h2 id="overview">Measure What Matters</h2>
<p>Conversion tracking is the foundation of successful advertising. Without accurate conversion data, bidding algorithms cannot optimize, budget allocation is guesswork, and ROI cannot be measured. Aidvertaiser provides <strong>18+ conversion-focused tools</strong> across Google Ads and Meta Ads, covering every aspect of conversion setup and management.</p>
<p>In a world where browser cookies are increasingly unreliable, server-side tracking and first-party data are essential. Aidvertaiser supports the latest tracking methods — Meta's Conversions API for server-side event delivery, Google's Enhanced Conversions for cookie-independent attribution, and offline conversion uploads for connecting CRM data with ad interactions.</p>

<h2 id="google-ads-conversions">Google Ads Conversion Tracking</h2>
<p>Set up Google Ads conversion actions with full configuration control. Define the conversion category (purchase, lead, sign-up, page view), set the conversion value (static or dynamic), choose the counting method (one per click or every), configure conversion windows (1-90 days for click-through, 1-30 days for view-through), and select the attribution model (data-driven, last click, first click, linear, time decay, position-based).</p>
<p>Designate conversions as primary (used for bidding optimization) or secondary (tracking only). This distinction is critical — including micro-conversions as primary actions can mislead Smart Bidding algorithms.</p>

<h3>Offline Conversion Upload</h3>
<p>For businesses where the final conversion happens offline — B2B sales, car dealerships, real estate, financial services — offline conversion upload closes the attribution gap. Upload conversion data with the original Google Click ID (GCLID) to tell Google Ads which clicks led to actual revenue. This enables Smart Bidding to optimize for real business outcomes rather than just form submissions.</p>

<h3>Enhanced Conversions</h3>
<p>Enhanced Conversions use hashed first-party data (email, phone, name, address) sent alongside conversion events to improve measurement accuracy. When cookies are blocked or cross-device journeys break traditional tracking, enhanced conversions use deterministic matching to attribute conversions correctly. Aidvertaiser supports both Enhanced Conversions for Web and Enhanced Conversions for Leads.</p>

<h2 id="meta-ads-conversions">Meta Ads Conversion Tracking</h2>
<p>Meta's conversion ecosystem revolves around the Meta Pixel and the Conversions API. Aidvertaiser provides tools for both.</p>

<h3>Meta Pixel Management</h3>
<p>Create and configure Meta Pixels for your websites. The pixel fires browser-side events (PageView, ViewContent, AddToCart, Purchase, Lead, CompleteRegistration) that Meta uses for conversion attribution, audience building, and campaign optimization.</p>

<h3>Conversions API (CAPI)</h3>
<p>The Conversions API sends conversion events server-to-server, bypassing browser limitations entirely. This is the most reliable tracking method available on Meta, and it works alongside the pixel through deduplication. Aidvertaiser's CAPI tools let you send events with user data parameters (email, phone, IP, user agent) for enhanced matching.</p>

<h3>Custom Conversions</h3>
<p>Define custom conversion events based on URL rules (contains, equals, starts with) or event parameters. Custom conversions let you track specific actions without modifying pixel code — for example, tracking visits to a specific thank-you page as a lead conversion.</p>

<h3>Offline Conversions</h3>
<p>Upload offline event data from your CRM or point-of-sale system. Connect in-store purchases, phone orders, and offline deals with the online ad interactions that drove them. This gives Meta's algorithm the full picture of your campaign performance.</p>

<h2 id="best-practices">Best Practices</h2>
<ul>
<li><strong>Implement both pixel and server-side tracking</strong> — Use browser and server events together with deduplication for maximum coverage</li>
<li><strong>Set conversion windows appropriately</strong> — B2C typically uses 7-day click/1-day view windows; B2B may need 30-90 day click windows</li>
<li><strong>Distinguish primary and secondary conversions</strong> — Only optimize bidding toward actions that directly represent business value</li>
<li><strong>Upload offline conversions regularly</strong> — Weekly uploads keep Smart Bidding algorithms informed about real outcomes</li>
<li><strong>Enable enhanced conversions</strong> — First-party data matching recovers 5-15% of conversions lost to cookie blocking</li>
</ul>`,
      cs: `<h2 id="overview">Merejte to, co je dulezite</h2>
<p>Sledovani konverzi je zakladem uspesne reklamy. Bez presnych konverznich dat nemohou algoritmy nabidek optimalizovat, alokace rozpoctu je hadani a ROI nelze merit. Aidvertaiser poskytuje <strong>18+ nastroju zamerenych na konverze</strong> napric Google Ads a Meta Ads.</p>

<h2 id="google-ads-conversions">Sledovani konverzi Google Ads</h2>
<p>Nastavte konverzni akce Google Ads s plnou kontrolou konfigurace. Definujte kategorii konverze, hodnotu, metodu pocitani, konverzni okna a atribucni model. Oznacte konverze jako primarni (pro optimalizaci nabidek) nebo sekundarni (pouze sledovani).</p>

<h3>Offline konverze</h3>
<p>Pro firmy, kde finalni konverze probehne offline, nahrajte konverzni data s puvodnim GCLID pro propojeni kliknuti s realnym prjimem.</p>

<h3>Vylepsene konverze</h3>
<p>Vylepsene konverze pouzivaji hashovana first-party data odeslanajako součast konverznich udalosti pro zlepseni presnosti mereni.</p>

<h2 id="meta-ads-conversions">Sledovani konverzi Meta Ads</h2>
<h3>Sprava Meta Pixelu</h3>
<p>Vytvarejte a konfigurujte Meta Pixely pro vase weby. Pixel spousti udalosti na strane prohlizece pro atribuci konverzi.</p>

<h3>Conversions API</h3>
<p>Conversions API odesila konverzni udalosti server-to-server, obchazejici omezeni prohlizece. Nejspolehlivejsi metoda sledovani na Meta.</p>

<h3>Vlastni konverze</h3>
<p>Definujte vlastni konverzni udalosti na zaklade pravidel URL nebo parametru udalosti.</p>

<h3>Offline konverze</h3>
<p>Nahravejte offline udalostni data z vaseho CRM. Propojte obchodni nakupy s online reklamnimi interakcemi.</p>`,
    },
    platforms: ['google-ads', 'meta-ads'],
    toolExamples: [
      'google_create_conversion_action',
      'google_upload_offline_conversions',
      'google_enable_enhanced_conversions',
      'meta_create_pixel',
      'meta_send_conversion_event',
      'meta_create_custom_conversion',
      'meta_upload_offline_conversions',
    ],
    relatedSlugs: ['campaign-management', 'analytics-reporting', 'budget-optimization'],
  },

  /* ==================================================================== */
  /*  3. Audience Targeting                                               */
  /* ==================================================================== */
  {
    slug: 'audience-targeting',
    icon: 'UsersThree',
    title: ml('Audience Targeting', 'Cileni na publika'),
    shortDescription: ml(
      'Reach the right people with precision targeting tools. Search interests and behaviors on Meta, estimate audience sizes, configure demographic targeting on Google Ads, and build audience signals for Performance Max campaigns.',
      'Oslovte spravne lidi s nastroji pro presne cileni. Prohledavejte zajmy a chovani na Meta, odhadujte velikosti publika, konfigurujte demograficke cileni na Google Ads a vytvarejte signaly publika pro kampane Performance Max.',
    ),
    metaDescription: ml(
      'Precision audience targeting across Google Ads and Meta Ads. Interest search, behavioral targeting, audience estimation, demographics, and P-Max audience signals with Aidvertaiser.',
      'Presne cileni na publika napric Google Ads a Meta Ads. Vyhledavani zajmu, behavioralni cileni, odhad publika a signaly pro P-Max s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Find Your Audience</h2>
<p>The difference between profitable advertising and wasted spend often comes down to targeting. Showing your ads to the right people at the right time is what turns ad budgets into revenue. Aidvertaiser provides audience targeting tools across both <strong>Google Ads</strong> and <strong>Meta Ads</strong>, each with its own targeting model and strengths.</p>
<p>Meta excels at interest-based and behavioral targeting with its massive first-party data from Facebook, Instagram, and WhatsApp. Google excels at intent-based targeting through search keywords and in-market audiences. Together, they cover the full marketing funnel from awareness to purchase intent.</p>

<h2 id="meta-targeting">Meta Ads Targeting</h2>
<h3>Interest Targeting</h3>
<p>Search Meta's interest database by keyword to discover targetable audience segments. When you search for "fitness," you'll discover interests like Gym, Yoga, CrossFit, Weight training, Running, and Healthy eating — each with estimated audience sizes. Layer multiple interests together to build precise audience definitions.</p>

<h3>Behavioral Targeting</h3>
<p>Target users based on their real-world behaviors tracked by Meta. This includes purchase behavior (online shoppers, luxury goods buyers), device usage (early technology adopters, specific phone models), travel patterns (frequent travelers, commuters), and more. Behavioral targeting reaches users based on what they do, not just what they say they are interested in.</p>

<h3>Geo-Location Search</h3>
<p>Find targetable geographic locations with Meta's geo-location search. Search by city name, region, postal code, or address. Results include the location key needed for ad set targeting, population estimates, and geographic coordinates. Combine locations with radius targeting for precise local campaigns.</p>

<h3>Audience Estimation</h3>
<p>Before spending a dollar, estimate the reach and daily results for any targeting combination. The audience estimation tool takes your complete targeting spec — interests, behaviors, demographics, locations, placements — and returns estimated daily reach, impressions, and results. Use this to validate targeting before campaign launch and to compare different audience strategies.</p>

<h2 id="google-targeting">Google Ads Targeting</h2>
<h3>Keyword Targeting</h3>
<p>Google's primary targeting mechanism is keyword-based. Aidvertaiser provides 11 keyword tools for managing this targeting layer. Add keywords with match types (exact, phrase, broad), set individual bids, and manage negative keywords to exclude irrelevant queries. The search terms report reveals the actual queries triggering your ads, enabling continuous targeting refinement.</p>

<h3>Demographic Targeting</h3>
<p>Refine your Google Ads targeting with demographic overlays. Target or exclude specific age ranges (18-24, 25-34, 35-44, 45-54, 55-64, 65+), genders, parental status, and household income tiers. Apply bid adjustments to demographic segments that perform better or worse than average.</p>

<h3>Performance Max Audience Signals</h3>
<p>Performance Max campaigns use audience signals to guide Google's AI toward your ideal customers. Define signals from your first-party data (customer lists, website visitors), Google audiences (in-market, affinity, life events), custom segments (based on search terms or URLs), and demographics. The AI uses these signals as starting points while continuously discovering new converting audiences.</p>

<h2 id="strategies">Targeting Strategies</h2>
<ul>
<li><strong>Prospecting</strong> — Use broad interest and in-market targeting to reach new potential customers</li>
<li><strong>Remarketing</strong> — Re-engage website visitors and past customers with tailored messaging</li>
<li><strong>Lookalike/Similar audiences</strong> — Find users who resemble your best customers</li>
<li><strong>Layered targeting</strong> — Combine interests, behaviors, and demographics for precise reach</li>
<li><strong>Exclusion targeting</strong> — Exclude existing customers, competitors' employees, or irrelevant demographics to maximize efficiency</li>
</ul>`,
      cs: `<h2 id="overview">Najdete sve publiko</h2>
<p>Rozdil mezi ziskovou reklamou a zbytecnymi vydaji casto spociva v cileni. Aidvertaiser poskytuje nastroje pro cileni na publika napric <strong>Google Ads</strong> i <strong>Meta Ads</strong>, kazdy s vlastnim modelem cileni a prednostmi.</p>

<h2 id="meta-targeting">Cileni na Meta Ads</h2>
<h3>Cileni podle zajmu</h3>
<p>Prohledavejte databazi zajmu Meta podle klicoveho slova a objevujte cilotelne segmenty publika s odhadovanymi velikostmi.</p>

<h3>Behavioralni cileni</h3>
<p>Cilte na uzivatele podle jejich skutecneho chovani sledovaneho Meta — nakupni chovani, pouzivani zarizeni, cestovni vzorce a dalsi.</p>

<h3>Odhad publika</h3>
<p>Pred utracenim koruny odhadnete dosah a denni vysledky pro jakoukoli kombinaci cileni.</p>

<h2 id="google-targeting">Cileni na Google Ads</h2>
<h3>Cileni na klicova slova</h3>
<p>Primarni mechanismus cileni Google je zalozeny na klicovych slovech s 11 nastroji pro spravu.</p>

<h3>Demograficke cileni</h3>
<p>Zpresnte cileni s demografickymi filtry — vekovymi skupinami, pohlavi, rodicovskym stavem a prijmovymi pasmami.</p>

<h3>Signaly publika pro Performance Max</h3>
<p>Definujte signaly z vasich first-party dat, publika Google, vlastnich segmentu a demografickych udaju pro navedeni AI.</p>`,
    },
    platforms: ['google-ads', 'meta-ads'],
    toolExamples: [
      'meta_search_interests',
      'meta_search_behaviors',
      'meta_search_geo_locations',
      'meta_estimate_audience',
      'google_add_keywords',
      'google_search_terms_report',
    ],
    relatedSlugs: ['campaign-management', 'analytics-reporting', 'budget-optimization'],
  },

  /* ==================================================================== */
  /*  4. Analytics & Reporting                                            */
  /* ==================================================================== */
  {
    slug: 'analytics-reporting',
    icon: 'ChartLineUp',
    title: ml('Analytics & Reporting', 'Analytika a reporting'),
    shortDescription: ml(
      'Unified analytics across GA4, Matomo, and advertising platforms. Pull real-time reports, visitor profiles, campaign performance data, search analytics, and custom metric queries — all through conversational AI.',
      'Sjednocena analytika napric GA4, Matomo a reklamnimi platformami. Stahujte real-time reporty, profily navstevniku, data o vykonnosti kampani, analyzy vyhledavani a vlastni dotazy — vse konverzacne.',
    ),
    metaDescription: ml(
      'Unified analytics from GA4, Matomo, Google Ads, and Meta Ads. Real-time reports, visitor profiles, campaign metrics, and search analytics through Aidvertaiser MCP tools.',
      'Sjednocena analytika z GA4, Matomo, Google Ads a Meta Ads. Real-time reporty, profily navstevniku, metriky kampani a analyzy vyhledavani pres Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">All Your Data in One Conversation</h2>
<p>Aidvertaiser connects to <strong>four analytics sources</strong> — Google Analytics 4, Matomo, Google Ads reporting, and Meta Ads insights — giving you a unified view of your marketing performance without switching between dashboards. Ask any question about your data and get answers instantly.</p>
<p>Traditional analytics workflows involve logging into multiple platforms, navigating complex interfaces, building reports, exporting CSVs, and manually combining data. With Aidvertaiser, you simply ask: "How did our campaigns perform last week across all platforms?" The AI pulls data from every connected source and presents a coherent analysis.</p>

<h2 id="ga4-reporting">Google Analytics 4 Reporting</h2>
<p>Query GA4 with any combination of dimensions (page path, source/medium, country, device category, landing page) and metrics (sessions, users, pageviews, engagement rate, conversions, revenue). Specify date ranges, apply filters, and sort by any metric. Real-time reports show current website activity — active users, pages being viewed, and events firing right now.</p>

<h2 id="matomo-reporting">Matomo Reporting</h2>
<p>Matomo provides 9 core reporting tools covering visit summaries, page analytics, entry/exit pages, referrer analysis, search keywords, and device/country breakdowns. Real-time monitoring shows live visitor counts and recent visitor sessions with full action trails. Visitor profiles give you a 360-degree view of individual user behavior across multiple sessions.</p>

<h2 id="ads-reporting">Advertising Performance</h2>
<p>Pull campaign, ad group, ad, and keyword-level performance data from Google Ads using GAQL queries. Get campaign, ad set, and ad-level insights from Meta Ads with flexible date ranges and metric breakdowns. Compare performance across platforms to optimize budget allocation.</p>

<h2 id="search-analytics">Search Analytics</h2>
<p>Google Search Console and Bing Webmaster Tools provide search performance data unavailable anywhere else. See which queries bring users to your site, which pages rank best, and how your search visibility changes over time. Combine organic search data with paid search data for a complete search presence analysis.</p>

<h2 id="workflows">Example Reporting Workflows</h2>
<ul>
<li>"Show me a weekly summary of sessions, users, and conversions from GA4 for the last 4 weeks"</li>
<li>"Compare organic vs paid traffic sources in Matomo for this month"</li>
<li>"What are our top 10 landing pages by conversion rate in GA4?"</li>
<li>"Pull Google Ads campaign performance for the last 30 days — show spend, conversions, CPA, and ROAS"</li>
<li>"How many visitors are on our site right now according to Matomo?"</li>
<li>"Which search queries drove the most clicks in Google Search Console this week?"</li>
</ul>`,
      cs: `<h2 id="overview">Vsechna data v jednom rozhovoru</h2>
<p>Aidvertaiser se pripojuje ke <strong>ctyrrem analytickym zdrojum</strong> — Google Analytics 4, Matomo, reporting Google Ads a Meta Ads insights — a dava vam sjednoceny pohled na vykonnost vaseho marketingu bez prepinani mezi dashboardy.</p>

<h2 id="ga4-reporting">Reporting Google Analytics 4</h2>
<p>Dotazujte se na GA4 s libovolnou kombinaci dimenzi a metrik. Real-time reporty ukazuji aktualni aktivitu na webu.</p>

<h2 id="matomo-reporting">Reporting Matomo</h2>
<p>Matomo poskytuje 9 zakladnich reportovacich nastroju pokryvajicich souhrny navstev, analyzu stranek, zdroje navstevnosti a profily navstevniku v realnem case.</p>

<h2 id="ads-reporting">Vykonnost reklam</h2>
<p>Stahujte data o vykonnosti kampani z Google Ads pomoci GAQL dotazu a z Meta Ads s flexibilnimi casovymi rozsahy.</p>

<h2 id="search-analytics">Analyza vyhledavani</h2>
<p>Google Search Console a Bing Webmaster Tools poskytuji data o vykonnosti vyhledavani nedostupna jinde. Kombinujte organicka a placena vyhledavaci data.</p>`,
    },
    platforms: ['google-analytics', 'matomo', 'google-ads', 'meta-ads', 'search-console', 'bing-webmaster'],
    toolExamples: [
      'ga4_run_report',
      'ga4_run_realtime_report',
      'matomo_get_visits_summary',
      'matomo_get_live_counters',
      'google_gaql_query',
      'meta_get_insights',
      'gsc_search_analytics',
    ],
    relatedSlugs: ['conversion-tracking', 'campaign-management', 'seo-indexing'],
  },

  /* ==================================================================== */
  /*  5. SEO & Indexing                                                   */
  /* ==================================================================== */
  {
    slug: 'seo-indexing',
    icon: 'MagnifyingGlass',
    title: ml('SEO & Indexing', 'SEO a indexace'),
    shortDescription: ml(
      'Monitor and improve your search engine presence. Submit URLs and sitemaps, inspect indexing status, track crawl health, analyze search queries, research keywords, and monitor backlinks across Google and Bing.',
      'Sledujte a zlepsujte svou pritomnost ve vyhledavacich. Odesilajte URL a sitemapy, kontrolujte stav indexace, sledujte zdravi prochazeni, analyzujte vyhledavaci dotazy a monitorujte zpetne odkazy na Google a Bing.',
    ),
    metaDescription: ml(
      'SEO and indexing tools for Google Search Console and Bing Webmaster. URL submission, sitemaps, crawl health, search analytics, keyword research, and link analysis with Aidvertaiser.',
      'SEO a indexacni nastroje pro Google Search Console a Bing Webmaster. Odeslani URL, sitemapy, zdravi prochazeni, analyza vyhledavani a vyzkum klicovych slov s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Complete Search Engine Management</h2>
<p>Organic search is the largest source of website traffic for most businesses, yet managing search engine presence typically requires navigating two separate webmaster tools interfaces. Aidvertaiser unifies <strong>Google Search Console</strong> and <strong>Bing Webmaster Tools</strong> into a single conversational interface with <strong>36 combined tools</strong> for search engine optimization and indexing management.</p>

<h2 id="url-submission">URL Submission & Indexing</h2>
<p>When you publish new content or update existing pages, you want search engines to discover the changes quickly. Aidvertaiser lets you submit URLs to both Google and Bing simultaneously. On Bing, batch-submit up to 500 URLs at once for large-scale content updates or site migrations. Track your submission quotas to stay within platform limits.</p>
<p>Use URL inspection on Google Search Console to check how Google has processed any specific page — indexing status, last crawl date, canonical URL selection, mobile usability, and rich result eligibility.</p>

<h2 id="sitemaps">Sitemap Management</h2>
<p>Sitemaps are the roadmap you give search engines. Submit, list, and manage XML sitemaps on both Google and Bing through Aidvertaiser. Monitor sitemap processing status, error counts, and the number of URLs discovered. Delete outdated sitemaps when your site structure changes.</p>

<h2 id="search-analytics">Search Analytics</h2>
<p>Understand how your site performs in search results. Query search analytics data from both Google and Bing with flexible filters — by query text, page URL, country, device type, and date range. Track impressions, clicks, click-through rates, and average positions. Identify trending queries, declining pages, and opportunities for improvement.</p>

<h2 id="crawl-health">Crawl Health Monitoring</h2>
<p>Bing Webmaster Tools provides crawl management capabilities including crawl statistics, crawl issue detection, and crawl rate configuration. Monitor how frequently Bingbot visits your site, which HTTP status codes it encounters, and whether any resources are blocked from crawling.</p>

<h2 id="keyword-research">Keyword Research</h2>
<p>Bing Webmaster Tools includes built-in keyword research — a feature not available in Google Search Console. Discover new keyword opportunities based on your site content and search trends. Find semantically related keywords to expand your content strategy and identify gaps in your keyword coverage.</p>

<h2 id="link-analysis">Link Analysis</h2>
<p>Backlinks remain one of the strongest ranking signals. Bing's link analysis tools show which external websites link to yours, the anchor text they use, and which pages receive the most inbound links. Use this data for competitive analysis, link building prioritization, and toxic link identification.</p>`,
      cs: `<h2 id="overview">Kompletni sprava vyhledavacu</h2>
<p>Organicke vyhledavani je nejvetsi zdrojem navstevnosti webu pro vetsinu firem. Aidvertaiser sjednocuje <strong>Google Search Console</strong> a <strong>Bing Webmaster Tools</strong> do jednoho konverzacniho rozhrani s <strong>36 kombinovanymi nastroji</strong>.</p>

<h2 id="url-submission">Odeslani URL a indexace</h2>
<p>Odesilajte URL na Google i Bing soucasne. Na Bingu davkove odesilajte az 500 URL naraz. Kontrolujte stav indexace prostrednictvim URL inspekce na Google Search Console.</p>

<h2 id="sitemaps">Sprava sitemap</h2>
<p>Odesilajte, vypisujte a spravujte XML sitemapy na obou platformach. Sledujte stav zpracovani a pocty chyb.</p>

<h2 id="search-analytics">Analyza vyhledavani</h2>
<p>Dotazujte se na data o vykonnosti vyhledavani z Google i Bing s flexibilnimi filtry. Sledujte zobrazeni, kliknuti, CTR a prumernou pozici.</p>

<h2 id="crawl-health">Monitoring zdravi prochazeni</h2>
<p>Sledujte, jak casto Bingbot navstevuje vas web a jake HTTP kody stavu naleza.</p>

<h2 id="keyword-research">Vyzkum klicovych slov</h2>
<p>Objevujte nove prilezitosti klicovych slov a nachazejte semanticky souvisejici klicova slova.</p>`,
    },
    platforms: ['search-console', 'bing-webmaster'],
    toolExamples: [
      'gsc_submit_url',
      'gsc_search_analytics',
      'gsc_inspect_url',
      'gsc_submit_sitemap',
      'bing_submit_url',
      'bing_batch_submit_urls',
      'bing_keyword_research',
      'bing_get_link_counts',
    ],
    relatedSlugs: ['analytics-reporting', 'campaign-management', 'conversion-tracking'],
  },

  /* ==================================================================== */
  /*  6. Budget Optimization                                              */
  /* ==================================================================== */
  {
    slug: 'budget-optimization',
    icon: 'CurrencyDollar',
    title: ml('Budget Optimization', 'Optimalizace rozpoctu'),
    shortDescription: ml(
      'Maximize return on ad spend with intelligent budget allocation. Configure bidding strategies, adjust budgets based on performance data, track cost metrics across platforms, and make data-driven spending decisions.',
      'Maximalizujte navratnost reklamnich vydaju s inteligentni alokaci rozpoctu. Konfigurujte strategie nabidek, upravujte rozpocty na zaklade dat o vykonnosti a delate datove rozhodnuti o utraceni.',
    ),
    metaDescription: ml(
      'Optimize advertising budgets across Google Ads and Meta Ads. Bidding strategies, budget allocation, cost tracking, and ROAS optimization with Aidvertaiser MCP tools.',
      'Optimalizujte reklamni rozpocty napric Google Ads a Meta Ads. Strategie nabidek, alokace rozpoctu, sledovani nakladu a optimalizace ROAS s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Every Dollar Working Harder</h2>
<p>Budget optimization is not about spending less — it is about spending smarter. Aidvertaiser gives you the tools to monitor cost metrics, adjust bidding strategies, reallocate budgets between campaigns and platforms, and identify underperforming spend. All powered by real performance data, not guesswork.</p>
<p>The combination of Google Ads and Meta Ads data in a single interface enables cross-platform budget optimization that is impossible when working in siloed platform dashboards. Compare cost-per-click, cost-per-acquisition, and return on ad spend between platforms to make informed allocation decisions.</p>

<h2 id="bidding-strategies">Bidding Strategy Configuration</h2>
<h3>Google Ads Bidding</h3>
<p>Google Ads offers multiple bidding strategies, each suited to different campaign maturity levels:</p>
<ul>
<li><strong>Manual CPC</strong> — Full control over keyword-level bids. Best for new campaigns with limited conversion data (fewer than 15 conversions per month)</li>
<li><strong>Maximize Clicks</strong> — Automated bidding to get the most clicks within budget. Useful for traffic-focused campaigns</li>
<li><strong>Maximize Conversions</strong> — Google's AI optimizes bids to drive the most conversions. Requires at least 15-20 conversions in the last 30 days for effective optimization</li>
<li><strong>Target CPA</strong> — Set your target cost-per-acquisition and let Google optimize bids to achieve it. Requires 30+ monthly conversions for stability</li>
<li><strong>Target ROAS</strong> — Optimize for return on ad spend. Best for e-commerce with dynamic conversion values. Requires 50+ monthly conversions</li>
<li><strong>Maximize Conversion Value</strong> — Drive the highest total conversion value within budget</li>
</ul>
<p>Aidvertaiser lets you switch between strategies as your campaign data matures. Start with Manual CPC, transition to Maximize Conversions after accumulating data, then graduate to Target CPA or Target ROAS for maximum efficiency.</p>

<h3>Meta Ads Bidding</h3>
<p>Meta Ads bidding operates at the ad set level with options including lowest cost (automatic), cost cap, bid cap, and minimum ROAS. Configure daily or lifetime budgets. Set campaign spending limits. Use Advantage Campaign Budget to let Meta automatically distribute budget across ad sets based on performance.</p>

<h2 id="budget-management">Budget Management</h2>
<p>Monitor and adjust budgets across all active campaigns. Identify campaigns that are under-spending their daily budget (a signal of overly restrictive targeting or low bids) and campaigns that are consistently hitting their budget cap (a signal of potential scaling opportunity).</p>
<p>Use GAQL queries on Google Ads to pull cost data segmented by any dimension — device, location, time of day, audience, keyword. Identify where money is being wasted and where additional investment would yield returns.</p>

<h2 id="performance-tracking">Performance Tracking</h2>
<p>Track the metrics that matter for budget decisions:</p>
<ul>
<li><strong>CPC (Cost Per Click)</strong> — How much you pay for each click. Compare across campaigns, ad groups, and keywords</li>
<li><strong>CPA (Cost Per Acquisition)</strong> — The cost to generate one conversion. Your primary efficiency metric</li>
<li><strong>ROAS (Return On Ad Spend)</strong> — Revenue generated per dollar spent. The ultimate measure of advertising profitability</li>
<li><strong>Impression Share</strong> — The percentage of available impressions your ads captured. Low impression share with good CPA suggests budget increases would be profitable</li>
<li><strong>Quality Score</strong> — Google's assessment of ad relevance. Higher Quality Scores mean lower CPCs for the same position</li>
</ul>

<h2 id="optimization-cycle">The Optimization Cycle</h2>
<ol>
<li><strong>Measure</strong> — Pull performance data from all platforms through Aidvertaiser</li>
<li><strong>Analyze</strong> — Identify high-performing and underperforming campaigns, ad groups, and keywords</li>
<li><strong>Reallocate</strong> — Move budget from underperformers to campaigns with room to scale</li>
<li><strong>Optimize</strong> — Adjust bids, refine targeting, improve ad creatives based on data insights</li>
<li><strong>Repeat</strong> — Continuous optimization is the key to sustained performance improvement</li>
</ol>`,
      cs: `<h2 id="overview">Kazda koruna pracuje tvrdeji</h2>
<p>Optimalizace rozpoctu neznamena utracet mene — znamena utracet chytreji. Aidvertaiser vam dava nastroje pro sledovani nakladovych metrik, upravu strategii nabidek, prerozdelovani rozpoctu mezi kampanemi a platformami a identifikaci neefektivnich vydaju.</p>

<h2 id="bidding-strategies">Konfigurace strategii nabidek</h2>
<h3>Nabidky Google Ads</h3>
<p>Google Ads nabizi vice strategii nabidek — Manualni CPC, Maximalizace kliknuti, Maximalizace konverzi, Cilova CPA a Cilova ROAS. Aidvertaiser vam umozni prepnat mezi strategiemi jak vase kampan ziskava data.</p>

<h3>Nabidky Meta Ads</h3>
<p>Meta Ads nabidky funguji na urovni sady reklam s moznostmi nejnizsi naklady, strop nakladu, strop nabidky a minimalni ROAS.</p>

<h2 id="budget-management">Sprava rozpoctu</h2>
<p>Sledujte a upravujte rozpocty napric vsemi aktivnimi kampanemi. Identifikujte kampane, ktere neutraceni cely denni rozpocet a kampane, ktere neustale dosahuje jeho limitu.</p>

<h2 id="performance-tracking">Sledovani vykonnosti</h2>
<p>Sledujte metriky dulezite pro rozpoctova rozhodnuti: CPC, CPA, ROAS, podil zobrazeni a skore kvality.</p>`,
    },
    platforms: ['google-ads', 'meta-ads'],
    toolExamples: [
      'google_update_campaign',
      'google_gaql_query',
      'meta_update_campaign',
      'meta_update_ad_set',
      'meta_get_insights',
    ],
    relatedSlugs: ['campaign-management', 'conversion-tracking', 'analytics-reporting'],
  },
];
