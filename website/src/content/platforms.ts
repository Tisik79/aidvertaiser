/* -------------------------------------------------------------------------- */
/*  Platform Data — Aidvertaiser Marketing Website                           */
/* -------------------------------------------------------------------------- */

export interface Platform {
  slug: string;
  icon: string;
  toolCount: number;
  title: Record<string, string>;
  shortDescription: Record<string, string>;
  metaDescription: Record<string, string>;
  content: Record<string, string>;
  features: string[];
  authMethod: string;
  configFile: string;
  relatedSlugs: string[];
}

/* Helper: for languages we haven't translated yet, fall back to English */
function ml(en: string, cs: string): Record<string, string> {
  return { en, cs, fr: en, es: en, zh: en, hi: en, pt: en, pl: en, ar: en, bn: en };
}

export const platforms: Platform[] = [
  /* ==================================================================== */
  /*  1. Google Ads                                                       */
  /* ==================================================================== */
  {
    slug: 'google-ads',
    icon: 'GoogleLogo',
    toolCount: 56,
    title: ml('Google Ads', 'Google Ads'),
    shortDescription: ml(
      'Full Google Ads management with 56 MCP tools covering campaigns, ad groups, ads, keywords, conversions, Performance Max, assets, and GAQL queries. Create, optimize, and analyze campaigns entirely through natural language.',
      'Kompletni sprava Google Ads s 56 MCP nastroji pokryvajicimi kampane, reklamni skupiny, reklamy, klicova slova, konverze, Performance Max, assety a GAQL dotazy. Vytvarejte, optimalizujte a analyzujte kampane pomoci prirozeneho jazyka.',
    ),
    metaDescription: ml(
      'Manage Google Ads with 56 AI-powered MCP tools. Campaigns, ad groups, keywords, conversions, Performance Max, and GAQL queries — all through natural language with Aidvertaiser.',
      'Spravujte Google Ads s 56 AI nastroji MCP. Kampane, reklamni skupiny, klicova slova, konverze, Performance Max a GAQL dotazy — vse pomoci prirozeneho jazyka s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Complete Google Ads Management</h2>
<p>Aidvertaiser provides <strong>56 dedicated tools</strong> for Google Ads, making it the most comprehensive MCP integration for Google's advertising platform. From campaign creation to advanced GAQL queries, every aspect of Google Ads management is accessible through natural language commands in your AI assistant.</p>
<p>Whether you are managing a single small-business account or orchestrating campaigns across dozens of client accounts, the Google Ads integration gives you programmatic control without writing a single line of code. Every tool returns structured data that your AI assistant can analyze, compare, and act upon.</p>

<h2 id="key-features">Key Features</h2>
<ul>
<li><strong>Campaign CRUD</strong> — Create, read, update, pause, enable, and remove campaigns across all campaign types including Search, Display, Shopping, Video, and Performance Max</li>
<li><strong>Ad Group management</strong> — Full lifecycle management of ad groups with bid adjustments, status control, and targeting configuration</li>
<li><strong>Responsive Search Ads</strong> — Create and manage RSAs with up to 15 headlines and 4 descriptions, with pinning support for controlled message delivery</li>
<li><strong>Keyword management</strong> — Add, update, and remove keywords across all match types (broad, phrase, exact) with 11 dedicated keyword tools</li>
<li><strong>Negative keywords</strong> — Campaign-level and ad-group-level negative keyword management to eliminate wasted spend</li>
<li><strong>Search terms report</strong> — Analyze actual search queries triggering your ads to discover new keyword opportunities and negative keyword candidates</li>
<li><strong>Conversion tracking</strong> — 9 conversion tools covering creation, listing, updates, offline upload, enhanced conversions, and conversion action management</li>
<li><strong>Asset management</strong> — Manage sitelinks, callouts, structured snippets, call assets, and image assets</li>
<li><strong>Performance Max</strong> — 16 tools for P-Max campaign management including asset groups, listing groups, brand guidelines, and audience signals</li>
<li><strong>GAQL queries</strong> — Execute arbitrary Google Ads Query Language queries for advanced reporting and data extraction</li>
<li><strong>Account management</strong> — Access customer information, billing status, and account-level settings</li>
</ul>

<h2 id="tool-categories">Tool Categories</h2>
<h3>Campaign Tools (8 tools)</h3>
<p>Create campaigns with full configuration including bidding strategy, budget, network settings, location targeting, and ad schedule. Update campaign status, budgets, and bidding parameters on the fly. List all campaigns with performance metrics or retrieve detailed information for specific campaigns.</p>

<h3>Ad Group Tools (6 tools)</h3>
<p>Manage ad groups within campaigns with control over default bids, status, ad rotation settings, and targeting refinements. Each ad group maintains its own keyword set and ad creatives for granular performance optimization.</p>

<h3>Ad Tools (5 tools)</h3>
<p>Create Responsive Search Ads with multiple headline and description combinations. Google's machine learning tests combinations to find the best-performing variants. Pin specific headlines or descriptions to fixed positions when message consistency is critical.</p>

<h3>Keyword Tools (11 tools)</h3>
<p>The most comprehensive keyword management available through MCP. Add keywords with match types and bids, update bids and status, remove underperformers, manage negative keywords at both campaign and ad group levels, and pull search terms reports to understand exactly what queries are triggering your ads.</p>

<h3>Conversion Tools (9 tools)</h3>
<p>Full conversion lifecycle management. Create conversion actions with configurable windows, attribution models, and value settings. Upload offline conversions using GCLIDs for closed-loop reporting. Enable enhanced conversions for improved measurement accuracy when cookies are blocked.</p>

<h3>Performance Max & Asset Tools (16 tools)</h3>
<p>Performance Max campaigns require asset groups instead of traditional ad groups. These tools let you create and manage asset groups, configure listing groups for Shopping feeds, set brand guidelines with logos and colors, and define audience signals to guide Google's AI targeting.</p>

<h3>Reporting (1 tool)</h3>
<p>The GAQL query tool is the most powerful reporting tool in the integration. Write arbitrary Google Ads Query Language queries to pull any metric, dimension, or segment combination available in the Google Ads API. This single tool replaces dozens of pre-built reports.</p>

<h2 id="authentication">Authentication</h2>
<p>Google Ads uses <strong>OAuth 2.0 browser-based authentication</strong>. On first use, Aidvertaiser opens a browser window for you to sign in with your Google account and grant access. The refresh token is stored locally and reused automatically for subsequent sessions.</p>
<p>You need a Google Ads developer token (available from your Google Ads Manager account) and OAuth client credentials. These are configured once and never need to be entered again.</p>

<h2 id="configuration">Configuration</h2>
<p>Create a configuration file at <code>~/google-ads.yaml</code>:</p>
<pre><code>developer_token: "YOUR_DEVELOPER_TOKEN"
client_id: "YOUR_OAUTH_CLIENT_ID"
client_secret: "YOUR_OAUTH_CLIENT_SECRET"
customer_id: "YOUR_CUSTOMER_ID"
login_customer_id: "YOUR_MCC_ID"  # Optional, for MCC accounts</code></pre>
<p>Alternatively, set the <code>GOOGLE_ADS_CREDENTIALS</code> environment variable pointing to the YAML file path.</p>`,
      cs: `<h2 id="overview">Kompletni sprava Google Ads</h2>
<p>Aidvertaiser poskytuje <strong>56 specializovanych nastroju</strong> pro Google Ads, coz z nej dela nejkomplexnejsi MCP integraci pro reklamni platformu Google. Od vytvareni kampani az po pokrocile GAQL dotazy je kazdy aspekt spravy Google Ads pristupny prostrednictvim prikazu v prirozenen jazyce ve vasem AI asistentovi.</p>
<p>At spravujete jediny ucet male firmy nebo orchestrujete kampane napric desitkami klientskych uctu, integrace Google Ads vam dava programovou kontrolu bez psani jedineho radku kodu. Kazdy nastroj vraci strukturovana data, ktera vas AI asistent muze analyzovat, porovnavat a podle nich jednat.</p>

<h2 id="key-features">Klicove funkce</h2>
<ul>
<li><strong>Sprava kampani</strong> — Vytvarejte, ctete, aktualizujte, pozastavujte a odstrante kampane vsech typu vcetne Search, Display, Shopping, Video a Performance Max</li>
<li><strong>Sprava reklamnich skupin</strong> — Kompletni sprava zivotniho cyklu reklamnich skupin s upravami nabidek, rizenim stavu a konfiguraci cileni</li>
<li><strong>Responzivni vyhledavaci reklamy</strong> — Vytvarejte a spravujte RSA s az 15 titulky a 4 popisy s podporou pripinani</li>
<li><strong>Sprava klicovych slov</strong> — Pridavejte, aktualizujte a odstrante klicova slova se vsemi typy shody (siroka, frazova, presna) s 11 dedicovanymi nastroji</li>
<li><strong>Negativni klicova slova</strong> — Sprava negativnich klicovych slov na urovni kampane i reklamni skupiny pro eliminaci zbytecnych vydaju</li>
<li><strong>Report vyhledavacich dotazu</strong> — Analyzujte skutecne vyhledavaci dotazy spoustejici vase reklamy</li>
<li><strong>Sledovani konverzi</strong> — 9 nastroju pro konverze pokryvajicich vytvareni, seznamy, aktualizace, offline nahrávani a vylepsene konverze</li>
<li><strong>Sprava assetu</strong> — Spravujte sitelinky, popisky, strukturovane udaje, assety pro volani a obrazkove assety</li>
<li><strong>Performance Max</strong> — 16 nastroju pro P-Max kampane vcetne skupin assetu, skupin polozek, pravidel znacky a signalu publika</li>
<li><strong>GAQL dotazy</strong> — Spoustejte libovolne GAQL dotazy pro pokrocily reporting a extrakci dat</li>
</ul>

<h2 id="tool-categories">Kategorie nastroju</h2>
<h3>Nastroje pro kampane (8 nastroju)</h3>
<p>Vytvarejte kampane s kompletni konfiguraci vcetne strategie nabidek, rozpoctu, nastaveni siti, cileni podle lokality a casoveho planu reklam.</p>

<h3>Nastroje pro reklamni skupiny (6 nastroju)</h3>
<p>Spravujte reklamni skupiny v kampanich s kontrolou nad vychozimi nabidkami, stavem, nastavenim rotace reklam a zpresovanim cileni.</p>

<h3>Nastroje pro reklamy (5 nastroju)</h3>
<p>Vytvarejte Responzivni vyhledavaci reklamy s vice kombinacemi titulku a popisku. Strojove uceni Google testuje kombinace pro nalezeni nejucinnejsich variant.</p>

<h3>Nastroje pro klicova slova (11 nastroju)</h3>
<p>Nejkomplexnejsi sprava klicovych slov dostupna prostrednictvim MCP. Pridavejte klicova slova s typy shody a nabidkami, aktualizujte nabidky a stavy, spravujte negativni klicova slova a stahujte reporty vyhledavacich dotazu.</p>

<h3>Nastroje pro konverze (9 nastroju)</h3>
<p>Kompletni sprava zivotniho cyklu konverzi. Vytvarejte konverzni akce s nastavitelnymi okny, atribucnimi modely a nastavenim hodnot. Nahravejte offline konverze pomoci GCLID.</p>

<h3>Performance Max a assety (16 nastroju)</h3>
<p>Kampane Performance Max vyzaduji skupiny assetu namisto tradicnich reklamnich skupin. Tyto nastroje vam umozni vytvareni a spravu skupin assetu, konfiguraci skupin polozek a definovani signalu publika.</p>

<h2 id="authentication">Autentizace</h2>
<p>Google Ads pouziva <strong>OAuth 2.0 autentizaci prostrednictvim prohlizece</strong>. Pri prvnim pouziti Aidvertaiser otevre okno prohlizece pro prihlaseni vasim uctem Google a udeleni pristupu.</p>

<h2 id="configuration">Konfigurace</h2>
<p>Vytvorte konfiguracni soubor <code>~/google-ads.yaml</code>:</p>
<pre><code>developer_token: "VAS_DEVELOPER_TOKEN"
client_id: "VASE_OAUTH_CLIENT_ID"
client_secret: "VAS_OAUTH_CLIENT_SECRET"
customer_id: "VASE_CUSTOMER_ID"
login_customer_id: "VASE_MCC_ID"  # Volitelne, pro MCC ucty</code></pre>`,
    },
    features: [
      'Campaign CRUD',
      'Ad Group management',
      'Responsive Search Ads',
      'Keyword management',
      'Negative keywords',
      'Search terms report',
      'Conversion tracking',
      'Offline conversion upload',
      'Enhanced conversions',
      'Asset management',
      'Performance Max',
      'GAQL queries',
    ],
    authMethod: 'OAuth 2.0 (browser)',
    configFile: '~/google-ads.yaml',
    relatedSlugs: ['meta-ads', 'google-analytics', 'search-console'],
  },

  /* ==================================================================== */
  /*  2. Meta Ads                                                         */
  /* ==================================================================== */
  {
    slug: 'meta-ads',
    icon: 'MetaLogo',
    toolCount: 38,
    title: ml('Meta Ads', 'Meta Ads'),
    shortDescription: ml(
      'Manage Facebook and Instagram advertising with 38 MCP tools. Full campaign lifecycle, audience targeting, pixel management, Conversions API, creative uploads, and performance reporting across Meta platforms.',
      'Spravujte reklamu na Facebooku a Instagramu s 38 MCP nastroji. Kompletni zivotni cyklus kampani, cileni na publika, sprava pixelu, Conversions API, nahravani kreativ a reporting vykonnosti na platformach Meta.',
    ),
    metaDescription: ml(
      'Control Meta Ads (Facebook & Instagram) with 38 AI-powered MCP tools. Campaign management, audience targeting, pixel tracking, Conversions API, and creative management through Aidvertaiser.',
      'Ovladejte Meta Ads (Facebook a Instagram) s 38 AI nastroji MCP. Sprava kampani, cileni na publika, sledovani pixelem, Conversions API a sprava kreativ pres Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Full-Stack Meta Advertising</h2>
<p>Aidvertaiser delivers <strong>38 specialized tools</strong> for the Meta Ads platform, covering Facebook and Instagram advertising from campaign creation to conversion attribution. The integration maps directly to the Meta Marketing API, giving you the same capabilities as the Meta Ads Manager but controlled through natural language.</p>
<p>Meta's advertising ecosystem is uniquely powerful for audience targeting. With over 3 billion monthly active users across Facebook, Instagram, Messenger, and the Audience Network, Meta offers unparalleled reach. Aidvertaiser makes this power accessible without navigating the complex Ads Manager interface.</p>

<h2 id="key-features">Key Features</h2>
<ul>
<li><strong>Campaign management</strong> — Create, update, pause, and archive campaigns with full objective configuration (awareness, traffic, engagement, leads, app promotion, sales)</li>
<li><strong>Ad set management</strong> — Configure budgets, schedules, bid strategies, placements, and optimization goals at the ad set level</li>
<li><strong>Creative management</strong> — Build ad creatives with images, videos, carousels, and collections with full copy configuration</li>
<li><strong>Image upload</strong> — Upload creative assets directly to your Meta ad account for use in ads</li>
<li><strong>Interest targeting</strong> — Search Meta's interest database to find targetable interests, behaviors, and demographics</li>
<li><strong>Behavioral targeting</strong> — Target users based on purchase behavior, device usage, travel patterns, and more</li>
<li><strong>Geo-location search</strong> — Find targetable geographic locations including cities, regions, countries, and custom radius targeting</li>
<li><strong>Audience estimation</strong> — Estimate reach and daily results for any targeting combination before spending a dollar</li>
<li><strong>Pixel management</strong> — Create and configure Meta Pixels for website event tracking with 5 dedicated pixel tools</li>
<li><strong>Conversions API</strong> — Send server-side events for reliable conversion tracking that works without cookies</li>
<li><strong>Custom conversions</strong> — Define custom conversion events based on URL rules or event parameters</li>
<li><strong>Offline conversions</strong> — Upload offline conversion data to attribute in-store purchases to online ad campaigns</li>
<li><strong>Performance insights</strong> — Pull campaign, ad set, and ad-level performance reports with flexible date ranges and breakdowns</li>
</ul>

<h2 id="tool-categories">Tool Categories</h2>
<h3>Campaign Tools (6 tools)</h3>
<p>Manage the top level of your Meta advertising hierarchy. Set campaign objectives (OUTCOME_AWARENESS, OUTCOME_TRAFFIC, OUTCOME_ENGAGEMENT, OUTCOME_LEADS, OUTCOME_APP_PROMOTION, OUTCOME_SALES), configure special ad categories for housing, credit, or employment, and control campaign-level spending limits.</p>

<h3>Ad Set Tools (6 tools)</h3>
<p>Ad sets are where you define who sees your ads, when they see them, and how much you spend. Configure detailed targeting including interests, behaviors, demographics, custom audiences, and lookalike audiences. Set daily or lifetime budgets, schedule start and end dates, and choose placements across Facebook, Instagram, Messenger, and the Audience Network.</p>

<h3>Creative & Ad Tools (8 tools)</h3>
<p>Build compelling ad experiences with single image, video, carousel, and collection formats. Upload images directly to your ad account. Configure primary text, headlines, descriptions, call-to-action buttons, and destination URLs. Preview ads across different placements before publishing.</p>

<h3>Audience Targeting Tools (5 tools)</h3>
<p>Meta's targeting capabilities are among the most sophisticated in digital advertising. Search interests by keyword to discover targetable audience segments. Explore behavioral targeting options. Search geographic locations for precise geo-targeting. Estimate audience size and potential reach for any targeting combination.</p>

<h3>Pixel & Tracking Tools (5 tools)</h3>
<p>The Meta Pixel and Conversions API form the foundation of Meta's measurement system. Create pixels, configure events, and send server-side conversion data. The Conversions API is especially critical in a post-cookie world where browser-based tracking is increasingly unreliable.</p>

<h3>Conversion Tools (9 tools)</h3>
<p>Go beyond basic pixel tracking with custom conversions, offline event uploads, and server-side event delivery. Define custom conversion rules based on URL patterns or event parameters. Upload CRM data to connect offline purchases with online ad interactions. Send real-time conversion events through the Conversions API for the most accurate attribution.</p>

<h2 id="authentication">Authentication</h2>
<p>Meta Ads uses <strong>OAuth 2.0 browser-based authentication</strong>. On first use, Aidvertaiser opens a browser window for you to log in with your Facebook account and authorize access to your ad accounts. The access token is refreshed automatically.</p>
<p>You need a Meta App with Marketing API access. Create one at <a href="https://developers.facebook.com">developers.facebook.com</a> and configure the app ID and secret.</p>

<h2 id="configuration">Configuration</h2>
<p>Set environment variables for Meta Ads access:</p>
<pre><code>export META_APP_ID="your_meta_app_id"
export META_APP_SECRET="your_meta_app_secret"
export META_AD_ACCOUNT_ID="act_your_account_id"</code></pre>
<p>The access token is managed automatically through the OAuth flow and stored securely for reuse across sessions.</p>`,
      cs: `<h2 id="overview">Kompletni Meta reklama</h2>
<p>Aidvertaiser poskytuje <strong>38 specializovanych nastroju</strong> pro platformu Meta Ads, pokryvajicich reklamu na Facebooku a Instagramu od vytvoreni kampane az po atribuci konverzi. Integrace se primo mapuje na Meta Marketing API a dava vam stejne moznosti jako Meta Ads Manager, ale ovladane prostrednictvim prirozeneho jazyka.</p>
<p>Reklamni ekosystem Meta je unikatne silny pro cileni na publika. S vice nez 3 miliardami mesicne aktivnich uzivatelu na Facebooku, Instagramu, Messengeru a Audience Network nabizi Meta nesrovnatelny dosah.</p>

<h2 id="key-features">Klicove funkce</h2>
<ul>
<li><strong>Sprava kampani</strong> — Vytvarejte, aktualizujte, pozastavujte a archivujte kampane s kompletni konfiguraci cilu</li>
<li><strong>Sprava sad reklam</strong> — Konfigurujte rozpocty, casove plany, strategie nabidek, umisteni a cile optimalizace</li>
<li><strong>Sprava kreativ</strong> — Vytvarejte reklamni kreativy s obrazky, videi, karusely a kolekcemi</li>
<li><strong>Cileni na zajmy</strong> — Prohledavejte databazi zajmu Meta pro nalezeni cilitelnych segmentu publika</li>
<li><strong>Behavioralni cileni</strong> — Cilte na uzivatele podle nakupniho chovani, pouzivani zarizeni a cestovnich vzorcu</li>
<li><strong>Odhad publika</strong> — Odhadnete dosah a denni vysledky pro jakoukoli kombinaci cileni pred utracenim koruny</li>
<li><strong>Sprava pixelu</strong> — Vytvarejte a konfigurujte Meta pixely pro sledovani udalosti na webu</li>
<li><strong>Conversions API</strong> — Odesilejte serverove udalosti pro spolehlivejsi sledovani konverzi bez zavislosti na cookies</li>
<li><strong>Offline konverze</strong> — Nahravejte offline konverzni data pro propojeni obchodnich nakupu s online reklamami</li>
</ul>

<h2 id="tool-categories">Kategorie nastroju</h2>
<h3>Nastroje pro kampane (6 nastroju)</h3>
<p>Spravujte nejvyssi uroven hierarchie Meta reklamy. Nastavte cile kampani, konfigurujte specialni kategorie reklam a kontrolujte limity utraceni.</p>

<h3>Nastroje pro sady reklam (6 nastroju)</h3>
<p>Sady reklam definuji, kdo vidi vase reklamy, kdy je vidi a kolik utracite. Konfigurujte detailni cileni vcetne zajmu, chovani a demografickych udaju.</p>

<h3>Nastroje pro kreativy a reklamy (8 nastroju)</h3>
<p>Vytvarejte poutave reklamni zkusenosti s formaty jednoho obrazku, videa, karuselu a kolekce. Nahravejte obrazky primo do vaseho reklamniho uctu.</p>

<h3>Nastroje pro cileni na publika (5 nastroju)</h3>
<p>Schopnosti cileni Meta patri k nejsofistikovanejsim v digitalni reklame. Prohledavejte zajmy, prozkoumavejte behavioralni moznosti a odhadujte velikost publika.</p>

<h3>Nastroje pro pixel a sledovani (5 nastroju)</h3>
<p>Meta Pixel a Conversions API tvori zaklad mericiho systemu Meta. Vytvarejte pixely, konfigurujte udalosti a odesilejte serverova konverzni data.</p>

<h2 id="authentication">Autentizace</h2>
<p>Meta Ads pouziva <strong>OAuth 2.0 autentizaci prostrednictvim prohlizece</strong>. Pri prvnim pouziti se otevre okno prohlizece pro prihlaseni uctem Facebook a autorizaci pristupu k vasim reklamnim uctum.</p>

<h2 id="configuration">Konfigurace</h2>
<p>Nastavte promenne prostredi:</p>
<pre><code>export META_APP_ID="vase_meta_app_id"
export META_APP_SECRET="vas_meta_app_secret"
export META_AD_ACCOUNT_ID="act_vase_account_id"</code></pre>`,
    },
    features: [
      'Campaign management',
      'Ad set management',
      'Creative management',
      'Image upload',
      'Interest targeting',
      'Behavioral targeting',
      'Geo-location search',
      'Audience estimation',
      'Pixel management',
      'Conversions API',
      'Custom conversions',
      'Offline conversions',
      'Performance insights',
    ],
    authMethod: 'OAuth 2.0 (browser)',
    configFile: 'Environment variables',
    relatedSlugs: ['google-ads', 'google-analytics', 'matomo'],
  },

  /* ==================================================================== */
  /*  3. Google Analytics                                                 */
  /* ==================================================================== */
  {
    slug: 'google-analytics',
    icon: 'ChartLine',
    toolCount: 21,
    title: ml('Google Analytics 4', 'Google Analytics 4'),
    shortDescription: ml(
      'Access Google Analytics 4 with 21 MCP tools for property management, data streams, reporting, real-time analytics, and key event tracking. Query your analytics data through natural language instead of navigating the GA4 interface.',
      'Pristupujte ke Google Analytics 4 s 21 MCP nastroji pro spravu properties, datovych proudu, reporting, real-time analytiku a sledovani klicovych udalosti. Dotazujte se na analyticka data prirozonym jazykem.',
    ),
    metaDescription: ml(
      'Query Google Analytics 4 with 21 MCP tools. Property management, data streams, real-time reports, and key event tracking through AI-powered natural language with Aidvertaiser.',
      'Dotazujte se na Google Analytics 4 s 21 MCP nastroji. Sprava properties, datove proudy, real-time reporty a sledovani klicovych udalosti pres AI s Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">GA4 at Your Fingertips</h2>
<p>Aidvertaiser provides <strong>21 tools</strong> for Google Analytics 4, covering the full range of GA4 administration and reporting capabilities. Instead of navigating the GA4 interface and building reports manually, you can ask your AI assistant to pull any metric, manage properties, configure data streams, and track key events — all through conversation.</p>
<p>The integration uses both the GA4 Admin API and the GA4 Data API, giving you administrative control and reporting power in a single unified interface. Manage accounts and properties, set up web, iOS, and Android data streams, run standard and real-time reports, and configure key events for conversion tracking.</p>

<h2 id="key-features">Key Features</h2>
<ul>
<li><strong>Property management</strong> — List, create, and configure GA4 properties with full settings control</li>
<li><strong>Data stream management</strong> — Create and manage web, iOS, and Android data streams with 8 dedicated tools</li>
<li><strong>Tracking code retrieval</strong> — Get the measurement ID and installation snippet for any web data stream</li>
<li><strong>Standard reports</strong> — Pull reports with any combination of dimensions, metrics, date ranges, and filters</li>
<li><strong>Real-time reports</strong> — Monitor live website activity with real-time dimension and metric queries</li>
<li><strong>Metadata discovery</strong> — Explore available dimensions and metrics programmatically to build precise reports</li>
<li><strong>Key event management</strong> — Create, list, update, and delete key events (formerly conversion events) with 4 dedicated tools</li>
</ul>

<h2 id="tool-categories">Tool Categories</h2>
<h3>Account & Property Tools (5 tools)</h3>
<p>Manage GA4 at the organizational level. List all accounts you have access to, enumerate properties within accounts, and retrieve detailed property configuration including industry category, time zone, and currency settings.</p>

<h3>Data Stream Tools (8 tools)</h3>
<p>Data streams are how GA4 collects data from your websites and apps. Create web streams with measurement IDs, iOS streams with bundle IDs, and Android streams with package names. List all streams for a property, retrieve stream details, and get the tracking code snippet for easy installation.</p>

<h3>Reporting Tools (3 tools)</h3>
<p>The reporting tools give you access to the full power of the GA4 Data API. Run standard reports with any combination of dimensions (page path, source/medium, country, device category) and metrics (sessions, users, pageviews, conversions, revenue). Pull real-time reports to see what is happening on your site right now. Discover available dimensions and metrics through the metadata endpoint.</p>

<h3>Key Event Tools (4 tools)</h3>
<p>Key events (formerly called conversions) are the actions that matter most to your business. Create key events from existing GA4 events, list all key events for a property, update key event configuration, and delete key events when they are no longer needed. Key events flow into Google Ads for conversion-based bidding optimization.</p>

<h2 id="authentication">Authentication</h2>
<p>Google Analytics uses <strong>OAuth 2.0 browser-based authentication</strong> with the same flow as Google Ads. On first use, a browser window opens for authorization. The scopes requested are <code>analytics.edit</code> for administration and <code>analytics.readonly</code> for reporting.</p>

<h2 id="configuration">Configuration</h2>
<p>Create a configuration file at <code>~/google-analytics.yaml</code>:</p>
<pre><code>client_id: "YOUR_OAUTH_CLIENT_ID"
client_secret: "YOUR_OAUTH_CLIENT_SECRET"
property_id: "YOUR_GA4_PROPERTY_ID"  # e.g., "properties/123456789"</code></pre>
<p>The same OAuth client credentials used for Google Ads can be reused for GA4 — just ensure the Analytics scopes are enabled in your Google Cloud project.</p>`,
      cs: `<h2 id="overview">GA4 na dosah ruky</h2>
<p>Aidvertaiser poskytuje <strong>21 nastroju</strong> pro Google Analytics 4, pokryvajicich celou skalu administrativnich a reportovacich schopnosti GA4. Misto navigace v rozhrani GA4 a manualniho tvoreni reportu se muzete sveho AI asistenta jednodusse zeptat na jakoukoli metriku, spravu properties, konfiguraci datovych proudu a sledovani klicovych udalosti.</p>

<h2 id="key-features">Klicove funkce</h2>
<ul>
<li><strong>Sprava properties</strong> — Vypisujte, vytvarejte a konfigurujte GA4 properties</li>
<li><strong>Sprava datovych proudu</strong> — Vytvarejte a spravujte webove, iOS a Android datove proudy s 8 nastroji</li>
<li><strong>Ziskani sledovaciho kodu</strong> — Ziskejte measurement ID a instalacni snippet pro jakykoliv webovy datovy proud</li>
<li><strong>Standardni reporty</strong> — Stahujte reporty s libovolnou kombinaci dimenzi, metrik, casovych rozsahu a filtru</li>
<li><strong>Real-time reporty</strong> — Sledujte zivou aktivitu na webu v realnem case</li>
<li><strong>Sprava klicovych udalosti</strong> — Vytvarejte, vypisujte, aktualizujte a mazejte klicove udalosti se 4 nastroji</li>
</ul>

<h2 id="tool-categories">Kategorie nastroju</h2>
<h3>Nastroje pro ucty a properties (5 nastroju)</h3>
<p>Spravujte GA4 na organizacni urovni. Vypisujte vsechny ucty, ke kterym mate pristup, a ziskavejte podrobnou konfiguraci properties.</p>

<h3>Nastroje pro datove proudy (8 nastroju)</h3>
<p>Datove proudy jsou zpusobem, jakym GA4 sbira data z vasich webovych stranek a aplikaci. Vytvarejte webove proudy s measurement ID, iOS proudy s bundle ID a Android proudy s nazvy balicku.</p>

<h3>Nastroje pro reporting (3 nastroje)</h3>
<p>Reportovaci nastroje vam daji pristup k plnemu vykonu GA4 Data API. Spoustejte standardni reporty s libovolnou kombinaci dimenzi a metrik. Stahujte real-time reporty a objevujte dostupne dimenze a metriky.</p>

<h3>Nastroje pro klicove udalosti (4 nastroje)</h3>
<p>Klicove udalosti (drive nazyvane konverze) jsou akce, ktere jsou pro vas podnik nejdulezitejsi. Vytvarejte je z existujicich GA4 udalosti a spravujte jejich konfiguraci.</p>

<h2 id="authentication">Autentizace</h2>
<p>Google Analytics pouziva <strong>OAuth 2.0 autentizaci prostrednictvim prohlizece</strong>. Scopes: <code>analytics.edit</code> pro administraci a <code>analytics.readonly</code> pro reporting.</p>

<h2 id="configuration">Konfigurace</h2>
<pre><code>client_id: "VASE_OAUTH_CLIENT_ID"
client_secret: "VAS_OAUTH_CLIENT_SECRET"
property_id: "VASE_GA4_PROPERTY_ID"</code></pre>`,
    },
    features: [
      'Property management',
      'Data stream management',
      'Web/iOS/Android streams',
      'Tracking code retrieval',
      'Standard reports',
      'Real-time reports',
      'Metadata discovery',
      'Key event management',
    ],
    authMethod: 'OAuth 2.0 (browser)',
    configFile: '~/google-analytics.yaml',
    relatedSlugs: ['google-ads', 'search-console', 'matomo'],
  },

  /* ==================================================================== */
  /*  4. Search Console                                                   */
  /* ==================================================================== */
  {
    slug: 'search-console',
    icon: 'MagnifyingGlass',
    toolCount: 15,
    title: ml('Google Search Console', 'Google Search Console'),
    shortDescription: ml(
      'Monitor and improve your search presence with 15 MCP tools for Google Search Console. Manage sites, analyze search performance, inspect URLs, submit sitemaps, and verify site ownership — all through AI conversation.',
      'Sledujte a zlepsujte svou pritomnost ve vyhledavani s 15 MCP nastroji pro Google Search Console. Spravujte weby, analyzujte vykon ve vyhledavani, kontrolujte URL, odesilajte sitemapy a overujte vlastnictvi webu.',
    ),
    metaDescription: ml(
      'Monitor search performance with 15 MCP tools for Google Search Console. Search analytics, URL inspection, sitemap management, and site verification through Aidvertaiser.',
      'Sledujte vykon ve vyhledavani s 15 MCP nastroji pro Google Search Console. Analyza vyhledavani, inspekce URL, sprava sitemap a overeni webu pres Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Search Intelligence Through AI</h2>
<p>Aidvertaiser brings <strong>15 tools</strong> for Google Search Console, giving you programmatic access to your website's search performance data. Understand how Google sees your site, which queries drive traffic, how your pages are indexed, and where technical issues might be hurting your visibility.</p>
<p>Search Console is essential for any website that depends on organic search traffic. The data it provides — impressions, clicks, click-through rates, and average positions — is available nowhere else. With Aidvertaiser, you can query this data conversationally and combine it with insights from your advertising platforms for a complete picture of your search presence.</p>

<h2 id="key-features">Key Features</h2>
<ul>
<li><strong>Site management</strong> — Add, list, and remove sites from your Search Console account with 5 management tools</li>
<li><strong>Search analytics</strong> — Query search performance data by queries, pages, countries, devices, and date ranges with 3 analytics tools</li>
<li><strong>Query analysis</strong> — See which search queries bring users to your site, with impressions, clicks, CTR, and average position</li>
<li><strong>Page analysis</strong> — Understand which pages perform best in search results and identify underperforming content</li>
<li><strong>URL inspection</strong> — Check how Google has indexed a specific URL, including last crawl date, indexing status, and any detected issues</li>
<li><strong>Sitemap management</strong> — Submit, list, delete, and check the status of XML sitemaps with 4 sitemap tools</li>
<li><strong>Site verification</strong> — Manage site verification methods and retrieve verification tokens with 3 verification tools</li>
</ul>

<h2 id="tool-categories">Tool Categories</h2>
<h3>Site Management Tools (5 tools)</h3>
<p>Manage which sites are tracked in your Search Console account. Add new sites (both domain properties and URL-prefix properties), list all verified sites, retrieve detailed site information, and remove sites when they are no longer needed.</p>

<h3>Search Analytics Tools (3 tools)</h3>
<p>The search analytics tools are the most powerful in the Search Console integration. Query performance data with flexible filtering by query text, page URL, country, device type, and search appearance. Group results by any dimension combination. Specify date ranges for trend analysis. The data includes impressions, clicks, click-through rate, and average position for every result row.</p>

<h3>URL Inspection Tool (1 tool)</h3>
<p>Inspect any URL on your verified sites to see how Google has processed it. The inspection results include whether the URL is in the Google index, the last crawl date, the canonical URL Google selected, any mobile usability issues, and rich result eligibility.</p>

<h3>Sitemap Tools (4 tools)</h3>
<p>Sitemaps tell Google which pages on your site should be crawled and indexed. Submit new sitemaps, list all submitted sitemaps with their processing status, check individual sitemap status for errors and warnings, and delete sitemaps that are no longer relevant.</p>

<h3>Verification Tools (3 tools)</h3>
<p>Before you can access Search Console data for a site, you need to verify ownership. These tools help manage the verification process by listing available verification methods, retrieving verification tokens (HTML file, meta tag, DNS record), and checking verification status.</p>

<h2 id="authentication">Authentication</h2>
<p>Search Console uses <strong>OAuth 2.0 browser-based authentication</strong>. The scope required is <code>webmasters.readonly</code> for read access or <code>webmasters</code> for full read-write access. The same OAuth client credentials used for Google Ads and GA4 work here.</p>

<h2 id="configuration">Configuration</h2>
<p>Search Console shares the OAuth configuration with other Google services. No additional configuration file is needed if you already have Google Ads or GA4 configured. The site URL is specified per tool call.</p>`,
      cs: `<h2 id="overview">Vyhledavaci inteligence prostrednictvim AI</h2>
<p>Aidvertaiser prinasi <strong>15 nastroju</strong> pro Google Search Console a dava vam programovy pristup k datum o vykonnosti vaseho webu ve vyhledavani. Pochopte, jak Google vidi vas web, ktere dotazy prinaseji navstevnost a kde technicke problemy mohou skodit vasi viditelnosti.</p>

<h2 id="key-features">Klicove funkce</h2>
<ul>
<li><strong>Sprava webu</strong> — Pridavejte, vypisujte a odstrante weby z vaseho uctu Search Console</li>
<li><strong>Analyza vyhledavani</strong> — Dotazujte se na data o vykonnosti podle dotazu, stranek, zemi, zarizeni a casovych rozsahu</li>
<li><strong>Inspekce URL</strong> — Zjistete, jak Google zaindexoval konkretni URL</li>
<li><strong>Sprava sitemap</strong> — Odesilajte, vypisujte, mazejte a kontrolujte stav XML sitemap</li>
<li><strong>Overeni webu</strong> — Spravujte metody overeni vlastnictvi a ziskavejte overovaci tokeny</li>
</ul>

<h2 id="tool-categories">Kategorie nastroju</h2>
<h3>Nastroje pro spravu webu (5 nastroju)</h3>
<p>Spravujte, ktere weby jsou sledovany ve vasem uctu Search Console. Pridavejte nove weby, vypisujte vsechny overene weby a odstrante weby, ktere uz nepotrebujete.</p>

<h3>Nastroje pro analyzu vyhledavani (3 nastroje)</h3>
<p>Dotazujte se na data o vykonnosti s flexibilnim filtrovanim podle textu dotazu, URL stranky, zeme, typu zarizeni a typu vyhledavani.</p>

<h3>Nastroj pro inspekci URL (1 nastroj)</h3>
<p>Zkontrolujte jakoukoli URL na vasich overenych webech a zjistete, jak ji Google zpracoval, vcetne stavu indexace a posledniho pruchodu.</p>

<h3>Nastroje pro sitemapy (4 nastroje)</h3>
<p>Odesilajte nove sitemapy, vypisujte vsechny odeslane sitemapy s jejich stavem zpracovani a mazejte nepotrebne sitemapy.</p>

<h2 id="authentication">Autentizace</h2>
<p>Search Console pouziva <strong>OAuth 2.0</strong>. Sdili OAuth konfiguraci s ostatnimi sluzbami Google.</p>`,
    },
    features: [
      'Site management',
      'Search analytics',
      'Query analysis',
      'Page analysis',
      'URL inspection',
      'Sitemap management',
      'Site verification',
      'Verification tokens',
    ],
    authMethod: 'OAuth 2.0 (browser)',
    configFile: 'Shared Google OAuth',
    relatedSlugs: ['google-analytics', 'bing-webmaster', 'google-ads'],
  },

  /* ==================================================================== */
  /*  5. Matomo                                                           */
  /* ==================================================================== */
  {
    slug: 'matomo',
    icon: 'ChartBar',
    toolCount: 27,
    title: ml('Matomo Analytics', 'Matomo Analytics'),
    shortDescription: ml(
      'Privacy-first analytics with 27 MCP tools for Matomo. Site management, core reporting, real-time monitoring, visitor profiles, and goal tracking — all with full data ownership and GDPR compliance.',
      'Analytika s durazem na soukromi s 27 MCP nastroji pro Matomo. Sprava webu, zakladni reporting, real-time monitoring, profily navstevniku a sledovani cilu — vse s plnym vlastnictvim dat a souladu s GDPR.',
    ),
    metaDescription: ml(
      'Privacy-first analytics with 27 MCP tools for Matomo. Site management, reporting, real-time monitoring, visitor profiles, and goal tracking through Aidvertaiser.',
      'Analytika s durazem na soukromi s 27 MCP nastroji pro Matomo. Sprava webu, reporting, real-time monitoring, profily navstevniku a sledovani cilu pres Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Privacy-First Analytics, AI-Powered</h2>
<p>Aidvertaiser integrates with <strong>Matomo</strong> through <strong>27 dedicated tools</strong>, providing comprehensive analytics without sending your data to third parties. Matomo is the leading open-source analytics platform, used by over 1 million websites worldwide. With Aidvertaiser, you get the same depth of analytics insight as GA4 while maintaining 100% data ownership.</p>
<p>Matomo can run on your own servers or as a cloud service, giving you complete control over where your analytics data is stored. This makes it the preferred choice for organizations that need GDPR compliance, government agencies, healthcare providers, and privacy-conscious businesses.</p>

<h2 id="key-features">Key Features</h2>
<ul>
<li><strong>Site management</strong> — Add, list, update, and delete tracked websites with 5 site management tools</li>
<li><strong>Tracking code</strong> — Retrieve the JavaScript tracking snippet for any managed site</li>
<li><strong>Visit summaries</strong> — Get aggregated visit data including visits, unique visitors, pageviews, bounce rate, and visit duration</li>
<li><strong>Page analytics</strong> — Analyze page URLs and page titles with traffic, time on page, and exit rate metrics</li>
<li><strong>Entry/exit pages</strong> — Identify which pages users land on and which pages they leave from</li>
<li><strong>Referrer analysis</strong> — Understand where your traffic comes from — search engines, social media, direct, campaigns, and referring websites</li>
<li><strong>Search keywords</strong> — See which search keywords bring visitors to your site from organic search</li>
<li><strong>Country/device reports</strong> — Break down visitors by country, browser, operating system, and device type</li>
<li><strong>Live counters</strong> — Real-time visitor counts and activity monitoring</li>
<li><strong>Recent visitors</strong> — View the most recent visitor sessions with full action details</li>
<li><strong>Visitor profiles</strong> — Deep-dive into individual visitor histories across multiple sessions</li>
<li><strong>Goal management</strong> — Create, list, update, and delete conversion goals</li>
<li><strong>Goal conversion reports</strong> — Track goal completion rates, conversion values, and goal attribution</li>
</ul>

<h2 id="tool-categories">Tool Categories</h2>
<h3>Site Management Tools (5 tools)</h3>
<p>Manage the websites tracked by your Matomo instance. Add new sites with their URLs, time zones, and currencies. List all tracked sites. Update site settings. Delete sites that are no longer needed. Retrieve the JavaScript tracking code for easy installation on any website.</p>

<h3>Core Reporting Tools (9 tools)</h3>
<p>The reporting tools cover the most important analytics dimensions. Visit summaries give you the big picture — total visits, unique visitors, pageviews, bounce rate, and average visit duration. Page analytics break down traffic by URL and page title. Entry and exit page reports show where users start and end their sessions. Referrer reports reveal traffic sources. Device and country reports help you understand your audience demographics.</p>

<h3>Real-Time Monitoring Tools (3 tools)</h3>
<p>Monitor your website in real time. Live counters show how many visitors are currently on your site. Recent visitor logs display the last visitor sessions with full action trails — every page viewed, every event triggered, every goal converted. Visitor profiles aggregate a single user's history across multiple visits for a complete behavioral picture.</p>

<h3>Goal & Conversion Tools (5 tools)</h3>
<p>Goals are the conversion actions that drive your business. Create goals based on URL visits, event triggers, download counts, or manual triggers. Track goal completion rates, conversion values, and which traffic sources drive the most conversions. Update or delete goals as your business objectives evolve.</p>

<h2 id="authentication">Authentication</h2>
<p>Matomo uses <strong>API token authentication</strong>. Generate a token in your Matomo instance under Settings > Personal > Security > Auth tokens. The token is passed with every API request and grants access based on the user's permissions in Matomo.</p>

<h2 id="configuration">Configuration</h2>
<p>Create a configuration file at <code>~/matomo.yaml</code>:</p>
<pre><code>matomo_url: "https://your-matomo-instance.com"
token_auth: "YOUR_MATOMO_API_TOKEN"
site_id: 1  # Default site ID (can be overridden per tool call)</code></pre>
<p>The Matomo URL should point to the root of your Matomo installation. The API is accessed at <code>{matomo_url}/?module=API</code> automatically.</p>`,
      cs: `<h2 id="overview">Analytika s durazem na soukromi, pohanena AI</h2>
<p>Aidvertaiser se integruje s <strong>Matomo</strong> prostrednictvim <strong>27 specializovanych nastroju</strong> a poskytuje komplexni analytiku bez odesilani vasich dat tretim stranam. Matomo je predni open-source analyticka platforma pouzivana vice nez 1 milionem webu po celem svete. S Aidvertaiser ziskate stejnou hloubku analytickych poznatku jako s GA4 pri zachovani 100% vlastnictvi dat.</p>

<h2 id="key-features">Klicove funkce</h2>
<ul>
<li><strong>Sprava webu</strong> — Pridavejte, vypisujte, aktualizujte a mazejte sledovane weby</li>
<li><strong>Sledovaci kod</strong> — Ziskejte JavaScript sledovaci snippet pro jakykoliv spravovany web</li>
<li><strong>Souhrny navstev</strong> — Ziskejte agregovana data o navstevach vcetne navstev, unikatnich navstevniku a miry okamziteho opusteni</li>
<li><strong>Analyza stranek</strong> — Analyzujte URL stranek a titulky s metrikami provozu</li>
<li><strong>Analyza zdroju</strong> — Pochopte, odkud prichazi vase navstevnost</li>
<li><strong>Real-time monitoring</strong> — Sledujte navstevniky v realnem case</li>
<li><strong>Profily navstevniku</strong> — Detailni nahledy do historii jednotlivych navstevniku</li>
<li><strong>Sprava cilu</strong> — Vytvarejte, vypisujte, aktualizujte a mazejte konverzni cile</li>
</ul>

<h2 id="tool-categories">Kategorie nastroju</h2>
<h3>Nastroje pro spravu webu (5 nastroju)</h3>
<p>Spravujte weby sledovane vasi instanci Matomo. Pridavejte nove weby s jejich URL, casovymi zonami a menami.</p>

<h3>Nastroje pro zakladni reporting (9 nastroju)</h3>
<p>Reportovaci nastroje pokryvaji nejdulezitejsi analyticke dimenze. Souhrny navstev, analyza stranek, vstupni a vystupni stranky, zdroje navstevnosti a demograficke reporty.</p>

<h3>Nastroje pro real-time monitoring (3 nastroje)</h3>
<p>Sledujte svuj web v realnem case. Pocitadla ukazuji aktualni pocet navstevniku. Zaznamy navstevniku zobrazuji posledni relace se vsemi akcemi.</p>

<h3>Nastroje pro cile a konverze (5 nastroju)</h3>
<p>Cile jsou konverzni akce, ktere pohaneji vas byznys. Vytvarejte cile na zaklade navstev URL, spousteni udalosti nebo rucnich triggeru.</p>

<h2 id="authentication">Autentizace</h2>
<p>Matomo pouziva <strong>autentizaci API tokenem</strong>. Token vygenerujte v Matomo pod Nastaveni > Osobni > Bezpecnost.</p>

<h2 id="configuration">Konfigurace</h2>
<pre><code>matomo_url: "https://vase-matomo-instance.com"
token_auth: "VAS_MATOMO_API_TOKEN"
site_id: 1</code></pre>`,
    },
    features: [
      'Site management',
      'Tracking code',
      'Visit summaries',
      'Page analytics',
      'Entry/exit pages',
      'Referrer analysis',
      'Search keywords',
      'Country/device reports',
      'Live counters',
      'Recent visitors',
      'Visitor profiles',
      'Goal management',
      'Goal conversion reports',
    ],
    authMethod: 'API token',
    configFile: '~/matomo.yaml',
    relatedSlugs: ['google-analytics', 'search-console', 'bing-webmaster'],
  },

  /* ==================================================================== */
  /*  6. Bing Webmaster                                                   */
  /* ==================================================================== */
  {
    slug: 'bing-webmaster',
    icon: 'Globe',
    toolCount: 21,
    title: ml('Bing Webmaster Tools', 'Bing Webmaster Tools'),
    shortDescription: ml(
      'Optimize for Bing search with 21 MCP tools covering site management, URL submission, sitemaps, search analytics, crawl management, keyword research, and link analysis. Essential for reaching the 1 billion+ Bing users.',
      'Optimalizujte pro vyhledavani Bing s 21 MCP nastroji pokryvajicimi spravu webu, odeslani URL, sitemapy, analyzu vyhledavani, spravu prochazeni, vyzkum klicovych slov a analyzu odkazu.',
    ),
    metaDescription: ml(
      'Optimize for Bing with 21 MCP tools. URL submission, sitemaps, search analytics, crawl management, keyword research, and link analysis through Aidvertaiser.',
      'Optimalizujte pro Bing s 21 MCP nastroji. Odeslani URL, sitemapy, analyza vyhledavani, sprava prochazeni, vyzkum klicovych slov a analyza odkazu pres Aidvertaiser.',
    ),
    content: {
      en: `<h2 id="overview">Bing Search Optimization</h2>
<p>Aidvertaiser provides <strong>21 tools</strong> for Bing Webmaster Tools, giving you complete control over how your website appears in Bing search results. Bing powers search across Microsoft Edge, Windows, Cortana, and Yahoo — reaching over 1 billion users worldwide. Ignoring Bing means leaving traffic on the table.</p>
<p>The Bing Webmaster integration covers everything from basic site management to advanced keyword research and link analysis. Unlike Google Search Console, Bing Webmaster Tools also provides keyword research data and inbound link information, making it a dual-purpose SEO and research tool.</p>

<h2 id="key-features">Key Features</h2>
<ul>
<li><strong>Site management</strong> — Add, list, retrieve details, and remove sites from your Bing Webmaster account with 4 management tools</li>
<li><strong>URL submission</strong> — Submit individual URLs for immediate crawling, batch-submit up to 500 URLs at once, and track submission quotas with 3 submission tools</li>
<li><strong>Submission quota tracking</strong> — Monitor your daily and monthly URL submission limits</li>
<li><strong>Sitemap management</strong> — Submit, list, and delete XML sitemaps with 3 sitemap tools</li>
<li><strong>Search statistics</strong> — Analyze search performance with impressions, clicks, CTR, and position data across 3 analytics tools</li>
<li><strong>Per-query metrics</strong> — See which search queries drive traffic from Bing</li>
<li><strong>Per-page metrics</strong> — Understand which pages perform best in Bing search results</li>
<li><strong>Crawl statistics</strong> — Monitor how Bingbot crawls your site, including crawl frequency and response codes</li>
<li><strong>Crawl issue detection</strong> — Identify crawl errors, blocked resources, and technical issues affecting indexing</li>
<li><strong>Crawl rate configuration</strong> — Control how aggressively Bingbot crawls your site</li>
<li><strong>Keyword research</strong> — Discover new keyword opportunities based on your site content and search trends</li>
<li><strong>Related keywords</strong> — Find semantically related keywords to expand your content strategy</li>
<li><strong>Inbound link analysis</strong> — See which external sites link to yours and analyze your backlink profile</li>
</ul>

<h2 id="tool-categories">Tool Categories</h2>
<h3>Site Management Tools (4 tools)</h3>
<p>Manage your Bing Webmaster account. Add new sites for tracking, list all registered sites, retrieve detailed site information including verification status, and remove sites you no longer need to monitor.</p>

<h3>URL Submission Tools (3 tools)</h3>
<p>Get your content indexed faster. Submit individual URLs for priority crawling when you publish new content or update existing pages. Batch-submit up to 500 URLs at once for large-scale content updates or site migrations. Track your submission quota to ensure you stay within Bing's daily and monthly limits.</p>

<h3>Sitemap Tools (3 tools)</h3>
<p>Sitemaps are essential for large sites. Submit XML sitemaps to tell Bing about all your indexable pages. List submitted sitemaps with their processing status and error counts. Delete outdated sitemaps when your site structure changes.</p>

<h3>Search Analytics Tools (3 tools)</h3>
<p>Understand your Bing search performance. Pull overall search statistics for your site. Drill down into per-query metrics to see which search terms drive impressions and clicks. Analyze per-page metrics to identify your best and worst performing content in Bing results.</p>

<h3>Crawl Management Tools (4 tools)</h3>
<p>Control and monitor how Bingbot interacts with your site. View crawl statistics to understand crawl frequency, response times, and HTTP status codes. Detect crawl issues that might prevent your pages from being indexed. Configure the crawl rate to balance between fast indexing and server load.</p>

<h3>Keyword Research Tools (2 tools)</h3>
<p>Bing Webmaster Tools includes built-in keyword research — a feature not available in Google Search Console. Discover new keyword opportunities based on your site content. Find related keywords to expand your targeting strategy and identify content gaps.</p>

<h3>Link Analysis Tools (2 tools)</h3>
<p>Analyze your site's inbound link profile. See which external websites link to yours, the anchor text they use, and the pages they link to. This data is invaluable for link building strategy and competitive analysis.</p>

<h2 id="authentication">Authentication</h2>
<p>Bing Webmaster Tools uses <strong>API key authentication</strong>. Generate an API key in your Bing Webmaster Tools account under Settings > API Access. The key is passed with every API request.</p>

<h2 id="configuration">Configuration</h2>
<p>Create a configuration file at <code>~/bing-webmaster.yaml</code>:</p>
<pre><code>api_key: "YOUR_BING_WEBMASTER_API_KEY"
site_url: "https://your-website.com"  # Default site URL</code></pre>
<p>The API key provides access to all sites registered under your Bing Webmaster account. The site URL can be overridden per tool call for multi-site management.</p>`,
      cs: `<h2 id="overview">Optimalizace pro Bing vyhledavani</h2>
<p>Aidvertaiser poskytuje <strong>21 nastroju</strong> pro Bing Webmaster Tools a dava vam kompletni kontrolu nad tim, jak se vas web zobrazuje ve vysledcich vyhledavani Bing. Bing pohani vyhledavani v Microsoft Edge, Windows, Cortane a Yahoo — oslovuje pres 1 miliardu uzivatelu po celem svete.</p>

<h2 id="key-features">Klicove funkce</h2>
<ul>
<li><strong>Sprava webu</strong> — Pridavejte, vypisujte a odstrante weby z vaseho uctu Bing Webmaster</li>
<li><strong>Odeslani URL</strong> — Odesilajte jednotlive URL nebo davkove az 500 URL naraz pro rychlejsi indexaci</li>
<li><strong>Sprava sitemap</strong> — Odesilajte, vypisujte a mazejte XML sitemapy</li>
<li><strong>Statistiky vyhledavani</strong> — Analyzujte vykon ve vyhledavani s daty o zobrazeni, kliknuti, CTR a pozici</li>
<li><strong>Sprava prochazeni</strong> — Sledujte, jak Bingbot prochazi vas web</li>
<li><strong>Vyzkum klicovych slov</strong> — Objevujte nove prilezitosti klicovych slov</li>
<li><strong>Analyza odkazu</strong> — Zjistete, ktere externi weby na vas odkazuji</li>
</ul>

<h2 id="tool-categories">Kategorie nastroju</h2>
<h3>Nastroje pro spravu webu (4 nastroje)</h3>
<p>Spravujte svuj ucet Bing Webmaster. Pridavejte nove weby, vypisujte vsechny registrovane weby a odstrante weby, ktere uz nepotrebujete sledovat.</p>

<h3>Nastroje pro odeslani URL (3 nastroje)</h3>
<p>Ziskejte rychlejsi indexaci. Odesilajte jednotlive URL nebo davkove az 500 URL naraz. Sledujte svou kvotu odeslani.</p>

<h3>Nastroje pro sitemapy (3 nastroje)</h3>
<p>Odesilajte XML sitemapy, vypisujte odeslane sitemapy s jejich stavem a mazejte zastarale sitemapy.</p>

<h3>Nastroje pro analyzu vyhledavani (3 nastroje)</h3>
<p>Pochopte svuj vykon v Bing vyhledavani. Analyzujte dotazy a stranky s metrikami zobrazeni, kliknuti a pozice.</p>

<h3>Nastroje pro spravu prochazeni (4 nastroje)</h3>
<p>Kontrolujte a sledujte interakci Bingbota s vasim webem. Detekujte problemy s prochazenim a konfigurujte rychlost prochazeni.</p>

<h3>Nastroje pro vyzkum klicovych slov (2 nastroje)</h3>
<p>Objevujte nove prilezitosti klicovych slov a nachazejte souvisejici klicova slova pro rozsireni vasi obsahove strategie.</p>

<h2 id="authentication">Autentizace</h2>
<p>Bing Webmaster Tools pouziva <strong>autentizaci API klicem</strong>. Vygenerujte klic v nastaveni vaseho uctu Bing Webmaster.</p>

<h2 id="configuration">Konfigurace</h2>
<pre><code>api_key: "VAS_BING_WEBMASTER_API_KLIC"
site_url: "https://vas-web.cz"</code></pre>`,
    },
    features: [
      'Site management',
      'URL submission',
      'Batch URL submission (up to 500)',
      'Submission quota tracking',
      'Sitemap management',
      'Search statistics',
      'Per-query metrics',
      'Per-page metrics',
      'Crawl statistics',
      'Crawl issue detection',
      'Crawl rate configuration',
      'Keyword research',
      'Related keywords',
      'Inbound link analysis',
    ],
    authMethod: 'API key',
    configFile: '~/bing-webmaster.yaml',
    relatedSlugs: ['search-console', 'google-analytics', 'matomo'],
  },
];
