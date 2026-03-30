import { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { animate, stagger, createTimeline } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import { MagnifyingGlass, Funnel, ArrowRight, Clock, CalendarBlank } from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import { blogPosts } from '@/content/blog-posts';
import { SITE_URL, buildGraphJsonLd, webPageEntity } from '@/content/seo-schema';

function BlogCard({ slug, title, description, date, readTime, tags }: { slug: string; title: string; description: string; date: string; readTime: string; tags: string[] }) {
  return (
    <Link to={`/blog/${slug}`} className="group relative flex flex-col rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] backdrop-blur-xl p-6 overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/5 hover:border-indigo-500/20 dark:hover:border-indigo-500/20">
      <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500 pointer-events-none" />
      <div className="relative flex flex-col flex-1">
        <div className="flex flex-wrap gap-1.5 mb-3">
          {tags.slice(0, 2).map((tag) => <span key={tag} className="inline-block px-2 py-0.5 text-[11px] font-medium rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">{tag}</span>)}
        </div>
        <h3 className="font-display font-semibold text-lg mb-2 text-zinc-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors line-clamp-2">{title}</h3>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed flex-1 line-clamp-3">{description}</p>
        <div className="mt-4 pt-4 border-t border-zinc-200/50 dark:border-white/5 flex items-center justify-between text-xs text-zinc-500">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1"><CalendarBlank size={12} /> {date}</span>
            <span className="flex items-center gap-1"><Clock size={12} /> {readTime}</span>
          </div>
          <ArrowRight size={14} className="text-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity" weight="bold" />
        </div>
      </div>
    </Link>
  );
}

export default function BlogPage() {
  const { t, i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const heroRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);
  const hasAnimatedGrid = useRef(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  const allTags = useMemo(() => {
    const tagSet = new Set<string>();
    blogPosts.forEach((p) => p.tags.forEach((t) => tagSet.add(t)));
    return Array.from(tagSet).sort();
  }, []);

  const filteredPosts = useMemo(() => {
    let posts = [...blogPosts];
    if (activeTag) posts = posts.filter((p) => p.tags.includes(activeTag));
    if (search.trim()) {
      const q = search.toLowerCase();
      posts = posts.filter((p) => { const ti = (p.title[lang] || p.title.en).toLowerCase(); const d = (p.description[lang] || p.description.en).toLowerCase(); return ti.includes(q) || d.includes(q) || p.tags.join(' ').toLowerCase().includes(q); });
    }
    posts.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    return posts;
  }, [activeTag, search, lang]);

  const formatDate = (iso: string) => { try { return new Date(iso).toLocaleDateString(lang === 'en' ? 'en-US' : lang, { year: 'numeric', month: 'long', day: 'numeric' }); } catch { return iso; } };

  useEffect(() => {
    if (!heroRef.current || !searchRef.current) return;
    if (prefersReducedMotion()) { heroRef.current.style.opacity = '1'; searchRef.current.style.opacity = '1'; return; }
    const tl = createTimeline({ defaults: { ease: 'outQuart' } }).add(heroRef.current, { opacity: [0, 1], translateY: [30, 0], duration: 600 }).add(searchRef.current, { opacity: [0, 1], translateY: [20, 0], duration: 500 }, '-=300');
    return () => { tl.pause(); };
  }, []);

  const animateGrid = useCallback(() => {
    if (!gridRef.current) return;
    const cards = gridRef.current.querySelectorAll('[data-blog-card]');
    if (cards.length === 0) return;
    if (prefersReducedMotion()) { cards.forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    animate(cards, { opacity: [0, 1], scale: [0.9, 1], translateY: [25, 0], duration: 450, delay: stagger(70, { from: 'first' }), ease: 'outQuart' });
  }, []);

  useEffect(() => {
    if (!gridRef.current) return;
    if (prefersReducedMotion()) { gridRef.current.querySelectorAll('[data-blog-card]').forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    observerRef.current = new IntersectionObserver(([entry]) => { if (entry.isIntersecting && !hasAnimatedGrid.current) { hasAnimatedGrid.current = true; animateGrid(); observerRef.current?.disconnect(); } }, { threshold: 0.1, rootMargin: '-60px' });
    observerRef.current.observe(gridRef.current);
    return () => { observerRef.current?.disconnect(); };
  }, [animateGrid]);

  useEffect(() => {
    if (!gridRef.current || prefersReducedMotion()) { if (gridRef.current) gridRef.current.querySelectorAll('[data-blog-card]').forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    hasAnimatedGrid.current = false;
    gridRef.current.querySelectorAll('[data-blog-card]').forEach((el) => { (el as HTMLElement).style.opacity = '0'; (el as HTMLElement).style.transform = ''; });
    observerRef.current?.disconnect();
    observerRef.current = new IntersectionObserver(([entry]) => { if (entry.isIntersecting && !hasAnimatedGrid.current) { hasAnimatedGrid.current = true; animateGrid(); observerRef.current?.disconnect(); } }, { threshold: 0.1, rootMargin: '-60px' });
    observerRef.current.observe(gridRef.current);
    return () => { observerRef.current?.disconnect(); };
  }, [filteredPosts, animateGrid]);

  const jsonLd = buildGraphJsonLd([webPageEntity(`${SITE_URL}/blog`, 'Blog - Aidvertaiser', 'Insights on AI-powered advertising, MCP integrations, and digital marketing automation.')]);

  return (
    <>
      <SEO title={`${t('blog.title', 'Blog')} | Aidvertaiser`} description={t('blog.subtitle', 'Insights on AI-powered advertising management, MCP integrations, and marketing automation.')} canonical={`${SITE_URL}/blog`} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: t('blog.title', 'Blog'), url: `${SITE_URL}/blog` }]} jsonLd={jsonLd} />
      <section className="py-20 md:py-28"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Breadcrumbs items={[{ label: t('blog.title', 'Blog') }]} />
        <div ref={heroRef} className="mt-8 mb-12 opacity-0">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('blog.title', 'Blog')}</h1>
          <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl">{t('blog.subtitle', 'Insights on AI-powered advertising management, MCP integrations, and marketing automation.')}</p>
        </div>
        <div ref={searchRef} className="mb-10 space-y-4 opacity-0">
          <div className="relative max-w-md">
            <MagnifyingGlass size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" weight="duotone" />
            <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder={t('blog.searchPlaceholder', 'Search articles...')} className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-zinc-200/50 dark:border-white/10 bg-white/50 dark:bg-white/5 backdrop-blur-sm text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500/30 transition-colors" />
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-medium text-zinc-500 dark:text-zinc-500 uppercase tracking-wider mr-1 flex items-center gap-1"><Funnel size={14} weight="duotone" /> Tags</span>
            <button onClick={() => setActiveTag(null)} className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors ${activeTag === null ? 'bg-indigo-500 text-white border-indigo-500' : 'bg-white/50 dark:bg-white/5 text-zinc-600 dark:text-zinc-400 border-zinc-200/50 dark:border-white/10 hover:border-indigo-500/30'}`}>All</button>
            {allTags.map((tag) => <button key={tag} onClick={() => setActiveTag(activeTag === tag ? null : tag)} className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors ${activeTag === tag ? 'bg-indigo-500 text-white border-indigo-500' : 'bg-white/50 dark:bg-white/5 text-zinc-600 dark:text-zinc-400 border-zinc-200/50 dark:border-white/10 hover:border-indigo-500/30'}`}>{tag}</button>)}
          </div>
        </div>
        {filteredPosts.length > 0 ? (
          <div ref={gridRef} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredPosts.map((post) => <div key={post.slug} data-blog-card className="opacity-0"><BlogCard slug={post.slug} title={post.title[lang] || post.title.en} description={post.description[lang] || post.description.en} date={formatDate(post.date)} readTime={`${post.readTime} ${t('blog.minRead', 'min read')}`} tags={post.tags} /></div>)}
          </div>
        ) : (
          <div className="text-center py-20">
            <p className="text-zinc-500 dark:text-zinc-500 text-lg">No articles match your search.</p>
            <button onClick={() => { setSearch(''); setActiveTag(null); }} className="mt-4 text-sm text-indigo-500 hover:text-indigo-400 transition-colors">Clear filters</button>
          </div>
        )}
      </div></section>
    </>
  );
}
