import { useRef, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, useInView } from 'motion/react';
import { animate, stagger } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import {
  Buildings,
  Briefcase,
  CalendarBlank,
  Copy,
  Check,
  Envelope,
  GithubLogo,
  Globe,
  Handshake,
  Heart,
  Lightning,
  LinkedinLogo,
  MapPin,
  Newspaper,
  Rocket,
  Sparkle,
  Star,
  TrendUp,
  Trophy,
  UsersThree,
  XLogo,
} from '@phosphor-icons/react';
import SEO from '@/components/SEO';
import Breadcrumbs from '@/components/Breadcrumbs';
import {
  SITE_URL,
  buildGraphJsonLd,
  organizationEntity,
  founderEntity,
  webPageEntity,
} from '@/content/seo-schema';

/* -------------------------------------------------------------------------- */
/*  Constants                                                                 */
/* -------------------------------------------------------------------------- */

const STATS = [
  { value: 6, label: 'Platforms Supported', suffix: '' },
  { value: 180, label: 'MCP Tools', suffix: '' },
  { value: 1, label: 'Unified Server', suffix: '' },
  { value: 100, label: 'Open Source', suffix: '%' },
] as const;

const TECHNOLOGY_PARTNERS = [
  { name: 'Google', desc: 'Ads & Analytics' },
  { name: 'Meta', desc: 'Advertising APIs' },
  { name: 'Matomo', desc: 'Web Analytics' },
  { name: 'Bing', desc: 'Webmaster Tools' },
  { name: 'Anthropic', desc: 'MCP Protocol' },
  { name: 'OpenAI', desc: 'AI Integration' },
] as const;

const CUSTOMER_QUOTES = [
  { quote: 'Aidvertaiser replaced three different API wrappers for us. One MCP server, all our ad platforms.', author: 'Marketing Lead', company: 'SaaS Startup' },
  { quote: 'The ability to manage Google Ads and Meta Ads through natural language is a game-changer for our team.', author: 'Head of Growth', company: 'E-commerce Brand' },
  { quote: 'We integrated Aidvertaiser into our CI/CD pipeline for automated campaign management. It just works.', author: 'DevOps Engineer', company: 'Agency' },
] as const;

const BENEFITS = [
  { icon: Lightning, title: 'Fast-Paced Innovation', desc: 'Ship new tools and platform integrations weekly.' },
  { icon: Globe, title: 'Remote-First Culture', desc: 'Work from anywhere in the world.' },
  { icon: Heart, title: 'Open Source Values', desc: 'Everything we build is MIT-licensed.' },
  { icon: Rocket, title: 'Growth Opportunity', desc: 'Shape the future of AI-powered advertising.' },
] as const;

const TOC_ITEMS = [
  { id: 'company', label: 'Company' },
  { id: 'leadership', label: 'Leadership' },
  { id: 'vision', label: 'Mission & Vision' },
  { id: 'careers', label: 'Careers' },
  { id: 'partners', label: 'Partners' },
  { id: 'stories', label: 'Customer Stories' },
  { id: 'press', label: 'Press' },
  { id: 'investors', label: 'Investors' },
  { id: 'events', label: 'Events' },
  { id: 'contact', label: 'Contact' },
] as const;

/* -------------------------------------------------------------------------- */
/*  Stat Counter                                                              */
/* -------------------------------------------------------------------------- */

function StatCounter({ value, label, suffix }: { value: number; label: string; suffix: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: '-50px' });
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    if (!isInView) return;
    if (prefersReducedMotion()) { setDisplayValue(value); return; }
    const obj = { val: 0 };
    const anim = animate(obj, { val: value, duration: 1500, ease: 'outExpo', onUpdate: () => setDisplayValue(Math.round(obj.val)) });
    return () => { anim.pause(); };
  }, [isInView, value]);

  return (
    <div ref={ref} className="text-center">
      <p className="text-3xl md:text-4xl font-display font-bold text-zinc-900 dark:text-white">
        {displayValue}{suffix}
      </p>
      <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">{label}</p>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  AboutPage                                                                 */
/* -------------------------------------------------------------------------- */

export default function AboutPage() {
  const { t } = useTranslation();
  const [emailCopied, setEmailCopied] = useState(false);

  const heroRef = useRef<HTMLDivElement>(null);
  const statsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!heroRef.current) return;
    if (prefersReducedMotion()) { heroRef.current.style.opacity = '1'; return; }
    const anim = animate(heroRef.current, { opacity: [0, 1], translateY: [30, 0], duration: 600, ease: 'outQuart' });
    return () => { anim.pause(); };
  }, []);

  useEffect(() => {
    if (!statsRef.current) return;
    const items = statsRef.current.querySelectorAll('[data-stat]');
    if (prefersReducedMotion()) { items.forEach((el) => { (el as HTMLElement).style.opacity = '1'; }); return; }
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        animate(items, { opacity: [0, 1], translateY: [20, 0], duration: 500, delay: stagger(100), ease: 'outQuart' });
        observer.disconnect();
      }
    }, { threshold: 0.2 });
    observer.observe(statsRef.current);
    return () => observer.disconnect();
  }, []);

  const handleCopyEmail = async () => {
    try { await navigator.clipboard.writeText('hello@aidvertaiser.com'); setEmailCopied(true); setTimeout(() => setEmailCopied(false), 2000); } catch { /* */ }
  };

  const canonical = `${SITE_URL}/about`;
  const graphJsonLd = buildGraphJsonLd([organizationEntity(), founderEntity(), webPageEntity(canonical, 'About Aidvertaiser', 'Learn about Aidvertaiser, the AI-powered advertising MCP server by Draivix. Meet the team, explore our mission, and discover partnership opportunities.')]);

  return (
    <>
      <SEO title={t('about.meta.title', 'About - Aidvertaiser')} description={t('about.meta.description', 'Learn about Aidvertaiser, the AI-powered advertising MCP server by Draivix. Meet the team, explore our mission, and discover partnership opportunities.')} canonical={canonical} breadcrumbs={[{ name: 'Home', url: SITE_URL }, { name: 'About', url: canonical }]} jsonLd={graphJsonLd} />

      {/* Hero */}
      <section className="pt-12 pb-8 md:pt-20 md:pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Breadcrumbs items={[{ label: t('about.breadcrumb', 'About') }]} />
          <div ref={heroRef} className="max-w-3xl opacity-0">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold tracking-tighter text-zinc-900 dark:text-white">
              {t('about.heroTitle', 'About')}{' '}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">{t('about.heroGradient', 'Draivix')}</span>
            </h1>
            <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed">
              {t('about.heroSubtitle', 'Building open-source tools that make advertising accessible to AI assistants. Aidvertaiser is our unified MCP server that connects 6 major ad platforms to any AI.')}
            </p>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-12 md:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div ref={statsRef} className="grid grid-cols-2 md:grid-cols-4 gap-8 p-8 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
            {STATS.map((stat) => <div key={stat.label} data-stat className="opacity-0"><StatCounter value={stat.value} label={stat.label} suffix={stat.suffix} /></div>)}
          </div>
        </div>
      </section>

      {/* Content + TOC */}
      <section className="pb-20 md:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-12">
            {/* Main Content */}
            <div className="flex-1 min-w-0 space-y-20">

              {/* Company */}
              <motion.div id="company" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Buildings size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.company.title', 'Company')}</h2>
                </div>
                <div className="prose prose-zinc dark:prose-invert max-w-none prose-p:leading-relaxed">
                  <p>{t('about.company.p1', 'Aidvertaiser is developed by Draivix, a software company focused on building developer tools that bridge the gap between AI and real-world services. Founded in 2025, Draivix creates open-source MCP servers that give AI assistants access to professional tools.')}</p>
                  <p>{t('about.company.p2', 'Aidvertaiser is our advertising-focused MCP server. It provides 180 tools across 6 major platforms: Google Ads, Meta Ads, Google Analytics 4, Google Search Console, Matomo, and Bing Webmaster Tools. All tools are accessible through the Model Context Protocol, making them compatible with any MCP-enabled AI assistant.')}</p>
                </div>
              </motion.div>

              {/* Leadership */}
              <motion.div id="leadership" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Star size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.leadership.title', 'Leadership')}</h2>
                </div>
                <div className="p-6 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                  <div className="flex items-start gap-4">
                    <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-display font-bold text-xl flex-shrink-0">DS</div>
                    <div>
                      <h3 className="font-display font-semibold text-lg text-zinc-900 dark:text-white">David Strejc</h3>
                      <p className="text-sm text-indigo-600 dark:text-indigo-400 font-medium">Founder & CEO</p>
                      <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('about.leadership.bio', 'Software engineer and entrepreneur with a passion for developer tools and open-source software. David founded Draivix to build the infrastructure layer that connects AI to professional services.')}</p>
                      <div className="mt-4 flex items-center gap-3">
                        <a href="https://github.com/david-strejc" target="_blank" rel="noopener noreferrer" className="text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors"><GithubLogo size={18} /></a>
                        <a href="https://x.com/aidvertaiser" target="_blank" rel="noopener noreferrer" className="text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors"><XLogo size={18} /></a>
                        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors"><LinkedinLogo size={18} /></a>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Vision */}
              <motion.div id="vision" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Sparkle size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.vision.title', 'Mission & Vision')}</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-6 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                    <h3 className="font-display font-semibold text-lg text-zinc-900 dark:text-white mb-3">{t('about.vision.missionTitle', 'Mission')}</h3>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('about.vision.missionText', 'Make advertising platform management accessible to every AI assistant through open, standardized protocols.')}</p>
                  </div>
                  <div className="p-6 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                    <h3 className="font-display font-semibold text-lg text-zinc-900 dark:text-white mb-3">{t('about.vision.visionTitle', 'Vision')}</h3>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('about.vision.visionText', 'A world where AI assistants can manage and optimize advertising campaigns as naturally as a human marketing expert.')}</p>
                  </div>
                </div>
              </motion.div>

              {/* Careers */}
              <motion.div id="careers" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Briefcase size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.careers.title', 'Join Us')}</h2>
                </div>
                <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">{t('about.careers.intro', 'We are building the future of AI-powered advertising. If you are passionate about developer tools, advertising APIs, or the Model Context Protocol, we want to hear from you.')}</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                  {BENEFITS.map(({ icon: Icon, title, desc }) => (
                    <div key={title} className="p-4 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                      <Icon size={20} weight="duotone" className="text-indigo-500 mb-2" />
                      <h4 className="font-display font-semibold text-sm text-zinc-900 dark:text-white">{title}</h4>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{desc}</p>
                    </div>
                  ))}
                </div>
                <div className="p-5 rounded-xl bg-gradient-to-br from-indigo-500/5 to-purple-500/5 border border-indigo-500/10">
                  <p className="text-sm text-zinc-700 dark:text-zinc-300">
                    <strong>{t('about.careers.ossTitle', 'Open Source Contributions')}</strong> - {t('about.careers.ossText', 'Not looking for a full-time role? We welcome open-source contributions to Aidvertaiser on GitHub. Every PR counts.')}
                  </p>
                </div>
              </motion.div>

              {/* Partners */}
              <motion.div id="partners" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Handshake size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.partners.title', 'Technology Partners')}</h2>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                  {TECHNOLOGY_PARTNERS.map((partner) => (
                    <div key={partner.name} className="p-4 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] text-center">
                      <p className="font-display font-semibold text-zinc-900 dark:text-white">{partner.name}</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{partner.desc}</p>
                    </div>
                  ))}
                </div>
              </motion.div>

              {/* Customer Stories */}
              <motion.div id="stories" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><UsersThree size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.stories.title', 'Customer Stories')}</h2>
                </div>
                <div className="space-y-4">
                  {CUSTOMER_QUOTES.map((q, i) => (
                    <div key={i} className="p-6 rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                      <blockquote className="text-zinc-700 dark:text-zinc-300 leading-relaxed italic">"{q.quote}"</blockquote>
                      <div className="mt-3 flex items-center gap-2 text-sm text-zinc-500"><span className="font-medium">{q.author}</span><span>-</span><span>{q.company}</span></div>
                    </div>
                  ))}
                </div>
              </motion.div>

              {/* Press */}
              <motion.div id="press" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Newspaper size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.press.title', 'Press')}</h2>
                </div>
                <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('about.press.text', 'For press inquiries, media kit requests, or interview scheduling, please contact us at press@aidvertaiser.com. We are happy to provide product screenshots, logos, and technical background information.')}</p>
              </motion.div>

              {/* Investors */}
              <motion.div id="investors" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><TrendUp size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.investors.title', 'Investor Relations')}</h2>
                </div>
                <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('about.investors.text', 'Aidvertaiser is part of the Draivix portfolio of open-source developer tools. For investor relations and partnership opportunities, please reach out to investors@draivix.com.')}</p>
              </motion.div>

              {/* Events */}
              <motion.div id="events" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><CalendarBlank size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.events.title', 'Events')}</h2>
                </div>
                <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">{t('about.events.text', 'We participate in developer conferences, AI summits, and digital marketing events. Follow us on X for event announcements and speaking opportunities.')}</p>
              </motion.div>

              {/* Contact */}
              <motion.div id="contact" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-80px' }} transition={{ duration: 0.5 }}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500 flex items-center justify-center"><Envelope size={22} weight="duotone" /></div>
                  <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('about.contact.title', 'Contact')}</h2>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="p-5 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                    <h4 className="font-display font-semibold text-sm text-zinc-900 dark:text-white mb-2">Email</h4>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-zinc-600 dark:text-zinc-400">hello@aidvertaiser.com</span>
                      <button onClick={handleCopyEmail} className="p-1 rounded hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors">
                        {emailCopied ? <Check size={14} className="text-emerald-500" weight="bold" /> : <Copy size={14} className="text-zinc-400" />}
                      </button>
                    </div>
                  </div>
                  <div className="p-5 rounded-xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02]">
                    <h4 className="font-display font-semibold text-sm text-zinc-900 dark:text-white mb-2">Location</h4>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 flex items-center gap-1.5"><MapPin size={14} /> Remote-First, Global</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center gap-3">
                  <a href="https://github.com/Draivix/aidvertaiser" target="_blank" rel="noopener noreferrer" className="p-2.5 rounded-lg border border-zinc-200/50 dark:border-white/10 text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:border-indigo-500/30 transition-colors"><GithubLogo size={20} /></a>
                  <a href="https://x.com/aidvertaiser" target="_blank" rel="noopener noreferrer" className="p-2.5 rounded-lg border border-zinc-200/50 dark:border-white/10 text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:border-indigo-500/30 transition-colors"><XLogo size={20} /></a>
                </div>
              </motion.div>

            </div>

            {/* Desktop Sidebar - TOC */}
            <aside className="hidden xl:block w-56 flex-shrink-0">
              <div className="sticky top-24">
                <h4 className="text-xs uppercase tracking-widest text-zinc-400 dark:text-zinc-500 font-medium mb-4">On this page</h4>
                <nav aria-label="Table of contents">
                  <ul className="space-y-2 border-l border-zinc-200 dark:border-white/5">
                    {TOC_ITEMS.map((item) => (
                      <li key={item.id}>
                        <a href={`#${item.id}`} className="block text-sm text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition-colors pl-4 -ml-px border-l border-transparent hover:border-indigo-500">{item.label}</a>
                      </li>
                    ))}
                  </ul>
                </nav>
              </div>
            </aside>
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="py-20 md:py-32 bg-zinc-900 dark:bg-zinc-950 text-white relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none" aria-hidden="true"><div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-r from-indigo-500/30 via-purple-500/20 to-pink-500/30 blur-[120px] rounded-full" /></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ duration: 0.6 }} className="text-center">
            <h2 className="text-3xl md:text-4xl font-display font-bold tracking-tight">{t('about.cta.title', 'Start Managing Ads with AI')}</h2>
            <p className="mt-4 text-lg text-zinc-400 max-w-xl mx-auto">{t('about.cta.subtitle', 'Install Aidvertaiser and connect your advertising platforms today. Open source, MIT-licensed.')}</p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <a href="/docs" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-semibold text-sm hover:scale-105 active:scale-[0.98] transition-transform shadow-xl"><Trophy size={16} weight="bold" /> Get Started</a>
              <div className="inline-flex items-center gap-3 bg-zinc-800/80 text-zinc-300 rounded-xl px-5 py-3 font-mono text-sm border border-zinc-700/50"><span className="text-zinc-500 select-none">$</span><span className="select-all">pip install unified-ads-mcp</span></div>
            </div>
          </motion.div>
        </div>
      </section>
    </>
  );
}
