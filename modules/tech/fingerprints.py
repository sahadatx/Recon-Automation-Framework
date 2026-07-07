"""
Technology Fingerprints

Technology fingerprint database used by
the Technology Detection module.
"""

# ==========================================================
# Server Fingerprints
# ==========================================================

SERVER_FINGERPRINTS = {

    "cloudflare": "Cloudflare",

    "nginx": "Nginx",

    "apache": "Apache",

    "apache/": "Apache",

    "openresty": "OpenResty",

    "caddy": "Caddy",

    "litespeed": "LiteSpeed",

    "iis": "Microsoft IIS",

    "microsoft-iis": "Microsoft IIS",

    "gunicorn": "Gunicorn",

    "uvicorn": "Uvicorn",

    "envoy": "Envoy",

    "gws": "Google Web Server",

    "awselb": "AWS Load Balancer",

}


# ==========================================================
# Framework Fingerprints
# ==========================================================

FRAMEWORK_FINGERPRINTS = {

    "php": "PHP",

    "express": "Express",

    "expressjs": "Express",

    "asp.net": "ASP.NET",

    "aspnet": "ASP.NET",

    "django": "Django",

    "flask": "Flask",

    "laravel": "Laravel",

    "symfony": "Symfony",

    "spring": "Spring",

    "springboot": "Spring Boot",

    "rails": "Ruby on Rails",

    "next.js": "Next.js",

    "nextjs": "Next.js",

    "nuxt": "Nuxt.js",

    "vue": "Vue.js",

    "react": "React",

    "angular": "Angular",

    "svelte": "Svelte",

    "nestjs": "NestJS",

}


# ==========================================================
# CDN / WAF Fingerprints
# ==========================================================

CDN_FINGERPRINTS = {

    "cloudflare": "Cloudflare",

    "cf-cache-status": "Cloudflare",

    "cf-ray": "Cloudflare",

    "akamai": "Akamai",

    "akamaighost": "Akamai",

    "fastly": "Fastly",

    "x-served-by": "Fastly",

    "cloudfront": "Amazon CloudFront",

    "x-amz-cf-id": "Amazon CloudFront",

    "x-cache": "Amazon CloudFront",

    "sucuri": "Sucuri",

    "imperva": "Imperva",

}


# ==========================================================
# CMS Fingerprints
# ==========================================================

CMS_FINGERPRINTS = {

    "wordpress": "WordPress",

    "wp-content": "WordPress",

    "wp-includes": "WordPress",

    "drupal": "Drupal",

    "/sites/default/": "Drupal",

    "joomla": "Joomla",

    "com_content": "Joomla",

    "shopify": "Shopify",

    "magento": "Magento",

    "prestashop": "PrestaShop",

    "ghost": "Ghost CMS",

}


# ==========================================================
# HTML Keywords
# ==========================================================

HTML_KEYWORDS = {

    "WordPress": [

        "wp-content",

        "wp-includes",

        "wordpress",

    ],

    "Laravel": [

        "laravel",

        "csrf-token",

    ],

    "Django": [

        "csrfmiddlewaretoken",

        "__admin",

    ],

    "Flask": [

        "flask",

    ],

    "React": [

        "__react",

        "react-root",

        "react-dom",

    ],

    "Next.js": [

        "_next/",

        "__next",

    ],

    "Vue.js": [

        "__vue",

        "vue.js",

    ],

    "Angular": [

        "ng-version",

    ],

    "Bootstrap": [

        "bootstrap.min.css",

        "bootstrap.bundle",

    ],

    "Tailwind CSS": [

        "tailwindcss",

    ],

    "jQuery": [

        "jquery",

        "jquery.min.js",

    ],

}


# ==========================================================
# Hosting Platforms
# ==========================================================

HOSTING_FINGERPRINTS = {

    "github.io": "GitHub Pages",

    "vercel": "Vercel",

    "netlify": "Netlify",

    "firebase": "Firebase",

    "heroku": "Heroku",

    "render": "Render",

    "pages.dev": "Cloudflare Pages",

    "amazonaws": "Amazon Web Services",

}