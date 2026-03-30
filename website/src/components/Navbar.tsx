import { useState, useRef, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { supportedLanguages, languageNames, changeLanguageSafe, resolveLanguage } from '@/i18n';
import type { SupportedLanguage } from '@/i18n';
import { motion, AnimatePresence } from 'motion/react';
import { animate, stagger } from 'animejs';
import { prefersReducedMotion } from '@/hooks/useAnime';
import {
  BookOpen,
  BookBookmark,
  Briefcase,
  CalendarBlank,
  CaretDown,
  ChartBar,
  ChartLineUp,
  Code,
  CurrencyDollar,
  GithubLogo,
  Globe,
  GraduationCap,
  Handshake,
  IdentificationBadge,
  Info,
  Lightbulb,
  List,
  MagnifyingGlass,
  MapPin,
  Megaphone,
  Moon,
  Newspaper,
  Question,
  Robot,
  Scan,
  ShieldStar,
  Sun,
  Target,
  Terminal,
  TrendUp,
  UsersThree,
  X,
} from '@phosphor-icons/react';

interface MegaMenuItem {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  desc: string;
  href?: string;
}

interface MegaMenuCategory {
  name: string;
  items: MegaMenuItem[];
}

const megaMenuData: MegaMenuCategory[] = [
  {
    name: 'menu.platforms.name',
    items: [
      { icon: Globe, title: 'menu.platforms.googleAds.title', desc: 'menu.platforms.googleAds.desc', href: '/platforms/google-ads' },
      { icon: UsersThree, title: 'menu.platforms.metaAds.title', desc: 'menu.platforms.metaAds.desc', href: '/platforms/meta-ads' },
      { icon: ChartLineUp, title: 'menu.platforms.ga4.title', desc: 'menu.platforms.ga4.desc', href: '/platforms/google-analytics' },
      { icon: MagnifyingGlass, title: 'menu.platforms.searchConsole.title', desc: 'menu.platforms.searchConsole.desc', href: '/platforms/search-console' },
      { icon: ChartBar, title: 'menu.platforms.matomo.title', desc: 'menu.platforms.matomo.desc', href: '/platforms/matomo' },
      { icon: Globe, title: 'menu.platforms.bing.title', desc: 'menu.platforms.bing.desc', href: '/platforms/bing-webmaster' },
    ],
  },
  {
    name: 'menu.capabilities.name',
    items: [
      { icon: Megaphone, title: 'menu.capabilities.campaigns.title', desc: 'menu.capabilities.campaigns.desc', href: '/capabilities/campaign-management' },
      { icon: Target, title: 'menu.capabilities.conversions.title', desc: 'menu.capabilities.conversions.desc', href: '/capabilities/conversion-tracking' },
      { icon: UsersThree, title: 'menu.capabilities.audiences.title', desc: 'menu.capabilities.audiences.desc', href: '/capabilities/audience-targeting' },
      { icon: ChartLineUp, title: 'menu.capabilities.analytics.title', desc: 'menu.capabilities.analytics.desc', href: '/capabilities/analytics-reporting' },
      { icon: MagnifyingGlass, title: 'menu.capabilities.seo.title', desc: 'menu.capabilities.seo.desc', href: '/capabilities/seo-indexing' },
      { icon: CurrencyDollar, title: 'menu.capabilities.budget.title', desc: 'menu.capabilities.budget.desc', href: '/capabilities/budget-bidding' },
    ],
  },
  {
    name: 'menu.useCases.name',
    items: [
      { icon: Megaphone, title: 'menu.useCases.multiPlatform.title', desc: 'menu.useCases.multiPlatform.desc', href: '/use-cases/multi-platform-campaigns' },
      { icon: ChartLineUp, title: 'menu.useCases.crossAnalytics.title', desc: 'menu.useCases.crossAnalytics.desc', href: '/use-cases/cross-platform-analytics' },
      { icon: Target, title: 'menu.useCases.conversionOpt.title', desc: 'menu.useCases.conversionOpt.desc', href: '/use-cases/conversion-optimization' },
      { icon: MagnifyingGlass, title: 'menu.useCases.searchPerf.title', desc: 'menu.useCases.searchPerf.desc', href: '/use-cases/search-performance' },
      { icon: UsersThree, title: 'menu.useCases.audienceResearch.title', desc: 'menu.useCases.audienceResearch.desc', href: '/use-cases/audience-research' },
      { icon: ShieldStar, title: 'menu.useCases.fraudPrevention.title', desc: 'menu.useCases.fraudPrevention.desc', href: '/use-cases/click-fraud-prevention' },
    ],
  },
  {
    name: 'menu.integrations.name',
    items: [
      { icon: Robot, title: 'menu.integrations.claude.title', desc: 'menu.integrations.claude.desc', href: '/integrations/claude-desktop' },
      { icon: Code, title: 'menu.integrations.cursor.title', desc: 'menu.integrations.cursor.desc', href: '/integrations/cursor' },
      { icon: Terminal, title: 'menu.integrations.vscode.title', desc: 'menu.integrations.vscode.desc', href: '/integrations/vscode-continue' },
      { icon: Scan, title: 'menu.integrations.windsurf.title', desc: 'menu.integrations.windsurf.desc', href: '/integrations/windsurf' },
      { icon: Terminal, title: 'menu.integrations.cline.title', desc: 'menu.integrations.cline.desc', href: '/integrations/cline' },
      { icon: Code, title: 'menu.integrations.custom.title', desc: 'menu.integrations.custom.desc', href: '/integrations/custom-ai-apps' },
    ],
  },
  {
    name: 'menu.resources.name',
    items: [
      { icon: BookOpen, title: 'menu.resources.ppcGuide.title', desc: 'menu.resources.ppcGuide.desc', href: '/resources/ppc-master-guide' },
      { icon: UsersThree, title: 'menu.resources.audienceGuide.title', desc: 'menu.resources.audienceGuide.desc', href: '/resources/audience-targeting-guide' },
      { icon: CurrencyDollar, title: 'menu.resources.biddingGuide.title', desc: 'menu.resources.biddingGuide.desc', href: '/resources/bidding-strategies' },
      { icon: Target, title: 'menu.resources.landingPages.title', desc: 'menu.resources.landingPages.desc', href: '/resources/landing-page-optimization' },
      { icon: ShieldStar, title: 'menu.resources.fraudGuide.title', desc: 'menu.resources.fraudGuide.desc', href: '/resources/click-fraud-prevention' },
      { icon: ChartLineUp, title: 'menu.resources.analysisGuide.title', desc: 'menu.resources.analysisGuide.desc', href: '/resources/campaign-analysis' },
    ],
  },
  {
    name: 'menu.about.name',
    items: [
      { icon: Info, title: 'menu.about.company.title', desc: 'menu.about.company.desc', href: '/about#company' },
      { icon: IdentificationBadge, title: 'menu.about.leadership.title', desc: 'menu.about.leadership.desc', href: '/about#leadership' },
      { icon: Briefcase, title: 'menu.about.careers.title', desc: 'menu.about.careers.desc', href: '/about#careers' },
      { icon: Newspaper, title: 'menu.about.press.title', desc: 'menu.about.press.desc', href: '/about#press' },
      { icon: TrendUp, title: 'menu.about.investors.title', desc: 'menu.about.investors.desc', href: '/about#investors' },
      { icon: Handshake, title: 'menu.about.partners.title', desc: 'menu.about.partners.desc', href: '/about#partners' },
      { icon: MapPin, title: 'menu.about.contact.title', desc: 'menu.about.contact.desc', href: '/about#contact' },
      { icon: Lightbulb, title: 'menu.about.blog.title', desc: 'menu.about.blog.desc', href: '/blog' },
      { icon: CalendarBlank, title: 'menu.about.events.title', desc: 'menu.about.events.desc', href: '/about#events' },
      { icon: UsersThree, title: 'menu.about.stories.title', desc: 'menu.about.stories.desc', href: '/about#stories' },
    ],
  },
  {
    name: 'menu.docs.name',
    items: [
      { icon: BookOpen, title: 'menu.docs.gettingStarted.title', desc: 'menu.docs.gettingStarted.desc', href: '/docs' },
      { icon: Code, title: 'menu.docs.apiReference.title', desc: 'menu.docs.apiReference.desc', href: '/docs#api-reference' },
      { icon: Terminal, title: 'menu.docs.configuration.title', desc: 'menu.docs.configuration.desc', href: '/docs#configuration' },
      { icon: ShieldStar, title: 'menu.docs.authentication.title', desc: 'menu.docs.authentication.desc', href: '/docs#authentication' },
      { icon: GraduationCap, title: 'menu.docs.tutorials.title', desc: 'menu.docs.tutorials.desc', href: '/docs#tutorials' },
      { icon: BookBookmark, title: 'menu.docs.faq.title', desc: 'menu.docs.faq.desc', href: '/docs#faq' },
      { icon: Question, title: 'menu.docs.faq.title', desc: 'menu.docs.faq.desc', href: '/docs#faq' },
    ],
  },
];

/* -------------------------------------------------------------------------- */
/*  NavMegaphoneLogo -- small animated SVG megaphone for the navbar logo      */
/* -------------------------------------------------------------------------- */

function NavMegaphoneLogo() {
  return (
    <Megaphone
      size={28}
      weight="duotone"
      className="text-indigo-500"
      aria-hidden="true"
    />
  );
}

/* -------------------------------------------------------------------------- */

interface NavbarProps {
  isDark: boolean;
  toggleTheme: () => void;
}

export default function Navbar({ isDark, toggleTheme }: NavbarProps) {
  const { t, i18n } = useTranslation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [expandedMobileMenu, setExpandedMobileMenu] = useState<string | null>(null);
  const [isLangOpen, setIsLangOpen] = useState(false);
  const [isChangingLang, setIsChangingLang] = useState(false);
  const langRef = useRef<HTMLDivElement>(null);

  const currentLang = resolveLanguage(i18n.language) ?? 'en';

  const handleLanguageChange = useCallback(async (lang: SupportedLanguage) => {
    if (lang === currentLang) {
      setIsLangOpen(false);
      return;
    }
    setIsChangingLang(true);
    try {
      await changeLanguageSafe(lang);
    } finally {
      setIsChangingLang(false);
      setIsLangOpen(false);
    }
  }, [currentLang]);
  const megaMenuRef = useRef<HTMLDivElement>(null);
  const mobileMenuRef = useRef<HTMLDivElement>(null);

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isMenuOpen]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (langRef.current && !langRef.current.contains(e.target as Node)) {
        setIsLangOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        setActiveMenu(null);
        setIsLangOpen(false);
        setIsMenuOpen(false);
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Desktop mega-menu item stagger animation
  useEffect(() => {
    if (!activeMenu) return;

    const container = megaMenuRef.current;
    if (!container) return;

    // If user prefers reduced motion, show items immediately without animation
    if (prefersReducedMotion()) {
      const items = container.querySelectorAll('[data-menu-item]');
      items.forEach((el) => {
        (el as HTMLElement).style.opacity = '1';
      });
      return;
    }

    // Reset all items to invisible immediately
    const items = container.querySelectorAll('[data-menu-item]');
    items.forEach((el) => {
      (el as HTMLElement).style.opacity = '0';
    });

    // Brief delay to let the framer-motion height transition start
    const timer = setTimeout(() => {
      const container = megaMenuRef.current;
      if (!container) return;
      const items = container.querySelectorAll('[data-menu-item]');
      if (items.length === 0) return;

      animate(items, {
        opacity: [0, 1],
        translateY: [12, 0],
        scale: [0.95, 1],
        duration: 300,
        delay: stagger(30),
        ease: 'outQuart',
      });
    }, 100);

    return () => clearTimeout(timer);
  }, [activeMenu]);

  // Mobile menu item stagger animation
  useEffect(() => {
    if (!expandedMobileMenu) return;

    const container = mobileMenuRef.current;
    if (!container) return;

    // If user prefers reduced motion, show items immediately without animation
    if (prefersReducedMotion()) {
      const items = container.querySelectorAll('[data-mobile-item]');
      items.forEach((el) => {
        (el as HTMLElement).style.opacity = '1';
      });
      return;
    }

    // Reset all items to invisible immediately
    const items = container.querySelectorAll('[data-mobile-item]');
    items.forEach((el) => {
      (el as HTMLElement).style.opacity = '0';
    });

    const timer = setTimeout(() => {
      const container = mobileMenuRef.current;
      if (!container) return;
      const items = container.querySelectorAll('[data-mobile-item]');
      if (items.length === 0) return;

      animate(items, {
        opacity: [0, 1],
        translateX: [-10, 0],
        duration: 250,
        delay: stagger(25),
        ease: 'outQuart',
      });
    }, 80);

    return () => clearTimeout(timer);
  }, [expandedMobileMenu]);

  const activeCategory = megaMenuData.find(c => c.name === activeMenu);

  return (
    <>
    <nav
      aria-label="Main navigation"
      className="fixed top-0 left-0 right-0 z-50 border-b border-zinc-200/50 dark:border-white/5 bg-white/50 dark:bg-[#030303]/50 backdrop-blur-xl"
      onMouseLeave={() => setActiveMenu(null)}
    >
      <div className="w-full px-4 sm:px-6 lg:px-10">
        <div className="relative flex items-center justify-between h-16">
          <div className="flex items-center gap-2 shrink-0">
            <Link to="/" className="flex items-center gap-2 font-display font-bold text-xl tracking-tighter">
              <NavMegaphoneLogo />
              <span>
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">Aid</span>
                <span className="text-zinc-900 dark:text-white">vertaiser</span>
              </span>
            </Link>
          </div>

          {/* Desktop Megamenu Items */}
          <div className="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2">
            {megaMenuData.map((category) => (
              <button
                key={category.name}
                onMouseEnter={() => setActiveMenu(category.name)}
                onClick={() => setActiveMenu(activeMenu === category.name ? null : category.name)}
                aria-expanded={activeMenu === category.name}
                aria-haspopup="true"
                className={`px-3 py-2 text-[13px] font-medium transition-colors flex items-center gap-1 rounded-lg whitespace-nowrap ${
                  activeMenu === category.name
                    ? 'text-zinc-900 dark:text-white bg-zinc-100 dark:bg-white/10'
                    : 'text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white'
                }`}
              >
                {t(category.name)}
                <CaretDown aria-hidden="true" className={`w-3 h-3 transition-transform duration-200 ${activeMenu === category.name ? 'rotate-180' : ''}`} />
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            {/* Language Switcher Dropdown */}
            <div ref={langRef} className="hidden lg:block relative">
              <button
                onClick={() => setIsLangOpen(!isLangOpen)}
                aria-label="Select language"
                aria-expanded={isLangOpen}
                aria-haspopup="true"
                disabled={isChangingLang}
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[11px] font-medium bg-zinc-100/50 dark:bg-white/5 border border-zinc-200/50 dark:border-white/5 text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition-colors disabled:opacity-50"
              >
                {isChangingLang ? (
                  <span className="w-3 h-3 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin" />
                ) : (
                  currentLang.toUpperCase()
                )}
                <CaretDown aria-hidden="true" className={`w-3 h-3 transition-transform duration-200 ${isLangOpen ? 'rotate-180' : ''}`} />
              </button>
              <AnimatePresence>
                {isLangOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -4 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -4 }}
                    transition={{ duration: 0.15, ease: 'easeOut' }}
                    className="absolute right-0 top-full mt-1.5 min-w-[140px] rounded-lg bg-white/90 dark:bg-[#111]/90 backdrop-blur-xl border border-zinc-200/50 dark:border-white/10 shadow-lg overflow-hidden"
                  >
                    {supportedLanguages.map((lang) => (
                      <button
                        key={lang}
                        onClick={() => handleLanguageChange(lang)}
                        disabled={isChangingLang}
                        className={`w-full px-3 py-2 text-[12px] font-medium text-left transition-colors flex items-center gap-2 ${
                          currentLang === lang
                            ? 'bg-zinc-100 dark:bg-white/10 text-zinc-900 dark:text-white'
                            : 'text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-white/5 hover:text-zinc-900 dark:hover:text-white'
                        } disabled:opacity-50`}
                      >
                        <span className="w-5 text-[10px] text-zinc-400 dark:text-zinc-500 uppercase">{lang}</span>
                        <span>{languageNames[lang]}</span>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <button
              onClick={toggleTheme}
              className="p-2 rounded-full hover:bg-zinc-100 dark:hover:bg-white/10 transition-colors"
              aria-label="Toggle theme"
            >
              {isDark ? <Sun aria-hidden="true" className="w-4 h-4" /> : <Moon aria-hidden="true" className="w-4 h-4" />}
            </button>
            <Link
              to="/docs"
              className="hidden lg:inline-flex items-center justify-center px-5 py-2 text-sm font-medium text-white bg-zinc-900 dark:bg-white dark:text-black rounded-full hover:scale-105 transition-transform duration-300 shadow-[0_0_20px_rgba(0,0,0,0.1)] dark:shadow-[0_0_20px_rgba(255,255,255,0.1)]"
            >
              {t('nav.getStarted')}
            </Link>
            <button
              className="lg:hidden p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={isMenuOpen}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <List className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Desktop Megamenu Dropdown */}
      <AnimatePresence>
        {activeMenu && activeCategory && (
          <motion.div
            key="megamenu-dropdown"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="hidden lg:block overflow-hidden border-t border-zinc-200/50 dark:border-white/5 bg-white/80 dark:bg-[#030303]/80 backdrop-blur-xl shadow-xl"
            ref={megaMenuRef}
          >
            <div className="w-full px-4 sm:px-6 lg:px-10 py-8">
              <div className={`grid grid-cols-2 gap-1 ${activeCategory.items.length > 8 ? 'lg:grid-cols-4' : 'lg:grid-cols-3'}`}>
                {activeCategory.items.map((item) => {
                  const content = (
                    <>
                      <div className="w-10 h-10 rounded-lg bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center text-indigo-600 dark:text-indigo-400 shrink-0 group-hover/item:scale-110 transition-transform">
                        <item.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-zinc-900 dark:text-white mb-1">{t(item.title)}</div>
                        <div className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">{t(item.desc)}</div>
                      </div>
                    </>
                  );

                  return item.href ? (
                    <Link
                      key={item.title}
                      to={item.href}
                      onClick={() => setActiveMenu(null)}
                      data-menu-item
                      style={{ opacity: 0 }}
                      className="flex items-start gap-4 p-4 rounded-xl hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors group/item"
                    >
                      {content}
                    </Link>
                  ) : (
                    <div
                      key={item.title}
                      data-menu-item
                      style={{ opacity: 0 }}
                      className="flex items-start gap-4 p-4 rounded-xl hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors group/item"
                    >
                      {content}
                    </div>
                  );
                })}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>

    {/* Mobile Menu -- rendered OUTSIDE nav to avoid backdrop-filter containing block */}
    <AnimatePresence>
      {isMenuOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-x-0 top-16 bottom-0 z-[60] bg-white/95 dark:bg-[#030303]/95 backdrop-blur-xl lg:hidden overflow-y-auto overscroll-contain touch-pan-y"
          ref={mobileMenuRef}
        >
          <div className="px-4 py-2">
            {/* Mobile Language Switcher */}
            <div className="flex flex-wrap items-center gap-1.5 py-3 mb-2">
              {supportedLanguages.map((lang) => (
                <button
                  key={lang}
                  onClick={() => handleLanguageChange(lang)}
                  disabled={isChangingLang}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    currentLang === lang
                      ? 'bg-zinc-200 dark:bg-white/15 text-zinc-900 dark:text-white'
                      : 'text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 bg-zinc-100 dark:bg-white/5'
                  } disabled:opacity-50`}
                >
                  {languageNames[lang]}
                </button>
              ))}
            </div>

            {megaMenuData.map((category) => (
              <div key={category.name} className="border-b border-zinc-200/50 dark:border-white/5">
                <button
                  onClick={() => setExpandedMobileMenu(expandedMobileMenu === category.name ? null : category.name)}
                  aria-expanded={expandedMobileMenu === category.name}
                  className="w-full flex items-center justify-between py-4 text-sm font-medium text-zinc-900 dark:text-white"
                >
                  {t(category.name)}
                  <CaretDown aria-hidden="true" className={`w-4 h-4 text-zinc-400 transition-transform duration-200 ${expandedMobileMenu === category.name ? 'rotate-180' : ''}`} />
                </button>
                <AnimatePresence>
                  {expandedMobileMenu === category.name && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3, ease: 'easeOut' }}
                      className="overflow-hidden"
                    >
                      <div className="pb-4 grid gap-1">
                        {category.items.map((item) => {
                          const content = (
                            <>
                              <item.icon className="w-4 h-4 text-indigo-500 shrink-0" />
                              <div>
                                <span className="text-sm text-zinc-900 dark:text-white">{t(item.title)}</span>
                                <p className="text-xs text-zinc-500 dark:text-zinc-400">{t(item.desc)}</p>
                              </div>
                            </>
                          );

                          return item.href ? (
                            <Link
                              key={item.title}
                              to={item.href}
                              onClick={() => setIsMenuOpen(false)}
                              data-mobile-item
                              style={{ opacity: 0 }}
                              className="flex items-center gap-3 p-3 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors"
                            >
                              {content}
                            </Link>
                          ) : (
                            <div
                              key={item.title}
                              data-mobile-item
                              style={{ opacity: 0 }}
                              className="flex items-center gap-3 p-3 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors"
                            >
                              {content}
                            </div>
                          );
                        })}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
            <div className="py-4">
              <Link
                to="/docs"
                onClick={() => setIsMenuOpen(false)}
                className="block w-full px-5 py-3 text-sm font-medium text-white bg-zinc-900 dark:bg-white dark:text-black rounded-full hover:scale-105 transition-transform duration-300 text-center"
              >
                {t('nav.getStarted')}
              </Link>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
    </>
  );
}
