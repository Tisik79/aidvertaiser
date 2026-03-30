import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, useInView } from 'motion/react';
import { animate, stagger, createTimeline } from 'animejs';
import {
  Megaphone,
  Target,
  UsersThree,
  ChartLineUp,
  MagnifyingGlass,
  Pulse,
  Copy,
  Check,
  ArrowRight,
  GithubLogo,
} from '@phosphor-icons/react';
import { prefersReducedMotion } from '@/hooks/useAnime';
import SEO from '@/components/SEO';
import {
  SITE_URL,
  buildGraphJsonLd,
  webPageEntity,
  organizationEntity,
  founderEntity,
} from '@/content/seo-schema';

/* -------------------------------------------------------------------------- */
/*  Constants                                                                 */
/* -------------------------------------------------------------------------- */

const featureKeys = [
  { key: 'campaigns', Icon: Megaphone },
  { key: 'conversions', Icon: Target },
  { key: 'audiences', Icon: UsersThree },
  { key: 'analytics', Icon: ChartLineUp },
  { key: 'seo', Icon: MagnifyingGlass },
  { key: 'monitoring', Icon: Pulse },
] as const;

const pipelineStageKeys = ['configure', 'connect', 'command', 'optimize'] as const;

const supportedPlatforms = ['Google Ads', 'Meta Ads', 'GA4', 'Search Console', 'Matomo', 'Bing'];

/* Terminal lines with embedded numeric targets for count-up animation */
const terminalLines = [
  { text: '$ pip install unified-ads-mcp', color: 'text-zinc-300', delay: 0, numbers: [] as { value: number; label: string }[] },
  { text: '', color: '', delay: 0.15, numbers: [] as { value: number; label: string }[] },
  { text: '  Aidvertaiser v1.0.0', color: 'text-indigo-400', delay: 0.3, numbers: [] as { value: number; label: string }[] },
  { text: '', color: '', delay: 0.35, numbers: [] as { value: number; label: string }[] },
  { text: '  Connecting...  Google Ads \u2713', color: 'text-zinc-400', delay: 0.5, numbers: [] as { value: number; label: string }[] },
  { text: '  Connecting...  Meta Ads \u2713', color: 'text-zinc-400', delay: 0.65, numbers: [] as { value: number; label: string }[] },
  { text: '  Connecting...  GA4 \u2713', color: 'text-zinc-400', delay: 0.8, numbers: [] as { value: number; label: string }[] },
  { text: '', color: '', delay: 0.9, numbers: [] as { value: number; label: string }[] },
  { text: '  > Create a search campaign for "cloud hosting"', color: 'text-emerald-400', delay: 1.0, numbers: [] as { value: number; label: string }[] },
  { text: '', color: '', delay: 1.1, numbers: [] as { value: number; label: string }[] },
  { text: '  Creating campaign...', color: 'text-zinc-400', delay: 1.2, numbers: [] as { value: number; label: string }[] },
  { text: '  \u251c\u2500\u2500 Campaign: Cloud Hosting Search', color: 'text-zinc-400', delay: 1.35, numbers: [] as { value: number; label: string }[] },
  { text: '  \u251c\u2500\u2500 Budget: ${50}/day', color: 'text-zinc-400', delay: 1.5, numbers: [{ value: 50, label: 'budget' }] },
  { text: '  \u251c\u2500\u2500 Keywords: {12} added', color: 'text-zinc-400', delay: 1.65, numbers: [{ value: 12, label: 'keywords' }] },
  { text: '  \u251c\u2500\u2500 Ads: {3} responsive search ads', color: 'text-zinc-400', delay: 1.8, numbers: [{ value: 3, label: 'ads' }] },
  { text: '  \u2514\u2500\u2500 Status: Active \u2713', color: 'text-emerald-400', delay: 1.95, numbers: [] as { value: number; label: string }[] },
  { text: '', color: '', delay: 2.05, numbers: [] as { value: number; label: string }[] },
  { text: '  Campaign live! Estimated daily reach: {4500}', color: 'text-indigo-400', delay: 2.15, numbers: [{ value: 4500, label: 'reach' }] },
];

/* -------------------------------------------------------------------------- */
/*  AdBackground -- advertising-themed SVG background                         */
/* -------------------------------------------------------------------------- */

function AdBackground() {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
      <svg
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] md:w-[800px] md:h-[800px] opacity-[0.04] dark:opacity-[0.06]"
        viewBox="0 0 400 400"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M120 160 L280 100 L280 300 L120 240 Z" stroke="currentColor" strokeWidth="2" className="text-indigo-500" />
        <circle cx="120" cy="200" r="40" stroke="currentColor" strokeWidth="2" className="text-purple-500" />
        <path d="M280 100 Q340 140 340 200 Q340 260 280 300" stroke="currentColor" strokeWidth="2" className="text-pink-500" />
        <path d="M300 120 Q360 160 360 200 Q360 240 300 280" stroke="currentColor" strokeWidth="1.5" className="text-pink-400" strokeDasharray="6 4" />
        <path d="M320 140 Q380 180 380 200 Q380 220 320 260" stroke="currentColor" strokeWidth="1" className="text-indigo-400" strokeDasharray="4 4" />
        <rect x="100" y="320" width="30" height="40" rx="4" stroke="currentColor" strokeWidth="1.5" className="text-indigo-400" />
        <rect x="140" y="300" width="30" height="60" rx="4" stroke="currentColor" strokeWidth="1.5" className="text-purple-400" />
        <rect x="180" y="310" width="30" height="50" rx="4" stroke="currentColor" strokeWidth="1.5" className="text-pink-400" />
        <rect x="220" y="290" width="30" height="70" rx="4" stroke="currentColor" strokeWidth="1.5" className="text-indigo-400" />
        <rect x="260" y="280" width="30" height="80" rx="4" stroke="currentColor" strokeWidth="1.5" className="text-purple-400" />
      </svg>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Hero Section                                                              */
/* -------------------------------------------------------------------------- */

function HeroSection() {
  const { t } = useTranslation();
  const [copied, setCopied] = useState(false);
  const titleRef = useRef<HTMLHeadingElement>(null);
  const subtitleRef = useRef<HTMLParagraphElement>(null);
  const ctaContainerRef = useRef<HTMLDivElement>(null);
  const heroGlowRef = useRef<HTMLDivElement>(null);
  const ctaButtonLeftRef = useRef<HTMLAnchorElement>(null);
  const ctaButtonRightRef = useRef<HTMLAnchorElement>(null);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText('pip install unified-ads-mcp');
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch { /* clipboard not available */ }
  };

  useEffect(() => {
    if (!titleRef.current) return;
    const h1 = titleRef.current;
    if (prefersReducedMotion()) {
      h1.style.opacity = '1';
      h1.querySelectorAll('[data-hero-word]').forEach((el) => { (el as HTMLElement).style.opacity = '1'; });
      const gs = h1.querySelector('[data-hero-gradient]') as HTMLElement | null;
      if (gs) gs.style.opacity = '1';
      return;
    }
    h1.style.opacity = '1';
    const words = h1.querySelectorAll('[data-hero-word]');
    const gradientSpan = h1.querySelector('[data-hero-gradient]');
    const wordAnim = animate(words, {
      opacity: [0, 1], translateY: [30, 0], scale: [0.7, 1.05, 1], filter: ['blur(8px)', 'blur(0px)'],
      duration: 700, delay: stagger(80), ease: 'outQuart',
    });
    let gradientAnim: ReturnType<typeof animate> | null = null;
    if (gradientSpan) {
      (gradientSpan as HTMLElement).style.perspective = '600px';
      gradientAnim = animate(gradientSpan, {
        opacity: [0, 1], translateY: [40, 0], scale: [0.7, 1.08, 1], rotateX: [15, 0], filter: ['blur(8px)', 'blur(0px)'],
        duration: 900, delay: words.length * 80 + 100, ease: 'outBack',
      });
    }
    return () => { wordAnim.pause(); gradientAnim?.pause(); };
  }, [t]);

  useEffect(() => {
    if (!subtitleRef.current) return;
    if (prefersReducedMotion()) { subtitleRef.current.style.opacity = '1'; return; }
    const anim = animate(subtitleRef.current, {
      opacity: [0, 1], translateY: [25, 0], filter: ['blur(4px)', 'blur(0px)'],
      duration: 700, delay: 400, ease: 'outQuart',
    });
    return () => { anim.pause(); };
  }, []);

  useEffect(() => {
    if (!ctaContainerRef.current) return;
    const children = ctaContainerRef.current.children;
    if (!children.length) return;
    if (prefersReducedMotion()) {
      Array.from(children).forEach((el) => { (el as HTMLElement).style.opacity = '1'; });
      if (ctaButtonLeftRef.current) ctaButtonLeftRef.current.style.opacity = '1';
      if (ctaButtonRightRef.current) ctaButtonRightRef.current.style.opacity = '1';
      return;
    }
    const anims: ReturnType<typeof animate>[] = [];
    anims.push(animate(children[0], { opacity: [0, 1], duration: 400, delay: 600, ease: 'outQuart' }));
    if (ctaButtonLeftRef.current) anims.push(animate(ctaButtonLeftRef.current, { opacity: [0, 1], translateX: [-60, 0], scale: [0.9, 1], duration: 600, delay: 650, ease: 'outBack' }));
    if (ctaButtonRightRef.current) anims.push(animate(ctaButtonRightRef.current, { opacity: [0, 1], translateX: [60, 0], scale: [0.9, 1], duration: 600, delay: 750, ease: 'outBack' }));
    if (children[1]) anims.push(animate(children[1], { opacity: [0, 1], translateY: [20, 0], scale: [0.95, 1], duration: 500, delay: 900, ease: 'outQuart' }));
    return () => { anims.forEach((a) => a.pause()); };
  }, []);

  useEffect(() => {
    if (!heroGlowRef.current || prefersReducedMotion()) return;
    const anim = animate(heroGlowRef.current, { opacity: [0.4, 0.8], scale: [0.85, 1.2], loop: true, alternate: true, duration: 4000, ease: 'inOutSine' });
    return () => { anim.pause(); };
  }, []);

  const title1 = t('hero.title1', 'Your Ads Deserve');
  const title1Words = title1.split(/\s+/);

  return (
    <section className="relative py-20 md:py-32 lg:py-40 overflow-hidden">
      <AdBackground />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <div ref={heroGlowRef} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-[60%] w-[500px] h-[200px] md:w-[700px] md:h-[280px] bg-gradient-to-r from-indigo-500/25 via-purple-500/20 to-pink-500/25 blur-[100px] rounded-full pointer-events-none" aria-hidden="true" />
        <div style={{ perspective: '800px' }}>
          <h1 ref={titleRef} className="text-[3rem] md:text-[4.5rem] lg:text-[5.5rem] font-display font-bold tracking-tighter leading-[1.05]" style={{ opacity: 0 }}>
            {title1Words.map((word, i) => (
              <span key={i} data-hero-word className="inline-block mr-[0.3em]" style={{ opacity: 0 }}>{word}</span>
            ))}
            <span data-hero-gradient className="inline-block bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" style={{ opacity: 0, transformStyle: 'preserve-3d' }}>
              {t('hero.title2', 'a Co-Pilot')}
            </span>
          </h1>
        </div>
        <p ref={subtitleRef} className="mt-6 text-lg md:text-xl text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto leading-relaxed" style={{ opacity: 0 }}>
          {t('hero.subtitle', '180 tools across 6 advertising platforms. Manage campaigns, track conversions, and optimize performance through the Model Context Protocol.')}
        </p>
        <div ref={ctaContainerRef}>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4" style={{ opacity: 0 }}>
            <a ref={ctaButtonLeftRef} href="/docs" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-black text-sm font-semibold hover:scale-105 active:scale-[0.98] transition-transform shadow-lg shadow-zinc-900/20 dark:shadow-white/10" style={{ opacity: 0 }}>
              {t('hero.cta1', 'Get Started')} <ArrowRight size={16} weight="bold" />
            </a>
            <a ref={ctaButtonRightRef} href="https://github.com/Draivix/aidvertaiser" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full border border-zinc-300 dark:border-white/10 text-zinc-700 dark:text-zinc-300 text-sm font-semibold hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors" style={{ opacity: 0 }}>
              <GithubLogo size={18} weight="bold" /> {t('hero.cta2', 'View on GitHub')}
            </a>
          </div>
          <div className="mt-8 mx-4 sm:mx-auto max-w-full sm:w-fit grid grid-cols-[auto_1fr_auto] items-center gap-2 sm:gap-3 bg-zinc-900 dark:bg-zinc-800/80 text-zinc-300 rounded-xl px-3 sm:px-5 py-3 font-mono text-[11px] sm:text-sm border border-zinc-800 dark:border-zinc-700/50" style={{ opacity: 0 }}>
            <span className="text-zinc-500 select-none">$</span>
            <div className="overflow-x-auto whitespace-nowrap scrollbar-none select-all">{t('hero.install', 'pip install unified-ads-mcp')}</div>
            <button onClick={handleCopy} className="p-1 rounded hover:bg-white/10 transition-colors" aria-label="Copy install command">
              {copied ? <Check size={16} className="text-emerald-400" weight="bold" /> : <Copy size={16} className="text-zinc-500" />}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Trusted Platforms Bar                                                      */
/* -------------------------------------------------------------------------- */

function TrustedBar() {
  const { t } = useTranslation();
  const sectionRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLParagraphElement>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    if (!sectionRef.current) return;
    const badges = sectionRef.current.querySelectorAll('[data-platform-badge]');
    if (prefersReducedMotion()) {
      badges.forEach((el) => { (el as HTMLElement).style.opacity = '1'; });
      if (titleRef.current) titleRef.current.style.opacity = '1';
      return;
    }
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !hasAnimated.current) {
        hasAnimated.current = true;
        if (titleRef.current) animate(titleRef.current, { opacity: [0, 1], translateY: [-15, 0], duration: 500, ease: 'outQuart' });
        animate(badges, { opacity: [0, 1], scale: [0.5, 1.1, 1], translateY: [20, -5, 0], rotateZ: [-4, 2, 0], duration: 700, delay: stagger(80, { from: 'center' }), ease: 'outElastic(1, .6)' });
        observer.disconnect();
      }
    }, { threshold: 0.1, rootMargin: '-50px' });
    observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section className="relative py-12 md:py-16" aria-label={t('trustedBy.title', 'Manage advertising across')}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div ref={sectionRef} className="text-center">
          <p ref={titleRef} className="text-xs uppercase tracking-widest text-zinc-400 dark:text-zinc-500 font-medium mb-6" style={{ opacity: 0 }}>
            {t('trustedBy.title', 'Manage advertising across')}
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 md:gap-6">
            {supportedPlatforms.map((platform) => (
              <span key={platform} data-platform-badge className="px-5 py-2 rounded-full bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/5 font-mono text-sm text-zinc-600 dark:text-zinc-400 backdrop-blur-sm" style={{ opacity: 0 }}>
                {platform}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Feature Bento Grid                                                        */
/* -------------------------------------------------------------------------- */

function FeatureCard({ featureKey, Icon }: { featureKey: string; Icon: React.ElementType; index: number }) {
  const { t } = useTranslation();
  return (
    <div data-feature-card className="group relative rounded-2xl border border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-white/[0.02] backdrop-blur-xl p-6 overflow-hidden transition-shadow hover:shadow-lg hover:shadow-indigo-500/5 opacity-0">
      <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500 pointer-events-none" />
      <div data-feature-shimmer className="absolute inset-0 rounded-2xl pointer-events-none opacity-0" style={{ background: 'linear-gradient(90deg, transparent 0%, rgba(99,102,241,0.3) 50%, transparent 100%)', backgroundSize: '200% 100%', mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)', maskComposite: 'exclude', WebkitMaskComposite: 'xor', padding: '1px', borderRadius: 'inherit' }} />
      <div className="relative">
        <div data-feature-icon className="mb-4 inline-flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/20 dark:to-purple-500/20 text-indigo-500" style={{ transform: 'scale(0)' }}>
          <Icon size={24} weight="duotone" />
        </div>
        <h3 className="font-display font-semibold text-lg mb-2 text-zinc-900 dark:text-white">{t(`features.${featureKey}.title`, featureKey)}</h3>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">{t(`features.${featureKey}.description`, '')}</p>
      </div>
    </div>
  );
}

function FeaturesSection() {
  const { t } = useTranslation();
  const gridRef = useRef<HTMLDivElement>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    if (!gridRef.current || prefersReducedMotion()) {
      if (gridRef.current) {
        gridRef.current.querySelectorAll('[data-feature-card]').forEach((el) => { (el as HTMLElement).style.opacity = '1'; });
        gridRef.current.querySelectorAll('[data-feature-icon]').forEach((el) => { (el as HTMLElement).style.transform = 'scale(1)'; });
      }
      return;
    }
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !hasAnimated.current) {
        hasAnimated.current = true;
        const cards = gridRef.current!.querySelectorAll('[data-feature-card]');
        const icons = gridRef.current!.querySelectorAll('[data-feature-icon]');
        const shimmers = gridRef.current!.querySelectorAll('[data-feature-shimmer]');
        animate(cards, { opacity: [0, 1], scale: [0.85, 1], translateY: [60, 0], duration: 700, delay: stagger(80, { grid: [3, 2], from: 'first' }), ease: 'outQuart' });
        animate(icons, { scale: [0, 1.3, 1], duration: 600, delay: stagger(80, { grid: [3, 2], from: 'first', start: 300 }), ease: 'outElastic(1, .6)' });
        animate(shimmers, { opacity: [0, 0.8, 0], backgroundPosition: ['200% 0%', '-200% 0%'], duration: 1200, delay: stagger(80, { grid: [3, 2], from: 'first', start: 600 }), ease: 'inOutSine' });
        observer.disconnect();
      }
    }, { threshold: 0.15, rootMargin: '-60px' });
    observer.observe(gridRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section id="features" className="py-20 md:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ duration: 0.6 }} className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('features.title', 'Everything You Need')}</h2>
          <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">{t('features.subtitle', '180 tools spanning campaign management, conversion tracking, audience targeting, and cross-platform analytics.')}</p>
        </motion.div>
        <div ref={gridRef} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featureKeys.map(({ key, Icon }, index) => (
            <FeatureCard key={key} featureKey={key} Icon={Icon} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Pipeline / How It Works                                                   */
/* -------------------------------------------------------------------------- */

function PipelineStage({ stageKey, index }: { stageKey: string; index: number }) {
  const { t } = useTranslation();
  return (
    <div data-pipeline-stage className="flex flex-col items-center text-center flex-1 min-w-0" style={{ opacity: 0 }}>
      <div className="relative flex-shrink-0">
        <div data-pipeline-glow className="absolute inset-0 w-12 h-12 rounded-full bg-indigo-500/40 blur-lg opacity-0" />
        <div data-pipeline-circle className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-display font-bold text-sm shadow-lg shadow-indigo-500/25 relative z-10" style={{ transform: 'scale(0)' }}>{index + 1}</div>
      </div>
      <h3 className="mt-4 font-display font-semibold text-zinc-900 dark:text-white text-sm md:text-base">{t(`pipeline.stages.${stageKey}.title`, stageKey)}</h3>
      <p className="mt-1 text-xs md:text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed max-w-[160px]">{t(`pipeline.stages.${stageKey}.description`, '')}</p>
    </div>
  );
}

function PipelineSection() {
  const { t } = useTranslation();
  const stagesContainerRef = useRef<HTMLDivElement>(null);
  const mobileStagesRef = useRef<HTMLDivElement>(null);
  const hasAnimatedStages = useRef(false);

  useEffect(() => {
    const dc = stagesContainerRef.current;
    const mc = mobileStagesRef.current;
    const allStages: Element[] = [];
    if (dc) allStages.push(...Array.from(dc.querySelectorAll('[data-pipeline-stage]')));
    if (mc) allStages.push(...Array.from(mc.querySelectorAll('[data-pipeline-stage]')));
    if (!allStages.length) return;
    if (prefersReducedMotion()) {
      allStages.forEach((el) => { (el as HTMLElement).style.opacity = '1'; const c = el.querySelector('[data-pipeline-circle]') as HTMLElement | null; if (c) c.style.transform = 'scale(1)'; });
      return;
    }
    const target = dc || mc;
    if (!target) return;
    const animC = (container: HTMLElement) => {
      const stages = container.querySelectorAll('[data-pipeline-stage]');
      const circles = container.querySelectorAll('[data-pipeline-circle]');
      const glows = container.querySelectorAll('[data-pipeline-glow]');
      if (!stages.length) return;
      animate(stages, { opacity: [0, 1], translateY: [30, 0], scale: [0.9, 1], duration: 500, delay: stagger(120, { from: 'first' }), ease: 'outQuart' });
      animate(circles, { scale: [0, 1.2, 1], duration: 600, delay: stagger(120, { from: 'first', start: 200 }), ease: 'outElastic(1, .6)' });
      animate(glows, { opacity: [0, 0.8, 0], scale: [0.8, 1.8, 1], duration: 800, delay: stagger(120, { from: 'first', start: 300 }), ease: 'outQuart' });
    };
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !hasAnimatedStages.current) {
        hasAnimatedStages.current = true;
        if (dc) animC(dc);
        if (mc) animC(mc);
        observer.disconnect();
      }
    }, { threshold: 0.1, rootMargin: '-60px' });
    observer.observe(target);
    return () => observer.disconnect();
  }, []);

  return (
    <section id="how-it-works" className="py-20 md:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: '-100px' }} transition={{ duration: 0.6 }} className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight text-zinc-900 dark:text-white">{t('pipeline.title', 'How It Works')}</h2>
          <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">{t('pipeline.subtitle', 'From installation to optimized campaigns in four simple steps.')}</p>
        </motion.div>
        <div className="hidden md:flex items-start justify-center relative">
          <div ref={stagesContainerRef} className="flex items-start justify-center w-full gap-4">
            {pipelineStageKeys.map((key, i) => <PipelineStage key={key} stageKey={key} index={i} />)}
          </div>
        </div>
        <div ref={mobileStagesRef} className="md:hidden grid grid-cols-2 gap-8">
          {pipelineStageKeys.map((key, i) => <PipelineStage key={key} stageKey={key} index={i} />)}
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Terminal Demo                                                             */
/* -------------------------------------------------------------------------- */

function TypewriterLine({ line, startTime }: { line: (typeof terminalLines)[number]; startTime: number }) {
  const lineRef = useRef<HTMLDivElement>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    if (!lineRef.current || hasAnimated.current || !line.text) return;
    hasAnimated.current = true;
    if (prefersReducedMotion()) { lineRef.current.textContent = line.text.replace(/\{(\d+)\}/g, '$1'); return; }
    const el = lineRef.current;
    const parts = line.text.split(/(\{\d+\})/g);
    el.innerHTML = '';
    const spans: HTMLSpanElement[] = [];
    const counterSpans: { span: HTMLSpanElement; target: number }[] = [];
    for (const part of parts) {
      const numMatch = part.match(/^\{(\d+)\}$/);
      if (numMatch) {
        const span = document.createElement('span'); span.textContent = '0'; span.style.opacity = '0'; span.style.display = 'inline';
        el.appendChild(span); spans.push(span); counterSpans.push({ span, target: parseInt(numMatch[1], 10) });
      } else {
        for (const char of part) { const span = document.createElement('span'); span.textContent = char; span.style.opacity = '0'; span.style.display = 'inline'; el.appendChild(span); spans.push(span); }
      }
    }
    const charDelay = Math.min(30, 600 / Math.max(spans.length, 1));
    const tl = createTimeline({ autoplay: true, delay: startTime });
    tl.add(spans, { opacity: [0, 1], duration: 50, delay: stagger(charDelay), ease: 'out' });
    for (const { span, target } of counterSpans) {
      const obj = { val: 0 };
      animate(obj, { val: target, duration: 800, delay: startTime + spans.indexOf(span) * charDelay + 100, ease: 'outExpo', onUpdate: () => { span.textContent = String(Math.round(obj.val)); } });
    }
    return () => { tl.pause(); };
  }, [line.text, startTime]);

  if (!line.text) return <div className={`${line.color} whitespace-pre`}>{'\u00A0'}</div>;
  return <div ref={lineRef} className={`${line.color} whitespace-pre`} />;
}

function TerminalCursor({ visible }: { visible: boolean }) {
  const cursorRef = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!visible || !cursorRef.current || prefersReducedMotion()) return;
    const anim = animate(cursorRef.current, { opacity: [1, 0.2, 1], duration: 800, loop: true, ease: 'steps(2)' });
    return () => { anim.pause(); };
  }, [visible]);
  if (!visible) return null;
  return <span ref={cursorRef} className="inline-block w-[8px] h-[14px] bg-zinc-300 ml-0.5 align-middle" />;
}

function TerminalDemo() {
  const termRef = useRef<HTMLDivElement>(null);
  const terminalContainerRef = useRef<HTMLDivElement>(null);
  const shimmerRef = useRef<HTMLDivElement>(null);
  const isInView = useInView(termRef, { once: true, margin: '-100px' });
  const [showCursor, setShowCursor] = useState(false);
  const [terminalReady, setTerminalReady] = useState(false);

  useEffect(() => {
    if (!isInView || !terminalContainerRef.current) return;
    if (prefersReducedMotion()) { terminalContainerRef.current.style.transform = 'scaleY(1)'; terminalContainerRef.current.style.opacity = '1'; setTerminalReady(true); return; }
    const anim = animate(terminalContainerRef.current, { scaleY: [0, 1], opacity: [0, 1], duration: 500, ease: 'outBack', onComplete: () => setTerminalReady(true) });
    return () => { anim.pause(); };
  }, [isInView]);

  useEffect(() => {
    if (!terminalReady) return;
    setShowCursor(true);
    const totalTime = terminalLines[terminalLines.length - 1].delay * 1000 + 2000;
    const shimmerTimer = setTimeout(() => { if (shimmerRef.current && !prefersReducedMotion()) animate(shimmerRef.current, { opacity: [0, 0.3, 0], translateX: ['-100%', '200%'], duration: 1000, ease: 'inOutSine' }); }, totalTime - 500);
    const cursorTimer = setTimeout(() => setShowCursor(false), totalTime);
    return () => { clearTimeout(shimmerTimer); clearTimeout(cursorTimer); };
  }, [terminalReady]);

  return (
    <section id="demo" className="py-20 md:py-32" aria-label="Terminal demo">
      <div ref={termRef} className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div ref={terminalContainerRef} className="rounded-2xl bg-zinc-900 dark:bg-zinc-950 border border-zinc-800 dark:border-zinc-800/60 shadow-2xl shadow-black/20 overflow-hidden origin-top" style={{ transform: 'scaleY(0)', opacity: 0 }} role="img" aria-label="Terminal showing Aidvertaiser creating a search campaign with 12 keywords, 3 ads, and $50/day budget">
          <div className="flex items-center gap-2 px-5 py-3 border-b border-zinc-800 dark:border-zinc-800/60" aria-hidden="true">
            <div className="w-3 h-3 rounded-full bg-red-500/80" /><div className="w-3 h-3 rounded-full bg-yellow-500/80" /><div className="w-3 h-3 rounded-full bg-green-500/80" />
            <span className="ml-3 text-xs text-zinc-500 font-mono">terminal</span>
          </div>
          <div className="p-5 md:p-6 font-mono text-xs md:text-sm leading-relaxed overflow-x-auto relative">
            <div ref={shimmerRef} className="absolute inset-0 pointer-events-none opacity-0" style={{ background: 'linear-gradient(90deg, transparent 0%, rgba(99,102,241,0.15) 50%, transparent 100%)', width: '50%' }} aria-hidden="true" />
            {terminalReady && terminalLines.map((line, i) => <TypewriterLine key={i} line={line} startTime={line.delay * 1000} />)}
            {showCursor && <div className="inline-flex items-center"><TerminalCursor visible={showCursor} /></div>}
          </div>
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  CTA Section                                                               */
/* -------------------------------------------------------------------------- */

function CtaSection() {
  const { t } = useTranslation();
  const glowRef = useRef<HTMLDivElement>(null);
  const buttonGlowRef = useRef<HTMLDivElement>(null);
  const ctaContentRef = useRef<HTMLDivElement>(null);
  const buttonShineRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (prefersReducedMotion()) return;
    const g = glowRef.current ? animate(glowRef.current, { opacity: [0.3, 0.8], scale: [0.9, 1.1], loop: true, alternate: true, duration: 4000, ease: 'inOutSine' }) : null;
    const b = buttonGlowRef.current ? animate(buttonGlowRef.current, { opacity: [0.4, 0.8], scale: [0.95, 1.08], loop: true, alternate: true, duration: 3000, ease: 'inOutSine' }) : null;
    return () => { g?.pause(); b?.pause(); };
  }, []);

  useEffect(() => {
    if (!buttonShineRef.current || prefersReducedMotion()) return;
    const anim = animate(buttonShineRef.current, { translateX: ['-100%', '300%'], duration: 1500, loop: true, delay: 3000, ease: 'inOutSine' });
    return () => { anim.pause(); };
  }, []);

  useEffect(() => {
    if (!ctaContentRef.current || prefersReducedMotion()) return;
    const el = ctaContentRef.current;
    const observer = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) { animate(el, { opacity: [0, 1], translateY: [50, 0], rotateY: [3, 0], duration: 800, ease: 'outQuart' }); observer.disconnect(); } }, { threshold: 0.2 });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section id="get-started" className="py-20 md:py-32 bg-zinc-900 dark:bg-zinc-950 text-white relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div ref={glowRef} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-r from-indigo-500/30 via-purple-500/20 to-pink-500/30 blur-[120px] rounded-full" />
      </div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative" style={{ perspective: '1000px' }}>
        <div ref={ctaContentRef} className="text-center" style={{ opacity: 0, transformStyle: 'preserve-3d' }}>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold tracking-tight">{t('cta.title', 'Start Managing Ads with AI')}</h2>
          <p className="mt-4 text-lg text-zinc-400 max-w-xl mx-auto">{t('cta.subtitle', 'Install Aidvertaiser and connect your advertising platforms in minutes. Open source, MIT-licensed.')}</p>
          <div className="mt-10 relative inline-block">
            <div ref={buttonGlowRef} className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-full blur-lg opacity-60" aria-hidden="true" />
            <a href="/docs" className="relative inline-flex items-center gap-2 px-8 py-4 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-semibold text-sm hover:scale-105 active:scale-[0.98] transition-transform shadow-xl overflow-hidden">
              <div ref={buttonShineRef} className="absolute inset-0 pointer-events-none" aria-hidden="true" style={{ background: 'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%)', width: '40%' }} />
              <span className="relative z-10 flex items-center gap-2">{t('cta.button', 'Get Started')} <ArrowRight size={16} weight="bold" /></span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  HomePage                                                                  */
/* -------------------------------------------------------------------------- */

export default function HomePage() {
  const homeJsonLd = buildGraphJsonLd([
    organizationEntity(),
    founderEntity(),
    webPageEntity(SITE_URL, 'Aidvertaiser - AI-Powered Advertising MCP Server | 180 Tools, 6 Platforms', 'AI-powered advertising management through the Model Context Protocol. 180 tools across Google Ads, Meta Ads, GA4, Search Console, Matomo, and Bing. Open source.'),
  ]);

  return (
    <>
      <SEO
        title="Aidvertaiser - AI-Powered Advertising MCP Server | 180 Tools, 6 Platforms"
        description="AI-powered advertising management through the Model Context Protocol. 180 tools across Google Ads, Meta Ads, GA4, Search Console, Matomo, and Bing. Open source, MIT-licensed."
        canonical={SITE_URL}
        jsonLd={homeJsonLd}
      />
      <HeroSection />
      <TrustedBar />
      <FeaturesSection />
      <PipelineSection />
      <TerminalDemo />
      <CtaSection />
    </>
  );
}
