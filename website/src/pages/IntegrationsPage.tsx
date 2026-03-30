import { useEffect, useRef, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { animate, stagger } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import { ArrowRight } from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import { integrations } from '@/content/integrations';
import type { Integration } from '@/content/integrations';
import { SITE_URL, buildGraphJsonLd, webPageEntity } from '@/content/seo-schema';

function IntegrationCard({ integration }: { integration: Integration }) {
  const { i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  const title = integration.title[lang] || integration.title.en;
  const description = integration.shortDescription[lang] || integration.shortDescription.en;

  return (
    <Link to={`/integrations/${integration.slug}`} className="group relative flex flex-col rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] backdrop-blur-xl p-6 overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/5 hover:border-indigo-500/20 dark:hover:border-indigo-500/20">
      <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500 pointer-events-none" />
      <div className="relative flex flex-col flex-1">
        <div className="flex items-start justify-between mb-4">
          <div className="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center text-indigo-600 dark:text-indigo-400 group-hover:scale-110 transition-transform text-xl">{integration.icon}</div>
        </div>
        <h3 className="font-display font-semibold text-lg mb-2 text-zinc-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{title}</h3>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed flex-1 line-clamp-3">{description}</p>
        {integration.configExample && (
          <pre className="mt-4 p-3 rounded-lg bg-zinc-900 dark:bg-zinc-950 border border-zinc-800 dark:border-zinc-800/60 text-zinc-400 font-mono text-[11px] overflow-x-auto line-clamp-3">{integration.configExample}</pre>
        )}
        <div className="mt-4 pt-4 border-t border-zinc-200/50 dark:border-white/5 flex items-center gap-1.5 text-sm font-medium text-indigo-600 dark:text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity">Learn more <ArrowRight size={14} weight="bold" className="transition-transform group-hover:translate-x-0.5" /></div>
      </div>
    </Link>
  );
}

export default function IntegrationsPage() {
  const { t } = useTranslation();
  const heroRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);
  const hasAnimatedGrid = useRef(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  const jsonLd = buildGraphJsonLd([webPageEntity(`${SITE_URL}/integrations`, 'Integrations - Aidvertaiser', 'Connect Aidvertaiser to Claude, ChatGPT, VS Code, and other AI assistants through the Model Context Protocol.')]);

  useEffect(() => {
    if (!heroRef.current) return;
    if (prefersReducedMotion()) { heroRef.current.style.opacity = '1'; heroRef.current.style.transform = 'none'; return; }
    const anim = animate(heroRef.current, { opacity: [0, 1], translateY: [30, 0], duration: 600, ease: 'outQuart' });
    return () => { anim.pause(); };
  }, []);

  const animateGrid = useCallback(() => {
    if (!gridRef.current) return;
    const cards = gridRef.current.querySelectorAll('[data-integration-card]');
    if (cards.length === 0) return;
    if (prefersReducedMotion()) { cards.forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    animate(cards, { opacity: [0, 1], scale: [0.85, 1], translateY: [30, 0], duration: 500, delay: stagger(60, { grid: [3, 2], from: 'first' }), ease: 'outQuart' });
  }, []);

  useEffect(() => {
    if (!gridRef.current) return;
    if (prefersReducedMotion()) { gridRef.current.querySelectorAll('[data-integration-card]').forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    observerRef.current = new IntersectionObserver(([entry]) => { if (entry.isIntersecting && !hasAnimatedGrid.current) { hasAnimatedGrid.current = true; animateGrid(); observerRef.current?.disconnect(); } }, { threshold: 0.1, rootMargin: '-60px' });
    observerRef.current.observe(gridRef.current);
    return () => { observerRef.current?.disconnect(); };
  }, [animateGrid]);

  return (
    <>
      <SEO title="Integrations - Aidvertaiser" description="Connect Aidvertaiser to Claude, ChatGPT, VS Code, and other AI assistants through the Model Context Protocol." canonical={`${SITE_URL}/integrations`} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: 'Integrations', url: `${SITE_URL}/integrations` }]} jsonLd={jsonLd} />
      <section className="pt-12 pb-8 md:pt-20 md:pb-12"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Breadcrumbs items={[{ label: t('nav.integrations', 'Integrations') }]} />
        <div ref={heroRef} className="max-w-3xl opacity-0">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('integrations.title', 'MCP')}{' '}<span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">{t('integrations.titleGradient', 'Integrations')}</span></h1>
          <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('integrations.subtitle', 'Connect Aidvertaiser to your favorite AI assistants and development tools through the Model Context Protocol.')}</p>
        </div>
      </div></section>
      <section className="pb-20 md:pb-32"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div ref={gridRef} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {integrations.map((i) => <div key={i.slug} data-integration-card className="opacity-0"><IntegrationCard integration={i} /></div>)}
        </div>
      </div></section>
      <section className="py-20 md:py-32 bg-zinc-900 dark:bg-zinc-950 text-white relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none" aria-hidden="true"><div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-r from-indigo-500/30 via-purple-500/20 to-pink-500/30 blur-[120px] rounded-full" /></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ duration: 0.6 }} className="text-center">
            <h2 className="text-3xl md:text-4xl font-display font-bold tracking-tight">Connect Your AI Assistant</h2>
            <p className="mt-4 text-lg text-zinc-400 max-w-xl mx-auto">One install to manage ads through any MCP-compatible AI. Open source, forever free.</p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <a href="/docs" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-semibold text-sm hover:scale-105 active:scale-[0.98] transition-transform shadow-xl">Get Started <ArrowRight size={16} weight="bold" /></a>
              <div className="inline-flex items-center gap-3 bg-zinc-800/80 text-zinc-300 rounded-xl px-5 py-3 font-mono text-sm border border-zinc-700/50"><span className="text-zinc-500 select-none">$</span><span className="select-all">pip install unified-ads-mcp</span></div>
            </div>
          </motion.div>
        </div>
      </section>
    </>
  );
}
