import { useMemo, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { motion } from 'motion/react';
import { animate, stagger } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import { ArrowRight, ArrowLeft, CheckCircle, WarningCircle } from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import { platforms } from '@/content/platforms';
import type { Platform } from '@/content/platforms';
import { SITE_URL, buildGraphJsonLd, webPageEntity } from '@/content/seo-schema';

interface TocEntry { id: string; text: string; level: number; }

function extractToc(html: string): TocEntry[] {
  const entries: TocEntry[] = [];
  const regex = /<h([2-3])\s+id="([^"]+)"[^>]*>(.*?)<\/h[2-3]>/g;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(html)) !== null) entries.push({ level: parseInt(match[1], 10), id: match[2], text: match[3].replace(/<[^>]+>/g, '') });
  return entries;
}

function RelatedPlatformCard({ platform }: { platform: Platform }) {
  const { i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  return (
    <Link to={`/platforms/${platform.slug}`} className="group relative flex flex-col rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] backdrop-blur-xl p-6 overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/5 hover:border-indigo-500/20 dark:hover:border-indigo-500/20">
      <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500 pointer-events-none" />
      <div className="relative flex flex-col flex-1">
        <div className="flex items-start justify-between mb-4">
          <div className="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center text-indigo-600 dark:text-indigo-400 group-hover:scale-110 transition-transform text-xl">{platform.icon}</div>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">{platform.toolCount} tools</span>
        </div>
        <h3 className="font-display font-semibold text-lg mb-2 text-zinc-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{platform.title[lang] || platform.title.en}</h3>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed flex-1 line-clamp-2">{platform.shortDescription[lang] || platform.shortDescription.en}</p>
        <div className="mt-4 pt-4 border-t border-zinc-200/50 dark:border-white/5 flex items-center gap-1.5 text-sm font-medium text-indigo-600 dark:text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity">Learn more <ArrowRight size={14} weight="bold" className="transition-transform group-hover:translate-x-0.5" /></div>
      </div>
    </Link>
  );
}

function NotFound() {
  return (
    <section className="py-32"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <WarningCircle size={48} className="mx-auto text-zinc-400 dark:text-zinc-600 mb-4" />
      <h1 className="text-2xl font-display font-bold text-zinc-900 dark:text-white mb-2">Platform Not Found</h1>
      <p className="text-zinc-500 dark:text-zinc-400 mb-8">The platform you are looking for does not exist or has been moved.</p>
      <Link to="/platforms" className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-black text-sm font-semibold hover:scale-105 transition-transform"><ArrowLeft size={16} weight="bold" /> Back to Platforms</Link>
    </div></section>
  );
}

export default function PlatformDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';

  const platform = platforms.find((p) => p.slug === slug);
  const title = platform ? platform.title[lang] || platform.title.en : '';
  const content = platform ? platform.content[lang] || platform.content.en : '';
  const toc = useMemo(() => extractToc(content), [content]);
  const related = useMemo(() => platforms.filter((p) => p.slug !== slug).slice(0, 3), [slug]);

  const heroRef = useRef<HTMLDivElement>(null);
  const featuresRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!heroRef.current) return;
    if (prefersReducedMotion()) { heroRef.current.style.opacity = '1'; heroRef.current.style.transform = 'none'; return; }
    const anim = animate(heroRef.current, { opacity: [0, 1], translateY: [30, 0], duration: 600, ease: 'outQuart' });
    return () => { anim.pause(); };
  }, [slug]);

  useEffect(() => {
    if (!featuresRef.current) return;
    const items = featuresRef.current.querySelectorAll('[data-feature-item]');
    if (items.length === 0) return;
    if (prefersReducedMotion()) { items.forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    const anim = animate(items, { opacity: [0, 1], translateX: [-15, 0], duration: 400, delay: stagger(50), ease: 'outQuart' });
    return () => { anim.pause(); };
  }, [slug]);

  if (!platform) return <NotFound />;

  const canonical = `${SITE_URL}/platforms/${platform.slug}`;
  const graphJsonLd = buildGraphJsonLd([webPageEntity(canonical, `${platform.title.en} - Aidvertaiser`, platform.shortDescription.en)]);

  return (
    <>
      <SEO title={`${title} - Aidvertaiser`} description={platform.shortDescription[lang] || platform.shortDescription.en} canonical={canonical} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: 'Platforms', url: `${SITE_URL}/platforms` }, { name: title, url: canonical }]} jsonLd={graphJsonLd} />

      <section className="pt-12 pb-8 md:pt-20 md:pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Breadcrumbs items={[{ label: 'Platforms', href: '/platforms' }, { label: title }]} />
          <div ref={heroRef} className="opacity-0">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-xl bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center text-indigo-600 dark:text-indigo-400 text-2xl">{platform.icon}</div>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">{platform.toolCount} tools</span>
            </div>
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight"><span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">{title}</span></h1>
            <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-3xl">{platform.shortDescription[lang] || platform.shortDescription.en}</p>
          </div>
        </div>
      </section>

      {platform.features.length > 0 && (
        <section className="pb-8 md:pb-12"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div ref={featuresRef} className="p-6 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
            <h3 className="font-display font-semibold text-lg text-zinc-900 dark:text-white mb-4">Key Features</h3>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {platform.features.map((f) => <li key={f} data-feature-item className="flex items-start gap-2 opacity-0"><CheckCircle size={18} weight="fill" className="text-emerald-500 flex-shrink-0 mt-0.5" /><span className="text-sm text-zinc-700 dark:text-zinc-300">{f}</span></li>)}
            </ul>
          </div>
        </div></section>
      )}

      {(platform.authMethod || platform.configFile) && (
        <section className="pb-8 md:pb-12"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {platform.authMethod && <div className="p-5 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]"><h4 className="text-sm font-semibold text-zinc-900 dark:text-white mb-2">Authentication</h4><p className="text-sm text-zinc-600 dark:text-zinc-400">{platform.authMethod}</p></div>}
          {platform.configFile && <div className="p-5 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]"><h4 className="text-sm font-semibold text-zinc-900 dark:text-white mb-2">Configuration</h4><code className="text-sm text-indigo-600 dark:text-indigo-400 font-mono">{platform.configFile}</code></div>}
        </div></div></section>
      )}

      <section className="pb-20 md:pb-32"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div className="flex gap-12">
        <motion.article initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.15 }} className="flex-1 min-w-0">
          <div className="prose prose-zinc dark:prose-invert prose-headings:font-display prose-headings:tracking-tight prose-h2:text-2xl prose-h2:mt-10 prose-h2:mb-4 prose-h3:text-xl prose-h3:mt-8 prose-h3:mb-3 prose-p:leading-relaxed prose-li:leading-relaxed prose-pre:bg-zinc-900 prose-pre:dark:bg-zinc-950 prose-pre:border prose-pre:border-zinc-800 prose-pre:dark:border-zinc-800/60 prose-pre:rounded-xl prose-code:text-indigo-600 prose-code:dark:text-indigo-400 prose-code:before:content-none prose-code:after:content-none prose-a:text-indigo-600 prose-a:dark:text-indigo-400 max-w-none" dangerouslySetInnerHTML={{ __html: content }} />
        </motion.article>
        {toc.length > 0 && (
          <aside className="hidden xl:block w-64 flex-shrink-0"><div className="sticky top-24">
            <h4 className="text-xs uppercase tracking-widest text-zinc-400 dark:text-zinc-500 font-medium mb-4">On this page</h4>
            <nav aria-label="Table of contents"><ul className="space-y-2 border-l border-zinc-200 dark:border-white/5">
              {toc.map((e) => <li key={e.id}><a href={`#${e.id}`} className={`block text-sm text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors ${e.level === 3 ? 'pl-6' : 'pl-4'} -ml-px border-l border-transparent hover:border-indigo-500`}>{e.text}</a></li>)}
            </ul></nav>
            <div className="mt-8 p-4 rounded-xl bg-gradient-to-br from-indigo-500/5 to-purple-500/5 border border-indigo-500/10">
              <p className="text-sm font-medium text-zinc-900 dark:text-white mb-2">Try Aidvertaiser</p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-3">Manage ads across all platforms.</p>
              <code className="block text-xs bg-zinc-900 dark:bg-zinc-950 text-zinc-300 px-3 py-2 rounded-lg font-mono">pip install unified-ads-mcp</code>
            </div>
          </div></aside>
        )}
      </div></div></section>

      {related.length > 0 && (
        <section className="py-16 md:py-24 border-t border-zinc-200/50 dark:border-white/5"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white mb-8">Other Platforms</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">{related.map((p) => <RelatedPlatformCard key={p.slug} platform={p} />)}</div>
        </div></section>
      )}

      <section className="py-16 md:py-24 bg-zinc-900 dark:bg-zinc-950 text-white"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight mb-4">Ready to Get Started?</h2>
        <p className="text-zinc-400 mb-8 max-w-lg mx-auto">Install Aidvertaiser and connect your ad platforms in under a minute.</p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a href="https://github.com/Draivix/aidvertaiser" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-semibold text-sm hover:scale-105 active:scale-[0.98] transition-transform shadow-xl">View on GitHub <ArrowRight size={16} weight="bold" /></a>
          <Link to="/platforms" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full border border-white/10 text-zinc-300 text-sm font-semibold hover:bg-white/5 transition-colors"><ArrowLeft size={16} weight="bold" /> All Platforms</Link>
        </div>
      </div></section>
    </>
  );
}
