/* -------------------------------------------------------------------------- */
/*  Use Case Data — Aidvertaiser Marketing Website                           */
/* -------------------------------------------------------------------------- */

export interface UseCase {
  slug: string;
  icon: string;
  title: Record<string, string>;
  shortDescription: Record<string, string>;
  metaDescription: Record<string, string>;
  content: Record<string, string>;
  platforms: string[];
  relatedSlugs: string[];
}

/* Helper: for languages we haven't translated yet, fall back to English */
function ml(en: string, cs: string): Record<string, string> {
  return { en, cs, fr: en, es: en, zh: en, hi: en, pt: en, pl: en, ar: en, bn: en };
}

export const useCases: UseCase[] = [
  /* ==================================================================== */
  /*  1. Multi-Platform Campaigns                                         */
  /* ==================================================================== */
  {
    slug: 'multi-platform-campaigns',
    icon: 'Broadcast',
    title: ml('Multi-Platform Campaigns', 'Kampane napric platformami'),
    shortDescription: ml(
      'Launch coordinated advertising campaigns on Google Ads and Meta Ads simultaneously. Set up Search campaigns for intent-driven traffic and social campaigns for audience-driven awareness in a single conversation.',
      'Spustete koordinovane reklamni kampane na Google Ads a Meta Ads soucasne. Nastavte Search kampane pro navstevnost rizenou zamerem a socialni kampane pro budovani povedomi v jedinem rozhovoru.',
    ),
    metaDescription: ml(
      'Launch coordinated campaigns on Google Ads and Meta Ads with AI. Multi-platform campaign setup, management, and optimization through Aidvertaiser MCP tools.',
      'Spoustejte koordinovane kampane na Google Ads a Meta Ads s AI. Nastaveni, sprava a optimalizace kampani napric platformami pres Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="the-challenge">The Multi-Platform Challenge</h2>
<p>Modern advertising demands presence on multiple platforms. Google Ads captures users who are actively searching for your products or services — high-intent traffic that converts at premium rates. Meta Ads reaches users based on interests, behaviors, and demographics — ideal for awareness, consideration, and retargeting. Most businesses need both, but managing them separately creates fragmentation, inconsistency, and wasted time.</p>
<p>The typical workflow involves logging into Google Ads Manager, building a campaign, switching to Meta Ads Manager, building another campaign, then switching between both platforms to monitor performance and make adjustments. Campaign names, targeting strategies, and budget allocations are tracked in spreadsheets. Performance comparison requires manual data export and analysis.</p>

<h2 id="the-solution">Unified Campaign Launch</h2>
<p>With Aidvertaiser, you can launch campaigns on both platforms in a single conversation. Describe your campaign goals, target audience, budget, and creative strategy to your AI assistant. It creates the Google Ads Search campaign with keywords, ad groups, and Responsive Search Ads while simultaneously building the Meta Ads campaign with audience targeting, ad sets, and creatives.</p>
<p>Here is what a coordinated launch looks like:</p>
<ol>
<li><strong>Brief your AI</strong> — "I want to promote our new CRM software to small business owners in the US with a $5,000 monthly budget split 60/40 between Google and Meta"</li>
<li><strong>Google Ads setup</strong> — The AI creates a Search campaign targeting CRM-related keywords with exact and phrase match, sets up ad groups by keyword theme, creates RSAs with your value propositions, and configures Target CPA bidding</li>
<li><strong>Meta Ads setup</strong> — Simultaneously, it creates a traffic campaign targeting small business owners interested in CRM, business software, and entrepreneurship, with age targeting 25-55, US-only geographic targeting, and automatic placements</li>
<li><strong>Budget allocation</strong> — $3,000/month to Google Ads (high-intent search), $2,000/month to Meta Ads (audience prospecting)</li>
<li><strong>Tracking</strong> — Conversion actions set up on Google Ads and Meta Pixel events configured for the same conversion goals</li>
</ol>

<h2 id="ongoing-management">Ongoing Cross-Platform Management</h2>
<p>Once campaigns are running, Aidvertaiser enables cross-platform performance monitoring. Compare CPC, CPA, and ROAS between Google and Meta in a single query. Identify which platform delivers better results for specific audience segments. Shift budget between platforms based on data, not assumptions.</p>
<p>When you discover a high-performing keyword on Google Ads, create a corresponding interest-based audience on Meta to reach users earlier in the funnel. When a Meta audience shows strong engagement but poor conversion, build a remarketing campaign on Google to capture those users when they search with purchase intent.</p>

<h2 id="coordination-strategies">Coordination Strategies</h2>
<ul>
<li><strong>Full-funnel coverage</strong> — Meta for awareness and consideration, Google for intent and conversion</li>
<li><strong>Sequential messaging</strong> — Use Meta to introduce your brand, then retarget on Google when users search your brand or product category</li>
<li><strong>Budget balancing</strong> — Shift spend to the platform delivering better CPA week over week</li>
<li><strong>Consistent messaging</strong> — Ensure ad copy, offers, and landing pages are aligned across both platforms</li>
<li><strong>Unified conversion tracking</strong> — Track the same conversion events on both platforms for accurate cross-platform attribution</li>
</ul>

<h2 id="who-benefits">Who Benefits</h2>
<p>Multi-platform campaigns are particularly valuable for:</p>
<ul>
<li><strong>E-commerce businesses</strong> — Reach shoppers across search and social for maximum coverage</li>
<li><strong>B2B companies</strong> — Target decision-makers through LinkedIn interest proxies on Meta and commercial-intent keywords on Google</li>
<li><strong>Local businesses</strong> — Geographic targeting on both platforms ensures you reach local customers wherever they browse</li>
<li><strong>Agencies</strong> — Manage multiple client campaigns across platforms from a single AI interface</li>
</ul>`,
      cs: `<h2 id="the-challenge">Vyzva vice platforem</h2>
<p>Moderni reklama vyzaduje pritomnost na vice platformach. Google Ads zachytava uzivatele aktivne hledajici vase produkty. Meta Ads oslovuje uzivatele na zaklade zajmu a chovani. Vetsina firem potrebuje oboje, ale oddelena sprava vytvari fragmentaci a zbytecne ztraceny cas.</p>

<h2 id="the-solution">Sjednocene spusteni kampani</h2>
<p>S Aidvertaiser muzete spustit kampane na obou platformach v jedinem rozhovoru. Popiste sve cile, cilove publikum, rozpocet a kreativni strategii svemu AI asistentovi. Ten vytvori kampan Google Ads Search s klicovymi slovy a zaroven postavi kampan Meta Ads s cilenim na publikum.</p>

<h2 id="ongoing-management">Prubezna sprava napric platformami</h2>
<p>Porovnavejte CPC, CPA a ROAS mezi Google a Meta v jedinem dotazu. Identifikujte, ktera platforma prinasi lepsi vysledky pro konkretni segmenty publika. Presouvejte rozpocet mezi platformami na zaklade dat.</p>

<h2 id="coordination-strategies">Koordinacni strategie</h2>
<ul>
<li><strong>Pokryti celeho funnelu</strong> — Meta pro povedomi, Google pro zamer a konverzi</li>
<li><strong>Sekvencni messaging</strong> — Meta pro predstaveni znacky, Google pro retargeting pri vyhledavani</li>
<li><strong>Vyrovnavani rozpoctu</strong> — Presouvejte vydaje na platformu s lepsi CPA</li>
<li><strong>Konzistentni messaging</strong> — Sladte texty reklam, nabidky a landing pages napric platformami</li>
</ul>`,
    },
    platforms: ['google-ads', 'meta-ads'],
    relatedSlugs: ['cross-platform-analytics', 'conversion-optimization', 'audience-research'],
  },

  /* ==================================================================== */
  /*  2. Cross-Platform Analytics                                         */
  /* ==================================================================== */
  {
    slug: 'cross-platform-analytics',
    icon: 'ChartPieSlice',
    title: ml('Cross-Platform Analytics', 'Analyza napric platformami'),
    shortDescription: ml(
      'Get a unified view of your marketing performance from GA4, Matomo, Google Search Console, and Bing Webmaster Tools. Combine organic and paid data, compare platforms, and identify trends across all channels.',
      'Ziskejte sjednoceny pohled na vykonnost vaseho marketingu z GA4, Matomo, Google Search Console a Bing Webmaster Tools. Kombinujte organicka a placena data a identifikujte trendy napric kanaly.',
    ),
    metaDescription: ml(
      'Unified analytics from GA4, Matomo, Search Console, and Bing. Cross-platform reporting, organic vs paid analysis, and trend identification with Aidvertaiser MCP tools.',
      'Sjednocena analytika z GA4, Matomo, Search Console a Bing. Reporting napric platformami, analyza organicke vs placene navstevnosti s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="the-challenge">Data Silos Kill Insights</h2>
<p>Most marketing teams work with data scattered across multiple platforms. GA4 shows website behavior. Matomo provides privacy-first visitor analytics. Google Search Console reveals organic search performance. Bing Webmaster Tools covers the Bing ecosystem. Google Ads and Meta Ads each have their own reporting dashboards. Getting a holistic view requires logging into six different platforms, exporting data, and manually combining it in spreadsheets.</p>
<p>This fragmentation leads to missed insights. A drop in organic traffic from Search Console might explain a spike in paid CPC on Google Ads. A new high-performing landing page in GA4 might suggest keyword expansion opportunities in Search Console. These connections are invisible when data lives in silos.</p>

<h2 id="the-solution">One Conversation, All Your Data</h2>
<p>Aidvertaiser connects to all six platforms through dedicated MCP tools. Ask any question about your marketing data and the AI pulls from the appropriate source — or combines data from multiple sources for cross-platform analysis.</p>
<p>Example queries that span multiple platforms:</p>
<ul>
<li>"Compare our organic traffic from GA4 with our organic search impressions from Search Console for the last 30 days"</li>
<li>"Which landing pages have the highest engagement in Matomo but the lowest organic rankings in Search Console?"</li>
<li>"Show me the correlation between Bing organic traffic and our Google Ads spending this quarter"</li>
<li>"What percentage of our total website traffic comes from paid sources vs organic sources vs direct?"</li>
</ul>

<h2 id="ga4-matomo">GA4 + Matomo: Complementary Analytics</h2>
<p>Running both GA4 and Matomo gives you the best of both worlds. GA4 provides Google's machine learning insights, predictive metrics, and tight integration with Google Ads. Matomo provides full data ownership, GDPR compliance without consent banners (when self-hosted), and individual visitor profiles that GA4 does not offer.</p>
<p>Use Aidvertaiser to compare metrics between the two platforms, validate data accuracy, and leverage the unique strengths of each. Matomo's real-time visitor logs show exactly what individual users are doing on your site right now. GA4's predictive metrics forecast future revenue and churn probability.</p>

<h2 id="search-platforms">Search Console + Bing: Complete Search Picture</h2>
<p>Google dominates search, but Bing reaches over 1 billion users through Edge, Windows, and Yahoo. Monitoring both gives you a complete picture of your search visibility. Compare query performance, identify keywords where you rank well on one engine but not the other, and discover Bing-specific opportunities through keyword research tools that Search Console does not offer.</p>

<h2 id="reporting-workflows">Unified Reporting Workflows</h2>
<ul>
<li><strong>Weekly performance review</strong> — Pull key metrics from all platforms in one conversation, compare week-over-week trends</li>
<li><strong>Monthly business review</strong> — Comprehensive analysis of organic and paid channels, budget efficiency, and audience growth</li>
<li><strong>Campaign launch analysis</strong> — Monitor new campaign impact across analytics platforms in real time</li>
<li><strong>Content performance</strong> — Combine page analytics from GA4/Matomo with search rankings from GSC/Bing</li>
</ul>`,
      cs: `<h2 id="the-challenge">Datove sila zabiji poznatky</h2>
<p>Vetsina marketingovych tymu pracuje s daty roztrousenymi napric platformami. GA4 ukazuje chovani na webu. Matomo poskytuje analyzu navstevniku s durazem na soukromi. Google Search Console odhaluje vykon organickeho vyhledavani. Ziskani celostniho pohledu vyzaduje prihlaseni do sesti ruznych platforem.</p>

<h2 id="the-solution">Jeden rozhovor, vsechna data</h2>
<p>Aidvertaiser se pripojuje ke vsem sesti platformam a umoznuje dotazy napric zdroji dat v jedinem rozhovoru.</p>

<h2 id="ga4-matomo">GA4 + Matomo: Doplnkova analytika</h2>
<p>Provoz GA4 i Matomo vam dava to nejlepsi z obou svetu. GA4 poskytuje strojove uceni Google a integraci s Google Ads. Matomo poskytuje plne vlastnictvi dat a soulad s GDPR.</p>

<h2 id="search-platforms">Search Console + Bing: Kompletni obraz vyhledavani</h2>
<p>Google dominuje vyhledavani, ale Bing oslovuje pres 1 miliardu uzivatelu. Sledovani obou dava uplny obraz vasi viditelnosti ve vyhledavani.</p>`,
    },
    platforms: ['google-analytics', 'matomo', 'search-console', 'bing-webmaster'],
    relatedSlugs: ['multi-platform-campaigns', 'conversion-optimization', 'search-performance'],
  },

  /* ==================================================================== */
  /*  3. Conversion Optimization                                          */
  /* ==================================================================== */
  {
    slug: 'conversion-optimization',
    icon: 'TrendUp',
    title: ml('Conversion Optimization', 'Optimalizace konverzi'),
    shortDescription: ml(
      'Optimize your conversion tracking and attribution for maximum accuracy. Set up server-side tracking, upload offline conversions, enable enhanced conversions, and refine attribution across Google Ads and Meta Ads.',
      'Optimalizujte sledovani konverzi a atribuci pro maximalni presnost. Nastavte serverove sledovani, nahrajte offline konverze, povolte vylepsene konverze a zpresnte atribuci na Google Ads a Meta Ads.',
    ),
    metaDescription: ml(
      'Optimize conversion tracking across Google Ads and Meta Ads. Server-side tracking, offline conversions, enhanced conversions, and attribution refinement with Aidvertaiser.',
      'Optimalizujte sledovani konverzi napric Google Ads a Meta Ads. Serverove sledovani, offline konverze a vylepsene konverze s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="the-challenge">The Attribution Crisis</h2>
<p>Conversion tracking has never been more challenging. Browser privacy restrictions (Safari ITP, Firefox ETP, Chrome's Privacy Sandbox), ad blockers, cookie consent requirements, and cross-device user journeys all conspire to make traditional pixel-based tracking increasingly unreliable. Businesses that rely solely on browser-side pixels are losing 15-30% of their conversion data, leading to suboptimal bidding, inaccurate reporting, and poor budget decisions.</p>

<h2 id="the-solution">Multi-Layer Tracking Architecture</h2>
<p>Aidvertaiser enables a resilient, multi-layer conversion tracking architecture that combines browser-side and server-side methods for maximum data capture:</p>

<h3>Layer 1: Browser-Side Pixels</h3>
<p>Set up Meta Pixels and Google Ads conversion tags as your baseline tracking layer. These capture conversions from users who allow cookies and have not installed ad blockers. Aidvertaiser's pixel management tools let you create, configure, and monitor pixels through natural language.</p>

<h3>Layer 2: Server-Side Events</h3>
<p>Meta's Conversions API (CAPI) and Google's Enhanced Conversions send conversion data server-to-server, bypassing all browser restrictions. These events are deduplicated against browser events to avoid double-counting. Aidvertaiser provides direct tools for sending CAPI events with user data parameters for enhanced matching.</p>

<h3>Layer 3: Offline Conversions</h3>
<p>For conversions that happen offline — phone calls, in-store purchases, B2B deal closings — offline conversion upload connects CRM data with ad platform data. Upload conversions with Google Click IDs (GCLIDs) to Google Ads and with hashed user data to Meta. This gives bidding algorithms the complete picture of which ad interactions lead to real revenue.</p>

<h3>Layer 4: Custom Conversions</h3>
<p>Define custom conversion events on Meta based on URL rules or event parameters without modifying pixel code. Create custom conversion actions on Google Ads with tailored windows, values, and counting methods. Track micro-conversions alongside macro-conversions to understand the full conversion funnel.</p>

<h2 id="optimization-workflow">The Optimization Workflow</h2>
<ol>
<li><strong>Audit current tracking</strong> — Use Aidvertaiser to list all conversion actions on Google Ads and Meta. Identify gaps and redundancies</li>
<li><strong>Implement server-side tracking</strong> — Set up Conversions API on Meta and Enhanced Conversions on Google for browser-independent measurement</li>
<li><strong>Configure offline uploads</strong> — Connect CRM data with ad platforms for closed-loop attribution</li>
<li><strong>Refine conversion windows</strong> — Match conversion windows to your actual sales cycle (7 days for e-commerce, 30-90 days for B2B)</li>
<li><strong>Validate and monitor</strong> — Regularly check conversion counts, compare browser vs server events, and investigate discrepancies</li>
</ol>

<h2 id="impact">Impact on Campaign Performance</h2>
<p>Businesses that implement comprehensive conversion tracking see measurable improvements:</p>
<ul>
<li><strong>5-15% more attributed conversions</strong> from Enhanced Conversions and server-side tracking</li>
<li><strong>10-20% improvement in Smart Bidding performance</strong> from feeding more accurate conversion data to algorithms</li>
<li><strong>Accurate ROAS measurement</strong> when offline conversions are included</li>
<li><strong>Better budget allocation</strong> when you can see which campaigns drive real revenue, not just form fills</li>
</ul>`,
      cs: `<h2 id="the-challenge">Krize atribuce</h2>
<p>Sledovani konverzi nebylo nikdy narocnejsi. Omezeni soukromi prohlizecu, blokatory reklam a souhlas s cookies delaji tradici sledovani na zaklade pixelu stale mene spolehlivym. Firmy spolechajici se na pixely ztraceli 15-30% konverznich dat.</p>

<h2 id="the-solution">Vicevrstva architektura sledovani</h2>
<h3>Vrstva 1: Pixely na strane prohlizece</h3>
<p>Nastavte Meta Pixely a konverzni tagy Google Ads jako zakladni vrstvu sledovani.</p>

<h3>Vrstva 2: Serverove udalosti</h3>
<p>Meta Conversions API a Google Enhanced Conversions odesilavaji konverzni data server-to-server, obchazejici vsechna omezeni prohlizece.</p>

<h3>Vrstva 3: Offline konverze</h3>
<p>Propojte CRM data s reklamnimi platformami pro atribuci offline konverzi — telefonatych hovorech, obchodu v prodejne a B2B obchodech.</p>

<h3>Vrstva 4: Vlastni konverze</h3>
<p>Definujte vlastni konverzni udalosti na zaklade pravidel URL nebo parametru udalosti.</p>

<h2 id="impact">Dopad na vykonnost kampani</h2>
<ul>
<li>5-15% vice atribuovanych konverzi z vylepsenych konverzi</li>
<li>10-20% zlepseni vykonu Smart Bidding z presnejsich konverznich dat</li>
<li>Presne mereni ROAS pri zahrnutych offline konverzich</li>
</ul>`,
    },
    platforms: ['google-ads', 'meta-ads'],
    relatedSlugs: ['multi-platform-campaigns', 'cross-platform-analytics', 'search-performance'],
  },

  /* ==================================================================== */
  /*  4. Search Performance                                               */
  /* ==================================================================== */
  {
    slug: 'search-performance',
    icon: 'MagnifyingGlass',
    title: ml('Search Performance Monitoring', 'Monitoring vykonu vyhledavani'),
    shortDescription: ml(
      'Monitor your search rankings and visibility across Google and Bing. Track query performance, inspect indexing status, manage sitemaps, identify crawl issues, and research keywords — all through AI conversation.',
      'Sledujte sve pozice a viditelnost ve vyhledavani na Google a Bing. Sledujte vykon dotazu, kontrolujte stav indexace, spravujte sitemapy, identifikujte problemy s prochazenim a vyzkumejte klicova slova.',
    ),
    metaDescription: ml(
      'Monitor search rankings on Google and Bing. Query tracking, indexing inspection, sitemap management, crawl monitoring, and keyword research with Aidvertaiser MCP tools.',
      'Sledujte pozice ve vyhledavani na Google a Bing. Sledovani dotazu, inspekce indexace, sprava sitemap a vyzkum klicovych slov s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="the-challenge">Search Visibility Is Revenue</h2>
<p>For most websites, organic search is the single largest traffic source. A drop in search rankings directly impacts revenue. Yet many businesses only check their search performance reactively — after traffic has already declined. Proactive search monitoring catches issues early and identifies opportunities before competitors do.</p>
<p>The challenge is compounded by the need to monitor two search engines: Google (90%+ market share) and Bing (growing to 1 billion+ users through Edge and Windows integration). Each has its own webmaster tools, its own metrics, and its own optimization levers.</p>

<h2 id="the-solution">Unified Search Monitoring</h2>
<p>Aidvertaiser combines <strong>Google Search Console</strong> (15 tools) and <strong>Bing Webmaster Tools</strong> (21 tools) into a single conversational interface. Monitor both search engines without switching between dashboards.</p>

<h3>Query Performance Tracking</h3>
<p>Track which search queries bring users to your site from both Google and Bing. See impressions, clicks, click-through rates, and average positions for each query. Identify trending queries gaining traction and declining queries losing ground. Compare your performance on the same queries across both search engines.</p>

<h3>Page-Level Analysis</h3>
<p>Understand which pages perform best in search results. Identify pages with high impressions but low CTR (opportunity to improve titles and meta descriptions). Find pages with declining positions (signal for content refresh). Compare page performance between Google and Bing to spot platform-specific issues.</p>

<h3>Indexing & Crawl Health</h3>
<p>Monitor the technical foundation of your search presence. Use URL inspection on Google to check indexing status, canonical selection, and mobile usability. Monitor Bing crawl statistics to understand crawl frequency and response codes. Detect crawl issues on both platforms before they impact rankings.</p>

<h3>Sitemap Management</h3>
<p>Submit and monitor sitemaps on both Google and Bing. Ensure all your important pages are discoverable. Track sitemap processing status and error counts. When you launch new content or restructure your site, submit updated sitemaps immediately through Aidvertaiser.</p>

<h3>Keyword Research & Expansion</h3>
<p>Bing Webmaster Tools provides built-in keyword research that Google Search Console lacks. Discover new keyword opportunities based on your site content. Find related keywords to expand your content strategy. Use these insights to inform both organic content planning and paid search keyword selection.</p>

<h2 id="monitoring-cadence">Recommended Monitoring Cadence</h2>
<ul>
<li><strong>Daily</strong> — Check for crawl errors and indexing issues</li>
<li><strong>Weekly</strong> — Review query performance trends, identify new opportunities and declining terms</li>
<li><strong>Monthly</strong> — Comprehensive search visibility analysis, sitemap audit, backlink review</li>
<li><strong>After site changes</strong> — Submit updated sitemaps, request re-indexing of changed URLs</li>
</ul>`,
      cs: `<h2 id="the-challenge">Viditelnost ve vyhledavani je prijem</h2>
<p>Pro vetsinu webu je organicke vyhledavani nejvetsi zdrojem navstevnosti. Pokles pozic ve vyhledavani primo ovlivnuje prijmy. Proaktivni monitoring vyhledavani odhaluje problemy vcas.</p>

<h2 id="the-solution">Sjednoceny monitoring vyhledavani</h2>
<p>Aidvertaiser kombinuje <strong>Google Search Console</strong> (15 nastroju) a <strong>Bing Webmaster Tools</strong> (21 nastroju) do jednoho konverzacniho rozhrani.</p>

<h3>Sledovani vykonu dotazu</h3>
<p>Sledujte, ktere dotazy prinaseji navstevniky z Google i Bing. Porovnavejte vykon na stejnych dotazech napric obema vyhledavaci.</p>

<h3>Analyza na urovni stranek</h3>
<p>Identifikujte stranky s vysokymi zobrazenimi ale nizkym CTR a stranky s klesajicimi pozicemi.</p>

<h3>Zdravi indexace a prochazeni</h3>
<p>Sledujte technicke zaklady vasi vyhledavaci pritomnosti na obou platformach.</p>

<h3>Vyzkum klicovych slov</h3>
<p>Vyuzijte vestaveny vyzkum klicovych slov v Bing Webmaster Tools pro objevovani novych prilezitosti.</p>`,
    },
    platforms: ['search-console', 'bing-webmaster'],
    relatedSlugs: ['cross-platform-analytics', 'audience-research', 'multi-platform-campaigns'],
  },

  /* ==================================================================== */
  /*  5. Audience Research                                                */
  /* ==================================================================== */
  {
    slug: 'audience-research',
    icon: 'Users',
    title: ml('Audience Research', 'Vyzkum publika'),
    shortDescription: ml(
      'Deep audience analysis across platforms. Explore interest categories on Meta, estimate audience sizes, analyze visitor demographics in GA4 and Matomo, and research search behavior through Search Console and Bing data.',
      'Hluboka analyza publika napric platformami. Prozkoumejte kategorie zajmu na Meta, odhadujte velikost publika, analyzujte demografii navstevniku v GA4 a Matomo a vyzkumejte vyhledavaci chovani.',
    ),
    metaDescription: ml(
      'Deep audience research across Meta Ads, GA4, Matomo, and search platforms. Interest exploration, audience sizing, demographics, and behavioral analysis with Aidvertaiser.',
      'Hloubkovy vyzkum publika napric Meta Ads, GA4, Matomo a vyhledavacimi platformami. Pruzkum zajmu, velikost publika a analyza chovani s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="the-challenge">Know Your Audience</h2>
<p>Effective advertising starts with deep audience understanding. Who are your customers? What are they interested in? How do they behave online? Where do they search, browse, and buy? These questions are answered across multiple platforms, but piecing together a complete audience picture typically requires hours of manual research.</p>

<h2 id="meta-audience">Meta Ads Audience Research</h2>
<p>Meta's advertising platform holds the richest audience data in digital marketing, built from billions of user interactions across Facebook, Instagram, WhatsApp, and Messenger. Aidvertaiser gives you direct access to this data through four targeting research tools.</p>

<h3>Interest Exploration</h3>
<p>Search Meta's interest taxonomy by keyword. When you search "cooking," you discover targetable interests like Home cooking, Baking, Italian cuisine, Cooking shows, Kitchen appliances, and Food photography — each with estimated audience sizes. Map out your audience's interest graph to find unexpected targeting opportunities.</p>

<h3>Behavioral Insights</h3>
<p>Go beyond interests to behaviors — actual actions people take. Target users who are small business owners, early technology adopters, frequent online shoppers, or frequent travelers. Behavioral targeting is more predictive than interest targeting because it is based on actions rather than self-reported preferences.</p>

<h3>Audience Sizing</h3>
<p>Before launching any campaign, use the audience estimation tool to validate your targeting. Input your complete targeting spec — interests, behaviors, demographics, locations — and get estimated daily reach, impressions, and results. Compare multiple audience definitions side by side to find the optimal balance between reach and relevance.</p>

<h2 id="analytics-audience">Analytics-Based Audience Research</h2>
<h3>GA4 Audience Insights</h3>
<p>GA4 reports reveal who is already visiting your site. Break down visitors by country, device category, browser, acquisition source, and engagement level. Identify which audience segments convert best. Use these insights to refine your advertising targeting — double down on segments that convert and exclude those that do not.</p>

<h3>Matomo Visitor Profiles</h3>
<p>Matomo's visitor profile tools provide individual-level audience understanding. See exactly which pages a visitor viewed, how long they spent, what they searched for on your site, and whether they converted. Aggregate these profiles to identify common behavioral patterns among your best customers.</p>

<h2 id="search-audience">Search-Based Audience Research</h2>
<p>Search data reveals intent — what people are actively looking for. Google Search Console shows which queries bring users to your site and which pages they land on. Bing keyword research discovers new terms related to your content. Together, these tools reveal the language your audience uses and the problems they are trying to solve.</p>

<h2 id="workflow">Audience Research Workflow</h2>
<ol>
<li><strong>Start with analytics</strong> — Use GA4 and Matomo to understand who currently visits and converts</li>
<li><strong>Expand with search data</strong> — Use Search Console and Bing to understand what your audience searches for</li>
<li><strong>Explore on Meta</strong> — Search interests and behaviors to find targetable audience segments that match your ideal customer</li>
<li><strong>Size and validate</strong> — Use audience estimation to validate that your targeting reaches enough people</li>
<li><strong>Test and refine</strong> — Launch campaigns with your audience hypothesis and let real performance data validate or adjust your targeting</li>
</ol>`,
      cs: `<h2 id="the-challenge">Poznejmte sve publikum</h2>
<p>Efektivni reklama zacina hlubokym porozumenim publiku. Kdo jsou vasi zakaznici? Co je zajima? Jak se chovaji online? Tyto otazky jsou zodpovedeny napric vice platformami.</p>

<h2 id="meta-audience">Vyzkum publika Meta Ads</h2>
<h3>Pruzkum zajmu</h3>
<p>Prohledavejte taxonomii zajmu Meta podle klicoveho slova a objevujte cilotelne segmenty publika s odhadovanymi velikostmi.</p>

<h3>Behavioralni poznatky</h3>
<p>Jdete nad ramec zajmu k chovani — skutecnym akcim, ktere lide vykonavaji.</p>

<h3>Dimenzovani publika</h3>
<p>Pred spustenim kampane vyuzijte nastroj pro odhad publika k validaci vaseho cileni.</p>

<h2 id="analytics-audience">Vyzkum publika z analytiky</h2>
<h3>GA4</h3>
<p>Reporty GA4 odhaluji, kdo uz navstevuje vas web. Identifikujte segmenty, ktere nejlepe konvertuji.</p>

<h3>Matomo</h3>
<p>Profily navstevniku Matomo poskytuji porozumeni na individualni urovni.</p>

<h2 id="search-audience">Vyzkum publika z vyhledavani</h2>
<p>Vyhledavaci data odhaluji zamer — co lide aktivne hledaji. Search Console a Bing keyword research odhaluji jazyk vaseho publika.</p>`,
    },
    platforms: ['meta-ads', 'google-analytics', 'matomo', 'search-console', 'bing-webmaster'],
    relatedSlugs: ['multi-platform-campaigns', 'cross-platform-analytics', 'search-performance'],
  },

  /* ==================================================================== */
  /*  6. Click Fraud Prevention                                           */
  /* ==================================================================== */
  {
    slug: 'click-fraud-prevention',
    icon: 'ShieldCheck',
    title: ml('Click Fraud Prevention', 'Prevence podvodnich kliknuti'),
    shortDescription: ml(
      'Monitor and protect your ad spend from click fraud. Track suspicious patterns in search terms reports, configure IP exclusions, analyze traffic quality through analytics, and identify bot activity across platforms.',
      'Sledujte a chrante sve reklamni vydaje pred podvodnymi kliknutimi. Sledujte podezrele vzorce v reportech vyhledavacich dotazu, konfigurujte vylouceni IP, analyzujte kvalitu navstevnosti a identifikujte aktivitu botu.',
    ),
    metaDescription: ml(
      'Protect ad spend from click fraud. Search terms analysis, IP exclusions, traffic quality monitoring, and bot detection across Google Ads and Meta Ads with Aidvertaiser.',
      'Chrante reklamni vydaje pred podvodnymi kliknutimi. Analyza vyhledavacich dotazu, vylouceni IP, monitoring kvality navstevnosti a detekce botu s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="the-challenge">The Click Fraud Problem</h2>
<p>Click fraud costs advertisers an estimated $100 billion annually worldwide. Competitors clicking your ads, bot networks generating fake clicks, click farms draining budgets, and accidental clicks from irrelevant audiences — all consume ad spend without generating any business value. Industry studies estimate that 14-20% of all PPC clicks are fraudulent or invalid.</p>
<p>Google and Meta have built-in fraud detection systems, but they catch only a portion of fraudulent activity. Sophisticated click fraud often mimics legitimate user behavior and evades automated detection. Proactive monitoring is essential for protecting your advertising investment.</p>

<h2 id="the-solution">Multi-Layer Fraud Detection</h2>
<p>Aidvertaiser enables a comprehensive approach to click fraud prevention by combining data from advertising platforms, analytics systems, and search tools.</p>

<h3>Search Terms Analysis</h3>
<p>The Google Ads search terms report is your first line of defense. Pull the report regularly to identify suspicious patterns: irrelevant search queries triggering your ads, the same query generating multiple clicks in short time periods, and queries from unexpected geographic locations. Use this data to build negative keyword lists that block fraudulent traffic at the source.</p>

<h3>IP Exclusion Management</h3>
<p>When you identify suspicious IP addresses — through analytics, server logs, or third-party fraud detection tools — add them to your Google Ads IP exclusion list. Aidvertaiser can manage up to 500 IP exclusions per campaign and 500 at the account level. Exclude competitor office IPs, your own office IPs (preventing employee clicks), and identified bot IP ranges.</p>

<h3>Analytics-Based Quality Monitoring</h3>
<p>GA4 and Matomo provide behavioral signals that distinguish legitimate visitors from fraudulent clicks. Monitor bounce rate by traffic source — fraudulent clicks typically show near-100% bounce rates. Check time on site — bot clicks often result in zero-second sessions. Analyze engagement patterns — legitimate users scroll, click, and interact; bots do not.</p>

<h3>Traffic Source Validation</h3>
<p>Compare click data from Google Ads with session data in GA4 and Matomo. Significant discrepancies between ad clicks and analytics sessions may indicate click fraud. If Google reports 1,000 clicks but GA4 shows only 700 sessions from paid search, the gap deserves investigation.</p>

<h2 id="prevention-strategies">Prevention Strategies</h2>
<ul>
<li><strong>Aggressive negative keywords</strong> — Use search terms reports to identify and exclude irrelevant queries that attract bot clicks</li>
<li><strong>Geographic restrictions</strong> — Set location targeting to "Presence only" (not "Presence or interest") to exclude clicks from irrelevant locations</li>
<li><strong>Ad scheduling</strong> — If fraud patterns correlate with specific time periods, reduce bids or pause ads during those windows</li>
<li><strong>Device targeting</strong> — If fraud is concentrated on specific device types, apply negative bid adjustments</li>
<li><strong>Network exclusions</strong> — Disable Search Partners on Google Ads campaigns, which carry 2-3x higher fraud rates</li>
<li><strong>Regular monitoring</strong> — Set up weekly fraud detection reviews using Aidvertaiser to pull cross-platform data</li>
</ul>

<h2 id="monitoring-workflow">Weekly Fraud Monitoring Workflow</h2>
<ol>
<li>Pull Google Ads search terms report for the past 7 days</li>
<li>Identify queries with high clicks but zero conversions and suspiciously high CTR</li>
<li>Add irrelevant queries as negative keywords</li>
<li>Compare Google Ads click counts with GA4 session counts by campaign</li>
<li>Check Matomo for sessions with zero engagement from paid traffic sources</li>
<li>Review IP addresses showing repetitive click patterns</li>
<li>Add suspicious IPs to campaign exclusion lists</li>
<li>Document findings and track fraud prevention savings over time</li>
</ol>`,
      cs: `<h2 id="the-challenge">Problem podvodnich kliknuti</h2>
<p>Podvodna kliknuti stoji inzerenty odhadovanych 100 miliard dolaru rocne po celem svete. Konkurenti klikajici na vase reklamy, botove site generujici falecna kliknuti a klikaci farmy vysavajici rozpocty — to vse spotrebovava reklamni vydaje bez jakehokoliv podniku. Studie odhaduji, ze 14-20% vsech PPC kliknuti je podvodnych.</p>

<h2 id="the-solution">Vicevrstva detekce podvodu</h2>
<h3>Analyza vyhledavacich dotazu</h3>
<p>Report vyhledavacich dotazu Google Ads je vasi prvni linii obrany. Identifikujte podezrele vzorce a vytvarejte negativni klicova slova.</p>

<h3>Sprava vylouceni IP</h3>
<p>Pridejte podezrele IP adresy do vaseho seznamu vylouceni Google Ads. Spravujte az 500 vylouceni IP na kampan.</p>

<h3>Monitoring kvality z analytiky</h3>
<p>GA4 a Matomo poskytuji behavioralni signaly odlisujici legitimni navstevniky od podvodnich kliknuti. Sledujte miru okamziteho opusteni, cas na webu a vzorce zapojeni.</p>

<h2 id="prevention-strategies">Preventivni strategie</h2>
<ul>
<li><strong>Agresivni negativni klicova slova</strong> — Vylucte irelevantni dotazy</li>
<li><strong>Geograficka omezeni</strong> — Nastavte cileni na lokality na "Pouze pritomnost"</li>
<li><strong>Planovani reklam</strong> — Snizujte nabidky v casovych obdobich s vysokym podvodem</li>
<li><strong>Vylouceni siti</strong> — Deaktivujte Search Partners na kampaních Google Ads</li>
</ul>`,
    },
    platforms: ['google-ads', 'meta-ads', 'google-analytics', 'matomo'],
    relatedSlugs: ['multi-platform-campaigns', 'cross-platform-analytics', 'conversion-optimization'],
  },
];
