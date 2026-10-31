# Cursor Prompt --- ProProstir: UX, Conversion, SEO & Technical Improvements

## Project context

Website: https://proprostir.com.ua/ Business direction to verify in the
repository/site: custom-made furniture in Dnipro (kitchens, wardrobes,
dressing rooms and related furniture). Main goal: improve qualified
enquiries and real customers. Also improve UX/UI, local SEO, technical
SEO, accessibility, performance and maintainability.

Act as a senior full-stack engineer, technical SEO specialist and
conversion-focused UX engineer. Work with the existing project. This is
an improvement task, NOT a rebuild.

## Non-negotiable rules

1.  Inspect the repository and current website before changing anything.
    Detect the actual framework, stack, routing, forms, integrations and
    deployment setup; do not assume.
2.  Preserve working functionality, existing routes, APIs, integrations,
    design identity and content unless a change is proven necessary.
3.  Do not replace frameworks, libraries, CMS, database, authentication
    or deployment architecture without explaining a compelling reason
    and obtaining approval.
4.  Do not make broad unrelated refactors. Work in small, reviewable
    phases.
5.  Never invent business facts: prices, guarantees, years of
    experience, completed-project counts, materials, brands, service
    areas, reviews, certifications or promises. Flag uncertain claims
    for owner confirmation.
6.  Never create fake reviews, ratings, project photos, credentials or
    misleading structured data.
7.  Never expose, print, commit or overwrite secrets. Do not modify
    `.env` values. Document missing variable NAMES only.
8.  Do not deploy, publish, migrate production data, change DNS or
    perform destructive operations.
9.  Do not silently change form/API contracts, field names, upload
    behavior or environment variable names.
10. Preserve the current visual identity. Improve clarity and conversion
    without making the site generic.
11. If a change requires missing information or owner approval, do not
    guess. Record the question.
12. Clearly distinguish confirmed defects from assumptions and
    recommendations.

## Customer journey

A visitor should quickly understand what ProProstir makes and where it
works, see credible completed projects, understand the process and
factors affecting price, then easily call/message/send an enquiry. The
business must reliably receive the enquiry and any attached
photos/drawings.

Use Ukrainian as the primary language if that is the current site
language. Preserve existing language versions and i18n routing.

# Phase 0 --- Audit only; no code changes

Inspect the repository and report: - Framework, language, package
manager, dependencies and entry points - Routes and page/component
structure - Styling system and responsive breakpoints - Image assets and
image delivery - Forms: validation, API endpoint, notifications, uploads
and error handling - Analytics and tracking - SEO: title, description,
canonical, robots, sitemap, Open Graph and JSON-LD - Tests,
lint/type-check/build commands - Deployment/runtime assumptions

Compare implementation with the rendered website where possible.

Produce a prioritized report containing: - Confirmed defects, with
evidence and affected routes/files - Potential issues requiring
browser/production verification - UX and conversion opportunities - SEO
and local SEO opportunities - Performance/accessibility risks -
Dependencies and owner decisions required

Do not call something broken merely because it is not obvious in source
code. Do not claim external Google indexation, PageSpeed or analytics
facts unless actually verified.

**Stop after Phase 0. Present the audit and proposed implementation
plan. Do not edit files until I approve the plan.**

# Phase 1 --- UX, conversion and responsive improvements

After approval, implement only changes supported by the audit.

## Homepage

Review the first screen on desktop and mobile. It should communicate: -
Custom-made furniture - Main categories actually offered - Dnipro /
confirmed service area - Main customer benefit - One clear primary CTA

Possible CTA wording (adapt to the existing workflow): "Розрахувати
вартість", "Надіслати фото для прорахунку", "Обговорити проєкт".

Improve copy only where needed. Do not add unverified promises.

## Enquiry form

Audit end-to-end before changing: - Required/optional fields - Client-
and server-side validation - Success/error/loading states - Duplicate
submission protection - Spam protection - Notifications and delivery
reliability - Upload size/type restrictions and failure handling -
Mobile usability and accessibility

Reduce friction without removing information the business needs. Do not
change backend contracts without updating and testing all dependent
code. If uploads exist, explain allowed formats and limits accurately.
Track a lead only after confirmed successful submission, and only if
analytics is correctly configured.

## Contacts

Verify phone, WhatsApp, Telegram and email links where present. Check
`tel:`, `mailto:` and messaging URLs, correct destinations and mobile
usability. Do not invent contact details or accounts.

## Portfolio

Make real projects easier to evaluate: - Clear title/category -
Responsive image gallery - Useful alt text - Project details only when
verified - Link to relevant service - CTA to request a similar project

Do not fabricate project locations, materials, dimensions or
specifications. List missing content fields for the owner.

## Trust

Clarify who performs the work, the
measurement/estimate/production/installation process, warranty terms,
price factors and contact process. Do not expand warranty claims beyond
confirmed terms. No fake testimonials, logos, partner badges or
certifications.

## Responsive UX and accessibility

Test representative mobile/tablet/desktop widths. Check horizontal
overflow, menus, contrast, typography, tap targets, image crops, forms,
keyboard navigation, focus states, semantic headings, accessible control
labels and reduced-motion preferences. Avoid unnecessary animations and
layout shifts.

# Phase 2 --- Technical SEO

Audit and safely improve according to the actual stack.

## Crawlability/indexation

Verify robots.txt, XML sitemap, indexability, internal links, HTTP
status codes, redirects and preferred host (HTTPS, www/non-www). Sitemap
should contain only canonical, indexable URLs. Do not block resources
needed to render pages.

## Metadata

For every indexable route, verify unique title, useful description,
canonical, locale/language metadata and Open Graph metadata. Avoid
keyword stuffing and duplicate placeholders.

## Structured data

Inspect existing JSON-LD first. Use only schema types/properties
supported by the real business and visible content. Consider
Organization, an appropriate LocalBusiness subtype, BreadcrumbList and
Service where valid. Do not invent address, coordinates, hours, prices,
ratings, reviews, social profiles or certifications. Avoid
duplicate/conflicting markup.

## Content and headings

Check one clear H1 per page, logical H2/H3 structure, descriptive links,
unique useful content and thin/duplicate pages. Do not create many
near-identical city/keyword pages or generic AI-written articles.

## Images

Review AVIF/WebP support, responsive sizing, dimensions to prevent CLS,
lazy loading below the fold, priority for the actual hero/LCP image,
useful alt text and image quality. Do not lazy-load the critical hero
image. Do not break galleries or rename assets without updating
references.

# Phase 3 --- Performance

Measure before optimizing. Use available local tooling and real
Lighthouse/PageSpeed results where possible. Review LCP, INP, CLS, image
weight, JS bundles, unused dependencies, render-blocking resources,
fonts, layout shifts, caching and compression.

Core Web Vitals guidance: - LCP \<= 2.5 seconds - INP \<= 200 ms - CLS
\<= 0.1

Do not claim targets are met without measurements. Avoid complex
infrastructure for marginal gains.

# Phase 4 --- Analytics and lead tracking

Inspect existing GA4/GTM before changing anything. If configured, verify
accurate events for phone clicks, WhatsApp, Telegram, successful form
submissions and important enquiry CTA clicks.

Never send personal data, phone numbers, names, message contents or
uploaded filenames to analytics. Do not count form opens, validation
errors or failed submissions as leads. Avoid duplicate events and
respect existing consent/privacy behavior. Do not invent IDs or create
new analytics properties. If configuration is missing, document what the
owner must supply.

# Phase 5 --- Local SEO readiness

Check consistency of public business name, phone, service area and other
confirmed details. Prepare a Google Business Profile checklist. Do not
claim/create external profiles or publish content/reviews. Do not expose
a residential address unless eligibility and owner approval are
confirmed.

# Testing and quality gates

After each approved phase: 1. Run existing lint, type-check and test
commands. 2. Run a production build. 3. Fix regressions introduced by
your changes. 4. Check all affected routes. 5. Test forms and uploads in
a safe local/staging environment where possible. 6. Check mobile and
desktop layouts. 7. Verify metadata, canonical URLs, sitemap and robots
output. 8. Review console/network errors where tooling permits.

Never report a test as passed unless it was actually run. Explain any
test that could not be run.

# Required workflow for every phase

1.  State findings and evidence.
2.  List exact files to modify.
3.  Explain expected behavior and risks.
4.  Make the smallest safe change.
5.  Run relevant checks.
6.  Summarize changed files and actual test results.
7.  List unresolved questions and owner-provided content needed.

Do not proceed to the next major phase if the current phase has
unresolved regressions.

# Final deliverables

At completion provide: - Executive summary of original problems -
Confirmed issues fixed - Improvements grouped by UX, SEO, performance
and analytics - Exact modified-file list - Commands/tests/builds run and
actual results - Remaining items requiring production access or owner
input - Next steps ordered by business impact - New required environment
variable names only (never values) - Manual verification checklist for
the owner

## First action --- important

Start with **Phase 0 only**. Inspect and report. Do not edit code,
install dependencies, run migrations, change configuration or deploy
during the initial audit.

The goal is not to make the code look different. The goal is to make
ProProstir more trustworthy, easier to use, technically sound and more
effective at generating real furniture enquiries while preserving the
existing working product.
