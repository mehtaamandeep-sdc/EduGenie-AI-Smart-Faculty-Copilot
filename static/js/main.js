/**
 * EduGenie AI - Main JavaScript
 * Handles UI interactions, API calls, and utility functions
 */

// ============================================================================
// Global Variables
// ============================================================================

let darkMode = localStorage.getItem('darkMode') === 'true';

// ============================================================================
// Initialize on DOM Load
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeDarkMode();
    initializeTooltips();
    initializeAnimations();
});

// ============================================================================
// Dark Mode
// ============================================================================

function initializeDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (darkModeToggle) {
        // Set initial state
        if (darkMode) {
            document.body.classList.add('dark-mode');
            darkModeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
        }
        
        // Toggle dark mode
        darkModeToggle.addEventListener('click', function() {
            darkMode = !darkMode;
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', darkMode);
            
            if (darkMode) {
                darkModeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
            } else {
                darkModeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
            }
        });
    }
}

// ============================================================================
// Loading Overlay
// ============================================================================

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('active');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// ============================================================================
// Toast Notifications
// ============================================================================

function showToast(message, type = 'success') {
    const toastId = type === 'success' ? 'successToast' : 'errorToast';
    const messageId = type === 'success' ? 'successMessage' : 'errorMessage';
    
    const toastElement = document.getElementById(toastId);
    const messageElement = document.getElementById(messageId);
    
    if (toastElement && messageElement) {
        messageElement.textContent = message;
        
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 3000
        });
        
        toast.show();
    }
}

// ============================================================================
// Tooltips
// ============================================================================

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ============================================================================
// Animations
// ============================================================================

function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all feature cards
    const cards = document.querySelectorAll('.feature-card, .agent-card, .stat-card');
    cards.forEach(card => {
        observer.observe(card);
    });
}

// ============================================================================
// API Calls
// ============================================================================

async function generateContent(featureType, formData) {
    try {
        showLoading();
        
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                feature_type: featureType,
                ...formData
            })
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            return {
                success: true,
                content: result.content,
                agent: result.agent_used
            };
        } else {
            throw new Error(result.error || 'Failed to generate content');
        }
    } catch (error) {
        hideLoading();
        throw error;
    }
}

async function sendChatMessage(message) {
    try {
        showLoading();
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            return {
                success: true,
                response: result.response
            };
        } else {
            throw new Error(result.error || 'Failed to get response');
        }
    } catch (error) {
        hideLoading();
        throw error;
    }
}

// ============================================================================
// Form Handling
// ============================================================================

function getFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// ============================================================================
// Content Actions
// ============================================================================

function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text)
            .then(() => {
                showToast('Content copied to clipboard!', 'success');
                return true;
            })
            .catch(err => {
                console.error('Failed to copy:', err);
                fallbackCopyToClipboard(text);
                return false;
            });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('Content copied to clipboard!', 'success');
    } catch (err) {
        showToast('Failed to copy content', 'error');
    }
    
    document.body.removeChild(textArea);
}

function downloadAsFile(content, filename = 'edugenie-document.txt') {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showToast('Content downloaded!', 'success');
}

function printContent(content) {
    const printWindow = window.open('', '', 'height=600,width=800');
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>EduGenie AI - Print</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    line-height: 1.6;
                }
                pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                @media print {
                    body {
                        padding: 0;
                    }
                }
            </style>
        </head>
        <body>
            <pre>${content}</pre>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    
    // Wait for content to load before printing
    setTimeout(() => {
        printWindow.print();
    }, 250);
}

// ============================================================================
// Utility Functions
// ============================================================================

function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(date).toLocaleDateString('en-US', options);
}

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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ============================================================================
// Statistics
// ============================================================================

async function updateStatistics() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update DOM elements if they exist
        const docsCount = document.getElementById('docsCount');
        const chatCount = document.getElementById('chatCount');
        const timeSaved = document.getElementById('timeSaved');
        
        if (docsCount) {
            animateCounter(docsCount, data.documents_generated || 0);
        }
        
        if (chatCount) {
            animateCounter(chatCount, data.chat_messages || 0);
        }
        
        if (timeSaved) {
            const hours = Math.round((data.documents_generated || 0) * 0.5);
            animateCounter(timeSaved, hours);
        }
    } catch (error) {
        console.error('Error updating statistics:', error);
    }
}

function animateCounter(element, target) {
    const duration = 1000;
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// ============================================================================
// Smooth Scroll
// ============================================================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ============================================================================
// Export functions for global use
// ============================================================================

window.EduGenieAI = {
    showLoading,
    hideLoading,
    showToast,
    generateContent,
    sendChatMessage,
    copyToClipboard,
    downloadAsFile,
    printContent,
    updateStatistics,
    formatDate
};

// ============================================================================
// Auto-update statistics on dashboard
// ============================================================================

if (window.location.pathname.includes('dashboard')) {
    updateStatistics();
    // Update every 30 seconds
    setInterval(updateStatistics, 30000);
}

// ============================================================================
// Service Worker Registration (for PWA support - optional)
// ============================================================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable PWA
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(err => console.log('SW registration failed'));
    });
}

// ============================================================================
// Error Handling
// ============================================================================

window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // You can send errors to a logging service here
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // You can send errors to a logging service here
});

// ============================================================================
// Console Welcome Message
// ============================================================================

console.log('%c🎓 EduGenie AI - Smart Faculty Copilot', 'color: #2563eb; font-size: 20px; font-weight: bold;');
console.log('%cPowered by IBM Watsonx.ai Granite Models', 'color: #059669; font-size: 14px;');
console.log('%cMulti-Agent Architecture | Agentic AI', 'color: #7c3aed; font-size: 12px;');

// Made with Bob
