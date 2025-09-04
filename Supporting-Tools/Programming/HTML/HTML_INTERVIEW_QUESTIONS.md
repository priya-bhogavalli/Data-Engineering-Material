# HTML Interview Questions

## 📋 Table of Contents

1. [HTML Fundamentals (1-10)](#html-fundamentals-1-10)
2. [Semantic HTML & Accessibility (11-20)](#semantic-html--accessibility-11-20)
3. [Advanced HTML Features (21-30)](#advanced-html-features-21-30)

---

## HTML Fundamentals (1-10)

### 1. What is HTML and what does it stand for?
**Answer**: HTML stands for HyperText Markup Language. It's the standard markup language for creating web pages and web applications. HTML describes the structure and content of web pages using elements and tags.

### 2. What is the difference between HTML elements and tags?
**Answer**:
- **Tag**: The markup syntax (`<p>`, `</p>`)
- **Element**: The complete structure including opening tag, content, and closing tag
```html
<!-- Tag examples -->
<p>  <!-- Opening tag -->
</p> <!-- Closing tag -->

<!-- Element example -->
<p>This is a paragraph element</p>
<!-- The entire structure above is an element -->
```

### 3. What is the DOCTYPE declaration and why is it important?
**Answer**: DOCTYPE tells the browser which version of HTML the document uses:
```html
<!DOCTYPE html> <!-- HTML5 -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"> <!-- HTML 4.01 -->
```
**Importance**:
- Ensures proper rendering mode
- Prevents quirks mode
- Validates HTML structure

### 4. What are void/empty elements in HTML?
**Answer**: Elements that don't have closing tags and can't contain content:
```html
<br>     <!-- Line break -->
<hr>     <!-- Horizontal rule -->
<img>    <!-- Image -->
<input>  <!-- Form input -->
<meta>   <!-- Metadata -->
<link>   <!-- External resource link -->
<area>   <!-- Image map area -->
<base>   <!-- Base URL -->
<col>    <!-- Table column -->
<embed>  <!-- Embedded content -->
<source> <!-- Media resource -->
<track>  <!-- Text track -->
<wbr>    <!-- Word break opportunity -->
```

### 5. What is the difference between block and inline elements?
**Answer**:
**Block Elements**:
- Take full width available
- Start on new line
- Can contain other block and inline elements
```html
<div>, <p>, <h1>-<h6>, <ul>, <ol>, <li>, <section>, <article>
```

**Inline Elements**:
- Take only necessary width
- Don't start on new line
- Can only contain other inline elements
```html
<span>, <a>, <strong>, <em>, <img>, <input>, <label>
```

### 6. What are HTML attributes and how do you use them?
**Answer**: Attributes provide additional information about elements:
```html
<!-- Global attributes -->
<div id="container" class="main-content" data-role="navigation">

<!-- Element-specific attributes -->
<img src="image.jpg" alt="Description" width="300" height="200">
<a href="https://example.com" target="_blank" rel="noopener">Link</a>
<input type="email" name="email" required placeholder="Enter email">
```

### 7. What is the difference between id and class attributes?
**Answer**:
**ID Attribute**:
- Unique identifier (should be unique per page)
- Higher CSS specificity
- Used for JavaScript targeting
```html
<div id="header">Unique element</div>
```

**Class Attribute**:
- Can be used multiple times
- Lower CSS specificity
- Used for styling groups of elements
```html
<div class="card featured">Card 1</div>
<div class="card">Card 2</div>
```

### 8. How do you create lists in HTML?
**Answer**: Three types of lists:
```html
<!-- Unordered list -->
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>

<!-- Ordered list -->
<ol>
    <li>First item</li>
    <li>Second item</li>
    <li>Third item</li>
</ol>

<!-- Description list -->
<dl>
    <dt>Term 1</dt>
    <dd>Description of term 1</dd>
    <dt>Term 2</dt>
    <dd>Description of term 2</dd>
</dl>
```

### 9. How do you create tables in HTML?
**Answer**: Table structure with semantic elements:
```html
<table>
    <caption>Sales Data</caption>
    <thead>
        <tr>
            <th scope="col">Product</th>
            <th scope="col">Price</th>
            <th scope="col">Quantity</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Laptop</td>
            <td>$999</td>
            <td>5</td>
        </tr>
        <tr>
            <td>Mouse</td>
            <td>$25</td>
            <td>10</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td>Total</td>
            <td colspan="2">$1,249</td>
        </tr>
    </tfoot>
</table>
```

### 10. How do you create forms in HTML?
**Answer**: Form elements and input types:
```html
<form action="/submit" method="POST" enctype="multipart/form-data">
    <fieldset>
        <legend>Personal Information</legend>
        
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        
        <label for="phone">Phone:</label>
        <input type="tel" id="phone" name="phone">
        
        <label for="birthdate">Birth Date:</label>
        <input type="date" id="birthdate" name="birthdate">
        
        <label for="gender">Gender:</label>
        <select id="gender" name="gender">
            <option value="">Select...</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
        </select>
        
        <label for="bio">Bio:</label>
        <textarea id="bio" name="bio" rows="4" cols="50"></textarea>
        
        <input type="checkbox" id="newsletter" name="newsletter" value="yes">
        <label for="newsletter">Subscribe to newsletter</label>
        
        <input type="submit" value="Submit">
        <input type="reset" value="Reset">
    </fieldset>
</form>
```

## Semantic HTML & Accessibility (11-20)

### 11. What are semantic HTML elements and why are they important?
**Answer**: Elements that clearly describe their meaning:
```html
<!-- Semantic structure -->
<header>
    <nav>
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <header>
            <h1>Article Title</h1>
            <time datetime="2024-01-15">January 15, 2024</time>
        </header>
        <section>
            <h2>Section Title</h2>
            <p>Content...</p>
        </section>
    </article>
    
    <aside>
        <h3>Related Links</h3>
        <ul>...</ul>
    </aside>
</main>

<footer>
    <p>&copy; 2024 Company Name</p>
</footer>
```

**Benefits**:
- Better SEO
- Improved accessibility
- Cleaner code structure
- Better browser support

### 12. How do you make HTML accessible?
**Answer**: Accessibility best practices:
```html
<!-- Use semantic elements -->
<button type="button">Click me</button> <!-- Not <div onclick="..."> -->

<!-- Provide alt text for images -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2">

<!-- Use proper heading hierarchy -->
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>

<!-- Associate labels with form controls -->
<label for="username">Username:</label>
<input type="text" id="username" name="username" required>

<!-- Use ARIA attributes when needed -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" aria-hidden="true">...</ul>

<!-- Provide skip links -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Use proper table headers -->
<table>
    <thead>
        <tr>
            <th scope="col">Name</th>
            <th scope="col">Age</th>
        </tr>
    </thead>
</table>

<!-- Indicate required fields -->
<input type="email" required aria-describedby="email-error">
<div id="email-error" role="alert">Please enter a valid email</div>
```

### 13. What are ARIA attributes and when do you use them?
**Answer**: ARIA (Accessible Rich Internet Applications) attributes enhance accessibility:
```html
<!-- Role attribute -->
<div role="button" tabindex="0">Custom Button</div>
<nav role="navigation">...</nav>

<!-- State attributes -->
<button aria-expanded="true" aria-controls="dropdown">Menu</button>
<div id="dropdown" aria-hidden="false">...</div>

<!-- Property attributes -->
<input type="text" aria-label="Search products" placeholder="Search...">
<div aria-describedby="help-text">Form field</div>
<div id="help-text">Enter your full name</div>

<!-- Live regions -->
<div aria-live="polite" id="status">Status updates appear here</div>
<div aria-live="assertive" id="errors">Error messages appear here</div>

<!-- Landmark roles -->
<div role="banner">Header content</div>
<div role="main">Main content</div>
<div role="complementary">Sidebar content</div>
<div role="contentinfo">Footer content</div>
```

### 14. What is the difference between section, article, and div?
**Answer**:
**`<section>`**: Thematic grouping of content
```html
<section>
    <h2>Products</h2>
    <p>Our product lineup...</p>
</section>
```

**`<article>`**: Self-contained, reusable content
```html
<article>
    <h2>Blog Post Title</h2>
    <p>Blog post content...</p>
</article>
```

**`<div>`**: Generic container with no semantic meaning
```html
<div class="wrapper">
    <div class="column">Layout purposes</div>
</div>
```

### 15. How do you implement proper heading hierarchy?
**Answer**: Logical heading structure:
```html
<!-- Correct hierarchy -->
<h1>Main Page Title</h1>
    <h2>Section 1</h2>
        <h3>Subsection 1.1</h3>
        <h3>Subsection 1.2</h3>
    <h2>Section 2</h2>
        <h3>Subsection 2.1</h3>
            <h4>Sub-subsection 2.1.1</h4>

<!-- Incorrect - skipping levels -->
<h1>Main Title</h1>
<h4>This skips h2 and h3</h4> <!-- Don't do this -->

<!-- Use CSS for styling, not heading level -->
<h2 class="small-heading">Properly structured but styled small</h2>
```

## Advanced HTML Features (21-30)

### 16. What are HTML5 input types and their uses?
**Answer**: Enhanced input types for better UX:
```html
<!-- Text inputs -->
<input type="email" placeholder="user@example.com">
<input type="url" placeholder="https://example.com">
<input type="tel" placeholder="+1-555-123-4567">
<input type="search" placeholder="Search...">

<!-- Numeric inputs -->
<input type="number" min="0" max="100" step="1">
<input type="range" min="0" max="100" value="50">

<!-- Date/time inputs -->
<input type="date">
<input type="time">
<input type="datetime-local">
<input type="month">
<input type="week">

<!-- Other inputs -->
<input type="color" value="#ff0000">
<input type="file" accept="image/*" multiple>
<input type="password" minlength="8">
```

### 17. How do you embed multimedia content in HTML?
**Answer**: Audio, video, and other media:
```html
<!-- Video with multiple sources -->
<video controls width="640" height="480" poster="thumbnail.jpg">
    <source src="video.mp4" type="video/mp4">
    <source src="video.webm" type="video/webm">
    <track kind="subtitles" src="subtitles.vtt" srclang="en" label="English">
    Your browser doesn't support video.
</video>

<!-- Audio with controls -->
<audio controls>
    <source src="audio.mp3" type="audio/mpeg">
    <source src="audio.ogg" type="audio/ogg">
    Your browser doesn't support audio.
</audio>

<!-- Embedded content -->
<iframe src="https://example.com" width="600" height="400" 
        title="External content" sandbox="allow-scripts allow-same-origin">
</iframe>

<!-- Images with responsive support -->
<picture>
    <source media="(min-width: 800px)" srcset="large.jpg">
    <source media="(min-width: 400px)" srcset="medium.jpg">
    <img src="small.jpg" alt="Responsive image">
</picture>
```

### 18. What are data attributes and how do you use them?
**Answer**: Custom attributes for storing data:
```html
<!-- HTML -->
<div data-user-id="123" data-role="admin" data-last-login="2024-01-15">
    User Profile
</div>

<button data-action="delete" data-confirm="Are you sure?">Delete</button>

<!-- JavaScript access -->
<script>
const element = document.querySelector('[data-user-id="123"]');
console.log(element.dataset.userId);     // "123"
console.log(element.dataset.role);       // "admin"
console.log(element.dataset.lastLogin);  // "2024-01-15"

// Setting data attributes
element.dataset.status = 'active';
</script>

<!-- CSS access -->
<style>
[data-role="admin"] {
    border: 2px solid gold;
}

.button::after {
    content: attr(data-confirm);
}
</style>
```

### 19. How do you implement responsive images in HTML?
**Answer**: Multiple techniques for responsive images:
```html
<!-- Using srcset for different resolutions -->
<img src="image-400.jpg" 
     srcset="image-400.jpg 400w, 
             image-800.jpg 800w, 
             image-1200.jpg 1200w"
     sizes="(max-width: 600px) 400px, 
            (max-width: 1000px) 800px, 
            1200px"
     alt="Responsive image">

<!-- Using picture element for art direction -->
<picture>
    <source media="(min-width: 1000px)" srcset="desktop.jpg">
    <source media="(min-width: 600px)" srcset="tablet.jpg">
    <img src="mobile.jpg" alt="Adaptive image">
</picture>

<!-- Different formats with fallback -->
<picture>
    <source srcset="image.avif" type="image/avif">
    <source srcset="image.webp" type="image/webp">
    <img src="image.jpg" alt="Modern format image">
</picture>
```

### 20. What are Web Components and how do you create them?
**Answer**: Custom reusable HTML elements:
```html
<!-- Custom element usage -->
<user-card name="John Doe" email="john@example.com"></user-card>

<script>
class UserCard extends HTMLElement {
    constructor() {
        super();
        
        // Create shadow DOM
        this.attachShadow({ mode: 'open' });
        
        // Define template
        this.shadowRoot.innerHTML = `
            <style>
                .card {
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    padding: 16px;
                    margin: 8px;
                }
                .name {
                    font-weight: bold;
                    font-size: 1.2em;
                }
                .email {
                    color: #666;
                }
            </style>
            <div class="card">
                <div class="name"></div>
                <div class="email"></div>
            </div>
        `;
    }
    
    connectedCallback() {
        this.render();
    }
    
    static get observedAttributes() {
        return ['name', 'email'];
    }
    
    attributeChangedCallback() {
        this.render();
    }
    
    render() {
        const name = this.getAttribute('name') || '';
        const email = this.getAttribute('email') || '';
        
        this.shadowRoot.querySelector('.name').textContent = name;
        this.shadowRoot.querySelector('.email').textContent = email;
    }
}

// Register the custom element
customElements.define('user-card', UserCard);
</script>
```

---

## 📚 Study Guide

### HTML Best Practices
1. **Use semantic elements** for better structure
2. **Validate HTML** using W3C validator
3. **Optimize for accessibility** from the start
4. **Use proper heading hierarchy**
5. **Include alt text** for all images

### Performance Considerations
- Minimize HTTP requests
- Optimize images (format, size, compression)
- Use lazy loading for images
- Minimize DOM depth
- Use efficient selectors

### SEO Best Practices
- Use semantic HTML structure
- Include proper meta tags
- Implement structured data
- Use descriptive URLs
- Optimize page loading speed