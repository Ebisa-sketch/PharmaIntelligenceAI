'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  Boxes,
  Check,
  ChevronDown,
  CircleHelp,
  ClipboardCheck,
  Database,
  HeartPulse,
  Layers3,
  LockKeyhole,
  Menu,
  Microscope,
  PackageCheck,
  ShieldCheck,
  Sparkles,
  Truck,
  UsersRound,
  X,
} from 'lucide-react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const forecastData = [
  { month: 'Jan', actual: 42, forecast: 39 },
  { month: 'Feb', actual: 34, forecast: 37 },
  { month: 'Mar', actual: 49, forecast: 44 },
  { month: 'Apr', actual: 43, forecast: 47 },
  { month: 'May', actual: 58, forecast: 53 },
  { month: 'Jun', actual: 51, forecast: 56 },
  { month: 'Jul', actual: 66, forecast: 62 },
];

const platformLinks = [
  { label: 'Platform', href: '#platform' },
  { label: 'Features', href: '#features' },
  { label: 'AI Intelligence', href: '#intelligence' },
  { label: 'How it works', href: '#how-it-works' },
  { label: 'About', href: '#trust' },
];

function Brand() {
  return (
    <Link href="/" className="brand" aria-label="PharmaIntelligence AI home">
      <span className="brand-mark" aria-hidden="true">
        <HeartPulse size={20} strokeWidth={2.2} />
        <span />
      </span>
      <span className="brand-name">
        Pharma<span>Intelligence</span>
        <small>AI</small>
      </span>
    </Link>
  );
}

function SectionHeading({
  eyebrow,
  title,
  description,
  align = 'left',
}: {
  eyebrow: string;
  title: string;
  description?: string;
  align?: 'left' | 'center';
}) {
  return (
    <div className={`section-heading section-heading-${align}`}>
      <span className="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      {description && <p>{description}</p>}
    </div>
  );
}

function DashboardPreview() {
  return (
    <div className="dashboard-shell" aria-label="Illustrative platform dashboard preview">
      <div className="dashboard-topbar">
        <div className="window-dots" aria-hidden="true"><i /><i /><i /></div>
        <span>PHARMAINTELLIGENCE <b>/</b> OVERVIEW</span>
        <span className="demo-tag"><span /> DEMO DATA</span>
      </div>
      <div className="dashboard-content">
        <div className="dashboard-heading">
          <div>
            <p className="dashboard-kicker">MONDAY, 14 OCTOBER 2024</p>
            <h3>Good morning, Amina</h3>
            <p>Here&apos;s your pharmaceutical inventory at a glance.</p>
          </div>
          <button type="button" className="period-button">Last 30 days <ChevronDown size={13} /></button>
        </div>

        <div className="preview-kpis">
          <div className="preview-kpi">
            <span>Medicines tracked</span>
            <strong>1,284</strong>
            <small><span className="kpi-dot blue-dot" /> Across 12 facilities</small>
          </div>
          <div className="preview-kpi">
            <span>Stockout risks</span>
            <strong>08 <em className="risk-pill">Needs review</em></strong>
            <small><span className="kpi-dot amber-dot" /> 3 critical · 5 elevated</small>
          </div>
          <div className="preview-kpi">
            <span>Expiry alerts</span>
            <strong>14</strong>
            <small><span className="kpi-dot green-dot" /> Batches to review</small>
          </div>
        </div>

        <div className="dashboard-grid">
          <div className="preview-panel forecast-panel">
            <div className="panel-title-row">
              <div><h4>Demand forecast</h4><p>Amoxicillin 500 mg · Units</p></div>
              <button type="button" className="icon-button" aria-label="Forecast options"><CircleHelp size={15} /></button>
            </div>
            <div className="chart-legend">
              <span><i className="legend-blue" /> Actual</span>
              <span><i className="legend-dashed" /> Predicted</span>
            </div>
            <div className="mini-chart">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={forecastData} margin={{ top: 8, right: 4, left: -26, bottom: 0 }}>
                  <CartesianGrid vertical={false} stroke="#edf1f6" />
                  <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} />
                  <YAxis hide domain={[20, 75]} />
                  <Tooltip contentStyle={{ border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 11 }} />
                  <Line type="monotone" dataKey="actual" stroke="#2563eb" strokeWidth={2.4} dot={false} />
                  <Line type="monotone" dataKey="forecast" stroke="#10b981" strokeWidth={2} strokeDasharray="4 4" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="preview-panel risk-panel">
            <div className="panel-title-row">
              <div><h4>Needs attention</h4><p>Prioritized for your review</p></div>
              <span className="count-badge">3</span>
            </div>
            <div className="risk-row">
              <span className="risk-icon critical"><Activity size={14} /></span>
              <div><strong>Insulin, human</strong><small>Projected stockout · 6 days</small></div>
              <ArrowUpRight size={14} className="risk-arrow" />
            </div>
            <div className="risk-row">
              <span className="risk-icon warning"><PackageCheck size={14} /></span>
              <div><strong>Oxytocin 10 IU</strong><small>Batch expiry · 28 days</small></div>
              <ArrowUpRight size={14} className="risk-arrow" />
            </div>
            <div className="risk-row">
              <span className="risk-icon success"><Truck size={14} /></span>
              <div><strong>Transfer opportunity</strong><small>Metformin · 2 facilities</small></div>
              <ArrowDownRight size={14} className="risk-arrow risk-green" />
            </div>
            <Link href="/dashboard" className="panel-link">Review recommendations <ArrowRight size={13} /></Link>
          </div>
        </div>
        <div className="dashboard-footnote"><Sparkles size={12} /> AI-generated insights are illustrative; review before acting.</div>
      </div>
    </div>
  );
}

const featureItems = [
  {
    number: '01',
    icon: Activity,
    title: 'AI Demand Forecasting',
    description: 'Anticipate what your facilities need with transparent, data-informed forecasts.',
    points: ['Analyze historical consumption', 'Compare forecasting models', 'Explore future demand'],
    className: 'feature-wide feature-forecast',
  },
  {
    number: '02',
    icon: ShieldCheck,
    title: 'Stockout Risk Intelligence',
    description: 'See emerging shortages early with a clear view of stock, consumption, and replenishment.',
    points: ['Highlight high-risk medicines', 'Review replenishment signals'],
    className: 'feature-stockout',
  },
  {
    number: '03',
    icon: PackageCheck,
    title: 'Expiry Prevention',
    description: 'Turn batch-level expiry visibility into timely, FEFO-informed inventory decisions.',
    points: ['Monitor medicine batches', 'Prioritize expiry risk'],
    className: 'feature-expiry',
  },
  {
    number: '04',
    icon: Truck,
    title: 'Smart Redistribution',
    description: 'Find potential transfers that account for donor and recipient facility needs.',
    points: ['Evaluate facility balances', 'Respect transfer constraints'],
    className: 'feature-redistribution',
  },
  {
    number: '05',
    icon: Microscope,
    title: 'Explainable AI',
    description: 'Understand the factors, assumptions, and uncertainty behind each recommendation.',
    points: ['Inspect prediction factors', 'Keep people in control'],
    className: 'feature-explainable',
  },
  {
    number: '06',
    icon: Database,
    title: 'Data Quality Intelligence',
    description: 'Build confidence in the data behind decisions by finding issues before analysis.',
    points: ['Flag missing or inconsistent records', 'Detect unusual movements'],
    className: 'feature-data',
  },
];

const processSteps = [
  { number: '01', title: 'Data collection', text: 'Import and validate pharmaceutical inventory records.', icon: Database },
  { number: '02', title: 'AI analysis', text: 'Analyze demand, stockout risks, and expiry risks.', icon: Layers3 },
  { number: '03', title: 'Intelligent recommendations', text: 'Generate explainable forecasts and optimization suggestions.', icon: Sparkles },
  { number: '04', title: 'Human decision', text: 'Authorized users review and approve operational recommendations.', icon: ClipboardCheck },
];

export default function HomePage() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 12);
    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const closeMenu = () => setMobileOpen(false);

  return (
    <main className="landing-page">
      <header className={`site-header${scrolled ? ' is-scrolled' : ''}`}>
        <div className="nav-wrap">
          <Brand />
          <nav className={`main-nav${mobileOpen ? ' nav-open' : ''}`} aria-label="Main navigation">
            {platformLinks.map((item) => (
              <a key={item.href} href={item.href} onClick={closeMenu}>{item.label}</a>
            ))}
            <div className="mobile-nav-actions">
              <Link href="/login" onClick={closeMenu}>Sign in</Link>
              <Link className="button button-primary" href="/dashboard" onClick={closeMenu}>Launch dashboard <ArrowRight size={15} /></Link>
            </div>
          </nav>
          <div className="nav-actions">
            <Link className="nav-signin" href="/login">Sign in</Link>
            <Link className="button button-primary nav-cta" href="/dashboard">Launch dashboard <ArrowRight size={15} /></Link>
          </div>
          <button
            type="button"
            className="mobile-menu-toggle"
            onClick={() => setMobileOpen((open) => !open)}
            aria-label={mobileOpen ? 'Close navigation menu' : 'Open navigation menu'}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X size={21} /> : <Menu size={21} />}
          </button>
        </div>
      </header>

      <section className="hero-section" id="platform">
        <div className="hero-inner page-container">
          <div className="hero-copy reveal">
            <div className="hero-eyebrow"><span className="eyebrow-pulse" /> NEXT-GENERATION PHARMACEUTICAL INTELLIGENCE</div>
            <h1>Predict smarter.<br /><span>Prevent shortages.</span><br />Protect medicine supply.</h1>
            <p className="hero-description">
              An explainable AI-powered decision-support platform that helps healthcare facilities forecast medicine demand, identify stockout risks, prevent pharmaceutical expiry, and optimize inventory redistribution.
            </p>
            <div className="hero-actions">
              <a href="#intelligence" className="button button-primary button-large">Explore platform <ArrowRight size={17} /></a>
              <Link href="/login" className="button button-secondary button-large">Sign in <ArrowRight size={16} /></Link>
            </div>
            <div className="hero-trust"><span className="trust-check"><Check size={13} /></span> Data-driven insights <i /> Explainable AI <i /> Human-controlled decisions</div>
          </div>
          <div className="hero-visual reveal reveal-delay">
            <div className="visual-orbit orbit-one" />
            <div className="visual-orbit orbit-two" />
            <DashboardPreview />
            <div className="floating-note"><span className="floating-note-icon"><Activity size={15} /></span><span><b>Insight, in context</b><small>Every signal has a story</small></span><ArrowUpRight size={14} /></div>
          </div>
        </div>
        <div className="hero-bottom-line" />
      </section>

      <section className="capabilities-strip" aria-label="Platform capabilities">
        <div className="page-container capability-list">
          <div className="capability-intro"><span className="eyebrow">ONE CONNECTED PLATFORM</span><strong>Clarity across the<br />medicine lifecycle.</strong></div>
          <div className="capability-item"><span className="capability-icon"><BarChart3 size={18} /></span><span>Demand<br />forecasting</span></div>
          <div className="capability-item"><span className="capability-icon icon-amber"><Activity size={18} /></span><span>Stockout risk<br />intelligence</span></div>
          <div className="capability-item"><span className="capability-icon icon-green"><PackageCheck size={18} /></span><span>Expiry<br />prevention</span></div>
          <div className="capability-item"><span className="capability-icon icon-violet"><Truck size={18} /></span><span>Inventory<br />optimization</span></div>
        </div>
      </section>

      <section className="features-section section-pad" id="features">
        <div className="page-container">
          <SectionHeading
            eyebrow="A MORE INFORMED WORKFLOW"
            title="Everything you need for smarter pharmaceutical decisions"
            description="Bring forecasting, risk visibility, and operational recommendations together in one clear view."
          />
          <div className="features-grid">
            {featureItems.map(({ number, icon: Icon, title, description, points, className }) => (
              <article className={`feature-card ${className}`} key={number}>
                <div className="feature-topline"><span className="feature-number">{number} / 06</span><span className="feature-icon"><Icon size={19} strokeWidth={1.8} /></span></div>
                <div className="feature-body">
                  <h3>{title}</h3>
                  <p>{description}</p>
                </div>
                <ul>
                  {points.map((point) => <li key={point}><Check size={13} />{point}</li>)}
                </ul>
                {number === '01' && <div className="feature-sparkline" aria-hidden="true"><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /></div>}
                {number === '04' && <div className="transfer-visual" aria-hidden="true"><span>Facility A<small>Surplus</small></span><i><ArrowRight size={16} /></i><span>Facility B<small>Need identified</small></span></div>}
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="process-section section-pad" id="how-it-works">
        <div className="page-container">
          <div className="process-header">
            <SectionHeading
              eyebrow="HOW IT WORKS"
              title="From raw records to a considered next step."
              description="A clear workflow that keeps data, models, and people connected."
            />
            <span className="process-side-note"><LockKeyhole size={15} /> Human approval stays in the loop</span>
          </div>
          <div className="process-track">
            {processSteps.map(({ number, title, text, icon: Icon }, index) => (
              <article className="process-step" key={number}>
                <div className="step-marker"><span>{number}</span><Icon size={17} /></div>
                {index < processSteps.length - 1 && <div className="step-connector" aria-hidden="true"><i /></div>}
                <p className="step-label">STEP {number}</p>
                <h3>{title}</h3>
                <p className="step-description">{text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="intelligence-section section-pad" id="intelligence">
        <div className="page-container">
          <div className="intelligence-intro">
            <SectionHeading
              eyebrow="A CLOSER LOOK AT THE INTELLIGENCE"
              title="See the signals behind the supply."
              description="Explore how forecast trends, risk indicators, and transfer possibilities can be brought into one reviewable workspace."
            />
            <span className="illustrative-label"><span /> Illustrative demonstration data</span>
          </div>
          <div className="intelligence-layout">
            <article className="intelligence-panel demand-panel">
              <div className="intelligence-panel-header">
                <div><span className="panel-overline">DEMAND FORECASTING</span><h3>Consumption, with context.</h3><p>Illustrative monthly units · Amoxicillin 500 mg</p></div>
                <span className="panel-select">7 months <ChevronDown size={13} /></span>
              </div>
              <div className="large-chart-legend">
                <span><i className="legend-blue" /> Actual demand</span>
                <span><i className="legend-green" /> Predicted demand</span>
                <span className="chart-demo-label">DEMO SERIES</span>
              </div>
              <div className="large-chart">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={forecastData} margin={{ top: 15, right: 15, bottom: 0, left: -18 }}>
                    <CartesianGrid stroke="#edf1f6" vertical={false} />
                    <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fontSize: 11, fill: '#8995a8' }} dy={10} />
                    <YAxis tickLine={false} axisLine={false} tick={{ fontSize: 10, fill: '#a2adbd' }} />
                    <Tooltip contentStyle={{ border: '1px solid #e2e8f0', borderRadius: 10, fontSize: 12, boxShadow: '0 8px 24px rgba(15, 23, 42, .08)' }} />
                    <Line type="monotone" dataKey="actual" name="Actual" stroke="#2563eb" strokeWidth={2.5} dot={{ r: 3, fill: '#2563eb', strokeWidth: 0 }} activeDot={{ r: 5 }} />
                    <Line type="monotone" dataKey="forecast" name="Predicted" stroke="#10b981" strokeWidth={2.5} strokeDasharray="5 5" dot={{ r: 3, fill: '#10b981', strokeWidth: 0 }} activeDot={{ r: 5 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="chart-insight"><Sparkles size={15} /><span><b>Forecast insight</b> — Predicted demand is shown alongside observed consumption for review.</span></div>
            </article>
            <div className="intelligence-side">
              <article className="intelligence-panel risk-visual-panel">
                <div className="intelligence-panel-header compact">
                  <div><span className="panel-overline">STOCKOUT RISK</span><h3>Signals to review</h3></div>
                  <span className="mini-status status-amber">DEMO</span>
                </div>
                <div className="risk-visual-row"><span>Insulin, human</span><span className="risk-level risk-high">Elevated</span><div className="risk-meter"><i style={{ width: '78%' }} /></div></div>
                <div className="risk-visual-row"><span>Oral rehydration salts</span><span className="risk-level risk-medium">Moderate</span><div className="risk-meter"><i style={{ width: '49%' }} /></div></div>
                <div className="risk-visual-row"><span>Amoxicillin 500 mg</span><span className="risk-level risk-low">Monitor</span><div className="risk-meter"><i style={{ width: '26%' }} /></div></div>
                <div className="risk-footnote">Risk levels are examples for interface demonstration.</div>
              </article>
              <article className="intelligence-panel expiry-panel">
                <div className="intelligence-panel-header compact">
                  <div><span className="panel-overline">BATCH EXPIRY</span><h3>Expiry horizon</h3></div>
                  <PackageCheck size={17} className="panel-header-icon" />
                </div>
                <div className="expiry-bar-group" aria-label="Illustrative batch expiry distribution">
                  <div><span>0–30 days</span><i><b className="bar-amber" style={{ width: '28%' }} /></i><strong>04</strong></div>
                  <div><span>31–90 days</span><i><b className="bar-blue" style={{ width: '56%' }} /></i><strong>09</strong></div>
                  <div><span>90+ days</span><i><b className="bar-green" style={{ width: '82%' }} /></i><strong>16</strong></div>
                </div>
                <span className="expiry-demo-note">Illustrative batch counts · not live inventory</span>
              </article>
            </div>
            <article className="redistribution-overview">
              <div className="redistribution-copy"><span className="panel-overline">INVENTORY REDISTRIBUTION</span><h3>Surface opportunities.<br /><span>Keep decisions local.</span></h3><p>Explore potential facility-to-facility transfers with donor availability, recipient needs, and review status visible together.</p><Link href="/dashboard" className="text-link">Explore recommendations <ArrowRight size={15} /></Link></div>
              <div className="route-visual">
                <div className="route-facility donor-facility"><span className="facility-pin"><Boxes size={16} /></span><span><b>Facility North</b><small>Potential surplus</small></span><em>DONOR</em></div>
                <div className="route-line"><i /><span><Truck size={14} /> Review transfer</span><i /></div>
                <div className="route-facility recipient-facility"><span className="facility-pin pin-recipient"><HeartPulse size={16} /></span><span><b>Facility Central</b><small>Potential need</small></span><em>RECIPIENT</em></div>
                <div className="route-note"><LockKeyhole size={13} /> Requires authorized human approval</div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section className="trust-section section-pad" id="trust">
        <div className="page-container trust-layout">
          <div className="trust-copy">
            <span className="eyebrow eyebrow-light">BUILT FOR RESPONSIBLE USE</span>
            <h2>Intelligent decisions.<br /><span>Responsible healthcare technology.</span></h2>
            <p>Designed to inform qualified teams—not replace their judgment. Every signal is there to support a more considered decision.</p>
            <Link href="/login" className="trust-link">Sign in to your workspace <ArrowRight size={15} /></Link>
          </div>
          <div className="trust-grid">
            <div className="trust-item"><span><UsersRound size={18} /></span><div><h3>Role-based access</h3><p>Workspace access is organized around user roles.</p></div></div>
            <div className="trust-item"><span><LockKeyhole size={18} /></span><div><h3>Secure data management</h3><p>Designed with careful data handling in mind.</p></div></div>
            <div className="trust-item"><span><Microscope size={18} /></span><div><h3>Explainable AI</h3><p>Understand the factors behind model outputs.</p></div></div>
            <div className="trust-item"><span><ClipboardCheck size={18} /></span><div><h3>Human approval</h3><p>Recommendations remain subject to review.</p></div></div>
            <div className="trust-item"><span><Activity size={18} /></span><div><h3>Audit trails</h3><p>Keep a record of important workspace activity.</p></div></div>
            <div className="trust-item"><span><ShieldCheck size={18} /></span><div><h3>Privacy-minded design</h3><p>Use data thoughtfully and with clear purpose.</p></div></div>
          </div>
        </div>
      </section>

      <section className="final-cta-section">
        <div className="page-container final-cta">
          <div className="cta-mark"><HeartPulse size={22} /></div>
          <span className="eyebrow">THE NEXT DECISION STARTS HERE</span>
          <h2>Make every pharmaceutical<br />inventory decision smarter.</h2>
          <p>Transform inventory data into actionable insights with AI-powered forecasting, risk intelligence, and optimization.</p>
          <div className="cta-actions">
            <Link href="/dashboard" className="button button-primary button-large">Launch platform <ArrowRight size={17} /></Link>
            <Link href="/login" className="button button-secondary button-large">Sign in</Link>
          </div>
        </div>
      </section>

      <footer className="site-footer">
        <div className="page-container footer-main">
          <div className="footer-brand-column">
            <Brand />
            <p>Pharmaceutical intelligence for a more informed supply chain.</p>
          </div>
          <div className="footer-links">
            <div><span>PLATFORM</span><a href="#platform">Overview</a><a href="#intelligence">AI intelligence</a><a href="#how-it-works">How it works</a></div>
            <div><span>CAPABILITIES</span><a href="#features">Features</a><a href="#features">Forecasting</a><a href="#features">Inventory insights</a></div>
            <div><span>COMPANY</span><a href="#trust">About</a><a href="#how-it-works">Documentation</a><a href="mailto:contact@pharmaintelligence.ai">Contact</a><Link href="/login">Sign in</Link></div>
          </div>
        </div>
        <div className="page-container footer-bottom">
          <span>© {new Date().getFullYear()} PharmaIntelligence AI. All rights reserved.</span>
          <span className="footer-note"><span /> Designed for informed, human-led decisions.</span>
        </div>
      </footer>
    </main>
  );
}
