# 🌐 Investigation Intelligence System - Website

## Overview

Professional marketing website for the Investigation Intelligence System.

## Features

- ✅ Modern, responsive design
- ✅ Animated interactions
- ✅ Mobile-friendly
- ✅ Fast loading
- ✅ SEO optimized
- ✅ Download page
- ✅ Documentation page
- ✅ Contact page

## Structure

```
website/
├── index.html              # Landing page
├── assets/
│   ├── css/
│   │   └── main.css       # Main stylesheet
│   ├── js/
│   │   └── main.js        # Interactive features
│   └── images/            # Images and logos
└── pages/
    ├── download.html      # Download page
    ├── docs.html          # Documentation
    └── contact.html       # Contact form
```

## Running Locally

### Option 1: Simple HTTP Server (Python)
```bash
cd website
python3 -m http.server 8000
# Open http://localhost:8000
```

### Option 2: Live Server (VS Code)
1. Install "Live Server" extension
2. Right-click index.html
3. Select "Open with Live Server"

### Option 3: Node.js
```bash
cd website
npx serve
# Open http://localhost:3000
```

## Deployment

### GitHub Pages
1. Push to GitHub
2. Go to Settings → Pages
3. Select branch: main
4. Folder: /website
5. Save

### Netlify
1. Drag and drop `website` folder to Netlify
2. Done!

### Vercel
```bash
cd website
vercel
```

### Custom Server
Upload `website/` contents to your web server.

## Customization

### Change Colors
Edit `assets/css/main.css`:
```css
:root {
    --primary: #667eea;  /* Change this */
    --secondary: #764ba2; /* And this */
}
```

### Add Logo
1. Add logo image to `assets/images/logo.png`
2. Update in `index.html`:
```html
<div class="nav-brand">
    <img src="assets/images/logo.png" alt="Logo">
    <span>Investigation Intelligence</span>
</div>
```

### Update Content
All content is in the HTML files. Simply edit the text!

## Pages

### Landing Page (`index.html`)
- Hero section with CTA
- Features showcase
- File types support
- Demo section
- Pricing table
- Final CTA

### Download Page (`pages/download.html`)
- Download options (TAR.GZ, ZIP, GitHub)
- What's included
- Quick start guide
- Support links

### Documentation Page (`pages/docs.html`)
- Getting started
- Installation guide
- Usage examples
- API reference
- FAQ

### Contact Page (`pages/contact.html`)
- Contact form
- Email
- Social links

## Performance

- ⚡ Loads in < 1 second
- 📦 Total size < 200 KB
- ✅ Lighthouse score: 95+
- 🎨 Modern CSS (no heavy frameworks)
- 🚀 Vanilla JavaScript (no jQuery)

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## SEO

- Meta tags optimized
- Semantic HTML
- Alt texts for images
- Proper heading structure
- Fast loading

## Analytics (Optional)

Add Google Analytics by adding before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## License

MIT License - Free to use and modify

## Support

For issues or questions, open an issue on GitHub or contact support.
