+++
title = "Theming"
summary = "Customize appearance with CSS variables and templates"
date = "2026-01-13"
+++

# Theming

Tenrankai supports complete visual customization through CSS variables and Liquid templates.

## Quick Theme Setup

1. Create a custom static directory:
   ```bash
   mkdir static-custom
   ```

2. Copy the theme override file:
   ```bash
   cp static/theme-override.css static-custom/
   ```

3. Configure cascading directories:
   ```toml
   [static_files]
   directories = ["static-custom", "static"]
   ```

4. Edit `static-custom/theme-override.css`

5. Restart Tenrankai

## CSS Variables

### Colors

```css
:root[data-theme="light"],
:root:not([data-theme]) {
    /* Backgrounds */
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --bg-card: #ffffff;
    --bg-hover: #f0f0f0;
    --header-bg: #ffffff;

    /* Text */
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --text-muted: #999999;

    /* Links */
    --link-color: #0066cc;
    --link-hover: #004499;

    /* Borders */
    --border-color: #e0e0e0;
}

:root[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2a2a2a;
    --bg-card: #333333;
    --bg-hover: #404040;
    --header-bg: #1a1a1a;

    --text-primary: #f0f0f0;
    --text-secondary: #aaaaaa;
    --text-muted: #777777;

    --link-color: #66b3ff;
    --link-hover: #99ccff;

    --border-color: #444444;
}
```

### Typography

```css
:root {
    --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-heading: var(--font-body);
    --font-mono: 'SF Mono', Monaco, 'Courier New', monospace;

    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.25rem;
    --font-size-xl: 1.5rem;
}
```

### Spacing

```css
:root {
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
}
```

## Example Themes

### Warm Sepia

```css
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600&display=swap');

:root[data-theme="light"],
:root:not([data-theme]) {
    --bg-primary: #faf8f5;
    --bg-secondary: #f5f0e8;
    --bg-card: #ffffff;
    --text-primary: #3d3d3d;
    --text-secondary: #6b6b6b;
    --link-color: #8b5a2b;
    --link-hover: #6b4423;
    --border-color: #e0d6c8;

    --font-body: 'Open Sans', sans-serif;
    --font-heading: 'Merriweather', Georgia, serif;
}

:root[data-theme="dark"] {
    --bg-primary: #1f1a15;
    --bg-secondary: #2a241d;
    --bg-card: #332b22;
    --text-primary: #e8e0d5;
    --text-secondary: #a89f94;
    --link-color: #d4a574;
    --link-hover: #e8c4a0;
    --border-color: #4a4035;
}
```

### Minimal Dark

```css
:root[data-theme="dark"],
:root:not([data-theme]) {
    --bg-primary: #000000;
    --bg-secondary: #111111;
    --bg-card: #1a1a1a;
    --text-primary: #ffffff;
    --text-secondary: #888888;
    --link-color: #ffffff;
    --link-hover: #cccccc;
    --border-color: #333333;
}

:root[data-theme="light"] {
    --bg-primary: #ffffff;
    --bg-secondary: #fafafa;
    --bg-card: #ffffff;
    --text-primary: #000000;
    --text-secondary: #666666;
    --link-color: #000000;
    --link-hover: #333333;
    --border-color: #e0e0e0;
}
```

## Custom Fonts

### Google Fonts

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap');

:root {
    --font-heading: 'Playfair Display', Georgia, serif;
    --font-body: 'Source Sans Pro', sans-serif;
}
```

### Self-Hosted Fonts

1. Add fonts to `static-custom/fonts/`
2. Define `@font-face`:

```css
@font-face {
    font-family: 'CustomFont';
    src: url('/static/fonts/CustomFont-Regular.woff2') format('woff2'),
         url('/static/fonts/CustomFont-Regular.woff') format('woff');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'CustomFont';
    src: url('/static/fonts/CustomFont-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
}

:root {
    --font-body: 'CustomFont', sans-serif;
}
```

## Safe CSS Classes

These classes are stable and safe for customization:

| Class | Element |
|-------|---------|
| `.gallery-grid` | Image grid container |
| `.gallery-item` | Individual image card |
| `.card` | Generic card component |
| `.navbar` | Navigation bar |
| `.container` | Content container |
| `.image-detail-content` | Image detail view |
| `.btn` | Buttons |
| `.btn-primary` | Primary action button |
| `.btn-secondary` | Secondary button |

## Template Customization

### Template Structure

```
templates/
├── pages/           # Full page templates
│   ├── index.html.liquid
│   ├── about.html.liquid
│   └── 404.html.liquid
├── modules/         # Feature templates
│   ├── gallery.html.liquid
│   ├── image_detail.html.liquid
│   ├── posts_index.html.liquid
│   └── post_detail.html.liquid
└── partials/        # Reusable fragments
    ├── _header.html.liquid
    ├── _footer.html.liquid
    └── _gallery_preview.html.liquid
```

### Overriding Templates

1. Create custom template directory:
   ```bash
   mkdir -p templates-custom/pages
   ```

2. Configure cascading:
   ```toml
   [templates]
   directories = ["templates-custom", "templates"]
   ```

3. Copy and modify specific templates:
   ```bash
   cp templates/pages/index.html.liquid templates-custom/pages/
   ```

### Template Variables

Common variables available in templates:

```liquid
{{ page_title }}           <!-- Page title -->
{{ meta_description }}     <!-- Meta description -->
{{ base_url }}            <!-- Site base URL -->
{{ current_year }}        <!-- Current year -->
{{ is_authenticated }}    <!-- User logged in? -->
{{ current_user }}        <!-- Current username -->
```

Gallery templates also get:

```liquid
{{ gallery_url }}         <!-- Gallery URL prefix -->
{{ images }}              <!-- Array of images -->
{{ folders }}             <!-- Array of subfolders -->
{{ breadcrumbs }}         <!-- Navigation breadcrumbs -->
{{ current_page }}        <!-- Pagination current page -->
{{ total_pages }}         <!-- Pagination total -->
```

### Custom Filters

```liquid
<!-- Cache-busted asset URL -->
{{ "style.css" | asset_url }}
<!-- Output: /static/style.css?v=1705123456 -->

<!-- Format dates -->
{{ image.date | date: "%B %d, %Y" }}
<!-- Output: January 15, 2026 -->
```

## Cascading Directories

Override specific files without copying everything:

```toml
[static_files]
directories = ["static-custom", "static-theme", "static"]

[templates]
directories = ["templates-brand", "templates"]
```

Files are searched left-to-right; first match wins.

**Use cases:**
- Brand-specific logos and colors
- Seasonal themes
- A/B testing
- Client-specific customization

## Dark/Light Mode

Tenrankai includes a built-in theme toggle. Support both modes in your CSS:

```css
/* Light mode (default) */
:root[data-theme="light"],
:root:not([data-theme]) {
    --bg-primary: #ffffff;
    --text-primary: #1a1a1a;
}

/* Dark mode */
:root[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --text-primary: #f0f0f0;
}
```

The `:root:not([data-theme])` selector handles the initial state before the user selects a preference.

## Tips

1. **Test both modes** - Always verify light and dark themes
2. **Use `font-display: swap`** - Prevents invisible text during font loading
3. **Override sparingly** - Cascade from defaults when possible
4. **Check mobile** - Test responsive breakpoints
5. **Validate contrast** - Ensure text is readable (WCAG AA minimum)

## Next Steps

- [Advanced Features](/docs/08-advanced) - S3 storage, AI analysis
- [API Reference](/docs/09-api) - Build custom integrations
