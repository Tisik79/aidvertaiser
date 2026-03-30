import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ErrorBoundary from './components/ErrorBoundary';
import Layout from './components/Layout';

const HomePage = lazy(() => import('./pages/HomePage'));
const PlatformsPage = lazy(() => import('./pages/PlatformsPage'));
const PlatformDetailPage = lazy(() => import('./pages/PlatformDetailPage'));
const CapabilitiesPage = lazy(() => import('./pages/CapabilitiesPage'));
const CapabilityDetailPage = lazy(() => import('./pages/CapabilityDetailPage'));
const UseCasesPage = lazy(() => import('./pages/UseCasesPage'));
const UseCaseDetailPage = lazy(() => import('./pages/UseCaseDetailPage'));
const IntegrationsPage = lazy(() => import('./pages/IntegrationsPage'));
const IntegrationDetailPage = lazy(() => import('./pages/IntegrationDetailPage'));
const ResourcesPage = lazy(() => import('./pages/ResourcesPage'));
const ResourceDetailPage = lazy(() => import('./pages/ResourceDetailPage'));
const DocsPage = lazy(() => import('./pages/DocsPage'));
const BlogPage = lazy(() => import('./pages/BlogPage'));
const BlogPostPage = lazy(() => import('./pages/BlogPostPage'));
const AboutPage = lazy(() => import('./pages/AboutPage'));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'));

const PageLoader = (
  <div className="min-h-screen flex items-center justify-center">
    <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
  </div>
);

function Lazy({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={PageLoader}>{children}</Suspense>;
}

export default function App() {
  return (
    <ErrorBoundary>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Lazy><HomePage /></Lazy>} />
          <Route path="platforms" element={<Lazy><PlatformsPage /></Lazy>} />
          <Route path="platforms/:slug" element={<Lazy><PlatformDetailPage /></Lazy>} />
          <Route path="capabilities" element={<Lazy><CapabilitiesPage /></Lazy>} />
          <Route path="capabilities/:slug" element={<Lazy><CapabilityDetailPage /></Lazy>} />
          <Route path="use-cases" element={<Lazy><UseCasesPage /></Lazy>} />
          <Route path="use-cases/:slug" element={<Lazy><UseCaseDetailPage /></Lazy>} />
          <Route path="integrations" element={<Lazy><IntegrationsPage /></Lazy>} />
          <Route path="integrations/:slug" element={<Lazy><IntegrationDetailPage /></Lazy>} />
          <Route path="resources" element={<Lazy><ResourcesPage /></Lazy>} />
          <Route path="resources/:slug" element={<Lazy><ResourceDetailPage /></Lazy>} />
          <Route path="docs" element={<Lazy><DocsPage /></Lazy>} />
          <Route path="blog" element={<Lazy><BlogPage /></Lazy>} />
          <Route path="blog/:slug" element={<Lazy><BlogPostPage /></Lazy>} />
          <Route path="about" element={<Lazy><AboutPage /></Lazy>} />
          <Route path="*" element={<Lazy><NotFoundPage /></Lazy>} />
        </Route>
      </Routes>
    </BrowserRouter>
    </ErrorBoundary>
  );
}
