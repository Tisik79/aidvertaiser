/* -------------------------------------------------------------------------- */
/*  Integration Data — Aidvertaiser Marketing Website                        */
/* -------------------------------------------------------------------------- */

export interface Integration {
  slug: string;
  icon: string;
  title: Record<string, string>;
  shortDescription: Record<string, string>;
  metaDescription: Record<string, string>;
  content: Record<string, string>;
  configExample: string;
  relatedSlugs: string[];
}

/* Helper: for languages we haven't translated yet, fall back to English */
function ml(en: string, cs: string): Record<string, string> {
  return { en, cs, fr: en, es: en, zh: en, hi: en, pt: en, pl: en, ar: en, bn: en };
}

export const integrations: Integration[] = [
  /* ==================================================================== */
  /*  1. Claude Desktop                                                   */
  /* ==================================================================== */
  {
    slug: 'claude-desktop',
    icon: 'Robot',
    title: ml('Claude Desktop', 'Claude Desktop'),
    shortDescription: ml(
      'Native MCP support in Claude Desktop. Add Aidvertaiser to your claude_desktop_config.json and manage all 180 advertising tools directly in Claude conversations. Zero setup beyond configuration.',
      'Nativni podpora MCP v Claude Desktop. Pridejte Aidvertaiser do vaseho claude_desktop_config.json a spravujte vsech 180 reklamnich nastroju primo v konverzacich s Claude.',
    ),
    metaDescription: ml(
      'Integrate Aidvertaiser with Claude Desktop for AI-powered advertising management. 180 MCP tools for Google Ads, Meta Ads, GA4, and more — directly in Claude conversations.',
      'Integrujte Aidvertaiser s Claude Desktop pro spravu reklam pomoci AI. 180 MCP nastroju pro Google Ads, Meta Ads, GA4 a dalsi — primo v konverzacich s Claude.',
    ),
    content: {
      en: `<h2 id="overview">Claude + Aidvertaiser: The Ideal Pairing</h2>
<p>Claude Desktop has <strong>native MCP (Model Context Protocol) support</strong>, making it the most seamless way to use Aidvertaiser. Once configured, all 180 advertising tools are available directly in your Claude conversations. No browser extensions, no API wrappers, no additional software — just Claude with full advertising platform access.</p>
<p>MCP is an open protocol developed by Anthropic that allows AI assistants to interact with external tools and data sources. Aidvertaiser implements the MCP server specification, meaning Claude can call any of its 180 tools natively. The AI understands when to use each tool based on your requests and chains multiple tools together for complex workflows.</p>

<h2 id="setup">Setup</h2>
<p>Configuration takes less than a minute. Add the Aidvertaiser server to your Claude Desktop configuration file:</p>
<ol>
<li>Open your Claude Desktop configuration file at <code>~/Library/Application Support/Claude/claude_desktop_config.json</code> (macOS) or <code>%APPDATA%\\Claude\\claude_desktop_config.json</code> (Windows)</li>
<li>Add the Aidvertaiser server entry to the <code>mcpServers</code> section</li>
<li>Restart Claude Desktop</li>
</ol>
<p>That is it. Claude will automatically discover all 180 tools and make them available in your conversations. You can verify by asking Claude: "What advertising tools do you have access to?"</p>

<h2 id="how-it-works">How It Works</h2>
<p>When you ask Claude to perform an advertising task — "Create a Google Ads Search campaign for CRM software" — Claude analyzes your request, determines which Aidvertaiser tools to call, executes them in the correct sequence, and presents the results conversationally. For complex tasks, Claude chains multiple tool calls: creating a campaign, then ad groups, then ads, then keywords, all in one conversation.</p>
<p>Claude's reasoning capabilities make it an exceptional advertising manager. It can analyze performance data, recommend optimizations, compare platforms, and execute changes — all while explaining its reasoning and asking for confirmation before making changes.</p>

<h2 id="capabilities">What You Can Do</h2>
<ul>
<li>Create and manage campaigns on Google Ads and Meta Ads through natural language</li>
<li>Pull analytics reports from GA4 and Matomo by asking questions about your data</li>
<li>Monitor search performance across Google Search Console and Bing Webmaster Tools</li>
<li>Set up conversion tracking, pixels, and server-side events through conversation</li>
<li>Research audiences, estimate reach, and configure targeting without touching an Ads Manager</li>
<li>Execute GAQL queries by describing what data you need in plain English</li>
</ul>`,
      cs: `<h2 id="overview">Claude + Aidvertaiser: Idealni kombinace</h2>
<p>Claude Desktop ma <strong>nativni podporu MCP (Model Context Protocol)</strong>, coz z nej dela nejplynulejsi zpusob pouzivani Aidvertaiser. Po konfiguraci je vsech 180 reklamnich nastroju dostupnych primo ve vasich konverzacich s Claude.</p>

<h2 id="setup">Nastaveni</h2>
<p>Konfigurace trva mene nez minutu. Pridejte Aidvertaiser server do konfiguracniho souboru Claude Desktop a restartujte Claude Desktop.</p>

<h2 id="how-it-works">Jak to funguje</h2>
<p>Kdyz pozadate Claude o reklamni ukol, Claude analyzuje vas pozadavek, urci ktere nastroje zavolat, provede je ve spravnem poradi a prezentuje vysledky konverzacne.</p>

<h2 id="capabilities">Co muzete delat</h2>
<ul>
<li>Vytvarejte a spravujte kampane na Google Ads a Meta Ads prirozenim jazykem</li>
<li>Stahujte analyticke reporty z GA4 a Matomo dotazy na svá data</li>
<li>Sledujte vykon vyhledavani napric Google Search Console a Bing</li>
<li>Nastavujte sledovani konverzi prostrednictvim konverzace</li>
</ul>`,
    },
    configExample: `{
  "mcpServers": {
    "aidvertaiser": {
      "command": "uvx",
      "args": ["unified-ads-mcp"],
      "env": {
        "META_APP_ID": "your_meta_app_id",
        "META_APP_SECRET": "your_meta_app_secret"
      }
    }
  }
}`,
    relatedSlugs: ['cursor-ide', 'vscode-continue', 'windsurf'],
  },

  /* ==================================================================== */
  /*  2. Cursor IDE                                                       */
  /* ==================================================================== */
  {
    slug: 'cursor-ide',
    icon: 'CursorClick',
    title: ml('Cursor IDE', 'Cursor IDE'),
    shortDescription: ml(
      'Use Aidvertaiser directly in Cursor IDE through its built-in MCP support. Manage advertising campaigns and analytics alongside your code, perfect for marketing developers and growth engineers.',
      'Pouzivejte Aidvertaiser primo v Cursor IDE diky vestavene podpore MCP. Spravujte reklamni kampane a analytiku vedle sveho kodu, idealni pro marketingove vyvojare.',
    ),
    metaDescription: ml(
      'Integrate Aidvertaiser with Cursor IDE for advertising management alongside code. 180 MCP tools for Google Ads, Meta Ads, and analytics in your development environment.',
      'Integrujte Aidvertaiser s Cursor IDE pro spravu reklam vedle kodu. 180 MCP nastroju pro Google Ads, Meta Ads a analytiku ve vasem vyvojovem prostredi.',
    ),
    content: {
      en: `<h2 id="overview">Advertising Meets Development</h2>
<p>Cursor IDE includes <strong>built-in MCP support</strong>, allowing you to access all 180 Aidvertaiser tools directly in your development environment. This is particularly powerful for growth engineers, marketing developers, and technical marketers who work with both code and advertising platforms daily.</p>
<p>Imagine writing a landing page component and simultaneously checking its Google Ads Quality Score, or building a conversion tracking integration while verifying the pixel fires correctly through Aidvertaiser. The boundary between development and marketing dissolves when both are accessible in the same interface.</p>

<h2 id="setup">Setup</h2>
<p>Configure Aidvertaiser in Cursor's MCP settings:</p>
<ol>
<li>Open Cursor Settings (Cmd+, on macOS, Ctrl+, on Windows)</li>
<li>Navigate to the MCP section</li>
<li>Add a new MCP server with the Aidvertaiser configuration</li>
<li>Restart Cursor</li>
</ol>
<p>Once configured, Aidvertaiser tools are available in Cursor's AI chat and inline editing features. Ask the AI assistant to manage campaigns, pull analytics, or check search performance — all without leaving your editor.</p>

<h2 id="use-cases">Developer-Focused Use Cases</h2>
<ul>
<li><strong>Conversion tracking implementation</strong> — Set up conversion actions in Google Ads while writing the GTM tag code</li>
<li><strong>Analytics integration</strong> — Create GA4 data streams and events while building the tracking code</li>
<li><strong>Landing page optimization</strong> — Check ad campaign performance data while developing landing page components</li>
<li><strong>API development</strong> — Build advertising automation scripts with real-time access to ad platform data</li>
<li><strong>Pixel debugging</strong> — Manage Meta Pixels and verify event configurations alongside your tracking code</li>
</ul>`,
      cs: `<h2 id="overview">Reklama potka vyvoj</h2>
<p>Cursor IDE obsahuje <strong>vestavenu podporu MCP</strong>, coz vam umoznuje pristup ke vsem 180 nastrojum Aidvertaiser primo ve vasem vyvojovem prostredi. Idealni pro growth engineery a technicke marketery.</p>

<h2 id="setup">Nastaveni</h2>
<p>Konfigurujte Aidvertaiser v nastaveni MCP v Cursoru. Otevrte nastaveni, prejdete do sekce MCP, pridejte novy MCP server a restartujte Cursor.</p>

<h2 id="use-cases">Pripadove uziti pro vyvojare</h2>
<ul>
<li><strong>Implementace sledovani konverzi</strong> — Nastavte konverzni akce zatimco pisete sledovaci kod</li>
<li><strong>Integrace analytiky</strong> — Vytvarejte GA4 datove proudy pri budovani sledovaciho kodu</li>
<li><strong>Optimalizace landing pages</strong> — Kontrolujte vykonnost kampani pri vyvoji komponent</li>
</ul>`,
    },
    configExample: `{
  "mcpServers": {
    "aidvertaiser": {
      "command": "uvx",
      "args": ["unified-ads-mcp"],
      "env": {
        "META_APP_ID": "your_meta_app_id",
        "META_APP_SECRET": "your_meta_app_secret"
      }
    }
  }
}`,
    relatedSlugs: ['claude-desktop', 'vscode-continue', 'windsurf'],
  },

  /* ==================================================================== */
  /*  3. VS Code + Continue                                               */
  /* ==================================================================== */
  {
    slug: 'vscode-continue',
    icon: 'Code',
    title: ml('VS Code + Continue', 'VS Code + Continue'),
    shortDescription: ml(
      'Access Aidvertaiser through the Continue extension in VS Code. Open-source AI assistant with MCP support, bringing 180 advertising tools to the most popular code editor in the world.',
      'Pristupujte k Aidvertaiser pres rozsireni Continue ve VS Code. Open-source AI asistent s podporou MCP, prinasejici 180 reklamnich nastroju do nejpopularnejsiho editoru kodu na svete.',
    ),
    metaDescription: ml(
      'Use Aidvertaiser in VS Code with the Continue extension. Open-source AI assistant with MCP support for 180 advertising management tools in your editor.',
      'Pouzivejte Aidvertaiser ve VS Code s rozsirenim Continue. Open-source AI asistent s podporou MCP pro 180 reklamnich nastroju ve vasem editoru.',
    ),
    content: {
      en: `<h2 id="overview">The Open-Source Path</h2>
<p><a href="https://continue.dev">Continue</a> is an open-source AI assistant for VS Code and JetBrains that supports the MCP protocol. By connecting Aidvertaiser to Continue, you bring all 180 advertising tools into <strong>the world's most popular code editor</strong> — VS Code has over 15 million monthly active users.</p>
<p>Continue's open-source nature means you can inspect exactly how the AI interacts with Aidvertaiser, customize the behavior, and contribute improvements. It supports multiple AI backends including Claude, GPT-4, and local models, giving you flexibility in choosing the AI that powers your advertising workflows.</p>

<h2 id="setup">Setup</h2>
<ol>
<li>Install the <a href="https://marketplace.visualstudio.com/items?itemName=Continue.continue">Continue extension</a> from the VS Code marketplace</li>
<li>Open Continue's configuration file at <code>~/.continue/config.json</code></li>
<li>Add the Aidvertaiser MCP server to the <code>mcpServers</code> section</li>
<li>Reload VS Code</li>
</ol>
<p>Continue will discover all 180 Aidvertaiser tools and make them available in the sidebar chat and inline editing features.</p>

<h2 id="benefits">Benefits of VS Code Integration</h2>
<ul>
<li><strong>Familiar environment</strong> — Work with advertising tools in the editor you already use every day</li>
<li><strong>Open source</strong> — Full transparency into how AI uses your advertising data</li>
<li><strong>Multi-model support</strong> — Choose Claude, GPT-4, Gemini, or local models to power your workflows</li>
<li><strong>Extension ecosystem</strong> — Combine with other VS Code extensions for enhanced workflows</li>
<li><strong>Free to use</strong> — Continue is free and open source; bring your own AI API key</li>
</ul>`,
      cs: `<h2 id="overview">Open-source cesta</h2>
<p><a href="https://continue.dev">Continue</a> je open-source AI asistent pro VS Code, ktery podporuje protokol MCP. Pripojenim Aidvertaiser ke Continue prinesete vsech 180 reklamnich nastroju do <strong>nejpopularnejsiho editoru kodu na svete</strong>.</p>

<h2 id="setup">Nastaveni</h2>
<ol>
<li>Nainstalujte rozsireni Continue z VS Code marketplace</li>
<li>Otevrte konfiguracni soubor Continue na <code>~/.continue/config.json</code></li>
<li>Pridejte Aidvertaiser MCP server do sekce <code>mcpServers</code></li>
<li>Znovu nactete VS Code</li>
</ol>

<h2 id="benefits">Vyhody integrace VS Code</h2>
<ul>
<li><strong>Znme prostredi</strong> — Pracujte s reklamnimi nastroji v editoru, ktery pouzivate kazdy den</li>
<li><strong>Open source</strong> — Plna transparentnost</li>
<li><strong>Podpora vice modelu</strong> — Vyberete si Claude, GPT-4 nebo lokalni modely</li>
</ul>`,
    },
    configExample: `{
  "mcpServers": [
    {
      "name": "aidvertaiser",
      "command": "uvx",
      "args": ["unified-ads-mcp"],
      "env": {
        "META_APP_ID": "your_meta_app_id",
        "META_APP_SECRET": "your_meta_app_secret"
      }
    }
  ]
}`,
    relatedSlugs: ['claude-desktop', 'cursor-ide', 'cline'],
  },

  /* ==================================================================== */
  /*  4. Windsurf                                                         */
  /* ==================================================================== */
  {
    slug: 'windsurf',
    icon: 'Wind',
    title: ml('Windsurf', 'Windsurf'),
    shortDescription: ml(
      'Integrate Aidvertaiser with Windsurf IDE for agentic advertising workflows. Windsurf\'s Cascade AI can autonomously manage campaigns, pull reports, and optimize targeting using all 180 MCP tools.',
      'Integrujte Aidvertaiser s Windsurf IDE pro agentni reklamni workflow. Cascade AI ve Windsurf muze autonomne spravovat kampane, stahovat reporty a optimalizovat cileni.',
    ),
    metaDescription: ml(
      'Connect Aidvertaiser to Windsurf IDE for agentic advertising management. Cascade AI uses 180 MCP tools to autonomously manage campaigns, analytics, and SEO.',
      'Pripojte Aidvertaiser k Windsurf IDE pro agentni spravu reklam. Cascade AI pouziva 180 MCP nastroju pro autonomni spravu kampani, analytiky a SEO.',
    ),
    content: {
      en: `<h2 id="overview">Agentic Advertising with Windsurf</h2>
<p>Windsurf is an AI-native IDE built by Codeium that features <strong>Cascade</strong>, an agentic AI that can autonomously execute multi-step tasks. When connected to Aidvertaiser through MCP, Cascade can independently manage advertising campaigns, pull performance reports, optimize targeting, and execute complex marketing workflows — with minimal human intervention.</p>
<p>This makes Windsurf + Aidvertaiser particularly powerful for repetitive advertising tasks. Set up a weekly performance review workflow, and Cascade executes it autonomously: pulling data from all six platforms, analyzing trends, identifying underperformers, and recommending (or executing) optimizations.</p>

<h2 id="setup">Setup</h2>
<p>Add Aidvertaiser to Windsurf's MCP configuration:</p>
<ol>
<li>Open Windsurf Settings</li>
<li>Navigate to the MCP Servers section</li>
<li>Add the Aidvertaiser server configuration</li>
<li>Restart Windsurf</li>
</ol>
<p>Cascade will automatically discover all 180 tools and incorporate them into its agentic capabilities.</p>

<h2 id="agentic-workflows">Agentic Workflow Examples</h2>
<ul>
<li><strong>Automated weekly reports</strong> — "Every Monday, pull performance data from Google Ads, Meta Ads, and GA4, compare week-over-week, and summarize key changes"</li>
<li><strong>Campaign optimization</strong> — "Review all active campaigns, pause any with CPA above $50 and no conversions in the last 7 days, and reallocate their budget to top performers"</li>
<li><strong>Search monitoring</strong> — "Check Google Search Console for any new crawl errors and submit sitemaps if any pages are missing from the index"</li>
<li><strong>Keyword management</strong> — "Pull the search terms report from Google Ads, add any irrelevant terms as negative keywords, and add any high-converting new terms as exact match keywords"</li>
</ul>`,
      cs: `<h2 id="overview">Agentni reklama s Windsurf</h2>
<p>Windsurf je AI-nativni IDE od Codeium s funkci <strong>Cascade</strong>, agentnim AI, ktery muze autonomne provadet vicekrokove ukoly. Po pripojeni k Aidvertaiser pres MCP muze Cascade nezavisle spravovat reklamni kampane a provadet komplexni marketingove workflow.</p>

<h2 id="setup">Nastaveni</h2>
<p>Pridejte Aidvertaiser do konfigurace MCP ve Windsurf, prejdete do sekce MCP Servers a restartujte Windsurf.</p>

<h2 id="agentic-workflows">Priklady agentnich workflow</h2>
<ul>
<li><strong>Automatizovane tydení reporty</strong> — Stahování dat z Google Ads, Meta Ads a GA4 a porovnani tyden po tydnu</li>
<li><strong>Optimalizace kampani</strong> — Pozastaveni kampani s vysokou CPA a prerozdeleni jejich rozpoctu</li>
<li><strong>Monitoring vyhledavani</strong> — Kontrola chyb prochazeni a odeslani sitemap</li>
</ul>`,
    },
    configExample: `{
  "mcpServers": {
    "aidvertaiser": {
      "command": "uvx",
      "args": ["unified-ads-mcp"],
      "env": {
        "META_APP_ID": "your_meta_app_id",
        "META_APP_SECRET": "your_meta_app_secret"
      }
    }
  }
}`,
    relatedSlugs: ['claude-desktop', 'cursor-ide', 'cline'],
  },

  /* ==================================================================== */
  /*  5. Cline                                                            */
  /* ==================================================================== */
  {
    slug: 'cline',
    icon: 'Terminal',
    title: ml('Cline', 'Cline'),
    shortDescription: ml(
      'Use Aidvertaiser with Cline, the autonomous coding agent for VS Code. Cline\'s agentic approach to MCP tools makes it ideal for complex, multi-step advertising automation tasks.',
      'Pouzivejte Aidvertaiser s Cline, autonomnim kodovacim agentem pro VS Code. Agentni pristup Cline k MCP nastrojum je idealni pro komplexni vicekrokove automatizacni ukoly.',
    ),
    metaDescription: ml(
      'Integrate Aidvertaiser with Cline autonomous agent. Complex advertising automation, multi-step campaign management, and agentic workflows through MCP in VS Code.',
      'Integrujte Aidvertaiser s autonomnim agentem Cline. Komplexni automatizace reklam a agentni workflow pres MCP ve VS Code.',
    ),
    content: {
      en: `<h2 id="overview">Autonomous Advertising Agent</h2>
<p>Cline is an <strong>autonomous AI agent</strong> that runs inside VS Code. Unlike simple chatbots, Cline can plan and execute multi-step tasks independently — making it exceptionally well-suited for complex advertising workflows that span multiple tools and platforms.</p>
<p>When connected to Aidvertaiser through MCP, Cline can autonomously create entire campaign structures, set up conversion tracking across platforms, run comprehensive performance audits, and execute optimization recommendations. It plans the sequence of tool calls, handles errors, and adapts its approach based on results.</p>

<h2 id="setup">Setup</h2>
<ol>
<li>Install Cline from the VS Code marketplace</li>
<li>Open Cline's MCP settings</li>
<li>Add the Aidvertaiser server configuration</li>
<li>Start a new Cline task</li>
</ol>
<p>Cline will discover all 180 Aidvertaiser tools and use them autonomously when executing advertising tasks.</p>

<h2 id="autonomous-tasks">Autonomous Task Examples</h2>
<ul>
<li><strong>Full campaign build-out</strong> — "Set up a complete Google Ads campaign for our SaaS product: create the campaign, build 5 ad groups by feature, add keywords for each group, create RSAs, set up conversion tracking, and configure negative keywords"</li>
<li><strong>Performance audit</strong> — "Audit all our Google Ads campaigns: identify campaigns with CPA above target, keywords with low Quality Score, ad groups with fewer than 3 ads, and missing conversion tracking"</li>
<li><strong>Cross-platform setup</strong> — "Set up tracking for our new landing page: create a GA4 data stream, configure a Meta Pixel, create conversion actions on Google Ads, and verify everything is connected"</li>
</ul>

<h2 id="safety">Safety and Control</h2>
<p>Cline asks for confirmation before executing actions that modify your advertising accounts. You maintain full control over what changes are applied. Review Cline's plan before it creates campaigns, adjusts budgets, or modifies targeting. This human-in-the-loop approach ensures autonomous efficiency without uncontrolled spending.</p>`,
      cs: `<h2 id="overview">Autonomni reklamni agent</h2>
<p>Cline je <strong>autonomni AI agent</strong> bezici uvnitr VS Code. Na rozdil od jednoduchych chatbotu muze Cline planovat a provadet vicekrokove ukoly nezavisle — vyjimecne vhodny pro komplexni reklamni workflow.</p>

<h2 id="setup">Nastaveni</h2>
<p>Nainstalujte Cline z VS Code marketplace, otevrte nastaveni MCP, pridejte konfiguraci serveru Aidvertaiser a spuste novy ukol.</p>

<h2 id="autonomous-tasks">Priklady autonomnich ukolu</h2>
<ul>
<li><strong>Kompletni stavba kampane</strong> — Vytvoreni kampane, reklamnich skupin, klicovych slov, reklam a konverzniho sledovani</li>
<li><strong>Audit vykonnosti</strong> — Identifikace kampani s vysokou CPA, klicovych slov s nizkym skore kvality a chybejiciho sledovani</li>
</ul>`,
    },
    configExample: `{
  "mcpServers": {
    "aidvertaiser": {
      "command": "uvx",
      "args": ["unified-ads-mcp"],
      "env": {
        "META_APP_ID": "your_meta_app_id",
        "META_APP_SECRET": "your_meta_app_secret"
      }
    }
  }
}`,
    relatedSlugs: ['vscode-continue', 'claude-desktop', 'custom-apps'],
  },

  /* ==================================================================== */
  /*  6. Custom Applications                                              */
  /* ==================================================================== */
  {
    slug: 'custom-apps',
    icon: 'Wrench',
    title: ml('Custom Applications', 'Vlastni aplikace'),
    shortDescription: ml(
      'Build custom advertising automation with the MCP SDK. Connect Aidvertaiser to your own applications, dashboards, and workflows using the standardized MCP protocol for 180 advertising tools.',
      'Vytvarejte vlastni automatizaci reklam s MCP SDK. Pripojte Aidvertaiser ke svym vlastnim aplikacim, dashboardum a workflow pomoci standardizovaneho protokolu MCP.',
    ),
    metaDescription: ml(
      'Build custom advertising automation with Aidvertaiser MCP SDK. Connect 180 advertising tools to your applications, dashboards, and workflows through the MCP protocol.',
      'Vytvarte vlastni automatizaci reklam s Aidvertaiser MCP SDK. Pripojte 180 reklamnich nastroju k vasim aplikacim pres protokol MCP.',
    ),
    content: {
      en: `<h2 id="overview">Build Your Own Advertising Platform</h2>
<p>Aidvertaiser is not limited to pre-built integrations. The <strong>MCP protocol</strong> is an open standard with SDKs available in Python, TypeScript, and other languages. You can build custom applications that connect to Aidvertaiser and use any of its 180 tools programmatically.</p>
<p>This opens the door to custom advertising dashboards, automated reporting systems, proprietary optimization algorithms, and any other advertising workflow you can imagine. The MCP protocol handles the communication layer — you focus on your business logic.</p>

<h2 id="use-cases">Custom Application Use Cases</h2>
<h3>Internal Dashboards</h3>
<p>Build a custom advertising dashboard that pulls data from all six platforms through Aidvertaiser. Display campaign performance, analytics metrics, search rankings, and conversion data in a single unified interface tailored to your team's needs. No third-party dashboard subscription required.</p>

<h3>Automated Reporting</h3>
<p>Create scheduled reporting scripts that connect to Aidvertaiser, pull performance data from all platforms, generate formatted reports, and distribute them to stakeholders. Automate your weekly and monthly reporting workflows completely.</p>

<h3>Optimization Engines</h3>
<p>Build custom bidding and budget optimization algorithms that use Aidvertaiser to read performance data and apply changes. Implement proprietary optimization logic that goes beyond what Google and Meta's built-in algorithms offer. Test hypotheses, backtest strategies, and deploy custom automation.</p>

<h3>Multi-Client Management</h3>
<p>Agencies can build client management portals that use Aidvertaiser to manage campaigns across multiple client accounts. White-label the interface, add custom approval workflows, and integrate with your existing client management systems.</p>

<h2 id="getting-started">Getting Started</h2>
<p>The MCP SDK is available on PyPI and npm. Start by installing the SDK, connecting to the Aidvertaiser server, and listing available tools:</p>

<h3>Python</h3>
<pre><code>from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="uvx",
    args=["unified-ads-mcp"],
    env={"META_APP_ID": "...", "META_APP_SECRET": "..."}
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        # Use any of the 180 tools programmatically</code></pre>

<h3>TypeScript</h3>
<pre><code>import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "uvx",
  args: ["unified-ads-mcp"],
  env: { META_APP_ID: "...", META_APP_SECRET: "..." }
});

const client = new Client({ name: "my-app", version: "1.0.0" });
await client.connect(transport);
const tools = await client.listTools();
// Use any of the 180 tools programmatically</code></pre>

<h2 id="protocol">The MCP Protocol</h2>
<p>MCP (Model Context Protocol) is an open protocol developed by Anthropic that standardizes how applications communicate with AI tool servers. It uses JSON-RPC 2.0 over stdio or HTTP, supports tool discovery, and provides a consistent interface for calling tools and receiving results. Learn more at <a href="https://modelcontextprotocol.io">modelcontextprotocol.io</a>.</p>`,
      cs: `<h2 id="overview">Vytvorte si vlastni reklamni platformu</h2>
<p>Aidvertaiser neni omezen na predpripravene integrace. <strong>Protokol MCP</strong> je otevreny standard se SDK dostupnymi v Pythonu, TypeScriptu a dalsich jazycich. Muzete vytvaret vlastni aplikace pripojene k Aidvertaiser.</p>

<h2 id="use-cases">Pripadove uziti vlastnich aplikaci</h2>
<h3>Interni dashboardy</h3>
<p>Vytvarte vlastni reklamni dashboard stahujici data ze vsech sesti platforem pres Aidvertaiser.</p>

<h3>Automatizovany reporting</h3>
<p>Vytvarte planovane reportovaci skripty pripojene k Aidvertaiser pro automatizaci tydenich a mesicnich reportu.</p>

<h3>Optimalizacni enginy</h3>
<p>Vytvarte vlastni algoritmy pro nabidky a rozpocty pouzivajici Aidvertaiser pro cteni dat o vykonnosti a aplikovani zmen.</p>

<h2 id="getting-started">Jak zacit</h2>
<p>MCP SDK je dostupne na PyPI a npm. Nainstalujte SDK, pripojte se k serveru Aidvertaiser a vypisujte dostupne nastroje.</p>`,
    },
    configExample: `# Python: pip install mcp
# TypeScript: npm install @modelcontextprotocol/sdk

# Server command for programmatic access:
# uvx unified-ads-mcp

# Or run directly with Python:
# uv run unified-ads-mcp`,
    relatedSlugs: ['claude-desktop', 'cline', 'cursor-ide'],
  },
];
