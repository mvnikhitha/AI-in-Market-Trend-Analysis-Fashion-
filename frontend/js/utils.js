// Kalainayam Utility Functions Module
// Common helper functions used across the application

const Utils = (function() {
  
  // Debounce function for event handlers
  function debounce(func, wait = 300) {
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

  // Throttle function for performance-critical handlers
  function throttle(func, limit = 300) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => (inThrottle = false), limit);
      }
    };
  }

  // Format currency
  function formatCurrency(value, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency.toUpperCase(),
    }).format(value);
  }

  // Format percentage
  function formatPercent(value, decimals = 1) {
    return `${parseFloat(value).toFixed(decimals)}%`;
  }

  // Parse query string parameters
  function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    const obj = {};
    for (const [key, value] of params) {
      obj[key] = value;
    }
    return obj;
  }

  // Get query parameter value
  function getQueryParam(key, defaultValue = null) {
    const params = getQueryParams();
    return params[key] || defaultValue;
  }

  // Check if element is in viewport
  function isInViewport(element) {
    if (!element) return false;
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  // Deep clone an object
  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  // Merge objects
  function mergeObjects(target, ...sources) {
    if (!sources.length) return target;
    const source = sources.shift();
    
    if (isObject(target) && isObject(source)) {
      for (const key in source) {
        if (isObject(source[key])) {
          if (!target[key]) Object.assign(target, { [key]: {} });
          mergeObjects(target[key], source[key]);
        } else {
          Object.assign(target, { [key]: source[key] });
        }
      }
    }
    return mergeObjects(target, ...sources);
  }

  function isObject(item) {
    return item && typeof item === 'object' && !Array.isArray(item);
  }

  // Validate email
  function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }

  // Validate URL
  function isValidURL(url) {
    try {
      new URL(url);
      return true;
    } catch (_) {
      return false;
    }
  }

  // Generate unique ID
  function generateId(prefix = 'id') {
    return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // Truncate text
  function truncate(text, length = 100, suffix = '...') {
    if (!text) return '';
    if (text.length <= length) return text;
    return text.substring(0, length - suffix.length) + suffix;
  }

  // Capitalize first letter
  function capitalize(text) {
    if (!text) return '';
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
  }

  // Capitalize all words
  function titleCase(text) {
    if (!text) return '';
    return text
      .split(' ')
      .map(word => capitalize(word))
      .join(' ');
  }

  // Delay promise
  function delay(ms = 1000) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Retry promise with exponential backoff
  async function retry(fn, maxAttempts = 3, delayMs = 1000) {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        return await fn();
      } catch (error) {
        if (i === maxAttempts - 1) throw error;
        await delay(delayMs * Math.pow(2, i));
      }
    }
  }

  // Local storage helpers
  const storage = {
    set: (key, value) => {
      try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
      } catch (e) {
        console.error('Storage set error:', e);
        return false;
      }
    },
    get: (key, defaultValue = null) => {
      try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
      } catch (e) {
        console.error('Storage get error:', e);
        return defaultValue;
      }
    },
    remove: (key) => {
      try {
        localStorage.removeItem(key);
        return true;
      } catch (e) {
        console.error('Storage remove error:', e);
        return false;
      }
    },
    clear: () => {
      try {
        localStorage.clear();
        return true;
      } catch (e) {
        console.error('Storage clear error:', e);
        return false;
      }
    },
  };

  return {
    debounce,
    throttle,
    formatCurrency,
    formatPercent,
    getQueryParams,
    getQueryParam,
    isInViewport,
    deepClone,
    mergeObjects,
    isValidEmail,
    isValidURL,
    generateId,
    truncate,
    capitalize,
    titleCase,
    delay,
    retry,
    storage,
  };
})();

// Export for use in modules if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Utils;
}
