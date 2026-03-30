import { useMemo, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { motion } from 'motion/react';
import { animate } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import { ArrowRight, ArrowLeft, Clock, WarningCircle } from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import { resources } from '@/content/resources';
import type { Resource } from '@/content/resources';
import { SITE_URL, buildGraphJsonLd, webPageEntity } from '@/content/seo-schema';

interface TocEntry { id: string; text: string; level: number; }
function extractToc(html: string): TocEntry[] {
  const entries: TocEntry[] = [];
  const regex = /<h([2-3])\s+id="([^"]+)"[^>]*>(.*?)<\/h[2-3]>/g;
  let m: RegExpExecArray | null;
  while ((m = regex.exec(html)) !== null) entries.push({ level: parseInt(m[1], 10), id: m[2], text: m[3].replace(/<[^>]+>/g, '') });
  return entries;
}

function RelatedCard({ item }: { item: Resource }) {
  const { i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  return (
    <Link to={`/resources/${item.slug}`} className="group relative flex flex-col rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] backdrop-blur-xl p-6 overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/5 hover:border-indigo-500/20 dark:hover:border-indigo-500/20">
      <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500 pointer-events-none" />
      <div className="relative flex flex-col flex-1">
        <h3 className="font-display font-semibold text-lg mb-2 text-zinc-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{item.title[lang] || item.title.en}</h3>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed flex-1 line-clamp-2">{item.shortDescription[lang] || item.shortDescription.en}</p>
        <div className="mt-4 pt-4 border-t border-zinc-200/50 dark:border-white/5 flex items-center gap-1.5 text-sm font-medium text-indigo-600 dark:text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity">Read <ArrowRight size={14} weight="bold" className="transition-transform group-hover:translate-x-0.5" /></div>
      </div>
    </Link>
  );
}

function NotFound() {
  return (
    <section className="py-32"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <WarningCircle size={48} className="mx-auto text-zinc-400 dark:text-zinc-600 mb-4" />
      <h1 className="text-2xl font-display font-bold text-zinc-900 dark:text-white mb-2">Resource Not Found</h1>
      <p className="text-zinc-500 dark:text-zinc-400 mb-8">The resource you are looking for does not exist or has been moved.</p>
      <Link to="/resources" className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-black text-sm font-semibold hover:scale-105 transition-transform"><ArrowLeft size={16} weight="bold" /> Back to Resources</Link>
    </div></section>
  );
}

export default function ResourceDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  const item = resources.find((r) => r.slug === slug);
  const title = item ? item.title[lang] || item.title.en : '';
  const content = item ? item.content[lang] || item.content.en : '';
  const toc = useMemo(() => extractToc(content), [content]);
  const related = useMemo(() => resources.filter((r) => r.slug !== slug).slice(0, 3), [slug]);
  const heroRef = useRef<HTMLElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!heroRef.current) return;
    if (prefersReducedMotion()) { heroRef.current.style.opacity = '1'; heroRef.current.style.transform = 'none'; return; }
    const anim = animate(heroRef.current, { opacity: [0, 1], translateY: [30, 0], duration: 600, ease: 'outQuart' });
    return () => { anim.pause(); };
  }, [slug]);

  useEffect(() => {
    if (!contentRef.current) return;
    if (prefersReducedMotion()) { contentRef.current.style.opacity = '1'; return; }
    const el = contentRef.current;
    const observer = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) { animate(el, { opacity: [0, 1], translateY: [20, 0], duration: 500, ease: 'outQuart' }); observer.disconnect(); } }, { threshold: 0.05, rootMargin: '-40px' });
    observer.observe(el);
    return () => observer.disconnect();
  }, [slug]);

  if (!item) return <NotFound />;
  const canonical = `${SITE_URL}/resources/${item.slug}`;
  const graphJsonLd = buildGraphJsonLd([webPageEntity(canonical, `${item.title.en} - Aidvertaiser`, item.shortDescription.en)]);

  return (
    <>
      <SEO title={`${title} - Aidvertaiser`} description={item.shortDescription[lang] || item.shortDescription.en} canonical={canonical} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: 'Resources', url: `${SITE_URL}/resources` }, { name: title, url: canonical }]} jsonLd={graphJsonLd} />
      <article className="py-20 md:py-28"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Breadcrumbs items={[{ label: 'Resources', href: '/resources' }, { label: title }]} />
        <Link to="/resources" className="inline-flex items-center gap-1.5 mt-2 mb-6 text-sm text-zinc-500 dark:text-zinc-500 hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"><ArrowLeft size={14} weight="bold" /> All Resources</Link>
        <header ref={heroRef} className="mb-12 max-w-3xl opacity-0">
          {item.category && <span className="inline-block px-2.5 py-0.5 text-xs font-medium rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/10 dark:border-indigo-500/20 mb-4">{item.category}</span>}
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight text-zinc-900 dark:text-white leading-tight">{title}</h1>
          {item.readTime && <div className="mt-4 flex items-center gap-2 text-sm text-zinc-500"><Clock size={16} weight="duotone" /> {item.readTime} min read</div>}
        </header>
        <div className="flex gap-12 items-start">
          <div ref={contentRef} className="flex-1 min-w-0 max-w-3xl opacity-0">
            <div className="prose prose-zinc dark:prose-invert prose-headings:font-display prose-headings:font-semibold prose-headings:tracking-tight prose-h2:text-2xl prose-h2:mt-12 prose-h2:mb-4 prose-h3:text-xl prose-h3:mt-8 prose-h3:mb-3 prose-p:leading-relaxed prose-p:text-zinc-600 prose-p:dark:text-zinc-400 prose-a:text-indigo-600 prose-a:dark:text-indigo-400 prose-a:no-underline hover:prose-a:underline prose-code:text-indigo-600 prose-code:dark:text-indigo-400 prose-code:bg-indigo-500/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:before:content-none prose-code:after:content-none prose-pre:bg-zinc-900 prose-pre:dark:bg-zinc-950 prose-pre:border prose-pre:border-zinc-800 prose-pre:dark:border-zinc-800/60 prose-pre:rounded-xl max-w-none" dangerouslySetInnerHTML={{ __html: content }} />
          </div>
          {toc.length > 0 && (
            <aside className="hidden xl:block w-64 flex-shrink-0"><nav className="sticky top-24 space-y-1">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-500 mb-3">On this page</h4>
              <ul className="space-y-1 text-sm border-l border-zinc-200/50 dark:border-white/10">
                {toc.map((e) => <li key={e.id}><a href={`#${e.id}`} className={`block py-1 text-zinc-500 dark:text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300 transition-colors ${e.level === 3 ? 'pl-6' : 'pl-3'}`}>{e.text}</a></li>)}
              </ul>
            </nav></aside>
          )}
        </div>
        {related.length > 0 && (
          <section className="mt-16 pt-12 border-t border-zinc-200/50 dark:border-white/10">
            <h2 className="text-2xl font-display font-bold text-zinc-900 dark:text-white mb-8">More Resources</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">{related.map((r) => <RelatedCard key={r.slug} item={r} />)}</div>
          </section>
        )}
      </div></article>
    </>
  );
}
