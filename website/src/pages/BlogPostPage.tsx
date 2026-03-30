import { useState, useEffect, useMemo, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { animate, stagger } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import { CalendarBlank, Clock, User, LinkSimple, Check, XLogo, ArrowLeft, List as ListIcon, CaretRight, ArrowRight } from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import { blogPosts } from '@/content/blog-posts';
import type { BlogPost } from '@/content/blog-posts';
import { SITE_URL, buildGraphJsonLd, webPageEntity, founderEntity } from '@/content/seo-schema';

interface TocItem { id: string; text: string; level: number; }
function extractToc(html: string): TocItem[] { const items: TocItem[] = []; const regex = /<h([23])\s+id="([^"]+)"[^>]*>(.*?)<\/h[23]>/gi; let m; while ((m = regex.exec(html)) !== null) items.push({ level: parseInt(m[1], 10), id: m[2], text: m[3].replace(/<[^>]*>/g, '') }); return items; }

function TableOfContents({ items, activeId, tocRef }: { items: TocItem[]; activeId: string; tocRef?: React.RefObject<HTMLElement | null> }) {
  if (items.length === 0) return null;
  return (
    <nav ref={tocRef} aria-label="Table of contents" className="sticky top-24 space-y-1">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-500 mb-3 flex items-center gap-1.5"><ListIcon size={14} weight="bold" /> On this page</h4>
      <ul className="space-y-1 text-sm border-l border-zinc-200/50 dark:border-white/10">
        {items.map((item) => <li key={item.id} data-toc-item className="opacity-0"><a href={`#${item.id}`} className={`block py-1 transition-colors ${item.level === 3 ? 'pl-6' : 'pl-3'} ${activeId === item.id ? 'text-indigo-600 dark:text-indigo-400 border-l-2 border-indigo-500 -ml-[1px] font-medium' : 'text-zinc-500 dark:text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300'}`}>{item.text}</a></li>)}
      </ul>
    </nav>
  );
}

function ShareButtons({ url, title }: { url: string; title: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => { try { await navigator.clipboard.writeText(url); setCopied(true); setTimeout(() => setCopied(false), 2000); } catch { /* */ } };
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider mr-1">Share</span>
      <button onClick={handleCopy} className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-zinc-200/50 dark:border-white/10 bg-white/50 dark:bg-white/5 text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:border-indigo-500/30 transition-colors" aria-label="Copy link">
        {copied ? <><Check size={14} weight="bold" className="text-emerald-500" /> Copied</> : <><LinkSimple size={14} weight="bold" /> Copy link</>}
      </button>
      <a href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-zinc-200/50 dark:border-white/10 bg-white/50 dark:bg-white/5 text-zinc-600 dark:text-zinc-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:border-indigo-500/30 transition-colors" aria-label="Share on X"><XLogo size={14} weight="bold" /> Post</a>
    </div>
  );
}

function PostNotFound() {
  return (
    <section className="py-32 text-center"><div className="max-w-2xl mx-auto px-4">
      <h1 className="text-4xl font-display font-bold text-zinc-900 dark:text-white mb-4">Article Not Found</h1>
      <p className="text-zinc-500 dark:text-zinc-400 mb-8">The blog post you are looking for does not exist or has been moved.</p>
      <Link to="/blog" className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-black text-sm font-semibold hover:scale-105 transition-transform"><ArrowLeft size={16} weight="bold" /> Back to Blog</Link>
    </div></section>
  );
}

function RelatedPosts({ post }: { post: BlogPost }) {
  const { i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  const related = blogPosts.filter((p) => p.slug !== post.slug && p.tags.some((t) => post.tags.includes(t))).slice(0, 2);
  if (related.length === 0) return null;
  const formatDate = (iso: string) => { try { return new Date(iso).toLocaleDateString(lang === 'en' ? 'en-US' : lang, { year: 'numeric', month: 'long', day: 'numeric' }); } catch { return iso; } };
  return (
    <section className="mt-16 pt-12 border-t border-zinc-200/50 dark:border-white/10">
      <h2 className="text-2xl font-display font-bold text-zinc-900 dark:text-white mb-8">Related Posts</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {related.map((r) => (
          <Link key={r.slug} to={`/blog/${r.slug}`} className="group p-5 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] hover:border-indigo-500/20 transition-colors">
            <h3 className="font-display font-semibold text-lg text-zinc-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors mb-2">{r.title[lang] || r.title.en}</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 line-clamp-2 mb-3">{r.description[lang] || r.description.en}</p>
            <div className="flex items-center gap-3 text-xs text-zinc-500"><span>{formatDate(r.date)}</span><span>{r.readTime} min read</span></div>
          </Link>
        ))}
      </div>
    </section>
  );
}

export default function BlogPostPage() {
  const { slug } = useParams<{ slug: string }>();
  const { t, i18n } = useTranslation();
  const lang = i18n.language?.slice(0, 2) || 'en';
  const post = blogPosts.find((p) => p.slug === slug);
  const title = post ? (post.title[lang] || post.title.en) : '';
  const description = post ? (post.description[lang] || post.description.en) : '';
  const metaDescription = post ? (post.description[lang] || post.description.en) : '';
  const content = post ? (post.content[lang] || post.content.en) : '';
  const tocItems = useMemo(() => (content ? extractToc(content) : []), [content]);
  const [activeId, setActiveId] = useState('');

  useEffect(() => {
    if (tocItems.length === 0) return;
    const observer = new IntersectionObserver((entries) => { for (const entry of entries) if (entry.isIntersecting) setActiveId(entry.target.id); }, { rootMargin: '-80px 0px -60% 0px', threshold: 0 });
    for (const item of tocItems) { const el = document.getElementById(item.id); if (el) observer.observe(el); }
    return () => observer.disconnect();
  }, [tocItems]);

  const heroRef = useRef<HTMLElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const tocNavRef = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!heroRef.current) return;
    if (prefersReducedMotion()) { heroRef.current.style.opacity = '1'; return; }
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

  useEffect(() => {
    if (!tocNavRef.current) return;
    const items = tocNavRef.current.querySelectorAll('[data-toc-item]');
    if (items.length === 0) return;
    if (prefersReducedMotion()) { items.forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    const timer = setTimeout(() => { animate(items, { opacity: [0, 1], translateX: [-10, 0], duration: 350, delay: stagger(40), ease: 'outQuart' }); }, 700);
    return () => clearTimeout(timer);
  }, [slug, tocItems]);

  const formatDate = (iso: string) => { try { return new Date(iso).toLocaleDateString(lang === 'en' ? 'en-US' : lang, { year: 'numeric', month: 'long', day: 'numeric' }); } catch { return iso; } };

  if (!post) return <><SEO title="Article Not Found | Aidvertaiser" description="The requested blog post could not be found." canonical={`${SITE_URL}/blog`} /><PostNotFound /></>;

  const canonicalUrl = `${SITE_URL}/blog/${post.slug}`;
  const graphJsonLd = buildGraphJsonLd([webPageEntity(canonicalUrl, `${post.title.en} - Aidvertaiser Blog`, post.description.en), founderEntity()]);

  return (
    <>
      <SEO title={`${title} | Aidvertaiser Blog`} description={metaDescription} canonical={canonicalUrl} article={{ publishedTime: post.date, modifiedTime: post.date, author: post.author, tags: post.tags }} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: 'Blog', url: `${SITE_URL}/blog` }, { name: title, url: canonicalUrl }]} jsonLd={graphJsonLd} />
      <article className="py-20 md:py-28"><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Breadcrumbs items={[{ label: 'Blog', href: '/blog' }, { label: title }]} />
        <Link to="/blog" className="inline-flex items-center gap-1.5 mt-6 text-sm text-zinc-500 hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors"><ArrowLeft size={14} weight="bold" /> {t('blog.backToBlog', 'Back to Blog')}</Link>
        <header ref={heroRef} className="mt-6 mb-12 max-w-3xl opacity-0">
          <div className="flex flex-wrap gap-1.5 mb-4">{post.tags.map((tag) => <span key={tag} className="inline-block px-2.5 py-0.5 text-xs font-medium rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/10 dark:border-indigo-500/20">{tag}</span>)}</div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight text-zinc-900 dark:text-white leading-tight">{title}</h1>
          <div className="mt-6 flex flex-wrap items-center gap-4 text-sm text-zinc-500">
            <span className="flex items-center gap-1.5"><User size={16} weight="duotone" /> {post.author} <CaretRight size={10} weight="bold" className="text-zinc-400" /> <span className="text-zinc-400">{post.authorRole}</span></span>
            <span className="flex items-center gap-1.5"><CalendarBlank size={16} weight="duotone" /> {formatDate(post.date)}</span>
            <span className="flex items-center gap-1.5"><Clock size={16} weight="duotone" /> {post.readTime} min read</span>
          </div>
          <div className="mt-6"><ShareButtons url={canonicalUrl} title={title} /></div>
        </header>
        <div className="flex gap-12 items-start">
          <div ref={contentRef} className="flex-1 min-w-0 max-w-3xl opacity-0">
            <div className="prose prose-zinc dark:prose-invert prose-headings:font-display prose-headings:font-semibold prose-headings:tracking-tight prose-h2:text-2xl prose-h2:mt-12 prose-h2:mb-4 prose-h3:text-xl prose-h3:mt-8 prose-h3:mb-3 prose-p:leading-relaxed prose-p:text-zinc-600 prose-p:dark:text-zinc-400 prose-a:text-indigo-600 prose-a:dark:text-indigo-400 prose-a:no-underline hover:prose-a:underline prose-code:text-indigo-600 prose-code:dark:text-indigo-400 prose-code:bg-indigo-500/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:before:content-none prose-code:after:content-none prose-pre:bg-zinc-900 prose-pre:dark:bg-zinc-950 prose-pre:border prose-pre:border-zinc-800 prose-pre:dark:border-zinc-800/60 prose-pre:rounded-xl max-w-none" dangerouslySetInnerHTML={{ __html: content }} />
            <div className="mt-12 pt-8 border-t border-zinc-200/50 dark:border-white/10"><ShareButtons url={canonicalUrl} title={title} /></div>
          </div>
          {tocItems.length > 0 && <aside className="hidden xl:block w-64 flex-shrink-0"><TableOfContents items={tocItems} activeId={activeId} tocRef={tocNavRef} /></aside>}
        </div>
        <RelatedPosts post={post} />
      </div></article>
    </>
  );
}
