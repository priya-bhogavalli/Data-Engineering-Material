# jQuery - Key Concepts

## Overview
jQuery is a fast, lightweight JavaScript library that simplifies HTML document manipulation, event handling, animation, and Ajax interactions.

## Core Concepts

### jQuery Object
- **$()**: jQuery function/selector
- **DOM Wrapping**: Wraps DOM elements
- **Method Chaining**: Fluent interface
- **Implicit Iteration**: Operates on all matched elements
- **jQuery vs DOM**: Differences in objects

### Selectors
- **CSS Selectors**: Standard CSS syntax
- **jQuery Extensions**: :first, :last, :even, :odd
- **Attribute Selectors**: [attribute=value]
- **Form Selectors**: :input, :checked, :selected
- **Hierarchy**: parent > child, ancestor descendant

## DOM Manipulation

### Content Methods
- **text()**: Get/set text content
- **html()**: Get/set HTML content
- **val()**: Get/set form values
- **attr()**: Get/set attributes
- **prop()**: Get/set properties

### Structure Methods
- **append/prepend**: Add content inside
- **after/before**: Add content outside
- **wrap/unwrap**: Wrap elements
- **clone()**: Copy elements
- **remove/detach**: Remove elements

### CSS & Styling
- **css()**: Get/set CSS properties
- **addClass/removeClass**: Manage classes
- **toggleClass**: Toggle class presence
- **hasClass**: Check class existence
- **show/hide**: Visibility control

## Event Handling

### Event Methods
- **on()**: Attach event handlers
- **off()**: Remove event handlers
- **one()**: One-time event handlers
- **trigger()**: Manually trigger events
- **Event delegation**: Handle dynamic content

### Common Events
- **click/dblclick**: Mouse clicks
- **mouseenter/mouseleave**: Mouse hover
- **keydown/keyup**: Keyboard events
- **submit**: Form submission
- **ready**: Document ready

### Event Object
- **preventDefault()**: Stop default behavior
- **stopPropagation()**: Stop event bubbling
- **target**: Event target element
- **which**: Key/button codes
- **pageX/pageY**: Mouse coordinates

## Effects & Animation

### Basic Effects
- **show/hide**: Visibility with animation
- **fadeIn/fadeOut**: Fade effects
- **slideUp/slideDown**: Slide effects
- **toggle**: Toggle visibility
- **Duration**: Animation timing

### Custom Animation
- **animate()**: Custom property animation
- **stop()**: Stop animations
- **delay()**: Add delays
- **queue()**: Animation queuing
- **Easing**: Animation curves

## Ajax

### Ajax Methods
- **$.ajax()**: Full Ajax control
- **$.get/$.post**: Simplified requests
- **load()**: Load content into elements
- **$.getJSON**: JSON data retrieval
- **$.getScript**: Dynamic script loading

### Ajax Configuration
- **url**: Request URL
- **type/method**: HTTP method
- **data**: Request data
- **dataType**: Expected response type
- **success/error**: Callback functions

## Utilities

### Utility Functions
- **$.each()**: Iterate over objects/arrays
- **$.map()**: Transform arrays
- **$.grep()**: Filter arrays
- **$.extend()**: Merge objects
- **$.isArray/$.isFunction**: Type checking

### Deferred Objects
- **$.Deferred()**: Promise-like objects
- **done/fail/always**: Callback registration
- **resolve/reject**: State changes
- **when()**: Multiple deferreds
- **Promise interface**: ES6-like promises

## Best Practices
- **Document Ready**: Wait for DOM
- **Event Delegation**: Handle dynamic content
- **Method Chaining**: Efficient operations
- **Performance**: Optimize selectors
- **Modern Alternatives**: Consider vanilla JS/frameworks