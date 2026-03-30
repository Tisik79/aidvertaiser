/* -------------------------------------------------------------------------- */
/*  Shared JSON-LD Schema Helpers — Aidvertaiser Marketing Website           */
/*  Centralizes @id references and entity definitions for the @graph pattern */
/* -------------------------------------------------------------------------- */

export const SITE_URL = 'https://aidvertaiser.com';
export const SITE_NAME = 'Aidvertaiser';

export function organizationEntity() {
  return {
    '@type': 'Organization',
    '@id': `${SITE_URL}/#organization`,
    name: SITE_NAME,
    url: SITE_URL,
    logo: { '@type': 'ImageObject', url: `${SITE_URL}/favicon.svg`, width: '512', height: '512' },
    sameAs: ['https://github.com/Draivix/aidvertaiser', 'https://x.com/aidvertaiser'],
    founder: { '@id': `${SITE_URL}/#founder` },
    foundingDate: '2025',
    parentOrganization: { '@type': 'Organization', name: 'Draivix', url: 'https://draivix.com' },
  };
}

export function founderEntity() {
  return {
    '@type': 'Person',
    '@id': `${SITE_URL}/#founder`,
    name: 'David Strejc',
    jobTitle: 'Founder & CEO',
    url: `${SITE_URL}/about`,
    sameAs: ['https://github.com/david-strejc', 'https://x.com/aidvertaiser'],
  };
}

export function webPageEntity(url: string, name: string, description: string) {
  return {
    '@type': 'WebPage',
    '@id': `${url}/#webpage`,
    url,
    name,
    description,
    isPartOf: { '@id': `${SITE_URL}/#website` },
    about: { '@id': `${SITE_URL}/#software` },
    inLanguage: 'en',
  };
}

export function buildGraphJsonLd(entities: object[]) {
  return { '@context': 'https://schema.org', '@graph': entities };
}
