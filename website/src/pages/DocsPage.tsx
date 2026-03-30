import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { Copy, Check, Terminal, GearSix, Code, BookOpen, ArrowRight, GithubLogo, Key, Plugs } from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import { platforms } from '@/content/platforms';
import { SITE_URL, buildGraphJsonLd, webPageEntity } from '@/content/seo-schema';

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => { try { await navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); } catch { /* */ } };
  return (
    <button onClick={handleCopy} className="p-1.5 rounded-md hover:bg-white/10 transition-colors" aria-label="Copy to clipboard">
      {copied ? <Check size={14} className="text-emerald-400" weight="bold" /> : <Copy size={14} className="text-zinc-500" />}
    </button>
  );
}

function CodeBlock({ code, language }: { code: string; language?: string }) {
  return (
    <div className="relative rounded-xl bg-zinc-900 dark:bg-zinc-950 border border-zinc-800 dark:border-zinc-800/60 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800 dark:border-zinc-800/60">
        <span className="text-xs text-zinc-500 font-mono">{language || 'shell'}</span>
        <CopyButton text={code} />
      </div>
      <pre className="p-4 overflow-x-auto text-sm font-mono text-zinc-300 leading-relaxed"><code>{code}</code></pre>
    </div>
  );
}

function SectionHeading({ id, icon: Icon, children }: { id: string; icon: React.ElementType; children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-3 mb-6">
      <div className="inline-flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex-shrink-0"><Icon size={22} weight="duotone" /></div>
      <h2 id={id} className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{children}</h2>
    </div>
  );
}

const MCP_CONFIG = `{
  "mcpServers": {
    "aidvertaiser": {
      "command": "unified-ads-mcp",
      "args": ["--config", "config.yaml"]
    }
  }
}`;

const YAML_CONFIG = `# config.yaml
google_ads:
  developer_token: "YOUR_DEV_TOKEN"
  client_id: "YOUR_CLIENT_ID"
  client_secret: "YOUR_CLIENT_SECRET"
  refresh_token: "YOUR_REFRESH_TOKEN"
  customer_id: "123-456-7890"

meta_ads:
  access_token: "YOUR_ACCESS_TOKEN"
  app_id: "YOUR_APP_ID"
  app_secret: "YOUR_APP_SECRET"
  ad_account_id: "act_123456789"

google_analytics:
  credentials_path: "ga4-credentials.json"
  property_id: "properties/123456789"

matomo:
  url: "https://analytics.example.com"
  token: "YOUR_API_TOKEN"
  site_id: 1`;

export default function DocsPage() {
  const { t } = useTranslation();
  const breadcrumbItems = [{ label: t('docs.title', 'Documentation') }];
  const graphJsonLd = buildGraphJsonLd([webPageEntity(`${SITE_URL}/docs`, 'Aidvertaiser Documentation', 'Complete documentation for Aidvertaiser: installation, platform configuration, MCP setup, and tool reference for all 180 advertising tools.')]);

  return (
    <>
      <SEO title={t('docs.meta.title', 'Documentation - Aidvertaiser')} description={t('docs.meta.description', 'Complete documentation for Aidvertaiser: installation, platform configuration, MCP setup, and tool reference for all 180 advertising tools across 6 platforms.')} canonical={`${SITE_URL}/docs`} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: 'Documentation', url: `${SITE_URL}/docs` }]} jsonLd={graphJsonLd} />

      {/* Hero */}
      <section className="relative py-16 md:py-24 overflow-hidden">
        <div className="absolute inset-0 pointer-events-none" aria-hidden="true"><div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-r from-indigo-500/15 via-purple-500/10 to-pink-500/15 blur-[120px] rounded-full" /></div>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="mb-8"><Breadcrumbs items={breadcrumbItems} /></motion.div>
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold tracking-tighter text-zinc-900 dark:text-white">{t('docs.title', 'Documentation')}</h1>
            <p className="mt-4 text-lg md:text-xl text-zinc-600 dark:text-zinc-400 max-w-2xl leading-relaxed">{t('docs.subtitle', 'Everything you need to install, configure, and use Aidvertaiser. From quick start to advanced platform configuration, this guide covers the entire workflow.')}</p>
          </motion.div>
          <motion.nav initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.15 }} className="mt-10 p-5 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] backdrop-blur-xl" aria-label="Table of contents">
            <h2 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 uppercase tracking-wider">{t('docs.toc', 'On this page')}</h2>
            <ul className="space-y-2 text-sm">
              {[{ id: 'quick-start', label: t('docs.quickStart.title', 'Quick Start') }, { id: 'platform-setup', label: t('docs.platformSetup.title', 'Platform Setup') }, { id: 'configuration', label: t('docs.configuration.title', 'Configuration') }, { id: 'authentication', label: t('docs.authentication.title', 'Authentication') }, { id: 'tool-reference', label: t('docs.toolReference.title', 'Tool Reference') }].map((item) => (
                <li key={item.id}><a href={`#${item.id}`} className="text-zinc-500 hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors">{item.label}</a></li>
              ))}
            </ul>
          </motion.nav>
        </div>
      </section>

      {/* Content Sections */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-20 md:pb-32 space-y-20 md:space-y-28">
        {/* Quick Start */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }} aria-labelledby="quick-start">
          <SectionHeading id="quick-start" icon={Terminal}>{t('docs.quickStart.title', 'Quick Start')}</SectionHeading>
          <div className="space-y-5">
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('docs.quickStart.intro', 'Get Aidvertaiser running in three steps. The package installs from PyPI and requires Python 3.12 or later.')}</p>
            <h3 className="text-lg font-display font-semibold text-zinc-900 dark:text-white mt-8 mb-3">1. Install Aidvertaiser</h3>
            <CodeBlock code="pip install unified-ads-mcp" />
            <h3 className="text-lg font-display font-semibold text-zinc-900 dark:text-white mt-8 mb-3">2. Configure Platform Credentials</h3>
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">Create a <code className="text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded text-sm">config.yaml</code> file with your platform credentials.</p>
            <CodeBlock code={YAML_CONFIG} language="yaml" />
            <h3 className="text-lg font-display font-semibold text-zinc-900 dark:text-white mt-8 mb-3">3. Connect to Your AI Assistant</h3>
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">Add Aidvertaiser to your MCP client configuration (Claude Desktop, VS Code, etc.).</p>
            <CodeBlock code={MCP_CONFIG} language="json" />
          </div>
        </motion.section>

        {/* Platform Setup */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }} aria-labelledby="platform-setup">
          <SectionHeading id="platform-setup" icon={Plugs}>{t('docs.platformSetup.title', 'Platform Setup')}</SectionHeading>
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-8">Each platform requires its own credentials. Click a platform below to see detailed setup instructions.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {platforms.map((p) => (
              <Link key={p.slug} to={`/platforms/${p.slug}`} className="flex items-center gap-3 p-4 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] hover:border-indigo-500/20 dark:hover:border-indigo-500/20 transition-colors group">
                <div className="w-8 h-8 rounded-lg bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center text-indigo-600 dark:text-indigo-400 text-lg">{p.icon}</div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-zinc-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{p.title.en}</p>
                  <p className="text-xs text-zinc-500">{p.toolCount} tools</p>
                </div>
                <ArrowRight size={14} className="text-zinc-400 group-hover:text-indigo-500 transition-colors" />
              </Link>
            ))}
          </div>
        </motion.section>

        {/* Configuration */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }} aria-labelledby="configuration">
          <SectionHeading id="configuration" icon={GearSix}>{t('docs.configuration.title', 'Configuration')}</SectionHeading>
          <div className="space-y-5">
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">Aidvertaiser uses a YAML configuration file to store platform credentials. You can also set credentials via environment variables.</p>
            <h3 className="text-lg font-display font-semibold text-zinc-900 dark:text-white mt-8 mb-3">Environment Variables</h3>
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">Every YAML key can be overridden with an environment variable using the pattern <code className="text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded text-sm">AIDVERTAISER_&lt;PLATFORM&gt;_&lt;KEY&gt;</code>.</p>
            <CodeBlock code={`# Google Ads via environment variables
export AIDVERTAISER_GOOGLE_ADS_DEVELOPER_TOKEN="YOUR_DEV_TOKEN"
export AIDVERTAISER_GOOGLE_ADS_CLIENT_ID="YOUR_CLIENT_ID"
export AIDVERTAISER_GOOGLE_ADS_CUSTOMER_ID="123-456-7890"

# Meta Ads
export AIDVERTAISER_META_ADS_ACCESS_TOKEN="YOUR_TOKEN"
export AIDVERTAISER_META_ADS_AD_ACCOUNT_ID="act_123456789"

# Then start without a config file
unified-ads-mcp`} language="shell" />
          </div>
        </motion.section>

        {/* Authentication */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }} aria-labelledby="authentication">
          <SectionHeading id="authentication" icon={Key}>{t('docs.authentication.title', 'Authentication')}</SectionHeading>
          <div className="space-y-5">
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">Different platforms use different authentication methods. Here is a summary.</p>
            <div className="space-y-4">
              {[
                { platform: 'Google Ads', method: 'OAuth 2.0', desc: 'Requires developer token, client ID/secret, and refresh token from Google Ads API console.' },
                { platform: 'Meta Ads', method: 'Access Token', desc: 'Long-lived access token from Meta for Developers. System user tokens recommended for production.' },
                { platform: 'GA4', method: 'Service Account', desc: 'JSON credentials file from Google Cloud console with Google Analytics Data API enabled.' },
                { platform: 'Search Console', method: 'Service Account', desc: 'Same Google Cloud service account with Search Console API enabled.' },
                { platform: 'Matomo', method: 'API Token', desc: 'Token auth from Matomo Settings > API. Works with both cloud and self-hosted.' },
                { platform: 'Bing Webmaster', method: 'API Key', desc: 'API key from Bing Webmaster Tools settings page.' },
              ].map(({ platform, method, desc }) => (
                <div key={platform} className="flex items-start gap-3 rounded-lg border border-zinc-200/30 dark:border-white/5 bg-white/30 dark:bg-white/[0.01] p-4">
                  <div className="flex-shrink-0"><span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">{method}</span></div>
                  <div><p className="text-sm font-medium text-zinc-900 dark:text-white">{platform}</p><p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mt-1">{desc}</p></div>
                </div>
              ))}
            </div>
          </div>
        </motion.section>

        {/* Tool Reference */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }} aria-labelledby="tool-reference">
          <SectionHeading id="tool-reference" icon={Code}>{t('docs.toolReference.title', 'Tool Reference')}</SectionHeading>
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-8">Aidvertaiser provides 180 tools organized by platform. Here is the breakdown.</p>
          <div className="rounded-xl border border-zinc-200/50 dark:border-white/5 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="bg-zinc-100/80 dark:bg-white/[0.03] border-b border-zinc-200/50 dark:border-white/5">
                  <th className="text-left px-5 py-3 font-display font-semibold text-zinc-900 dark:text-white">Platform</th>
                  <th className="text-left px-5 py-3 font-display font-semibold text-zinc-900 dark:text-white">Tools</th>
                  <th className="text-left px-5 py-3 font-display font-semibold text-zinc-900 dark:text-white hidden md:table-cell">Auth</th>
                </tr></thead>
                <tbody className="divide-y divide-zinc-200/30 dark:divide-white/5">
                  {platforms.map((p) => (
                    <tr key={p.slug} className="hover:bg-zinc-50/50 dark:hover:bg-white/[0.01] transition-colors">
                      <td className="px-5 py-3.5"><Link to={`/platforms/${p.slug}`} className="font-medium text-zinc-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">{p.title.en}</Link></td>
                      <td className="px-5 py-3.5"><span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">{p.toolCount}</span></td>
                      <td className="px-5 py-3.5 text-zinc-600 dark:text-zinc-400 hidden md:table-cell text-xs">{p.authMethod}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <p className="mt-4 text-sm text-zinc-500 dark:text-zinc-500">Click any platform to see the complete list of tools and their documentation.</p>
        </motion.section>

        {/* CTA */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }} className="rounded-2xl bg-zinc-900 dark:bg-zinc-950 border border-zinc-800 dark:border-zinc-800/60 p-8 md:p-12 text-center relative overflow-hidden">
          <div className="absolute inset-0 pointer-events-none" aria-hidden="true"><div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[200px] bg-gradient-to-r from-indigo-500/20 via-purple-500/15 to-pink-500/20 blur-[100px] rounded-full" /></div>
          <div className="relative z-10">
            <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-white">{t('docs.cta.title', 'Explore the Full Source')}</h2>
            <p className="mt-3 text-zinc-400 max-w-md mx-auto leading-relaxed">{t('docs.cta.description', 'Aidvertaiser is open source under the MIT License. Browse the source code, report issues, and contribute on GitHub.')}</p>
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
              <a href="https://github.com/Draivix/aidvertaiser" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full bg-white text-black text-sm font-semibold hover:scale-105 active:scale-[0.98] transition-transform"><GithubLogo size={18} weight="bold" /> {t('docs.cta.github', 'View on GitHub')}</a>
              <Link to="/resources" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full border border-zinc-700 text-zinc-300 text-sm font-semibold hover:bg-white/5 transition-colors"><BookOpen size={16} weight="bold" /> Resources <ArrowRight size={14} weight="bold" /></Link>
            </div>
          </div>
        </motion.section>
      </div>
    </>
  );
}
