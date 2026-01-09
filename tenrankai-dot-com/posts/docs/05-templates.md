+++
title = "Template Customization"
summary = "Learn how to customize Tenrankai's templates and create custom themes"
date = "2026-01-09"
+++

# Template Customization

Tenrankai uses the [Liquid template engine](https://shopify.github.io/liquid/) to render all pages. This guide covers how to customize templates, create custom themes, and understand the template system.

## Template Structure

Tenrankai organizes templates in three main directories:

```
templates/
├── pages/          # Full page templates
├── modules/        # Reusable components  
└── partials/       # Shared template fragments
```

### Pages Directory

Contains complete page templates:

- `index.html.liquid` - Homepage template
- `about.html.liquid` - About page template
- `features.html.liquid` - Features page template
- `contact.html.liquid` - Contact page template  
- `404.html.liquid` - Error page template
- `passkeys.html.liquid` - Passkey management page

### Modules Directory

Contains reusable components for specific functionality:

- `gallery.html.liquid` - Photo gallery grid
- `image_detail.html.liquid` - Individual photo view
- `posts_index.html.liquid` - Blog/docs listing page
- `post_detail.html.liquid` - Individual blog/doc post
- `login.html.liquid` - Authentication login form
- `profile.html.liquid` - User profile page

### Partials Directory

Contains shared template fragments:

- `_header.html.liquid` - Site header and navigation
- `_footer.html.liquid` - Site footer
- `_gallery_preview.html.liquid` - Gallery thumbnail preview
- `_user_menu.html.liquid` - User authentication menu

## Available Variables

### Global Variables

Available in all templates:

```liquid
{{ app_name }}          # Application name from config
{{ current_year }}      # Current year for copyright
{{ request_path }}      # Current request path
{{ user }}              # Current authenticated user (if any)
{{ is_authenticated }}  # Boolean authentication status
```

### Page-Specific Variables

#### Gallery Templates

```liquid
{{ gallery }}           # Gallery object with metadata
{{ gallery.name }}      # Gallery name
{{ gallery.description }} # Gallery description
{{ gallery.url_prefix }} # Gallery URL prefix
{{ images }}            # Array of images in gallery
{{ folders }}           # Array of subfolders
{{ breadcrumbs }}       # Navigation breadcrumb array
```

#### Image Detail Templates

```liquid
{{ image }}             # Current image object
{{ image.filename }}    # Image filename
{{ image.caption }}     # Image caption (from .txt file)
{{ image.width }}       # Image width in pixels
{{ image.height }}      # Image height in pixels
{{ image.url_original }} # Original image URL
{{ image.url_large }}   # Large version URL
{{ image.url_medium }}  # Medium version URL
{{ image.url_thumbnail }} # Thumbnail URL
{{ prev_image }}        # Previous image in gallery
{{ next_image }}        # Next image in gallery
```

#### Posts Templates

```liquid
{{ posts }}             # Array of blog posts or docs
{{ post }}              # Individual post object
{{ post.title }}        # Post title
{{ post.summary }}      # Post summary
{{ post.date }}         # Post date
{{ post.content }}      # Rendered post content (HTML)
{{ post.url }}          # Post URL path
```

## Customizing Existing Templates

### 1. Basic Customization

To customize a template, simply edit the `.liquid` files:

```liquid
<!-- Example: Customizing the header -->
<header class="site-header">
    <div class="container">
        <h1><a href="/">{{ app_name }}</a></h1>
        <nav>
            <ul>
                <li><a href="/features">Features</a></li>
                <li><a href="/gallery">Gallery</a></li>
                <li><a href="/docs">Docs</a></li>
                <li><a href="/blog">Blog</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
    </div>
</header>
```

### 2. Adding Custom CSS

Reference custom CSS in your templates:

```liquid
<!-- In pages/index.html.liquid -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ app_name }}</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="/static/custom.css">
</head>
<body>
    <!-- Your custom content -->
</body>
</html>
```

Then place your custom CSS in `static/custom.css`.

### 3. Conditional Content

Use Liquid conditionals for dynamic content:

```liquid
{% if is_authenticated %}
    <p>Welcome back, {{ user.username }}!</p>
    <a href="/profile">Profile</a>
    <a href="/logout">Logout</a>
{% else %}
    <a href="/login">Login</a>
{% endif %}
```

## Gallery Template Customization

### 1. Grid Layout

Customize the gallery grid in `modules/gallery.html.liquid`:

```liquid
<div class="gallery-grid">
    {% for image in images %}
        <div class="gallery-item">
            <a href="{{ image.url }}">
                <img src="{{ image.url_thumbnail }}" 
                     alt="{{ image.caption | default: image.filename }}"
                     loading="lazy">
            </a>
            {% if image.caption %}
                <div class="caption">{{ image.caption }}</div>
            {% endif %}
        </div>
    {% endfor %}
</div>
```

### 2. Image Detail Page

Enhance the image detail view in `modules/image_detail.html.liquid`:

```liquid
<div class="image-detail">
    <div class="image-container">
        <img src="{{ image.url_large }}" 
             alt="{{ image.caption | default: image.filename }}"
             width="{{ image.width }}" 
             height="{{ image.height }}">
    </div>
    
    {% if image.caption %}
        <div class="image-caption">
            {{ image.caption | markdownify }}
        </div>
    {% endif %}
    
    <div class="image-navigation">
        {% if prev_image %}
            <a href="{{ prev_image.url }}" class="nav-prev">← Previous</a>
        {% endif %}
        
        {% if next_image %}
            <a href="{{ next_image.url }}" class="nav-next">Next →</a>
        {% endif %}
    </div>
    
    <div class="image-metadata">
        <p>Filename: {{ image.filename }}</p>
        <p>Dimensions: {{ image.width }} × {{ image.height }}</p>
    </div>
</div>
```

## Blog and Documentation Templates

### 1. Posts Index

Customize the posts listing in `modules/posts_index.html.liquid`:

```liquid
<div class="posts-index">
    {% for post in posts %}
        <article class="post-preview">
            <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
            <div class="post-meta">
                <time datetime="{{ post.date | date: '%Y-%m-%d' }}">
                    {{ post.date | date: '%B %d, %Y' }}
                </time>
            </div>
            {% if post.summary %}
                <div class="post-summary">
                    {{ post.summary }}
                </div>
            {% endif %}
        </article>
    {% endfor %}
</div>
```

### 2. Post Detail

Enhance individual posts in `modules/post_detail.html.liquid`:

```liquid
<article class="post-detail">
    <header class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
            <time datetime="{{ post.date | date: '%Y-%m-%d' }}">
                {{ post.date | date: '%B %d, %Y' }}
            </time>
        </div>
    </header>
    
    <div class="post-content">
        {{ post.content }}
    </div>
    
    <footer class="post-footer">
        <div class="tags">
            <!-- Add tag support if implemented -->
        </div>
        
        <div class="sharing">
            <!-- Add social sharing buttons -->
        </div>
    </footer>
</article>
```

## Creating Custom Themes

### 1. Theme Structure

Create a theme by organizing your templates and assets:

```
my-theme/
├── templates/
│   ├── pages/
│   ├── modules/
│   └── partials/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── theme.toml
```

### 2. Theme Configuration

Create `theme.toml` to define theme metadata:

```toml
[theme]
name = "My Custom Theme"
version = "1.0.0"
author = "Your Name"
description = "A custom theme for Tenrankai"

[assets]
css = ["css/main.css", "css/gallery.css"]
js = ["js/main.js"]
```

### 3. Base Layout Template

Create a base layout in `templates/base.html.liquid`:

```liquid
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if page_title %}{{ page_title }} | {% endif %}{{ app_name }}</title>
    
    <!-- Theme CSS -->
    <link rel="stylesheet" href="/static/css/main.css">
    <link rel="stylesheet" href="/static/css/gallery.css">
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="{{ page_description | default: 'Photo gallery powered by Tenrankai' }}">
    
    {% block head %}{% endblock %}
</head>
<body>
    {% include 'partials/_header' %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% include 'partials/_footer' %}
    
    <!-- Theme JavaScript -->
    <script src="/static/js/main.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### 4. Extend Base Layout

Extend the base layout in page templates:

```liquid
{% extends 'base.html.liquid' %}

{% block head %}
    <link rel="stylesheet" href="/static/css/homepage.css">
{% endblock %}

{% block content %}
    <section class="hero">
        <h1>Welcome to {{ app_name }}</h1>
        <p>Your photo gallery description here</p>
    </section>
    
    {% include 'partials/_gallery_preview' %}
{% endblock %}
```

## Advanced Customization

### 1. Custom Filters

While you cannot add custom Liquid filters directly, you can use the built-in filters creatively:

```liquid
<!-- Format dates -->
{{ post.date | date: '%B %d, %Y' }}

<!-- Truncate text -->
{{ post.summary | truncate: 150 }}

<!-- Convert markdown -->
{{ post.content | markdownify }}

<!-- URL encoding -->
{{ image.filename | url_encode }}

<!-- String manipulation -->
{{ gallery.name | upcase }}
{{ post.title | downcase | replace: ' ', '-' }}
```

### 2. Responsive Design

Use CSS media queries for responsive templates:

```css
/* In your static/css/main.css */
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}

@media (max-width: 768px) {
    .gallery-grid {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 0.5rem;
    }
}

@media (max-width: 480px) {
    .gallery-grid {
        grid-template-columns: 1fr;
    }
}
```

### 3. JavaScript Enhancement

Add interactive features with JavaScript:

```javascript
// In static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Lazy loading for images
    const images = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Keyboard navigation for galleries
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && window.prevImageUrl) {
            window.location.href = window.prevImageUrl;
        } else if (e.key === 'ArrowRight' && window.nextImageUrl) {
            window.location.href = window.nextImageUrl;
        }
    });
});
```

## Template Development Tips

### 1. Template Debugging

Add debugging output to templates:

```liquid
<!-- Debug: Show all available variables -->
{% comment %}
{{ . | json }}
{% endcomment %}

<!-- Debug: Show specific variable -->
<!-- Debug: gallery object = {{ gallery | json }} -->
```

### 2. Fallback Content

Always provide fallbacks for optional content:

```liquid
{{ image.caption | default: image.filename }}
{{ post.summary | default: post.title }}
{{ gallery.description | default: "Photo gallery" }}
```

### 3. Performance Considerations

- Use `loading="lazy"` for images below the fold
- Minimize template complexity for galleries with many images
- Consider using CSS sprites for small icons
- Optimize images in the `static` directory

### 4. Accessibility

Make your templates accessible:

```liquid
<!-- Proper alt text for images -->
<img src="{{ image.url_thumbnail }}" 
     alt="{{ image.caption | default: 'Photo: ' | append: image.filename }}"
     loading="lazy">

<!-- Semantic HTML structure -->
<nav aria-label="Gallery navigation">
    <ul>
        <li><a href="{{ prev_image.url }}" aria-label="Previous image">←</a></li>
        <li><a href="{{ next_image.url }}" aria-label="Next image">→</a></li>
    </ul>
</nav>

<!-- Focus management -->
<button onclick="openLightbox()" aria-expanded="false" aria-controls="lightbox">
    View full size
</button>
```

## Template Configuration

### Gallery-Specific Templates

You can configure different templates per gallery in your `config.toml`:

```toml
[[galleries]]
name = "portfolio"
url_prefix = "/portfolio"
source_directory = "photos/portfolio"
template_overrides = { gallery = "portfolio_gallery.html.liquid" }

[[galleries]]  
name = "events"
url_prefix = "/events"
source_directory = "photos/events"
template_overrides = { gallery = "events_gallery.html.liquid" }
```

### Template Inheritance

While Liquid doesn't have true inheritance, you can simulate it with includes:

```liquid
<!-- templates/layouts/gallery_base.html.liquid -->
<!DOCTYPE html>
<html>
<head>
    {% include 'partials/_head' %}
</head>
<body>
    {% include 'partials/_header' %}
    <main class="gallery-main">
        <!-- This will be replaced by including templates -->
        {{ content }}
    </main>
    {% include 'partials/_footer' %}
</body>
</html>
```

## Troubleshooting

### Common Template Errors

1. **Variable not found**: Use `| default` filters for optional variables
2. **Syntax errors**: Check Liquid syntax, especially closing tags
3. **Missing includes**: Ensure included templates exist in the correct directory
4. **CSS not loading**: Verify paths in `/static/` directory

### Testing Templates

- Restart Tenrankai after template changes
- Check server logs for template errors
- Use browser developer tools to debug CSS and JavaScript
- Test responsive design at different screen sizes

## Next Steps

With custom templates, you can:

- Create unique gallery experiences
- Build marketing sites like this one
- Add blog functionality with custom styling
- Integrate with external services via JavaScript

For more advanced customization:

- [Configuration Reference](/docs/02-configuration) - Configure template paths and behavior
- [Deployment Guide](/docs/03-deployment) - Deploy your custom theme to production
- [API Documentation](/docs/04-api) - Integrate with external systems

The Liquid template engine offers powerful features - explore the [official documentation](https://shopify.github.io/liquid/) for advanced techniques.