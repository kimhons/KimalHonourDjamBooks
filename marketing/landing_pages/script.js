// Pain Alchemy Landing Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initCountdownTimer();
    initFAQToggle();
    initNewsletterSignup();
    initSmoothScrolling();
    initScrollAnimations();
    initFormValidation();
});

// Countdown Timer
function initCountdownTimer() {
    function updateCountdown() {
        const launchDate = new Date();
        launchDate.setDate(launchDate.getDate() + 25);
        
        const now = new Date();
        const timeLeft = launchDate - now;
        
        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        
        const countdownText = `${days} days, ${hours} hours`;
        
        // Update all countdown elements
        const countdownElements = document.querySelectorAll('#countdown, #countdown-final');
        countdownElements.forEach(element => {
            if (element) {
                element.textContent = countdownText;
            }
        });
    }
    
    // Update immediately and then every minute
    updateCountdown();
    setInterval(updateCountdown, 60000);
}

// FAQ Toggle Functionality
function initFAQToggle() {
    window.toggleFAQ = function(element) {
        const answer = element.nextElementSibling;
        const isActive = element.classList.contains('active');
        
        // Close all FAQ answers
        document.querySelectorAll('.faq-question').forEach(q => {
            q.classList.remove('active');
            q.nextElementSibling.classList.remove('active');
        });
        
        // If this wasn't active, open it
        if (!isActive) {
            element.classList.add('active');
            answer.classList.add('active');
        }
    };
}

// Newsletter Signup
function initNewsletterSignup() {
    const newsletterForms = document.querySelectorAll('.newsletter-form, .footer-newsletter');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const submitButton = this.querySelector('button[type="submit"]');
            const email = emailInput.value.trim();
            
            if (!isValidEmail(email)) {
                showMessage('Please enter a valid email address.', 'error');
                return;
            }
            
            // Disable button and show loading state
            submitButton.disabled = true;
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Subscribing...';
            
            // Simulate API call (replace with actual implementation)
            setTimeout(() => {
                showMessage('Thank you for subscribing! You\'ll receive weekly insights and updates.', 'success');
                emailInput.value = '';
                submitButton.disabled = false;
                submitButton.textContent = originalText;
                
                // Track newsletter signup (replace with actual analytics)
                trackEvent('newsletter_signup', { email: email });
            }, 1500);
        });
    });
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show messages to user
function showMessage(message, type = 'info') {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message-popup');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-popup message-${type}`;
    messageDiv.textContent = message;
    
    // Style the message
    Object.assign(messageDiv.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 25px',
        borderRadius: '10px',
        color: 'white',
        fontWeight: '600',
        zIndex: '1000',
        maxWidth: '400px',
        boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Set background color based on type
    if (type === 'success') {
        messageDiv.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
    } else if (type === 'error') {
        messageDiv.style.background = 'linear-gradient(45deg, #dc3545, #fd7e14)';
    } else {
        messageDiv.style.background = 'linear-gradient(45deg, #ff6b35, #f7931e)';
    }
    
    document.body.appendChild(messageDiv);
    
    // Animate in
    setTimeout(() => {
        messageDiv.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        messageDiv.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 300);
    }, 5000);
}

// Smooth Scrolling
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Add stagger effect for grid items
                if (entry.target.parentElement.classList.contains('value-grid') ||
                    entry.target.parentElement.classList.contains('testimonial-grid') ||
                    entry.target.parentElement.classList.contains('stats-grid')) {
                    
                    const siblings = Array.from(entry.target.parentElement.children);
                    const index = siblings.indexOf(entry.target);
                    entry.target.style.transitionDelay = `${index * 0.1}s`;
                }
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll(`
        .value-card, 
        .incentive-card, 
        .testimonial, 
        .toc-section, 
        .stat-card,
        .faq-item
    `);
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

// Form Validation
function initFormValidation() {
    const emailInputs = document.querySelectorAll('input[type="email"]');
    
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const email = this.value.trim();
            if (email && !isValidEmail(email)) {
                this.style.borderColor = '#dc3545';
                showValidationMessage(this, 'Please enter a valid email address.');
            } else {
                this.style.borderColor = '';
                hideValidationMessage(this);
            }
        });
        
        input.addEventListener('input', function() {
            this.style.borderColor = '';
            hideValidationMessage(this);
        });
    });
}

function showValidationMessage(input, message) {
    hideValidationMessage(input); // Remove existing message
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'validation-message';
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        color: #dc3545;
        font-size: 0.8rem;
        margin-top: 5px;
        display: block;
    `;
    
    input.parentNode.appendChild(messageDiv);
}

function hideValidationMessage(input) {
    const existingMessage = input.parentNode.querySelector('.validation-message');
    if (existingMessage) {
        existingMessage.remove();
    }
}

// Analytics and Tracking
function trackEvent(eventName, properties = {}) {
    // Replace with your actual analytics implementation
    console.log('Event tracked:', eventName, properties);
    
    // Example implementations:
    // Google Analytics 4
    // gtag('event', eventName, properties);
    
    // Facebook Pixel
    // fbq('track', eventName, properties);
    
    // Custom analytics
    // analytics.track(eventName, properties);
}

// Pre-order button tracking
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn-primary') || e.target.closest('.btn-primary')) {
        trackEvent('pre_order_click', {
            button_location: getButtonLocation(e.target),
            page_section: getCurrentSection(e.target)
        });
    }
});

function getButtonLocation(button) {
    if (button.closest('.hero')) return 'hero';
    if (button.closest('.incentives')) return 'incentives';
    if (button.closest('.final-cta')) return 'final-cta';
    return 'other';
}

function getCurrentSection(element) {
    const sections = ['hero', 'value-prop', 'incentives', 'toc', 'author', 'testimonials', 'faq', 'final-cta'];
    
    for (let section of sections) {
        if (element.closest(`.${section}`)) {
            return section;
        }
    }
    return 'unknown';
}

// Scroll progress indicator
function initScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        z-index: 1001;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
        const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = Math.min(scrolled, 100) + '%';
    });
}

// Initialize scroll progress
initScrollProgress();

// Lazy loading for images (if any are added later)
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll events
const optimizedScrollHandler = debounce(function() {
    // Any scroll-based functionality can go here
}, 16); // ~60fps

window.addEventListener('scroll', optimizedScrollHandler);

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // You could send this to your error tracking service
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // You could send this to your error tracking service
});

// Export functions for testing or external use
window.PainAlchemyLanding = {
    trackEvent,
    showMessage,
    isValidEmail
};

