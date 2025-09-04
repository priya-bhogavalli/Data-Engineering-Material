# CSS Interview Questions for Data Engineering

## 📋 Table of Contents
1. [CSS Fundamentals](#css-fundamentals)
2. [Layout & Positioning](#layout--positioning)
3. [Responsive Design](#responsive-design)
4. [Data Visualization Styling](#data-visualization-styling)
5. [Dashboard Design](#dashboard-design)
6. [Performance & Optimization](#performance--optimization)
7. [CSS Frameworks](#css-frameworks)
8. [Advanced CSS](#advanced-css)

---

## CSS Fundamentals

### Q1: What is CSS and how does it relate to data visualization?
**Answer:**
CSS (Cascading Style Sheets) is used to style HTML elements and is crucial for data engineering in:
- **Dashboard styling**: Creating professional-looking data dashboards
- **Report formatting**: Styling data reports and tables
- **Data visualization**: Enhancing charts and graphs appearance
- **Responsive design**: Making data displays work across devices
- **User experience**: Improving readability of data presentations

### Q2: Explain the CSS box model
**Answer:**
```css
/* Box model components */
.data-container {
    width: 300px;           /* Content width */
    height: 200px;          /* Content height */
    padding: 20px;          /* Space inside border */
    border: 2px solid #333; /* Border around element */
    margin: 10px;           /* Space outside border */
}

/* Total width = width + padding + border + margin */
/* Total width = 300 + 40 + 4 + 20 = 364px */

/* Box-sizing alternative */
.modern-container {
    box-sizing: border-box; /* Includes padding and border in width */
    width: 300px;           /* Total width including padding/border */
    padding: 20px;
    border: 2px solid #333;
}
```

### Q3: What are CSS selectors and their specificity?
**Answer:**
```css
/* Specificity (highest to lowest) */

/* 1. Inline styles (1000) */
<div style="color: red;">High specificity</div>

/* 2. IDs (100) */
#dashboard-header { color: blue; }

/* 3. Classes, attributes, pseudo-classes (10) */
.data-table { color: green; }
[data-type="chart"] { color: purple; }
:hover { color: orange; }

/* 4. Elements and pseudo-elements (1) */
table { color: black; }
::before { content: "→"; }

/* Specificity calculation examples */
#main .data-table td     /* 100 + 10 + 1 = 111 */
.dashboard .chart.active /* 10 + 10 + 10 = 30 */
table tr td             /* 1 + 1 + 1 = 3 */
```

---

## Layout & Positioning

### Q4: Compare Flexbox vs Grid for dashboard layouts
**Answer:**
```css
/* Flexbox - One-dimensional layout */
.dashboard-header {
    display: flex;
    justify-content: space-between; /* Distribute items */
    align-items: center;           /* Center vertically */
    gap: 20px;                     /* Space between items */
}

.metric-cards {
    display: flex;
    flex-wrap: wrap;               /* Allow wrapping */
    gap: 15px;
}

.metric-card {
    flex: 1 1 250px;              /* Grow, shrink, basis */
    min-width: 250px;
}

/* Grid - Two-dimensional layout */
.dashboard-layout {
    display: grid;
    grid-template-columns: 250px 1fr 300px; /* Sidebar, main, aside */
    grid-template-rows: 60px 1fr 40px;      /* Header, content, footer */
    grid-template-areas: 
        "sidebar header  aside"
        "sidebar main    aside"
        "sidebar footer  aside";
    gap: 20px;
    height: 100vh;
}

.sidebar { grid-area: sidebar; }
.header  { grid-area: header; }
.main    { grid-area: main; }
.aside   { grid-area: aside; }
.footer  { grid-area: footer; }

/* Responsive grid */
.chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}
```

### Q5: How do you create responsive data tables?
**Answer:**
```css
/* Basic responsive table */
.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

.data-table th,
.data-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.data-table th {
    background-color: #f5f5f5;
    font-weight: 600;
    position: sticky;  /* Sticky header */
    top: 0;
    z-index: 10;
}

/* Mobile-first responsive approach */
@media (max-width: 768px) {
    .data-table {
        font-size: 14px;
    }
    
    /* Hide less important columns on mobile */
    .data-table .optional-column {
        display: none;
    }
    
    /* Stack table for very small screens */
    .data-table,
    .data-table thead,
    .data-table tbody,
    .data-table th,
    .data-table td,
    .data-table tr {
        display: block;
    }
    
    .data-table tr {
        border: 1px solid #ccc;
        margin-bottom: 10px;
        padding: 10px;
    }
    
    .data-table td {
        border: none;
        position: relative;
        padding-left: 50%;
    }
    
    .data-table td:before {
        content: attr(data-label) ": ";
        position: absolute;
        left: 6px;
        width: 45%;
        font-weight: bold;
    }
}

/* Horizontal scroll for wide tables */
.table-container {
    overflow-x: auto;
    margin: 20px 0;
}

.table-container::-webkit-scrollbar {
    height: 8px;
}

.table-container::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.table-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}
```

---

## Responsive Design

### Q6: How do you implement responsive design for data dashboards?
**Answer:**
```css
/* Mobile-first approach */
.dashboard {
    padding: 10px;
}

.metric-grid {
    display: grid;
    grid-template-columns: 1fr;  /* Single column on mobile */
    gap: 15px;
}

/* Tablet styles */
@media (min-width: 768px) {
    .dashboard {
        padding: 20px;
    }
    
    .metric-grid {
        grid-template-columns: repeat(2, 1fr); /* Two columns */
        gap: 20px;
    }
}

/* Desktop styles */
@media (min-width: 1024px) {
    .dashboard {
        padding: 30px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .metric-grid {
        grid-template-columns: repeat(4, 1fr); /* Four columns */
        gap: 25px;
    }
}

/* Large desktop */
@media (min-width: 1440px) {
    .metric-grid {
        grid-template-columns: repeat(6, 1fr); /* Six columns */
    }
}

/* Container queries (modern approach) */
.chart-container {
    container-type: inline-size;
}

@container (min-width: 400px) {
    .chart {
        display: flex;
        flex-direction: row;
    }
}

@container (min-width: 600px) {
    .chart {
        grid-template-columns: 1fr 2fr;
    }
}
```

### Q7: How do you handle different screen densities and devices?
**Answer:**
```css
/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2),
       (min-resolution: 192dpi) {
    .chart-icon {
        background-image: url('chart-icon@2x.png');
        background-size: 24px 24px;
    }
}

/* Touch-friendly design */
@media (hover: none) and (pointer: coarse) {
    .interactive-element {
        min-height: 44px;  /* Minimum touch target */
        min-width: 44px;
        padding: 12px;
    }
    
    .tooltip {
        display: none;     /* Hide hover tooltips on touch */
    }
}

/* Print styles for reports */
@media print {
    .dashboard {
        background: white;
        color: black;
    }
    
    .no-print {
        display: none;
    }
    
    .chart {
        break-inside: avoid;  /* Avoid page breaks in charts */
        margin-bottom: 20px;
    }
    
    .data-table {
        font-size: 12px;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .dashboard {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .data-table {
        background-color: #2d2d2d;
        border-color: #444;
    }
}
```

---

## Data Visualization Styling

### Q8: How do you style charts and graphs with CSS?
**Answer:**
```css
/* SVG chart styling */
.chart-container {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart svg {
    width: 100%;
    height: auto;
    max-height: 400px;
}

/* Bar chart styles */
.bar-chart .bar {
    fill: #3498db;
    transition: fill 0.3s ease;
}

.bar-chart .bar:hover {
    fill: #2980b9;
    cursor: pointer;
}

.bar-chart .bar.selected {
    fill: #e74c3c;
}

/* Line chart styles */
.line-chart .line {
    fill: none;
    stroke: #2ecc71;
    stroke-width: 2px;
    stroke-linecap: round;
}

.line-chart .dot {
    fill: #2ecc71;
    stroke: white;
    stroke-width: 2px;
    r: 4px;
}

.line-chart .dot:hover {
    r: 6px;
    fill: #27ae60;
}

/* Pie chart styles */
.pie-chart .slice {
    stroke: white;
    stroke-width: 2px;
    transition: transform 0.3s ease;
}

.pie-chart .slice:hover {
    transform: scale(1.05);
    transform-origin: center;
}

/* Chart axes and labels */
.chart .axis {
    stroke: #666;
    stroke-width: 1px;
}

.chart .axis text {
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    fill: #666;
}

.chart .grid-line {
    stroke: #e0e0e0;
    stroke-width: 1px;
    stroke-dasharray: 2,2;
}

/* Legend styling */
.chart-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 15px;
    justify-content: center;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 14px;
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
}
```

### Q9: How do you create animated data visualizations?
**Answer:**
```css
/* Loading animations */
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

.chart-loading {
    animation: pulse 1.5s ease-in-out infinite;
}

/* Data update animations */
@keyframes slideIn {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.new-data-point {
    animation: slideIn 0.5s ease-out;
}

/* Bar growth animation */
@keyframes growBar {
    from {
        transform: scaleY(0);
        transform-origin: bottom;
    }
    to {
        transform: scaleY(1);
        transform-origin: bottom;
    }
}

.bar-chart .bar {
    animation: growBar 0.8s ease-out;
    animation-delay: calc(var(--index) * 0.1s);
}

/* Number counter animation */
@keyframes countUp {
    from { --num: 0; }
    to { --num: var(--target); }
}

.metric-value {
    animation: countUp 2s ease-out;
    counter-reset: num var(--num);
}

.metric-value::after {
    content: counter(num);
}

/* Hover effects */
.interactive-chart .element {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interactive-chart .element:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Progress indicators */
@keyframes progress {
    0% { width: 0%; }
    100% { width: var(--progress); }
}

.progress-bar {
    height: 8px;
    background: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3498db, #2ecc71);
    animation: progress 1.5s ease-out;
}
```

---

## Dashboard Design

### Q10: How do you create a professional dashboard layout?
**Answer:**
```css
/* Dashboard container */
.dashboard {
    min-height: 100vh;
    background: #f8f9fa;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header */
.dashboard-header {
    background: white;
    border-bottom: 1px solid #e9ecef;
    padding: 0 24px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.dashboard-title {
    font-size: 20px;
    font-weight: 600;
    color: #212529;
    margin: 0;
}

/* Sidebar */
.dashboard-sidebar {
    width: 280px;
    background: white;
    border-right: 1px solid #e9ecef;
    height: calc(100vh - 64px);
    position: fixed;
    left: 0;
    top: 64px;
    overflow-y: auto;
    padding: 24px 0;
}

.sidebar-nav {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar-nav li {
    margin: 4px 16px;
}

.sidebar-nav a {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    color: #6c757d;
    text-decoration: none;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
    background: #e3f2fd;
    color: #1976d2;
}

/* Main content */
.dashboard-main {
    margin-left: 280px;
    padding: 24px;
}

/* Widget grid */
.widget-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
    margin-bottom: 24px;
}

/* Widget card */
.widget {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
    transition: box-shadow 0.2s ease;
}

.widget:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.widget-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.widget-title {
    font-size: 16px;
    font-weight: 600;
    color: #212529;
    margin: 0;
}

.widget-actions {
    display: flex;
    gap: 8px;
}

.widget-action {
    padding: 6px;
    border: none;
    background: none;
    color: #6c757d;
    cursor: pointer;
    border-radius: 4px;
    transition: background 0.2s ease;
}

.widget-action:hover {
    background: #f8f9fa;
}
```

### Q11: How do you implement a responsive navigation menu?
**Answer:**
```css
/* Desktop navigation */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    height: 64px;
    background: white;
    border-bottom: 1px solid #e9ecef;
}

.navbar-brand {
    font-size: 20px;
    font-weight: 700;
    color: #212529;
    text-decoration: none;
}

.navbar-nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 8px;
}

.navbar-nav a {
    padding: 8px 16px;
    color: #6c757d;
    text-decoration: none;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.navbar-nav a:hover,
.navbar-nav a.active {
    background: #e3f2fd;
    color: #1976d2;
}

/* Mobile menu toggle */
.navbar-toggle {
    display: none;
    flex-direction: column;
    gap: 4px;
    padding: 8px;
    background: none;
    border: none;
    cursor: pointer;
}

.navbar-toggle span {
    width: 24px;
    height: 2px;
    background: #212529;
    transition: all 0.3s ease;
}

/* Mobile styles */
@media (max-width: 768px) {
    .navbar-nav {
        position: fixed;
        top: 64px;
        left: -100%;
        width: 100%;
        height: calc(100vh - 64px);
        background: white;
        flex-direction: column;
        padding: 24px;
        transition: left 0.3s ease;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    .navbar-nav.active {
        left: 0;
    }
    
    .navbar-toggle {
        display: flex;
    }
    
    .navbar-toggle.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .navbar-toggle.active span:nth-child(2) {
        opacity: 0;
    }
    
    .navbar-toggle.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }
    
    .navbar-nav a {
        padding: 16px 0;
        border-bottom: 1px solid #e9ecef;
    }
}
```

---

## Performance & Optimization

### Q12: How do you optimize CSS for large dashboards?
**Answer:**
```css
/* Critical CSS - inline in HTML head */
.dashboard-critical {
    font-family: system-ui, -apple-system, sans-serif;
    margin: 0;
    padding: 0;
    background: #f8f9fa;
}

/* Use CSS custom properties for theming */
:root {
    --primary-color: #1976d2;
    --secondary-color: #424242;
    --success-color: #2e7d32;
    --warning-color: #f57c00;
    --error-color: #d32f2f;
    --background-color: #f8f9fa;
    --surface-color: #ffffff;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #e9ecef;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
    --border-radius: 8px;
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
}

/* Efficient selectors - avoid deep nesting */
.widget { /* Good - single class */ }
.widget-header { /* Good - BEM methodology */ }
.widget__title--large { /* Good - specific class */ }

/* Avoid */
.dashboard .content .widget .header h3 { /* Bad - too specific */ }

/* Use transform and opacity for animations (GPU accelerated) */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Efficient grid layouts */
.efficient-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    /* Avoid complex calculations */
}

/* Use will-change for elements that will animate */
.animated-chart {
    will-change: transform, opacity;
}

.animated-chart.complete {
    will-change: auto; /* Remove when animation complete */
}

/* Optimize images and icons */
.icon {
    width: 24px;
    height: 24px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}

/* Use CSS containment for isolated components */
.widget {
    contain: layout style paint;
}

/* Efficient media queries */
@media (min-width: 768px) {
    .responsive-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .responsive-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

### Q13: How do you implement CSS-in-JS for dynamic styling?
**Answer:**
```css
/* CSS Custom Properties for dynamic values */
.dynamic-chart {
    --data-value: 75;
    --max-value: 100;
    --percentage: calc(var(--data-value) / var(--max-value) * 100%);
    --color: hsl(calc(var(--data-value) * 1.2), 70%, 50%);
}

.progress-bar {
    width: var(--percentage);
    background-color: var(--color);
    transition: width 0.5s ease, background-color 0.3s ease;
}

/* Data attributes for styling */
[data-status="success"] {
    color: var(--success-color);
    background-color: rgba(46, 125, 50, 0.1);
}

[data-status="warning"] {
    color: var(--warning-color);
    background-color: rgba(245, 124, 0, 0.1);
}

[data-status="error"] {
    color: var(--error-color);
    background-color: rgba(211, 47, 47, 0.1);
}

/* Conditional styling with CSS */
.metric-card {
    border-left: 4px solid var(--border-color);
}

.metric-card[data-trend="up"] {
    border-left-color: var(--success-color);
}

.metric-card[data-trend="down"] {
    border-left-color: var(--error-color);
}

.metric-card[data-trend="stable"] {
    border-left-color: var(--warning-color);
}

/* Theme switching */
[data-theme="dark"] {
    --background-color: #121212;
    --surface-color: #1e1e1e;
    --text-primary: #ffffff;
    --text-secondary: #b3b3b3;
    --border-color: #333333;
}

/* Component state styling */
.button {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.2s ease;
}

.button:hover {
    background: color-mix(in srgb, var(--primary-color) 90%, black);
    transform: translateY(-1px);
}

.button:active {
    transform: translateY(0);
}

.button[disabled] {
    background: var(--text-secondary);
    cursor: not-allowed;
    transform: none;
}
```

---

## CSS Frameworks

### Q14: How do you customize Bootstrap for data dashboards?
**Answer:**
```css
/* Custom Bootstrap variables */
:root {
    --bs-primary: #1976d2;
    --bs-secondary: #424242;
    --bs-success: #2e7d32;
    --bs-info: #0288d1;
    --bs-warning: #f57c00;
    --bs-danger: #d32f2f;
    --bs-light: #f8f9fa;
    --bs-dark: #212529;
    --bs-font-family-base: 'Inter', system-ui, sans-serif;
    --bs-border-radius: 8px;
    --bs-box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Custom dashboard components */
.dashboard-card {
    @extend .card;
    border: none;
    box-shadow: var(--bs-box-shadow);
    transition: box-shadow 0.2s ease;
}

.dashboard-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.metric-card {
    @extend .dashboard-card;
    text-align: center;
    padding: 2rem;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--bs-primary);
    margin-bottom: 0.5rem;
}

.metric-label {
    color: var(--bs-secondary);
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Custom table styling */
.data-table {
    @extend .table, .table-hover, .table-responsive;
}

.data-table th {
    background-color: var(--bs-light);
    border-top: none;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    color: var(--bs-secondary);
}

/* Custom button variants */
.btn-outline-custom {
    color: var(--bs-primary);
    border-color: var(--bs-primary);
    background: transparent;
}

.btn-outline-custom:hover {
    background: var(--bs-primary);
    border-color: var(--bs-primary);
    color: white;
}

/* Utility classes */
.shadow-custom {
    box-shadow: var(--bs-box-shadow) !important;
}

.rounded-custom {
    border-radius: var(--bs-border-radius) !important;
}

.text-muted-custom {
    color: var(--bs-secondary) !important;
}
```

### Q15: How do you use Tailwind CSS for rapid dashboard development?
**Answer:**
```css
/* Tailwind configuration for dashboards */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e3f2fd',
          500: '#1976d2',
          600: '#1565c0',
          700: '#0d47a1',
        },
        gray: {
          50: '#f8f9fa',
          100: '#f1f3f4',
          200: '#e8eaed',
          300: '#dadce0',
          400: '#bdc1c6',
          500: '#9aa0a6',
          600: '#80868b',
          700: '#5f6368',
          800: '#3c4043',
          900: '#202124',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      }
    }
  }
}

/* Custom component classes */
@layer components {
  .dashboard-card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200;
  }
  
  .metric-card {
    @apply dashboard-card text-center;
  }
  
  .metric-value {
    @apply text-3xl font-bold text-primary-600 mb-2;
  }
  
  .metric-label {
    @apply text-sm text-gray-500 uppercase tracking-wide;
  }
  
  .data-table {
    @apply w-full border-collapse;
  }
  
  .data-table th {
    @apply bg-gray-50 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200;
  }
  
  .data-table td {
    @apply px-4 py-3 text-sm text-gray-900 border-b border-gray-200;
  }
  
  .btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200;
  }
  
  .btn-secondary {
    @apply bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors duration-200;
  }
}

/* Utility classes */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
  
  .scrollbar-thin {
    scrollbar-width: thin;
  }
  
  .scrollbar-thin::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  
  .scrollbar-thin::-webkit-scrollbar-track {
    @apply bg-gray-100;
  }
  
  .scrollbar-thin::-webkit-scrollbar-thumb {
    @apply bg-gray-300 rounded-full;
  }
}
```

---

## Advanced CSS

### Q16: How do you implement CSS Grid for complex dashboard layouts?
**Answer:**
```css
/* Complex dashboard grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: 
        [sidebar-start] 280px 
        [sidebar-end main-start] 1fr 
        [main-end aside-start] 320px 
        [aside-end];
    grid-template-rows: 
        [header-start] 64px 
        [header-end content-start] 1fr 
        [content-end footer-start] 40px 
        [footer-end];
    grid-template-areas:
        "sidebar header  aside"
        "sidebar main    aside"
        "sidebar footer  aside";
    height: 100vh;
    gap: 0;
}

/* Subgrid for nested layouts */
.main-content {
    grid-area: main;
    display: grid;
    grid-template-columns: subgrid;
    grid-template-rows: subgrid;
    gap: 24px;
    padding: 24px;
}

/* Dynamic grid areas */
.widget-large {
    grid-column: span 2;
    grid-row: span 2;
}

.widget-wide {
    grid-column: span 2;
}

.widget-tall {
    grid-row: span 2;
}

/* Responsive grid with container queries */
.chart-container {
    container-type: inline-size;
    display: grid;
    gap: 16px;
}

@container (min-width: 400px) {
    .chart-container {
        grid-template-columns: 1fr 200px;
    }
}

@container (min-width: 600px) {
    .chart-container {
        grid-template-columns: 1fr 1fr;
    }
}

/* Grid with auto-placement */
.masonry-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    grid-auto-rows: min-content;
    gap: 20px;
    align-items: start;
}

/* Dense packing for varied sizes */
.dense-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    grid-auto-flow: row dense;
    gap: 16px;
}
```

### Q17: How do you implement advanced CSS animations for data updates?
**Answer:**
```css
/* Keyframe animations */
@keyframes dataUpdate {
    0% {
        transform: scale(1);
        background-color: var(--surface-color);
    }
    50% {
        transform: scale(1.05);
        background-color: var(--success-color);
        box-shadow: 0 0 20px rgba(46, 125, 50, 0.3);
    }
    100% {
        transform: scale(1);
        background-color: var(--surface-color);
    }
}

@keyframes numberCount {
    from {
        --progress: 0;
    }
    to {
        --progress: var(--target);
    }
}

@keyframes chartGrow {
    from {
        clip-path: inset(100% 0 0 0);
    }
    to {
        clip-path: inset(0 0 0 0);
    }
}

/* Animation classes */
.data-updated {
    animation: dataUpdate 1s ease-in-out;
}

.counter {
    animation: numberCount 2s ease-out;
    counter-reset: num var(--progress);
}

.counter::after {
    content: counter(num);
}

.chart-animate {
    animation: chartGrow 1.5s ease-out;
}

/* Staggered animations */
.stagger-item {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out forwards;
    animation-delay: calc(var(--index) * 0.1s);
}

@keyframes fadeInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Morphing shapes */
.morphing-chart {
    transition: d 0.5s ease-in-out;
}

/* Loading states */
@keyframes skeleton {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200px 100%;
    animation: skeleton 1.5s infinite;
}

/* Hover animations */
.interactive-element {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: center;
}

.interactive-element:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* Scroll-triggered animations */
@keyframes slideInFromLeft {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.scroll-animate {
    opacity: 0;
    transform: translateX(-100%);
}

.scroll-animate.in-view {
    animation: slideInFromLeft 0.8s ease-out forwards;
}
```

### Q18: How do you implement CSS custom properties for theming?
**Answer:**
```css
/* Base theme system */
:root {
    /* Color palette */
    --color-primary-h: 210;
    --color-primary-s: 79%;
    --color-primary-l: 46%;
    --color-primary: hsl(var(--color-primary-h), var(--color-primary-s), var(--color-primary-l));
    --color-primary-light: hsl(var(--color-primary-h), var(--color-primary-s), calc(var(--color-primary-l) + 20%));
    --color-primary-dark: hsl(var(--color-primary-h), var(--color-primary-s), calc(var(--color-primary-l) - 20%));
    
    /* Semantic colors */
    --color-success: hsl(122, 39%, 49%);
    --color-warning: hsl(35, 91%, 62%);
    --color-error: hsl(354, 70%, 54%);
    --color-info: hsl(188, 78%, 41%);
    
    /* Neutral colors */
    --color-gray-50: hsl(210, 20%, 98%);
    --color-gray-100: hsl(220, 14%, 96%);
    --color-gray-200: hsl(220, 13%, 91%);
    --color-gray-300: hsl(216, 12%, 84%);
    --color-gray-400: hsl(218, 11%, 65%);
    --color-gray-500: hsl(220, 9%, 46%);
    --color-gray-600: hsl(215, 14%, 34%);
    --color-gray-700: hsl(217, 19%, 27%);
    --color-gray-800: hsl(215, 28%, 17%);
    --color-gray-900: hsl(221, 39%, 11%);
    
    /* Typography */
    --font-family-base: 'Inter', system-ui, -apple-system, sans-serif;
    --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 1.875rem;
    --font-size-4xl: 2.25rem;
    
    /* Spacing */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;
    --space-12: 3rem;
    --space-16: 4rem;
    --space-20: 5rem;
    
    /* Layout */
    --border-radius-sm: 0.25rem;
    --border-radius: 0.5rem;
    --border-radius-lg: 0.75rem;
    --border-radius-xl: 1rem;
    --border-width: 1px;
    --border-width-2: 2px;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
    --transition-slow: 350ms ease;
}

/* Dark theme */
[data-theme="dark"] {
    --color-gray-50: hsl(221, 39%, 11%);
    --color-gray-100: hsl(217, 19%, 27%);
    --color-gray-200: hsl(215, 28%, 17%);
    --color-gray-300: hsl(215, 14%, 34%);
    --color-gray-400: hsl(220, 9%, 46%);
    --color-gray-500: hsl(218, 11%, 65%);
    --color-gray-600: hsl(216, 12%, 84%);
    --color-gray-700: hsl(220, 13%, 91%);
    --color-gray-800: hsl(220, 14%, 96%);
    --color-gray-900: hsl(210, 20%, 98%);
    
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
}

/* High contrast theme */
[data-theme="high-contrast"] {
    --color-primary: #0000ff;
    --color-gray-900: #000000;
    --color-gray-50: #ffffff;
    --border-width: 2px;
    --shadow: none;
}

/* Theme-aware components */
.dashboard {
    background-color: var(--color-gray-50);
    color: var(--color-gray-900);
    font-family: var(--font-family-base);
    transition: background-color var(--transition-base), color var(--transition-base);
}

.card {
    background-color: var(--color-gray-50);
    border: var(--border-width) solid var(--color-gray-200);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow);
    padding: var(--space-6);
    transition: all var(--transition-base);
}

.button {
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    padding: var(--space-3) var(--space-6);
    font-size: var(--font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.button:hover {
    background-color: var(--color-primary-dark);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Dynamic color generation */
.status-indicator {
    --hue: var(--status-hue, 0);
    --saturation: var(--status-saturation, 70%);
    --lightness: var(--status-lightness, 50%);
    
    background-color: hsl(var(--hue), var(--saturation), var(--lightness));
    color: hsl(var(--hue), var(--saturation), calc(var(--lightness) - 40%));
    border: 1px solid hsl(var(--hue), var(--saturation), calc(var(--lightness) - 20%));
}

/* Usage with JavaScript */
.metric-card[data-value] {
    --progress: attr(data-value number, 0);
    --color-hue: calc(var(--progress) * 1.2); /* Green to red based on value */
    border-left: 4px solid hsl(var(--color-hue), 70%, 50%);
}
```

---

## 🎯 Key Takeaways

### **Essential CSS Concepts for Data Engineering:**
1. **Responsive Design** - Dashboards must work on all devices
2. **Grid & Flexbox** - Essential for complex dashboard layouts
3. **CSS Custom Properties** - Enable dynamic theming and styling
4. **Performance Optimization** - Critical for large-scale applications
5. **Animation & Transitions** - Enhance user experience with data updates
6. **Component-based Styling** - Maintainable and scalable CSS architecture

### **Best Practices:**
- Use mobile-first responsive design
- Implement CSS custom properties for theming
- Optimize for performance with efficient selectors
- Use CSS Grid for complex layouts, Flexbox for components
- Implement proper accessibility with focus states and contrast
- Use CSS frameworks wisely - customize for your needs

### **Common Patterns:**
- Dashboard grid layouts with sidebar and main content
- Responsive data tables with horizontal scrolling
- Interactive charts with hover effects and animations
- Theme switching with CSS custom properties
- Loading states and skeleton screens
- Progressive enhancement for better performance