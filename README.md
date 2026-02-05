# Bootcamp Presentation Slides

A modern, interactive web-based presentation system for your bootcamp sessions.

## Features

- 🎨 Beautiful, modern design with gradient themes
- ⌨️ Keyboard navigation (Arrow keys, Spacebar, Home, End)
- 📱 Touch/swipe support for mobile devices
- 🖱️ Click navigation buttons
- 📊 Multiple slide layouts (title, agenda, timeline, grid, etc.)
- 📱 Responsive design for all screen sizes

## Quick Start

1. Open `index.html` in your web browser
2. Navigate through slides using:
   - **Arrow keys** (← →) or **Spacebar** to advance
   - Click the **Previous/Next** buttons at the bottom
   - Swipe left/right on mobile devices

## Customizing Your Slides

### Adding a New Slide

Add a new `<section>` element inside the `.presentation-container`:

```html
<section class="slide">
    <div class="slide-content">
        <h1>Your Slide Title</h1>
        <p>Your content here</p>
    </div>
</section>
```

### Slide Types

#### Title Slide
```html
<section class="slide">
    <div class="slide-content title-slide">
        <h1>Main Title</h1>
        <h2>Subtitle</h2>
        <p class="subtitle">Additional info</p>
    </div>
</section>
```

#### Content with Grid
```html
<section class="slide">
    <div class="slide-content">
        <h1>Title</h1>
        <div class="content-grid">
            <div class="content-item">
                <h3>Item 1</h3>
                <p>Content</p>
            </div>
            <div class="content-item">
                <h3>Item 2</h3>
                <p>Content</p>
            </div>
        </div>
    </div>
</section>
```

#### Timeline
```html
<section class="slide">
    <div class="slide-content">
        <h1>Timeline</h1>
        <div class="timeline">
            <div class="timeline-item">
                <div class="timeline-marker">1</div>
                <div class="timeline-content">
                    <h3>Step 1</h3>
                    <p>Description</p>
                </div>
            </div>
        </div>
    </div>
</section>
```

#### Resource Cards
```html
<section class="slide">
    <div class="slide-content">
        <h1>Resources</h1>
        <div class="resources-grid">
            <div class="resource-card">
                <h3>📚 Title</h3>
                <p>Content</p>
            </div>
        </div>
    </div>
</section>
```

### Styling

- Edit `styles.css` to customize colors, fonts, and layouts
- The main gradient colors are defined in the CSS (currently purple/blue theme)
- All colors use CSS variables for easy customization

### Navigation

The presentation automatically:
- Updates slide counters
- Disables navigation buttons at first/last slide
- Supports keyboard shortcuts
- Handles touch gestures on mobile

## File Structure

```
Bootcamp/
├── index.html      # Main presentation file
├── styles.css      # Styling and themes
├── script.js       # Navigation and interactivity
└── README.md       # This file
```

## Tips

1. **Keep slides concise** - Each slide should focus on one main point
2. **Use consistent formatting** - Follow the existing slide patterns
3. **Test on different devices** - The presentation is responsive but preview on mobile too
4. **Practice navigation** - Familiarize yourself with keyboard shortcuts before presenting

## Browser Support

Works best in modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Customization Ideas

- Change the gradient colors in `styles.css` (search for `#667eea` and `#764ba2`)
- Add animations by modifying CSS transitions
- Include images by adding `<img>` tags in slide content
- Add code blocks with syntax highlighting
- Embed videos or interactive content

## Need Help?

Edit the HTML file directly - it's straightforward HTML/CSS/JavaScript. All slides follow the same basic structure, so you can easily copy and modify existing slides.





