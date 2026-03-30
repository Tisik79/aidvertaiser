/* -------------------------------------------------------------------------- */
/*  Resource Data — Aidvertaiser Marketing Website                           */
/* -------------------------------------------------------------------------- */

export interface Resource {
  slug: string;
  icon: string;
  category: string;
  title: Record<string, string>;
  shortDescription: Record<string, string>;
  metaDescription: Record<string, string>;
  content: Record<string, string>;
  readTime: number;
  relatedSlugs: string[];
}

/* Helper: for languages we haven't translated yet, fall back to English */
function ml(en: string, cs: string): Record<string, string> {
  return { en, cs, fr: en, es: en, zh: en, hi: en, pt: en, pl: en, ar: en, bn: en };
}

export const resources: Resource[] = [
  /* ==================================================================== */
  /*  1. PPC Master Guide                                                 */
  /* ==================================================================== */
  {
    slug: 'ppc-master-guide',
    icon: 'BookOpen',
    category: 'Guide',
    title: ml(
      'PPC Campaign Master Guide 2026',
      'Hlavni prirucka PPC kampani 2026',
    ),
    shortDescription: ml(
      'The complete end-to-end guide to building, launching, and optimizing PPC campaigns in 2026. Covers every setting, every decision point, and every optimization lever across Google Ads and Microsoft Ads.',
      'Kompletni prirucka pro stavbu, spusteni a optimalizaci PPC kampani v roce 2026. Pokryva kazde nastaveni, kazdy rozhodovaci bod a kazdy optimalizacni prvek na Google Ads a Microsoft Ads.',
    ),
    metaDescription: ml(
      'Complete PPC campaign guide for 2026. Every setting, checklist, and best practice for Google Ads and Microsoft Ads campaigns — from landing pages to advanced bidding strategies.',
      'Kompletni prirucka PPC kampani pro rok 2026. Kazde nastaveni, checklist a best practice pro kampane Google Ads a Microsoft Ads.',
    ),
    content: {
      en: `<h2 id="introduction">The Definitive PPC Manual</h2>
<p>This guide distills everything you need to know about running successful PPC campaigns in 2026. Whether you are launching your first Google Ads campaign or managing a portfolio of accounts spending millions per month, this manual covers every setting, every decision point, and every optimization technique that separates profitable campaigns from money-burning experiments.</p>
<p>The PPC landscape has evolved significantly in 2025-2026. Enhanced CPC was deprecated in March 2025. AI Max for Search arrived in May 2025. Performance Max campaigns expanded their negative keyword limits to 10,000. Customer Match data must migrate to the Data Manager API by April 2026. Search Partners removed parked domains in February 2026. This guide reflects all these changes and their implications for campaign strategy.</p>

<h2 id="pre-launch">Phase 1: Pre-Launch Foundation</h2>
<p>Every successful campaign starts before the first ad is created. The pre-launch phase establishes the business goals, competitive landscape, and keyword universe that will shape your entire campaign structure.</p>
<h3>Business Goals Definition</h3>
<p>Define your primary campaign objective: leads, sales, awareness, app installs, or phone calls. Set target CPA based on your business economics — calculate Customer Lifetime Value (CLV) to determine the maximum acceptable cost per acquisition. If your CLV is $5,000 and your close rate is 20%, you can afford a cost-per-lead of up to $1,000. Most advertisers set target CPA at 20-30% of CLV.</p>
<p>Set target ROAS if you are running e-commerce campaigns. The formula is Revenue divided by Spend times 100. A 400% ROAS (4:1) is considered good for most industries. Identify primary conversion actions (form submissions, purchases, phone calls) and secondary micro-conversions (PDF downloads, video views, page scrolls) that indicate engagement but should not be used for bidding optimization.</p>

<h3>Competitive Research</h3>
<p>Before spending your first dollar, understand what competitors are doing. Use SpyFu, SEMrush, or Ahrefs to extract competitor keywords, ad copy, and estimated spending. Check the Google Ads Transparency Center for actual competitor ad creatives. Document competitor landing pages — screenshot their offers, CTAs, and trust signals. Identify gaps that competitors are not covering.</p>

<h3>Keyword Research</h3>
<p>Use Google Keyword Planner to extract search volume, CPC estimates, and competition levels. Cross-reference with SEMrush or Ahrefs data. Group keywords by intent: informational (how to, what is), navigational (brand searches), commercial (best, review, comparison), and transactional (buy, price, discount, near me). Map keywords to ad groups and landing pages before creating anything.</p>

<h2 id="landing-pages">Phase 2: Landing Page Setup</h2>
<p>The landing page is where campaigns succeed or fail. No amount of keyword optimization or bid management can compensate for a landing page that does not convert.</p>
<p><strong>Critical rule:</strong> One ad group equals one offer equals one landing page. Never send PPC traffic to a generic homepage for non-brand campaigns. Businesses with 40+ landing pages generate 12x more leads than those with 5 or fewer.</p>

<h3>Above-the-Fold Requirements</h3>
<p>Every landing page must include above the fold: a headline that matches the ad copy exactly (message match equals 25% higher conversions), a supporting subheadline with specifics, a hero image or video (video increases conversions by 80-86%), a visible primary CTA button, and the value proposition in 1-2 sentences.</p>

<h3>Technical Requirements</h3>
<p>HTTPS is mandatory — non-HTTPS pages are penalized. Core Web Vitals must pass: LCP under 2.5 seconds, INP under 200ms, CLS under 0.1. A 0.1-second improvement in page speed produces 8-10% conversion lift. 53% of mobile users abandon after 3 or more seconds of load time. Optimize images with WebP format, lazy loading, and srcset for responsive delivery.</p>

<h2 id="tracking">Phase 3: Tracking & Conversion Setup</h2>
<p>Tracking is the foundation that everything else depends on. Without accurate conversion data, bidding algorithms cannot optimize, budget allocation is guesswork, and ROI measurement is impossible.</p>

<h3>Google Ads Conversion Tracking</h3>
<p>Create conversion actions in Google Ads with careful configuration. For each action, set the conversion category, value (static or dynamic), counting method ("One" for leads, "Every" for purchases), click-through window (30 days default, range 1-90 days), view-through window (1 day default, range 1-30 days), and attribution model (Data-Driven is the 2026 default). Critically, designate conversions as Primary (used for bidding optimization) or Secondary (tracking only).</p>

<h3>Enhanced Conversions</h3>
<p>Enhanced Conversions for Web sends hashed first-party data (email, phone, name, address) alongside conversion events, improving measurement when cookies are blocked. Enhanced Conversions for Leads uses GCLID-based offline conversion upload — critical for B2B lead generation where you need to optimize toward closed deals, not just form submissions.</p>

<h3>GA4 Integration</h3>
<p>Link your GA4 property with Google Ads. Configure UTM parameters on all ads. Set up custom dimensions for client type and lead score. Create GA4 audiences for remarketing export. Enable cross-device tracking through Google Signals.</p>

<h2 id="account-structure">Phase 4: Account Structure</h2>
<p>Use consistent naming conventions: <code>[Campaign Type]_[Product/Service]_[Targeting]_[Match Type]_[Geography]</code>. Separate brand from non-brand campaigns always. Separate remarketing from prospecting. Never combine Search and Display in the same campaign. Keep ad groups tightly themed with 5-10 keywords maximum.</p>

<h2 id="campaign-creation">Phase 5: Campaign Creation</h2>
<p>The network settings are where most beginners make critical mistakes. For Search campaigns: Search Network ON, Search Partners OFF initially (2-3x higher fraud rate), Display Network OFF always. Google often auto-includes Display in Search campaigns — always verify this is disabled.</p>
<p><strong>Location targeting critical setting:</strong> Select "Presence: People in or regularly in your targeted locations." Do NOT use "Presence or interest" (the default) — this shows ads to people merely interested in your location who may be anywhere in the world. This single setting is the number one cause of wasted spend from irrelevant geographies.</p>

<h2 id="keywords">Phase 6: Keyword Strategy</h2>
<p>In 2026, match types work differently than their names suggest. Exact match matches same meaning and intent, including close variants and rewordings. Phrase match matches queries including the meaning of your keyword in the same order. Broad match matches related meanings, synonyms, and related searches — only use with Smart Bidding.</p>
<p>Start with exact match for proven, high-converting keywords. Add phrase match for discovery. Use broad match only with Smart Bidding. Long-tail keywords convert 25x better than broad terms.</p>

<h2 id="bidding">Phase 7: Bidding Strategy</h2>
<p>The bidding strategy progression for lead generation campaigns: Manual CPC for weeks 1-4 (collect 15-20 conversions), Maximize Conversions for weeks 5-8 (reach 30+ conversions), Target CPA from month 3 onward (50+ monthly conversions required for stability). For e-commerce: Maximize Conversion Value transitioning to Target ROAS with 50+ monthly conversions. Set daily budget at minimum 2-3x your target CPA. Follow the 20% rule — never change budget or bids by more than 20% per week.</p>
<p>The learning period is 7-30 days (typically 14 days or approximately 50 conversion events). During learning: do not make additional changes, do not panic at volatile performance, do not switch strategies mid-learning. Make one change at a time and wait one week before evaluating.</p>

<h2 id="fraud-prevention">Phase 8: Fraud Prevention</h2>
<p>Click fraud costs advertisers an estimated $100 billion annually. Industry studies estimate 14-20% of all PPC clicks are fraudulent. Key prevention measures: set up IP exclusions (500 per campaign, 500 at account level), disable Search Partners initially, monitor search terms weekly for suspicious patterns, use "Presence only" for location targeting, and review analytics for zero-engagement sessions from paid traffic.</p>

<h2 id="optimization">Phase 9: Ongoing Optimization</h2>
<p>Daily checks: budget pacing, conversion tracking verification, significant performance changes. Weekly: search terms review and negative keyword additions, ad performance comparison, bid adjustments. Monthly: Quality Score audit, landing page testing, audience expansion, competitive analysis. Quarterly: complete account restructuring if needed, strategy review, market analysis.</p>

<h2 id="benchmarks">Industry Benchmarks 2026</h2>
<p>Average Google Ads CTR across industries: 6.66% (up from 3.17% five years ago). Average CPC: $4.66. Average conversion rate: 7.04%. These vary dramatically by industry — legal services average $8.94 CPC while real estate averages $1.81. Use these as directional benchmarks, not absolute targets. Your own historical data is always the best benchmark.</p>`,
      cs: `<h2 id="introduction">Definitivni PPC manual</h2>
<p>Tento pruvodce shrnuje vse, co potrebujete vedet o uspesnem provozovani PPC kampani v roce 2026. At spoustite svou prvni kampan Google Ads nebo spravujete portfolio uctu utracejicich miliony mesicne, tento manual pokryva kazde nastaveni a kazdou optimalizacni techniku.</p>

<h2 id="pre-launch">Faze 1: Pred spustenim</h2>
<p>Kazda uspesna kampan zacina pred vytvorenim prvni reklamy. Definujte primarni cil kampane, nastavte cilovou CPA na zaklade ekonomiky vaseho podniku a provedte konkurencni vyzkum.</p>

<h2 id="landing-pages">Faze 2: Landing pages</h2>
<p>Landing page je misto, kde kampane uspivaji nebo selhavaji. Kriticke pravidlo: jedna reklamni skupina = jedna nabidka = jedna landing page. Firmy se 40+ landing pages generuji 12x vice leadu nez ty s 5 nebo mene.</p>

<h2 id="tracking">Faze 3: Sledovani a konverze</h2>
<p>Bez presnych konverznich dat nemohou algoritmy nabidek optimalizovat. Nastavte konverzni akce, vylepsene konverze a GA4 integraci.</p>

<h2 id="campaign-creation">Faze 4: Vytvoreni kampane</h2>
<p>Kriticke nastaveni lokality: vyberete "Pritomnost: Lide v nebo pravidelne ve vasich cilových lokalitach." Nepouzivejte "Pritomnost nebo zájem" — toto jedno nastaveni je pricinou c. 1 zbytecnych vydaju.</p>

<h2 id="bidding">Faze 5: Strategie nabidek</h2>
<p>Progrese pro lead generation: Manualni CPC (tydny 1-4), Maximalizace konverzi (tydny 5-8), Cilova CPA (od mesice 3). Dodrzujte pravidlo 20% — nikdy nemente rozpocet nebo nabidky o vice nez 20% za tyden.</p>

<h2 id="benchmarks">Benchmarky 2026</h2>
<p>Prumerne CTR Google Ads: 6.66%. Prumerne CPC: $4.66. Prumerny konverzni pomer: 7.04%. Tyto se dramaticky lisi podle odvetvi.</p>`,
    },
    readTime: 25,
    relatedSlugs: ['bidding-strategies', 'audience-targeting-guide', 'landing-page-optimization'],
  },

  /* ==================================================================== */
  /*  2. Audience Targeting Guide                                         */
  /* ==================================================================== */
  {
    slug: 'audience-targeting-guide',
    icon: 'UsersThree',
    category: 'Guide',
    title: ml(
      'Audience Targeting & Segmentation Guide',
      'Pruvodce cilenim a segmentaci publika',
    ),
    shortDescription: ml(
      'Master audience targeting across Google Ads and Meta Ads. Learn segmentation strategies, remarketing lists, Customer Match, lookalike audiences, interest targeting, and sequential messaging for every funnel stage.',
      'Ovladnete cileni na publika na Google Ads a Meta Ads. Naucte se segmentacni strategie, remarketing, Customer Match, lookalike publika, cileni podle zajmu a sekvencni messaging.',
    ),
    metaDescription: ml(
      'Master PPC audience targeting. Segmentation strategies, remarketing, Customer Match, lookalikes, interest targeting, and funnel-stage messaging for Google Ads and Meta Ads.',
      'Ovladnete PPC cileni na publika. Segmentacni strategie, remarketing, Customer Match, lookalike publika a funnelovy messaging pro Google Ads a Meta Ads.',
    ),
    content: {
      en: `<h2 id="introduction">Beyond Keywords: The Audience Revolution</h2>
<p>The shift from keyword-only targeting to audience-driven advertising represents the biggest change in PPC strategy over the last five years. While keywords capture intent (what users are searching for), audiences capture identity (who the users are). The most effective campaigns combine both — showing the right message to the right person at the right moment in their buying journey.</p>
<p>Google Ads now offers over 1,000 in-market segments, 150+ affinity segments, custom segments by keywords and URLs, detailed demographics, life events, and remarketing lists. Meta Ads provides interest targeting across thousands of categories, behavioral targeting based on real-world actions, custom audiences from CRM data, and lookalike audiences that find users similar to your best customers. Understanding how to layer these targeting options is what separates amateurs from professionals.</p>

<h2 id="google-audiences">Google Ads Audience Types</h2>
<h3>Affinity Segments</h3>
<p>Affinity segments target users based on their long-term interests and habits. Google identifies these through browsing history, search patterns, and content consumption. With approximately 150 pre-built affinity segments like "Cooking Enthusiasts," "Outdoor Enthusiasts," and "Technophiles," these are best for top-of-funnel awareness campaigns. They cast a wide net and work well with broad messaging.</p>

<h3>In-Market Segments</h3>
<p>In-market segments target users who are actively researching or considering a purchase. Google's algorithm identifies purchase intent through recent search queries, website visits, video views, and ad interactions. With over 1,000 in-market segments, these are your mid-to-bottom funnel targeting power. A user classified as "in-market for CRM Software" has demonstrated active purchase intent through their behavior.</p>

<h3>Custom Segments</h3>
<p>Custom segments let you define your own audience criteria using keywords, URLs, and apps. Target users who have searched for specific terms on Google, visited specific competitor websites, or used specific apps. This is the most flexible targeting option — you can create highly specific audience definitions that no pre-built segment covers.</p>

<h3>Detailed Demographics</h3>
<p>Beyond basic age and gender, Google provides detailed demographic targeting: parental status (parent or not), household income (top 10% through lower 50%), education level, homeowner status, and employment industry. These are particularly valuable for financial services, luxury goods, real estate, and education advertisers.</p>

<h3>Life Events</h3>
<p>Nine life event segments capture users going through major milestones: getting married, moving, graduating, starting a new job, buying a home, having a baby, retiring, starting a business, and getting a pet. Life events create temporary but intense buying needs. A user about to move needs movers, furniture, internet service, and home insurance — all within a compressed time window.</p>

<h2 id="meta-audiences">Meta Ads Audience Targeting</h2>
<h3>Interest Targeting</h3>
<p>Meta's interest database draws from user behavior across Facebook, Instagram, WhatsApp, and Messenger. Unlike Google's inferred interests, Meta's are based on explicit signals: pages liked, content engaged with, groups joined, and activities participated in. Search interests by keyword through Aidvertaiser to discover targetable segments and their estimated sizes.</p>

<h3>Behavioral Targeting</h3>
<p>Behavioral targeting on Meta goes beyond expressed interests to actual behaviors. Target users based on purchase behavior (online shoppers, luxury goods buyers, deal seekers), device usage (early technology adopters, specific phone models, operating system versions), travel patterns (frequent travelers, international travelers, commuters), and financial behavior (investors, credit card users). Behavioral targeting is more predictive than interest targeting because it reflects what people do, not just what they say they like.</p>

<h3>Custom Audiences</h3>
<p>Upload your customer data (email, phone, name) to Meta to create Custom Audiences. Meta matches your data against its user base with typical match rates of 30-70%. Use Custom Audiences for remarketing to existing customers, creating exclusion lists (do not show acquisition ads to current customers), and building lookalike audiences. Include multiple identifiers (email plus phone plus address) for 10-30% higher match rates.</p>

<h3>Lookalike Audiences</h3>
<p>Lookalike audiences find new users who resemble your best customers. Create a source audience (your customer list, website converters, or app users), select the geographic market, and choose a similarity percentage (1% is most similar, 10% is broadest reach). Start with 1% lookalikes for the highest quality, then expand to 2-5% for scale. Lookalikes based on high-value customers outperform those based on all customers.</p>

<h2 id="remarketing">Remarketing Strategy</h2>
<p>Remarketing — showing ads to people who have already interacted with your business — is consistently the highest-ROI targeting strategy in PPC. Create these remarketing lists:</p>
<ul>
<li><strong>All website visitors</strong> (30, 60, 90 day windows) — General remarketing for staying top-of-mind</li>
<li><strong>Specific page visitors</strong> — Target users who viewed product pages, pricing pages, or key content</li>
<li><strong>Cart/form abandoners</strong> (7-30 days) — Highest intent; these users were about to convert</li>
<li><strong>Past converters</strong> — For upselling, cross-selling, or exclusion from acquisition campaigns</li>
<li><strong>YouTube viewers and subscribers</strong> — Video engagement indicates strong brand awareness</li>
</ul>
<p>Minimum list sizes for Google Ads: 100 active users for Display, Search, and Shopping. 1,000 for Demand Gen campaigns. Maximum membership duration is 540 days.</p>

<h2 id="sequential">Sequential Messaging by Funnel Stage</h2>
<p>The most sophisticated audience strategies use sequential messaging — different ads for different stages of the buying journey:</p>
<ul>
<li><strong>Top of funnel (Cold)</strong> — Affinity segments, broad in-market. Messaging focuses on problem awareness and education. Exclude warm and hot audiences</li>
<li><strong>Middle of funnel (Warm)</strong> — Site visitors 30-90 days, YouTube engagers. Messaging focuses on trust, social proof, and case studies. Exclude hot audiences and recent converters</li>
<li><strong>Bottom of funnel (Hot)</strong> — Cart abandoners 7-14 days, pricing page visitors. Messaging includes direct CTA, offers, and urgency. Exclude recent converters</li>
</ul>

<h2 id="exclusions">Audience Exclusions</h2>
<p>What you exclude is as important as what you target. Always exclude: recent converters (7-30 day window based on buying cycle), existing customers from acquisition campaigns, job seekers who visited careers pages, competitor employees (upload list if available), your own employees, support page visitors (already customers), and disengaged visitors identified through GA4 low-engagement audiences.</p>

<h2 id="bid-adjustments">Audience Bid Adjustments</h2>
<p>For Manual CPC campaigns, apply bid adjustments to audience segments: cart abandoners +50% to +150%, pricing page visitors +30% to +100%, past converters for upsell +20% to +80%, in-market segments +10% to +25%, non-converting audiences -30% to -90%. With Smart Bidding, manual adjustments are overridden — focus on providing quality audience signals instead.</p>`,
      cs: `<h2 id="introduction">Za klicova slova: Revoluce publika</h2>
<p>Prechod od cileni pouze na klicova slova k reklame rizene publikem je nejvetsi zmena v PPC strategii za poslednich pet let. Nejucinnejsi kampane kombinuji oboje — ukazuji spravnou zpravu spravne osobe ve spravny okamzik.</p>

<h2 id="google-audiences">Typy publika Google Ads</h2>
<p>Google nabizi 1000+ in-market segmentu, 150+ affinity segmentu, vlastni segmenty, detailni demografii, zivotni udalosti a remarketingove seznamy. Kazdy typ slouzi k jinemu ucelu v marketingovem funnelu.</p>

<h2 id="meta-audiences">Cileni publika Meta Ads</h2>
<p>Meta nabizi cileni podle zajmu, behavioralni cileni, vlastni publika z CRM dat a lookalike publika pro nalezeni uzivatelu podobnych vasim nejlepsim zakaznikum.</p>

<h2 id="remarketing">Strategie remarketingu</h2>
<p>Remarketing je trvale strategii s nejvyssim ROI v PPC. Vytvorte seznamy vsech navstevniku, navstevniku konkretnich stranek, opustenych kosiku a minulych konverzi.</p>

<h2 id="sequential">Sekvencni messaging</h2>
<p>Ruzne reklamy pro ruzne faze nakupni cesty: horni cast funnelu (povedomi), stredni cast (duvera) a spodni cast (primy CTA a nabidky).</p>`,
    },
    readTime: 18,
    relatedSlugs: ['ppc-master-guide', 'bidding-strategies', 'campaign-analysis'],
  },

  /* ==================================================================== */
  /*  3. Bidding Strategies                                               */
  /* ==================================================================== */
  {
    slug: 'bidding-strategies',
    icon: 'CurrencyDollar',
    category: 'Guide',
    title: ml(
      'PPC Bidding & Budget Management Guide',
      'Pruvodce strategiemi nabidek a spravou rozpoctu v PPC',
    ),
    shortDescription: ml(
      'Navigate the complex world of PPC bidding strategies. From Manual CPC for beginners to Target ROAS for advanced advertisers, understand when to use each strategy, how to manage learning periods, and how to optimize budgets.',
      'Orientujte se ve slozitem svete PPC strategii nabidek. Od Manualniho CPC pro zacatecniky po Cilovou ROAS pro pokrocile inzerenty. Pochopte, kdy pouzit kazdou strategii a jak spravovat rozpocty.',
    ),
    metaDescription: ml(
      'Complete guide to PPC bidding strategies for 2026. Manual CPC, Maximize Conversions, Target CPA, Target ROAS — when to use each, learning periods, and budget optimization.',
      'Kompletni pruvodce strategiemi nabidek PPC pro rok 2026. Manualni CPC, Maximalizace konverzi, Cilova CPA, Cilova ROAS — kdy co pouzit a jak optimalizovat rozpocty.',
    ),
    content: {
      en: `<h2 id="introduction">Bidding: Where Money Meets Machine Learning</h2>
<p>Your bidding strategy is the single most impactful decision in your Google Ads campaigns. It determines how much you pay for each click, how aggressively you pursue conversions, and how efficiently your budget is spent. Choose wrong, and you will either overpay for low-quality traffic or miss high-value conversions. Choose right, and your campaigns become self-optimizing profit machines.</p>
<p>The bidding landscape changed significantly in 2025. Enhanced CPC was deprecated in March 2025, forcing all advertisers to choose between full manual control and full algorithmic control. Smart Bidding Exploration was introduced, seeing 18% more unique search queries with conversions and 19% more conversions overall. Understanding the current state of bidding is essential for competitive PPC management.</p>

<h2 id="strategy-selection">Strategy Selection Guide</h2>
<p>Choosing the right bidding strategy depends on your data maturity, campaign goals, and budget. Here is a decision framework:</p>
<ul>
<li><strong>New account, no conversion data:</strong> Manual CPC — You need full control while building a conversion baseline</li>
<li><strong>Small budget under $2,000/month:</strong> Manual CPC — Budget constraints require careful per-keyword bid management</li>
<li><strong>Building traffic, no conversion tracking:</strong> Maximize Clicks with a maximum CPC limit — Get traffic flowing while setting up tracking</li>
<li><strong>Brand protection campaigns:</strong> Target Impression Share with a maximum CPC limit — Ensure visibility on brand searches</li>
<li><strong>Lead generation with 15-30 monthly conversions:</strong> Maximize Conversions — Let Google's algorithm optimize with moderate data</li>
<li><strong>Lead generation with 30+ monthly conversions:</strong> Target CPA — Set your ideal cost-per-lead and let Google hit it</li>
<li><strong>E-commerce with varying product values and 30+ conversions:</strong> Maximize Conversion Value transitioning to Target ROAS</li>
</ul>

<h2 id="progression">The Bidding Progression Path</h2>
<h3>Phase 1: Manual CPC (Weeks 1-4)</h3>
<p>Start here when you have no conversion history. Set bids manually at the keyword level based on estimated value. Your goal is to collect 15-20 conversions to give Smart Bidding enough data to work with. Focus on getting clicks from your highest-intent keywords. Review search terms daily. Add negative keywords aggressively. This phase is about building a data foundation.</p>

<h3>Phase 2: Maximize Conversions (Weeks 5-8)</h3>
<p>Switch to Maximize Conversions when you have 15-20 conversions in the last 30-45 days. This strategy will spend your entire daily budget to get as many conversions as possible. Important: Maximize Conversions will spend your full budget — set the daily budget to what you are comfortable spending even on bad days. Your goal is to reach 30+ monthly conversions.</p>

<h3>Phase 3: Target CPA (Month 3+)</h3>
<p>Graduate to Target CPA when you have 30-50+ monthly conversions. Set your initial target CPA at or slightly above your actual average CPA from Phase 2. Lower the target by no more than 20% per week. Your daily budget should be at least 2-3x your target CPA to give the algorithm room to work. This strategy optimizes for conversion volume at your target cost.</p>

<h3>Phase 4: Target ROAS (For E-commerce)</h3>
<p>Target ROAS requires 50+ monthly conversions with accurate conversion value tracking. The formula: ROAS equals Revenue divided by Spend times 100. Industry average is 200% (2:1); a common target is 400% (4:1). This strategy requires dynamic conversion values — if all your conversions have the same value, use Target CPA instead.</p>

<h2 id="learning-period">Managing the Learning Period</h2>
<p>When you change bidding strategies, budgets, or targets, the algorithm enters a learning period of 7-30 days (typically 14 days or approximately 50 conversion events). Performance during learning is volatile — CPAs may spike, impressions may fluctuate, and ROAS may dip temporarily.</p>
<p>What triggers learning: new campaigns or strategy changes, bid strategy switches, target CPA or ROAS changes, budget changes over 20%, conversion action changes, major targeting changes, and adding or removing more than 20% of keywords.</p>
<p>Rules during learning: do not make additional changes, do not panic at volatile performance, do not switch strategies mid-learning, make one change at a time and wait one full week before evaluating. Use a graduated budget approach: 60% of target budget in week 1, 80% in week 2, full budget after learning completes.</p>
<p>If your campaign shows "Limited by Learning," check that you have sufficient conversion volume (30-50 per month minimum), ensure budget is at least 2-3x target CPA, consider consolidating small campaigns to pool conversion data, or step down to a less data-hungry strategy.</p>

<h2 id="budget-management">Budget Management Principles</h2>
<p>Google can spend up to 2x your daily budget on any single day, but the monthly maximum is daily budget times 30.4. Set your daily budget based on monthly goals: if your monthly budget is $3,000, your daily budget is $98.68 ($3,000 divided by 30.4).</p>
<p>Follow the 20% rule religiously — never change your budget by more than 20% in a single week. Larger changes trigger the learning period and reset algorithmic optimization. If you need to double your budget, do it in 20% weekly increments over 4-5 weeks.</p>
<p>Monitor impression share alongside budget. If your impression share is low (under 80%) with good CPA, you have room to increase budget profitably. If impression share is high (over 90%) with rising CPA, you are competing for diminishing returns.</p>

<h2 id="smart-bidding-signals">Smart Bidding: What the Algorithm Knows</h2>
<p>Google's Smart Bidding evaluates 70+ million signal combinations at auction time. Signals include device type, operating system, and browser; physical location at city level; location intent from search queries; time of day and day of week; remarketing list membership; ad creative characteristics; search query and landing page; language settings; and demographics. This real-time, per-auction optimization is why Smart Bidding outperforms manual bidding at scale — no human can process 70 million signals in real time.</p>

<h2 id="portfolio">Portfolio Bidding Strategies</h2>
<p>Portfolio strategies apply a single bidding strategy across multiple campaigns. They pool conversion data from all campaigns in the portfolio, which is particularly valuable when individual campaigns have low conversion volume. Use portfolio strategies with shared budgets for campaigns targeting the same business goal. This approach accelerates learning and provides the algorithm with more data for optimization.</p>`,
      cs: `<h2 id="introduction">Nabidky: Kde se penize setkavaji se strojovym ucenim</h2>
<p>Vase strategie nabidek je jednim nejdulezitejsim rozhodnutim ve vasich kampaních Google Ads. Urcuje, kolik platite za kazde kliknuti a jak efektivne je vas rozpocet vynakladan.</p>

<h2 id="strategy-selection">Pruvodce vyberem strategie</h2>
<p>Vyber spravne strategie zavisi na zralosti vasich dat, cilech kampani a rozpoctu. Novy ucet: Manualni CPC. Lead generation s 15-30 konverzemi: Maximalizace konverzi. S 30+ konverzemi: Cilova CPA.</p>

<h2 id="learning-period">Sprava ucebniho obdobi</h2>
<p>Pri zmene strategii algoritmus vstoupi do ucebniho obdobi 7-30 dnu. Behem uceni: nedelejte dalsi zmeny, nepanikte pri kolisavem vykonu a neprepinjejte strategie.</p>

<h2 id="budget-management">Principy spravy rozpoctu</h2>
<p>Dodrzujte pravidlo 20% — nikdy nemente rozpocet o vice nez 20% za tyden. Sledujte podil zobrazeni vedle rozpoctu pro informovane rozhodovani o skalovani.</p>`,
    },
    readTime: 15,
    relatedSlugs: ['ppc-master-guide', 'audience-targeting-guide', 'campaign-analysis'],
  },

  /* ==================================================================== */
  /*  4. Landing Page Optimization                                        */
  /* ==================================================================== */
  {
    slug: 'landing-page-optimization',
    icon: 'Browser',
    category: 'Guide',
    title: ml(
      'Landing Page Optimization for PPC',
      'Optimalizace landing pages pro PPC',
    ),
    shortDescription: ml(
      'Build high-converting landing pages for PPC campaigns. Design principles, technical requirements, form optimization, CTA best practices, mobile optimization, and A/B testing strategies backed by data.',
      'Vytvarejte vysoce konvertujici landing pages pro PPC kampane. Designove principy, technicke pozadavky, optimalizace formularu, CTA best practices a A/B testovaci strategie podlozene daty.',
    ),
    metaDescription: ml(
      'Landing page optimization guide for PPC. Design, technical specs, forms, CTAs, mobile optimization, and testing strategies to maximize conversion rates from ad traffic.',
      'Pruvodce optimalizaci landing pages pro PPC. Design, technicke specifikace, formulare, CTA, mobilni optimalizace a testovaci strategie pro maximalizaci konverznich pomeru.',
    ),
    content: {
      en: `<h2 id="introduction">The Landing Page Is the Campaign</h2>
<p>You can have the perfect keyword strategy, flawless ad copy, and an unlimited budget — but if your landing page does not convert, none of it matters. The landing page is where advertising spend becomes revenue. A 1% improvement in landing page conversion rate has the same impact as a 1% decrease in CPC — but is often easier to achieve.</p>
<p>The data is unambiguous. Businesses with 40+ landing pages generate 12x more leads than those with 5 or fewer. Message match between ad and landing page delivers 25% higher conversions. Video on landing pages increases conversions by 80-86%. Multi-step forms convert 86% better than single-step forms. A 0.1-second improvement in page speed yields 8-10% conversion lift. Every element matters, and every element is measurable.</p>

<h2 id="one-page-rule">The One-Page Rule</h2>
<p>The fundamental principle of PPC landing pages is specificity. One ad group equals one offer equals one landing page. Never send PPC traffic to a generic homepage for non-brand campaigns. The only exception is brand campaigns (users searching your company name), where the homepage is the appropriate destination.</p>
<p>For product-specific keywords, create dedicated landing pages per ad group. For high-volume, high-value keyword groups, create unique pages per keyword group. For promotions and offers, build dedicated promo landing pages. For low-volume long-tail keywords, use dynamic content on template pages that adjust headlines and hero images based on the keyword trigger.</p>

<h2 id="above-fold">Above-the-Fold Requirements</h2>
<p>The above-the-fold content determines whether users stay or leave. Every PPC landing page must include these five elements without requiring a scroll:</p>
<ol>
<li><strong>Headline matching the ad copy</strong> — Message match is non-negotiable. If your ad says "Get 30% Off CRM Software," the landing page headline must reference the same offer. Mismatched messaging creates cognitive dissonance and immediate bounces. Message match alone produces 25% higher conversion rates</li>
<li><strong>Supporting subheadline</strong> — Expand on the headline with specifics: pricing, time frames, unique differentiators. "Enterprise CRM starting at $29/user/month. Free migration included."</li>
<li><strong>Hero image or video</strong> — Visual content that demonstrates the product or service. Video increases conversions by 80-86%. Product screenshots, demo recordings, and customer testimonial videos all outperform stock photography</li>
<li><strong>Primary CTA button</strong> — Visible without scrolling, high contrast color that appears nowhere else on the page, action-oriented text ("Get My Free Trial" not "Submit"), minimum 44x44px tap target for mobile</li>
<li><strong>Value proposition</strong> — One to two sentences summarizing why the user should act now. Focus on benefits, not features. "Close deals 40% faster" beats "Advanced pipeline management features"</li>
</ol>

<h2 id="trust-signals">Trust Signals</h2>
<p>Trust signals are what convert browsers into buyers. Include as many as applicable:</p>
<ul>
<li><strong>Customer testimonials</strong> — Video testimonials outperform text by 80-86%. Include name, title, company, and photo for credibility. Feature testimonials relevant to the visitor's use case</li>
<li><strong>Client and partner logos</strong> — Social proof through association. "Trusted by" logo bars are one of the highest-converting page elements</li>
<li><strong>Industry certifications and awards</strong> — Third-party validation builds credibility</li>
<li><strong>Security badges</strong> — SSL, Norton, BBB, PCI compliance. Particularly important for e-commerce and financial services</li>
<li><strong>Money-back guarantee</strong> — Removes purchase risk. "30-day money-back guarantee, no questions asked"</li>
<li><strong>Social proof numbers</strong> — "Join 10,000+ users" or "4.8/5 from 2,000+ reviews." Specific numbers are more believable than round numbers</li>
<li><strong>Privacy policy link</strong> — Visible near forms to address data concern anxiety</li>
</ul>

<h2 id="form-optimization">Form Optimization</h2>
<p>Forms are where most landing page conversion is won or lost. Every additional field reduces conversions. The data shows:</p>
<ul>
<li>Forms with 5 or fewer fields convert 120% better than longer forms</li>
<li>Multi-step forms convert 86% higher than single-step forms (progressive disclosure reduces perceived effort)</li>
<li>Start with easy fields (name, email) before asking for sensitive information (phone, budget, company size)</li>
<li>Use single-column layout — multi-column forms confuse the eye flow</li>
<li>Implement inline validation so users know immediately if something is wrong</li>
<li>Clear field labels above each field, not placeholder text inside the field (placeholder text disappears on focus and users lose context)</li>
</ul>

<h2 id="cta-design">CTA Button Design</h2>
<p>The CTA button is the single most important element on your landing page. Design principles:</p>
<ul>
<li><strong>High contrast color</strong> — The button color should stand out from the page and not appear anywhere else. Orange, green, and red buttons typically outperform blue and gray</li>
<li><strong>Action-oriented text</strong> — First-person phrasing converts better: "Get My Free Trial" outperforms "Start Your Free Trial" which outperforms "Submit." Avoid generic text like "Submit," "Click Here," or "Learn More"</li>
<li><strong>Size matters</strong> — Minimum 44x44px for mobile tap targets. The button should be the most prominent visual element in its section</li>
<li><strong>Repeat at scroll points</strong> — Place the CTA at logical intervals: above the fold, after benefits, after testimonials, and at the page bottom</li>
<li><strong>Sticky CTA on mobile</strong> — A fixed-position CTA that stays visible as users scroll generates 27% more clicks on mobile devices</li>
</ul>

<h2 id="mobile">Mobile Optimization</h2>
<p>83% of traffic is mobile. If your landing page is not optimized for mobile, you are wasting 83% of your ad spend. Mobile requirements:</p>
<ul>
<li>Fully responsive design that adapts to any screen width</li>
<li>Minimum 16px font size for body text (users should not need to pinch-zoom)</li>
<li>Thumb-friendly buttons and interactive elements in the lower two-thirds of the screen</li>
<li>Click-to-call phone numbers that open the phone dialer</li>
<li>No horizontal scrolling under any circumstances</li>
<li>Single-column layout for all content sections</li>
<li>Reduced image sizes for faster mobile loading</li>
</ul>

<h2 id="page-structure">Optimal Page Structure</h2>
<p>The most effective landing page follows this top-to-bottom structure:</p>
<ol>
<li><strong>Value proposition</strong> (above fold) — Headline, subheadline, hero visual, primary CTA</li>
<li><strong>Benefits</strong> — How you solve the user's problems. 3-4 benefit blocks with icons, headlines, and short descriptions</li>
<li><strong>Features</strong> — Specific capabilities. Feature comparison tables, screenshots, specification lists</li>
<li><strong>Social proof</strong> — Testimonials, case studies, client logos, review scores, usage statistics</li>
<li><strong>Final CTA</strong> — Repeat the offer with urgency or additional incentive. "Start your free trial today — no credit card required"</li>
</ol>

<h2 id="technical">Technical Performance</h2>
<p>Landing page speed directly impacts both Quality Score and conversion rate. Core Web Vitals requirements: LCP under 2.5 seconds, INP under 200ms, CLS under 0.1. Server response time (TTFB) should be under 200ms. Implement WebP images, lazy loading, srcset for responsive images, and specify image dimensions to prevent layout shift. No redirect chains between the ad click URL and the final page — maximum one redirect.</p>
<p>For PPC-only landing pages, add <code>&lt;meta name="robots" content="noindex, nofollow"&gt;</code> to prevent organic indexing. Do not block the page via robots.txt — the crawler must be able to reach and read the noindex tag.</p>

<h2 id="post-click">Post-Click Experience</h2>
<p>The conversion does not end at the form submission. The thank-you page and follow-up sequence are where 20% secondary conversion rate is achievable. The thank-you page should confirm the action taken, set expectations for next steps, offer a secondary CTA (referral, social share, related content), and optionally include a video introducing the team or next steps. The confirmation email should deliver the promised asset, outline next steps, include social proof reinforcement, and use a real person's name as the sender.</p>`,
      cs: `<h2 id="introduction">Landing page je kampan</h2>
<p>Muzete mit dokonalou strategii klicovych slov a neomezeny rozpocet — ale pokud vase landing page nekonvertuje, nic z toho nezalezi. Data jsou jednoznacna: firmy se 40+ landing pages generuji 12x vice leadu. Message match prinasi 25% vyssi konverze. Video zvysuje konverze o 80-86%.</p>

<h2 id="above-fold">Pozadavky nad ohybem</h2>
<p>Kazda PPC landing page musi obsahovat bez nutnosti scrollovani: titulek shodny s textem reklamy, podporny podtitulek, hero obrazek nebo video, viditelne CTA tlacitko a hodnotovou nabidku v 1-2 vetach.</p>

<h2 id="form-optimization">Optimalizace formularu</h2>
<p>Formulare s 5 nebo mene poli konvertuji o 120% lepe. Vicekrokove formulare konvertuji o 86% lepe. Zacnete snadnymi poli pred citlivymi informacemi.</p>

<h2 id="mobile">Mobilni optimalizace</h2>
<p>83% navstevnosti je mobilni. Minimalni velikost pisma 16px. Priatelska tlacitka pro palec. Click-to-call telefonni cisla. Zadne horizontalni scrollovani.</p>

<h2 id="technical">Technicky vykon</h2>
<p>LCP pod 2.5 sekundy, INP pod 200ms, CLS pod 0.1. Zlepseni rychlosti o 0.1 sekundy prinasi 8-10% narust konverzi.</p>`,
    },
    readTime: 16,
    relatedSlugs: ['ppc-master-guide', 'campaign-analysis', 'click-fraud-prevention'],
  },

  /* ==================================================================== */
  /*  5. Click Fraud Prevention                                           */
  /* ==================================================================== */
  {
    slug: 'click-fraud-prevention',
    icon: 'ShieldCheck',
    category: 'Guide',
    title: ml(
      'PPC Click Fraud Prevention Guide',
      'Pruvodce prevenci podvodnich kliknuti v PPC',
    ),
    shortDescription: ml(
      'Protect your ad budget from click fraud. Understand the types of fraud, detection methods, prevention strategies, and how to use Aidvertaiser tools to monitor and block fraudulent activity across your campaigns.',
      'Chrante svuj reklamni rozpocet pred podvodnymi kliknutimi. Pochopte typy podvodu, metody detekce, preventivni strategie a jak pouzit nastroje Aidvertaiser pro monitoring a blokovani podvodne aktivity.',
    ),
    metaDescription: ml(
      'Complete guide to PPC click fraud prevention. Detection methods, IP exclusions, analytics monitoring, and protection strategies for Google Ads and Meta Ads campaigns.',
      'Kompletni pruvodce prevenci podvodnich kliknuti v PPC. Metody detekce, vylouceni IP, monitoring analytiky a ochranne strategie pro kampane Google Ads a Meta Ads.',
    ),
    content: {
      en: `<h2 id="introduction">The $100 Billion Problem</h2>
<p>Click fraud is estimated to cost advertisers over $100 billion annually worldwide. Industry studies indicate that 14-20% of all PPC clicks are fraudulent or invalid — meaning that for every $10,000 you spend on ads, $1,400 to $2,000 is consumed by clicks that will never become customers. The problem is growing as bot networks become more sophisticated and harder to distinguish from legitimate users.</p>
<p>Google and Meta have built-in fraud detection systems that automatically filter invalid clicks and issue credits. Google reports that its automated systems detect and filter most invalid clicks before they even appear in your account. But "most" is not "all." Sophisticated click fraud operations use residential IP addresses, mimic human browsing patterns, and distribute clicks across time periods to evade automated detection. This is where proactive monitoring becomes essential.</p>

<h2 id="types">Types of Click Fraud</h2>
<h3>Competitor Click Fraud</h3>
<p>Your competitors click your ads to drain your budget, pushing your ads out of auction when your daily budget is exhausted. This is the most common form of click fraud in competitive industries. Signs include: repeated clicks from the same IP addresses during business hours, clicks with immediate bounces (zero time on site), and geographic concentration from areas where your competitors are located.</p>

<h3>Bot Networks</h3>
<p>Automated bot networks generate large volumes of fraudulent clicks using distributed networks of compromised devices. Modern bots simulate human behavior — they scroll pages, move the mouse, and even submit forms — making them harder to detect through simple behavioral analysis. Signs include: unusual traffic spikes during off-hours, sessions with identical browser fingerprints, and traffic from data center IP ranges.</p>

<h3>Click Farms</h3>
<p>Organized operations where low-wage workers click ads manually. Because the clicks come from real humans on real devices, they bypass many automated detection systems. Signs include: traffic from developing countries not in your targeting, high click volumes from specific geographic clusters, and clicks with minimal engagement (no page scrolls, no link clicks, no form interactions).</p>

<h3>Publisher Fraud</h3>
<p>On the Display Network and Search Partners, publishers may inflate their ad revenue by clicking or encouraging clicks on the ads displayed on their properties. Google Search Partners carry a 2-3x higher fraud rate than Google Search itself. This is why disabling Search Partners and running Display as a separate, monitored campaign is recommended.</p>

<h3>Accidental Invalid Clicks</h3>
<p>Not all invalid clicks are malicious. Fat-finger taps on mobile ads, double-clicks, and clicks from users who immediately realize the ad is not relevant are classified as invalid. While not fraud, they still consume budget without value.</p>

<h2 id="detection">Detection Methods</h2>
<h3>Search Terms Report Analysis</h3>
<p>The Google Ads search terms report reveals the actual queries triggering your ads. Review it weekly and look for: irrelevant queries that should not be triggering your ads, the same query generating multiple clicks in short time windows, queries from unexpected geographic patterns, and queries with abnormally high CTR but zero conversions.</p>

<h3>Analytics Cross-Referencing</h3>
<p>Compare ad platform click data with analytics session data. If Google Ads reports 1,000 clicks but GA4 shows only 700 sessions from paid search, the 30% gap warrants investigation. Some gap is normal (users who click but navigate away before the page loads), but gaps above 15-20% suggest click fraud or bot activity.</p>
<p>In your analytics platform, monitor: bounce rate by traffic source (fraudulent clicks typically show near-100% bounce rates), time on site from paid traffic (bot clicks often result in zero-second sessions), pages per session (legitimate users browse; bots do not), and conversion rate anomalies by time of day or geographic segment.</p>

<h3>IP Pattern Analysis</h3>
<p>Monitor server logs for IP addresses that repeatedly click your ads. Look for: the same IP clicking multiple ads within minutes, IPs from data center ranges (not residential), clusters of clicks from the same IP subnet, and IPs that appear consistently across multiple days without any conversions.</p>

<h3>Session Recording Analysis</h3>
<p>Tools like Microsoft Clarity (free) or Hotjar provide session recordings that show exactly what visitors do on your landing pages. Review sessions from paid traffic to identify bot-like behavior: instant page loads followed by immediate exits, no mouse movement or scrolling, identical navigation patterns across multiple sessions, and form fills with random or nonsensical data.</p>

<h2 id="prevention">Prevention Strategies</h2>
<h3>IP Exclusions</h3>
<p>Google Ads allows 500 IP exclusions per campaign and 500 at the account level. Add: known fraudulent IPs identified through log analysis, competitor office IPs (search their business address, check IP geolocation), your own office IPs (prevent employee clicks that waste budget), and known data center IP ranges associated with bot networks. Note: IP exclusions are not available for Performance Max, Video, Hotel, or App campaigns.</p>

<h3>Geographic Targeting</h3>
<p>The location targeting setting is your first line of defense. Always select "Presence: People in or regularly in your targeted locations" instead of the default "Presence or interest." The default setting shows ads to anyone who has shown interest in your targeted location — even if they are on the other side of the world. This single change eliminates a significant source of irrelevant and potentially fraudulent clicks.</p>

<h3>Network Restrictions</h3>
<p>Disable Search Partners initially. Google's Search Partners network includes YouTube search, Google Maps, Google Shopping, Google Images, and various third-party sites. The fraud rate on Search Partners is 2-3x higher than on Google Search itself. Only enable Search Partners after you have established baseline performance and can monitor for quality degradation.</p>
<p>For Display campaigns, maintain an aggressive placement exclusion list. Exclude mobile app categories (games, utilities) that generate accidental clicks. Exclude parked domains and low-quality content sites. Use the placement report to identify sites with high clicks but zero conversions and add them to your exclusion list. Google allows up to 65,000 placement exclusions at the account level.</p>

<h3>Ad Scheduling</h3>
<p>If fraud patterns correlate with specific time periods — often overnight or on weekends — reduce bids by 50-90% or pause ads during those windows. Use Aidvertaiser to pull performance data by hour of day and day of week to identify periods with high clicks but low conversion rates.</p>

<h3>Device Targeting</h3>
<p>If fraud is concentrated on specific device types — mobile is more common for accidental clicks and bot traffic — apply negative bid adjustments (-50% to -100%) for those device categories. Set -100% to completely exclude a device type from specific campaigns.</p>

<h2 id="monitoring">Ongoing Monitoring with Aidvertaiser</h2>
<p>Set up a weekly fraud monitoring workflow using Aidvertaiser:</p>
<ol>
<li>Pull the Google Ads search terms report for the past 7 days — identify queries with high clicks, zero conversions, and suspicious CTR</li>
<li>Add irrelevant queries as campaign-level negative keywords</li>
<li>Compare Google Ads click counts with GA4 session counts by campaign — investigate gaps above 15%</li>
<li>Check Matomo for paid traffic sessions with zero engagement (zero scroll depth, zero time on page)</li>
<li>Review geographic distribution of clicks — flag any unexpected concentration</li>
<li>Add identified suspicious IPs to campaign exclusion lists</li>
<li>Document findings and track fraud prevention savings over time</li>
</ol>

<h2 id="third-party">Third-Party Fraud Prevention Tools</h2>
<p>For advertisers spending over $10,000/month on PPC, dedicated fraud prevention platforms provide additional protection. ClickCease, Lunio (formerly PPC Protect), ClickGUARD, and CHEQ offer real-time click monitoring, automated IP blocking, bot detection algorithms, and detailed fraud reports. These tools typically cost $50-500/month but can save multiples of their cost in prevented fraud. They integrate with Google Ads to automatically add IP exclusions when fraud is detected.</p>

<h2 id="refunds">Requesting Refunds from Google</h2>
<p>If you identify click fraud that Google's automated systems did not catch, you can request a manual review. Go to Google Ads Help > Contact Us, provide evidence of the suspected fraud (IP logs, analytics data, session recordings), specify the date range and campaigns affected, and request an invalid click investigation. Google will review and issue credits for confirmed invalid clicks. Document all fraud incidents for reference.</p>`,
      cs: `<h2 id="introduction">Problem za 100 miliard dolaru</h2>
<p>Podvodna kliknuti stoji inzerenty pres 100 miliard dolaru rocne. Studie ukazuji, ze 14-20% vsech PPC kliknuti je podvodnych — za kazd 10 000 Kc utraceno na reklamy se 1 400 az 2 000 Kc spotrebuje na kliknuti, ktera se nikdy nestanou zakazniky.</p>

<h2 id="types">Typy podvodnich kliknuti</h2>
<p>Konkurencni kliknuti (konkurenti klikaji na vase reklamy), botove site (automatizovane generovani kliknuti), klikaci farmy (rucni klikani pracovniky) a podvody vydavatelu (nafukovani prijmu z reklam na Display siti).</p>

<h2 id="detection">Metody detekce</h2>
<p>Analyza reportu vyhledavacich dotazu, krizove porovnani dat analytiky s daty reklamni platformy, analyza vzorcu IP adres a analyza zaznamu relaci.</p>

<h2 id="prevention">Preventivni strategie</h2>
<p>Vylouceni IP (500 na kampan, 500 na uctu), nastaveni lokality na "Pouze pritomnost," deaktivace Search Partners, agresivni vylouceni umisteni na Display siti a planovani reklam s nizssimi nabidkami v podezrelych casovych obdobich.</p>

<h2 id="monitoring">Prubezny monitoring s Aidvertaiser</h2>
<p>Nastavte tydenni workflow pro monitoring podvodu pomoci Aidvertaiser: stahujte reporty vyhledavacich dotazu, porovnavejte kliknuti s relacemi, kontrolujte publikum s nulovym zapojenim a spravujte seznamy vylouceni IP.</p>`,
    },
    readTime: 14,
    relatedSlugs: ['ppc-master-guide', 'campaign-analysis', 'bidding-strategies'],
  },

  /* ==================================================================== */
  /*  6. Campaign Analysis & Reporting                                    */
  /* ==================================================================== */
  {
    slug: 'campaign-analysis',
    icon: 'ChartBar',
    category: 'Guide',
    title: ml(
      'PPC Campaign Analysis & Reporting Optimization',
      'Analyza a optimalizace reportingu PPC kampani',
    ),
    shortDescription: ml(
      'Transform raw campaign data into actionable insights. Learn how to analyze performance across dimensions, set up optimization cadences, interpret Quality Scores, and build reporting workflows that drive continuous improvement.',
      'Premente surova data kampani na akcni poznatky. Naucte se analyzovat vykonnost, nastavit optimalizacni kadence, interpretovat skore kvality a budovat reportovaci workflow pro neustale zlepsovani.',
    ),
    metaDescription: ml(
      'PPC campaign analysis and optimization guide. Performance analysis, Quality Score optimization, reporting cadences, and data-driven decision making for Google Ads and Meta Ads.',
      'Pruvodce analyzou a optimalizaci PPC kampani. Analyza vykonnosti, optimalizace skore kvality, reportovaci kadence a datove rozhodovani pro Google Ads a Meta Ads.',
    ),
    content: {
      en: `<h2 id="introduction">Data Without Analysis Is Just Numbers</h2>
<p>Every PPC platform generates enormous amounts of data — impressions, clicks, CTR, CPC, conversions, CPA, ROAS, Quality Score, impression share, and dozens more metrics. But data alone is not insight. The difference between advertisers who grow and those who stagnate is the ability to transform raw metrics into actionable decisions. This guide provides the frameworks, cadences, and techniques for systematic campaign analysis and optimization.</p>

<h2 id="key-metrics">The Metrics That Matter</h2>
<h3>Primary Performance Metrics</h3>
<p><strong>Click-Through Rate (CTR):</strong> The percentage of impressions that result in clicks. The 2026 Google Ads average across industries is 6.66%, up from 3.17% five years ago. CTR is your best indicator of ad relevance — if users are clicking, your message resonates. Low CTR (below industry average) usually means poor ad copy, wrong keywords, or targeting mismatch. A high CTR with low conversions means your ad promises something your landing page does not deliver.</p>
<p><strong>Cost Per Click (CPC):</strong> What you pay for each click. The 2026 average is $4.66, but this varies enormously by industry (legal services average $8.94; real estate averages $1.81). CPC is a function of Quality Score, bid amount, and competitive intensity. Improving Quality Score is the most sustainable way to reduce CPC.</p>
<p><strong>Conversion Rate:</strong> The percentage of clicks that result in a conversion. The 2026 average is 7.04%. Conversion rate is primarily a landing page metric — it tells you how well your post-click experience converts traffic into leads or sales. Low conversion rates with high CTR indicate a landing page problem, not an ad problem.</p>
<p><strong>Cost Per Acquisition (CPA):</strong> The cost to generate one conversion. This is your primary efficiency metric. CPA equals total spend divided by total conversions. Set your target CPA based on Customer Lifetime Value — typically 20-30% of CLV for sustainable growth.</p>
<p><strong>Return On Ad Spend (ROAS):</strong> Revenue generated per dollar spent, expressed as a percentage. ROAS equals revenue divided by ad spend times 100. A ROAS of 400% means you generate $4 in revenue for every $1 spent. Industry average is 200% (2:1); 400% (4:1) is considered strong.</p>

<h3>Quality Score Components</h3>
<p>Quality Score is a 1-10 scale based on three components: Expected CTR (approximately 39% weight), Ad Relevance (approximately 22% weight), and Landing Page Experience (approximately 39% weight). An above-average landing page experience correlates with 750% better conversion rate and 36% lower CPC. Monitor Quality Score weekly for your top keywords. Fix "Below Average" components before increasing bids — a high Quality Score reduces CPC at the same ad position.</p>

<h3>Impression Share Metrics</h3>
<p>Impression Share is the percentage of available impressions your ads captured. Lost impression share due to budget means your budget ran out before the day ended. Lost impression share due to rank means your Ad Rank (bid times Quality Score) was too low. If you have good CPA but low impression share due to budget, increasing budget is likely profitable. If you have low impression share due to rank, improve Quality Score or increase bids.</p>

<h2 id="analysis-framework">The Analysis Framework</h2>
<h3>Campaign-Level Analysis</h3>
<p>Start with the big picture. For each campaign, track: total spend vs budget (is the campaign fully spending?), conversion volume and CPA trend (improving or degrading?), impression share (room to grow or maxed out?), and ROAS for e-commerce campaigns. Red flags: campaigns spending less than 80% of budget (targeting too narrow or bids too low), CPA trending upward for 3+ consecutive weeks, impression share lost to rank above 40%.</p>

<h3>Ad Group Analysis</h3>
<p>Drill into ad groups within campaigns. Compare CPA across ad groups in the same campaign. Ad groups with CPA 50%+ above the campaign average need attention — the keywords or ads in that group are underperforming. Check that each ad group has at least 3 active RSAs. Verify that all ad groups have negative keywords that prevent overlap with other groups in the same campaign.</p>

<h3>Keyword Analysis</h3>
<p>Keywords are where the most granular optimization happens. For each keyword, evaluate: impression volume (is it getting enough exposure?), CTR relative to the ad group average, conversion rate, CPA relative to target, and Quality Score. Action framework: keywords with high impressions, low CTR — improve ad relevance or check match type. Keywords with high CTR, low conversions — landing page problem. Keywords with CPA above 2x target — reduce bid or pause. Keywords with CPA below target and low impression share — increase bid.</p>

<h3>Search Terms Analysis</h3>
<p>The search terms report shows the actual queries that triggered your ads. This is your richest source of optimization signals. Weekly, review search terms and: add high-performing new queries as keywords (promote them from discovery to targeted), add irrelevant queries as negative keywords, identify query themes that convert well (expand into new ad groups), and identify query themes that waste spend (tighten match types or add negatives).</p>

<h2 id="optimization-cadence">Optimization Cadence</h2>
<h3>Daily (15 minutes)</h3>
<ul>
<li>Check budget pacing — ensure campaigns are spending at expected rates</li>
<li>Verify conversion tracking is firing — any day with zero conversions should trigger investigation</li>
<li>Review any significant performance changes (clicks, conversions, CPA deviating more than 30% from average)</li>
<li>Check for ad disapprovals or policy violations</li>
</ul>

<h3>Weekly (1-2 hours)</h3>
<ul>
<li>Search terms review — add negatives, promote winning queries</li>
<li>Ad performance comparison — pause lowest-performing RSAs, test new variants</li>
<li>Bid adjustments — increase bids on high-performing keywords and segments, decrease on underperformers</li>
<li>Audience performance review — adjust bid modifiers based on segment performance</li>
<li>Device and geographic performance — apply adjustments where data warrants</li>
</ul>

<h3>Monthly (Half day)</h3>
<ul>
<li>Quality Score audit — review all keywords with Quality Score below 6, prioritize improvements</li>
<li>Landing page testing — review conversion rates by landing page, plan A/B tests</li>
<li>Audience expansion — explore new in-market and affinity segments based on conversion data</li>
<li>Competitive analysis — review competitor ads, keywords, and positioning changes</li>
<li>Budget reallocation — shift budget from underperforming campaigns to those with room to scale</li>
</ul>

<h3>Quarterly (Full day)</h3>
<ul>
<li>Account structure review — do campaigns and ad groups still reflect business priorities?</li>
<li>Bidding strategy evaluation — should any campaigns graduate to the next bidding strategy?</li>
<li>Market analysis — seasonal trends, industry changes, new competitor entries</li>
<li>Goal review — are PPC goals aligned with business objectives?</li>
</ul>

<h2 id="reporting">Building Effective Reports</h2>
<p>Effective PPC reports answer three questions: What happened? Why did it happen? What should we do next?</p>
<p><strong>What happened:</strong> Present key metrics (spend, conversions, CPA, ROAS) with trend lines. Show period-over-period comparisons (week-over-week, month-over-month). Highlight significant changes in either direction.</p>
<p><strong>Why did it happen:</strong> Attribution — which campaigns, ad groups, keywords, or audiences drove the change. External factors — seasonality, competitive changes, market shifts. Internal changes — bid adjustments, new ads, budget changes, targeting modifications.</p>
<p><strong>What should we do next:</strong> Specific, prioritized action items with expected impact. "Increase budget on Campaign X by 20% based on CPA headroom" is actionable. "Improve performance" is not.</p>

<h2 id="cross-platform">Cross-Platform Analysis with Aidvertaiser</h2>
<p>Aidvertaiser enables cross-platform analysis that is impossible when working in siloed platform dashboards. Use GAQL queries for Google Ads data, Meta insights endpoints for Meta data, GA4 and Matomo for on-site behavior, and Search Console and Bing for organic context. The AI can pull data from all sources in a single conversation, compare metrics across platforms, and generate unified insights that inform holistic marketing decisions.</p>
<p>Example cross-platform analysis: "Compare CPA across Google Ads and Meta Ads for the last 30 days, broken down by week. For the platform with higher CPA, pull the top 5 campaigns by spend and identify which ones are driving up the average." This analysis would require hours of manual work across two platforms — with Aidvertaiser, it takes one conversation.</p>`,
      cs: `<h2 id="introduction">Data bez analyzy jsou jen cisla</h2>
<p>Kazda PPC platforma generuje obrovske mnozstvi dat. Ale data sama o sobe nejsou poznatky. Rozdil mezi inzerenty, kteri rostou, a temi, co staguni, je schopnost premenovat surove metriky na akcni rozhodnuti.</p>

<h2 id="key-metrics">Metriky, na kterych zalezi</h2>
<p>CTR (prumer 2026: 6.66%), CPC (prumer: $4.66), konverzni pomer (prumer: 7.04%), CPA a ROAS. Skore kvality 1-10 na zaklade ocekavaneho CTR (39% vaha), relevance reklamy (22%) a zkusenosti s landing page (39%).</p>

<h2 id="optimization-cadence">Optimalizacni kadence</h2>
<p>Denne (15 minut): kontrola rozpoctu a konverziho sledovani. Tyden (1-2 hodiny): analyza vyhledavacich dotazu, porovnani reklam, upravy nabidek. Mesicne (pul dne): audit skore kvality, testovani landing pages, konkurencni analyza. Ctvrtletne: revize struktury uctu a strategii nabidek.</p>

<h2 id="reporting">Efektivni reporty</h2>
<p>Efektivni PPC reporty odpovidaji na tri otazky: Co se stalo? Proc se to stalo? Co bychom meli delat dal?</p>

<h2 id="cross-platform">Analyza napric platformami s Aidvertaiser</h2>
<p>Aidvertaiser umoznuje analyzu napric platformami, ktera je nemozna pri praci v oddelenych dashboardech. AI muze stahnout data ze vsech zdroju v jedinem rozhovoru a generovat sjednocene poznatky.</p>`,
    },
    readTime: 20,
    relatedSlugs: ['ppc-master-guide', 'bidding-strategies', 'audience-targeting-guide'],
  },
];
